#!/usr/bin/env python3
"""Pack a bounded, deterministic prefix of archived selected biological paper text."""
import argparse
import array
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
MIB = 1024 ** 2
GIB = 1024 ** 3


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(MIB), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, value):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    temporary.replace(path)


def under_root(path):
    path = (ROOT / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
    path.relative_to(ROOT)
    return path


def append_uint32(stream, ids):
    values = array.array("I", ids)
    if values.itemsize != 4:
        raise RuntimeError("Platform unsigned integer must occupy4bytes")
    if sys.byteorder != "little":
        values.byteswap()
    values.tofile(stream)


def selected_records(database):
    # The old worker is stopped; immutable+read-only forbids journal creation or
    # accidental writes while preserving a stable deterministic record order.
    connection = sqlite3.connect(database.as_uri() + "?mode=ro&immutable=1", uri=True)
    try:
        for pmcid, source_hash, normalized_hash, tokens, details in connection.execute(
                "SELECT pmcid,source_hash,normalized_hash,tokens,details FROM records "
                "WHERE selected_kept=1 ORDER BY pmcid,source_key"):
            yield dict(pmcid=pmcid, source_xml_sha256=source_hash, normalized_hash=normalized_hash,
                       original_token_count=tokens, details=json.loads(details))
    finally:
        connection.close()


def pack(args, *, tokenizer=None):
    started = time.monotonic()
    config_path = under_root(args.source_config)
    config = json.loads(config_path.read_text())
    source = under_root(config["destination"])
    database = source / "papers.sqlite3"
    output = under_root(args.output_dir)
    if output == source or source in output.parents:
        raise ValueError("New token pack must be outside the archived source run")
    output.mkdir(parents=True, exist_ok=True)
    final = output / "tokens.uint32"
    manifest_path = output / "manifest.json"
    if final.exists() or manifest_path.exists():
        raise FileExistsError("A token pack already exists; preserve it instead of silently overwriting")
    if args.tokens < 1 or args.tokens * 4 + 16 * MIB > args.maximum_artifact_bytes:
        raise ValueError("Token target plus provenance reserve exceeds the artifact budget")
    tokenizer_path = under_root(args.tokenizer_path or config["tokenizer_path"])
    tokenizer_hash = sha256(tokenizer_path)
    if tokenizer_hash != (args.tokenizer_sha256 or config["tokenizer_sha256"]):
        raise ValueError("Archived tokenizer hash differs from its frozen source configuration")
    if tokenizer is None:
        from tokenizers import Tokenizer
        tokenizer = Tokenizer.from_file(str(tokenizer_path))
    separator_id = tokenizer.token_to_id("<|endoftext|>")
    if separator_id is None or not 0 <= separator_id < args.vocabulary_size:
        raise ValueError("Tokenizer lacks the recorded document-boundary token")
    before_database_hash = sha256(database)
    manifest = dict(status="running", started_utc=datetime.now(timezone.utc).isoformat(),
                    source_config_sha256=sha256(config_path), source_database_sha256=before_database_hash,
                    source_run=config["run_id"], source_selection="selected_kept=1; exact-unique coarse biology selection",
                    order="pmcid,source_key ascending; no shuffle, source modification or document replay",
                    tokenizer=dict(path=str(tokenizer_path.relative_to(ROOT)), sha256=tokenizer_hash,
                                   revision=tokenizer_path.parent.name,
                                   family=("Pinned Qwen3-4B-Base tokenizer" if tokenizer_path.parent.name.startswith("qwen3")
                                           else "Archived olmOCR2 tokenizer; byte identity with native tokenizer must be established")),
                    dtype="uint32_le", separator_token_id=separator_id,
                    target_tokens=args.tokens, token_count=0, source_records=0,
                    maximum_token_id=0, raw_utf8_bytes=0,
                    boundary_policy="One end-of-text token after each complete document; final document may be truncated")
    temporary = output / "tokens.uint32.partial"
    provenance = output / "records.jsonl"
    write_json(output / "progress.json", manifest)
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    with temporary.open("xb") as stream, provenance.open("x", encoding="utf-8") as records:
        for row in selected_records(database):
            if time.monotonic() - started >= args.maximum_runtime_seconds:
                raise TimeoutError("CPU token packing exceeded its fixed wall-clock allowance")
            if shutil.disk_usage(output).free < args.minimum_free_bytes + 16 * MIB:
                raise RuntimeError("Shared free-space floor reached; source data preserved")
            locator = under_root(row["details"]["canonical_locator"])
            with gzip.open(locator, "rt", encoding="utf-8") as source_stream:
                text_record = json.loads(source_stream.readline())
                if source_stream.read(1):
                    raise ValueError("Expected exactly one canonical JSONL record per archived file")
            text = text_record["text"]
            if text_record.get("id") != row["pmcid"] or text_record.get("source_xml_sha256") != row["source_xml_sha256"]:
                raise ValueError("Canonical text provenance differs from the archived ledger")
            if text_record.get("selected") is not True:
                raise ValueError("An unselected canonical paper entered the selected ledger query")
            text_bytes = text.encode("utf-8")
            if len(text_bytes) > 4 * MIB:
                raise ValueError("Archived canonical text exceeds the bounded document size")
            ids = tokenizer.encode(text, add_special_tokens=False).ids
            if not ids:
                continue
            if min(ids) < 0 or max(ids) >= args.vocabulary_size:
                raise ValueError("Token IDs fall outside the pinned model vocabulary")
            remaining = args.tokens - manifest["token_count"]
            retained = (ids + [separator_id])[:remaining]
            cursor = manifest["token_count"]
            append_uint32(stream, retained)
            row_details = dict(pmcid=row["pmcid"], source_xml_sha256=row["source_xml_sha256"],
                               canonical_gzip_sha256=sha256(locator), canonical_text_sha256=hashlib.sha256(text_bytes).hexdigest(),
                               normalized_hash=row["normalized_hash"], token_start=cursor,
                               tokens_written=len(retained), document_tokens=len(ids),
                               final_document_truncated=len(retained) < len(ids) + 1,
                               licenses=row["details"].get("licenses", []))
            records.write(json.dumps(row_details, ensure_ascii=False) + "\n")
            manifest["token_count"] += len(retained)
            manifest["source_records"] += 1
            manifest["maximum_token_id"] = max(manifest["maximum_token_id"], max(retained))
            manifest["raw_utf8_bytes"] += len(text_bytes)
            if manifest["source_records"] % 100 == 0:
                write_json(output / "progress.json", manifest)
            if manifest["token_count"] == args.tokens:
                break
    if manifest["token_count"] != args.tokens:
        raise RuntimeError("Selected archived records exhausted before the token target; no replay permitted")
    if sha256(database) != before_database_hash:
        raise RuntimeError("Archived database changed while packing; no completed manifest published")
    temporary.replace(final)
    artifact_bytes = final.stat().st_size + provenance.stat().st_size
    if artifact_bytes > args.maximum_artifact_bytes:
        raise RuntimeError("Pack plus provenance exceeded its artifact ceiling")
    manifest.update(status="completed", pack_sha256=sha256(final),
                    records_sha256=sha256(provenance), bytes=final.stat().st_size,
                    artifact_bytes=artifact_bytes, runtime_seconds=time.monotonic() - started,
                    vocabulary_size=args.vocabulary_size,
                    ended_utc=datetime.now(timezone.utc).isoformat(),
                    counted_document_bytes_per_token=manifest["raw_utf8_bytes"] / manifest["token_count"])
    write_json(manifest_path, manifest)
    write_json(output / "progress.json", manifest)
    return manifest


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-config", type=Path, default=Path("config/paper_collection_2026-10-19.json"))
    parser.add_argument("--tokenizer-path", type=Path)
    parser.add_argument("--tokenizer-sha256")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--tokens", type=int, default=64 * MIB)
    parser.add_argument("--vocabulary-size", type=int, default=151936)
    parser.add_argument("--maximum-artifact-bytes", type=int, default=512 * MIB)
    parser.add_argument("--minimum-free-bytes", type=int, default=64 * GIB)
    parser.add_argument("--maximum-runtime-seconds", type=int, default=3600)
    args = parser.parse_args(argv)
    if args.tokens <= 0 or not 0 < args.maximum_artifact_bytes <= 512 * MIB:
        parser.error("Token target must be positive and artifacts may occupy at most512MiB")
    if not 0 < args.maximum_runtime_seconds <= 3600 or args.minimum_free_bytes < 64 * GIB:
        parser.error("Packing permits at most1hour and requires64GiB shared free space")
    return args


if __name__ == "__main__":
    args = arguments()
    try:
        print(json.dumps(pack(args), indent=2))
    except Exception as error:
        destination = under_root(args.output_dir)
        destination.mkdir(parents=True, exist_ok=True)
        write_json(destination / "failure.json", dict(status="failed", failure_type=type(error).__name__,
                                                      reason=str(error), ended_utc=datetime.now(timezone.utc).isoformat()))
        raise
