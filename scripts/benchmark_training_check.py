#!/usr/bin/env python3
"""Bounded, offline diagnostic rerun with separately reported baseline and tuning."""
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
import resource
import shutil
import signal
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/benchmark_4b_training.py"
RUN_DIRECTORY = ROOT / "experiments/training_throughput_check_2026-10-19"
ORIGINAL_RUN = ROOT / "experiments/training_throughput_2026-10-18"
MIB = 1024 ** 2


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def profiles(mode, world_size, gpu_type):
    if mode == "b200_tuning" and (world_size, gpu_type.lower()) == (2, "b200"):
        choices = [("baseline", 4, "on", "full_shard"),
                   ("tuned_micro4", 4, "off", "shard_grad_op"),
                   ("tuned_micro8", 8, "off", "shard_grad_op")]
    elif mode == "a100_diagnostic" and (world_size, gpu_type.lower()) == (8, "a100"):
        choices = [("baseline", 4, "on", "full_shard")]
    else:
        raise ValueError("Diagnostic modes require exactly two B200 or eight A100 GPUs")
    return [dict(name=name, role="baseline" if name == "baseline" else "tuning",
                 microbatch_per_gpu=microbatch, accumulation=32 // (world_size * microbatch),
                 activation_checkpointing=checkpoint, sharding=sharding,
                 profile_steps=1 if name == "baseline" else 0)
            for name, microbatch, checkpoint, sharding in choices]


def configuration(args):
    raw = args.config.read_bytes()
    config = json.loads(raw)
    expected = {"sequence_length": 4096, "global_batch_sequences": 32,
                "warmup_optimizer_steps": 3, "measured_optimizer_steps": 8}
    if any(config.get(key) != value for key, value in expected.items()):
        raise ValueError("The matched diagnostic requires context4096, globalbatch32, warmup3, steps8")
    model_config = (ROOT / config["model_config"]).resolve()
    model_config.relative_to(ROOT)
    model_sha = hashlib.sha256(model_config.read_bytes()).hexdigest()
    if config.get("model_config_sha256") != model_sha:
        raise ValueError("Pinned model configuration hash differs")
    runner_sha = hashlib.sha256(RUNNER.read_bytes()).hexdigest()
    if config.get("runner_sha256") and config["runner_sha256"] != runner_sha:
        raise ValueError("Pinned benchmark runner hash differs")
    bounds = config["bounds"]
    ceilings = {"suite_seconds": 1080, "b200_profile_seconds": 320,
                "a100_profile_seconds": 900, "new_run_artifact_bytes": 64 * MIB,
                "new_environment_and_artifact_bytes": 16 * 1024 ** 3}
    if any(not isinstance(bounds.get(key), int) or not 0 < bounds[key] <= maximum
           for key, maximum in ceilings.items()):
        raise ValueError("A diagnostic bound is missing, invalid or exceeds the approved allowance")
    if bounds.get("minimum_free_bytes", 0) < 64 * 1024 ** 3:
        raise ValueError("Minimum shared free-space floor is 64 GiB")
    baseline = config.get("baseline_environment_and_artifact_bytes")
    if not isinstance(baseline, int) or baseline < 0 or not config.get("baseline_checked_epoch"):
        raise ValueError("A recorded CPU-side environment/artifact preflight is required")
    binding = dict(config_sha256=hashlib.sha256(raw).hexdigest(),
                   runner_sha256=runner_sha, model_config_sha256=model_sha,
                   suite_runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   mode=args.mode, world_size=args.world_size, gpu_type=args.gpu_type.lower(),
                   profiles=profiles(args.mode, args.world_size, args.gpu_type))
    planned = [{key: value for key, value in item.items() if key not in ("role", "profile_steps")}
               for item in binding["profiles"]]
    if "profiles" in config and config["profiles"].get(args.mode) != planned:
        raise ValueError("Configured diagnostic profiles differ from the bounded matched plan")
    return config, model_config, binding


def load_state(path, binding, runtime, now):
    if path.exists():
        state = json.loads(path.read_text())
        if state["configuration"] != binding:
            raise ValueError("Existing diagnostic configuration differs; its budget cannot be reset")
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


def tree_bytes(directory):
    """Only the small new diagnostic run; never traverse the installed environment."""
    total = 0
    for current, _, files in os.walk(directory, followlinks=False):
        for name in files:
            try:
                total += (Path(current) / name).lstat().st_size
            except FileNotFoundError:
                pass
    return total


def storage_reason(config, directory=RUN_DIRECTORY):
    bounds = config["bounds"]
    new_bytes = tree_bytes(directory)
    if new_bytes >= bounds["new_run_artifact_bytes"] - 2 * MIB:
        return "new_artifact_limit"
    if (config["baseline_environment_and_artifact_bytes"] + new_bytes
            >= bounds["new_environment_and_artifact_bytes"] - 2 * MIB):
        return "environment_and_artifact_limit"
    if shutil.disk_usage(directory).free < bounds["minimum_free_bytes"] + 2 * MIB:
        return "shared_free_space_floor"
    return None


