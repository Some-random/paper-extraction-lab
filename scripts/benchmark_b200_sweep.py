#!/usr/bin/env python3
"""Run a locked, bounded B200 optimization sweep with independent correctness gates."""
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
import resource
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/benchmark_b200_optimized.py"
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
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


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
    expected = {"world_size": 2, "sequence_length": 4096, "global_batch_sequences": 32,
                "warmup_optimizer_steps": 3, "measured_optimizer_steps": 8}
    if args.world_size != 2 or any(config.get(key) != value for key, value in expected.items()):
        raise ValueError("Sweep requires two B200s, context4096, globalbatch32, warmup3 and steps8")
    bounds = config.get("bounds", {})
    ceilings = {"suite_seconds": 6600, "profile_seconds": 420,
                "compile_profile_seconds": 900, "new_log_bytes": 64 * MIB,
                "new_run_artifact_bytes": 256 * MIB, "new_compile_cache_bytes": 4 * GIB,
                "new_environment_and_artifact_bytes": 16 * GIB}
    for key, ceiling in ceilings.items():
        if not is_positive_int(bounds.get(key)) or bounds[key] > ceiling:
            raise ValueError(f"Invalid or excessive {key} bound")
    if bounds.get("minimum_free_bytes", 0) < 64 * GIB:
        raise ValueError("Minimum shared free-space floor is 64 GiB")
    baseline = config.get("baseline_environment_and_artifact_bytes")
    if not isinstance(baseline, int) or baseline < 0 or not config.get("baseline_checked_epoch"):
        raise ValueError("A CPU-side footprint preflight is required; no environment walk on GPU")
    model = (ROOT / config["model_config"]).resolve()
    model.relative_to(ROOT)
    model_sha, runner_sha = sha256(model), sha256(RUNNER)
    if config.get("model_config_sha256") != model_sha:
        raise ValueError("Pinned model configuration hash differs")
    if config.get("runner_sha256") != runner_sha:
        raise ValueError("Pinned optimized runner hash differs")
    profiles = validate_profiles(config, args.world_size)
    binding = dict(config_sha256=hashlib.sha256(raw).hexdigest(), runner_sha256=runner_sha,
                   suite_runner_sha256=sha256(__file__), model_config_sha256=model_sha,
                   mode="b200_optimization", gpu_type="b200", world_size=args.world_size,
                   profiles=profiles)
    return config, model, binding


def load_state(path, binding, runtime, now):
    if path.exists():
        state = json.loads(path.read_text())
        if state["configuration"] != binding:
            raise ValueError("Saved sweep configuration differs; do not reset its budget")
        return state
    return dict(configuration=binding, started_epoch=now,
                started_utc=datetime.fromtimestamp(now, timezone.utc).isoformat(),
                deadline_epoch=now + runtime, attempted_profiles={}, status="running")


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


def child_command(profile, args, config, model_config, output, runtime):
    command = [sys.executable, "-B", "-u", "-m", "torch.distributed.run", "--standalone",
               "--nnodes=1", f"--nproc_per_node={args.world_size}", "--max-restarts=0",
               str(RUNNER), "--model-config", str(model_config), "--output", str(output),
               "--sequence-length", str(config["sequence_length"]),
               "--global-batch-sequences", str(config["global_batch_sequences"]),
               "--batch-size", str(profile["microbatch_per_gpu"]),
               "--accumulation", str(profile["accumulation"]),
               "--warmup", str(config["warmup_optimizer_steps"]),
               "--steps", str(config["measured_optimizer_steps"]),
               "--profile-steps", str(profile["profile_steps"]),
               "--max-runtime-seconds", str(max(1, math.floor(runtime - 10)))]
    for key in FEATURES:
        command += ["--" + FLAGS.get(key, key), profile["features"][key]]
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


def child_file_limit():
    resource.setrlimit(resource.RLIMIT_FSIZE, (8 * MIB, 8 * MIB))


