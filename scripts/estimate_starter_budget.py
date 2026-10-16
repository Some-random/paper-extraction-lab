#!/usr/bin/env python3
"""Reproduce assumption-driven starter forecasts from checked-in probe counts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/bio_foundation_review_2026-10-15"
probe = json.loads((REPORT / "starter_corpus_probe.json").read_text())
availability = json.loads((ROOT / "reports/pmc_cns_availability_2026-10-13/availability.json").read_text())
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

# Runtime scenarios: these rates and experiment counts are planning assumptions.
# Input parsing and scoring must process candidate text, not just retained text.
input_tokens = pmc * parameters["central"]["paper_tokens_each"] + web_raw + records_raw
score_tokens = sum(central["dedup_only_tokens"][k] for k in ("papers", "web_origin"))
transfer_bytes = sum(storage["available_source_download_bytes"].values()) + pmc * paper_xml_bytes_each
acquisition_hours = [transfer_bytes / rate / 3600 + pmc * latency / 3600
                     for rate, latency in [(100e6, .2), (20e6, 1.)]]
cpu_pass_hours = [input_tokens * 4 / rate / 3600 for rate in (3e6, 1e6)]
application_gpu_hours = [score_tokens / rate / 3600 for rate in (200000, 50000)]
teacher_gpu_hours = [20000 * (2048 / prefill + 256 / decode) / 3600
                     for prefill, decode in [(2000, 80), (500, 20)]]
scoring_total = [application_gpu_hours[i] + teacher_gpu_hours[i] + [4, 12][i]
                 for i in (0, 1)]
proxy_gpu_hours = [30 * 6 * 30e6 * 3e9 / rate / 3600 for rate in (75e12, 20e12)]
confirmation_gpu_hours = [3 * 6 * 7e9 * 1e9 / rate / 3600 for rate in (125e12, 50e12)]
mix_gpu_hours = [(proxy_gpu_hours[i] + confirmation_gpu_hours[i]) * 1.25 for i in (0, 1)]
resource_plan = {
    "status": "unbenchmarked_execution_scenarios_not_jobs_or_reservations",
    "cluster_reference": {"date_pst": "2026-10-16", "a100_80gb": 71, "b200_180gb": 8,
                          "shared_scratch_free_tib_rounded": 1.5,
                          "note": "Installed/shared capacity, not an allocation. B200 speedup is not assumed."},
    "acquisition": {"candidate_xml_objects": pmc, "selected_source_bytes": transfer_bytes,
                    "assumed_transfer_bytes_per_second": [20e6, 100e6],
                    "assumed_xml_request_overhead_seconds": [.2, 1.],
                    "calculated_hours": acquisition_hours, "planning_days": [2, 7],
                    "note": "One serial fetcher; dataset shards transfer in hours, but individual XML requests add latency. PDFs/figures excluded."},
    "normalization_cleaning_dedup": {"candidate_tokens": input_tokens, "assumed_token_passes": 4,
                                   "assumed_aggregate_tokens_per_second": [1e6, 3e6],
                                   "cpu_cores": 16, "ram_gib": [128, 256],
                                   "calculated_pass_hours": cpu_pass_hours, "planning_days": [3, 10],
                                   "note": "Throughput is assumed for a compact implementation; extra time covers sorting, I/O and checks. The current two-thread runner is not this allocation."},
    "scoring_and_review": {"paper_web_candidate_tokens": score_tokens,
                           "assumed_compact_scorer_tokens_per_second_per_a100": [50000, 200000],
                           "teacher_label_passages": 20000, "teacher_prompt_tokens_each": 2048,
                           "teacher_output_tokens_each": 256,
                           "assumed_teacher_prefill_tokens_per_second": [500, 2000],
                           "assumed_teacher_decode_tokens_per_second": [20, 80],
                           "teacher_gpu_hours": teacher_gpu_hours,
                           "application_gpu_hours": application_gpu_hours,
                           "student_training_gpu_hours": [4, 12],
                           "calculated_a100_gpu_hours": scoring_total,
                           "planning_a100_gpu_hours": [150, 600],
                           "human_review_person_hours": [32, 64],
                           "human_review_design": "400 passages, two independent reviewers, 2-4 minutes each plus adjudication.",
                           "note": "Score candidate paper/web text before research rejection. Validate sequence/chemical records with representation-specific checks. Compact-scorer and teacher throughput are assumptions."},
    "mixture_experiments": {"proxy_runs": 30, "proxy_groups": 6, "proxy_parameters": 30000000,
                            "proxy_training_tokens_each": 3000000000,
                            "assumed_proxy_effective_a100_tflops": [20, 75],
                            "target_runs": 3, "target_design": "One baseline and two shortlisted recipes, one seed each.",
                            "target_parameters": 7000000000, "target_training_tokens_each": 1000000000,
                            "assumed_target_effective_a100_tflops": [50, 125],
                            "overhead_fraction": .25, "calculated_a100_gpu_hours": mix_gpu_hours,
                            "planning_a100_gpu_hours": [400, 1200],
                            "proposed_gpus": [4, 8], "planning_days_at_proposed_allocation": [2, 13],
                            "note": "An illustrative 7B CPT campaign, not a requirement to train 49B tokens or run three seeds. A 27B target costs about 27/7 times as much for target runs, excluding proxy costs.",
                            "references": ["https://arxiv.org/html/2512.13961v2#S3.SS4", "https://arxiv.org/html/2406.11794v3"]},
    "boundaries": ["Runtimes exclude implementation work, scheduler wait, major outages and full-paper OCR.",
                   "These larger allocations are scenarios only; current paper-project limits remain two CPU threads and at most one GPU, with no training authorized.",
                   "With one A100, scoring alone is roughly 6-25 days. Full-parameter 7B confirmation needs sharding across GPUs.",
                   "Several stages can overlap, but no end-to-end completion date is guaranteed."]
}
report = {
    "date_pst": "2026-10-16", "status": "planning_scenarios_not_measured_corpus_yield",
    "scope": "Selected 55-journal PMC XML candidates; FineFineWeb biology; TheBioCollection free-text stream only.",
    "scope_exclusions": ["TheBioCollection instruction stream", "general replay", "new generated training data", "additional raw UniRef/PubChem/RNAcentral copies", "unmeasured incremental peS2o/S2ORC/Dolma additions", "whole-PMC expansion beyond selected journals"],
    "counting": "One retained exposure in the pinned local Qwen-family extraction tokenizer; no repeated training passes. External counts converted using convenience-probe ratios.",
    "published_input_counts": {"selected_pmc_xml_candidates": pmc, "finefineweb_biology_source_tokens": 86.99e9,
                               "biocollection_free_text_gravity_tokens": 33.8e9},
    "sources": {"pmc_inventory": "../pmc_cns_availability_2026-10-13/availability.json",
                "finefineweb": "https://huggingface.co/datasets/m-a-p/FineFineWeb",
                "biocollection": "https://huggingface.co/datasets/trillionlabs/TheBioCollection",
                "biocollection_paper": "https://arxiv.org/html/2607.08803v1"},
    "scenarios": scenarios,
    "central_modality_tokens_conditional_on_prefix_representativeness": modality,
    "storage": storage,
    "resource_plan": resource_plan,
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
for key, value in scenarios.items():
    print(key, "dedup-only B", round(value["dedup_only_total_tokens"] / 1e9, 2),
          "research B", round(value["research_starter_total_tokens"] / 1e9, 2),
          {k: round(v / 1e9, 3) for k, v in value["research_starter_content_tokens"].items()})
print("central modality B", {k: round(v / 1e9, 3) for k, v in modality.items()})
print("storage GiB", {k: round(v / 2**30, 1) for k, v in storage.items() if isinstance(v, (float, int)) and "bytes" in k})
