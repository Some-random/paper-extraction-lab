# General data preparation

Updated **October 25, 17:09 UTC, 2026**. Counts below were observed between 17:03 and 17:09 UTC. FineWeb’s full-source hash inventory is advancing from its saved checkpoints. Cross-source deduplication is running. PMC is processing downloaded XML again and has recorded additional primary texts; its main paper-text total remains partial. BioCollection’s source-only exact pass, all 32 keep-list exports and retained token accounting are complete. Further paper downloads and bulk web scoring remain paused. The protein question-answer dataset is documented separately.

## Source content and progress

**Each percentage describes its named stage, not an approved training corpus.** Recent changes compare with the preceding public report, around **October 25, 15:39 UTC**.

| Source content | Collection | Processing progress and measured content | Remaining work and recent change |
|---|---|---|---|
| **PMC research papers** | **1,186,806 collected paper IDs**, against **9,273,077 inventory entries**. Some inventory entries do not offer accessible full text. | **504,208 / 1,186,806 collected IDs have a chosen primary text; 21.287783328 GB; 5.544292676 billion tokens.** This is the main paper-text total and remains **partial**: one primary text per paper, using all available text without the old keyword filter. | **679,854 downloaded XML papers await parsing.** The parser has completed startup checks and recorded additional primary texts. Network acquisition remains paused while downloaded XML is processed. Retraction, eligibility and final duplicate checks remain unfinished.<br>Recent change: **+2,462 primary texts; +0.088081 GB; +0.022700 billion tokens.** |
| **TheBioCollection: biological text, protein/DNA/RNA sequences and molecular representations** | **All 32 selected files downloaded and verified; 37,227,086 records.** | **Source-only exact deduplication and all 32 keep-list exports are complete.**<br>`████████████████████`<br>**36,900,548 retained records; 92.032531 GB; 36.658781 billion measured tokens.** The pass excluded **326,538 exact repeats** from this derivative. | **Zero records remain unchecked in this source-only exact pass.** Cross-source duplicate checks, quality review and final combined packaging remain unfinished.<br>Recent change: **no change to the completed source-only counts.** These exports point to retained records in the original files; final combined training files are still pending. |
| **FineWeb-Edu: educational web pages** | **190,168,005 original source rows**; local source files are available. | **Full-source exact-duplicate inventory is running: at least 48,989,304 / 190,168,005 original rows durably recorded — 25.761%.** 64 shards have started; 56 have completed their inventory. Saved checkpoints are being extended; sorting and merging remain unfinished.<br>Separately, saved classifier decisions cover **48,551,899 rows (25.531%)**, with **2,982,308 provisionally retained pages; 10.331942 GB; 2.350637 billion tokens**. | **At most 141,178,701 rows remain outside the new hash inventory at this snapshot.** Sorting, exact representative selection, cross-source and near-copy checks are unfinished. **141,616,106 rows remain outside the older classifier-decision frame.** Its retained totals are unchanged saved measurements, not new scoring or confirmed biological pages. Bulk scoring is paused; filter quality remains unqualified.<br>Recent change: **+10,464,944 rows recorded; +16 shard inventories completed.** |

## Quality evidence

These results are unchanged. More processed data does not by itself improve filter quality.

| Review | Result | What it establishes |
|---|---|---|
| Complete-source classifier development check: 64 documents | **22 core candidates, 13 outside the core, 29 held unknown.** Holds include 26 format failures, two uncertainties and one output-limit case | Assistant review of the 22 proposed core pages supported **10**, held **11** and classified **one** as catalog content. Known development cases do not estimate corpus precision; semantic quality remains unqualified |
| Fresh blinded assistant audit: 400 retained candidates and 150 vetoed documents | **Failed both 90% targets:** **333/400 (83.25%)** met strict biology, usefulness and readability criteria. Document Wilson 95%: **79.3–86.6%**. Token-weighted precision: **86.63%** | The rule was frozen before all 550 judgments. Higher classifier confidence did not establish adequate quality; the pool remains provisional |
| Earlier blinded assistant review: 200 retained and 200 rejected or noncandidate documents | **159/200 retained (79.5%)** met strict criteria. Document Wilson 95%: **73.4–84.5%**. Token-weighted precision: **85.9%** | Development evidence for the later rule; no independent validation or whole-corpus quality claim |
| Earlier standalone BERT gate | **Failed: no precision-qualified rule** | Completed inference does not establish a validated filter; the standalone gate remains failed |
| Separate earlier BERT + clinical-filter pilot | **55/60 documents (91.7%)**; document Wilson 95%: **81.9–96.4%**; token precision: **94.3%** | A separate offline combination. It does not replace the standalone BERT gate, establish release or complete full-corpus filtering |

All judgments above are **assistant reviews, not expert human ground truth**. Wilson 95% ranges apply only to document precision. **No filter has been approved for production release by these results.**

## Preparation stages

Remove exact duplicates before further expensive scoring, then verify near-copies before final selection.

| Stage | Purpose | Current position |
|---|---|---|
| **1. Collect** | Download and verify original material | Selected BioCollection files are available. PMC is processing downloaded XML; further network acquisition remains paused |
| **2. Extract** | Preserve usable text, sequences, tables and source links | BioCollection’s 32 keep-list exports and source-only token accounting are complete. PMC processing has resumed, with new primary texts saved; its paper-text total remains partial |
| **3. Remove duplicates** | Identify exact repeats, then verify near-identical copies | Bio’s source-only exact pass is complete; the full-original web hash inventory is advancing. The earlier **13-snapshot merge completed with 22 duplicate records**, using already-retained web pages and a **frozen 348,123-paper view**. Its **45-source follow-up is running**, with **7,843,066 / 39,756,831 input records processed (19.73%)**, using the same older 13 snapshots plus all 32 Bio inventories. Its 65,060 raw-exact omissions include Bio’s already-detected source-only duplicates; they are not all additional cross-source removals. Recent change: **+3,911,137 input records processed.** These older retained-source passes do not cover the full 190,168,005-row web universe or later PMC additions. Full sorting/merging, current cross-source and near-copy checks remain unfinished |
| **4. Score and filter** | Select useful material and audit decisions | Bulk web scoring remains paused until full-source exact preparation and filter qualification are ready. The stricter rule failed its fresh audit |
| **5. Validate and package** | Check exclusions, provenance, boundaries and exports | Source exclusions, licence/retraction review, current near-copy verification and final exports remain unfinished. Token accounting after cross-source deduplication awaits the current merge and its follow-up |

Original sources and unresolved cases are preserved. **No final combined exports or training release are available.** GB uses decimal units; reported token amounts are recorded tokenizer measurements. **No model training is part of this corpus work. Recurring two-hour chat updates are off.**