def run_process(command, log_path, timeout, guard, cache_directory):
    (cache_directory / "tmp").mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="2", MKL_NUM_THREADS="2",
               OPENBLAS_NUM_THREADS="2", TOKENIZERS_PARALLELISM="false", HF_HUB_OFFLINE="1",
               TRANSFORMERS_OFFLINE="1", WANDB_DISABLED="true", PYTHONUNBUFFERED="1",
               TORCHINDUCTOR_CACHE_DIR=str(cache_directory / "inductor"),
               TRITON_CACHE_DIR=str(cache_directory / "triton"),
               CUDA_CACHE_PATH=str(cache_directory / "cuda"), CUTE_DSL_CACHE_DIR=str(cache_directory / "cute"),
               XDG_CACHE_HOME=str(cache_directory / "xdg"), TMPDIR=str(cache_directory / "tmp"))
    started, reason = time.monotonic(), None
    with log_path.open("ab") as log:
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT,
                                   env=env, start_new_session=True, preexec_fn=child_file_limit)
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
    return process.returncode, reason, time.monotonic() - started


def profile_result(profile, path, code, reason, *, world_size, config):
    record = dict(profile, status="failed", exit_code=code)
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
            "optimizer_state_encoding", "optimizer_state_dtypes", "master_parameter_dtypes", "gradient_dtypes")
    record.update({key: result[key] for key in keys if key in result})
    if "failure_message" in record:
        record["failure_message"] = str(record["failure_message"])[:4000]
    if isinstance(result.get("profiler"), dict):
        record["profiler_seconds"] = result["profiler"].get("elapsed_seconds")
    args, throughput, hardware = result.get("arguments", {}), result.get("throughput", {}), result.get("hardware", [])
    expected = dict(sequence_length=config["sequence_length"], batch_size=profile["microbatch_per_gpu"],
                    accumulation=profile["accumulation"])
    expected.update({ARGUMENTS.get(key, key): value for key, value in profile["features"].items()})
    rate = throughput.get("input_tokens_per_second")
    tokens = config["sequence_length"] * config["global_batch_sequences"]
    if reason:
        record.update(failure_type="ProfileTimeout" if reason == "profile_wall_timeout" else "ResourceGuardStop",
                      stop_reason=reason)
    elif code != 0:
        if result.get("failure_type") in ("FeatureUnavailable", "UnsupportedFeature", "ModuleNotFoundError", "ImportError"):
            record["status"] = "unavailable"
        record.setdefault("failure_type", "LauncherNonzeroExit")
    elif result.get("status") != "completed":
        record.setdefault("failure_type", "IncompleteProfile")
    elif result.get("world_size") != world_size or any(args.get(key) != value for key, value in expected.items()):
        record["failure_type"] = "MatchedConfigurationMismatch"
    elif (throughput.get("input_tokens_per_step") != tokens
          or throughput.get("measured_optimizer_steps") != config["measured_optimizer_steps"]
          or throughput.get("measured_input_tokens") != tokens * config["measured_optimizer_steps"]
          or result.get("completed_warmup_steps") != config["warmup_optimizer_steps"]):
        record["failure_type"] = "IncompleteMatchedMeasurement"
    elif result.get("config_sha256") != config["model_config_sha256"]:
        record["failure_type"] = "ModelConfigurationHashMismatch"
    elif result.get("runner_sha256") != config["runner_sha256"]:
        record["failure_type"] = "RunnerHashMismatch"
    elif len(hardware) != world_size or any("b200" not in item.get("gpu", "").lower() for item in hardware):
        record["failure_type"] = "ActualHardwareMismatch"
    elif result.get("smoke_checks", {}).get("status") != "passed":
        record["failure_type"] = "NumericalSmokeCheckFailed"
    elif result.get("optimizer_update_check", {}).get("status") != "passed":
        record["failure_type"] = "OptimizerUpdateCheckFailed"
    elif not isinstance(rate, (int, float)) or isinstance(rate, bool) or not math.isfinite(rate) or rate <= 0:
        record["failure_type"] = "InvalidThroughput"
    else:
        record.update(status="completed", throughput=throughput, input_tokens_per_second=rate)
    return record


