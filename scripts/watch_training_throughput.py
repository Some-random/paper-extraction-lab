#!/usr/bin/env python3
"""Monitor only recorded benchmark jobs; publish hourly and on state changes.

This CPU-only watcher never submits, cancels, releases or extends SLURM jobs.
Saved/GitHub reports do not deliver proactive chat notifications.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

import report_training_throughput as report

TERMINAL = {"success", "failed", "cancelled"}
QUEUED = {"PENDING", "REQUEUED", "REQUEUE_FED", "REQUEUE_HOLD", "SPECIAL_EXIT"}
RUNNING = {"RUNNING", "COMPLETING", "CONFIGURING", "RESIZING", "SIGNALING", "STAGE_OUT", "SUSPENDED", "STOPPED"}
FAILED = {"BOOT_FAIL", "DEADLINE", "FAILED", "NODE_FAIL", "OUT_OF_MEMORY", "PREEMPTED", "REVOKED", "TIMEOUT"}
SETUP_TERMINAL = {"setup_failed", "setup_cancelled", "ready_jobs_released", "ready", "completed"}


def timestamp(epoch):
    return datetime.fromtimestamp(epoch, report.PST).isoformat(timespec="seconds")


def scheduler_command(arguments):
    """Spool bounded command output, avoiding potentially unbounded pipe buffering."""
    with tempfile.TemporaryFile() as output:
        process = subprocess.Popen(arguments, stdout=output, stderr=subprocess.STDOUT)
        try:
            code = process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            raise RuntimeError(f"{arguments[0]} exceeded 20 seconds") from None
        if code:
            raise RuntimeError(f"{arguments[0]} returned exit code {code}")
        if output.tell() > 128 * 1024:
            raise RuntimeError(f"{arguments[0]} exceeded output bound")
        output.seek(0)
        return output.read().decode("utf-8", errors="replace")


def normalized_slurm(state):
    # sacct can append a truncation '+' or a cancellation UID to the state.
    return state.strip().split(" ", 1)[0].rstrip("+").upper()


def query_scheduler(job_ids, command=scheduler_command):
    """Query exactly the allowlisted launch IDs, never a user's whole queue."""
    if not job_ids:
        return {}, []
    if any(not report.JOB_ID.fullmatch(value) for value in job_ids):
        raise ValueError("Invalid benchmark job ID")
    joined = ",".join(job_ids)
    allowed, queued, accounted, errors = set(job_ids), {}, {}, []
    commands = (
        ("squeue", ["squeue", "--noheader", "--jobs", joined, "--format=%i|%T|%r"]),
        ("sacct", ["sacct", "--noheader", "--parsable2", "--allocations", "--jobs", joined,
                   "--format=JobIDRaw,State,ExitCode"]),
    )
    for kind, arguments in commands:
        try:
            output = command(arguments)
        except (OSError, RuntimeError, subprocess.SubprocessError) as error:
            errors.append({"source": kind, "error_type": type(error).__name__})
            continue
        for line in output.splitlines():
            fields = line.strip().split("|")
            if len(fields) < 2 or fields[0] not in allowed:
                continue  # No job steps, unexpected IDs or unrecorded jobs.
            target = queued if kind == "squeue" else accounted
            target[fields[0]] = {"state": normalized_slurm(fields[1]), "source": kind}
            if kind == "squeue" and len(fields) > 2:
                target[fields[0]]["reason"] = fields[2]
            if kind == "sacct" and len(fields) > 2:
                target[fields[0]]["exit_code"] = fields[2]
    # The current queue wins over potentially delayed accounting entries.
    return {**accounted, **queued}, errors


def observed_status(launch, scheduler, result):
    state = scheduler.get("state") if scheduler else None
    if not scheduler and launch.get("slurm_state") in FAILED | {"CANCELLED", "COMPLETED"}:
        # A later accounting outage cannot resurrect a terminal allocation from
        # a stale initializing/result file. Keep its last terminal observation.
        state = launch["slurm_state"]
    if state == "CANCELLED":
        return "cancelled"
    if state in FAILED:
        return "failed"
    if state in QUEUED:
        return "queued"
    if state in RUNNING:
        return "running"
    if state == "COMPLETED":
        return "success" if result and result.get("status") == "completed" else "failed"
    # Accounting can lag. Retained output is useful when the queue has forgotten
    # a job, but an observed terminal scheduler state always takes precedence.
    previous = str(launch.get("status", "queued")).lower()
    if previous == "cancelled":
        return previous
    if result:
        output_status = result.get("status")
        if output_status == "completed":
            return "success"
        if output_status in {"failed", "runtime_limit"}:
            return "failed"
        if output_status == "initializing":
            return "running"
    return {"pending": "queued", "submitted": "queued", "completed": "success",
            "runtime_limit": "failed"}.get(previous, previous)


