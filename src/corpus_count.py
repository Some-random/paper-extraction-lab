"""Resumable, source-preserving CPU census of complete JSONL(/zstd) inputs.

Counts are candidate corpus tokens, not training exposure or biology validation.
All token positions are assigned exactly once; tagged-content boundaries use the
start offset of each token. Exact deduplication preserves case and punctuation.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path

TAG = re.compile(r"<(protein|dna|rna|smiles|inchi)>(.*?)</\1>", re.I | re.S)
MODALITIES = ("protein", "dna", "rna", "smiles", "inchi", "text_or_unclassified")


def canonical_paper_text(document):
    """One copy per source block/visual, including visuals outside the body."""
    blocks = document["blocks"]
    parts = [document["title"]] + [b["training_text"] for b in blocks]
    captions = {b.get("visual_id") for b in blocks if b["kind"] == "caption"}
    tables = {b.get("visual_id") for b in blocks if b["kind"] == "table"}
    excluded = {b.get("visual_id") for b in document.get("excluded_blocks", [])}
    for visual in document["visuals"]:
        identity = visual["id"]
        if identity in excluded:
            continue
        if identity not in captions:
            parts.append(visual.get("caption_training_text", ""))
        # Table blocks already include their footnotes; figure notes are
        # otherwise absent from the block stream.
        if identity not in tables:
            parts.append(visual.get("notes_training_text", ""))
            if visual.get("table"):
                parts.append(visual["table"]["text_tsv"])
    return "\n\n".join(part for part in parts if part.strip())


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_text(text, tokenizer):
    encoded = tokenizer.encode(text, add_special_tokens=False)
    spans = [(m.start(2), m.end(2), m.group(1).lower()) for m in TAG.finditer(text)]
    counts = Counter({kind: 0 for kind in MODALITIES})
    cursor = 0
    for start, end in encoded.offsets:
        while cursor < len(spans) and spans[cursor][1] <= start:
            cursor += 1
        kind = "text_or_unclassified"
        if cursor < len(spans) and spans[cursor][0] <= start < spans[cursor][1]:
            kind = spans[cursor][2]
        counts[kind] += 1
    assert sum(counts.values()) == len(encoded.ids)
    normalized = re.sub(r"\s+", " ", text).strip()
    return {
        "tokens": len(encoded.ids), "utf8_bytes": len(text.encode("utf-8")),
        "raw_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "normalized_sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
        "modalities": dict(counts),
        "tagged_native_characters": dict(Counter({kind: sum(
            not char.isspace() for a, b, k in spans if k == kind for char in text[a:b]
        ) for kind in MODALITIES[:-1]})),
    }


class Ledger:
    def __init__(self, path, manifest_hash, tokenizer_hash):
        self.db = sqlite3.connect(path)
        self.db.executescript("""
            PRAGMA journal_mode=WAL;
            PRAGMA synchronous=FULL;
            CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS files(
                id TEXT PRIMARY KEY, source TEXT NOT NULL, status TEXT NOT NULL,
                cursor INTEGER NOT NULL DEFAULT 0, error TEXT);
            CREATE TABLE IF NOT EXISTS records(
                file_id TEXT NOT NULL, row_number INTEGER NOT NULL,
                normalized_hash TEXT NOT NULL, raw_hash TEXT NOT NULL,
                tokens INTEGER NOT NULL, kept INTEGER NOT NULL,
                provenance TEXT NOT NULL, measurements TEXT NOT NULL,
                PRIMARY KEY(file_id,row_number));
            CREATE INDEX IF NOT EXISTS content_hash ON records(normalized_hash);
            CREATE TABLE IF NOT EXISTS totals(
                source TEXT NOT NULL, metric TEXT NOT NULL, value INTEGER NOT NULL,
                PRIMARY KEY(source,metric));
            CREATE TABLE IF NOT EXISTS input_extensions(
                id TEXT PRIMARY KEY, definition TEXT NOT NULL);
        """)
        for key, value in [("manifest_sha256", manifest_hash), ("tokenizer_sha256", tokenizer_hash)]:
            previous = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
            if previous and previous[0] != value:
                raise ValueError("Ledger identity changed: " + key)
            self.db.execute("INSERT OR IGNORE INTO meta VALUES(?,?)", (key, value))
        self.db.commit()

    def register(self, files):
        with self.db:
            for item in files:
                self.db.execute("INSERT OR IGNORE INTO files(id,source,status) VALUES(?,?,'pending')",
                                (item["id"], item["source"]))

    def file_state(self, file_id):
        return self.db.execute("SELECT status,cursor FROM files WHERE id=?", (file_id,)).fetchone()

    def bind_identity(self, key, value):
        previous = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        if previous and previous[0] != value:
            raise ValueError("Registered extension identity changed: " + key)
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO meta VALUES(?,?)", (key, value))

    def register_extension(self, item):
        serialized = json.dumps(item, sort_keys=True)
        with self.db:
            previous = self.db.execute("SELECT definition FROM input_extensions WHERE id=?", (item["id"],)).fetchone()
            if previous and previous[0] != serialized:
                raise ValueError("Registered acquired input changed")
            self.db.execute("INSERT OR IGNORE INTO input_extensions VALUES(?,?)", (item["id"], serialized))
            self.db.execute("INSERT OR IGNORE INTO files(id,source,status) VALUES(?,?,'pending')", (item["id"], item["source"]))

    def extensions(self):
        return [json.loads(row[0]) for row in self.db.execute("SELECT definition FROM input_extensions ORDER BY rowid")]

    def status(self, file_id, status, error=None):
        with self.db:
            self.db.execute("UPDATE files SET status=?,error=? WHERE id=?", (status, error, file_id))

    def append(self, item, rows):
        """Commit counters, exact-content decisions and resume cursor together."""
        totals = Counter()
        with self.db:
            for number, measured, provenance in rows:
                if self.db.execute("SELECT 1 FROM records WHERE file_id=? AND row_number=?",
                                   (item["id"], number)).fetchone():
                    continue
                duplicate = self.db.execute("SELECT 1 FROM records WHERE normalized_hash=? LIMIT 1",
                                            (measured["normalized_sha256"],)).fetchone()
                kept = not bool(duplicate)
                self.db.execute("INSERT INTO records VALUES(?,?,?,?,?,?,?,?)", (
                    item["id"], number, measured["normalized_sha256"], measured["raw_sha256"],
                    measured["tokens"], int(kept), json.dumps(provenance), json.dumps(measured)))
                totals["raw_records"] += 1
                totals["raw_tokens"] += measured["tokens"]
                totals["raw_utf8_bytes"] += measured["utf8_bytes"]
                totals["unique_records"] += int(kept)
                totals["unique_tokens"] += measured["tokens"] if kept else 0
                for kind, count in measured["modalities"].items():
                    totals["raw_" + kind + "_tokens"] += count
                    totals["unique_" + kind + "_tokens"] += count if kept else 0
                for kind, count in measured["tagged_native_characters"].items():
                    totals["raw_tagged_" + kind + "_characters"] += count
                self.db.execute("UPDATE files SET cursor=? WHERE id=?", (number, item["id"]))
            for metric, count in totals.items():
                self.db.execute("INSERT INTO totals VALUES(?,?,?) ON CONFLICT(source,metric) "
                                "DO UPDATE SET value=value+excluded.value", (item["source"], metric, count))

    def totals(self):
        result = {}
        for source, metric, count in self.db.execute("SELECT source,metric,value FROM totals"):
            result.setdefault(source, {})[metric] = count
        return result

    def retire_file(self, file_id, correction_hash, audit_path):
        """Audit and subtract a corrected input before its explicit recount.

        Refuse implicit changes to cross-file deduplication representatives.
        The initial caption/table correction has no external hash matches.
        """
        marker = "correction:" + file_id
        previous = self.db.execute("SELECT value FROM meta WHERE key=?", (marker,)).fetchone()
        if previous:
            if previous[0] != correction_hash:
                raise ValueError("Input has a different recorded correction")
            return
        if self.db.execute("SELECT 1 FROM records WHERE file_id!=? AND normalized_hash IN "
                           "(SELECT normalized_hash FROM records WHERE file_id=?) LIMIT 1",
                           (file_id, file_id)).fetchone():
            raise ValueError("Correction requires rebuilding external deduplication representatives")
        source = self.db.execute("SELECT source FROM files WHERE id=?", (file_id,)).fetchone()[0]
        columns = [row[1] for row in self.db.execute("PRAGMA table_info(records)")]
        rows = [dict(zip(columns, row)) for row in self.db.execute(
            "SELECT * FROM records WHERE file_id=? ORDER BY row_number", (file_id,))]
        audit = {"file_id": file_id, "correction_sha256": correction_hash,
                 "reason": "Caption/table views were added after they already appeared in article blocks.",
                 "superseded_records": rows}
        serialized = json.dumps(audit, indent=2) + "\n"
        audit_path = Path(audit_path)
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        if audit_path.exists() and audit_path.read_text() != serialized:
            raise ValueError("Correction audit would overwrite a different result")
        audit_path.write_text(serialized)
        subtraction = Counter()
        for row in rows:
            measured = json.loads(row["measurements"])
            kept = row["kept"]
            subtraction.update(raw_records=1, unique_records=kept,
                               raw_tokens=measured["tokens"], unique_tokens=kept * measured["tokens"],
                               raw_utf8_bytes=measured["utf8_bytes"])
            for kind, count in measured["modalities"].items():
                subtraction["raw_" + kind + "_tokens"] += count
                subtraction["unique_" + kind + "_tokens"] += count * kept
            for kind, count in measured["tagged_native_characters"].items():
                subtraction["raw_tagged_" + kind + "_characters"] += count
        with self.db:
            for metric, value in subtraction.items():
                self.db.execute("UPDATE totals SET value=value-? WHERE source=? AND metric=?", (value, source, metric))
            self.db.execute("DELETE FROM records WHERE file_id=?", (file_id,))
            self.db.execute("UPDATE files SET status='pending',cursor=0,error=NULL WHERE id=?", (file_id,))
            self.db.execute("INSERT INTO meta VALUES(?,?)", (marker, correction_hash))

    def close(self):
        self.db.close()
