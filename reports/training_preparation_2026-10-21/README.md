# General data preparation

Updated **October 24, 2026**. We are building a clean, deduplicated, quality-checked collection with traceable sources and usable training files. Collection and processing continue in parallel. This report covers the general collection; the protein question-answer dataset is documented separately.

## Source content and progress

**Percentages show coverage of the named stage, not completion of a validated training corpus.** Progress bars are rounded; percentages use the recorded counts. The snapshot is **October 24 at 20:32 PST (UTC-8)**. Recent changes compare with the **19:46 PST** snapshot. Individual worker observations were collected over about one second.

| Source content | Collection | Processing progress and measured content | Remaining work and recent change |
|---|---|---|---|
| **PMC research papers** | **1,179,718 paper IDs recorded as collected**, against an inventory of **9,273,077 entries**. Full-text accessibility varies; the inventory is not a promise that every entry has downloadable XML. | **434,464 primary paper texts; 18.280152 GB; 4.775289 billion tokens.** This is the main paper-text total and remains partial. One primary text per paper, including all available text without the old keyword filter. | **743,252 downloaded papers await conversion; collection and conversion continue.** Retraction, eligibility and final duplicate checks remain incomplete; original sources are preserved.<br>Recent change: **+12,976 recorded collected IDs; +5,261 paper texts.** |
| **TheBioCollection: biological text, protein/DNA/RNA sequences and molecular representations** | **All 32 selected source files downloaded and verified; 37,227,086 records.** | **Exact duplicate pass: 25,269,397 / 37,227,086 records — 67.879%**<br>`██████████████░░░░░░`<br>All files have completed hashing; record-level duplicate checks continue. The retained prefix contains **25,047,868 records; 62.470418 GB**. | **11,957,689 records remain unchecked.** Retained-prefix tokenizer counts are **not measured**; final retained totals and quality approval remain pending. Sequence variants are preserved.<br>Recent change: **+315,213 records checked.** |
| **FineWeb-Edu: educational web pages** | **190,168,005 source rows**; local source files are available. | **First source pass: 47,426,899 / 190,168,005 rows — 24.9395%**<br>`█████░░░░░░░░░░░░░░░`<br>**2,783,396 pages provisionally retained; 9.671876 GB; 2.201475 billion tokens.** | **142,741,106 rows remain untraversed.** Traversed rows include **1,899,000 source-read unknowns**. Filtering continues. Retained pages are provisional web text, not a confirmed biological corpus; the quality gate remains failed.<br>Recent change: **+448,732 rows traversed; +26,279 provisionally retained.** |
| **FineWeb-Edu repair pass — separate from the totals above** | Earlier source-read failures are being revisited across **13,721,000 rows**. | **2,444,000 rows checked; 164,703 pages provisionally retained; 0.541338 GB; 0.122113 billion tokens.** | **11,277,000 repair rows remain.** These replacement decisions are not merged into the canonical totals and add **no extra source-row coverage**. Their merge and quality checks remain pending.<br>Recent change: **+95,000 repair rows checked.** |

## Quality evidence

The following development and audit results are unchanged in this snapshot. More processed data does not by itself improve the evidence for filter quality.

| Review | Result | What it establishes |
|---|---|---|
| Complete-source classifier development check on 64 documents | **Completed: 22 core candidates, 13 outside the core, 29 held unknown.** The held outputs include 26 format failures, two explicit uncertainties and one output-limit case | An assistant content review of the 22 proposed core pages supported **10**, held **11** and classified **one** as catalog content. These known development cases do not estimate corpus precision; semantic quality remains unqualified. Original held outputs remain held |
| Fresh blinded assistant audit of a stricter selection rule: 400 retained candidates and 150 vetoed documents | **Failed both 90% precision targets:** **333/400 (83.25%)** met the strict biology, usefulness and readability criteria. Document precision Wilson 95% range: **79.3–86.6%**. Token-weighted precision: **86.63%** | The rule was frozen before the 550 new judgments. Tightening classifier confidence did not establish sufficient quality. The pool remains provisional; these reviews are assistant judgments, not expert human ground truth |
| Earlier blinded assistant review of 400 web documents: 200 retained and 200 rejected or noncandidate | **159/200 retained documents (79.5%)** met the strict criteria. Document precision Wilson 95% range: **73.4–84.5%**. Token-weighted precision: **85.9%** | Development evidence for the later rule, not an independent validation of it. Neither review establishes whole-corpus quality or production release |
| Earlier standalone BERT filter gate | **Failed: no precision-qualified rule** | Completed classifier inference does not establish a validated filter. The standalone gate remains failed |
| Separate earlier BERT + clinical-filter pilot | **55/60 documents (91.7%)**; document Wilson 95% range **81.9–96.4%**; token precision **94.3%** | A small offline combination, separate from the standalone BERT gate and broader reviews above. This pilot does not replace that gate, establish production release or complete full-corpus filtering |

All review judgments in this table, including the separate 60-document offline pilot, are assistant judgments, not expert human ground truth. Wilson 95% ranges apply only to document precision. **No filter has been approved for production release by these results.**

## Preparation stages

Different sources advance through these stages in parallel. Remove exact duplicates before additional expensive scoring, then verify near-copies before final selection. Existing filtered batches also receive duplicate checks.

| Stage | What it does | Current position |
|---|---|---|
| **1. Collect** | Download and verify original source material | In progress; selected source files are available and additional paper acquisition continues |
| **2. Extract** | Preserve usable text, sequences, tables and source links | In progress; paper conversion continues. Bio retained-prefix tokenizer counts remain unmeasured |
| **3. Remove duplicates** | Identify exact repeats, then verify near-identical copies | The combined-source run covers the **initial 13 source snapshots** and is now **grouping identical text into duplicate families**; this stage remains partial. The **45-source follow-up is queued and has no completed combined inventory yet**. A historical pass checked **157,977 near-copy pairs**, proposing **958 containment links** across its frozen **750,715-record** snapshot. No removals were applied; this does not complete near-copy checks on the current full corpus |
| **4. Score and filter** | Select relevant, useful material and audit the decisions | Inference and selection development continue. The stricter rule failed its fresh audit; final quality approval is pending |
| **5. Validate and package** | Check exclusions, source provenance, document boundaries and final exports | Generated-file checks passed. Actual-source exclusion checks and full export validation remain unfinished. The current full-corpus near-copy follow-up awaits its dependencies; no final combined training release |

Rights and licence eligibility, retraction review, and held-out evaluation exclusions must be checked before release. Source-read unknowns and held outputs remain unresolved; they are not silently treated as verified training material. Original sources are preserved.

**The final combined training collection is still being prepared. No final combined exports or training release are available.** GB uses decimal units. Token amounts shown are measured tokenizer counts; retained Bio tokenizer counts are explicitly unmeasured. Source bindings and raw processing measurements remain in local artifacts. Corpus preparation does not start model training.