def collect_snapshot(run_dir, root, now, query=query_scheduler):
    manifests = sorted(run_dir.glob("launch*.json"))
    if len(manifests) > 100:
        raise ValueError("Unexpectedly many benchmark manifests")
    launches, seen = [], set()
    for path in manifests:
        launch = report.read_json(path)
        job_id = str(launch.get("job_id", ""))
        if not report.JOB_ID.fullmatch(job_id) or job_id in seen:
            raise ValueError(f"Invalid or duplicate job ID in {path.name}")
        seen.add(job_id)
        launches.append((path, launch))
    states, errors = query(sorted(seen))
    admission_path = run_dir / "admission_state.json"
    admission = report.read_json(admission_path) if admission_path.exists() else {}
    jobs = []
    for path, launch in launches:
        job_id = str(launch["job_id"])
        output = report.result_path(launch, run_dir, root)
        if not output.resolve().is_relative_to(run_dir.resolve()):
            raise ValueError(f"Result path is outside the benchmark run for job {job_id}")
        result = report.read_json(output) if output.exists() else None
        scheduler = states.get(job_id)
        status = observed_status(launch, scheduler, result)
        if status not in TERMINAL | {"queued", "running"}:
            raise ValueError(f"Unsupported benchmark status for job {job_id}: {status}")
        job = {"job_id": job_id, "status": status,
               "scheduler_state": scheduler.get("state") if scheduler else None,
               "scheduler_observed": scheduler is not None,
               "requested_gpus": launch.get("requested_gpus"),
               "target_gpu": launch.get("target_gpu")}
        job.update({key: launch[key] for key in ("admission_status", "hold_reason", "comparison_group") if key in launch})
        admission_job = admission.get("jobs", {}).get(job_id, {})
        if launch.get("admission_required") and admission_job:
            admission_status = admission_job.get("status", "waiting_spare_capacity")
            if (admission.get("stop_reason") == "admission_runtime_limit"
                    and admission_status not in {"released", "already_started", "terminal"}):
                admission_status = "expired"
            job["admission_status"] = admission_status
            if admission_status in {"released", "already_started", "terminal"}:
                job.pop("hold_reason", None)
        if scheduler:
            job.update({key: scheduler[key] for key in ("source", "reason", "exit_code") if key in scheduler})
        if result:
            job["result_status"] = result.get("status")
            job["failure_type"] = result.get("failure_type")
            job["input_tokens_per_second"] = result.get("throughput", {}).get("input_tokens_per_second")
        # Refresh only this recorded manifest; re-read to retain concurrent worker
        # fields. Slurm status beats stale launch status, including cancellation.
        fresh = report.read_json(path)
        fresh.update(status=status, status_checked_at_pst=timestamp(now),
                     scheduler_observed=scheduler is not None)
        if "admission_status" in job:
            fresh["admission_status"] = job["admission_status"]
            if "hold_reason" not in job:
                fresh.pop("hold_reason", None)
        if scheduler:
            fresh.update(slurm_state=scheduler["state"], scheduler_source=scheduler["source"])
        report.write_json(path, fresh)
        jobs.append(job)
    setup_path = run_dir / "setup_state.json"
    setup = report.read_json(setup_path) if setup_path.exists() else {}
    return {"checked_at_pst": timestamp(now), "checked_epoch": now,
            "setup": {key: setup[key] for key in ("stage", "error_type", "updated_at_pst") if key in setup},
            "scheduler_errors": errors, "jobs": jobs,
            "admission": {key: admission[key] for key in
                          ("checked_at_pst", "supervisor_status", "stop_reason") if key in admission}}


def meaningful_fingerprint(snapshot):
    value = {"setup": {key: snapshot.get("setup", {}).get(key) for key in ("stage", "error_type")},
             "scheduler_errors": snapshot.get("scheduler_errors", []),
             "jobs": snapshot.get("jobs", []), "stop_reason": snapshot.get("stop_reason")}
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def terminal_snapshot(snapshot):
    jobs = snapshot.get("jobs", [])
    setup_stage = snapshot.get("setup", {}).get("stage")
    return setup_stage in SETUP_TERMINAL and all(job["status"] in TERMINAL for job in jobs)


