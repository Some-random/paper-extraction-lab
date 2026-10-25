# General data preparation

Updated **October 25, 2026, around 14:28 UTC**. BioCollection has completed its source-only exact-duplicate pass, all 32 exports and retained token accounting. The cross-source duplicate follow-up and full-source web hash inventory are running. PMC is checkpointed while a parser performance update completes restart checks. Further paper downloads and bulk web scoring remain paused. The protein question-answer dataset is documented separately.

## Source content and progress

**Each percentage describes its named stage, not an approved training corpus.** Recent changes compare with the preceding public report, around **October 25, 14:09 UTC**.

| Source content | Collection | Processing progress and measured content | Remaining work and recent change |
|---|---|---|---|
| **PMC research papers** | **1,186,806 collected paper IDs**, against **9,273,077 inventory entries**. Some inventory entries do not offer accessible full text. | **494,751 / 1,186,806 collected IDs have a chosen primary text; 20.866230 GB; 5.436035 billion tokens.** This is the main paper-text total and remains **partial**: one primary text per paper, using all available text without the old keyword filter. | **689,374 downloaded XML papers await parsing.** Parsing is temporarily checkpointed while the performance update completes restart checks. Network acquisition is paused. Retraction, eligibility and final duplicate checks remain unfinished.<br>Recent change: **+2,523 primary texts; no additional collected IDs.** |
| **TheBioCollection: biological text, protein/DNA/RNA sequences and molecular representations** | **All 32 selected files downloaded and verified; 37,227,086 records.** | **Source-only exact deduplication and all 32 exports are complete.**<br>`████████████████████`<br>**36,900,548 retained records; 92.032531 GB; 36.658781 billion measured tokens.** The pass excluded **326,538 exact repeats** from this derivative. | **Zero records remain unchecked in this source-only exact pass.** Cross-source duplicate checks, quality review and final combined packaging remain unfinished.<br>Recent change: **the remaining 16 exports completed; the complete retained token total is now available.** |
| **FineWeb-Edu: educational web pages** | **190,168,005 original source rows**; local source files are available. | **Full-source exact-duplicate inventory is running: at least 28,250,888 / 190,168,005 original rows durably recorded — 14.856%.** 40 shards have started; 32 have completed their inventory. Sorting and merging remain unfinished.<br>Separately, saved classifier decisions cover **48,551,899 rows (25.531%)**, with **2,982,308 provisionally retained pages; 10.331942 GB; 2.350637 billion tokens**. | **At most 161,917,117 rows remain outside the new hash inventory at this snapshot.** Sorting, exact representative selection, cross-source and near-copy checks are unfinished. **141,616,106 rows remain outside the older classifier-decision frame.** Its retained totals are unchanged saved measurements, not new scoring or confirmed biological pages. Bulk scoring is paused; filter quality remains unqualified.<br>Recent change: **+4,187,472 rows recorded in the full-source hash inventory.** |

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
| **1. Collect** | Download and verify original material | Selected BioCollection files are available. Further PMC acquisition is paused while its downloaded backlog is processed |
| **2. Extract** | Preserve usable text, sequences, tables and source links | BioCollection’s 32 exports and source-only token accounting are complete. PMC is checkpointed for a parser update |
| **3. Remove duplicates** | Identify exact repeats, then verify near-identical copies | Bio’s source-only exact pass is complete; the full-original web hash inventory is running. The earlier **13-snapshot merge completed with 22 duplicate records**, using already-retained web pages and a **frozen 348,123-paper view**. Its **45-source follow-up is running**, using the same older 13 snapshots plus all 32 Bio inventories. Those passes do not cover all original web rows. Full sorting/merging, current cross-source and near-copy checks remain unfinished |
| **4. Score and filter** | Select useful material and audit decisions | Bulk web scoring remains paused until full-source exact preparation and filter qualification are ready. The stricter rule failed its fresh audit |
| **5. Validate and package** | Check exclusions, provenance, boundaries and exports | Source exclusions, licence/retraction review, current near-copy verification and final exports remain unfinished. Token accounting after cross-source deduplication awaits the current merge and its follow-up |

Original sources and unresolved cases are preserved. **No final combined exports or training release are available.** GB uses decimal units; reported token amounts are recorded tokenizer measurements. **No model training is part of this corpus work. Recurring two-hour chat updates are off.**
