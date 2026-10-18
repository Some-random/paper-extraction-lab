#!/usr/bin/env python3
"""Run a bounded, matched-global-batch sweep inside an existing GPU allocation."""
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
import signal
import subprocess
import sys
import time


RUNNER = Path(__file__).with_name("benchmark_4b_training.py")


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def profiles(world_size, global_batch=32, microbatches=(1, 2, 4)):
    if world_size <= 0 or global_batch <= 0:
        raise ValueError("GPU count and global batch must be positive")
    output = []
    for microbatch in microbatches:
        divisor = world_size * microbatch
        if microbatch <= 0 or global_batch % divisor:
            raise ValueError("Every profile must divide the fixed global sequence batch")
        output.append({"name": f"micro_{microbatch}", "microbatch_per_gpu": microbatch,
                       "accumulation": global_batch // divisor})
    return output


def child_command(profile, *, python, world_size, model_config, output,
                  sequence_length, warmup, steps, runtime_seconds):
    command = [str(python), "-u"]
    if world_size > 1:
        command += ["-m", "torch.distributed.run", "--standalone", "--nnodes=1",
                    f"--nproc_per_node={world_size}", "--max-restarts=0"]
    command += [str(RUNNER), "--model-config", str(model_config), "--output", str(output),
                "--sequence-length", str(sequence_length),
                "--batch-size", str(profile["microbatch_per_gpu"]),
                "--accumulation", str(profile["accumulation"]),
                "--warmup", str(warmup), "--steps", str(steps),
                "--max-runtime-seconds", str(runtime_seconds)]
    return command


def fastest_completed(records):
    candidates = []
    for record in records:
        rate = record.get("input_tokens_per_second")
        if (record.get("status") == "completed" and record.get("exit_code") == 0
                and isinstance(rate, (float, int)) and not isinstance(rate, bool)
                and math.isfinite(rate) and rate > 0):
            candidates.append(record)
    return max(candidates, key=lambda record: record["input_tokens_per_second"], default=None)


def eligible(profile, state, now, required_seconds):
    return (profile["name"] not in state["attempted_profiles"]
            and state["deadline_epoch"] - now >= required_seconds)


def load_state(path, configuration, total_runtime, now):
    if path.exists():
        state = json.loads(path.read_text())
        if state["configuration"] != configuration:
            raise ValueError("Existing suite configuration differs; its budget cannot be reset")
        return state
    return {"configuration": configuration, "started_epoch": now,
            "started_utc": datetime.fromtimestamp(now, timezone.utc).isoformat(),
            "deadline_epoch": now + total_runtime, "attempted_profiles": {},
            "status": "running"}


@contextmanager
def suite_lock(directory):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "suite.lock").open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def run_process(command, log_path, timeout):
    """Bound the launcher and every distributed child, with private file logs."""
    with log_path.open("ab") as log:
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        try:
            return process.wait(timeout=timeout), False
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                pass
            # The launcher may exit before a distributed worker does. Kill the
            # original group even when waiting for the launcher already ended.
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=3)
            return process.returncode, True


def read_profile_result(profile, result_path, exit_code, timed_out, *,
                        world_size=None, sequence_length=None, global_batch_sequences=None):
    record = dict(profile, exit_code=exit_code, status="failed")
    if result_path.exists():
        result = json.loads(result_path.read_text())
        record["status"] = result.get("status", "failed")
        if result.get("failure_type"):
            record["failure_type"] = result["failure_type"]
        throughput = result.get("throughput", {})
        for key in ("input_tokens_per_second", "measured_optimizer_steps", "input_tokens_per_step"):
            if key in throughput:
                record[key] = throughput[key]
        for key in ("peak_cuda_allocated_bytes", "peak_cuda_reserved_bytes"):
            if key in result:
                record[key] = result[key]
        if record["status"] == "completed" and world_size is not None:
            arguments = result.get("arguments", {})
            expected = {"sequence_length": sequence_length,
                        "batch_size": profile["microbatch_per_gpu"],
                        "accumulation": profile["accumulation"]}
            if (result.get("world_size") != world_size
                    or any(arguments.get(key) != value for key, value in expected.items())
                    or throughput.get("input_tokens_per_step")
                    != sequence_length * global_batch_sequences):
                record.update(status="failed", failure_type="MatchedConfigurationMismatch")
    if timed_out:
        # A child can write a completed result and then hang in collective exit.
        # The allocation did not successfully complete that profile.
        record.update(status="failed", failure_type="ProfileTimeout")
    elif exit_code != 0 and record["status"] == "completed":
        record.update(status="failed", failure_type="LauncherNonzeroExit")
    elif not result_path.exists():
        record["failure_type"] = "MissingProfileResult"
    return record


