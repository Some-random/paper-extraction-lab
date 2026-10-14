# Paper extraction lab

The initial pilot tests how to turn scientific papers into evidence linked to
their source: figures/tables, captions, referring paragraphs, table structure,
page images, and a few exact-source QA examples. All work lives here under
`/data/rustfs1/dongweij`. Downloads and experiments run sequentially, without
subagents or new SSH connections. This pilot used CPU only.

Open [the sample viewer](reports/sample_viewer.html) to inspect source pages,
table structures, referring text, provenance, and questions/answers. Open
[the experiment report](reports/pilot_report.html) for measured results.

## What was tested

Three open papers: [Ryze v1](https://arxiv.org/pdf/2606.00902v1),
[LLaVA-Med v1](https://arxiv.org/pdf/2306.00890v1), and the
[Affibody domain-permutation paper](https://doi.org/10.3390/pharmaceutics13111974).
Together they contain 44 PDF pages. The Affibody paper also provides native
JATS XML through the [Europe PMC API](https://europepmc.org/RestfulWebService).
Two source pages were converted to image-only PDFs at 144 dpi as controlled
OCR stress cases. These are derived copies, not additional independent papers.

Actual methods executed:

- PyMuPDF native text and original/position-sorted reading order.
- pdfplumber line- and text-based table detection.
- Native JATS extraction, including `floats-group`, explicit cross-references,
  HTML table spans, units, uncertainty, and footnotes.
- Docling layout/table extraction with OCR disabled for born-digital PDFs.
- Docling plus RapidOCR on the two image-only cases.
- A hybrid binder using source captions, spatial checks, XML when present,
  and explicit full-page image fallback for ambiguous/multi-panel figures.
- Exact-source QA generation and replay checks; no model was trained.

## Main observations

| Exploratory diagnostic | Result |
| --- | --- |
| Ryze Table 2: pdfplumber line/text strategies | 0/12 checked cells in correct row/column positions |
| Same table: Docling, digital PDF | 12/12 |
| Same table: OCR of image-only page | 12/12 matrix values; caption attached to wrong neighboring table |
| OCR plus geometry-based binding | 12/12 values with corrected caption link, repair flagged for review |
| Affibody digital PDF: all five tables vs XML | 42/60 exact labelled-cell matches; tables 3/4/5 failed binding or structure |
| Targeted OCR of Affibody page 11, tables 3/4 | 12/12 checked values, compared with 0/12 in the digital-text run |
| Native Affibody XML | 6 figures, 5 tables, all 11 with explicit referring text; no unresolved visual references |
| Exported evidence-enriched QA samples | 36/36 answers replay exactly from their evidence |

These checks are deliberately tiny and exploratory. The Affibody XML is a
source-derived reference for the matching PDF, not an independently annotated
benchmark. The OCR repair page was selected after observing failure. Table
tests use optimistic best-candidate selection for pdfplumber and separately
report caption-linked extraction for Docling. A replayed answer proves that
the export matches its cited extraction; it does not validate scientific
conclusions or model reasoning.

The hybrid output contains 34 evidence bundles across the three original
papers, plus one bundle for the Ryze OCR stress page. Full source pages are
explicitly marked as full pages. Region crops remain optional because the
layout model split some multi-panel figures and detected publisher logos.
An Affibody chart was classified as a table; XML retains its actual role.
The raw model outputs and all structural flags are preserved.

Twenty-seven structured binding measurements were extracted from the two
Affibody binding tables: 23 numerical values with uncertainty and 4 explicitly
not-determined values. No binder/nonbinder labels were inferred. A measured
value, a missing measurement, an author interpretation, and an inferred
conclusion must remain separate fields.

The OCR fallback is useful but imperfect. On the Ryze scan it read one other
table cell's `38.4` as `384`. On the Affibody scan it read one header footnote
superscript `a` as `ª`. Successful checks on selected cells do not imply every
cell, header, or footnote is correct. Raw evidence and review flags matter.

## Recommended direction

Use native XML/HTML when available. For PDF-only papers, keep native text and
source geometry, use layout/table extraction, and route only failed or
ambiguous pages/regions to OCR or a document VLM. Build an evidence graph
before generating claims or QA: every value keeps its original string, unit,
row/column, source hash, page or XML path, caption, footnotes and referring
paragraph IDs. Missing/contradictory evidence should produce an abstention or
review item, not an invented correction.

[Ryze](https://arxiv.org/pdf/2606.00902v1) motivates the evidence bundling and
selective chart/table extraction. [OLMo 3 §3.4.2](https://arxiv.org/html/2512.13961v2#S3.SS4.SSS2)
uses the first olmOCR version for science PDFs and describes fallback,
deduplication, and filtering. Its table/numeric-heavy document exclusions serve
general pretraining; blindly copying those policies would remove useful data
for this extraction task. [olmOCR 2](https://arxiv.org/abs/2510.19817) motivates
checks of specific text, reading order, and table structure rather than judging
Markdown by appearance alone.

[LLaVA-Med §3](https://arxiv.org/pdf/2306.00890v1) already includes referring
sentences in part of its instruction data. Ryze's introduction describes older
figure-caption methods as discarding referring prose, so that contrast should
not be treated as universal. The newer paper's benchmark and cost claims were
not reproduced in this extraction pilot.

[olmOCR](https://github.com/allenai/olmocr),
[GLM-OCR](https://github.com/zai-org/GLM-OCR), and
[GROBID](https://github.com/grobidOrg/grobid) were reviewed but not run. The next
useful comparison is one local document VLM on the flagged pages using the same
source-based checks, followed by a small teacher-generated QA experiment and
an independent answer/evidence verifier. These are next experiments, not
completed results.

## Artifacts

- `inputs/manifest.json`: original source URLs, exact versions, hashes and sizes.
- `inputs/*.provenance.json`: image-only stress-case derivations.
- `outputs/native/`, `outputs/jats/`, `outputs/docling/`: unchanged raw extraction.
- `outputs/hybrid_evidence.jsonl`: preferred evidence bundles with page images.
- `outputs/binding_measurements.jsonl`: typed binding-value examples.
- `outputs/hybrid_qa_samples.jsonl`: questions, answers and exact evidence IDs.
- `outputs/evidence_enriched_sft_samples.jsonl`: message-format examples and images.
- `outputs/audit.json`, `outputs/targeted_ocr_audit.json`: checks and failures.
- `outputs/layout_binding_flags.json`: detected caption/region conflicts.
- `outputs/context_ablation.json`: caption-only versus added-context sizes.
- `reports/sample_viewer.html`, `reports/pilot_report.html`: inspectable results.

The SFT-format file is a pipeline demonstration built by deterministic table
and caption lookup. It contains no teacher-generated reasoning and is not an
approved training release. Image paths are relative to this project root.

## Reproduce

The existing `.venv` is ready. It reuses installed PyTorch and its dependencies
read-only from the existing Affibody environment via a `.pth` file. That
environment was not changed. New packages and caches are in this project;
exact package versions and model revisions are recorded in `sources/`.

```bash
cd /data/rustfs1/dongweij/paper-extraction-lab
bash scripts/run_pilot.sh
```

The runner submits one document at a time, uses two CPU math threads and one
Torch inter-op thread, and hides all GPUs. Model downloads use one download
worker. Rerunning replaces derived outputs in this experiment directory and
reuses existing original inputs and model caches.