def child_command(profile, args, config, model_config, result_path, runtime):
    return [sys.executable, "-B", "-u", "-m", "torch.distributed.run", "--standalone",
            "--nnodes=1", f"--nproc_per_node={args.world_size}", "--max-restarts=0",
            str(RUNNER), "--model-config", str(model_config), "--output", str(result_path),
            "--sequence-length", str(config["sequence_length"]),
            "--batch-size", str(profile["microbatch_per_gpu"]),
            "--accumulation", str(profile["accumulation"]),
            "--warmup", str(config["warmup_optimizer_steps"]),
            "--steps", str(config["measured_optimizer_steps"]),
            "--activation-checkpointing", profile["activation_checkpointing"],
            "--sharding", profile["sharding"],
            "--profile-steps", str(profile["profile_steps"]),
            "--max-runtime-seconds", str(runtime)]


def terminate_owned(process):
    """Only the new session created for this launcher and its descendants."""
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
    # Bound noisy launcher output without a pipe reader or unbounded memory buffering.
    resource.setrlimit(resource.RLIMIT_FSIZE, (8 * MIB, 8 * MIB))


def run_process(command, log_path, timeout, guard):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="2",
               MKL_NUM_THREADS="2", TOKENIZERS_PARALLELISM="false", HF_HUB_OFFLINE="1",
               TRANSFORMERS_OFFLINE="1", WANDB_DISABLED="true", PYTHONUNBUFFERED="1")
    started = time.monotonic()
    reason = None
    with log_path.open("ab") as log:
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                   cwd=ROOT, env=env, start_new_session=True,
                                   preexec_fn=child_file_limit)
        last_guard = started - 5
        try:
            while process.poll() is None:
                now = time.monotonic()
                if now - started >= timeout:
                    reason = "profile_wall_timeout"
                    break
                if now - last_guard >= 5:
                    reason = guard()
                    last_guard = now
                    if reason:
                        break
                try:
                    process.wait(timeout=min(1, max(.01, timeout - (now - started))))
                except subprocess.TimeoutExpired:
                    pass
        finally:
            # Cleanup also runs for parent interruption; a launcher may leave descendants.
            terminate_owned(process)
        return process.returncode, reason, time.monotonic() - started


def profile_result(profile, path, code, stop_reason, *, world_size, gpu_type, config):
    record = dict(profile, status="failed", exit_code=code)
    result = json.loads(path.read_text()) if path.exists() else {}
    for key in ("failure_type", "failure_message", "stop_reason", "runtime_seconds",
                "phase_timings", "phase_seconds", "timing", "timings", "profiler",
                "profiler_summary", "hardware", "peak_cuda_allocated_bytes",
                "peak_cuda_reserved_bytes", "completed_warmup_steps", "setup_seconds",
                "warmup_seconds", "measurement_seconds"):
        if key in result:
            record[key] = result[key]
    arguments = result.get("arguments", {})
    throughput = result.get("throughput", {})
    expected = {"sequence_length": config["sequence_length"],
                "batch_size": profile["microbatch_per_gpu"], "accumulation": profile["accumulation"],
                "activation_checkpointing": profile["activation_checkpointing"],
                "sharding": profile["sharding"], "profile_steps": profile["profile_steps"]}
    hardware = result.get("hardware", [])
    rate = throughput.get("input_tokens_per_second")
    if stop_reason:
        record.update(failure_type="ProfileTimeout" if stop_reason == "profile_wall_timeout"
                      else "ResourceGuardStop", stop_reason=stop_reason)
    elif code != 0:
        record.setdefault("failure_type", "LauncherNonzeroExit")
    elif result.get("status") != "completed":
        record.setdefault("failure_type", "IncompleteProfile")
    elif (result.get("world_size") != world_size
          or any(arguments.get(key) != value for key, value in expected.items())
          or throughput.get("input_tokens_per_step") != 131072
          or throughput.get("measured_optimizer_steps") != config["measured_optimizer_steps"]
          or result.get("completed_warmup_steps") != config["warmup_optimizer_steps"]):
        record["failure_type"] = "MatchedConfigurationMismatch"
    elif (config.get("model_config_sha256")
          and result.get("config_sha256") != config["model_config_sha256"]):
        record["failure_type"] = "ModelConfigurationHashMismatch"
    elif (config.get("runner_sha256")
          and result.get("runner_sha256") != config["runner_sha256"]):
        record["failure_type"] = "RunnerHashMismatch"
    elif len(hardware) != world_size or any(gpu_type.lower() not in item.get("gpu", "").lower()
                                            for item in hardware):
        record["failure_type"] = "ActualHardwareMismatch"
    elif not isinstance(rate, (int, float)) or isinstance(rate, bool) or not math.isfinite(rate) or rate <= 0:
        record["failure_type"] = "InvalidThroughput"
    else:
        record.update(status="completed", throughput=throughput,
                      input_tokens_per_second=rate)
    return record