def publication_due(previous, snapshot, now, interval=3600):
    fingerprint = meaningful_fingerprint(snapshot)
    changed = fingerprint != previous.get("last_report_fingerprint")
    retry_at = previous.get("last_report_attempt_epoch", -float("inf")) + 300
    if previous.get("last_report_error") and not changed and now < retry_at:
        return False
    return (changed or now - previous.get("last_report_epoch", -float("inf")) >= interval
            or bool(previous.get("last_report_error") and now >= retry_at))


@contextmanager
def watcher_lock(run_dir):
    run_dir.mkdir(parents=True, exist_ok=True)
    with (run_dir / "watcher.lock").open("a") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("A benchmark status watcher is already running") from None
        handle.seek(0)
        handle.truncate()
        handle.write(str(os.getpid()) + "\n")
        handle.flush()
        yield


def watch(run_dir, report_dir, *, root=report.ROOT, publish=False, interval=3600,
          poll_seconds=30, max_days=7, clock=time.time, sleep=time.sleep,
          query=query_scheduler, renderer=report.build_report):
    with watcher_lock(run_dir):
        status_path = run_dir / "status.json"
        previous = report.read_json(status_path) if status_path.exists() else {}
        started = previous.get("watcher_started_epoch", clock())
        deadline = min(previous.get("watcher_deadline_epoch", float("inf")), started + max_days * 86400)
        while True:
            now = clock()
            collection_failed = False
            try:
                snapshot = collect_snapshot(run_dir, root, now, query=query)
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                collection_failed = True
                snapshot = {"checked_at_pst": timestamp(now), "checked_epoch": now,
                            "setup": previous.get("setup", {}), "jobs": previous.get("jobs", []),
                            "scheduler_errors": [{"source": "watcher", "error_type": type(error).__name__}]}
            stop = "all_known_work_terminal" if not collection_failed and terminal_snapshot(snapshot) else None
            if now >= deadline:
                stop = "watcher_runtime_limit"
            snapshot.update(watcher_started_epoch=started, watcher_deadline_epoch=deadline,
                            watcher_status="stopped" if stop else "watching", stop_reason=stop,
                            delivery="Local status files and optional GitHub reports; a separate session monitor queues chat updates")
            for key in ("last_report_epoch", "last_report_attempt_epoch", "last_report_error", "last_report_fingerprint"):
                if key in previous:
                    snapshot[key] = previous[key]
            due = publication_due(previous, snapshot, now, interval)
            # Save the observation before rendering: reports can surface query errors.
            report.write_json(status_path, snapshot)
            if due:
                snapshot["last_report_attempt_epoch"] = now
                snapshot["last_report_fingerprint"] = meaningful_fingerprint(snapshot)
                try:
                    rendered = renderer(run_dir, report_dir, root=root, publish_requested=publish)
                    snapshot.update(last_report_epoch=now, last_report_error=None, report_result=rendered)
                except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
                    snapshot["last_report_error"] = {"error_type": type(error).__name__}
                    if stop and now < deadline:
                        snapshot["watcher_status"] = "retrying_final_publication"
                report.write_json(status_path, snapshot)
                with (run_dir / "status_history.jsonl").open("a") as history:
                    history.write(json.dumps(snapshot, sort_keys=True, allow_nan=False) + "\n")
                print(json.dumps({"checked_at_pst": snapshot["checked_at_pst"],
                                  "watcher_status": snapshot["watcher_status"], "jobs": snapshot.get("jobs", []),
                                  "report_error": snapshot.get("last_report_error")}), flush=True)
            previous = snapshot
            # A transient git/report failure must not silently lose the final
            # update. Retry at five-minute cadence within the original deadline.
            if stop and (not snapshot.get("last_report_error") or now >= deadline):
                return snapshot
            sleep(min(poll_seconds, max(0, deadline - clock())))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, default=report.ROOT / report.DEFAULT_RUN)
    parser.add_argument("--report-dir", type=Path, default=report.ROOT / report.DEFAULT_REPORT)
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--poll-seconds", type=float, default=30)
    parser.add_argument("--report-seconds", type=float, default=3600)
    parser.add_argument("--max-days", type=float, default=7)
    args = parser.parse_args()
    if not 10 <= args.poll_seconds <= 60 or not 60 <= args.report_seconds <= 3600 or not 0 < args.max_days <= 7:
        parser.error("Require 10–60 second polls, 60–3600 second reports and at most seven days")
    try:
        watch(args.run_dir, args.report_dir, publish=args.publish, interval=args.report_seconds,
              poll_seconds=args.poll_seconds, max_days=args.max_days)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        parser.exit(1, f"Benchmark watcher failed: {type(error).__name__}: {error}\n")


if __name__ == "__main__":
    main()
