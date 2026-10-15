#!/usr/bin/env python3
"""Inspect a bounded, versioned web-corpus prefix; never fetch a full shard.

Use --input-prefix to reproduce parsing without network access. Text and raw
bytes belong in ignored experiment storage; the summary contains metadata only.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

import requests


REVISION = "7fd92dc825a75cbff271a5a52eea0eda91a2c112"
SOURCE_URL = (
    "https://huggingface.co/datasets/m-a-p/FineFineWeb/resolve/"
    + REVISION + "/biology/biology_000000.jsonl"
)


def parse_prefix(raw):
    records, discarded = [], 0
    # A range may end inside a JSON object or a UTF-8 character. Only the
    # terminal fragment may be incomplete; malformed interior rows are errors.
    lines = raw.splitlines(keepends=True)
    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
        except (ValueError, UnicodeDecodeError):
            if i != len(lines) - 1 or line.endswith(b"\n"):
                raise ValueError("malformed complete JSONL record") from None
            discarded = len(line)
            continue
        if not isinstance(record, dict) or not isinstance(record.get("text"), str):
            raise ValueError("record lacks a text field")
        records.append(record)
    return records, discarded


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input-prefix", type=Path)
    ap.add_argument("--bytes", type=int, default=65536)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if not 1 <= args.bytes <= 1048576:
        ap.error("byte budget must be between 1 and 1,048,576")
    if args.output.exists():
        ap.error("output directory already exists; preserve previous samples")
    transport = {"mode": "offline_prefix", "network_bytes_this_run": 0}
    if args.input_prefix:
        if args.input_prefix.stat().st_size > args.bytes:
            ap.error("input exceeds the byte budget")
        raw = args.input_prefix.read_bytes()
    else:
        # Cache-bust the resolver, not the original content: stale signed CDN
        # redirects can expire. HTTPS verification remains enabled.
        try:
            with requests.get(
                SOURCE_URL,
                params={"download": "true", "bounded_probe": int(time.time())},
                headers={"Range": f"bytes=0-{args.bytes - 1}", "Accept-Encoding": "identity"},
                stream=True, timeout=(15, 40),
            ) as response:
                response.raise_for_status()
                content_range = response.headers.get("Content-Range", "")
                if response.status_code != 206 or not content_range.startswith("bytes 0-"):
                    raise ValueError("server did not honor the bounded range request")
                raw = response.raw.read(args.bytes, decode_content=False)
                if response.headers.get("Content-Encoding", "identity") != "identity":
                    raise ValueError("unexpected transfer encoding")
                transport = {"mode": "http_range", "status": 206,
                             "content_range": content_range,
                             "network_bytes_this_run": len(raw)}
        except requests.RequestException as exc:
            # Avoid printing signed redirect URLs in routine error reports.
            raise SystemExit(f"{type(exc).__name__}: bounded request failed") from None
    records, discarded = parse_prefix(raw)
    metadata = []
    for i, record in enumerate(records):
        entry = {k: v for k, v in record.items() if k != "text"}
        entry.update(prefix_record_index=i,
                     text_characters=len(record["text"]),
                     text_sha256=hashlib.sha256(record["text"].encode()).hexdigest())
        metadata.append(entry)
    summary = {
        "dataset": "m-a-p/FineFineWeb", "revision": REVISION,
        "source_url": SOURCE_URL, "sampling": "first complete records of a shard prefix; not random",
        "prefix_bytes": len(raw), "prefix_sha256": hashlib.sha256(raw).hexdigest(),
        "complete_records": len(records), "discarded_terminal_fragment_bytes": discarded,
        "dataset_reported_token_count_sum": sum(r.get("token_count", 0) for r in records),
        "counting_tokenizer": "not identified by the dataset card; no target retokenization here",
        "accepted_for_training": 0, "transport": transport, "records": metadata,
    }
    args.output.mkdir(parents=True)
    (args.output / "prefix.bin").write_bytes(raw)
    (args.output / "records.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ["prefix_bytes", "complete_records",
          "dataset_reported_token_count_sum", "accepted_for_training"]}))


if __name__ == "__main__":
    main()