def summarize(state, selected_profiles, now):
    records = [state["attempted_profiles"].get(item["name"],
               dict(item, status="skipped", failure_type="InsufficientRemainingBudget"))
               for item in selected_profiles]
    for record in records:
        if record["status"] == "initializing":
            record.update(status="failed", failure_type="InterruptedPreviousAttempt")
    completed = [record for record in records if record["status"] == "completed"]
    fastest = max(completed, key=lambda item: item["input_tokens_per_second"], default=None)
    baseline = next(record for record in records if record["role"] == "baseline")
    return dict(status="completed" if completed else "failed", profiles=records,
                mode=state["configuration"]["mode"], world_size=state["configuration"]["world_size"],
                sequence_length=4096, global_batch_sequences=32, input_tokens_per_update=131072,
                baseline_result=baseline, fastest_completed_profile=fastest,
                tuning_speedup_over_baseline=(fastest["input_tokens_per_second"] /
                    baseline["input_tokens_per_second"] if fastest and baseline["status"] == "completed" else None),
                configuration=state["configuration"], started_utc=state["started_utc"],
                deadline_epoch=state["deadline_epoch"], runtime_seconds=now - state["started_epoch"],
                stop_reason=state.get("stop_reason"),
                rate_scope="Global input tokens per second after warmup; setup and the separate profiler step excluded")


def run_suite(args):
    output = args.output_dir.resolve()
    if output.parent not in (RUN_DIRECTORY, ORIGINAL_RUN) or not output.name.startswith("job_"):
        raise ValueError("Use a dedicated job directory in an approved throughput experiment")
    config, model_config, binding = configuration(args)
    selected_profiles = binding["profiles"]
    bounds = config["bounds"]
    profile_seconds = bounds["b200_profile_seconds" if args.mode == "b200_tuning" else "a100_profile_seconds"]
    with suite_lock(output):
        state_path = output / "suite_state.json"
        state = load_state(state_path, binding, bounds["suite_seconds"], time.time())
        write_json(state_path, state)
        for profile in selected_profiles:
            if profile["name"] in state["attempted_profiles"]:
                continue
            if time.time() + profile_seconds + 8 >= state["deadline_epoch"]:
                state["stop_reason"] = "suite_deadline"
                break
            reason = storage_reason(config, output)
            if reason:
                state["stop_reason"] = reason
                break
            directory = output / profile["name"]
            directory.mkdir(exist_ok=True)
            result_path = directory / "results.json"
            command = child_command(profile, args, config, model_config, result_path, profile_seconds - 10)
            if hashlib.sha256(RUNNER.read_bytes()).hexdigest() != binding["runner_sha256"]:
                state["stop_reason"] = "runner_changed"
                break
            record = dict(profile, status="initializing", started_epoch=time.time(), command=command)
            state["attempted_profiles"][profile["name"]] = record
            write_json(state_path, state)
            write_json(directory / "profile_metadata.json", record)
            print(json.dumps(dict(stage="profile_start", **profile)), flush=True)
            def guard():
                return "suite_deadline" if time.time() >= state["deadline_epoch"] - 5 else storage_reason(config, output)
            try:
                code, reason, elapsed = run_process(command, directory / "worker.log", profile_seconds, guard)
                record = profile_result(profile, result_path, code, reason,
                    world_size=args.world_size, gpu_type=args.gpu_type, config=config)
                record["launcher_wall_seconds"] = elapsed
            except InterruptedError:
                record = dict(profile, status="failed", failure_type="Interrupted", stop_reason="interrupted")
                state["stop_reason"] = "interrupted"
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                record = dict(profile, status="failed", failure_type=type(error).__name__)
            record.update(finished_epoch=time.time(), result_path=str(result_path.relative_to(ROOT)))
            state["attempted_profiles"][profile["name"]] = record
            write_json(state_path, state)
            print(json.dumps(dict(stage="profile_finish", name=profile["name"], status=record["status"],
                                  failure_type=record.get("failure_type"))), flush=True)
            if record.get("failure_type") == "ResourceGuardStop":
                state["stop_reason"] = record["stop_reason"]
                break
            if state.get("stop_reason") == "interrupted":
                break
        suite = summarize(state, selected_profiles, time.time())
        baseline = suite["baseline_result"]
        if baseline["status"] == "completed":
            result = json.loads((output / "baseline/results.json").read_text())
        else:
            result = dict(status="failed", failure_type="BaselineCheckFailed",
                          world_size=args.world_size, started_utc=state["started_utc"])
        result["suite"] = suite
        state.update(status=result["status"], finished_epoch=time.time())
        write_json(state_path, state)
        write_json(output / "results.json", result)
        print(json.dumps(dict(stage="suite_finish", status=result["status"],
                              stop_reason=suite["stop_reason"])), flush=True)
        return 0 if result["status"] == "completed" else 1


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--world-size", type=int, choices=(2, 8), required=True)
    parser.add_argument("--gpu-type", choices=("b200", "a100"), required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--mode", choices=("b200_tuning", "a100_diagnostic"), required=True)
    return parser.parse_args()


if __name__ == "__main__":
    def interrupted(signum, frame):
        raise InterruptedError(f"Diagnostic interrupted by signal {signum}")
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    raise SystemExit(run_suite(arguments()))