def summarize(state, selected_profiles, now, *, terminal=True):
    records = []
    for profile in selected_profiles:
        unattempted = dict(profile, status="skipped" if terminal else "pending")
        if terminal:
            unattempted["failure_type"] = "InsufficientRemainingBudget"
        record = dict(state["attempted_profiles"].get(profile["name"], unattempted))
        if terminal and record["status"] == "initializing":
            record.update(status="failed", failure_type="InterruptedPreviousAttempt")
        records.append(record)
    completed = [record for record in records if record["status"] == "completed"]
    fastest = max(completed, key=lambda item: item["input_tokens_per_second"], default=None)
    baseline = records[0]
    return dict(status=("completed" if completed else "failed") if terminal else "running", profiles=records,
                mode="b200_optimization", world_size=state["configuration"]["world_size"],
                sequence_length=4096, global_batch_sequences=32, input_tokens_per_update=131072,
                baseline_result=baseline, fastest_completed_profile=fastest,
                baseline_profile=baseline["name"], fastest_completed_profile_name=fastest["name"] if fastest else None,
                tuning_speedup_over_baseline=(fastest["input_tokens_per_second"] / baseline["input_tokens_per_second"]
                    if fastest and baseline["status"] == "completed" else None),
                configuration=state["configuration"], started_utc=state["started_utc"],
                deadline_epoch=state["deadline_epoch"], runtime_seconds=now - state["started_epoch"],
                stop_reason=state.get("stop_reason"),
                rate_scope="Global input tokens per second after warmup; setup, compile-inclusive warmup and separate profiler excluded")


