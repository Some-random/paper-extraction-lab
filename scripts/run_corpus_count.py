#!/usr/bin/env python3
"""One bounded, restartable worker: acquire full shards, verify, count and dedup."""
from __future__ import annotations

import argparse
import fcntl
import io
import importlib.metadata
import json
import os
import shutil
import signal
import socket
import sys
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["OPENBLAS_NUM_THREADS"] = "2"
os.environ["MKL_NUM_THREADS"] = "2"
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import requests
import zstandard
from tokenizers import Tokenizer
from corpus_count import Ledger, MODALITIES, inspect_text, sha256

PST = timezone(timedelta(hours=-8))


def now():
    return datetime.now(PST).isoformat()


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


class StopWork(Exception):
    pass


class Worker:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = json.loads(config_path.read_text())
        self.run = ROOT / self.config["destination"]
        self.run.mkdir(parents=True, exist_ok=True)
        self.lock = (self.run / "worker.lock").open("a")
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit("A counting worker already holds this run's lock.") from None
        if hasattr(os, "sched_getaffinity"):
            os.sched_setaffinity(0, set(sorted(os.sched_getaffinity(0))[:2]))
        tokenizer_path = ROOT / self.config["tokenizer_path"]
        if sha256(tokenizer_path) != self.config["tokenizer_sha256"]:
            raise ValueError("Pinned tokenizer checksum mismatch")
        self.tokenizer = Tokenizer.from_file(str(tokenizer_path))
        self.ledger = Ledger(self.run / "counts.sqlite3", sha256(config_path), self.config["tokenizer_sha256"])
        self.ledger.register(self.config["files"])
        state_path = self.run / "state.json"
        self.state = json.loads(state_path.read_text()) if state_path.exists() else {
            "started_at_pst": now(), "network_reserved_bytes": 0,
            "network_body_bytes": 0, "counting_seconds": 0,
        }
        self.state.update(pid=os.getpid(), status="running", error=None)
        self.state.pop("stop_reason", None)
        self.state.setdefault("execution_history", []).append({
            "started_at_pst": now(), "pid": os.getpid(), "host": socket.gethostname(),
            "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
            "python": sys.version.split()[0],
            "packages": {name: importlib.metadata.version(name) for name in ("tokenizers", "zstandard", "requests", "PySocks")},
            "counting_code_sha256": sha256(ROOT / "src/corpus_count.py"),
            "runner_code_sha256": sha256(Path(__file__)),
        })
        self.deadline = datetime.fromisoformat(self.state["started_at_pst"]).timestamp() + self.config["limits"]["runtime_seconds"]
        self.state["stop_at_pst"] = datetime.fromtimestamp(self.deadline, PST).isoformat()
        self.last_storage_check = 0
        self.last_published = 0
        self.signalled = False
        signal.signal(signal.SIGTERM, lambda *_: setattr(self, "signalled", True))
        signal.signal(signal.SIGINT, lambda *_: setattr(self, "signalled", True))
        self.persist()

    def persist(self):
        self.state["updated_at_pst"] = now()
        write_json(self.run / "state.json", self.state)

    def guard(self):
        if self.signalled or (self.run / "STOP").exists():
            raise StopWork("stop_requested")
        if time.time() >= self.deadline:
            raise StopWork("runtime_limit")
        if time.monotonic() - self.last_storage_check >= 15:
            self.last_storage_check = time.monotonic()
            free = shutil.disk_usage(self.run).free
            size = sum(p.stat().st_size for p in self.run.rglob("*") if p.is_file())
            self.state.update(filesystem_free_bytes=free, new_artifact_bytes=size)
            if free < self.config["limits"]["minimum_free_bytes"]:
                raise StopWork("free_space_floor")
            if size >= self.config["limits"]["new_artifact_bytes"]:
                raise StopWork("artifact_limit")

    def acquire(self, item):
        path = ROOT / item["path"]
        if path.exists():
            if path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
                raise ValueError("Existing input failed size/checksum validation: " + item["id"])
            return path
        if "url" not in item:
            raise FileNotFoundError("Local canonical input missing")
        path.parent.mkdir(parents=True, exist_ok=True)
        partial = path.with_suffix(path.suffix + ".part")
        self.ledger.status(item["id"], "downloading")
        for attempt in range(3):
            self.guard()
            start = partial.stat().st_size if partial.exists() else 0
            remaining = item["bytes"] - start
            if remaining < 0:
                raise ValueError("Partial download is larger than the frozen input")
            if remaining == 0:
                break
            limits = self.config["limits"]
            if self.state["network_reserved_bytes"] + remaining > limits["network_reserved_bytes"]:
                raise StopWork("network_budget")
            if self.state["new_artifact_bytes"] + remaining + 16 * 2**20 > limits["new_artifact_bytes"]:
                raise StopWork("artifact_budget_for_next_shard")
            # Persist the whole request reservation before I/O. A crash can
            # overcount this conservative budget, never silently reset it.
            self.state["network_reserved_bytes"] += remaining
            self.persist()
            headers = {"Accept-Encoding": "identity", "User-Agent": "paper-extraction-lab/corpus-census"}
            if start:
                headers["Range"] = f"bytes={start}-"
            try:
                with requests.get(item["url"], params={"download": "true", "census": int(time.time())},
                                  headers=headers, stream=True, timeout=(15, 35)) as response:
                    response.raise_for_status()
                    if response.headers.get("Content-Encoding", "identity") != "identity":
                        raise ValueError("Unexpected transport encoding")
                    if start and (response.status_code != 206 or not response.headers.get(
                            "Content-Range", "").startswith(f"bytes {start}-")):
                        raise ValueError("Server did not honor download resume range")
                    if not start and response.status_code != 200:
                        raise ValueError("Unexpected full-object response")
                    expected = int(response.headers.get("Content-Length", "0"))
                    if expected and expected != remaining:
                        raise ValueError("Response size differs from frozen manifest")
                    with partial.open("ab") as handle:
                        while remaining:
                            self.guard()
                            data = response.raw.read(min(2**20, remaining), decode_content=False)
                            if not data:
                                break
                            handle.write(data)
                            remaining -= len(data)
                            self.state["network_body_bytes"] += len(data)
                            if time.monotonic() - self.last_published >= 30:
                                self.publish()
                    if remaining:
                        raise OSError("Incomplete response body; partial input retained")
                break
            except (requests.RequestException, OSError) as exc:
                self.state["last_transport_error"] = type(exc).__name__
                self.persist()
                if attempt == 2:
                    raise RuntimeError("Download failed after three attempts; partial input retained") from None
                time.sleep(2)
        if partial.stat().st_size != item["bytes"] or sha256(partial) != item["sha256"]:
            raise ValueError("Downloaded input failed size/checksum validation")
        partial.replace(path)
        self.ledger.status(item["id"], "downloaded")
        self.publish()
        return path

    def count(self, item, path):
        _, cursor = self.ledger.file_state(item["id"])
        self.ledger.status(item["id"], "counting")
        rows = []
        batch_started = time.monotonic()
        number = 0
        with path.open("rb") as raw:
            decoded = zstandard.ZstdDecompressor().stream_reader(raw, read_across_frames=True) if item["format"] == "jsonl.zst" else raw
            stream = io.BufferedReader(decoded)
            try:
                while True:
                    self.guard()
                    line = stream.readline(self.config["limits"]["maximum_line_bytes"] + 1)
                    if not line:
                        break
                    number += 1
                    if len(line) > self.config["limits"]["maximum_line_bytes"]:
                        raise ValueError("Oversized JSONL row; not silently truncated")
                    if number <= cursor:
                        batch_started = time.monotonic()
                        continue
                    if not line.strip():
                        continue
                    record = json.loads(line)
                    if not isinstance(record, dict) or not isinstance(record.get("text"), str) or not record["text"].strip():
                        raise ValueError(f"Invalid/empty text at physical row {number}")
                    if len(record["text"].encode("utf-8")) > self.config["limits"]["maximum_text_bytes"]:
                        raise ValueError(f"Oversized text at row {number}; no truncation")
                    measured = inspect_text(record["text"], self.tokenizer)
                    provenance = {k: record[k] for k in ("id", "global_id", "url", "date", "doi", "license", "version",
                        "source_xml_sha256", "source_document", "source_document_sha256", "images", "token_count") if k in record}
                    rows.append((number, measured, provenance))
                    if len(rows) >= 250 or time.monotonic() - batch_started >= 10:
                        self.ledger.append(item, rows)
                        self.state["counting_seconds"] += time.monotonic() - batch_started
                        rows.clear()
                        batch_started = time.monotonic()
                        if time.monotonic() - self.last_published >= 30:
                            self.publish()
            finally:
                # Even a stop/error retains previously validated rows. A bad row
                # remains unconsumed and will be revisited on resume.
                if rows:
                    self.ledger.append(item, rows)
                    self.state["counting_seconds"] += time.monotonic() - batch_started
                stream.close()
        if item.get("expected_records") is not None:
            count = self.ledger.db.execute("SELECT COUNT(*) FROM records WHERE file_id=?", (item["id"],)).fetchone()[0]
            if count != item["expected_records"]:
                raise ValueError("Record count differs from frozen local paper count")
        self.ledger.status(item["id"], "complete")
        self.publish()

    def publish(self):
        self.persist()
        totals = self.ledger.totals()
        files = {row[0]: {"status": row[1], "rows_committed": row[2], "error": row[3]} for row in
                 self.ledger.db.execute("SELECT id,status,cursor,error FROM files")}
        aggregate, categories = Counter(), {}
        routes = {route: Counter({metric: 0 for metric in ("raw_records", "raw_tokens", "unique_records", "unique_tokens")})
                  for route in ("online_papers", "web_urls", "existing_datasets")}
        sources = {}
        for key, info in self.config["sources"].items():
            metrics = totals.get(key, {})
            aggregate.update(metrics)
            route = routes.setdefault(info["acquisition_route"], Counter())
            category = categories.setdefault(info["content_category"], Counter())
            for k in ("raw_records", "raw_tokens", "unique_records", "unique_tokens"):
                route[k] += metrics.get(k, 0)
                category[k] += metrics.get(k, 0)
            relevant = [f for f in self.config["files"] if f["source"] == key]
            completed = sum(files[f["id"]]["status"] == "complete" for f in relevant)
            sources[key] = {**info, **metrics, "completed_files": completed,
                            "complete_frozen_input_scan": completed == info["expected_files"],
                            "available_raw_bytes": sum(f["bytes"] for f in relevant)}
        coverage = []
        for family in self.config["source_families"]:
            key = family["id"]
            status = "requires_source_adapter_or_release_inventory"
            if key in sources:
                status = "counting_partial" if sources[key].get("raw_records", 0) else "queued"
                if sources[key]["complete_frozen_input_scan"]:
                    status = "complete_frozen_input_scan" if sources[key]["whole_source_inventory"] else "local_selected_papers_counted"
            elif family["group"] == "general":
                status = "outside_biology_total"
            elif family["group"] == "raw":
                status = "secondary_raw_modality_not_counted"
            elif family["upstream_of"]:
                status = "upstream_of_bundle_incremental_coverage_unmeasured"
            coverage.append({**family, "counting_status": status})
        elapsed = self.state["counting_seconds"]
        for basis in ("raw", "unique"):
            assert sum(aggregate.get(basis + "_" + kind + "_tokens", 0) for kind in MODALITIES) == aggregate.get(basis + "_tokens", 0)
        summary = {
            "run_id": self.config["run_id"], **self.state,
            "tokenizer_path": self.config["tokenizer_path"], "tokenizer_sha256": self.config["tokenizer_sha256"],
            "tokenizer_identity": self.config["tokenizer_identity"],
            "sources": sources, "totals": dict(aggregate), "acquisition_routes": routes,
            "content_categories": categories, "files": files, "source_coverage": coverage,
            "counting_tokens_per_second": aggregate.get("raw_tokens", 0) / elapsed if elapsed else None,
            "final_retained_biology_tokens": None, "near_deduplicated_tokens": None,
            "image_tokens": None, "whole_available_biology_total": None,
            "counting_policy": self.config["counting_policy"], "limits": self.config["limits"],
        }
        write_json(self.run / "summary.json", summary)
        report = ROOT / self.config["report_directory"]
        report.mkdir(parents=True, exist_ok=True)
        write_json(report / "summary.json", summary)
        title = "# Measured biological-corpus candidate tokens"
        body = [title, "", f"Snapshot: {self.state['updated_at_pst']} (fixed PST). Worker status: **{self.state['status']}**.", "",
            "Actual counts in the pinned counting tokenizer, without added special tokens. These are scanned candidate records; the full available biological corpus and its final retained total remain unmeasured.",
            "",
            "| Content | Records scanned | Raw tokens | Tokens after exact deduplication | Complete files / inventory |",
            "|:---|---:|---:|---:|---:|"]
        for key, info in sources.items():
            body.append(f"| {info['name']} | {info.get('raw_records',0):,} | {info.get('raw_tokens',0):,} | {info.get('unique_tokens',0):,} | {info['completed_files']} / {info['expected_files']} |")
        body.append(f"| **Measured total** | **{aggregate.get('raw_records',0):,}** | **{aggregate.get('raw_tokens',0):,}** | **{aggregate.get('unique_tokens',0):,}** | |")
        body.extend(["", "## Modality partition of tokens after exact deduplication", "",
                     "| Explicit content | Tokens |", "|:---|---:|"])
        for kind in MODALITIES:
            body.append(f"| {kind.replace('_',' ')} | {aggregate.get('unique_' + kind + '_tokens',0):,} |")
        body.extend(["", "The modality rows sum to the deduplicated total. Only explicit sequence/molecule tags identify those spans; untagged sequences remain unclassified. Image pixels are retained in existing paper assets; vision-token counts are unknown.",
            "", "## What this scan measures", "",
            "- PMC is the frozen local collection, not a PMC-wide count. Each paper contributes its selected text, captions/notes and tables once; chunk and interleaved copies are excluded.",
            "- FineFineWeb is imported web-origin text; TheBioCollection is imported database-record text. Both have acquisition route `existing_datasets`. Route and content totals are alternative breakdowns of the same records.",
            "- Deduplication compares SHA-256 after whitespace collapse across all scanned sources, preserving case and punctuation. The first record in the frozen order supplies the unique tokens. Distinct annotations survive. Near duplicates and paper versions with different text remain unresolved.",
            "- No biology/clinical scope classifier, quality filter, new OCR or training has run. A source's biology label is not validation of every record.",
            "- Source coverage tracks all " + str(len(coverage)) + " inventoried families. A database appearing inside a bundle is not a separate measured export or an additional token total.",
            "", "[Counting setup and commands](../../docs/corpus_counting.md) · [Processing recipe](../bio_foundation_review_2026-10-15/data_pipeline.md)"])
        (report / "README.md").write_text("\n".join(body) + "\n")
        coverage_lines = ["# Source coverage for the measured census", "",
            f"Snapshot: {self.state['updated_at_pst']} (fixed PST).", "",
            "Every inventoried family is listed. A dash means unmeasured, not zero. Upstream resources are not counted again as independent exports.", "",
            "| Source family | Coverage | Scanned candidate tokens | Tokens after exact deduplication |",
            "|:---|:---|---:|---:|"]
        labels = {
            "requires_source_adapter_or_release_inventory": "Release inventory / adapter required",
            "counting_partial": "Partial scan", "queued": "Queued",
            "complete_frozen_input_scan": "Complete frozen release inventory scanned",
            "local_selected_papers_counted": "Local selected papers counted",
            "outside_biology_total": "Outside biological total",
            "secondary_raw_modality_not_counted": "Secondary raw-modality pool; unmeasured",
            "upstream_of_bundle_incremental_coverage_unmeasured": "Upstream of a bundle; independent coverage unmeasured",
        }
        for family in coverage:
            info = sources.get(family["id"], {})
            raw_count = f"{info['raw_tokens']:,}" if info.get("raw_records") else "—"
            unique_count = f"{info['unique_tokens']:,}" if info.get("raw_records") else "—"
            coverage_lines.append(f"| {family['name']} | {labels[family['counting_status']]} | {raw_count} | {unique_count} |")
        coverage_lines.extend(["", "[Measured totals](README.md) · [Counting setup](../../docs/corpus_counting.md)"])
        (report / "source_coverage.md").write_text("\n".join(coverage_lines) + "\n")
        with (report / "README.md").open("a") as handle:
            handle.write("\n[Coverage of all 87 source families](source_coverage.md).\n")
        self.last_published = time.monotonic()
        print(json.dumps({"at_pst": self.state["updated_at_pst"], "status": self.state["status"],
                          "file": self.state.get("current_file"), "raw_tokens": aggregate.get("raw_tokens", 0),
                          "unique_tokens": aggregate.get("unique_tokens", 0), "records": aggregate.get("raw_records", 0)}), flush=True)

    def execute(self, local_only=False):
        try:
            self.publish()
            for item in self.config["files"]:
                if local_only and "url" in item:
                    continue
                self.guard()
                if self.ledger.file_state(item["id"])[0] == "complete":
                    continue
                self.state["current_file"] = item["id"]
                self.publish()
                path = self.acquire(item)
                self.count(item, path)
            self.state["status"] = "local_scan_complete" if local_only else "frozen_inventory_scan_complete"
        except StopWork as exc:
            self.state.update(status="stopped", stop_reason=str(exc))
        except Exception as exc:
            self.state.update(status="failed", error=f"{type(exc).__name__}: {exc}" if not isinstance(exc, requests.RequestException) else type(exc).__name__)
            if self.state.get("current_file"):
                self.ledger.status(self.state["current_file"], "failed", self.state["error"])
            raise
        finally:
            self.publish()
            self.ledger.close()
            self.lock.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config/corpus_count_2026-10-17.json")
    parser.add_argument("--local-only", action="store_true")
    args = parser.parse_args()
    Worker(args.config).execute(args.local_only)


if __name__ == "__main__":
    main()