def run_suite(args):
    selected_profiles = profiles(args.world_size, args.global_batch_sequences)
    configuration = {"world_size": args.world_size, "sequence_length": args.sequence_length,
                     "global_batch_sequences": args.global_batch_sequences,
                     "model_config_sha256": hashlib.sha256(args.model_config.read_bytes()).hexdigest(),
                     "warmup": args.warmup, "steps": args.steps,
                     "profile_runtime_seconds": args.profile_runtime_seconds,
                     "total_runtime_seconds": args.total_runtime_seconds,
                     "profiles": selected_profiles}
    with suite_lock(args.output_dir):
        state_path = args.output_dir / "suite_state.json"
        state = load_state(state_path, configuration, args.total_runtime_seconds, time.time())
        write_json(state_path, state)
        for profile in selected_profiles:
            # Twenty seconds cover launcher startup/exit; six cover TERM/KILL.
            reserve = args.profile_runtime_seconds + 26
            if not eligible(profile, state, time.time(), reserve):
                continue
            profile_dir = args.output_dir / profile["name"]
            profile_dir.mkdir(parents=True, exist_ok=True)
            result_path = profile_dir / "results.json"
            command = child_command(profile, python=sys.executable, world_size=args.world_size,
                                    model_config=args.model_config, output=result_path,
                                    sequence_length=args.sequence_length, warmup=args.warmup,
                                    steps=args.steps, runtime_seconds=args.profile_runtime_seconds)
            # Mark before launch: rerunning the wrapper cannot repeat a profile.
            state["attempted_profiles"][profile["name"]] = dict(profile, status="initializing")
            write_json(state_path, state)
            print(json.dumps({"stage": "profile_start", **profile}), flush=True)
            try:
                code, timed_out = run_process(command, profile_dir / "worker.log",
                                              args.profile_runtime_seconds + 20)
                record = read_profile_result(profile, result_path, code, timed_out,
                                             world_size=args.world_size,
                                             sequence_length=args.sequence_length,
                                             global_batch_sequences=args.global_batch_sequences)
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                record = dict(profile, status="failed", failure_type=type(error).__name__)
            state["attempted_profiles"][profile["name"]] = record
            write_json(state_path, state)
            print(json.dumps({"stage": "profile_finish", **record}), flush=True)
        records = []
        for profile in selected_profiles:
            record = state["attempted_profiles"].get(profile["name"])
            if record is None:
                record = dict(profile, status="skipped", failure_type="InsufficientRemainingBudget")
            elif record["status"] == "initializing":
                record = dict(profile, status="failed", failure_type="InterruptedPreviousAttempt")
                state["attempted_profiles"][profile["name"]] = record
            records.append(record)
        winner = fastest_completed(records)
        summary = {"status": "completed" if winner else "failed",
                   "world_size": args.world_size,
                   "sequence_length": args.sequence_length,
                   "global_batch_sequences": args.global_batch_sequences,
                   "input_tokens_per_update": args.sequence_length * args.global_batch_sequences,
                   "selection": "Fastest fully completed profile with successful launcher exit",
                   "profiles": records,
                   "started_utc": state["started_utc"],
                   "runtime_seconds": time.time() - state["started_epoch"],
                   "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        if winner:
            result = json.loads((args.output_dir / winner["name"] / "results.json").read_text())
            summary["selected_profile"] = winner["name"]
        else:
            result = {"status": "failed", "failure_type": "NoCompletedMatchedProfile",
                      "world_size": args.world_size, "started_utc": state["started_utc"],
                      "runtime_seconds": summary["runtime_seconds"]}
        result["suite"] = summary
        write_json(args.output_dir / "results.json", result)
        state["status"] = summary["status"]
        state["finished_epoch"] = time.time()
        write_json(state_path, state)
        print(json.dumps(summary), flush=True)
        return 0 if winner else 1


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--world-size", type=int, choices=(2, 8), required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model-config", type=Path, required=True)
    parser.add_argument("--global-batch-sequences", type=int, default=32)
    parser.add_argument("--sequence-length", type=int, default=4096)
    parser.add_argument("--warmup", type=int, default=3)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--profile-runtime-seconds", type=int, default=280)
    parser.add_argument("--total-runtime-seconds", type=int, default=1020)
    args = parser.parse_args()
    for name in ("global_batch_sequences", "sequence_length", "warmup", "steps",
                 "profile_runtime_seconds", "total_runtime_seconds"):
        if getattr(args, name) <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    return args


if __name__ == "__main__":
    raise SystemExit(run_suite(arguments()))
