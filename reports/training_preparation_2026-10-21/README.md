# General data preparation

Updated **October 25, 2026, around 10:25 UTC**. We are preparing a clean collection with traceable sources, duplicate checks and quality review. Paper processing has restarted and is checking saved work before continuing from the local cache. BioCollection duplicate processing is running. Additional paper downloads and bulk web scoring are paused. The protein question-answer dataset is documented separately.

## Source content and progress

**Percentages describe the named processing stage, not completion of an approved training corpus.** Paper totals are the latest published measurements; the restarted parser has not yet published new progress. Recent changes compare with the preceding public report, observed around **October 25, 08:38 UTC**.

| Source content | Collection | Processing progress and measured content | Remaining work and recent change |
|---|---|---|---|
| **PMC research papers** | **1,186,806 paper IDs recorded as collected**, against **9,273,077 inventory entries**. Accessibility varies; some entries do not offer downloadable full text. | **456,959 primary paper texts; 19.220798 GB; 5.016074 billion tokens.** This is the main paper-text total and remains partial: one primary text per paper, including all available text without the old keyword filter. | **727,754 downloaded XML papers await parsing.** The parser is checking saved work before resuming this backlog; network acquisition is paused. Retraction, eligibility and final duplicate checks remain incomplete.<br>Recent change: **+7,586 primary texts; no additional collected IDs.** |
| **TheBioCollection: biological text, protein/DNA/RNA sequences and molecular representations** | **All 32 selected files downloaded and verified; 37,227,086 records.** | **Exact duplicate pass: 29,131,477 / 37,227,086 records — 78.253%**<br>`████████████████░░░░`<br>All files have completed hashing. The retained prefix contains **28,876,237 records; 72.021257 GB**. | **8,095,609 records remain unchecked.** Retained-prefix tokenizer counts are **not measured**. Final retained totals, quality review and packaging remain pending; sequence variants are preserved.<br>Recent change: **+2,489,456 checked; +2,467,764 retained records.** |
| **FineWeb-Edu: educational web pages** | **190,168,005 original source rows**; local source files are available. | **Reconciled saved decisions: 48,551,899 / 190,168,005 rows — 25.531%**<br>`█████░░░░░░░░░░░░░░░`<br>**2,982,308 pages provisionally retained; 10.331942 GB; 2.350637 billion tokens.** These are complete saved measurements for the represented decisions, not a fresh rereading of page contents. | **141,616,106 original rows remain outside this reconciled decision frame**, including unresolved source-read failures. Existing repair decisions are now combined with the earlier pass within the same original source universe. This is **reconciliation, not new classifier progress**. Bulk scoring is paused until duplicate preparation over all original rows and filter qualification are ready. Retained pages remain provisional; the quality gate is failed. |

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

Remove exact duplicates before further expensive scoring, then verify near-copies before final selection. The sources advance through these stages in parallel.

| Stage | What it does | Current position |
|---|---|---|
| **1. Collect** | Download and verify original material | Selected BioCollection files are available. Further paper acquisition is paused while the downloaded backlog is processed |
| **2. Extract** | Preserve usable text, sequences, tables and source links | Paper processing has restarted with saved-work checks before further parsing. Bio retained-prefix tokenizer counts remain unmeasured |
| **3. Remove duplicates** | Identify exact repeats, then verify near-identical copies | BioCollection exact processing is running. The initial **13-snapshot exact merge completed**, identifying **22 duplicate records**; its web inputs were already-retained pages. The **45-source follow-up is waiting for BioCollection**. These passes do not inventory all original web rows: exact checks over the full **190 million-row** source are still being prepared. Current near-copy and cross-source checks remain unfinished |
| **4. Score and filter** | Select relevant, useful material and audit decisions | Bulk web scoring is paused pending full-source exact duplicate preparation and a qualified filter. The stricter rule failed its fresh audit; engineering and quality work remain incomplete |
| **5. Validate and package** | Check exclusions, provenance, document boundaries and exports | Source exclusions, licence and retraction review, current near-copy verification and actual export validation remain unfinished. Final Bio token accounting waits for its required processing stages. No final combined training release |

Original sources are preserved. Source-read unknowns and held outputs remain unresolved; they are not silently accepted as training material. **No final combined exports or training release are available.** GB uses decimal units. Token amounts shown are tokenizer measurements recorded during processing; retained Bio tokenizer counts remain unmeasured. **No model training is part of this corpus-preparation work. Recurring two-hour chat updates are off.**
