#!/usr/bin/env python3
"""Render compact, allowlisted status for the bounded native-paper collection."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
from src.corpus_progress_publish import publish_reports

PST = timezone(timedelta(hours=-8))
DEFAULT = "paper_collection_2026-10-19"
JOB_ID = re.compile(r"[0-9]+")
SAFE_WORD = re.compile(r"[A-Za-z0-9_ .:-]{1,100}")
TERMINAL = {"completed", "stopped", "failed"}
QUEUED = {"PENDING", "REQUEUED", "REQUEUE_HOLD", "REQUEUE_FED"}
FAILED = {"FAILED", "TIMEOUT", "OUT_OF_MEMORY", "NODE_FAIL", "BOOT_FAIL", "PREEMPTED", "DEADLINE", "REVOKED"}
ACTIVE = {"RUNNING", "CONFIGURING", "COMPLETING", "RESIZING", "SIGNALING", "STAGE_OUT", "SUSPENDED"}
COUNT_KEYS = ("reused_papers", "new_papers", "new_processed_papers", "rejected_papers", "known_id_skips", "raw_tokens",
              "exact_unique_tokens", "selected_tokens", "selected_exact_unique_tokens", "artifact_bytes",
              "network_bytes", "network_charged_bytes", "pipeline_bytes", "known_pmcids")
LIMIT_KEYS = ("runtime_seconds", "network_bytes", "new_artifact_bytes", "minimum_free_bytes", "maximum_pipeline_data_bytes")
INVENTORY_KEYS = ("native_xml_papers", "known_pmcids", "known_pmids", "known_dois")
STAGES = {
    "index_known_identifiers": "Indexing existing paper identifiers",
    "index_local_xml_metadata": "Checking existing XML metadata",
    "process_reused_xml": "Extracting existing XML papers",
    "discover_new_papers": "Finding missing papers",
    "acquire_missing_papers": "Downloading and processing missing papers",
    "finished": "Finished",
}
DELTA_LABELS = {"reused_papers": "existing papers", "new_papers": "new papers", "raw_tokens": "raw tokens",
                "exact_unique_tokens": "exact-unique tokens", "selected_tokens": "biology-selected tokens",
                "artifact_bytes": "artifact bytes", "network_bytes": "HTTP response bytes"}


def read_json(path):
    return json.loads(path.read_text()) if path.exists() else {}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")
    temporary.replace(path)


def timestamp(epoch):
    return datetime.fromtimestamp(epoch, PST).isoformat(timespec="seconds")


def number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0 else None


def word(value):
    return value if isinstance(value, str) and SAFE_WORD.fullmatch(value) else None


def epoch(value):
    if number(value) is not None:
        return value
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value)
            return parsed.timestamp() if parsed.tzinfo is not None else None
        except ValueError:
            pass
    return None


def query_scheduler(job_id, command=subprocess.run):
    """Read only the recorded allocation, with no queue-wide or node query."""
    if not JOB_ID.fullmatch(str(job_id)):
        return {}, []
    found, errors = {}, []
    for source, arguments in (
        ("sacct", ["sacct", "-n", "-P", "-X", "-j", str(job_id), "--format=JobIDRaw,State,ExitCode"]),
        ("squeue", ["squeue", "-h", "-j", str(job_id), "-o", "%i|%T"]),
    ):
        try:
            result = command(arguments, capture_output=True, text=True, timeout=15, check=True)
            if len(result.stdout) > 65536:
                raise ValueError("Scheduler response exceeded bound")
            for line in result.stdout.splitlines():
                fields = line.strip().split("|")
                if len(fields) >= 2 and fields[0] == str(job_id):
                    state = fields[1].split(" ", 1)[0].rstrip("+").upper()
                    found = {"state": state, "source": source}
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            errors.append({"source": source, "error_type": type(error).__name__})
    return found, errors


def collect_snapshot(config, run_dir, now, *, query=query_scheduler, previous=None):
    """Construct public data from fixed fields; source paths never cross this boundary."""
    previous = previous or {}
    launch = read_json(run_dir / "launch.json")
    worker = read_json(run_dir / "summary.json")
    state = read_json(run_dir / "state.json")
    job_id = str(launch.get("job_id", ""))
    scheduler, errors = query(job_id) if JOB_ID.fullmatch(job_id) else ({}, [])
    slurm = scheduler.get("state")
    worker_status = worker.get("status", state.get("status"))
    worker_status = "completed" if worker_status == "complete" else worker_status
    heartbeat = next((parsed for key in ("heartbeat_epoch", "updated_epoch", "updated_at_pst", "heartbeat_at_pst")
                      for value in (worker.get(key), state.get(key)) if (parsed := epoch(value)) is not None), None)
    age = max(0, now - heartbeat) if heartbeat is not None else None
    first_running = previous.get("first_running_epoch", now)
    status, reason = "not_submitted", None
    if slurm in QUEUED:
        status = "queued"
    elif slurm in FAILED:
        status, reason = "failed", slurm.lower()
    elif slurm == "CANCELLED":
        status, reason = "stopped", "scheduler_cancelled"
    elif slurm == "COMPLETED":
        status = worker_status if worker_status in TERMINAL else "failed"
        reason = None if worker_status in TERMINAL else "worker_final_status_missing"
    elif slurm in ACTIVE:
        if worker_status in TERMINAL:
            status = worker_status
        elif (age is not None and age > 180) or (age is None and now - first_running > 180):
            status, reason = "stalled", "worker_heartbeat_stale"
        else:
            status = "running"
    elif previous.get("scheduler_state") in FAILED | {"CANCELLED", "COMPLETED"}:
        status, reason = previous.get("status", "failed"), previous.get("reason")
    elif worker_status in TERMINAL:
        status = worker_status
    elif JOB_ID.fullmatch(job_id):
        status, reason = "stalled", "scheduler_unavailable"
    counters = dict(worker.get("counts", worker))
    events, inputs = worker.get("events", {}), worker.get("input_statuses", {})
    rejected = [number(inputs.get(kind, {}).get("rejected")) for kind in ("catalog", "candidates")]
    known_skips = [number(events.get(key)) for key in ("known_pmcid_skips", "known_secondary_identifier_skips")]
    counters.update(reused_papers=worker.get("reused_distinct_papers", worker.get("reused_processed_papers")), new_papers=worker.get("new_selected_papers"),
                    new_processed_papers=worker.get("new_processed_papers"),
                    rejected_papers=sum(value for value in rejected if value is not None) if any(value is not None for value in rejected) else None,
                    known_id_skips=sum(value for value in known_skips if value is not None) if any(value is not None for value in known_skips) else None,
                    artifact_bytes=worker.get("new_artifact_bytes"), network_bytes=worker.get("network_bytes"),
                    network_charged_bytes=worker.get("network_charged_bytes"),
                    known_pmcids=worker.get("known_identifier_counts", {}).get("pmcid"))
    baseline, added = number(config.get("existing_pipeline_bytes")), number(worker.get("new_artifact_bytes"))
    counters["pipeline_bytes"] = baseline + added if baseline is not None and added is not None else None
    counts = {key: number(counters.get(key)) for key in COUNT_KEYS}
    limits = config.get("limits", {})
    safe_limits = {key: number(limits.get(key)) for key in LIMIT_KEYS}
    inventory = {key: number(config.get("inventory", {}).get(key)) for key in INVENTORY_KEYS}
    output = {"run_id": word(config.get("run_id")) or DEFAULT,
              "checked_at_pst": timestamp(now), "checked_epoch": now, "status": status,
              "stage": word(worker.get("stage", state.get("stage"))), "reason": word(reason),
              "job_id": job_id if JOB_ID.fullmatch(job_id) else None,
              "scheduler_state": word(slurm), "scheduler_observed": bool(scheduler),
              "scheduler_errors": errors, "worker_heartbeat_age_seconds": age,
              "counts": counts, "limits": safe_limits, "inventory": inventory,
              "target_new_papers": number(config.get("target_new_papers")),
              "submitted_at_pst": timestamp(value) if (value := epoch(launch.get("submitted_at_pst"))) is not None else None,
              "deadline_at_pst": timestamp(value) if (value := epoch(state.get("deadline_epoch", worker.get("deadline_epoch")))) is not None else None,
              "stop_reason": word(worker.get("stop_reason", state.get("stop_reason"))),
              "error_type": word(worker.get("error", worker.get("error_type", state.get("error_type"))))}
    if slurm in ACTIVE:
        output["first_running_epoch"] = first_running
    return output


def empty_snapshot(config, now):
    """A valid safe report even when the first worker files cannot be read."""
    return {"run_id": word(config.get("run_id")) or DEFAULT, "checked_at_pst": timestamp(now),
            "checked_epoch": now, "status": "stalled", "stage": None, "reason": "monitor_read_failed",
            "counts": dict.fromkeys(COUNT_KEYS), "limits": {key: number(config.get("limits", {}).get(key)) for key in LIMIT_KEYS},
            "inventory": {key: number(config.get("inventory", {}).get(key)) for key in INVENTORY_KEYS},
            "target_new_papers": number(config.get("target_new_papers")), "job_id": None,
            "scheduler_state": None, "scheduler_observed": False, "scheduler_errors": []}


def display(value):
    return f"{value:,.0f}" if number(value) is not None else "—"


def gib(value):
    return f"{value / 2**30:.2f} GiB" if number(value) is not None else "—"


def build_report(config_path, run_dir, report_dir, *, root=ROOT, publish=False, snapshot=None, now=None):
    config = read_json(config_path)
    snapshot = snapshot or collect_snapshot(config, run_dir, time.time() if now is None else now)
    report_dir.mkdir(parents=True, exist_ok=True)
    counts, limits, inventory = snapshot["counts"], snapshot["limits"], snapshot["inventory"]
    lines = ["# Native-paper collection", "", f"**Status: {snapshot['status']}** · Updated {snapshot['checked_at_pst']} (fixed PST).", "",
             f"Process existing cluster XML first, then acquire up to **{display(snapshot['target_new_papers'])} additional papers** whose identifiers are absent from the known cluster inventory.", "",
             "| Measure | Current amount |", "|:--|--:|",
             f"| Existing native XML available | {display(inventory['native_xml_papers'])} papers |",
             f"| Known PMC identifiers checked before acquisition | {display(counts['known_pmcids'] if counts['known_pmcids'] is not None else inventory['known_pmcids'])} |"]
    for label, key in (("Existing papers processed", "reused_papers"), ("New papers processed", "new_processed_papers"),
                       ("New papers retained by biology rules", "new_papers"),
                       ("Metadata/parse rejections", "rejected_papers"), ("Candidates skipped because already present", "known_id_skips"),
                       ("Raw processed tokens", "raw_tokens"), ("Exact-unique processed tokens", "exact_unique_tokens"),
                       ("Biology-selected tokens before exact deduplication", "selected_tokens"),
                       ("Biology-selected exact-unique tokens", "selected_exact_unique_tokens")):
        lines.append(f"| {label} | {display(counts[key])} |")
    lines.extend([f"| New artifacts | {gib(counts['artifact_bytes'])} / {gib(limits['new_artifact_bytes'])} |",
                  f"| Counted pipeline storage | {gib(counts['pipeline_bytes'])} / {gib(limits['maximum_pipeline_data_bytes'])} |",
                  f"| Measured HTTP response bodies | {gib(counts['network_bytes'])} |",
                  f"| HTTP budget charged | {gib(counts['network_charged_bytes'])} / {gib(limits['network_bytes'])} |", "",
                  f"Job: {snapshot['job_id'] or 'not submitted'}; scheduler: {snapshot['scheduler_state'] or 'not observed'}; stage: {STAGES.get(snapshot['stage'], snapshot['stage'] or 'not started')}.", "",
                  f"The worker has an original {display(limits['runtime_seconds'] / 3600 if limits['runtime_seconds'] is not None else None)}-hour allowance, two CPU cores and zero GPUs. It stops at the first time, download, storage or candidate limit. The shared free-space floor is {gib(limits['minimum_free_bytes'])}.", ""])
    if snapshot.get("deadline_at_pst"):
        lines.extend([f"Worker deadline: {snapshot['deadline_at_pst']} (fixed PST).", ""])
    if snapshot.get("reason") or snapshot.get("stop_reason") or snapshot.get("error_type"):
        lines.extend(["Run detail: " + "; ".join(value for value in (
            snapshot.get("reason"), snapshot.get("stop_reason"), snapshot.get("error_type")) if value) + ".", ""])
    if snapshot["scheduler_errors"]:
        lines.extend(["Scheduler query incomplete; the observed status includes that uncertainty.", ""])
    if snapshot.get("watcher_status"):
        lines.extend([f"Monitor: {snapshot['watcher_status']}" + (f" ({snapshot['monitor_stop_reason']})" if snapshot.get("monitor_stop_reason") else "") + ".", ""])
    deltas = {key: value for key, value in snapshot.get("since_previous_report", {}).items()
              if key in DELTA_LABELS and isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)}
    delta_text = "Since the previous successful report: " + "; ".join(
        f"{value:+,.0f} {DELTA_LABELS[key]}" for key, value in deltas.items()) + "." if deltas else ""
    if delta_text:
        lines.extend([delta_text, ""])
    lines.extend(["Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.", "",
                  "Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.", "",
                  "An independent monitor refreshes this report hourly, including while queued, and on status changes. These are GitHub updates; automatic chat notifications are not configured.", ""])
    # Watcher bookkeeping remains private, including any future extra fields.
    public_keys = set(empty_snapshot(config, 0)) | {"worker_heartbeat_age_seconds", "submitted_at_pst",
                  "deadline_at_pst", "stop_reason", "error_type", "watcher_status", "monitor_stop_reason"}
    public = {key: value for key, value in snapshot.items() if key in public_keys}
    public["since_previous_report"] = deltas
    write_json(report_dir / "summary.json", public)
    (report_dir / "README.md").write_text("\n".join(lines))
    progress = f"Updated {snapshot['checked_at_pst']} (fixed PST).\n\nStatus: **{snapshot['status']}**. New papers: {display(counts['new_papers'])}; reused papers: {display(counts['reused_papers'])}; exact-unique tokens: {display(counts['exact_unique_tokens'])}.\n"
    if delta_text:
        progress += "\n" + delta_text + "\n"
    (report_dir / "progress.md").write_text(progress)
    return publish_reports(root, run_dir, report_dir) if publish else {"status": "rendered"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config" / f"{DEFAULT}.json")
    parser.add_argument("--run-dir", type=Path, default=ROOT / "experiments" / DEFAULT)
    parser.add_argument("--report-dir", type=Path, default=ROOT / "reports" / DEFAULT)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build_report(args.config, args.run_dir, args.report_dir, publish=args.publish)))


if __name__ == "__main__":
    main()
