#!/usr/bin/env python3
"""Reproduce assumption-driven starter forecasts from checked-in probe counts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/bio_foundation_review_2026-10-15"
probe = json.loads((REPORT / "starter_corpus_probe.json").read_text())
availability = json.loads((ROOT / "reports/pmc_cns_availability_2026-10-13/availability.json").read_text())
global_availability = json.loads((ROOT / "reports/pmc_global_availability_2026-10-14.json").read_text())
archive = json.loads((REPORT / "pmc_archive_snapshot.json").read_text())
pmc = next(r["xml_text_mining_candidates"] for r in availability["rows"]
           if r["scope"] == "curated_related_union")
web_raw = 86.99e9 * probe["finefineweb_target_per_reported_token"]
records_raw = 33.8e9 * probe["biocollection_target_per_gravity_token"]
parameters = {
    "low": {"paper_tokens_each": 8000, "paper_research_fraction": .5,
            "paper_dedup_retention": .8, "web_research_fraction": .05,
            "web_dedup_retention": .85, "record_dedup_retention": .8},
    "central": {"paper_tokens_each": 12000, "paper_research_fraction": .7,
                "paper_dedup_retention": .9, "web_research_fraction": .15,
                "web_dedup_retention": .9, "record_dedup_retention": .9},
    "high": {"paper_tokens_each": 23334, "paper_research_fraction": .9,
             "paper_dedup_retention": .95, "web_research_fraction": .25,
             "web_dedup_retention": .95, "record_dedup_retention": .95},
}
scenarios = {}
for name, p in parameters.items():
    paper_dedup = pmc * p["paper_tokens_each"] * p["paper_dedup_retention"]
    web_dedup = web_raw * p["web_dedup_retention"]
    records = records_raw * p["record_dedup_retention"]
    content = {"direct_paper_text": paper_dedup * p["paper_research_fraction"],
               "imported_web_origin_text": web_dedup * p["web_research_fraction"],
               "imported_biological_records": records}
    total = sum(content.values())
    routes = {"online_papers": content["direct_paper_text"], "direct_web_urls": 0,
              "existing_datasets": content["imported_web_origin_text"] + records}
    assert abs(sum(routes.values()) - total) < 1
    scenarios[name] = {"assumptions": p,
                       "dedup_only_tokens": {"papers": paper_dedup, "web_origin": web_dedup,
                                             "biological_records": records},
                       "dedup_only_total_tokens": paper_dedup + web_dedup + records,
                       "research_starter_content_tokens": content,
                       "research_starter_total_tokens": total,
                       "acquisition_route_tokens": routes,
                       "content_percentages": {k: 100 * v / total for k, v in content.items()}}

central = scenarios["central"]
sample = probe["biocollection_totals"]
record_tokens = central["research_starter_content_tokens"]["imported_biological_records"]
modality = {
    "protein_sequence_spans": record_tokens * sample["protein_content_tokens"] / sample["target_tokens"],
    "dna_rna_sequence_spans": record_tokens * (sample["dna_content_tokens"] + sample["rna_content_tokens"]) / sample["target_tokens"],
    "smiles_inchi_spans": record_tokens * (sample["smiles_content_tokens"] + sample["inchi_content_tokens"]) / sample["target_tokens"],
}
modality["other_text_including_annotations_and_tag_boundaries"] = central["research_starter_total_tokens"] - sum(modality.values())
assert abs(sum(modality.values()) - central["research_starter_total_tokens"]) < 1
for source in central["research_starter_content_tokens"]:
    assert scenarios["low"]["research_starter_content_tokens"][source] <= central["research_starter_content_tokens"][source] <= scenarios["high"]["research_starter_content_tokens"][source]

# Ratios from small source probes are used for planning, not statistical estimates.
record_text_bytes = record_tokens * sample["utf8_text_bytes"] / sample["target_tokens"]
web_sample = probe["finefineweb_totals"]
web_text_bytes = central["research_starter_content_tokens"]["imported_web_origin_text"] * web_sample["utf8_text_bytes"] / web_sample["target_tokens"]
paper_text_bytes = central["research_starter_content_tokens"]["direct_paper_text"] * 4
paper_count = pmc * parameters["central"]["paper_research_fraction"]
# Actual size measurements from 454 local accepted papers; content selection may change these means.
paper_original_bytes_each = (2301887326 + 1284695666) / 454
paper_xml_bytes_each = 98461187 / 454
all_paper_artifact_bytes_each = 4633654285 / 454
storage = {
    "available_source_download_bytes": {"all_finefineweb_biology_jsonl": probe["finefineweb_biology_compressed_or_stored_bytes"],
                                        "biocollection_free_text_zstd": probe["free_text_compressed_bytes"]},
    "central_text_utf8_bytes_proxy": paper_text_bytes + web_text_bytes + record_text_bytes,
    "central_uint32_token_ids_bytes": central["research_starter_total_tokens"] * 4,
    "central_scope_selected_paper_count_before_training_dedup_proxy": paper_count,
    "central_paper_pdf_figure_bytes_proxy": paper_count * paper_original_bytes_each,
    "central_paper_xml_bytes_proxy": paper_count * paper_xml_bytes_each,
    "central_paper_current_export_layout_bytes_proxy": paper_count * all_paper_artifact_bytes_each,
    "text_sequence_processing_allowance_GiB": [500, 800],
    "notes": ["500-800 GiB is an engineering allowance for selected raw inputs, canonical text, token IDs, indexes and bounded scratch; not a measured peak.",
              "The full FineFineWeb biology download is not needed simultaneously if shards are processed serially.",
              "The text/sequence allowance excludes paper PDFs/figures, supplementary raw experiments, model weights, environments and checkpoints.",
              "Training deduplication earns no automatic storage saving: selected originals remain preserved, and token retention is not a document-retention measurement.",
              "Retaining all paper originals/figures is a separate multi-TiB budget. The current export layout contains several text/JSON views."]
}

# One combined capacity estimate for the quantified subset, including original paper assets.
# Additional-paper storage is a size extrapolation, not an estimate of biological relevance.
storage.update({
    "central_overall_working_bytes": [
        storage["central_paper_pdf_figure_bytes_proxy"] + gib * 2**30
        for gib in storage["text_sequence_processing_allowance_GiB"]],
    "recommended_initial_capacity_tib": 4,
    "additional_million_papers_pdf_figure_bytes_proxy": 1_000_000 * paper_original_bytes_each,
    "one_trillion_uint32_token_ids_bytes": 1_000_000_000_000 * 4,
    "shared_scratch_free_tib_snapshot": 1.4,
    "shared_scratch_snapshot_date_pst": "2026-10-16",
})
paper_availability = {
    "archive_article_records_rounded": archive["archive_records_rounded"],
    "archive_source": archive["source"],
    "archive_checked_date_pst": archive["checked_date_pst"],
    "journal_subset_count": 55,
    "journal_subset_xml_candidates": pmc,
    "broader_xml_candidates": global_availability["queries"]["xml_text_mining_candidates"]["count"],
    "broader_inventory_date_pst": global_availability["checked_date_pst"],
    "broader_biological_yield": "unmeasured",
    "note": "Archive total, bulk text-mining candidates and the journal subset are nested, not additive. Counts are not a measured nonclinical-biology corpus. The legacy 49.1B forecast is superseded as an overall estimate.",
}
broader_pmc = paper_availability["broader_xml_candidates"]
paper_text_scenarios = {
    "status": "gross_text_volume_scenarios_not_retained_biology_counts",
    "candidate_papers": broader_pmc,
    "assumed_tokens_per_paper": [8000, 12000, 23334],
    "gross_text_tokens": [broader_pmc * n for n in (8000, 12000, 23334)],
    "note": "Uses the full text-mining candidate inventory, before biological scope selection and deduplication. Per-paper lengths are assumptions, not a representative measured distribution.",
}
report = {
    "date_pst": "2026-10-16", "status": "broad_source_inventory_with_legacy_subset_scenarios",
    "scope": "Full PMC text-mining candidate inventory, other scientific-paper pools, biology-labelled web text, annotated biological database records; raw biomolecule pools grouped as secondary priority.",
    "scope_exclusions": ["TheBioCollection instruction stream from the free-text amount", "general replay from the biological inventory", "unmeasured incremental counts assigned to overlapping sources"],
    "counting": "Current inventories retain author-native units; gross paper scenarios use assumed per-paper lengths. Legacy retained-token scenarios use the pinned Qwen-family tokenizer and convenience-probe ratios.",
    "published_input_counts": {"selected_pmc_xml_candidates": pmc, "finefineweb_biology_source_tokens": 86.99e9,
                               "biocollection_free_text_gravity_tokens": 33.8e9},
    "sources": {"pmc_inventory": "../pmc_cns_availability_2026-10-13/availability.json",
                "broader_pmc_inventory": "../pmc_global_availability_2026-10-14.json",
                "finefineweb": "https://huggingface.co/datasets/m-a-p/FineFineWeb",
                "biocollection": "https://huggingface.co/datasets/trillionlabs/TheBioCollection",
                "biocollection_paper": "https://arxiv.org/html/2607.08803v1"},
    "scenarios": scenarios,
    "legacy_scenarios_status": "Superseded as an overall corpus forecast. Retained for provenance; the 15% central web research-retention assumption is unmeasured and is not the current planning estimate.",
    "collection_priorities": {
        "primary": ["research_papers", "biology_web_text", "annotated_biological_database_records"],
        "secondary": ["raw_sequence_and_structure_exports"],
        "basis": "Project priority for text-centred biological CPT: prefer content connecting entities to functions, mechanisms and observations. This is not an experimentally established ranking of training usefulness.",
    },
    "paper_text_scenarios": paper_text_scenarios,
    "current_web_and_record_inventory": {
        "web_source_tokens": 86.99e9, "record_source_tokens": 33.8e9,
        "web_tokens_local_tokenizer_proxy": web_raw,
        "record_tokens_local_tokenizer_proxy": records_raw,
        "web_research_retention": None,
        "note": "Published source amounts before our filtering and cross-source deduplication. Local-tokenizer conversions use convenience samples. No point estimate of retained web tokens is supported yet.",
    },
    "central_modality_tokens_conditional_on_prefix_representativeness": modality,
    "storage": storage,
    "paper_availability": paper_availability,
    "larger_source_inventory": [
        {"id": "olmo3_science_pdfs", "name": "OLMo 3 / olmOCR science PDFs",
         "amount": 972_000_000_000, "unit": "source_tokenizer_text_tokens",
         "scope": "Academic documents across subjects; biological share not yet measured.",
         "source": "https://arxiv.org/html/2512.13961v2#S3.SS4",
         "release": "https://github.com/allenai/dolma3/blob/main/datasets/dolma3_mix/pools/9T/README.md",
         "included_in_starter_forecast": False},
        {"id": "opengenome2", "name": "OpenGenome2 / Evo 2",
         "amount": 8_800_000_000_000, "unit": "nucleotide_positions_rounded",
         "scope": "Biological sequence corpus; not a count in the local Qwen tokenizer or a cross-source deduplicated total.",
         "source": "https://www.nature.com/articles/s41586-026-10176-5",
         "release": "https://huggingface.co/datasets/arcinstitute/opengenome2",
         "included_in_starter_forecast": False},
    ],
    "limitations": ["Low/high are sensitivity scenarios, not confidence intervals or measured retention rates.",
                    "Research selection fractions (especially web 5/15/25%) and additional dedup retention are explicit assumptions.",
                    "Prefixes are not a probability sample; modality and tokenizer ratios may shift after wider sampling.",
                    "The 454-paper sample is journal-balanced and length-capped, not representative of the 552,024-candidate inventory.",
                    "A biological database-domain count includes descriptions/annotations and is not a pure sequence count.",
                    "Modality projections count tagged spans in imported database records only; untagged sequence strings in paper/web prose are not separately identified.",
                    "Dedup across datasets uses identity/content checks; dedup within protein/molecule records must preserve distinct annotations and relations.",
                    "No full corpus, trained scorer, global dedup index or learned mixture was produced for this estimate."]
}
(REPORT / "starter_corpus_estimate.json").write_text(json.dumps(report, indent=2) + "\n")
print("PMC archive records", archive["archive_records_rounded"], "text-mining candidates", broader_pmc)
print("Full-PMC gross text scenarios, B", [round(v / 1e9, 1) for v in paper_text_scenarios["gross_text_tokens"]])
print("Source-native tokens, B", {"biology_web": 86.99, "annotated_database_records": 33.8})
print("Earlier 35-70B subset scenarios retained as superseded provenance; not a current corpus total.")
