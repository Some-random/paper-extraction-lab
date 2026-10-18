"""Durable hourly progress snapshots; delivery is the caller's responsibility."""
from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

PST = timezone(timedelta(hours=-8))
METRICS = ("raw_records", "raw_tokens", "unique_records", "unique_tokens")
TERMINAL = {"stopped", "failed", "complete", "completed", "cancelled",
            "local_scan_complete", "frozen_inventory_scan_complete"}


def _atomic_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def _counts(value):
    return {key: value.get(key, 0) for key in METRICS}


def _phase(summary):
    current = summary.get("current_file")
    if summary.get("status") in TERMINAL:
        return summary["status"].replace("_", " ")
    if current == "pmc_candidate_discovery":
        return "Discovering native papers"
    if current and current.startswith("acquiring_"):
        return "Acquiring native paper"
    status = summary.get("files", {}).get(current, {}).get("status")
    return (status or summary.get("status", "unknown")).replace("_", " ")


def _gib(value):
    return "Unknown" if value is None else f"{value / 2**30:,.2f} GiB"


def render_progress(event):
    totals, delta = event["totals"], event["delta"]
    label = "Final" if event["kind"] == "terminal" else event["kind"].capitalize()
    lines = ["# Corpus progress", "",
             f"**{label} update · {event['at_pst']} (fixed PST)**", "",
             f"Status: **{event['status']}**. Stage: **{event['phase']}**.",
             f"Worker snapshot: {event.get('source_updated_at_pst') or 'Not recorded'}.",
             f"Current / last input: `{event.get('current_file') or 'None'}`.", "",
             f"**{totals['raw_records']:,} records; {totals['raw_tokens']:,} candidate tokens; "
             f"{totals['unique_tokens']:,} tokens after exact deduplication.**"]
    if delta is not None:
        lines.append(f"Since the previous update ({event['elapsed_seconds'] / 60:,.1f} minutes): "
                     f"{delta['raw_records']:+,} records, {delta['raw_tokens']:+,} candidate tokens, "
                     f"{delta['unique_tokens']:+,} exact-unique tokens.")
    else:
        lines.append("No earlier progress snapshot was recorded for comparison.")
    papers = event.get("papers")
    if papers:
        lines.extend(["", f"Selected papers: **{papers['selected_papers']:,}** "
                      f"(**{papers['new_selected_papers']:,} newly selected**); "
                      f"{papers['scope_excluded_acquired_papers']:,} acquired candidates excluded from that selection."])
    lines.extend(["", "| Content / source | Records | Candidate tokens | Exact-unique tokens | Change in exact-unique tokens |",
                  "|:---|---:|---:|---:|---:|"])
    for source in event["sources"].values():
        change = source.get("delta_unique_tokens")
        label = f"{source['content_category'].replace('_', ' ')} / {source['name']}".replace("|", "/")
        lines.append(f"| {label} | {source['raw_records']:,} | {source['raw_tokens']:,} | "
                     f"{source['unique_tokens']:,} | {change:+,} |" if change is not None else
                     f"| {label} | {source['raw_records']:,} | {source['raw_tokens']:,} | {source['unique_tokens']:,} | — |")
    resources = event["resources"]
    lines.extend(["", f"Downloaded response bodies: **{_gib(resources['network_body_bytes'])}**. "
                  f"Run artifacts: **{_gib(resources['new_artifact_bytes'])}**. "
                  f"Filesystem free at the source snapshot: **{_gib(resources['filesystem_free_bytes'])}**.",
                  f"Original run deadline: {event.get('stop_at_pst') or 'Not recorded'}."])
    if event.get("stop_reason"):
        lines.append(f"Stop reason: **{event['stop_reason']}**.")
    if event.get("error"):
        lines.append(f"Error: {event['error']}")
    lines.extend(["", "These are candidate counts before quality filtering, full biology/clinical selection and near-duplicate removal. "
                  "Only exact duplicates have been removed from the exact-unique total; final usable biology tokens remain unmeasured.", ""])
    return "\n".join(lines)


