# Biology paper extraction lab

The project converts **experimental biology papers** into source-linked text,
tables, figures, and training-data candidates. Foundation-model reports inform
the data-curation recipes; PDF extractor comparisons remain a separate branch.

Everything is stored in `/data/rustfs1/dongweij/paper-extraction-lab`.
Experiments run sequentially with one document/inference worker, at most one
GPU, no subagents, and no new SSH connections.

## Updated native-source preview: three papers

Read the [current three-paper results directly on GitHub](reports/pmc_native_v4_citations_2026-10-15/README.md).
The first table links the full extracted research text, original figures with
captions and referring paragraphs, source tables, and complete structured JSON.
Each paper also includes every text chunk and figure/table–context record;
Q&A examples appear as optional derivatives below the extracted outputs.
It includes 140 research paragraphs, 25 original figure images, four source
tables, 35 text chunks of at most 2,048 tokens, 23 figure/table–context records,
and nine source-checked reading/lookup examples. The tracked
[summary](reports/pmc_native_v4_citations_2026-10-15/summary.json) and
[examples](reports/pmc_native_v4_citations_2026-10-15/examples.json) include provenance.

Literature citations now use full cited titles and first author/et al. All 211
bibliography records retain source-supplied authors and identifiers; all 322
source citation-marker elements were checked, including 12 numeric ranges.
The original-marker views remain available. No citation-policy comparison is run.

The [supplementary-file inventory and full spreadsheet exports](reports/pmc_native_v4_citations_2026-10-15/supplements/README.md)
cover 41 linked files, including 33 XLSX files. Two source workbooks were fully
parsed: nine worksheets, 35,468 nonempty source rows and 184,530 populated cells.
Full TSV sheets preserve source row/column coordinates; preview excerpts are
labeled separately. Original workbooks add approximately 1.9 MB on RustFS.
Unparsed supplements have explicit status. The [previous v3 preview](reports/pmc_native_v3_preview_2026-10-15/README.md)
is retained.

The preview uses the same CC BY OTULIN/Wnt, population-proteomics, and Lsp2
papers already cached in the October 14 batch. It parses publisher XML, retains
paragraph/section boundaries and scientific notation, separates figures/tables
nested inside publisher paragraphs, preserves merged cells, and connects
context only through explicit figure/table references. Merged table values are
not repeated as independent counts in the text representation. Bibliographies
and administrative sections are routed outside the training-text stream;
their sources and exclusion reasons remain available.

Original figure files are matched by XML filename and checked against the
official media-manifest checksum. The GitHub documents include all 25 figure
images and link to the unchanged earlier olmOCR text. The source PDFs/XML remain
on RustFS. This run uses one CPU worker and no GPU, teacher API, new OCR
inference, or training. Quality checks are structural/provenance diagnostics,
not an independent scientific or OCR-accuracy benchmark. No learned educational
classifier or biological entity linker has been run.

```bash
OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 \
  TOKENIZERS_PARALLELISM=false .venv/bin/python src/run_native_preview.py
.venv/bin/python scripts/export_github_preview.py
.venv/bin/python scripts/extract_supplement_sample.py
.venv/bin/python -m unittest discover -s tests -v
```

Configuration is in [config/pmc_native_v4_citations.json](config/pmc_native_v4_citations.json).
The text-packing demonstration uses the cached Qwen-family tokenizer on CPU;
re-tokenize for the eventual training backbone. Multimodal records have explicit
source-linked segments but have not been vision-tokenized for a particular VLM.

The [biological continued-pretraining review](reports/bio_foundation_review_2026-10-15/README.md)
compares 11 CPT models and studies, with five from-scratch comparisons.
It reports token amounts from online papers, web URLs and existing datasets,
names the starting checkpoints, and explains each count. Linked study pages
retain extraction, filtering, figures, citations and source evidence.
[Maintenance instructions](reports/bio_foundation_review_2026-10-15/maintenance.md)
describe the underlying registry and generated files.

