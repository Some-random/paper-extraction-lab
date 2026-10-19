#!/usr/bin/env python3
"""Bounded, serial reuse-first PMC collection; all payloads and locators stay private."""
from __future__ import annotations

import argparse
import csv
import fcntl
import gzip
import hashlib
import json
import os
import re
import shutil
import signal
import sqlite3
import sys
import time
import traceback
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit

import requests
from lxml import etree
from tokenizers import Tokenizer
from urllib3.exceptions import HTTPError as RawHTTPError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from corpus_count import canonical_paper_text, inspect_text, sha256
from native_training import parse_jats
from pmc_count_expansion import (ESEARCH, S3, biology_markers,
                                 choose_metadata, clinical_title_reason, public_url)

PST = timezone(timedelta(hours=-8))
MIB = 2**20
DEFAULT_TYPES = ["research-article", "review-article", "methods-article", "brief-report"]


def now():
    return datetime.now(PST).isoformat()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def identifier(kind, value):
    value = str(value or "").strip()
    if not value:
        return None
    if kind == "pmcid":
        match = re.fullmatch(r"(?:PMC)?([0-9]+)(?:\.[0-9]+)?", value, re.I)
        return "PMC" + str(int(match[1])) if match else None
    if kind == "pmid":
        return str(int(value)) if value.isdigit() else None
    if kind == "doi":
        value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value, flags=re.I)
        return value.casefold() if value else None
    raise ValueError("Unknown identifier kind")


class StopCollection(Exception):
    pass


class RejectPaper(Exception):
    pass


class TransportUnavailable(Exception):
    pass


def native_metadata(raw, expected_pmcid):
    """Read identifiers without tokenization, entities, external DTDs or network."""
    article = etree.fromstring(raw, etree.XMLParser(resolve_entities=False, no_network=True))
    if etree.QName(article).localname != "article":
        raise RejectPaper("native_root_is_not_article")
    metas = article.xpath('./*[local-name()="front"]/*[local-name()="article-meta"]')
    if not metas:
        raise RejectPaper("native_article_metadata_missing")
    meta = metas[0]
    ids = {}
    declared_ids = []
    for node in meta.xpath('./*[local-name()="article-id"]'):
        declared_ids.append({"type": node.get("pub-id-type"), "value": "".join(node.itertext()).strip()})
        kind = {"pmc": "pmcid", "pmcid": "pmcid", "pmcaid": "pmcid", "pmid": "pmid", "doi": "doi"}.get(node.get("pub-id-type"))
        if kind:
            value = identifier(kind, "".join(node.itertext()))
            if value:
                ids[kind] = value
    if not ids.get("pmcid"):
        raise RejectPaper("native_pmcid_not_declared")
    if ids["pmcid"] != identifier("pmcid", expected_pmcid):
        raise RejectPaper("native_pmcid_mismatch")
    licenses = []
    for node in meta.xpath('.//*[local-name()="license"]'):
        licenses.append({"attributes": dict(node.attrib), "text": " ".join("".join(node.itertext()).split())})
    titles = meta.xpath('./*[local-name()="title-group"]/*[local-name()="article-title"]')
    return {"identifiers": ids, "article_type": article.get("article-type"),
            "declared_identifiers": declared_ids, "article_version_attribute": article.get("article-version"),
            "declared_versions": ["".join(n.itertext()).strip() for n in meta.xpath('./*[local-name()="article-version"]')],
            "title": " ".join("".join(titles[0].itertext()).split()) if titles else "",
            "licenses": licenses, "source_xml_sha256": digest(raw)}


def selection(document, metadata, accepted_types):
    markers = biology_markers(document)
    if metadata["article_type"] not in accepted_types:
        reason = "article_type_outside_selection"
    elif clinical_title_reason(document["title"]):
        reason = "explicit_clinical_title"
    elif len(markers) < 2 or not {"gene", "protein", "organism"}.intersection(markers):
        reason = "insufficient_biology_title_abstract_markers"
    elif len(" ".join(b["text"] for b in document["blocks"] if b.get("region") == "body")) < 500:
        reason = "insufficient_native_body"
    elif document["duplicate_visual_ids"]:
        reason = "ambiguous_duplicate_visual_identifiers"
    else:
        reason = None
    return reason is None, reason, markers


