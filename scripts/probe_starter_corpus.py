#!/usr/bin/env python3
"""Bounded, serial source probes for a starter-corpus planning estimate.

Shard prefixes are convenience samples, not a probability sample of records.
No inference, scorer training, full-shard acquisition, or corpus deduplication.
"""
import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import requests
import zstandard
from tokenizers import Tokenizer

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments/starter_corpus_estimate_2026-10-16"
OUT.mkdir(parents=True, exist_ok=True)
SESSION = requests.Session()
MAX_BYTES = 64 * 1024 * 1024
transferred = 0
cached_bytes_read = 0


def fetch(url, name, limit, partial=False):
    global transferred, cached_bytes_read
    path = OUT / name
    if path.exists():
        data = path.read_bytes()
        cached_bytes_read += len(data)
        return data
    headers = {"Range": f"bytes=0-{limit-1}"} if partial else {}
    with SESSION.get(url, headers=headers, stream=True, timeout=40) as response:
        response.raise_for_status()
        if partial and response.status_code != 206:
            raise RuntimeError(f"Range not honored: {response.status_code}")
        parts, size = [], 0
        for part in response.iter_content(65536):
            size += len(part)
            transferred += len(part)
            if size > limit or transferred > MAX_BYTES:
                raise RuntimeError("Probe download bound exceeded")
            parts.append(part)
    data = b"".join(parts)
    path.write_bytes(data)
    return data


def meta(repo, kind):
    return json.loads(fetch(
        f"https://huggingface.co/api/{kind}/{repo}?blobs=true",
        repo.replace("/", "__") + "__metadata.json", 1024 * 1024))


target_path = ROOT / "cache/tokenizers/olmocr2-e52d6f090b7a9007afffbbd6ce510876222fea93/tokenizer.json"
target = Tokenizer.from_file(str(target_path))
gravity_repo = "trillionlabs/Gravity-16B-A3B-Base"
gravity_meta = meta(gravity_repo, "models")
gravity_raw = fetch(
    f"https://huggingface.co/{gravity_repo}/resolve/{gravity_meta['sha']}/tokenizer.json",
    "gravity_tokenizer.json", 24 * 1024 * 1024)
gravity = Tokenizer.from_str(gravity_raw.decode())
dataset = "trillionlabs/TheBioCollection"
data_meta = meta(dataset, "datasets")
files = [f for f in data_meta["siblings"] if "/free_text_stream/" in f["rfilename"]]
tags = re.compile(r"<(protein|dna|rna|smiles|inchi)>(.*?)</\1>", re.I | re.S)
totals = Counter()
domains = Counter()
per_shard = []
hashes = set()
for index, file in enumerate(files):
    raw = fetch(
        f"https://huggingface.co/datasets/{dataset}/resolve/{data_meta['sha']}/{file['rfilename']}",
        f"free_text_prefix_{index:03}.zst", 128 * 1024, partial=True)
    decoded = zstandard.ZstdDecompressor().decompressobj().decompress(raw)
    rows = []
    for line in decoded.split(b"\n")[:-1]:
        if not line.strip():
            continue
        record = json.loads(line)
        if isinstance(record.get("text"), str):
            rows.append(record)
        if len(rows) == 64:
            break
    counts = Counter()
    for record in rows:
        text = record["text"]
        n_target = len(target.encode(text, add_special_tokens=False).ids)
        n_gravity = len(gravity.encode(text, add_special_tokens=False).ids)
        counts.update(records=1, target_tokens=n_target, gravity_tokens=n_gravity,
                      utf8_text_bytes=len(text.encode("utf-8")))
        digest = hashlib.sha256(text.encode()).hexdigest()
        counts["sample_exact_repeats"] += int(digest in hashes)
        hashes.add(digest)
        present = set()
        for match in tags.finditer(text):
            kind = match.group(1).lower()
            counts[kind + "_content_tokens"] += len(target.encode(match.group(2), add_special_tokens=False).ids)
            present.add("molecule" if kind in ("smiles", "inchi") else "genomic" if kind in ("dna", "rna") else "protein")
        domain = next(iter(present)) if len(present) == 1 else "cross_domain" if len(present) > 1 else "untagged"
        domains[domain] += n_target
    totals.update(counts)
    per_shard.append({"path": file["rfilename"], "prefix_sha256": hashlib.sha256(raw).hexdigest(), **dict(counts)})
    print(f"probe {index+1}/{len(files)}: {len(rows)} records", flush=True)

