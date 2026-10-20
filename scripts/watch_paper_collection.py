#!/usr/bin/env python3
"""Monitor one paper allocation and publish two-hour progress plus state changes."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import time

import report_paper_collection as report


def meaningful_fingerprint(snapshot):
    # Counters/heartbeats progress continuously. Publish those at the requested interval, with
    # immediate delivery reserved for status, stage and failure transitions.
    value = {key: snapshot.get(key) for key in (
        "status", "stage", "scheduler_state", "reason", "stop_reason", "error_type", "scheduler_errors")}
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def publication_due(previous, snapshot, now, interval=3600):
    changed = meaningful_fingerprint(snapshot) != previous.get("last_report_fingerprint")
    if previous.get("last_report_error") and not changed:
        return now >= previous.get("last_report_attempt_epoch", 0) + 300
    return changed or now >= previous.get("last_report_epoch", -float("inf")) + interval


def report_deltas(previous_counts, current_counts):
    return {key: current_counts[key] - previous_counts[key] for key in report.DELTA_LABELS
            if report.number(previous_counts.get(key)) is not None
            and report.number(current_counts.get(key)) is not None}


@contextmanager
def watcher_lock(run_dir):
    run_dir.mkdir(parents=True, exist_ok=True)
    with (run_dir / "watcher.lock").open("a") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("A paper collection watcher is already running") from None
        (run_dir / "watcher.pid").write_text(str(os.getpid()) + "\n")
        yield


def watch(config_path, run_dir, report_dir, *, root=report.ROOT, publish=False,
          interval=3600, poll_seconds=60, max_hours=48, clock=time.time, sleep=time.sleep,
          query=report.query_scheduler, renderer=report.build_report):
    with watcher_lock(run_dir):
        status_path = run_dir / "watcher_status.json"
        previous = report.read_json(status_path)
        started = previous.get("watcher_started_epoch", clock())
        deadline = min(previous.get("watcher_deadline_epoch", float("inf")), started + max_hours * 3600)
        while True:
            now = clock()
            config = {}
            try:
                config = report.read_json(config_path)
                snapshot = report.collect_snapshot(config, run_dir, now,
                                                   query=query, previous=previous)
            except (OSError, ValueError, TypeError) as error:
                # Preserve last safe observation on malformed/partial private
                # state; never copy an exception message or raw traceback.
                snapshot = {**report.empty_snapshot(config, now), **previous,
                            "checked_at_pst": report.timestamp(now), "checked_epoch": now,
                            "status": "stalled", "reason": "monitor_read_failed", "error_type": type(error).__name__}
            terminal = snapshot["status"] in report.TERMINAL
            stop = "worker_terminal" if terminal else None
            if now >= deadline:
                stop = "monitor_runtime_limit"
            snapshot.update(watcher_started_epoch=started, watcher_deadline_epoch=deadline,
                            watcher_status="stopped" if stop else "watching", monitor_stop_reason=stop)
            for key in ("last_report_epoch", "last_report_attempt_epoch", "last_report_fingerprint", "last_report_error", "last_report_counts"):
                if key in previous:
                    snapshot[key] = previous[key]
            if publication_due(previous, snapshot, now, interval):
                snapshot["last_report_attempt_epoch"] = now
                snapshot["last_report_fingerprint"] = meaningful_fingerprint(snapshot)
                snapshot["since_previous_report"] = report_deltas(previous.get("last_report_counts", {}), snapshot.get("counts", {}))
                try:
                    result = renderer(config_path, run_dir, report_dir, root=root, publish=publish, snapshot=snapshot)
                    if result.get("status") == "failed":
                        raise RuntimeError("Report publication failed")
                    snapshot.update(last_report_epoch=now, last_report_error=None, last_report_counts=snapshot.get("counts", {}).copy())
                except (OSError, ValueError, RuntimeError) as error:
                    snapshot["last_report_error"] = {"error_type": type(error).__name__}
                print(json.dumps({"checked_at_pst": snapshot["checked_at_pst"], "status": snapshot["status"],
                                  "watcher_status": snapshot["watcher_status"],
                                  "report_error": snapshot.get("last_report_error")}), flush=True)
            report.write_json(status_path, snapshot)
            if stop and (not snapshot.get("last_report_error") or now >= deadline):
                return snapshot
            previous = snapshot
            sleep(min(poll_seconds, max(0, deadline - clock())))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=report.ROOT / "config" / f"{report.DEFAULT}.json")
    parser.add_argument("--run-dir", type=Path, default=report.ROOT / "experiments" / report.DEFAULT)
    parser.add_argument("--report-dir", type=Path, default=report.ROOT / "reports" / report.DEFAULT)
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--poll-seconds", type=float, default=60)
    parser.add_argument("--report-seconds", type=float, default=7200)
    parser.add_argument("--max-hours", type=float, default=48)
    args = parser.parse_args()
    if not 10 <= args.poll_seconds <= 60 or not 60 <= args.report_seconds <= 7200 or not 0 < args.max_hours <= 168:
        parser.error("Require 10–60 second polls, 60–7200 second reports and at most 168 hours")
    watch(args.config, args.run_dir, args.report_dir, publish=args.publish,
          interval=args.report_seconds, poll_seconds=args.poll_seconds, max_hours=args.max_hours)


if __name__ == "__main__":
    main()
