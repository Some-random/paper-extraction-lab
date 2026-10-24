# General data preparation

Updated **October 24, 2026**. We are building a clean, deduplicated, quality-checked collection with traceable sources and usable training files. Collection and processing continue in parallel. This report covers the general collection; the protein question-answer dataset is documented separately.

## Source content and progress

**Percentages show coverage of the named stage, not completion of a validated training corpus.** Progress bars are rounded; percentages use the recorded counts. The current snapshot is **October 24 at 12:46 PST (UTC-8)**. Recent changes compare two saved observations about 89 minutes apart.

| Source content | Collection | Processing progress and measured content | Remaining work and recent change |
|---|---|---|---|
| **PMC research papers** | **1,056,264 collected / 9,273,077 inventory records — 11.39%**<br>`██░░░░░░░░░░░░░░░░░░`<br>**8,216,813 inventory records not yet collected.** Full-text accessibility varies; the inventory is not a promise that every entry has downloadable XML. | **387,060 primary paper texts; 16.254 GB; 4.256 billion tokens.** This is the main paper-text total and remains partial. One primary text per paper, including all available text without the old keyword filter.<br>Primary texts cover **4.17% of the inventory**: `█░░░░░░░░░░░░░░░░░░░` | **667,578 downloaded papers await conversion.** There are **8,886,017 inventory records without a processed primary text**; this includes material not yet collected or whose accessibility is unresolved. Downloading and conversion continue. Retraction, eligibility and final duplicate checks remain incomplete; original sources are preserved.<br>Recent change: **+21,646 collected; +6,991 paper texts.** |
| **TheBioCollection: biological prose, protein/DNA/RNA sequences and molecular representations** | **All 32 selected source files downloaded and verified; 37,227,086 records.** Raw content counted: **92.61 GB; 36.978 billion tokens.** | **Exact duplicate pass: 18,405,576 / 37,227,086 records — 49.44%**<br>`██████████░░░░░░░░░░`<br>All files have completed hashing; record-level duplicate checks continue. | **18,821,510 records remain unchecked.** Final retained text and token totals are not yet measured. Sequence variants are preserved.<br>Recent change: **+1,191,869 records checked.** |
| **FineWeb-Edu: educational web pages** | **190,168,005 source rows**; source files available and 34 replacement files verified. | **First source pass: 43,019,435 / 190,168,005 rows — 22.62%**<br>`█████░░░░░░░░░░░░░░░`<br>**2,528,466 pages provisionally retained; 8.773 GB; 1.996 billion tokens.** | **147,148,570 rows remain untraversed.** Traversed rows include **1,899,000 source-read unknowns** held for separate repair. Filtering work continues. Retained pages are provisional web text, not a confirmed biological corpus; the quality gate remains failed.<br>Recent change: **+689,683 rows traversed.** |

## Quality evidence

| Review | Result | What it establishes |
|---|---|---|
| Content-quality development test on 64 previously reviewed documents | Retained **27/32 prior positive controls**, but also **12/32 known problem cases**. Five judgments were held because their evidence did not validate | A useful diagnostic, not an independent quality audit. This method is not qualified for scaling; held judgments are unresolved, not negative labels |
| Fresh blinded assistant audit of a stricter selection rule: 400 retained candidates and 150 vetoed documents | **Failed both 90% precision targets:** **333/400 (83.25%)** met the strict biology, usefulness and readability criteria. Document precision Wilson 95% range: **79.3–86.6%**. Token-weighted precision: **86.63%** | The rule was frozen before the 550 new judgments. Tightening classifier confidence did not establish sufficient quality. The pool remains provisional; these reviews are assistant judgments, not expert human ground truth |
| Earlier blinded assistant review of 400 web documents: 200 retained and 200 rejected or noncandidate | **159/200 retained documents (79.5%)** met the strict criteria. Document precision Wilson 95% range: **73.4–84.5%**. Token-weighted precision: **85.9%** | Development evidence for the later rule, not an independent validation of it. Neither review establishes whole-corpus quality or production release |
| Earlier standalone BERT filter gate | **Failed: no precision-qualified rule** | Completed classifier inference does not establish a validated filter. The standalone gate remains failed |
| Separate earlier BERT + clinical-filter pilot | **55/60 documents (91.7%)**; document Wilson 95% range **81.9–96.4%**; token precision **94.3%** | A small offline combination, separate from the standalone BERT gate and broader reviews above. This pilot does not replace that gate, establish production release or complete full-corpus filtering |

All review judgments in this table, including the separate 60-document offline pilot, are assistant judgments, not expert human ground truth. Wilson 95% ranges apply only to document precision. **No filter has been approved for production release by these results.**

## Preparation stages

Different sources advance through these stages in parallel. Remove exact duplicates before additional expensive scoring, then verify near-copies before final selection. Existing filtered batches also receive duplicate checks.

| Stage | What it does | Current position |
|---|---|---|
| **1. Collect** | Download and verify original source material | In progress; selected source files are available and additional acquisition continues |
| **2. Extract** | Preserve usable text, sequences, tables and source links | In progress; text conversion continues and raw reference counting is complete |
| **3. Remove duplicates** | Identify exact repeats, then verify near-identical copies | Exact checks, combined-source hashing and near-copy work remain unfinished. Candidate matches are not removals |
| **4. Score and filter** | Select relevant, useful material and audit the decisions | Inference and selection development continue. The fresh audit failed the stricter rule; final quality approval is pending |
| **5. Validate and package** | Check exclusions, source provenance, document boundaries and final exports | Benchmark and development-set exclusions and export validation remain unfinished; no final combined training release |

**The final combined training collection is still being prepared. No final combined exports or training release are available.** GB uses decimal units. All token amounts above come from measured tokenizer counts; raw counts, source bindings and processing records remain in local artifacts. The corpus-preparation work does not start model training.
