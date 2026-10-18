#!/usr/bin/env python3
"""Freeze a PMC expansion plan and preserve the corrected local paper view."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from corpus_count import canonical_paper_text, sha256


def main():
    path = ROOT / "config/corpus_count_pmc_expansion_2026-10-17.json"
    if path.exists():
        raise SystemExit("Expansion plan already frozen; resume it.")
    run = ROOT / "experiments/corpus_count_2026-10-17"
    corrected = run / "local_papers_corrected.jsonl"
    with (run / "local_papers.jsonl").open() as source, corrected.open("x") as out:
        for line in source:
            record = json.loads(line)
            doc = json.loads((ROOT / record["source_document"]).read_text())
            record["text"] = canonical_paper_text(doc)
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    plan = {
        "base_config": "config/corpus_count_2026-10-17.json",
        "target_new_papers": 5000, "maximum_phase_seconds": 10800,
        "maximum_new_paper_download_bytes": 3 * 2**30,
        "maximum_xml_bytes": 4 * 2**20, "maximum_table_rows": 2000,
        "candidates_per_stratum": 500,
        "years": [[2000, 2009], [2010, 2014], [2015, 2019], [2020, 2023], [2024, 2026]],
        "topics": {
            "genes_and_genomes": ["gene", "genome", "RNA", "transcription"],
            "proteins_and_cells": ["protein", "enzyme", "cellular", "metabolism"],
            "organisms_and_ecology": ["bacteria", "plant", "microbiome", "evolution"],
            "neuroscience_and_immunity": ["neuron", "synapse", "immune", "antibody"],
        },
        "accepted_article_types": ["research-article", "review-article", "methods-article", "brief-report"],
        "correction": {"file_id": "pmc_local", "path": str(corrected.relative_to(ROOT)),
                       "sha256": sha256(corrected), "bytes": corrected.stat().st_size,
                       "expected_records": 454,
                       "reason": "Count captions and tables already present in blocks once, retaining unmatched source visuals."},
        "policy": "One serial worker using existing counting ledger and cumulative 8 GiB/16 GiB/12h limits. Prioritize this bounded paper phase, then resume web/database scanning. Native XML, version/license/checksum metadata and source-linked parsed records; PDF/media/supplement bytes deferred and their source URLs preserved. No OCR, inference or training. Broad PMC topic/year queries; no journal restriction; selected convenience corpus, not a representative sample or a biology-wide census.",
        "authorization": "User asked why we do not process more papers on October 17; expand the actual counting/acquisition queue.",
    }
    path.write_text(json.dumps(plan, indent=2) + "\n")
    print(json.dumps({"plan": str(path.relative_to(ROOT)), "target_new_papers": 5000,
                      "corrected_local_bytes": corrected.stat().st_size}))


if __name__ == "__main__":
    main()
