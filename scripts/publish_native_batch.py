#!/usr/bin/env python3
"""Publish only the compact batch index once the serial worker finishes.

No documents are processed and no network requests occur while waiting. Other
staged files are excluded from the commit. A branch change or push failure is
recorded locally rather than triggering merges/rebases or a branch switch.
"""
import argparse
import csv
import json
import subprocess
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PST = timezone(timedelta(hours=-8))
TERMINAL = {"completed", "limited", "failed", "candidate_pool_exhausted"}


def command(*args):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=120, check=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--once", action="store_true", help="Check status and exit; never commit or push")
    args = ap.parse_args()
    config = json.loads(args.config.read_text())
    batch = ROOT / config["destination"]
    report = ROOT / config["report_directory"]
    status_path = batch / "publication_status.json"
    deadline = time.monotonic() + (config["maximum_runtime_hours"] + 1) * 3600
    state = {}
    while time.monotonic() < deadline:
        state = json.loads((batch / "state.json").read_text())
        if args.once:
            print(json.dumps({"worker_status": state["status"], "papers": len(state["papers"]), "published": False}))
            return
        if state["status"] in TERMINAL:
            break
        time.sleep(30)
    else:
        raise RuntimeError("Worker did not finish within the bounded publication window")
    # persist() writes state, then the compact report; wait for a consistent
    # terminal snapshot instead of publishing a still-changing CSV.
    for _ in range(10):
        time.sleep(2)
        summary = json.loads((report / "summary.json").read_text())
        with (report / "papers.csv").open() as f:
            rows = list(csv.DictReader(f))
        if summary["status"] == state["status"] and len(rows) == summary["ready_papers"] == len(state["papers"]):
            break
    else:
        raise RuntimeError("Final paper manifest and summary disagree")
    if command("git", "branch", "--show-current") != "main":
        raise RuntimeError("Repository branch changed; publication deferred")
    paths = [str((report / name).relative_to(ROOT)) for name in ["README.md", "summary.json", "papers.csv"]]
    diff = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", *paths], cwd=ROOT)
    if diff.returncode == 1:
        command("git", "commit", "--only", "-m", f"Publish native biology batch: {len(rows)} papers, {state['status']}", "--", *paths)
    elif diff.returncode:
        raise RuntimeError("Could not inspect final report diff")
    command("git", "push", "origin", "main")
    commit = command("git", "rev-parse", "HEAD")
    remote = command("git", "ls-remote", "origin", "refs/heads/main").split()[0]
    if commit != remote:
        raise RuntimeError("Remote commit verification failed")
    status_path.write_text(json.dumps({"status": "published", "papers": len(rows),
        "worker_status": state["status"], "commit": commit,
        "published_at_pst": datetime.now(PST).isoformat()}, indent=2) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # Keep errors concise; subprocess output can contain transport details.
        error = {"status": "failed", "error": type(exc).__name__ + ": " + str(exc)[:250],
                 "at_pst": datetime.now(PST).isoformat()}
        import sys
        try:
            cfg = json.loads(Path(sys.argv[sys.argv.index("--config") + 1]).read_text())
            (ROOT / cfg["destination"] / "publication_status.json").write_text(json.dumps(error, indent=2) + "\n")
        finally:
            print(json.dumps(error))
        raise SystemExit(1)
