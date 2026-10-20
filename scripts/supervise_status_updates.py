#!/usr/bin/env python3
"""Keep the existing status reporters and same-chat timer in one CPU allocation."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def reporter_commands(config, config_path):
    interval = config.get("interval_seconds", 7200)
    if not isinstance(interval, int) or not 60 <= interval <= 7200:
        raise ValueError("Require 60–7200 second reporting interval")
    papers = [sys.executable, "-B", "-u", str(ROOT / "scripts/watch_paper_collection.py"),
              "--publish", "--report-seconds", str(interval), "--max-hours", "168"]
    for key, option in (("paper_config_path", "--config"), ("paper_run_directory", "--run-dir"),
                        ("paper_report_directory", "--report-dir")):
        if config.get(key):
            papers += [option, str(config[key])]
    return {
        "papers": papers,
        "throughput": [sys.executable, "-B", "-u", str(ROOT / "scripts/watch_training_throughput.py"),
                       "--publish", "--report-seconds", str(interval)],
        "chat": [sys.executable, "-B", "-u", str(ROOT / "scripts/queue_chat_updates.py"),
                 "--config", str(config_path)],
    }


def supervise(config_path):
    config = json.loads(config_path.read_text())
    directory = Path(config["run_directory"])
    directory = directory if directory.is_absolute() else ROOT / directory
    directory.mkdir(parents=True, exist_ok=True)
    deadline = config["deadline_epoch"]
    commands = reporter_commands(config, config_path)
    stop = False

    def request_stop(*_):
        nonlocal stop
        stop = True

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    children, finished, retry_at = {}, set(), {}
    with (directory / "supervisor.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        (directory / "supervisor.pid").write_text(str(os.getpid()) + "\n")
        try:
            while not stop and time.time() < deadline:
                now = time.time()
                for name, command in commands.items():
                    child = children.get(name)
                    if child is not None and child.poll() is not None:
                        code = child.returncode
                        del children[name]
                        if code == 0:
                            finished.add(name)
                        else:
                            retry_at[name] = now + 60
                        print(json.dumps({"component": name, "exit_code": code}), flush=True)
                    if name not in children and name not in finished and now >= retry_at.get(name, 0):
                        with (directory / (name + ".log")).open("ab") as log:
                            children[name] = subprocess.Popen(command, cwd=ROOT, stdout=log,
                                                              stderr=subprocess.STDOUT)
                snapshot = {"status": "watching", "updated_epoch": now, "deadline_epoch": deadline,
                            "children": {name: child.pid for name, child in children.items()},
                            "finished": sorted(finished), "retry_at": retry_at}
                temporary = directory / "supervisor_state.json.tmp"
                temporary.write_text(json.dumps(snapshot, indent=2) + "\n")
                temporary.replace(directory / "supervisor_state.json")
                if len(finished) == len(commands):
                    break
                time.sleep(min(10, max(0, deadline - time.time())))
        finally:
            for child in children.values():
                if child.poll() is None:
                    child.terminate()
            for child in children.values():
                try:
                    child.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait()
            snapshot = {"status": "stopped", "updated_epoch": time.time(), "deadline_epoch": deadline,
                        "reason": "stop_requested" if stop else "all_reporters_finished" if len(finished) == len(commands) else "original_deadline"}
            (directory / "supervisor_state.json").write_text(json.dumps(snapshot, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    supervise(args.config.resolve())


if __name__ == "__main__":
    main()
