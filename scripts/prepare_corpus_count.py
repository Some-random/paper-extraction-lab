#!/usr/bin/env python3
"""Freeze existing paper exports and full released-shard inventories for counting."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "experiments/corpus_count_2026-10-17"
CONFIG = ROOT / "config/corpus_count_2026-10-17.json"
PROBE = ROOT / "experiments/starter_corpus_estimate_2026-10-16"


def main():
    if CONFIG.exists():
        raise SystemExit("Frozen configuration already exists; use it to resume.")
    RUN.mkdir(parents=True, exist_ok=True)
    native = ROOT / "experiments/pmc_native_fresh_500_2026-10-15"
    state_bytes = (native / "state.json").read_bytes()
    papers = json.loads(state_bytes)["papers"]
    canonical = RUN / "local_papers.jsonl"
    document_hashes = {}
    with canonical.open("x") as out:
        for paper in sorted(papers, key=lambda p: p["pmcid"]):
            path = ROOT / paper["source_directory"] / "document.json"
            raw = path.read_bytes()
            document_hashes[paper["pmcid"]] = hashlib.sha256(raw).hexdigest()
            doc = json.loads(raw)
            parts = [doc["title"]] + [b["training_text"] for b in doc["blocks"]]
            for visual in doc["visuals"]:
                parts.extend([visual.get("caption_training_text", ""), visual.get("notes_training_text", "")])
                if visual.get("table"):
                    parts.append(visual["table"]["text_tsv"])
            record = {
                "text": "\n\n".join(p for p in parts if p.strip()),
                "id": paper["pmcid"], "doi": paper.get("doi"),
                "source_xml_sha256": doc["source_xml_sha256"],
                "source_document": str(path.relative_to(ROOT)),
                "source_document_sha256": document_hashes[paper["pmcid"]],
                "license": paper.get("license_code"), "version": paper.get("version"),
                "images": sum(len(v.get("assets", [])) for v in doc["visuals"]),
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    tokenizer = "cache/tokenizers/olmocr2-e52d6f090b7a9007afffbbd6ce510876222fea93/tokenizer.json"
    bio = json.loads((PROBE / "trillionlabs__TheBioCollection__metadata.json").read_text())
    web_rev = json.loads((PROBE / "finefineweb_revision.json").read_text())["sha"]
    bio_files = [f for f in bio["siblings"] if "/free_text_stream/" in f["rfilename"]]
    web_files = json.loads((PROBE / "finefineweb_biology_tree.json").read_text())
    files = [{"id": "pmc_local", "source": "pmc", "path": str(canonical.relative_to(ROOT)),
              "format": "jsonl", "bytes": canonical.stat().st_size,
              "sha256": hashlib.sha256(canonical.read_bytes()).hexdigest(),
              "expected_records": len(papers)}]
    remote = {"biocollection": [], "finefineweb": []}
    for source, dataset, revision, entries in [
        ("biocollection", "trillionlabs/TheBioCollection", bio["sha"], bio_files),
        ("finefineweb", "m-a-p/FineFineWeb", web_rev, web_files),
    ]:
        for entry in entries:
            path = entry.get("rfilename", entry.get("path"))
            if not path.endswith((".jsonl", ".jsonl.zst")):
                continue
            expected_hash = entry["lfs"].get("sha256", entry["lfs"].get("oid"))
            remote[source].append({
                "id": source + "_" + Path(path).name, "source": source,
                "path": str((RUN / "raw" / source / Path(path).name).relative_to(ROOT)),
                "url": f"https://huggingface.co/datasets/{dataset}/resolve/{revision}/{path}",
                "format": "jsonl.zst" if path.endswith(".zst") else "jsonl",
                "bytes": entry["size"], "sha256": expected_hash,
                "dataset_path": path, "revision": revision,
            })
    # Expose both source types early; the bounded run will leave an explicit tail.
    for index in range(max(map(len, remote.values()))):
        for source in ("finefineweb", "biocollection"):
            if index < len(remote[source]):
                files.append(remote[source][index])
    inventory = json.loads((ROOT / "reports/bio_foundation_review_2026-10-15/starter_corpus_estimate.json").read_text())
    config = {
        "run_id": RUN.name, "destination": str(RUN.relative_to(ROOT)),
        "report_directory": "reports/corpus_count_2026-10-17", "tokenizer_path": tokenizer,
        "tokenizer_sha256": hashlib.sha256((ROOT / tokenizer).read_bytes()).hexdigest(),
        "tokenizer_identity": "cached olmOCR 2 Qwen-family tokenizer; fixed counting reference, no added special tokens",
        "limits": {"runtime_seconds": 43200, "network_reserved_bytes": 8 * 2**30,
                   "new_artifact_bytes": 16 * 2**30, "minimum_free_bytes": 32 * 2**30,
                   "maximum_line_bytes": 16 * 2**20, "maximum_text_bytes": 4 * 2**20},
        "cpu_threads": 2, "gpu_count": 0, "files": files,
        "sources": {
            "pmc": {"name": "PMC local biology papers", "acquisition_route": "online_papers",
                    "content_category": "papers", "source_scope": "Frozen local selected papers, not the whole PMC archive",
                    "expected_files": 1, "expected_records": len(papers), "whole_source_inventory": False},
            "finefineweb": {"name": "FineFineWeb biology", "acquisition_route": "existing_datasets",
                            "content_category": "web_text", "revision": web_rev,
                            "expected_files": len(remote["finefineweb"]), "whole_source_inventory": True},
            "biocollection": {"name": "TheBioCollection free-text stream", "acquisition_route": "existing_datasets",
                              "content_category": "database_records", "revision": bio["sha"],
                              "expected_files": len(remote["biocollection"]), "whole_source_inventory": True},
        },
        "source_families": [{"id": f["id"], "name": f["name"], "group": f["group"],
                             "upstream_of": f["upstream_of"]} for f in inventory["aggregation"]["families"]],
        "local_paper_state_sha256": hashlib.sha256(state_bytes).hexdigest(),
        "counting_policy": {
            "text": "Count original dataset text; local papers count title, selected blocks, captions/notes and tables once. Do not add chunks/interleaved copies.",
            "exact_dedup": "SHA256 after whitespace collapse; preserve case, punctuation and scientific strings. Fixed input order keeps first occurrence across all sources.",
            "modalities": "Assign each full-record token by its starting character offset to explicit protein/dna/rna/smiles/inchi content, otherwise text_or_unclassified. Tag boundaries stay in text_or_unclassified.",
            "images": "Preserved original assets are not vision-tokenized; image token count is unknown.",
            "scope": "Candidate tokens before biology/clinical selection, quality filtering and near-duplicate removal. No extrapolation to unscanned files.",
        },
        "authorization": "User requested setting up the actual counting pipeline and starting work on 2026-10-17. New bounded CPU-only run; old acquisition jobs remain untouched.",
    }
    CONFIG.write_text(json.dumps(config, indent=2) + "\n")
    print(json.dumps({"config": str(CONFIG.relative_to(ROOT)), "papers": len(papers),
                      "remote_shards": {k: len(v) for k, v in remote.items()},
                      "remote_bytes": sum(f.get("bytes", 0) for f in files if "url" in f)}))


if __name__ == "__main__":
    main()