class ProgressReporter:
    """Single-writer reporter with restart-safe cadence and recoverable writes.

    A pending event is saved before journal/report writes. A failed write can be
    retried by the next ``emit`` without losing a notification or duplicating its
    journal entry. Exceptions propagate so the caller can record/report delivery
    problems separately from acquisition. This class performs no network I/O.
    """

    def __init__(self, run_dir, report_dir, interval_seconds=3600):
        if interval_seconds <= 0:
            raise ValueError("Progress interval must be positive")
        self.run_dir, self.report_dir = Path(run_dir), Path(report_dir)
        self.interval_seconds = interval_seconds
        self.state_path = self.run_dir / "progress_state.json"
        self.events_path = self.run_dir / "progress_events.jsonl"

    def _save(self, state):
        _atomic_text(self.state_path, json.dumps(state, indent=2) + "\n")

    def _flush(self, state):
        event = state.get("pending_event")
        if event is None:
            return
        # Hourly journals are small. Atomic replacement also prevents a killed
        # writer from leaving a partial JSONL record that breaks later retries.
        events = [json.loads(line) for line in self.events_path.read_text().splitlines()] if self.events_path.exists() else []
        if not any(item["event_id"] == event["event_id"] for item in events):
            events.append(event)
            _atomic_text(self.events_path, "".join(json.dumps(item) + "\n" for item in events))
        _atomic_text(self.report_dir / "progress.md", render_progress(event))
        state.pop("pending_event")
        self._save(state)

    def emit(self, summary, *, now_epoch=None):
        """Return a new/recovered event, or None when no update is due."""
        current_time = time.time() if now_epoch is None else now_epoch
        run_id = summary.get("run_id", self.run_dir.name)
        state = json.loads(self.state_path.read_text()) if self.state_path.exists() else {"run_id": run_id}
        if state["run_id"] != run_id:
            raise ValueError("Progress state belongs to another run")
        recovered = state.get("pending_event")
        self._flush(state)
        previous = state.get("last_event")
        terminal = summary.get("status") in TERMINAL
        fingerprint = hashlib.sha256(json.dumps({"status": summary.get("status"),
            "stop_reason": summary.get("stop_reason"), "error": summary.get("error"),
            "totals": _counts(summary.get("totals", {}))}, sort_keys=True).encode()).hexdigest()
        if terminal:
            if previous and previous["kind"] == "terminal" and previous["fingerprint"] == fingerprint:
                return recovered
            kind = "terminal"
        elif previous is None or previous["kind"] == "terminal":
            kind = "start"
        elif current_time - previous["at_epoch"] >= self.interval_seconds:
            kind = "hourly"
        else:
            return recovered
        totals = _counts(summary.get("totals", {}))
        delta = {key: totals[key] - previous["totals"][key] for key in METRICS} if previous else None
        sources = {}
        for key, value in summary.get("sources", {}).items():
            sources[key] = {"name": value.get("name", key), "content_category": value.get("content_category", key),
                            **_counts(value)}
            sources[key]["delta_unique_tokens"] = (sources[key]["unique_tokens"] -
                previous["sources"].get(key, {}).get("unique_tokens", 0)) if previous else None
        event = {"run_id": run_id, "kind": kind, "at_epoch": current_time,
            "at_pst": datetime.fromtimestamp(current_time, PST).isoformat(),
            "source_updated_at_pst": summary.get("updated_at_pst"), "status": summary.get("status", "unknown"),
            "phase": _phase(summary), "current_file": summary.get("current_file"),
            "totals": totals, "delta": delta,
            "elapsed_seconds": current_time - previous["at_epoch"] if previous else None,
            "sources": sources, "content_categories": summary.get("content_categories", {}),
            "resources": {key: summary.get(key) for key in ("network_body_bytes", "new_artifact_bytes", "filesystem_free_bytes")},
            "stop_at_pst": summary.get("stop_at_pst"), "stop_reason": summary.get("stop_reason"),
            "error": summary.get("error"), "fingerprint": fingerprint}
        if "pmc" in sources:
            expansion = summary.get("paper_expansion", {})
            excluded = expansion.get("scope_excluded_acquired_papers", 0)
            event["papers"] = {"selected_papers": sources["pmc"]["raw_records"] - excluded,
                "new_selected_papers": expansion.get("accepted_new_papers", 0),
                "scope_excluded_acquired_papers": excluded}
        event["event_id"] = hashlib.sha256(json.dumps({"run_id": run_id, "kind": kind,
            "at_epoch": current_time, "fingerprint": fingerprint}, sort_keys=True).encode()).hexdigest()
        state.update(last_event=event, pending_event=event)
        self._save(state)
        self._flush(state)
        return event
