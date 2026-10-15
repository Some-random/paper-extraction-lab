# Three biology papers: updated extraction results

[Current v4 results: cited titles/authors and full supplementary spreadsheet exports](../pmc_native_v4_citations_2026-10-15/README.md). The v3 outputs below are preserved as the earlier snapshot.

The actual extracted content is linked directly below: full research text, original figure images with extracted captions and referring paragraphs, source tables, and complete structured data. The Q&A examples are optional derivatives of these outputs.

Results generated **2026-10-14T20:42:29.106737-08:00** (fixed PST, UTC-8).

## Read the extracted results

| Paper | Extracted research text | Figures + captions + context | Tables | Structured data |
| --- | --- | --- | --- | --- |
| Science Advances: Canonical Wnt induction by OTULIN prevents keratinocyte death and skin inflammation | [Read extracted text](papers/PMC13651886/article.md) | [Figures and context](papers/PMC13651886/figures.md) | [Tables](papers/PMC13651886/tables.md) | [Full structured extraction](papers/PMC13651886/extracted.json) |
| Nature Communications: Genome-wide analysis of 439 mass spectrometry-based proteomic profiles in a population of 15,035 Scottish individuals | [Read extracted text](papers/PMC13655163/article.md) | [Figures and context](papers/PMC13655163/figures.md) | [Tables](papers/PMC13655163/tables.md) | [Full structured extraction](papers/PMC13655163/extracted.json) |
| Nature: Lsp2 links early-life diet to adult translation and lifespan in Drosophila | [Read extracted text](papers/PMC13645648/article.md) | [Figures and context](papers/PMC13645648/figures.md) | No source tables | [Full structured extraction](papers/PMC13645648/extracted.json) |

The research-text view includes the abstract, main sections and methods; bibliography and administrative material are retained separately in the structured extraction. Each paper overview also links the earlier native output and the unchanged PDF-only olmOCR transcript.

## Output counts and paper overviews

| Paper | Research paragraphs | Figures | Tables | Text chunks |
| --- | ---: | ---: | ---: | ---: |
| [Science Advances: Canonical Wnt induction by OTULIN prevents keratinocyte death and skin inflammation](papers/PMC13651886/README.md) | 33 | 6 | 2 | 9 |
| [Nature Communications: Genome-wide analysis of 439 mass spectrometry-based proteomic profiles in a population of 15,035 Scottish individuals](papers/PMC13655163/README.md) | 42 | 5 | 2 | 7 |
| [Nature: Lsp2 links early-life diet to adult translation and lifespan in Drosophila](papers/PMC13645648/README.md) | 65 | 14 | 0 | 14 |

**Totals:** 140 research paragraphs, 25 original figure images, four source tables, 30 text chunks, 23 figure/table–context records, and nine source-checked examples.

## What changed

- Figures/tables nested in publisher paragraphs are separated from the prose.
- Merged table cells, scientific notation, captions and notes are retained.
- Context comes from explicit article figure/table references.
- Bibliography and administrative material are routed outside the text-training stream.
- Text chunks retain source-fragment offsets and stay within the configured token limit.

## What was checked

All 25 images match their source media checksums. The pipeline checked 179 figure/table-reference edges against raw XML and retained XPath provenance for 218 physical source table cells. All nine examples have source excerpts and PDF text-literal corroboration. Five scientific content/provenance regression tests passed.

These are **source preservation and consistency checks**, not an independent OCR-accuracy benchmark. Figure interpretations and model-training benefit remain untested. This preview used one CPU worker and no new OCR inference, teacher API, or model training.

## Inspect the machine-readable results

- [Summary](summary.json)
- [Nine source-checked examples](examples.json)
- [Validation counts](validation.json)
- [Pipeline configuration](../../config/pmc_native_v3_preview.json)
- [Parser and record construction](../../src/native_training.py)
- [Source-content regression checks](../../tests/test_native_training.py)

## Related reading

[How biomedical foundation models construct their training data](../bio_foundation_review_2026-10-15/README.md).

Original PDFs/XML, model weights and bulk experiment files remain on RustFS. This GitHub export contains review text, original figure assets with attribution, and small reports.