Biological model evaluation has its own private repository:
[bio-evaluation](https://github.com/Some-random/bio-evaluation).
Benchmark protocols, cases, model runs and scores belong there. This repository
holds paper extraction, data preparation and literature review; its extraction
diagnostics are not biological model evaluations.

The [web acquisition guide](reports/bio_foundation_review_2026-10-15/web_acquisition.md),
[executed web probe](reports/bio_foundation_review_2026-10-15/web_sample.md) and
[figure representation guide](reports/bio_foundation_review_2026-10-15/figure_handling.md)
remain topic guides linked from that catalog.

The user-confirmed [500-paper native-source expansion](reports/pmc_native_500_2026-10-15/README.md)
retains original figures, full captions, referring paragraphs and source tables,
with no new OCR or model training. The [storage/time estimate and firm limits](reports/pmc_native_500_2026-10-15/scaling_estimate.md)
precede the run. Acquisition is paused at the user's request while literature
is consolidated; the batch's STOP file remains in place.

## Overnight download and full-paper extraction

The October 14 batch finished at **04:14 PST**: **50 papers downloaded and parsed
from XML, 37 complete OCR papers, one partial OCR paper and 12 papers deferred
at the 1,000-page limit**. Of the retained OCR pages, 999 completed and one
reached the per-page time limit. The batch used about 341 MiB of artifacts and
303 MiB of downloaded response bodies. See the tracked
[result summary](reports/pmc_cns_biology_2026-10-14/summary.json) and
[paper manifest](reports/pmc_cns_biology_2026-10-14/papers.csv).

The batch used [these resource limits](config/pmc_overnight_2026-10-14.json).
Its [detailed report](experiments/pmc_cns_biology_2026-10-14/report.html) and
[state](experiments/pmc_cns_biology_2026-10-14/state.json) are retained on RustFS.
It targeted 50 biology papers across ten CNS and related journals, with one
serial worker, GPU 0 only, at most 1,000 OCR pages, 2 GiB of new batch artifacts,
1 GiB of downloaded response bodies and six hours of cumulative runtime.
Cached olmOCR 2 weights were reused offline, with no paid model API calls.
All human-facing times use fixed PST (UTC-8). No extraction worker remains
running for this completed batch.

### Review the extracted results

Three small, byte-identical text examples are tracked here for browser review.
The source authors, article links, licenses and text hashes are retained in each
sample's `provenance.json`.

| Paper | olmOCR output | Native XML text |
| --- | --- | --- |
| Nature: Lsp2, early-life diet and adult lifespan in Drosophila | [OCR](reports/pmc_cns_biology_2026-10-14/samples/PMC13645648/fullpaper_olmocr.md) | [Native text](reports/pmc_cns_biology_2026-10-14/samples/PMC13645648/fullpaper_native.md) |
| Nature Communications: population proteomic profiles | [OCR](reports/pmc_cns_biology_2026-10-14/samples/PMC13655163/fullpaper_olmocr.md) | [Native text](reports/pmc_cns_biology_2026-10-14/samples/PMC13655163/fullpaper_native.md) |
| Science Advances: OTULIN, Wnt and skin inflammation | [OCR](reports/pmc_cns_biology_2026-10-14/samples/PMC13651886/fullpaper_olmocr.md) | [Native text](reports/pmc_cns_biology_2026-10-14/samples/PMC13651886/fullpaper_native.md) |

For all 50 papers, run `.venv/bin/python scripts/render_pmc_review.py` on the
machine holding the experiment artifacts. It creates a standalone
`experiments/pmc_cns_biology_2026-10-14/review.html` with searchable papers,
OCR/native text, source tables, captions, referring paragraphs, original table
diagnostics and lookup QA. Open it directly in a browser; no server is needed.
`paper_review.zip` in that directory packages the reader and compact manifests.
Original PDFs are linked through the official PMC cloud distribution.

The [table-check audit](reports/pmc_cns_biology_2026-10-14/table_diagnostic_audit.json)
found that the original caption matcher linked 4 of 18 checked source tables.
Of 1,211 source cells, 1,072 had no linked generated table; 91 of the remaining
139 passed strict value/header checks. Captions using `Table 1 | ...` and
unnumbered resource tables are unsupported by that matcher. These counts explain
the existing diagnostic; they do not change original scores or model outputs.

The [500-paper estimate](reports/pmc_cns_biology_2026-10-14/scaling_estimate.json)
extrapolates about 15,820 pages and 53 hours of full-page OCR on the same GPU,
plus downloading and XML parsing. Batch artifacts would occupy a few GiB with
temporary page images removed. This estimate does not start a new batch.

Each accepted paper retains its original PDF/XML, version/license metadata,
hashes, full native section text, tables, captions and explicitly referring
paragraphs. Whole-paper olmOCR 2 runs shortest-first within the page/time budget.
Raw per-page outputs and combined text are kept, while temporary page images
are regenerated from the source PDF and removed after inference. The report
distinguishes complete, partial and deferred OCR from XML parsing. This is a
selected starter corpus, not a representative benchmark. Figure interpretation
is unverified; generated lookup QA remains diagnostic, with no training run.

Outputs are in `experiments/pmc_cns_biology_2026-10-14/`. Each paper has
`fullpaper_native.md`, `native_document.json` and `source_evidence.jsonl`.
OCR papers also have `fullpaper_olmocr.md`, `olmocr_document.json`, raw page
outputs, `table_checks.json` and `lookup_qa_diagnostics.jsonl`. The final
`exports/` directory holds path manifests, avoiding redundant corpus copies.
Its `summary.json` records completed/partial/deferred counts, inference time,
GPU memory, resource usage and table diagnostics for completed OCR papers.
The exploratory caption/row/column adapter matched 91 of 1,211 checked source
cells, with the same 91 passing header checks. Missing caption bindings, split
tables and unsupported markup affect this diagnostic; it is not a general OCR
accuracy score or scientific validation. Original outputs remain unchanged.
Secure downloads use the existing CPU environment through `src/pmc_http_fetch.py`;
model inference uses the existing GPU environment. Workers can run detached from
the chat session and checkpoint after every accepted paper and inferred page.

To stop gracefully, create `experiments/pmc_cns_biology_2026-10-14/STOP`.
Before resuming, confirm no worker is running and remove that stop file only
if a resume is intended. The worker lock also rejects duplicate starts.

```bash
CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 \
  HF_HUB_OFFLINE=1 .ocr-venv/bin/python -u src/run_pmc_batch.py \
  --config config/pmc_overnight_2026-10-14.json
```

Open [the current comparison](experiments/bio_tool_comparison_v1/reports/results.html)
to inspect source pages and cell-by-cell tool output. Detailed results, frozen
inputs, references, exact model revisions, logs and source-native evidence live
in `experiments/bio_tool_comparison_v1/`.

**Selected PDF extractor: olmOCR 2** (`allenai/olmOCR-2-7B-1025`). The default
is pinned in [config/extraction.json](config/extraction.json). The existing
comparison already ran this checkpoint on all nine pages. It uses Transformers
and the official v4 no-anchoring page prompt; this is not an execution of the
full official pipeline with its retry, rotation and document-level heuristics.
Preserve source pages, raw output, captions and referring text. Check scientific
identifiers, quantities, units and table structure before producing grounded QA.

## Completed comparison

All five methods have finished all nine diagnostic pages. No inference or
model-download process remains running for that comparison. The separate
overnight batch above reused its cached olmOCR 2 model and is also complete.

| Executed method | Caption-linked cells / 243 | Value + header checks / 243 | Correct power-bearing headers / 12 | Page seconds |
| --- | ---: | ---: | ---: | ---: |
| docling | 189 | 165 | 0 | 48.4 |
| docling_rapidocr | 162 | 106 | 0 | 114.9 |
| olmocr | 201 | 183 | 0 | 150.4 |
| mineru | 200 | 200 | 12 | 218.9 |
| glmocr_docling | 159 | 159 | 12 | 188.2 |

For this small stress set, MinerU preserves scientific table structure and
headers most consistently; olmOCR has one additional strict value match.
MinerU's 43 CD69 failures preserve the values but alter identifier punctuation;
the source/model pairs are recorded in the identifier error audit, without
repairing outputs or changing its strict score. The GLM result is a custom
Docling-region hybrid, not its official SDK. Current public leaders beyond
these tested tools are listed separately in the report.

Use publisher XML/JATS first when available. For PDF-only extraction, preserve
source pixels, use layout/table recognition, bind captions and referring text,
and check identifiers, row groups, units, powers and uncertainty before using
the evidence in QA. Figure annotations in this run were not validated as chart
values or biological image interpretations.

## Meaning of the two cell scores

These are local source-reference checks, not official olmOCR-bench metrics.
The denominator is 243 logical body cells from 12 tables in publisher JATS XML.
Merged or multiline measurements can form one logical cell; headers are not
part of this denominator. XML is used by the evaluator, never by OCR inference.

**Reference-matched labelled cells** require the extracted table to bind to the
correct caption label, the row/group identifier to match, the column count to
match, and the value to match at the same column position. Normalization permits
equivalent whitespace, Unicode and TeX formatting, but not number rounding,
changed uncertainty, signs or identifier punctuation. Caption binding uses
extractor output, not the expected values. The separate best-matrix oracle
score is not this score.

**Also passed quantity/unit header checks** counts the subset of those cells
whose column header preserves the quantity, units and numeric powers after
format normalization. Plain category headers can be discarded; quantity/unit
parent headers are retained. This is a conservative text/notation check, not a
semantic verifier, so equivalent wording may fail.

olmOCR 2 scored **201/243 (82.7%)** and **183/243 (75.3%)**, respectively.
For example, source `−23 ± 1` and extracted `-23 \pm 1` match, but the source
header `Thermodynamic / ΔG° (kJ mol⁻¹)` became only `Thermodynamic`, failing
the second check. The 18-cell difference comes from the first two plasma-protein
tables. See [metric definitions and the recorded example](experiments/bio_tool_comparison_v1/reports/metric_definitions.json)
and [the evaluator](src/bio_table_metrics.py). Raw outputs and scores are retained.

## Current experiment

Three papers cover HER2 Affibody drug conjugates, CD69-binding Affibodies, and
oligopeptide interactions with plasma proteins. Nine fixed pages contain 12
tables and six figures. Publisher JATS XML provides a source-derived silver
reference, with 243 logical body-value cells. This is an exploratory diagnostic,
not an independently annotated or representative benchmark.

The comparison runs Docling on digital PDFs, Docling plus RapidOCR on text-free
rendered copies, olmOCR-2-7B-1025, MinerU2.5-Pro-2605, and a GLM-OCR hybrid using
Docling region proposals. Runtime progress is in the experiment logs; only
completed outputs contribute to the report. Exact values, row/group labels,
caption binding, merged/multiline cells, headers, powers, signs, missing values,
time and peak GPU allocation are retained. Neither reference XML nor expected
answers enter model inference.

The separate native-source evidence branch contains 34 bundles across the full
three-paper corpus: visual pages, captions, structured source tables, notes,
explicitly referring paragraphs, source hashes and XML provenance. Its 29 QA
examples are deterministic table lookups verified against source cells; they
are not teacher-generated reasoning or an approved training dataset.

## Commands

```bash
cd /data/rustfs1/dongweij/paper-extraction-lab
CUDA_VISIBLE_DEVICES=0 .ocr-venv/bin/python src/run_bio_tool.py
CUDA_VISIBLE_DEVICES='' .venv/bin/python src/run_bio_tool.py --tool docling
CUDA_VISIBLE_DEVICES='' .venv/bin/python src/run_bio_tool.py --tool docling_rapidocr
CUDA_VISIBLE_DEVICES=0 .ocr-venv/bin/python src/run_bio_tool.py --tool olmocr
CUDA_VISIBLE_DEVICES=0 .ocr-venv/bin/python src/run_bio_tool.py --tool mineru
CUDA_VISIBLE_DEVICES=0 .glm-venv/bin/python src/run_glm_regions.py
.venv/bin/python src/evaluate_bio_tools.py --tools docling docling_rapidocr olmocr mineru glmocr_docling
.venv/bin/python src/render_bio_comparison.py
```

Model records must exist before their inference commands. Inputs and raw outputs
are preserved; a completed case is skipped on rerun. Per-page timing excludes
model downloads and records initialization separately. GLM's custom region
hybrid is distinguished from its official PP-DocLayoutV3 SDK. GPU runtimes
reuse the existing Torch installation read-only; local package additions and
all model caches remain inside this project.

## PMC corpus availability

The user confirmed including related journals alongside Cell, Nature and
Science. The October 13, 2026 [availability report](reports/pmc_cns_availability_2026-10-13/index.html)
counts an explicit set of 55 journal titles, including a historical predecessor;
it is not an exhaustive publisher catalogue or a biology-only corpus.
The combined query returns 552,532 public PMC records, 552,024 XML/text-mining
candidates and 490,354 open-access records marked as having PDFs. Excluding
Scientific Reports yields 187,791 PDF candidates. Counts are availability
inventory, not successful full-corpus downloads or completed extractions.

Six actual PDF/XML pairs from Cell, Nature, Science, Nature Communications,
Cell Reports and Science Advances were downloaded through the official PMC S3
dataset. Their hashes match, and their version/license provenance is retained.
No OCR inference was run on these new availability probes. The corpus-size
report includes explicit throughput and storage assumptions; the current
filesystem cannot hold the entire pool under ordinary PDF-size assumptions.

```bash
.venv/bin/python src/inventory_pmc_cns.py
.venv/bin/python src/probe_pmc_downloads.py
.venv/bin/python src/render_pmc_inventory.py
```

## Earlier pilot

The earlier mixed-domain CPU pilot remains available as
[an archived description](reports/legacy_mixed_pilot_readme.md), with its original
inputs, outputs and reports preserved. Its Ryze/LLaVA-Med extraction results do
not constitute the current biological-paper tool comparison.
