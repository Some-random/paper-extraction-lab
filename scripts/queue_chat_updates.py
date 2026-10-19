#!/usr/bin/env python3
"""Queue requested hourly status checks into one existing Codex thread.

This monitor reads only the recorded paper/benchmark jobs. Queue acceptance is
recorded separately from message delivery; it never starts a Codex session.
"""
from __future__ import annotations

import argparse
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
    if not 60 <= config.get("interval_seconds", 3600) <= 3600:
        raise ValueError("Require 60–3600 second interval")
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
    return {"paper": observed, "gpu_jobs": jobs, "scheduler_errors": errors}


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
    return (
        "The user explicitly requested hourly progress in THIS chat. Give a concise status update now, "
        "including whether the paper run and GPU benchmarks are running, queued, stopped, failed or complete. "
        "Read the current compact worker states and the exact recorded scheduler IDs before answering. "
        "For papers report processed/reused/new counts, token counts, artifact/download storage and any stop reason. "
        "For benchmarks report configurations and available measurements. State changes since the previous "
        "accepted update below where measurable, and state uncertainty honestly. This is a READ-ONLY status "
        "request: do not submit, resume, cancel, alter jobs, delete files, change budgets or publish Git changes. "
        "Queued acceptance does not prove an earlier update was displayed.\n"
        f"Paper run: {config['paper_run_directory']}\n"
        f"Benchmark run: {config['throughput_run_directory']}\n"
        "Latest observed status: " + json.dumps(observed, sort_keys=True) + "\n"
        "Previous accepted update observation: " + json.dumps(previous, sort_keys=True)
    )


def enqueue(config, prompt):
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
    if state.get("thread_id", config["thread_id"]) != config["thread_id"]:
        raise ValueError("Existing monitor belongs to another thread")
    state["thread_id"] = config["thread_id"]
    if state.get("monitor_status") == "stopped" and not force:
        return state
    started = state.setdefault("started_epoch", now)
    state["deadline_epoch"] = min(state.get("deadline_epoch", float("inf")),
                                  config["deadline_epoch"], started + MAX_SECONDS)
    state.setdefault("next_due_epoch", now + config.get("interval_seconds", 3600))
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
                         next_due_epoch=now + config.get("interval_seconds", 3600),
                         accepted_count=state.get("accepted_count", 0) + 1)
        except (OSError, RuntimeError, subprocess.SubprocessError) as error:
            state.update(queue_error={"error_type": type(error).__name__}, retry_after_epoch=now + RETRY_SECONDS)
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