def run_suite(args):
    output = args.output_dir.resolve()
    if output.parent != REGISTRY or not output.name.startswith("job_"):
        raise ValueError("Use a dedicated job directory in the existing throughput registry")
    config, model_config, binding = configuration(args)
    profiles, bounds = binding["profiles"], config["bounds"]
    with suite_lock(output):
        state_path = output / "suite_state.json"
        state = load_state(state_path, binding, bounds["suite_seconds"], time.time())
        # An interrupted profile has consumed budget. Never silently retry it on resume.
        for item in state["attempted_profiles"].values():
            if item["status"] == "initializing":
                item.update(status="failed", failure_type="InterruptedPreviousAttempt", finished_epoch=time.time())
        write_json(state_path, state)
        for plan in profiles:
            if plan["name"] in state["attempted_profiles"]:
                continue
            profile = resolve_profile(plan, profiles, state)
            parent_record = state["attempted_profiles"].get(profile.get("resolved_parent"), {})
            if profile.get("requires_parent_success") and parent_record.get("status") != "completed":
                state["attempted_profiles"][profile["name"]] = dict(profile, status="skipped", failure_type="ParentNotSuccessful")
                write_json(state_path, state)
                continue
            maximum = bounds["compile_profile_seconds"] if profile["features"]["compile"] == "on" else bounds["profile_seconds"]
            timeout = profile.get("timeout_seconds", maximum)
            remaining = state["deadline_epoch"] - time.time() - 8
            if remaining < min(timeout, 30):
                state["stop_reason"] = "suite_deadline"
                break
            timeout = min(timeout, remaining)
            reason = storage_reason(config, output)
            if reason:
                state["stop_reason"] = reason
                break
            if sha256(RUNNER) != binding["runner_sha256"]:
                state["stop_reason"] = "runner_changed"
                break
            directory = output / profile["name"]
            directory.mkdir(exist_ok=True)
            result_path = directory / "results.json"
            command = child_command(profile, args, config, model_config, result_path, timeout)
            initial = dict(profile, status="initializing", started_epoch=time.time(), command=command)
            state["attempted_profiles"][profile["name"]] = initial
            write_json(state_path, state)
            write_json(directory / "profile_metadata.json", initial)
            write_suite_result(output, state, summarize(state, profiles, time.time(), terminal=False))
            print(json.dumps(dict(stage="profile_start", name=profile["name"], parent=profile.get("resolved_parent"),
                                  features=profile["features"], timeout_seconds=timeout)), flush=True)
            def guard():
                return "suite_deadline" if time.time() >= state["deadline_epoch"] - 5 else storage_reason(config, output)
            try:
                code, reason, elapsed = run_process(command, directory / "worker.log", timeout, guard, output / "compile_cache")
                record = profile_result(profile, result_path, code, reason, world_size=args.world_size, config=config)
                record["launcher_wall_seconds"] = elapsed
            except InterruptedError:
                record = dict(profile, status="failed", failure_type="Interrupted", stop_reason="interrupted")
                state["stop_reason"] = "interrupted"
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                record = dict(profile, status="failed", failure_type=type(error).__name__, failure_message=str(error)[:4000])
            record.update(finished_epoch=time.time(), result_path=str(result_path.relative_to(ROOT)))
            state["attempted_profiles"][profile["name"]] = record
            write_json(state_path, state)
            # Publish a compact local snapshot as each attempt finishes; independent monitors read it.
            suite = summarize(state, profiles, time.time(), terminal=False)
            write_suite_result(output, state, suite)
            print(json.dumps(dict(stage="profile_finish", name=profile["name"], status=record["status"],
                                  failure_type=record.get("failure_type"),
                                  input_tokens_per_second=record.get("input_tokens_per_second"))), flush=True)
            if record.get("failure_type") == "ResourceGuardStop" or state.get("stop_reason") == "interrupted":
                state["stop_reason"] = record.get("stop_reason", state.get("stop_reason"))
                break
        suite = summarize(state, profiles, time.time())
        result = write_suite_result(output, state, suite)
        state.update(status=result["status"], finished_epoch=time.time())
        write_json(state_path, state)
        print(json.dumps(dict(stage="suite_finish", status=result["status"], stop_reason=suite["stop_reason"],
                              fastest_completed_profile_name=suite["fastest_completed_profile_name"])), flush=True)
        return 0 if result["status"] == "completed" else 1


def write_suite_result(output, state, suite):
    baseline = suite["baseline_result"]
    if baseline["status"] == "completed":
        raw = json.loads((output / baseline["name"] / "results.json").read_text())
        # Full traces remain in the per-profile result. Keep the monitored snapshot small.
        keys = ("status", "world_size", "arguments", "hardware", "throughput", "config_sha256",
                "runner_sha256", "started_utc", "runtime_seconds", "setup_seconds", "warmup_seconds",
                "compile_seconds", "measurement_seconds", "completed_warmup_steps",
                "peak_cuda_allocated_bytes", "peak_cuda_reserved_bytes", "smoke_checks",
                "optimizer_update_check", "attention_backend", "attention_kernels", "attention_evidence",
                "actual_parameter_count", "precision_recipe", "checkpointing_recipe", "converted_linears",
                "compile_timing_scope", "loss_summary", "compilation_evidence", "optimizer_state_encoding",
                "optimizer_state_dtypes", "master_parameter_dtypes", "gradient_dtypes")
        result = {key: raw[key] for key in keys if key in raw}
    else:
        result = dict(status="running" if suite["status"] == "running" else "failed",
                      failure_type="BaselineNotYetComplete" if suite["status"] == "running" else "BaselineCheckFailed",
                      world_size=state["configuration"]["world_size"],
                      started_utc=state["started_utc"])
    result["suite"] = suite
    write_json(output / "results.json", result)
    return result


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--world-size", type=int, choices=(2,), default=2)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    def interrupted(signum, frame):
        raise InterruptedError(f"Sweep interrupted by signal {signum}")
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    raise SystemExit(run_suite(arguments()))
