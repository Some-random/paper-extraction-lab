# Three biology papers: updated extraction results

The actual extracted content is linked directly below: full research text, original figure images with extracted captions and referring paragraphs, source tables, and complete structured data. The Q&A examples are optional derivatives of these outputs.

Results generated **2026-10-14T22:20:45.074854-08:00** (fixed PST, UTC-8).

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
| [Science Advances: Canonical Wnt induction by OTULIN prevents keratinocyte death and skin inflammation](papers/PMC13651886/README.md) | 33 | 6 | 2 | 11 |
| [Nature Communications: Genome-wide analysis of 439 mass spectrometry-based proteomic profiles in a population of 15,035 Scottish individuals](papers/PMC13655163/README.md) | 42 | 5 | 2 | 8 |
| [Nature: Lsp2 links early-life diet to adult translation and lifespan in Drosophila](papers/PMC13645648/README.md) | 65 | 14 | 0 | 16 |

**Totals:** 140 research paragraphs, 25 original figure images, 4 full main-article tables, 35 text chunks, 211 bibliography records, and 322 source citation-marker elements checked.

## What changed

- Figures/tables nested in publisher paragraphs are separated from the prose.
- Inline literature citations become full cited titles plus first author/et al., including explicit numeric ranges.
- Complete bibliography metadata and original-marker article views remain available.
- Merged table cells, scientific notation, captions and notes are retained.
- Context comes from explicit article figure/table references.
- Bibliography and administrative material are routed outside the text-training stream.
- Text chunks retain source-fragment offsets and stay within the configured token limit.

## What was checked

All 25 images match their source media checksums. The pipeline checked 179 figure/table-reference edges against raw XML and retained XPath provenance for 218 physical source table cells. All nine examples have source excerpts and PDF text-literal corroboration. Citation source nodes, bibliography IDs and complete packed-block reconstruction were checked. The regression suite covers citation ranges, title/author expansion, source preservation, scientific notation, merged cells and unresolved metadata.

These are **source preservation and consistency checks**, not an independent OCR-accuracy benchmark. Figure interpretations and model-training benefit remain untested. This preview used one CPU worker and no new OCR inference, teacher API, or model training.

## Inspect the machine-readable results

- [Summary](summary.json)
- [Nine source-checked examples](examples.json)
- [Validation counts](validation.json)
- [Source-value and spreadsheet verification](verification.json)
- [Pipeline configuration](../../config/pmc_native_v4_citations.json)
- [Parser and record construction](../../src/native_training.py)
- [Source-content regression checks](../../tests/test_native_training.py)

## Related reading

[Supplementary-file inventory and larger biological tables](supplements/README.md).

[How biomedical foundation models construct their training data](../bio_foundation_review_2026-10-15/README.md).

Original PDFs/XML, model weights and bulk experiment files remain on RustFS. This GitHub export contains review text, original figure assets with attribution, and small reports.
