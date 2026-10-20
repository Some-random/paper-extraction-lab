#!/usr/bin/env python3
"""Run bounded GPU recipe probes, then independent ten-minute real-data confirmations."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import threading
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/benchmark_gpu_optimized.py"
REGISTRY = ROOT / "experiments/training_throughput_2026-10-18"
MIB = 1024 ** 2
GIB = 1024 ** 3
FEATURES = {
    "attention": {"sdpa_auto", "sdpa_flash", "sdpa_cudnn", "flash_attn4"},
    "kernels": {"none", "liger_loss", "liger_full", "cce"},
    "checkpointing": {"off", "full", "selective"},
    "sharding": {"full_shard", "shard_grad_op", "fsdp2"},
    "compile": {"off", "on"},
    "precision": {"bf16", "float8_tensorwise", "float8_rowwise", "mxfp8", "nvfp4"},
    "float8_all_gather": {"off", "on"},
    "optimizer": {"adamw_fp32", "adamw_8bit"},
}
OPTIONAL_FEATURE_DEFAULTS = {"float8_all_gather": "off", "optimizer": "adamw_fp32"}
FLAGS = {"kernels": "fused-kernels", "checkpointing": "activation-checkpointing",
         "float8_all_gather": "float8-all-gather"}
ARGUMENTS = {"kernels": "fused_kernels", "checkpointing": "activation_checkpointing"}
NAME = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$")


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(MIB), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def validate_profiles(config, world_size):
    profiles = config.get("profiles")
    if not isinstance(profiles, list) or not profiles or len(profiles) > 40:
        raise ValueError("A bounded list of one to forty profiles is required")
    names = set()
    for index, profile in enumerate(profiles):
        name, parent = profile.get("name"), profile.get("parent")
        if not isinstance(name, str) or not NAME.fullmatch(name) or name in names:
            raise ValueError("Profile names must be unique safe directory names")
        if index == 0:
            if profile.get("role") != "baseline" or parent is not None:
                raise ValueError("The first profile must be the sole baseline, without a parent")
        elif profile.get("role") not in ("tuning", "combination") or parent not in names | {"@best"}:
            raise ValueError("Tuning profiles must name an earlier parent or @best")
        names.add(name)
        overrides = profile.get("features", {})
        if not isinstance(overrides, dict) or set(overrides) - FEATURES.keys():
            raise ValueError("Unknown feature override")
        if index == 0 and not (FEATURES.keys() - OPTIONAL_FEATURE_DEFAULTS.keys()) <= set(overrides):
            raise ValueError("The baseline must state every feature explicitly")
        for key, value in overrides.items():
            if value not in FEATURES[key] and value != f"@best:{key}":
                raise ValueError(f"Invalid {key} feature")
            if index == 0 and value.startswith("@"):
                raise ValueError("The baseline cannot inherit adaptive settings")
        candidates = profile.get("feature_candidates", {})
        if not isinstance(candidates, dict) or set(candidates) - FEATURES.keys():
            raise ValueError("Unknown adaptive feature candidate field")
        for key, choices in candidates.items():
            if (not isinstance(choices, list) or not choices or len(set(choices)) != len(choices)
                    or any(choice not in names - {name} for choice in choices)):
                raise ValueError("Feature candidates must name distinct earlier profiles")
            if overrides.get(key) != f"@best:{key}":
                raise ValueError("Candidate lists require an explicit adaptive feature override")
        micro, accumulation = profile.get("microbatch_per_gpu"), profile.get("accumulation")
        if not is_positive_int(micro) or not is_positive_int(accumulation):
            raise ValueError("Every profile must state positive microbatch and accumulation")
        if world_size * micro * accumulation != config["global_batch_sequences"]:
            raise ValueError("Every profile must preserve the matched global batch")
        timeout = profile.get("timeout_seconds")
        ceiling = (config["bounds"]["compile_profile_seconds"] if overrides.get("compile") in ("on", "@best:compile")
                   else config["bounds"]["profile_seconds"])
        if timeout is not None and (not is_positive_int(timeout) or timeout > max(ceiling, config["bounds"]["profile_seconds"])):
            raise ValueError("Profile timeout exceeds its approved allowance")
        if profile.get("profile_steps", 0) not in (0, 1):
            raise ValueError("At most one separate profiler step is allowed")
    return profiles


def configuration(args):
    raw = args.config.read_bytes()
    config = json.loads(raw)
    world = {"a100": 8, "b200": 2}[args.gpu_type]
    expected = {"world_size": world, "gpu_type": args.gpu_type, "sequence_length": 4096,
                "global_batch_sequences": 32, "warmup_optimizer_steps": 3,
                "measured_optimizer_steps": 8}
    if args.world_size != world or any(config.get(key) != value for key, value in expected.items()):
        raise ValueError("Sweep requires eight A100s or two B200s, context4096/globalbatch32/warmup3/steps8")
    bounds = config.get("bounds", {})
    ceilings = {"suite_seconds": 6600, "profile_seconds": 420, "compile_profile_seconds": 900,
                "confirmation_profile_seconds": 900, "new_log_bytes": 64 * MIB,
                "new_run_artifact_bytes": 256 * MIB, "new_compile_cache_bytes": 4 * GIB,
                "new_environment_and_artifact_bytes": 16 * GIB}
    for key, ceiling in ceilings.items():
        if not is_positive_int(bounds.get(key)) or bounds[key] > ceiling:
            raise ValueError(f"Invalid or excessive {key} bound")
    reserve = bounds.get("confirmation_reserve_seconds")
    if (not is_positive_int(reserve) or reserve < 2 * bounds["confirmation_profile_seconds"] + 20
            or reserve >= bounds["suite_seconds"]):
        raise ValueError("Reserve two complete confirmation allowances and cleanup before short probes")
    if bounds.get("minimum_free_bytes", 0) < 64 * GIB:
        raise ValueError("Minimum shared free-space floor is 64 GiB")
    baseline = config.get("baseline_environment_and_artifact_bytes")
    if not isinstance(baseline, int) or baseline < 0 or not config.get("baseline_checked_epoch"):
        raise ValueError("A CPU-side footprint preflight is required; no environment walk on GPU")
    confirmation = config.get("confirmations", {})
    if (not is_positive_int(confirmation.get("minimum_measurement_seconds"))
            or confirmation["minimum_measurement_seconds"] < 600
            or confirmation["minimum_measurement_seconds"] >= bounds["confirmation_profile_seconds"] - 30
            or confirmation.get("minimum_optimizer_steps") != 8):
        raise ValueError("Real-data confirmation requires at least600 measured seconds and eight updates")
    for key in ("baseline_name", "winner_name"):
        if not isinstance(confirmation.get(key), str) or not NAME.fullmatch(confirmation[key]):
            raise ValueError("Confirmation names must be safe explicit directory names")
    if confirmation["baseline_name"] == confirmation["winner_name"]:
        raise ValueError("Baseline and winner confirmations must have distinct names")
    paths = {}
    for key in ("model_config", "data_pack", "data_manifest", "environment_preflight"):
        path = (ROOT / config[key]).resolve()
        path.relative_to(ROOT)
        digest = sha256(path)
        if config.get(key + "_sha256") != digest:
            raise ValueError(f"Pinned {key} hash differs")
        paths[key] = path
    if paths["data_pack"].stat().st_size < 64_000_000 * 4 or paths["data_pack"].stat().st_size % 4:
        raise ValueError("A frozen uint32 input pack with at least64M tokens is required before GPU launch")
    preflight = json.loads(paths["environment_preflight"].read_text())
    monitored_packages = {"torch", "transformers", "torchao", "liger-kernel", "cut-cross-entropy", "flash-attn-4", "triton"}
    versions = {name: value.get("version") if isinstance(value, dict) else value
                for name, value in preflight.get("packages", {}).items() if name in monitored_packages}
    if not all(isinstance(versions.get(name), str) for name in ("torch", "transformers")):
        raise ValueError("CPU package preflight must pin torch and transformers versions")
    config["_expected_runtime_packages"] = versions
    runner_sha = sha256(RUNNER)
    if config.get("runner_sha256") != runner_sha:
        raise ValueError("Pinned optimized runner hash differs")
    profiles = validate_profiles(config, args.world_size)
    if any(profile["name"] in (confirmation["baseline_name"], confirmation["winner_name"]) for profile in profiles):
        raise ValueError("Confirmation names must differ from every short probe")
    if args.gpu_type == "a100":
        for profile in profiles:
            features = profile.get("features", {})
            if features.get("attention") == "flash_attn4" or features.get("precision", "bf16") != "bf16":
                raise ValueError("A100 probes must use supported BF16 recipes, without Blackwell-only FA4/FP8")
    binding = dict(config_sha256=hashlib.sha256(raw).hexdigest(), runner_sha256=runner_sha,
                   suite_runner_sha256=sha256(__file__), model_config_sha256=config["model_config_sha256"],
                   data_pack_sha256=config["data_pack_sha256"], data_manifest_sha256=config["data_manifest_sha256"],
                   environment_preflight_sha256=config["environment_preflight_sha256"],
                   mode="gpu_optimization_confirmation", gpu_type=args.gpu_type, world_size=args.world_size,
                   runtime_package_versions=versions,
                   profiles=profiles, confirmations=confirmation)
    return config, paths, binding


def load_state(path, binding, runtime, now):
    if path.exists():
        state = json.loads(path.read_text())
        if state["configuration"] != binding:
            raise ValueError("Saved sweep configuration differs; do not reset its budget")
        return state
    return dict(configuration=binding, started_epoch=now,
                started_utc=datetime.fromtimestamp(now, timezone.utc).isoformat(),
                deadline_epoch=now + runtime, attempted_profiles={}, confirmations={}, status="running",
                stage="short_sweep")


@contextmanager
def suite_lock(directory):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "suite.lock").open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def completed_records(state):
    return [p for p in state["attempted_profiles"].values()
            if p.get("status") == "completed" and p.get("input_tokens_per_second", 0) > 0]


def resolve_profile(profile, selected_profiles, state):
    """Resolve adaptive choices from completed measurements, retaining their origins."""
    by_name = {item["name"]: item for item in selected_profiles}
    completed = completed_records(state)
    best = max(completed, key=lambda item: item["input_tokens_per_second"], default=None)
    parent_name = profile.get("parent")
    if parent_name == "@best":
        parent_name = best["name"] if best else selected_profiles[0]["name"]
    parent = state["attempted_profiles"].get(parent_name)
    if parent is None and parent_name:
        parent = resolve_profile(by_name[parent_name], selected_profiles, state)
    result = dict(profile)
    features = dict(parent["features"]) if parent else dict(OPTIONAL_FEATURE_DEFAULTS)
    sources = {key: parent_name for key in features}
    for key, value in profile.get("features", {}).items():
        if value == f"@best:{key}":
            candidate_names = profile.get("feature_candidates", {}).get(key)
            eligible = ([item for item in completed if item["name"] in candidate_names]
                        if candidate_names is not None else completed)
            source = max(eligible, key=lambda item: item["input_tokens_per_second"], default=None)
            source = source if source else parent
            if source is None:
                raise ValueError("Adaptive feature has no baseline fallback")
            features[key] = source["features"][key]
            sources[key] = source["name"]
        else:
            features[key], sources[key] = value, profile["name"]
    result.update(features=features, resolved_parent=parent_name, feature_sources=sources,
                  changed_features=([key for key in FEATURES if features[key] != parent["features"][key]]
                                    if parent else []), profile_steps=profile.get("profile_steps", 0))
    return result


def tree_sizes(directory):
    """Count only this small job tree, never installed packages or older experiment data."""
    total = logs = cache = 0
    for current, dirs, files in os.walk(directory, followlinks=False):
        dirs[:] = [name for name in dirs if not (Path(current) / name).is_symlink()]
        for name in files:
            try:
                size = (Path(current) / name).lstat().st_size
            except FileNotFoundError:
                continue
            if (Path(current) / name).is_relative_to(directory / "compile_cache"):
                cache += size
            else:
                total += size
                if name.endswith(".log"):
                    logs += size
    return total, logs, cache


def storage_reason(config, directory):
    total, logs, cache = tree_sizes(directory)
    bounds = config["bounds"]
    reserve = 2 * MIB
    if logs >= bounds["new_log_bytes"] - reserve:
        return "new_log_limit"
    if total >= bounds["new_run_artifact_bytes"] - reserve:
        return "new_artifact_limit"
    if cache >= bounds["new_compile_cache_bytes"] - reserve:
        return "compile_cache_limit"
    if config["baseline_environment_and_artifact_bytes"] + total + cache >= bounds["new_environment_and_artifact_bytes"] - reserve:
        return "environment_and_artifact_limit"
    if shutil.disk_usage(directory).free < bounds["minimum_free_bytes"] + reserve:
        return "shared_free_space_floor"
    return None


def child_command(profile, args, config, paths, output, runtime, *, real_data=False):
    command = [sys.executable, "-B", "-u", "-m", "torch.distributed.run", "--standalone",
               "--nnodes=1", f"--nproc_per_node={args.world_size}", "--max-restarts=0",
               str(RUNNER), "--hardware", args.gpu_type, "--model-config", str(paths["model_config"]),
               "--output", str(output), "--sequence-length", str(config["sequence_length"]),
               "--global-batch-sequences", str(config["global_batch_sequences"]),
               "--batch-size", str(profile["microbatch_per_gpu"]), "--accumulation", str(profile["accumulation"]),
               "--warmup", str(config["warmup_optimizer_steps"]),
               "--steps", str(config["confirmations"]["minimum_optimizer_steps"] if real_data
                              else config["measured_optimizer_steps"]),
               "--profile-steps", str(profile.get("profile_steps", 0)),
               "--max-runtime-seconds", str(max(1, math.floor(runtime - 10)))]
    for key in FEATURES:
        command += ["--" + FLAGS.get(key, key), profile["features"][key]]
    if real_data:
        command += ["--input-token-pack", str(paths["data_pack"]),
                    "--input-token-pack-sha256", config["data_pack_sha256"],
                    "--data-manifest", str(paths["data_manifest"]),
                    "--minimum-measured-seconds", str(config["confirmations"]["minimum_measurement_seconds"]),
                    "--maximum-measured-steps", "10000", "--input-start-token", "0"]
    return command


def terminate_owned(process):
    for sig, timeout in ((signal.SIGTERM, 3), (signal.SIGKILL, 2)):
        try:
            os.killpg(process.pid, sig)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            pass
    return process.poll()


def capture_log(source, target, byte_limit, capture):
    """Bound the retained log, while continuously draining a potentially noisy child."""
    retained = discarded = 0
    try:
        while True:
            chunk = source.read1(64 * 1024)
            if not chunk:
                break
            keep = chunk[:max(0, byte_limit - retained)]
            if keep:
                target.write(keep)
                target.flush()
                retained += len(keep)
            discarded += len(chunk) - len(keep)
    except (OSError, ValueError) as error:
        capture["error_type"] = type(error).__name__
    finally:
        capture.update(retained_bytes=retained, discarded_bytes=discarded, truncated=discarded > 0)
        source.close()


def run_process(command, log_path, timeout, guard, cache_directory, *, log_limit=8 * MIB):
    (cache_directory / "tmp").mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="2", MKL_NUM_THREADS="2",
               OPENBLAS_NUM_THREADS="2", TOKENIZERS_PARALLELISM="false", HF_HUB_OFFLINE="1",
               TRANSFORMERS_OFFLINE="1", WANDB_DISABLED="true", PYTHONUNBUFFERED="1",
               TORCHINDUCTOR_CACHE_DIR=str(cache_directory / "inductor"),
               TRITON_CACHE_DIR=str(cache_directory / "triton"), CUDA_CACHE_PATH=str(cache_directory / "cuda"),
               CUTE_DSL_CACHE_DIR=str(cache_directory / "cute"), XDG_CACHE_HOME=str(cache_directory / "xdg"),
               TMPDIR=str(cache_directory / "tmp"))
    started, reason, capture = time.monotonic(), None, {}
    with log_path.open("ab") as log:
        # Deliberately no RLIMIT_FSIZE: compiler artifacts may exceed the log cap.
        # The owned reader bounds stdout separately from aggregate cache guards.
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=ROOT,
                                   env=env, start_new_session=True)
        reader = threading.Thread(target=capture_log, args=(process.stdout, log, log_limit, capture), daemon=True)
        reader.start()
        last_guard = started - 5
        try:
            while process.poll() is None:
                now = time.monotonic()
                if now - started >= timeout:
                    reason = "profile_wall_timeout"
                    break
                if now - last_guard >= 5:
                    reason, last_guard = guard(), now
                    if reason:
                        break
                try:
                    process.wait(timeout=min(1, max(.01, timeout - (now - started))))
                except subprocess.TimeoutExpired:
                    pass
        finally:
            terminate_owned(process)
            reader.join(timeout=2)
            if reader.is_alive():
                capture["error_type"] = "LogReaderDidNotFinish"
    if capture.get("error_type") and not reason:
        reason = "log_capture_failure"
    return process.returncode, reason, time.monotonic() - started, capture


def launcher_signatures(log_path):
    """Read a bounded suffix, describing observed failures without inventing a cause."""
    if not log_path.exists():
        return {}
    with log_path.open("rb") as handle:
        handle.seek(max(0, log_path.stat().st_size - 64 * 1024))
        suffix = handle.read(64 * 1024).decode(errors="replace")
    return {name: True for name, marker in (("segmentation_fault", "SIGSEGV"),
            ("file_size_error", "[Errno 27] File too large"), ("cuda_out_of_memory", "CUDA out of memory"))
            if marker in suffix}


def profile_result(profile, path, code, reason, *, world_size, gpu_type, config, real_data=False, launcher_seconds=None):
    record = dict(profile, status="failed", exit_code=code, measurement_kind="real_data_confirmation" if real_data
                  else "synthetic_short_probe")
    try:
        result = json.loads(path.read_text()) if path.exists() else {}
    except (OSError, json.JSONDecodeError):
        return dict(record, failure_type="UnreadableResult")
    keys = ("failure_type", "failure_message", "runtime_seconds", "setup_seconds", "warmup_seconds",
            "compile_seconds", "measurement_seconds", "completed_warmup_steps", "hardware",
            "peak_cuda_allocated_bytes", "peak_cuda_reserved_bytes", "smoke_checks",
            "optimizer_update_check", "attention_backend", "attention_kernels", "attention_evidence",
            "actual_parameter_count", "precision_recipe", "checkpointing_recipe", "converted_linears",
            "compile_timing_scope", "loss_summary", "phase_seconds", "compilation_evidence",
            "optimizer_state_encoding", "optimizer_state_dtypes", "master_parameter_dtypes", "gradient_dtypes",
            "input_kind", "data_validation", "data_pack_sha256", "data_manifest_sha256", "data_cursor_tokens",
            "data", "chunk_rates", "measurement_requirements", "host_input_prepare_and_transfer_schedule_seconds",
            "host_input_timing_scope", "completed_optimizer_updates", "first_warmup_seconds", "packages")
    record.update({key: result[key] for key in keys if key in result})
    if "failure_message" in record:
        record["failure_message"] = str(record["failure_message"])[:4000]
    if isinstance(result.get("profiler"), dict):
        record["profiler_seconds"] = result["profiler"].get("elapsed_seconds")
    args, throughput, hardware = result.get("arguments", {}), result.get("throughput", {}), result.get("hardware", [])
    expected = dict(sequence_length=config["sequence_length"], batch_size=profile["microbatch_per_gpu"],
                    accumulation=profile["accumulation"], hardware=gpu_type)
    expected.update({ARGUMENTS.get(key, key): value for key, value in profile["features"].items()})
    rate, steps = throughput.get("input_tokens_per_second"), throughput.get("measured_optimizer_steps")
    seconds = throughput.get("measured_wall_seconds")
    tokens = config["sequence_length"] * config["global_batch_sequences"]
    minimum_steps = config["confirmations"]["minimum_optimizer_steps"] if real_data else config["measured_optimizer_steps"]
    signatures = launcher_signatures(path.with_name("worker.log"))
    if signatures:
        record["log_signatures"] = signatures
    if reason:
        timeout = reason in ("profile_wall_timeout", "short_phase_deadline", "suite_deadline")
        record.update(failure_type="ProfileTimeout" if timeout else "ResourceGuardStop", stop_reason=reason)
    elif code != 0:
        if result.get("failure_type") in ("FeatureUnavailable", "UnsupportedFeature", "ModuleNotFoundError", "ImportError"):
            record["status"] = "unavailable"
        record.setdefault("failure_type", "WorkerSegmentationFault" if signatures.get("segmentation_fault")
                          else "LauncherNonzeroExit")
    elif result.get("status") != "completed":
        record.setdefault("failure_type", "IncompleteProfile")
    elif result.get("world_size") != world_size or any(args.get(key) != value for key, value in expected.items()):
        record["failure_type"] = "MatchedConfigurationMismatch"
    elif (not is_positive_int(steps) or steps < minimum_steps or (not real_data and steps != minimum_steps)
          or throughput.get("input_tokens_per_step") != tokens
          or throughput.get("measured_input_tokens") != tokens * steps
          or result.get("completed_warmup_steps") != config["warmup_optimizer_steps"]):
        record["failure_type"] = "IncompleteMatchedMeasurement"
    elif result.get("config_sha256") != config["model_config_sha256"]:
        record["failure_type"] = "ModelConfigurationHashMismatch"
    elif result.get("runner_sha256") != config["runner_sha256"]:
        record["failure_type"] = "RunnerHashMismatch"
    elif any(result.get("packages", {}).get(name) != version
             for name, version in config.get("_expected_runtime_packages", {}).items()):
        record["failure_type"] = "RuntimePackageVersionMismatch"
    elif len(hardware) != world_size or any(gpu_type not in item.get("gpu", "").lower() for item in hardware):
        record["failure_type"] = "ActualHardwareMismatch"
    elif result.get("smoke_checks", {}).get("status") != "passed":
        record["failure_type"] = "NumericalSmokeCheckFailed"
    elif result.get("optimizer_update_check", {}).get("status") != "passed":
        record["failure_type"] = "OptimizerUpdateCheckFailed"
    elif not isinstance(rate, (int, float)) or isinstance(rate, bool) or not math.isfinite(rate) or rate <= 0:
        record["failure_type"] = "InvalidThroughput"
    elif not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or seconds <= 0:
        record["failure_type"] = "InvalidMeasuredDuration"
    elif not math.isclose(rate, tokens * steps / seconds, rel_tol=1e-8):
        record["failure_type"] = "ThroughputArithmeticMismatch"
    elif real_data and (not isinstance(launcher_seconds, (int, float))
                       or launcher_seconds < config["confirmations"]["minimum_measurement_seconds"]
                       or launcher_seconds + 1 < seconds):
        record["failure_type"] = "ParentMeasuredDurationMismatch"
    elif real_data and (throughput.get("valid_sustained_measurement") is not True
                       or result.get("measurement_requirements", {}).get("satisfied") is not True
                       or result.get("measurement_requirements", {}).get("last_completed_update_end_seconds", 0)
                          < config["confirmations"]["minimum_measurement_seconds"]):
        record["failure_type"] = "IncompleteSustainedUpdates"
    elif real_data and (result.get("data_pack_sha256") != config["data_pack_sha256"]
                       or result.get("data_manifest_sha256") != config["data_manifest_sha256"]
                       or result.get("data", {}).get("replay") is not False):
        record["failure_type"] = "RealDataIdentityMismatch"
    elif real_data and (seconds < config["confirmations"]["minimum_measurement_seconds"]
                       or args.get("minimum_measured_seconds") != config["confirmations"]["minimum_measurement_seconds"]
                       or args.get("input_start_token") != 0
                       or args.get("input_token_pack_sha256") != config["data_pack_sha256"]):
        record["failure_type"] = "InsufficientRealDataConfirmation"
    else:
        record.update(status="completed", throughput=throughput, input_tokens_per_second=rate)
    return record


def short_winner(state):
    return max(completed_records(state), key=lambda record: record["input_tokens_per_second"], default=None)


def confirmation_profile(config, state, *, winner):
    original = short_winner(state) if winner else None
    if original is None:
        original = resolve_profile(config["profiles"][0], config["profiles"], state)
    name = config["confirmations"]["winner_name" if winner else "baseline_name"]
    return dict(name=name, parent=original["name"], resolved_parent=original["name"],
                role="confirmation_winner" if winner else "confirmation_baseline",
                features=dict(original["features"]), microbatch_per_gpu=original["microbatch_per_gpu"],
                accumulation=original["accumulation"], profile_steps=0,
                selection="Fastest complete synthetic probe" if winner else "Unmodified baseline recipe",
                minimum_measurement_seconds=config["confirmations"]["minimum_measurement_seconds"])


def summarize(state, config, now, *, terminal=False):
    records = []
    for profile in config["profiles"]:
        pending = dict(profile, status="skipped" if terminal or state.get("stage") != "short_sweep" else "pending",
                       measurement_kind="synthetic_short_probe")
        if pending["status"] == "skipped":
            pending["failure_type"] = "ShortProbeBudgetExhausted"
        record = dict(state["attempted_profiles"].get(profile["name"], pending))
        if terminal and record["status"] == "initializing":
            record.update(status="failed", failure_type="InterruptedPreviousAttempt")
        records.append(record)
    confirms = []
    for winner in (False, True):
        profile = confirmation_profile(config, state, winner=winner)
        pending = dict(profile, status="skipped" if terminal else "pending",
                       measurement_kind="real_data_confirmation")
        if terminal:
            pending["failure_type"] = "ConfirmationBudgetExhausted"
        record = dict(state["confirmations"].get(profile["name"], pending))
        if terminal and record["status"] == "initializing":
            record.update(status="failed", failure_type="InterruptedPreviousAttempt")
        confirms.append(record)
    successful = [record for record in confirms if record["status"] == "completed"]
    fastest = max(successful, key=lambda record: record["input_tokens_per_second"], default=None)
    baseline, candidate = confirms
    both_confirmed = baseline["status"] == candidate["status"] == "completed"
    return dict(status=("completed" if both_confirmed else "failed") if terminal else "running",
                stage=state.get("stage"), mode="gpu_optimization_confirmation",
                world_size=state["configuration"]["world_size"], gpu_type=state["configuration"]["gpu_type"],
                sequence_length=4096, global_batch_sequences=32, input_tokens_per_update=131072,
                profiles=records + confirms, short_probe_profiles=records,
                diagnostic_baseline_result=records[0], short_sweep_winner=short_winner(state),
                baseline_result=baseline, confirmation_candidate=candidate, real_data_confirmations=confirms,
                fastest_completed_profile=fastest, baseline_profile=baseline["name"],
                fastest_completed_profile_name=fastest["name"] if fastest else None,
                tuning_speedup_over_baseline=(fastest["input_tokens_per_second"] / baseline["input_tokens_per_second"]
                    if fastest and baseline["status"] == "completed" else None),
                candidate_speedup_over_baseline=(candidate["input_tokens_per_second"] / baseline["input_tokens_per_second"]
                    if both_confirmed else None),
                configuration=state["configuration"], started_utc=state["started_utc"],
                deadline_epoch=state["deadline_epoch"], runtime_seconds=now - state["started_epoch"],
                stop_reason=state.get("stop_reason"), short_stop_reason=state.get("short_stop_reason"),
                correctness_scope="Functional smoke and actual optimizer updates; no CPT quality or convergence claim",
                rate_scope="Real-data confirmations only: mmap reads/H2D/training included; setup and warmup excluded",
                allocation_timing_scope="Suite wall time includes probe setup/warmup/compilation/logging; scheduler allocation includes wrapper startup too")


def write_suite_result(output, state, config, *, terminal=False):
    suite = summarize(state, config, time.time(), terminal=terminal)
    baseline = suite["baseline_result"]
    if baseline["status"] == "completed":
        result = {key: baseline[key] for key in
                  ("world_size", "hardware", "throughput", "runtime_seconds", "setup_seconds", "warmup_seconds",
                   "compile_seconds", "measurement_seconds", "completed_warmup_steps", "peak_cuda_allocated_bytes",
                   "peak_cuda_reserved_bytes", "smoke_checks", "optimizer_update_check", "data_validation",
                   "data_pack_sha256", "data_manifest_sha256", "data_cursor_tokens", "loss_summary", "data",
                   "chunk_rates", "measurement_requirements", "host_input_prepare_and_transfer_schedule_seconds",
                   "host_input_timing_scope", "completed_optimizer_updates", "first_warmup_seconds", "packages") if key in baseline}
    else:
        result = dict(failure_type="RealDataBaselineNotComplete")
    result.update(status=suite["status"], world_size=state["configuration"]["world_size"],
                  started_utc=state["started_utc"], suite=suite)
    write_json(output / "results.json", result)
    return result


def run_one(profile, args, config, paths, state, output, *, real_data, phase_deadline):
    container = state["confirmations"] if real_data else state["attempted_profiles"]
    directory = output / profile["name"]
    directory.mkdir(exist_ok=True)
    result_path = directory / "results.json"
    maximum = config["bounds"]["confirmation_profile_seconds"] if real_data else (
        config["bounds"]["compile_profile_seconds"] if profile["features"]["compile"] == "on"
        else config["bounds"]["profile_seconds"])
    timeout = min(profile.get("timeout_seconds", maximum), phase_deadline - time.time() - 8)
    command = child_command(profile, args, config, paths, result_path, timeout, real_data=real_data)
    initial = dict(profile, status="initializing", started_epoch=time.time(), command=command,
                   measurement_kind="real_data_confirmation" if real_data else "synthetic_short_probe")
    container[profile["name"]] = initial
    write_json(output / "suite_state.json", state)
    write_json(directory / "profile_metadata.json", initial)
    write_suite_result(output, state, config)
    print(json.dumps(dict(stage="profile_start", name=profile["name"], parent=profile.get("resolved_parent"),
                          real_data=real_data, timeout_seconds=timeout, features=profile["features"])), flush=True)
    def guard():
        if (output / "STOP").exists():
            return "stop_file_requested"
        if time.time() >= phase_deadline - 5:
            return "suite_deadline" if real_data else "short_phase_deadline"
        return storage_reason(config, output)
    try:
        code, reason, elapsed, capture = run_process(command, directory / "worker.log", timeout, guard,
                                                    output / "compile_cache")
        record = profile_result(profile, result_path, code, reason, world_size=args.world_size,
                                gpu_type=args.gpu_type, config=config, real_data=real_data, launcher_seconds=elapsed)
        record.update(launcher_wall_seconds=elapsed, log_capture=capture)
        write_json(directory / "log_capture.json", capture)
    except InterruptedError:
        record = dict(profile, status="failed", failure_type="Interrupted", stop_reason="interrupted")
        state["stop_reason"] = "interrupted"
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        record = dict(profile, status="failed", failure_type=type(error).__name__, failure_message=str(error)[:4000])
    record.update(finished_epoch=time.time(), result_path=str(result_path.relative_to(ROOT)),
                  measurement_kind="real_data_confirmation" if real_data else "synthetic_short_probe")
    container[profile["name"]] = record
    write_json(output / "suite_state.json", state)
    write_suite_result(output, state, config)
    print(json.dumps(dict(stage="profile_finish", name=profile["name"], status=record["status"],
                          failure_type=record.get("failure_type"), real_data=real_data,
                          input_tokens_per_second=record.get("input_tokens_per_second"))), flush=True)
    return record


def run_suite(args):
    output = args.output_dir.resolve()
    if output.parent != REGISTRY or not output.name.startswith("job_"):
        raise ValueError("Use a dedicated job directory in the existing throughput registry")
    called_epoch = time.time()
    config, paths, binding = configuration(args)
    bounds = config["bounds"]
    with suite_lock(output):
        state_path = output / "suite_state.json"
        state = load_state(state_path, binding, bounds["suite_seconds"], called_epoch)
        state.setdefault("preflight_wall_seconds", time.time() - called_epoch)
        for container in (state["attempted_profiles"], state["confirmations"]):
            for item in container.values():
                if item["status"] == "initializing":
                    item.update(status="failed", failure_type="InterruptedPreviousAttempt", finished_epoch=time.time())
        write_json(state_path, state)
        write_suite_result(output, state, config)
        short_deadline = state["deadline_epoch"] - bounds["confirmation_reserve_seconds"]
        if state.get("stage") == "short_sweep" and not state.get("stop_reason"):
            for plan in config["profiles"]:
                if plan["name"] in state["attempted_profiles"]:
                    continue
                if time.time() + 60 >= short_deadline:
                    state["short_stop_reason"] = "reserved_for_real_data_confirmations"
                    break
                reason = storage_reason(config, output)
                if reason or (output / "STOP").exists():
                    state["stop_reason"] = reason or "stop_file_requested"
                    break
                if sha256(RUNNER) != binding["runner_sha256"]:
                    state["stop_reason"] = "runner_changed"
                    break
                profile = resolve_profile(plan, config["profiles"], state)
                parent = state["attempted_profiles"].get(profile.get("resolved_parent"), {})
                if profile.get("requires_parent_success") and parent.get("status") != "completed":
                    state["attempted_profiles"][profile["name"]] = dict(profile, status="skipped", failure_type="ParentNotSuccessful")
                    write_json(state_path, state)
                    continue
                record = run_one(profile, args, config, paths, state, output, real_data=False,
                                 phase_deadline=short_deadline)
                if record.get("failure_type") == "ResourceGuardStop" or state.get("stop_reason"):
                    state["stop_reason"] = record.get("stop_reason", state.get("stop_reason"))
                    break
        for winner in (False, True):
            profile = confirmation_profile(config, state, winner=winner)
            if profile["name"] in state["confirmations"]:
                continue
            if state.get("stop_reason"):
                break
            state["stage"] = "confirm_winner" if winner else "confirm_baseline"
            write_json(state_path, state)
            write_suite_result(output, state, config)
            if time.time() + config["confirmations"]["minimum_measurement_seconds"] + 30 >= state["deadline_epoch"]:
                state["stop_reason"] = "insufficient_real_data_confirmation_budget"
                break
            reason = storage_reason(config, output)
            if reason or (output / "STOP").exists():
                state["stop_reason"] = reason or "stop_file_requested"
                break
            if sha256(RUNNER) != binding["runner_sha256"]:
                state["stop_reason"] = "runner_changed"
                break
            record = run_one(profile, args, config, paths, state, output, real_data=True,
                             phase_deadline=state["deadline_epoch"])
            if record.get("failure_type") == "ResourceGuardStop" or state.get("stop_reason"):
                state["stop_reason"] = record.get("stop_reason", state.get("stop_reason"))
                break
        state["stage"] = "finished"
        result = write_suite_result(output, state, config, terminal=True)
        state.update(status=result["status"], finished_epoch=time.time())
        write_json(state_path, state)
        print(json.dumps(dict(stage="suite_finish", status=result["status"], stop_reason=state.get("stop_reason"),
                              fastest_confirmed_profile=result["suite"]["fastest_completed_profile_name"])), flush=True)
        return 0 if result["status"] == "completed" else 1


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--world-size", type=int, choices=(2, 8), required=True)
    parser.add_argument("--gpu-type", choices=("a100", "b200"), required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    def interrupted(signum, frame):
        raise InterruptedError(f"Sweep interrupted by signal {signum}")
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    raise SystemExit(run_suite(arguments()))