fine_repo = "m-a-p/FineFineWeb"
fine_meta = json.loads(fetch(
    f"https://huggingface.co/api/datasets/{fine_repo}?expand[]=sha",
    "finefineweb_revision.json", 65536))
fine_tree = json.loads(fetch(
    f"https://huggingface.co/api/datasets/{fine_repo}/tree/{fine_meta['sha']}/biology?recursive=false&limit=1000",
    "finefineweb_biology_tree.json", 1024 * 1024))
fine_files = [{"rfilename": f["path"], "size": f.get("size", 0)} for f in fine_tree if f.get("path", "").endswith(".jsonl")]
fine = Counter()
fine_per_shard = []
for i in range(8):
    f = fine_files[round(i * (len(fine_files) - 1) / 7)]
    raw = fetch(
        f"https://huggingface.co/datasets/{fine_repo}/resolve/{fine_meta['sha']}/{f['rfilename']}",
        f"fineweb_prefix_{i:02}.jsonl", 65536, partial=True)
    shard_counts = Counter()
    for line in raw.split(b"\n")[:-1]:
        if not line.strip():
            continue
        record = json.loads(line)
        text = record.get("text", "")
        count = record.get("token_count")
        if text and isinstance(count, (int, float)):
            shard_counts.update(records=1, reported_tokens=int(count),
                                target_tokens=len(target.encode(text, add_special_tokens=False).ids),
                                utf8_text_bytes=len(text.encode("utf-8")))
    fine.update(shard_counts)
    fine_per_shard.append({"path": f["rfilename"], "prefix_sha256": hashlib.sha256(raw).hexdigest(), **dict(shard_counts)})

report = {
    "method": "First at most 64 complete records in each of 32 free-text shard prefixes; eight spread-out FineFineWeb biology prefixes.",
    "limitations": ["Convenience prefixes, not uniformly sampled records; no statistical confidence interval or corpus-wide duplicate-rate estimate.", "Tag-content token counts omit boundary-context effects; full-record token counts use both tokenizers without added special tokens.", "No model inference, new labels, training, full-shard download or corpus-level deduplication."],
    "network_body_bytes_this_execution": transferred,
    "cached_input_bytes_read_this_execution": cached_bytes_read,
    "maximum_network_body_bytes": MAX_BYTES,
    "target_tokenizer_sha256": hashlib.sha256(target_path.read_bytes()).hexdigest(),
    "gravity_tokenizer_revision": gravity_meta["sha"],
    "biocollection_revision": data_meta["sha"],
    "free_text_compressed_bytes": sum(f.get("size", 0) for f in files),
    "biocollection_totals": dict(totals),
    "biocollection_domain_target_tokens": dict(domains),
    "biocollection_target_per_gravity_token": totals["target_tokens"] / totals["gravity_tokens"],
    "biocollection_per_shard": per_shard,
    "finefineweb_revision": fine_meta["sha"],
    "finefineweb_biology_compressed_or_stored_bytes": sum(f.get("size", 0) for f in fine_files),
    "finefineweb_totals": dict(fine),
    "finefineweb_per_shard": fine_per_shard,
    "finefineweb_target_per_reported_token": fine["target_tokens"] / fine["reported_tokens"] if fine["reported_tokens"] else None,
}
(OUT / "probe_summary.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if k != "biocollection_per_shard"}, indent=2))