class CollectionLedger:
    """Separate source versions, exact text decisions and resume cursors atomically."""

    def __init__(self, path, identity):
        self.db = sqlite3.connect(path, timeout=30)
        self.db.executescript("""
            PRAGMA journal_mode=WAL;
            PRAGMA synchronous=FULL;
            CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS identifiers(kind TEXT,value TEXT,origin TEXT,
                PRIMARY KEY(kind,value));
            CREATE TABLE IF NOT EXISTS catalog(row_number INTEGER PRIMARY KEY,pmcid TEXT,path TEXT,
                status TEXT NOT NULL DEFAULT 'pending',metadata TEXT,error TEXT);
            CREATE TABLE IF NOT EXISTS candidates(ordinal INTEGER PRIMARY KEY AUTOINCREMENT,
                pmcid TEXT UNIQUE,stratum TEXT,sampling_rank INTEGER DEFAULT 0,status TEXT DEFAULT 'pending',reason TEXT);
            CREATE TABLE IF NOT EXISTS queries(name TEXT PRIMARY KEY,details TEXT);
            CREATE TABLE IF NOT EXISTS records(source_key TEXT PRIMARY KEY,pmcid TEXT,source_hash TEXT,
                route TEXT,tokens INTEGER,normalized_hash TEXT,kept INTEGER,selected INTEGER,
                selected_kept INTEGER,selection_reason TEXT,details TEXT);
            CREATE INDEX IF NOT EXISTS normalized_text ON records(normalized_hash);
            CREATE INDEX IF NOT EXISTS catalog_status ON catalog(status,row_number);
            CREATE INDEX IF NOT EXISTS candidate_status ON candidates(status,sampling_rank,ordinal);
            CREATE TABLE IF NOT EXISTS events(kind TEXT PRIMARY KEY,count INTEGER NOT NULL);
        """)
        try:
            for key, value in identity.items():
                self.bind(key, value)
        except Exception:
            self.db.close()
            raise

    def bind(self, key, value):
        old = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        if old and old[0] != str(value):
            raise ValueError("Run identity changed: " + key)
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO meta VALUES(?,?)", (key, str(value)))

    def get(self, key, default=None):
        row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row[0] if row else default

    def set(self, key, value):
        self.db.execute("INSERT OR REPLACE INTO meta VALUES(?,?)", (key, str(value)))

    def seed(self, ids, origin):
        for kind in ("pmcid", "pmid", "doi"):
            value = identifier(kind, ids.get(kind))
            if value:
                self.db.execute("INSERT OR IGNORE INTO identifiers VALUES(?,?,?)", (kind, value, origin))

    def known(self, ids):
        return any(self.db.execute("SELECT 1 FROM identifiers WHERE kind=? AND value=?",
                                  (kind, value)).fetchone()
                   for kind in ("pmcid", "pmid", "doi")
                   if (value := identifier(kind, ids.get(kind))))

    def event(self, kind, amount=1):
        self.db.execute("INSERT INTO events VALUES(?,?) ON CONFLICT(kind) DO UPDATE SET count=count+excluded.count",
                        (kind, amount))

    def finish(self, table, key, status, reason=None):
        if table == "catalog":
            self.db.execute("UPDATE catalog SET status=?,error=? WHERE row_number=?", (status, reason, key))
        elif table == "candidates":
            self.db.execute("UPDATE candidates SET status=?,reason=? WHERE pmcid=?", (status, reason, key))
        else:
            raise ValueError("Unknown cursor table")

    def append(self, record, table, cursor):
        """Output files are durable first; this transaction owns counts + cursor."""
        with self.db:
            exists = self.db.execute("SELECT 1 FROM records WHERE source_key=?", (record["source_key"],)).fetchone()
            if exists:
                self.event("identical_source_skips")
            else:
                text_hash = record["measurements"]["normalized_sha256"]
                kept = not self.db.execute("SELECT 1 FROM records WHERE normalized_hash=? LIMIT 1", (text_hash,)).fetchone()
                selected_kept = record["selected"] and not self.db.execute(
                    "SELECT 1 FROM records WHERE normalized_hash=? AND selected=1 LIMIT 1", (text_hash,)).fetchone()
                self.db.execute("INSERT INTO records VALUES(?,?,?,?,?,?,?,?,?,?,?)", (
                    record["source_key"], record["pmcid"], record["source_xml_sha256"], record["route"],
                    record["measurements"]["tokens"], text_hash, int(kept), int(record["selected"]),
                    int(bool(selected_kept)), record["selection_reason"], json.dumps(record, ensure_ascii=False)))
                self.seed(record["identifiers"], record["source_key"])
            self.finish(table, cursor, "processed")


