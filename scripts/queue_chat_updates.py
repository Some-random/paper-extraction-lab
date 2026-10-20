#!/usr/bin/env python3
"""Queue requested two-hour status checks into one existing Codex thread.

This monitor reads only the recorded paper/benchmark jobs. Queue acceptance is
recorded separately from message delivery; it never starts a Codex session.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time
import uuid

import report_paper_collection as paper
import watch_training_throughput as gpu

ROOT = Path(__file__).resolve().parents[1]
RETRY_SECONDS = 300
MAX_SECONDS = 7 * 86400
MAX_PROMPT_BYTES = 64 * 1024


class PromptTooLargeError(RuntimeError):
    def __init__(self, size):
        self.prompt_bytes = size
        super().__init__(f"Status prompt exceeds {MAX_PROMPT_BYTES}-byte bound")


def fields(value, names):
    """Copy explicitly named scalar fields; never include nested raw results."""
    if not isinstance(value, dict):
        return {}
    return {key: value[key] for key in names if key in value
            and (value[key] is None or isinstance(value[key], (str, int, float, bool)))}


def compact_measurement(value):
    result = fields(value, ("input_tokens_per_second", "input_tokens_per_step",
                           "measured_input_tokens", "measured_optimizer_steps", "measured_wall_seconds",
                           "valid_sustained_measurement"))
    if isinstance(value, dict) and isinstance(value.get("step_seconds"), dict):
        result["step_seconds"] = fields(value["step_seconds"], ("mean", "p50", "p95"))
    return result


def compact_profile(value):
    result = fields(value, ("name", "role", "status", "failure_type", "exit_code",
                           "microbatch_per_gpu", "accumulation", "activation_checkpointing", "sharding",
                           "input_tokens_per_second", "input_tokens_per_step", "measured_optimizer_steps",
                           "setup_seconds", "warmup_seconds", "measurement_seconds", "runtime_seconds",
                           "profiler_seconds", "launcher_wall_seconds", "completed_warmup_steps", "peak_cuda_allocated_bytes",
                           "peak_cuda_reserved_bytes", "measurement_kind", "compile_seconds",
                           "minimum_measurement_seconds", "data_cursor_tokens"))
    if isinstance(value, dict) and value.get("throughput"):
        # Keep each measured count once; rates/timings often appear both on the
        # profile and in its throughput object.
        for key, item in compact_measurement(value["throughput"]).items():
            if key != "step_seconds":
                result.setdefault(key, item)
    if isinstance(value, dict) and isinstance(value.get("features"), dict):
        result["features"] = fields(value["features"],
                                    ("attention", "kernels", "checkpointing", "sharding", "compile", "precision",
                                     "float8_all_gather", "optimizer"))
        # Older profiles need the original fields; optimized profiles already
        # state these settings in their complete feature recipe.
        for legacy, feature in (("activation_checkpointing", "checkpointing"), ("sharding", "sharding")):
            if feature in result["features"]:
                result.pop(legacy, None)
    if isinstance(value, dict) and isinstance(value.get("profiler"), dict):
        elapsed = value["profiler"].get("elapsed_seconds")
        if isinstance(elapsed, (int, float)):
            result["profiler_seconds"] = elapsed
    if isinstance(value, dict) and isinstance(value.get("measurement_requirements"), dict):
        result["measurement_requirements"] = fields(value["measurement_requirements"],
            ("minimum_optimizer_steps", "minimum_measured_seconds", "last_completed_update_end_seconds", "satisfied"))
    return result


def compact_suite(value):
    result = fields(value, ("status", "stage", "mode", "stop_reason", "short_stop_reason", "runtime_seconds", "deadline_epoch",
                           "global_batch_sequences", "input_tokens_per_update", "sequence_length",
                           "world_size", "selected_profile", "tuning_speedup_over_baseline",
                           "baseline_profile", "fastest_completed_profile_name", "candidate_speedup_over_baseline", "rate_scope"))
    if not isinstance(value, dict):
        return result
    if isinstance(value.get("profiles"), list):
        result["profiles"] = [compact_profile(item) for item in value["profiles"]]
        # Older completed sweeps accumulate across jobs. Keep detailed evidence
        # for baseline/winner/active profiles and short outcomes for the rest.
        # This bounds both current and previous observations without dropping IDs,
        # measured winning rates, failed attempts or the active recipe.
        profiles = result["profiles"]
        if len(profiles) > 6:
            detailed = {profiles[0].get("name"), value.get("baseline_profile"),
                        value.get("fastest_completed_profile_name"), value.get("selected_profile")}
            for key in ("baseline_result", "fastest_completed_profile", "confirmation_candidate", "short_sweep_winner"):
                if isinstance(value.get(key), dict):
                    detailed.add(value[key].get("name"))
            detailed.update(item.get("name") for item in profiles
                            if item.get("status") in ("initializing", "running"))
            result["profile_counts"] = dict(Counter(item.get("status", "unknown") for item in profiles))
            result["profiles"] = [item if item.get("name") in detailed else fields(item,
                ("name", "status", "failure_type", "exit_code", "input_tokens_per_second",
                 "microbatch_per_gpu", "accumulation")) for item in profiles]
    names = {item.get("name") for item in result.get("profiles", [])}
    for key, reference in (("baseline_result", "baseline_profile"),
                           ("fastest_completed_profile", "fastest_completed_profile_name"),
                           ("confirmation_candidate", "confirmation_candidate_name"),
                           ("short_sweep_winner", "short_sweep_winner_name")):
        if isinstance(value.get(key), dict):
            name = value[key].get("name")
            if name is not None and name in names:
                result[reference] = name
            else:
                result[key] = compact_profile(value[key])
    configuration = fields(value.get("configuration"), ("gpu_type", "mode", "world_size"))
    if configuration:
        result["configuration"] = configuration
    return result


def compact_snapshot(value):
    """Keep status evidence, counts and timings; exclude duplicated profiler dumps.

    Also accepts snapshots from older monitor states, so restarting after a large
    result cannot reinsert the old profiler into the previous-update prompt.
    """
    if value is None:
        return None
    observed = value.get("paper", {})
    compact_paper = fields(observed, ("checked_at_pst", "checked_epoch", "deadline_at_pst", "job_id",
                                     "run_id", "scheduler_observed", "scheduler_state", "stage", "status",
                                     "stop_reason", "reason", "error_type", "submitted_at_pst",
                                     "target_new_papers", "worker_heartbeat_age_seconds",
                                     "storage_bounded_continuation", "control_plane_reserve_bytes"))
    for key in ("counts", "inventory", "limits"):
        if isinstance(observed.get(key), dict):
            compact_paper[key] = {name: count for name, count in observed[key].items()
                                  if count is None or isinstance(count, (int, float, bool))}
    jobs = []
    for item in value.get("gpu_jobs", []):
        job = fields(item, ("job_id", "status", "scheduler_state", "gpus", "gpu_type"))
        job["measurement"] = compact_measurement(item.get("measurement"))
        job["suite"] = compact_suite(item.get("suite"))
        jobs.append(job)
    result = {"paper": compact_paper, "gpu_jobs": jobs}
    for key in ("scheduler_errors", "monitor_error"):
        if key in value:
            result[key] = value[key]
    return result


def check_prompt_size(prompt):
    size = len(prompt.encode("utf-8"))
    if size > MAX_PROMPT_BYTES:
        raise PromptTooLargeError(size)
    return prompt


def queue_error(error):
    result = {"error_type": type(error).__name__}
    if isinstance(error, OSError) and error.errno is not None:
        # The system description is actionable without filenames, argv or IDs.
        result.update(errno=error.errno, strerror=os.strerror(error.errno))
    if isinstance(error, PromptTooLargeError):
        result.update(prompt_bytes=error.prompt_bytes, maximum_prompt_bytes=MAX_PROMPT_BYTES)
    return result


def read(path):
    if not path.exists():
        return {}
    if path.stat().st_size > 2 * 1024 * 1024:
        raise ValueError("Status file exceeds bound")
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError("Expected status object")
    return value


def load_config(path):
    config = read(path)
    config["thread_id"] = str(uuid.UUID(config["thread_id"]))
    if not Path(config["codex_path"]).is_absolute():
        raise ValueError("Codex executable must be absolute")
    if not 60 <= config.get("interval_seconds", 7200) <= 7200:
        raise ValueError("Require 60–7200 second interval")
    if not 10 <= config.get("poll_seconds", 60) <= 60:
        raise ValueError("Require 10–60 second polls")
    for key in ("run_directory", "paper_run_directory", "throughput_run_directory"):
        config[key] = str((ROOT / config[key]).resolve())
    return config


def snapshot(config, now, previous=None, query=gpu.query_scheduler):
    """One combined allowlisted scheduler observation; no manifest mutations."""
    paper_run, gpu_run = Path(config["paper_run_directory"]), Path(config["throughput_run_directory"])
    launch = read(paper_run / "launch.json")
    manifests = sorted(gpu_run.glob("launch_*.json"))
    if len(manifests) > 100:
        raise ValueError("Too many benchmark manifests")
    launches = [read(path) for path in manifests]
    identifiers = [str(item.get("job_id", "")) for item in [launch, *launches]]
    if any(not gpu.report.JOB_ID.fullmatch(item) for item in identifiers):
        raise ValueError("Invalid recorded job ID")
    states, errors = query(sorted(set(identifiers)))
    paper_config = read(ROOT / launch.get("config_path", "config/paper_collection_2026-10-19.json"))
    observed = paper.collect_snapshot(paper_config, paper_run, now,
        query=lambda identifier: (states.get(str(identifier), {}), errors),
        previous=(previous or {}).get("paper", {}))
    jobs = []
    for manifest in launches:
        identifier = str(manifest["job_id"])
        result_path = gpu.report.result_path(manifest, gpu_run, ROOT).resolve()
        if not result_path.is_relative_to(gpu_run.resolve()):
            raise ValueError("Result path outside benchmark run")
        result = read(result_path)
        scheduler = states.get(identifier, {})
        jobs.append({"job_id": identifier,
                     "status": gpu.observed_status(manifest, scheduler, result),
                     "scheduler_state": scheduler.get("state"),
                     "gpus": manifest.get("requested_gpus"), "gpu_type": manifest.get("target_gpu"),
                     "measurement": result.get("throughput", {}),
                     "suite": result.get("suite", {})})
    return compact_snapshot({"paper": observed, "gpu_jobs": jobs, "scheduler_errors": errors})


def fingerprint(value):
    observed = value.get("paper", {})
    compact = {"paper": {key: observed.get(key) for key in
                          ("status", "stage", "stop_reason", "reason", "error_type")},
               "jobs": [{key: item.get(key) for key in ("job_id", "status", "scheduler_state")}
                        for item in value.get("gpu_jobs", [])],
               "monitor_error": value.get("monitor_error"),
               "scheduler_errors": value.get("scheduler_errors", [])}
    return hashlib.sha256(json.dumps(compact, sort_keys=True).encode()).hexdigest()


def all_terminal(value):
    return (value.get("paper", {}).get("status") in paper.TERMINAL
            and bool(value.get("gpu_jobs"))
            and all(item.get("status") in gpu.TERMINAL for item in value["gpu_jobs"]))


def message(config, observed, previous):
    return check_prompt_size(
        "The user explicitly requested progress every two hours in THIS chat, plus prompt completion/failure updates. "
        "Give a concise status update now, "
        "including whether the paper run and GPU benchmarks are running, queued, stopped, failed or complete. "
        "Read the current compact worker states and the exact recorded scheduler IDs before answering. "
        "For papers report processed/reused/new counts, token counts, artifact/download storage and any stop reason. "
        "For benchmarks report configurations and available measurements. State changes since the previous "
        "accepted update below where measurable, and state uncertainty honestly. This is a READ-ONLY status "
        "request: do not submit, resume, cancel, alter jobs, delete files, change budgets or publish Git changes. "
        "Queued acceptance does not prove an earlier update was displayed.\n"
        f"Paper run: {config['paper_run_directory']}\n"
        f"Benchmark run: {config['throughput_run_directory']}\n"
        "Latest observed status: " + json.dumps(compact_snapshot(observed), sort_keys=True,
                                               separators=(",", ":")) + "\n"
        "Previous accepted update observation: " + json.dumps(compact_snapshot(previous), sort_keys=True,
                                                             separators=(",", ":"))
    )


def enqueue(config, prompt):
    check_prompt_size(prompt)
    arguments = [config["codex_path"], "queue", "--thread", config["thread_id"], "--message", prompt]
    # No shell, resume invocation, new session, model override or message to others.
    with subprocess.Popen(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as process:
        try:
            code = process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            raise RuntimeError("Codex queue timed out") from None
    if code:
        raise RuntimeError(f"Codex queue exited {code}")
    return {"status": "accepted", "exit_code": 0}


def tick(config, state, observed, now, *, force=False, send=enqueue):
    state = dict(state)
    observed = compact_snapshot(observed)
    if state.get("last_accepted_snapshot") is not None:
        state["last_accepted_snapshot"] = compact_snapshot(state["last_accepted_snapshot"])
    if state.get("thread_id", config["thread_id"]) != config["thread_id"]:
        raise ValueError("Existing monitor belongs to another thread")
    state["thread_id"] = config["thread_id"]
    if state.get("monitor_status") == "stopped" and not force:
        return state
    started = state.setdefault("started_epoch", now)
    state["deadline_epoch"] = min(state.get("deadline_epoch", float("inf")),
                                  config["deadline_epoch"], started + MAX_SECONDS)
    interval = config.get("interval_seconds", 7200)
    if state.get("interval_seconds", 3600) != interval:
        # A user-requested cadence change keeps the last accepted update and
        # original deadline; restarting must not postpone updates repeatedly.
        state["next_due_epoch"] = state.get("last_accepted_epoch", now) + interval
    state["interval_seconds"] = interval
    state.setdefault("next_due_epoch", now + interval)
    current = fingerprint(observed)
    state.setdefault("last_accepted_fingerprint", current)
    terminal, expired = all_terminal(observed), now >= state["deadline_epoch"]
    due = (force or terminal or expired or state.get("pending_fingerprint") is not None
           or current != state["last_accepted_fingerprint"] or now >= state["next_due_epoch"])
    retry_ready = now >= state.get("retry_after_epoch", 0)
    if due and (retry_ready or force):
        state.update(last_attempt_epoch=now, pending_fingerprint=current)
        try:
            result = send(config, message(config, observed, state.get("last_accepted_snapshot")))
            if result.get("status") != "accepted" or result.get("exit_code") != 0:
                raise RuntimeError("Queue acceptance unconfirmed")
            state.update(last_accepted_epoch=now, last_accepted_fingerprint=current,
                         last_accepted_snapshot=observed, pending_fingerprint=None,
                         queue_error=None, retry_after_epoch=0,
                         next_due_epoch=now + interval,
                         accepted_count=state.get("accepted_count", 0) + 1)
        except (OSError, RuntimeError, subprocess.SubprocessError) as error:
            state.update(queue_error=queue_error(error), retry_after_epoch=now + RETRY_SECONDS)
    state.update(checked_epoch=now, observation=observed,
                 monitor_status="watching", delivery="queue_acceptance_only")
    if terminal and state.get("last_accepted_fingerprint") == current and state.get("last_accepted_epoch") is not None:
        state.update(monitor_status="stopped", stop_reason="all_work_terminal_final_update_accepted")
    elif expired:
        state.update(monitor_status="stopped", stop_reason="monitor_deadline")
    return state


@contextmanager
def lock(directory):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "queue.lock").open("a") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("Chat update monitor already running") from None
        (directory / "queue.pid").write_text(str(os.getpid()) + "\n")
        yield


def watch(config, *, once=False, force=False, clock=time.time, sleep=time.sleep,
          collect=snapshot, send=enqueue):
    directory = Path(config["run_directory"])
    stopping = False
    def stop(_signum, _frame):
        nonlocal stopping
        stopping = True
    for signum in (signal.SIGTERM, signal.SIGINT):
        signal.signal(signum, stop)
    with lock(directory):
        state = read(directory / "queue_state.json")
        while True:
            now = clock()
            if stopping or (directory / "STOP").exists():
                state.update(monitor_status="stopped", stop_reason="requested_stop", checked_epoch=now)
                paper.write_json(directory / "queue_state.json", state)
                return state
            try:
                observed = collect(config, now, state.get("observation"))
            except (OSError, ValueError, TypeError, KeyError, RuntimeError) as error:
                observed = {**state.get("observation", {}), "monitor_error": type(error).__name__}
            state = tick(config, state, observed, now, force=force, send=send)
            paper.write_json(directory / "queue_state.json", state)
            print(json.dumps({key: state.get(key) for key in
                              ("checked_epoch", "monitor_status", "last_accepted_epoch", "queue_error")}), flush=True)
            if once or state["monitor_status"] == "stopped":
                return state
            force = False
            sleep(min(config.get("poll_seconds", 60), max(0, state["deadline_epoch"] - clock())))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--force", action="store_true")
    arguments = parser.parse_args()
    watch(load_config(arguments.config), once=arguments.once, force=arguments.force)


if __name__ == "__main__":
    main()
