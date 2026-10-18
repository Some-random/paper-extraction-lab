#!/usr/bin/env python3
"""Reconcile frozen shard and paper manifests without reading source payloads.

The public outputs contain dataset-relative names and aggregate paper counts.
Local/private paper paths are written only with --private-paper-manifest.
Equal file size is deliberately not presented as a successful checksum check.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ONLINE_SOURCES = ("finefineweb", "biocollection")


def normalize_pmcid(value):
    """Normalize the article ID, keeping version comparison a separate task."""
    value = str(value or "").strip()
    match = re.fullmatch(r"(?:PMC)?([0-9]+)(?:\.[0-9]+)?", value, re.I)
    if not match:
        raise ValueError("Invalid PMC identifier")
    return "PMC" + str(int(match.group(1)))


def inspect_local_file(path, expected_bytes):
    """Only stat a named final file or its runner-compatible .part file."""
    path = Path(path)
    try:
        size = path.stat().st_size
    except FileNotFoundError:
        partial = path.with_suffix(path.suffix + ".part")
        try:
            partial_size = partial.stat().st_size
        except FileNotFoundError:
            return {"local_file_status": "missing", "local_bytes": 0,
                    "partial_bytes": 0, "checksum_status": "not_recomputed"}
        except OSError:
            return {"local_file_status": "unreadable_metadata", "local_bytes": None,
                    "partial_bytes": None, "checksum_status": "not_recomputed"}
        return {"local_file_status": "partial_download", "local_bytes": 0,
                "partial_bytes": partial_size, "checksum_status": "not_recomputed"}
    except OSError:
        return {"local_file_status": "unreadable_metadata", "local_bytes": None,
                "partial_bytes": None, "checksum_status": "not_recomputed"}
    status = ("same_size_unverified" if size == expected_bytes else
              "truncated" if size < expected_bytes else "oversized")
    return {"local_file_status": status, "local_bytes": size,
            "partial_bytes": 0, "checksum_status": "not_recomputed"}


def reconcile_online(files, counting_files, root):
    rows = []
    for item in files:
        if item["source"] not in ONLINE_SOURCES:
            continue
        count = counting_files.get(item["id"], {})
        rows.append({"source": item["source"], "file_id": item["id"],
                     "dataset_path": item["dataset_path"],
                     "revision": item["revision"], "expected_bytes": item["bytes"],
                     "expected_sha256": item["sha256"],
                     **inspect_local_file(Path(root) / item["path"], item["bytes"]),
                     "count_status": count.get("status", "not_in_counting_summary"),
                     "rows_counted": count.get("rows_committed", 0)})
    return rows


def summarize_online(rows):
    sources = {}
    for source in ONLINE_SOURCES:
        selected = [row for row in rows if row["source"] == source]
        same_size = [row for row in selected
                     if row["local_file_status"] == "same_size_unverified"]
        sources[source] = {
            "release_files": len(selected),
            "release_bytes": sum(row["expected_bytes"] for row in selected),
            "local_same_size_files": len(same_size),
            "local_same_size_bytes": sum(row["local_bytes"] for row in same_size),
            "local_file_status_counts": dict(Counter(row["local_file_status"] for row in selected)),
            "completed_counting_files": sum(row["count_status"] == "complete" for row in selected),
            "partly_counted_files": sum(row["rows_counted"] > 0 and row["count_status"] != "complete"
                                        for row in selected),
            "missing_files": sum(row["local_file_status"] == "missing" for row in selected),
            "missing_file_bytes": sum(row["expected_bytes"] for row in selected
                                      if row["local_file_status"] == "missing"),
            "revisions": sorted({row["revision"] for row in selected}),
            "payload_checksums_recomputed": 0,
        }
    return sources


def selected_papers(initial_state, counting_files, expansion_directory):
    """Use accepted initial metadata and completed expansion rows, not all probes."""
    selected = {}
    for paper in initial_state["papers"]:
        pmcid = normalize_pmcid(paper["pmcid"])
        selected[pmcid] = {"pmcid": pmcid, "origin": "initial_pilot",
                           "doi": paper.get("doi"), "version": paper.get("version")}
    for file_id, count in counting_files.items():
        if not file_id.startswith("pmc_new_") or count["status"] != "complete":
            continue
        pmcid = normalize_pmcid(file_id.removeprefix("pmc_new_"))
        metadata_path = Path(expansion_directory) / pmcid / "selected_metadata.json"
        metadata = json.loads(metadata_path.read_text())
        if normalize_pmcid(metadata["pmcid"]) != pmcid:
            raise ValueError("Expansion identifier disagrees with counting summary")
        selected[pmcid] = {"pmcid": pmcid, "origin": "expansion_pilot",
                           "doi": metadata.get("doi"), "version": metadata.get("version")}
    return selected


def reconcile_papers(selected, cached_rows):
    cached = {}
    for row in cached_rows:
        pmcid = normalize_pmcid(row["pmcid"])
        cached.setdefault(pmcid, []).append(row)
    selected_ids, cached_ids = set(selected), set(cached)
    overlap = selected_ids & cached_ids
    summary = {
        "selected_pilot_pmcs": len(selected_ids), "cached_pmcids": len(cached_ids),
        "cached_xml_files": sum(len(rows) for rows in cached.values()),
        "cached_manifest_bytes": sum(int(row["bytes"]) for rows in cached.values() for row in rows),
        "overlap_by_pmcid": len(overlap),
        "additional_cached_pmcids": len(cached_ids - selected_ids),
        "union_pmcids": len(selected_ids | cached_ids),
        "scope_and_version_equivalence": "Not established by identifier comparison",
        "paper_payloads_read": 0,
    }
    private = []
    for pmcid in sorted(selected_ids | cached_ids):
        private.append({"pmcid": pmcid, "selected_pilot": pmcid in selected_ids,
                        "cached": pmcid in cached_ids,
                        "pilot_metadata": selected.get(pmcid),
                        "cached_manifest_rows": cached.get(pmcid, [])})
    return summary, private


def write_outputs(public_directory, source_summary, paper_summary, rows, private_path=None,
                  private_papers=None, counting_updated_at=None):
    public_directory = Path(public_directory)
    public_directory.mkdir(parents=True, exist_ok=True)
    summary = {
        "checked_at_pst": datetime.now(timezone(timedelta(hours=-8))).isoformat(),
        "method": "Metadata-only joins of frozen shard manifests, local file stats, counting summary and paper ID metadata",
        "counting_summary_updated_at_pst": counting_updated_at,
        "online_sources": source_summary, "papers": paper_summary,
        "limitations": [
            "Matching byte size is not a payload checksum or complete readability check.",
            "Counting status is historical evidence from the supplied summary, not a new scan.",
            "PMC IDs identify articles; versions, source hashes, licenses and biology scope require separate checks.",
            "Missing-file bytes describe the pinned release remainder, not cross-source unique bytes or a download instruction.",
            "No record contents were read and no new token counts were computed.",
        ],
    }
    summary_path = public_directory / "reconciliation_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    csv_path = public_directory / "online_shard_reconciliation.csv"
    if rows:
        with csv_path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    if private_path:
        private_path = Path(private_path)
        private_path.parent.mkdir(parents=True, exist_ok=True)
        private_path.write_text(json.dumps(private_papers, indent=2) + "\n")
    return summary_path, csv_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--config", default="config/corpus_count_2026-10-17.json")
    parser.add_argument("--counting-summary", default="reports/corpus_count_2026-10-17/summary.json")
    parser.add_argument("--initial-paper-state", default="experiments/pmc_native_fresh_500_2026-10-15/state.json")
    parser.add_argument("--expansion-directory", default="experiments/corpus_count_2026-10-17/pmc_expansion/papers")
    parser.add_argument("--cached-paper-manifest", default="experiments/cluster_data_inventory_2026-10-18/pmc_xml_manifest.csv")
    parser.add_argument("--public-output", default="reports/corpus_overview_2026-10-18")
    parser.add_argument("--private-paper-manifest", default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    read_json = lambda path: json.loads((root / path).read_text())
    config = read_json(args.config)
    counting = read_json(args.counting_summary)
    rows = reconcile_online(config["files"], counting["files"], root)
    selected = selected_papers(read_json(args.initial_paper_state), counting["files"], root / args.expansion_directory)
    with (root / args.cached_paper_manifest).open(newline="") as handle:
        paper_summary, private = reconcile_papers(selected, csv.DictReader(handle))
    paths = write_outputs(root / args.public_output, summarize_online(rows), paper_summary, rows,
                          root / args.private_paper_manifest if args.private_paper_manifest else None,
                          private, counting.get("updated_at_pst"))
    for path in paths:
        print(path.relative_to(root))


if __name__ == "__main__":
    main()