class Worker:
    def __init__(self, config_path):
        try:
            self.initialize(config_path)
        except Exception:
            self.close()
            raise

    def close(self):
        if hasattr(self, "session"):
            self.session.close()
        if hasattr(self, "ledger"):
            self.ledger.db.close()
        if hasattr(self, "lock"):
            self.lock.close()

    def initialize(self, config_path):
        self.config_path = Path(config_path).resolve()
        self.config = json.loads(self.config_path.read_text())
        self.run = self.resolve(self.config["destination"])
        self.run.mkdir(parents=True, exist_ok=True)
        self.lock = (self.run / "worker.lock").open("a")
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("This collection already has a worker") from None
        if hasattr(os, "sched_getaffinity"):
            os.sched_setaffinity(0, set(sorted(os.sched_getaffinity(0))[:2]))
        self.limits = self.config["limits"]
        self.max_xml = self.limits.get("max_xml_bytes", 8 * MIB)
        self.max_text = self.limits.get("max_text_bytes", 4 * MIB)
        self.max_document = self.limits.get("max_document_gzip_bytes", 32 * MIB)
        self.catalog_path = self.resolve(self.config["source_catalog"])
        self.tokenizer_path = self.resolve(self.config["tokenizer_path"])
        for field in ("source_catalog", "presence_ids_csv"):
            expected_hash = self.config.get(field + "_sha256")
            if expected_hash and sha256(self.resolve(self.config[field])) != expected_hash:
                raise ValueError("Frozen input checksum mismatch: " + field)
        if sha256(self.tokenizer_path) != self.config["tokenizer_sha256"]:
            raise ValueError("Pinned tokenizer checksum mismatch")
        self.tokenizer = Tokenizer.from_file(str(self.tokenizer_path))
        self.ledger = CollectionLedger(self.run / "papers.sqlite3", {
            "config_sha256": sha256(self.config_path), "catalog_sha256": sha256(self.catalog_path),
            "tokenizer_sha256": self.config["tokenizer_sha256"]})
        self.state_path = self.run / "state.json"
        self.state = json.loads(self.state_path.read_text()) if self.state_path.exists() else {
            "run_id": self.config["run_id"], "started_at_pst": now(), "started_epoch": time.time(),
            "network_charged_bytes": 0, "network_body_bytes": 0}
        self.state["deadline_epoch"] = self.state["started_epoch"] + self.limits["runtime_seconds"]
        self.state["stop_at_pst"] = datetime.fromtimestamp(self.state["deadline_epoch"], PST).isoformat()
        self.state.update(pid=os.getpid(), status="running", error=None, stop_reason=None)
        self.signalled = False
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda *_: setattr(self, "signalled", True))
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "paper-extraction-lab/PMC-reuse-first (serial)", "Accept-Encoding": "identity"})
        self.last_publish = 0
        self.last_ncbi = 0
        self.reserved_artifacts = 0
        self.non_database_bytes = sum(p.stat().st_size for p in self.run.rglob("*")
                                      if p.is_file() and not p.name.startswith("papers.sqlite3"))
        overrides = self.resolve(self.config.get("citation_metadata_path", "config/pmc_citation_metadata.json"))
        self.overrides = json.loads(overrides.read_text())["papers"] if overrides.exists() else {}
        self.persist()

    def resolve(self, path):
        path = Path(path)
        return path if path.is_absolute() else ROOT / path

    def artifact_bytes(self):
        return self.non_database_bytes + sum(p.stat().st_size for p in self.run.glob("papers.sqlite3*") if p.is_file())

    def guard(self, reserve=0):
        if self.signalled or (self.run / "STOP").exists():
            raise StopCollection("stop_requested")
        if time.time() >= self.state["deadline_epoch"]:
            raise StopCollection("runtime_limit")
        free = shutil.disk_usage(self.run).free
        self.state["filesystem_free_bytes"] = free
        if free < self.limits["minimum_free_bytes"] + reserve:
            raise StopCollection("free_space_floor")
        current = self.artifact_bytes()
        if current + self.reserved_artifacts + reserve > self.limits["new_artifact_bytes"]:
            raise StopCollection("artifact_limit")
        existing = self.config.get("existing_pipeline_bytes", 0)
        ceiling = self.limits.get("maximum_pipeline_data_bytes", 200 * 2**30)
        if existing + current + self.reserved_artifacts + reserve > ceiling:
            raise StopCollection("pipeline_storage_limit")

    def write(self, path, raw):
        """Account for both old and temporary payloads during atomic replacement."""
        self.guard(len(raw) + MIB)
        path.parent.mkdir(parents=True, exist_ok=True)
        previous = path.stat().st_size if path.exists() else 0
        temporary = path.with_suffix(path.suffix + ".tmp")
        old_temp = temporary.stat().st_size if temporary.exists() else 0
        with temporary.open("wb") as out:
            out.write(raw)
            out.flush()
            os.fsync(out.fileno())
        temporary.replace(path)
        self.non_database_bytes += len(raw) - previous - old_temp

    def persist(self):
        self.state["updated_at_pst"] = now()
        raw = (json.dumps(self.state, indent=2) + "\n").encode()
        # State must remain writable when a work budget stops the run. Its small
        # fixed control-plane allowance is reserved before each payload write.
        target = self.state_path
        old = target.stat().st_size if target.exists() else 0
        temporary = target.with_suffix(".json.tmp")
        with temporary.open("wb") as out:
            out.write(raw)
            out.flush()
            os.fsync(out.fileno())
        temporary.replace(target)
        if hasattr(self, "non_database_bytes"):
            self.non_database_bytes += len(raw) - old

    def publish(self, force=False):
        if not force and time.monotonic() - self.last_publish < 30:
            return
        counts = {"raw_records": 0, "raw_tokens": 0, "exact_unique_records": 0, "exact_unique_tokens": 0,
                  "selected_records": 0, "selected_tokens": 0, "selected_exact_unique_tokens": 0}
        by_route = {}
        for row in self.ledger.db.execute("""SELECT route,COUNT(*),COALESCE(SUM(tokens),0),SUM(kept),SUM(tokens*kept),
                SUM(selected),SUM(tokens*selected),SUM(tokens*selected_kept) FROM records GROUP BY route"""):
            values = dict(zip(counts, row[1:]))
            by_route[row[0]] = values
            for key, value in values.items():
                counts[key] += value or 0
        events = dict(self.ledger.db.execute("SELECT kind,count FROM events"))
        statuses = {table: dict(self.ledger.db.execute(f"SELECT status,COUNT(*) FROM {table} GROUP BY status"))
                    for table in ("catalog", "candidates")}
        self.state["updated_at_pst"] = now()
        summary = {**self.state, **counts, "counts": counts, "by_route": by_route, "events": events,
                   "input_statuses": statuses,
                   "new_selected_papers": self.ledger.db.execute("SELECT COUNT(DISTINCT pmcid) FROM records WHERE route='new' AND selected=1").fetchone()[0],
                   "new_processed_papers": self.ledger.db.execute("SELECT COUNT(DISTINCT pmcid) FROM records WHERE route='new'").fetchone()[0],
                   "reused_processed_papers": self.ledger.db.execute("SELECT COUNT(DISTINCT pmcid) FROM records WHERE route='reused'").fetchone()[0],
                   "raw_distinct_papers": self.ledger.db.execute("SELECT COUNT(DISTINCT pmcid) FROM records").fetchone()[0],
                   "selected_distinct_papers": self.ledger.db.execute("SELECT COUNT(DISTINCT pmcid) FROM records WHERE selected=1").fetchone()[0],
                   "catalog_total": sum(statuses["catalog"].values()),
                   "known_identifier_counts": dict(self.ledger.db.execute("SELECT kind,COUNT(*) FROM identifiers GROUP BY kind")),
                   "queries_completed": self.ledger.db.execute("SELECT COUNT(*) FROM queries").fetchone()[0],
                   "target_new_papers": self.config.get("target_new_papers", 10000),
                   "new_artifact_bytes": self.artifact_bytes(),
                   "network_bytes": self.state["network_body_bytes"],
                   "scope_method": "Coarse source-type, title/abstract biology markers and clinical-title rules; not a validated classifier",
                   "tokenizer_sha256": self.config["tokenizer_sha256"],
                   "deduplication": "Whitespace-normalized full-record SHA-256; distinct PMCID/source-hash versions retained",
                   "limits": self.limits, "gpu_count": 0, "cpu_threads": 2,
                   "media": "Native captions, table structures and source media links retained; no binary media/PDF acquisition or OCR"}
        raw = (json.dumps(summary, indent=2) + "\n").encode()
        target = self.run / "summary.json"
        old = target.stat().st_size if target.exists() else 0
        temporary = target.with_suffix(".json.tmp")
        temporary.write_bytes(raw)
        temporary.replace(target)
        self.non_database_bytes += len(raw) - old
        self.persist()
        self.last_publish = time.monotonic()

    def stage(self, name, pmcid=None):
        self.state.update(stage=name, current_pmcid=pmcid)
        self.publish()

    def reject(self, table, cursor, reason, kind="rejected_documents"):
        with self.ledger.db:
            self.ledger.finish(table, cursor, "rejected", reason)
            self.ledger.event(kind)

    def seed_known(self):
        self.stage("index_known_identifiers")
        catalog = json.loads(self.catalog_path.read_text())
        catalog = catalog.get("native_xml", catalog.get("sources", [])) if isinstance(catalog, dict) else catalog
        if self.ledger.get("catalog_registered") != "1":
            for start in range(0, len(catalog), 1000):
                self.guard(8 * MIB)
                with self.ledger.db:
                    for number, row in enumerate(catalog[start:start + 1000], start + 1):
                        pmcid = identifier("pmcid", row["pmcid"])
                        if not pmcid:
                            raise ValueError("Catalog contains an invalid PMCID")
                        self.ledger.db.execute("INSERT OR IGNORE INTO catalog(row_number,pmcid,path) VALUES(?,?,?)",
                                               (number, pmcid, str(self.resolve(row["path"]))))
                        self.ledger.seed({"pmcid": pmcid, "pmid": row.get("pmid"), "doi": row.get("doi")}, "catalog")
                self.publish()
            with self.ledger.db:
                self.ledger.set("catalog_registered", 1)
        presence = self.config.get("presence_ids_csv")
        if presence and self.ledger.get("presence_complete") != "1":
            path = self.resolve(presence)
            self.ledger.bind("presence_sha256", sha256(path))
            cursor = int(self.ledger.get("presence_cursor", "0"))
            batch = []
            with path.open(newline="") as source:
                for number, row in enumerate(csv.DictReader(source), 1):
                    if number <= cursor:
                        continue
                    batch.append(row)
                    if len(batch) >= 1000:
                        self.seed_presence_batch(batch, number)
                        batch = []
                if batch:
                    self.seed_presence_batch(batch, number)
            with self.ledger.db:
                self.ledger.set("presence_complete", 1)
        self.stage("index_local_xml_metadata")
        while True:
            row = self.ledger.db.execute("SELECT row_number,pmcid,path FROM catalog WHERE status='pending' ORDER BY row_number LIMIT 1").fetchone()
            if not row:
                break
            number, pmcid, path = row
            self.state["current_pmcid"] = pmcid
            self.guard(8 * MIB)
            raw = None
            try:
                frozen = catalog[number - 1]
                stat = Path(path).stat()
                if ((frozen.get("bytes") is not None and stat.st_size != frozen["bytes"]) or
                        (frozen.get("mtime_ns") is not None and stat.st_mtime_ns != frozen["mtime_ns"])):
                    raise RejectPaper("local_xml_changed_since_catalog_freeze")
                raw = self.read_source(Path(path))
                metadata = native_metadata(raw, pmcid)
                with self.ledger.db:
                    self.ledger.seed(metadata["identifiers"], "local_xml")
                    self.ledger.db.execute("UPDATE catalog SET status='indexed',metadata=? WHERE row_number=?",
                                           (json.dumps(metadata), number))
            except (RejectPaper, etree.XMLSyntaxError, OSError) as exc:
                reason = str(exc) if isinstance(exc, RejectPaper) else type(exc).__name__
                with self.ledger.db:
                    if raw is not None:
                        self.ledger.db.execute("UPDATE catalog SET metadata=? WHERE row_number=?",
                                               (json.dumps({"source_xml_sha256": digest(raw)}), number))
                    self.ledger.finish("catalog", number, "rejected", reason)
                    self.ledger.event("local_metadata_rejections")
            self.publish()
        with self.ledger.db:
            self.ledger.set("known_index_complete", 1)

    def seed_presence_batch(self, batch, cursor):
        self.guard(8 * MIB)
        with self.ledger.db:
            for row in batch:
                self.ledger.seed(row, "presence_manifest")
            self.ledger.set("presence_cursor", cursor)
        self.publish()

    def read_source(self, path):
        self.guard()
        if path.stat().st_size > self.max_xml:
            raise RejectPaper("native_xml_exceeds_byte_limit")
        with path.open("rb") as source:
            raw = source.read(self.max_xml + 1)
        if len(raw) > self.max_xml:
            raise RejectPaper("native_xml_exceeds_byte_limit")
        return raw

    def process(self, path, pmcid, route, table, cursor, expected=None, upstream=None):
        self.guard(self.max_document + self.max_text + 8 * MIB)
        raw = self.read_source(path)
        metadata = native_metadata(raw, pmcid)
        if expected and metadata["source_xml_sha256"] != expected["source_xml_sha256"]:
            raise RejectPaper("local_xml_changed_since_identifier_index")
        source_hash = metadata["source_xml_sha256"]
        key = pmcid + ":" + source_hash
        if self.ledger.db.execute("SELECT 1 FROM records WHERE source_key=?", (key,)).fetchone():
            with self.ledger.db:
                self.ledger.finish(table, cursor, "processed")
                self.ledger.event("identical_source_skips")
            return
        document = parse_jats(path, pmcid, self.tokenizer, citation_overrides=self.overrides.get(pmcid),
                              maximum_table_rows=self.config.get("maximum_table_rows", 2000))
        if document["source_xml_sha256"] != source_hash:
            raise RejectPaper("local_xml_changed_during_parse")
        text = canonical_paper_text(document)
        if len(text.encode()) > self.max_text:
            raise RejectPaper("canonical_text_exceeds_byte_limit")
        selected, reason, markers = selection(document, metadata, self.config.get("accepted_article_types", DEFAULT_TYPES))
        measured = inspect_text(text, self.tokenizer)
        document.update(source_metadata=metadata, upstream_metadata=upstream, source_locator=str(path),
                        selection={"selected": selected, "reason": reason, "biology_markers": markers})
        compressed = gzip.compress(json.dumps(document, ensure_ascii=False).encode(), mtime=0)
        if len(compressed) > self.max_document:
            raise RejectPaper("parsed_document_exceeds_byte_limit")
        output = self.run / "parsed" / pmcid / source_hash
        canonical = {"id": pmcid, "source_xml_sha256": source_hash, "text": text,
                     "identifiers": metadata["identifiers"], "licenses": metadata["licenses"],
                     "selected": selected, "selection_reason": reason}
        self.write(output / "document.json.gz", compressed)
        self.write(output / "canonical.jsonl.gz", gzip.compress((json.dumps(canonical, ensure_ascii=False) + "\n").encode(), mtime=0))
        self.guard(8 * MIB)
        self.ledger.append({"source_key": key, "pmcid": pmcid, "source_xml_sha256": source_hash,
                            "route": route, "measurements": measured, "selected": selected,
                            "selection_reason": reason, "biology_markers": markers, "identifiers": metadata["identifiers"],
                            "source_locator": str(path), "document_locator": str(output / "document.json.gz"),
                            "canonical_locator": str(output / "canonical.jsonl.gz"), "licenses": metadata["licenses"],
                            "article_type": metadata["article_type"], "upstream_metadata": upstream}, table, cursor)

    def reused(self, maximum=None):
        self.stage("process_reused_xml")
        attempted = 0
        while True:
            row = self.ledger.db.execute("SELECT row_number,pmcid,path,metadata FROM catalog WHERE status='indexed' ORDER BY row_number LIMIT 1").fetchone()
            if not row:
                break
            if maximum is not None and attempted >= maximum:
                raise StopCollection("local_probe_limit")
            number, pmcid, path, metadata = row
            self.state["current_pmcid"] = pmcid
            try:
                self.process(Path(path), pmcid, "reused", "catalog", number, expected=json.loads(metadata))
            except (RejectPaper, ValueError, etree.XMLSyntaxError, OSError) as exc:
                reason = str(exc) if isinstance(exc, RejectPaper) else type(exc).__name__
                self.reject("catalog", number, reason, "native_parse_rejections")
            attempted += 1
            self.publish()

    def fetch(self, url, path, maximum):
        if path.exists():
            raw = path.read_bytes()
            if len(raw) > maximum:
                raise RejectPaper("cached_response_exceeds_byte_limit")
            return raw
        if self.ledger.get("known_index_complete") != "1":
            raise RuntimeError("Network acquisition requires the complete local identifier index")
        for attempt in range(3):
            self.guard(maximum + 2 * MIB)
            charged = self.state["network_charged_bytes"]
            if charged + maximum > self.limits["network_bytes"]:
                raise StopCollection("network_budget")
            self.state["network_charged_bytes"] += maximum
            self.persist()
            received = 0
            body_read_pending = False
            unmeasured_partial_body = False
            try:
                if url.startswith(ESEARCH):
                    delay = 0.4 - (time.monotonic() - self.last_ncbi)
                    if delay > 0:
                        time.sleep(delay)
                    self.last_ncbi = time.monotonic()
                with self.session.get(url, stream=True, timeout=(15, 35)) as response:
                    if response.status_code == 404:
                        raise RejectPaper("distributed_object_not_found")
                    response.raise_for_status()
                    expected = int(response.headers.get("Content-Length", "0"))
                    if expected > maximum:
                        raise RejectPaper("response_exceeds_byte_limit")
                    chunks = []
                    while received < maximum:
                        self.guard()
                        body_read_pending = True
                        block = response.raw.read(min(65536, maximum - received), decode_content=False)
                        body_read_pending = False
                        if not block:
                            break
                        chunks.append(block)
                        received += len(block)
                    if (expected and received != expected) or (not expected and received == maximum):
                        raise RejectPaper("response_incomplete_or_byte_limit")
                    raw = b"".join(chunks)
                self.write(path, raw)
                return raw
            except requests.HTTPError as exc:
                status = exc.response.status_code if exc.response is not None else None
                if status and status < 500 and status not in {408, 425, 429}:
                    raise RejectPaper("http_" + str(status)) from None
                if attempt == 2:
                    raise TransportUnavailable(type(exc).__name__) from None
            except (requests.RequestException, RawHTTPError, OSError) as exc:
                # urllib3's raw reader can raise directly after consuming bytes
                # that it never returns to us. Keep the whole reservation in
                # that case; known returned bytes remain a lower bound.
                unmeasured_partial_body = body_read_pending
                if attempt == 2:
                    raise TransportUnavailable(type(exc).__name__) from None
            finally:
                if unmeasured_partial_body:
                    self.state["network_body_bytes_is_lower_bound"] = True
                    self.state["unmeasured_partial_responses"] = self.state.get("unmeasured_partial_responses", 0) + 1
                else:
                    self.state["network_charged_bytes"] -= maximum - received
                self.state["network_body_bytes"] += received
                self.persist()
                self.publish()
            time.sleep(attempt + 1)
        raise AssertionError("Unreachable retry state")

    def discover(self):
        self.stage("discover_new_papers")
        topics = self.config.get("query_topics", self.config.get("topics", {
            "genes_genomes": ["gene", "genome", "RNA", "transcription"],
            "proteins_cells": ["protein", "enzyme", "cellular", "metabolism"],
            "organisms_ecology": ["bacteria", "plant", "microbiome", "evolution"],
            "neuroscience_immunity": ["neuron", "synapse", "immune", "antibody"]}))
        years = self.config.get("query_years", self.config.get("years", [[2000, 2009], [2010, 2014], [2015, 2019], [2020, 2023], [2024, 2026]]))
        retmax = self.config.get("candidates_per_query", self.config.get("candidates_per_stratum", 2000))
        if not 1 <= retmax <= 10000:
            raise ValueError("PMC retmax must be between 1 and 10000")
        if isinstance(topics, list):
            topics = {"topic" + str(index + 1): query for index, query in enumerate(topics)}
        for topic, terms in topics.items():
            for first, last in years:
                name = topic + "_" + str(first) + "_" + str(last)
                if self.ledger.db.execute("SELECT 1 FROM queries WHERE name=?", (name,)).fetchone():
                    continue
                term = terms if isinstance(terms, str) else "(" + " OR ".join(word + "[tiab]" for word in terms) + ")"
                term += f' AND {first}:{last}[pdat] AND (open_access[filter] OR author_manuscript[filter]) NOT "pmc embargo"[filter] NOT (articletyperetraction OR articletypecorrection OR hasretractionin)'
                url = ESEARCH + "?" + urlencode({"db": "pmc", "term": term, "retmode": "json", "retmax": retmax, "tool": "paper_extraction_lab"})
                raw = self.fetch(url, self.run / "queries" / (digest(name.encode()) + ".json"), 2 * MIB)
                result = json.loads(raw)
                found = result["esearchresult"]
                if result.get("error") or found.get("error") or found.get("errorlist") or found.get("warninglist", {}).get("quotedphrasesnotfound"):
                    raise ValueError("PMC discovery query was not accepted exactly")
                ids = [identifier("pmcid", uid) for uid in found["idlist"]]
                if None in ids:
                    raise ValueError("PMC returned an invalid identifier")
                ids.sort(key=lambda uid: digest((name + uid).encode()))
                self.guard(8 * MIB)
                with self.ledger.db:
                    for rank, uid in enumerate(ids):
                        self.ledger.db.execute("INSERT OR IGNORE INTO candidates(pmcid,stratum,sampling_rank) VALUES(?,?,?)", (uid, name, rank))
                    self.ledger.db.execute("INSERT INTO queries VALUES(?,?)", (name, json.dumps({
                        "url": url, "query": term, "matches": int(found["count"]), "returned": len(ids),
                        "response_sha256": digest(raw), "selection": "Convenience search-return subset, not probability sampling"})))
                self.publish()

    def metadata(self, pmcid, directory):
        url = S3 + "/?" + urlencode({"list-type": 2, "prefix": "metadata/" + pmcid + "."})
        raw = self.fetch(url, directory / "versions.xml", MIB)
        listing = etree.fromstring(raw, etree.XMLParser(resolve_entities=False, no_network=True))
        if listing.findtext("{*}IsTruncated") == "true":
            raise RejectPaper("version_listing_truncated")
        keys = [n.text for n in listing.findall(".//{*}Key") if n.text and n.text.endswith(".json")]
        if len(keys) > 100:
            raise RejectPaper("too_many_distributed_versions")
        options = []
        for key in keys:
            row = json.loads(self.fetch(S3 + "/" + key, directory / Path(key).name, MIB))
            if identifier("pmcid", row.get("pmcid")) != pmcid:
                raise RejectPaper("distributed_metadata_pmcid_mismatch")
            options.append(row)
        try:
            chosen = choose_metadata(options)
        except Exception as exc:
            from pmc_count_expansion import RejectedPaper
            if isinstance(exc, RejectedPaper):
                raise RejectPaper("no_nonretracted_distributed_xml") from None
            raise
        self.write(directory / "selected_metadata.json", (json.dumps(chosen, indent=2) + "\n").encode())
        return chosen

    def new(self):
        self.discover()
        self.stage("acquire_missing_papers")
        target = self.config.get("target_new_papers", 10000)
        while True:
            self.guard()
            selected = self.ledger.db.execute("SELECT COUNT(DISTINCT pmcid) FROM records WHERE route='new' AND selected=1").fetchone()[0]
            if selected >= target:
                self.state["completion_reason"] = "new_paper_target_reached"
                return
            candidate = self.ledger.db.execute("SELECT pmcid FROM candidates WHERE status='pending' ORDER BY sampling_rank,ordinal LIMIT 1").fetchone()
            if not candidate:
                self.state["completion_reason"] = "candidate_query_subsets_exhausted"
                return
            pmcid = candidate[0]
            self.state["current_pmcid"] = pmcid
            source_meta = None
            try:
                if self.ledger.known({"pmcid": pmcid}):
                    with self.ledger.db:
                        self.ledger.finish("candidates", pmcid, "known", "pmcid_already_present")
                        self.ledger.event("known_pmcid_skips")
                    self.publish()
                    continue
                directory = self.run / "raw" / pmcid
                metadata = self.metadata(pmcid, directory)
                ids = {kind: metadata.get(kind) for kind in ("pmcid", "pmid", "doi")}
                if self.ledger.known(ids):
                    with self.ledger.db:
                        self.ledger.finish("candidates", pmcid, "known", "pmid_or_doi_already_present")
                        self.ledger.event("known_secondary_identifier_skips")
                    self.publish()
                    continue
                url = public_url(metadata["xml_url"])
                raw = self.fetch(url, directory / "source.xml", self.max_xml)
                self.write(directory / "source_manifest.json", (json.dumps({
                    "source_url": url, "source_xml_sha256": digest(raw), "bytes": len(raw),
                    "metadata_sha256": digest(json.dumps(metadata, sort_keys=True).encode()),
                    "fetched_at_pst": now()}) + "\n").encode())
                expected = parse_qs(urlsplit(url).query).get("md5", [None])[0]
                if not expected or hashlib.md5(raw).hexdigest().casefold() != expected.casefold():
                    raise RejectPaper("distributed_xml_md5_missing_or_mismatch")
                source_meta = native_metadata(raw, pmcid)
                for kind in ("pmid", "doi"):
                    if identifier(kind, ids.get(kind)) and source_meta["identifiers"].get(kind) and identifier(kind, ids[kind]) != source_meta["identifiers"][kind]:
                        raise RejectPaper("distributed_xml_identifier_mismatch")
                self.process(directory / "source.xml", pmcid, "new", "candidates", pmcid, upstream=metadata)
            except (RejectPaper, ValueError, etree.XMLSyntaxError) as exc:
                reason = str(exc) if isinstance(exc, RejectPaper) else type(exc).__name__
                with self.ledger.db:
                    # Finalizing the attempt and recording downloaded IDs is
                    # atomic; a crash before parsing must leave it resumable.
                    if source_meta:
                        self.ledger.seed(source_meta["identifiers"], "rejected_downloaded_xml")
                    self.ledger.finish("candidates", pmcid, "rejected", reason)
                    self.ledger.event("new_paper_rejections")
            self.publish()

    def execute(self, local_only=False, max_local_papers=None):
        try:
            self.publish(force=True)
            self.guard()
            self.seed_known()
            self.reused(maximum=max_local_papers)
            if max_local_papers is not None:
                raise StopCollection("local_probe_limit")
            if not local_only and self.config.get("target_new_papers", 10000) > 0:
                self.new()
            self.state.update(status="complete", stage="finished")
        except StopCollection as exc:
            self.state.update(status="stopped", stop_reason=str(exc))
        except TransportUnavailable as exc:
            self.state.update(status="failed", stop_reason="network_unavailable", error=type(exc).__name__)
            traceback.print_exc()
        except Exception as exc:
            self.state.update(status="failed", error=type(exc).__name__)
            traceback.print_exc()
        finally:
            self.publish(force=True)
            self.close()
        return 1 if self.state["status"] == "failed" else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--local-only", action="store_true")
    parser.add_argument("--max-local-papers", type=int,
                        help="Diagnostic limit; always stops before network acquisition")
    args = parser.parse_args()
    if args.max_local_papers is not None and args.max_local_papers < 0:
        parser.error("--max-local-papers must be nonnegative")
    return Worker(args.config).execute(args.local_only, args.max_local_papers)


if __name__ == "__main__":
    raise SystemExit(main())
