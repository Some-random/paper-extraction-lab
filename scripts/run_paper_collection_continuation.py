#!/usr/bin/env python3
"""Storage-bounded native-paper continuation with preserved prior-run history."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import sqlite3
import sys
import time
import traceback
from urllib.parse import parse_qs, urlencode, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_paper_collection as base

ROOT = base.ROOT
CHECKPOINT_EXIT = 75


def resolve(path):
    path = Path(path)
    return path if path.is_absolute() else ROOT / path


def file_bytes(directory):
    return sum(p.stat().st_size for p in directory.rglob("*") if p.is_file())


def ensure_capacity(config, run, reserve=0):
    limits = config["limits"]
    control = limits.get("control_plane_reserve_bytes", 16 * base.MIB)
    free = shutil.disk_usage(run).free
    if free < limits["minimum_free_bytes"] + reserve + control:
        raise base.StopCollection("free_space_floor")
    if config["existing_pipeline_bytes"] + file_bytes(run) + reserve + control > limits["maximum_pipeline_data_bytes"]:
        raise base.StopCollection("pipeline_storage_limit")


def prepare(config_path):
    """Clone the stopped ledger; share durable old payloads through their locators."""
    config_path = Path(config_path).resolve()
    config = json.loads(config_path.read_text())
    prior = resolve(config["continuation"]["source_run"])
    run = resolve(config["destination"])
    run.mkdir(parents=True, exist_ok=True)
    with (run / "worker.lock").open("a") as target_lock, (prior / "worker.lock").open("rb") as prior_lock:
        fcntl.flock(target_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(prior_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if json.loads((prior / "state.json").read_text()).get("status") == "running":
            raise RuntimeError("Prior worker must be stopped before a continuation is prepared")
        source_db = prior / "papers.sqlite3"
        source_wal = prior / "papers.sqlite3-wal"
        if source_wal.exists() and source_wal.stat().st_size:
            raise RuntimeError("Prior ledger must be quiescent with no uncheckpointed WAL")
        for field in ("source_config", "source_summary"):
            path = resolve(config["continuation"][field])
            if base.sha256(path) != config["continuation"][field + "_sha256"]:
                raise ValueError("Frozen prior-run input changed: " + field)
        manifest = run / "continuation_preflight.json"
        target_db = run / "papers.sqlite3"
        if target_db.exists():
            if not manifest.exists():
                raise RuntimeError("Continuation ledger exists without a completed preparation manifest")
            old = json.loads(manifest.read_text())
            if old["config_sha256"] != base.sha256(config_path):
                raise ValueError("Continuation config changed after preparation")
            return old
        ensure_capacity(config, run, source_db.stat().st_size + 64 * base.MIB)
        source_hash = base.sha256(source_db)
        source = sqlite3.connect(source_db.as_uri() + "?mode=ro&immutable=1", uri=True)
        temporary = run / "papers.sqlite3.prepare"
        if temporary.exists():
            raise RuntimeError("An incomplete preparation exists; preserve and inspect it before retrying")
        target = sqlite3.connect(temporary)
        try:
            source.backup(target)
            if target.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                raise RuntimeError("Copied ledger failed SQLite integrity check")
            if target.execute("SELECT value FROM meta WHERE key='known_index_complete'").fetchone() != ("1",):
                raise RuntimeError("Prior identifier index is incomplete")
            if target.execute("SELECT COUNT(*) FROM catalog WHERE status IN ('pending','indexed')").fetchone()[0]:
                raise RuntimeError("Prior cached XML processing is incomplete")
            with target:
                target.execute("UPDATE meta SET value=? WHERE key='config_sha256'", (base.sha256(config_path),))
                target.execute("INSERT OR REPLACE INTO meta VALUES('continuation_source_ledger_sha256',?)", (source_hash,))
            pending = {row[0] for row in target.execute("SELECT pmcid FROM candidates WHERE status='pending'")}
            # Only interrupted candidates need their already-downloaded cache.
            # Hard links avoid payload duplication; later writes replace only
            # continuation links atomically and cannot overwrite prior files.
            linked_files = linked_bytes = 0
            old_raw = prior / "raw"
            if old_raw.exists():
                for directory in old_raw.iterdir():
                    if directory.name not in pending or not directory.is_dir():
                        continue
                    for cached in directory.iterdir():
                        if not cached.is_file() or cached.is_symlink() or cached.suffix == ".tmp":
                            continue
                        ensure_capacity(config, run, cached.stat().st_size)
                        destination = run / "raw" / directory.name / cached.name
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        os.link(cached, destination)
                        linked_files += 1
                        linked_bytes += cached.stat().st_size
            copied_counts = {
                "records": target.execute("SELECT COUNT(*) FROM records").fetchone()[0],
                "known_pmcids": target.execute("SELECT COUNT(*) FROM identifiers WHERE kind='pmcid'").fetchone()[0],
                "pending_candidates": len(pending),
            }
        finally:
            target.close()
            source.close()
        if base.sha256(source_db) != source_hash:
            raise RuntimeError("Prior ledger changed during continuation preparation")
        temporary.replace(target_db)
        result = {
            "prepared_at_pst": base.now(), "config_sha256": base.sha256(config_path),
            "source_ledger_sha256": source_hash, "source_ledger_unchanged": True,
            "source_run": str(prior), "copied_counts": copied_counts,
            "interrupted_cache_hardlinks": linked_files, "interrupted_cache_logical_bytes": linked_bytes,
            "initial_artifact_bytes": file_bytes(run), "shared_free_bytes": shutil.disk_usage(run).free,
            "prior_payloads": "Retained in place; copied records preserve original source/document/canonical locators",
            "scope": "Preparation only; no network requests, paper parsing or job submission",
        }
        manifest.write_text(json.dumps(result, indent=2) + "\n")
        return result


class ContinuationWorker(base.Worker):
    def initialize(self, config_path):
        self.config_path = Path(config_path).resolve()
        self.config = json.loads(self.config_path.read_text())
        self.run = self.resolve(self.config["destination"])
        self.run.mkdir(parents=True, exist_ok=True)
        self.lock = (self.run / "worker.lock").open("a")
        fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        preflight = json.loads((self.run / "continuation_preflight.json").read_text())
        if preflight["config_sha256"] != base.sha256(self.config_path):
            raise ValueError("Continuation config changed after preparation")
        if hasattr(os, "sched_getaffinity"):
            os.sched_setaffinity(0, set(sorted(os.sched_getaffinity(0))[:2]))
        self.limits = self.config["limits"]
        self.max_xml = self.limits.get("max_xml_bytes", 8 * base.MIB)
        self.max_text = self.limits.get("max_text_bytes", 4 * base.MIB)
        self.max_document = self.limits.get("max_document_gzip_bytes", 32 * base.MIB)
        self.catalog_path = self.resolve(self.config["source_catalog"])
        self.tokenizer_path = self.resolve(self.config["tokenizer_path"])
        for field in ("source_catalog", "presence_ids_csv"):
            if base.sha256(self.resolve(self.config[field])) != self.config[field + "_sha256"]:
                raise ValueError("Frozen input checksum mismatch: " + field)
        if base.sha256(self.tokenizer_path) != self.config["tokenizer_sha256"]:
            raise ValueError("Pinned tokenizer checksum mismatch")
        self.tokenizer = base.Tokenizer.from_file(str(self.tokenizer_path))
        self.ledger = base.CollectionLedger(self.run / "papers.sqlite3", {
            "config_sha256": base.sha256(self.config_path), "catalog_sha256": base.sha256(self.catalog_path),
            "tokenizer_sha256": self.config["tokenizer_sha256"],
        })
        self.state_path = self.run / "state.json"
        self.state = json.loads(self.state_path.read_text()) if self.state_path.exists() else {
            "run_id": self.config["run_id"], "started_at_pst": base.now(), "started_epoch": time.time(),
            "network_charged_bytes": 0, "network_body_bytes": 0,
        }
        self.state.update(pid=os.getpid(), status="running", error=None, stop_reason=None,
                          deadline_epoch=None, stop_at_pst=None, runtime_policy="Storage-bounded across allocation checkpoints")
        self.signalled = self.allocation_checkpoint = False
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda *_: setattr(self, "signalled", True))
        signal.signal(signal.SIGUSR1, lambda *_: setattr(self, "allocation_checkpoint", True))
        self.session = base.requests.Session()
        self.session.headers.update({"User-Agent": "paper-extraction-lab/PMC-storage-continuation (serial)", "Accept-Encoding": "identity"})
        self.last_publish = self.last_ncbi = 0
        self.reserved_artifacts = 0
        self.non_database_bytes = sum(p.stat().st_size for p in self.run.rglob("*") if p.is_file() and not p.name.startswith("papers.sqlite3"))
        overrides = self.resolve(self.config.get("citation_metadata_path", "config/pmc_citation_metadata.json"))
        self.overrides = json.loads(overrides.read_text())["papers"] if overrides.exists() else {}
        self.persist()

    def guard(self, reserve=0):
        if self.signalled or (self.run / "STOP").exists():
            raise base.StopCollection("stop_requested")
        if self.allocation_checkpoint:
            raise base.StopCollection("allocation_checkpoint")
        reserve += self.limits.get("control_plane_reserve_bytes", 16 * base.MIB)
        free = shutil.disk_usage(self.run).free
        self.state["filesystem_free_bytes"] = free
        if free < self.limits["minimum_free_bytes"] + reserve:
            raise base.StopCollection("free_space_floor")
        current = self.artifact_bytes()
        if current + self.reserved_artifacts + reserve > self.limits["new_artifact_bytes"]:
            raise base.StopCollection("artifact_limit")
        if self.config["existing_pipeline_bytes"] + current + self.reserved_artifacts + reserve > self.limits["maximum_pipeline_data_bytes"]:
            raise base.StopCollection("pipeline_storage_limit")

    def publish(self, force=False):
        before = self.last_publish
        super().publish(force=force)
        if self.last_publish == before:
            return
        target = self.run / "summary.json"
        previous = target.stat().st_size
        summary = json.loads(target.read_text())
        baseline = self.config["continuation"]["baseline_counts"]
        summary["continuation"] = self.config["continuation"]
        summary["new_since_continuation"] = {
            "processed_papers": summary["new_processed_papers"] - baseline["new_processed_papers"],
            "selected_papers": summary["new_selected_papers"] - baseline["new_selected_papers"],
            "raw_tokens": summary["raw_tokens"] - baseline["raw_tokens"],
            "selected_exact_unique_tokens": summary["selected_exact_unique_tokens"] - baseline["selected_exact_unique_tokens"],
        }
        summary["target_new_papers"] = None
        summary["pipeline_data_bytes"] = self.config["existing_pipeline_bytes"] + self.artifact_bytes()
        raw = (json.dumps(summary, indent=2) + "\n").encode()
        temporary = target.with_suffix(".json.tmp")
        temporary.write_bytes(raw)
        temporary.replace(target)
        self.non_database_bytes += len(raw) - previous

    def discover_next(self):
        """Append one versioned search subset after the current candidate pool drains."""
        discovery = self.config["continuation_discovery"]
        retmax = discovery["candidates_per_query"]
        if not 1 <= retmax <= 10000:
            raise ValueError("PMC retmax must be between 1 and 10000")
        for first, last in discovery["query_years"]:
            for topic, terms in self.config["query_topics"].items():
                name = f"{discovery['version']}:{topic}:{first}:{last}:r{retmax}"
                if self.ledger.db.execute("SELECT 1 FROM queries WHERE name=?", (name,)).fetchone():
                    continue
                self.stage("discover_new_papers")
                term = "(" + " OR ".join(word + "[tiab]" for word in terms) + ")"
                term += f' AND {first}:{last}[pdat] AND (open_access[filter] OR author_manuscript[filter]) NOT "pmc embargo"[filter] NOT (articletyperetraction OR articletypecorrection OR hasretractionin)'
                url = base.ESEARCH + "?" + urlencode({"db": "pmc", "term": term, "retmode": "json", "retmax": retmax, "tool": "paper_extraction_lab"})
                raw = self.fetch(url, self.run / "queries" / (base.digest(name.encode()) + ".json"), 2 * base.MIB)
                result = json.loads(raw)
                found = result["esearchresult"]
                if result.get("error") or found.get("error") or found.get("errorlist") or found.get("warninglist", {}).get("quotedphrasesnotfound"):
                    raise ValueError("PMC discovery query was not accepted exactly")
                ids = [base.identifier("pmcid", value) for value in found["idlist"]]
                if None in ids:
                    raise ValueError("PMC returned an invalid identifier")
                ids.sort(key=lambda uid: base.digest((name + uid).encode()))
                self.guard(8 * base.MIB)
                with self.ledger.db:
                    for rank, uid in enumerate(ids):
                        self.ledger.db.execute("INSERT OR IGNORE INTO candidates(pmcid,stratum,sampling_rank) VALUES(?,?,?)", (uid, name, rank))
                    self.ledger.db.execute("INSERT INTO queries VALUES(?,?)", (name, json.dumps({
                        "url": url, "query": term, "matches": int(found["count"]), "returned": len(ids),
                        "response_sha256": base.digest(raw), "selection": "Convenience search subset; not probability sampling",
                    })))
                self.publish()
                if self.ledger.db.execute("SELECT 1 FROM candidates WHERE status='pending' LIMIT 1").fetchone():
                    return True
        return False

    def acquire_candidate(self, pmcid):
        self.state["current_pmcid"] = pmcid
        source_meta = None
        try:
            if self.ledger.known({"pmcid": pmcid}):
                with self.ledger.db:
                    self.ledger.finish("candidates", pmcid, "known", "pmcid_already_present")
                    self.ledger.event("known_pmcid_skips")
                return
            directory = self.run / "raw" / pmcid
            metadata = self.metadata(pmcid, directory)
            ids = {kind: metadata.get(kind) for kind in ("pmcid", "pmid", "doi")}
            if self.ledger.known(ids):
                with self.ledger.db:
                    self.ledger.finish("candidates", pmcid, "known", "pmid_or_doi_already_present")
                    self.ledger.event("known_secondary_identifier_skips")
                return
            url = base.public_url(metadata["xml_url"])
            source_path = directory / "source.xml"
            cached = source_path.exists()
            raw = self.fetch(url, source_path, self.max_xml)
            manifest_path = directory / "source_manifest.json"
            if not (cached and manifest_path.exists()):
                self.write(manifest_path, (json.dumps({
                    "source_url": url, "source_xml_sha256": base.digest(raw), "bytes": len(raw),
                    "metadata_sha256": base.digest(json.dumps(metadata, sort_keys=True).encode()),
                    "fetched_at_pst": base.now(), "cached_response": cached,
                }) + "\n").encode())
            expected = parse_qs(urlsplit(url).query).get("md5", [None])[0]
            if not expected or hashlib.md5(raw).hexdigest().casefold() != expected.casefold():
                raise base.RejectPaper("distributed_xml_md5_missing_or_mismatch")
            source_meta = base.native_metadata(raw, pmcid)
            for kind in ("pmid", "doi"):
                if base.identifier(kind, ids.get(kind)) and source_meta["identifiers"].get(kind) and base.identifier(kind, ids[kind]) != source_meta["identifiers"][kind]:
                    raise base.RejectPaper("distributed_xml_identifier_mismatch")
            self.process(source_path, pmcid, "new", "candidates", pmcid, upstream=metadata)
        except (base.RejectPaper, ValueError, base.etree.XMLSyntaxError) as exc:
            reason = str(exc) if isinstance(exc, base.RejectPaper) else type(exc).__name__
            with self.ledger.db:
                if source_meta:
                    self.ledger.seed(source_meta["identifiers"], "rejected_downloaded_xml")
                self.ledger.finish("candidates", pmcid, "rejected", reason)
                self.ledger.event("new_paper_rejections")

    def new(self):
        while True:
            self.guard()
            candidate = self.ledger.db.execute("SELECT pmcid FROM candidates WHERE status='pending' ORDER BY sampling_rank,ordinal LIMIT 1").fetchone()
            if not candidate:
                if self.discover_next():
                    continue
                self.state["completion_reason"] = "expanded_candidate_scope_exhausted"
                return
            self.stage("acquire_missing_papers", candidate[0])
            self.acquire_candidate(candidate[0])
            self.publish()

    def execute(self):
        try:
            self.publish(force=True)
            self.guard()
            self.new()
            self.state.update(status="complete", stage="finished")
        except base.StopCollection as exc:
            self.state.update(status="stopped", stop_reason=str(exc))
        except base.TransportUnavailable as exc:
            self.state.update(status="failed", stop_reason="network_unavailable", error=type(exc).__name__)
            traceback.print_exc()
        except Exception as exc:
            self.state.update(status="failed", error=type(exc).__name__)
            traceback.print_exc()
        finally:
            self.publish(force=True)
            self.close()
        if self.state.get("stop_reason") == "allocation_checkpoint":
            return CHECKPOINT_EXIT
        return 1 if self.state["status"] == "failed" else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    if args.prepare_only:
        print(json.dumps(prepare(args.config), indent=2))
        return 0
    return ContinuationWorker(args.config).execute()


if __name__ == "__main__":
    raise SystemExit(main())
