# General data preparation

Updated **October 24, 2026**. The goal is a clean, deduplicated, quality-checked collection with traceable sources and usable training files. Counts are snapshots and continue to grow while workers run. This report covers the general collection; the protein question-answer dataset is documented separately.

## Source content and progress

| Source content | Total available in this source | Collected so far | Prepared so far | Current work |
|---|---:|---:|---|---|
| PMC research papers | **9,273,077 papers** in the frozen source inventory | **952,438 papers** across the existing collection and new downloads | **348,123 paper texts; 14.44 GB; 3.791 billion tokens.** One primary text per paper, including all available text without the old keyword filter. This total is partial. | Downloads and extraction continue with eight parser processes; **602,560 downloaded papers** await conversion. Retraction, eligibility and final duplicate checks remain |
| TheBioCollection: biological prose, protein/DNA/RNA sequences and molecular representations | **37,227,086 records** in the selected free-text stream | All 32 source files downloaded and verified | Raw content fully counted: **92.61 GB; 36.978 billion tokens** | Cleaning and exact duplicate checks are running. These are raw totals; the final retained amount is not yet measured |
| FineWeb-Edu: educational web pages | **190,168,005 source rows** | Source files available; 34 replacement files verified | **2,138,160 pages provisionally retained; 7.377 GB; 1.677 billion tokens** | Main filtering reached **36,230,654 rows; 153,937,351 remain**. Five filtering GPUs and one separate source-error-repair GPU are running. Retained pages are not yet an approved biological corpus |

## Quality evidence

| Review | Result | What it establishes |
|---|---|---|
| Blinded assistant review of 400 web documents: 200 retained and 200 rejected or noncandidate | **159/200 retained documents (79.5%)** met the strict biology, usefulness and readability criteria. Document precision Wilson 95% range: **73.4–84.5%**. Token-weighted precision: **85.9%** | A diagnostic for the sampled, closed portion of the collection. Assistant reviews are not expert human ground truth; this does not validate the whole corpus or authorize production release |
| Earlier standalone BERT filter gate | **Failed:** no precision-qualified rule | Completed classifier inference does not establish a validated filter |
| Separate earlier BERT + clinical-filter pilot | **55/60 documents (91.7%)**; document Wilson 95% range **81.9–96.4%**; token precision **94.3%** | A small offline pilot, separate from the standalone BERT gate and the broader review above. It is not production release or completed full-corpus filtering |

## Preparation stages

Different sources advance through these stages in parallel. Remove exact duplicates before additional expensive scoring, then verify near-copies before final selection. Existing filtered batches also receive duplicate checks.

| Stage | What it does | Progress |
|---|---|---|
| **1. Collect** | Download and verify original source material | Paper downloads continue; selected reference and web files are available |
| **2. Extract** | Preserve usable text, sequences, tables and source links | Paper conversion continues; reference-collection counting is complete |
| **3. Remove duplicates** | Identify exact repeats, then verify near-identical copies | Reference-collection exact deduplication and an earlier near-copy pass are running. Combined-source checks remain unfinished; candidate matches are not removals |
| **4. Score and filter** | Select relevant, useful material and audit the decisions | Web inference continues. The broader quality review identified material needing better selection; final approval is pending |
| **5. Validate and package** | Check exclusions, source provenance, document boundaries and final exports | Not yet complete; no final combined training release |

**The final combined training collection is still being prepared.** GB uses decimal units. All token amounts above come from measured tokenizer counts; raw counts, source bindings and processing records are retained in the local artifacts. The corpus-preparation work does not start model training.
