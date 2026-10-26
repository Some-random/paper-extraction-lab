# General data preparation

Updated **October 26, 17:53 UTC, 2026**. PMC downloading continues. BioCollection’s exact duplicate removal and record-count checks are complete. FineWeb-Edu’s full-source inventory is complete; duplicate removal and biology selection remain unfinished. The protein question-answer dataset is documented separately.

## Source content and progress

**Completion refers to the named processing stage, not a finished training corpus.** Recent changes compare with the preceding public report from **October 25, 18:39 UTC**.

| Source content | Collection | Processing progress and measured content | Remaining work and recent change |
|---|---|---|---|
| **PMC research papers** | **2.22 million verified XML papers in the current download batch**, with approximately **5.98 million targets still to check**. The broader inventory contains **9.27 million entries**; some do not offer accessible full text. | **1,164,222 papers processed; 51.41 GB of paper text; 13.234 billion measured tokens.** This main paper-text total remains **partial**. It uses one primary text per paper and includes all available full text without the old keyword filter. Newly downloaded papers enter this total after extraction. | Continue downloading and extracting, then complete duplicate removal, eligibility checks and final packaging.<br>Recent change: **+610,437 processed papers; +28.14 GB; +7.183 billion tokens.** |
| **TheBioCollection: biological text, protein/DNA/RNA sequences and molecular representations** | **All 32 selected files downloaded and verified; 37.23 million source records.** | **36.90 million retained records; 92.03 GB**, after removing **326,539 exact duplicates**. Exact duplicate removal and record-count checks are complete. **Tokens for this updated retained set have not yet been remeasured.** | Near-copy and cross-source checks, token recounting, quality selection and final packaging remain.<br>Recent change: **exact duplicate removal and record-count verification completed for the updated set.** |
| **FineWeb-Edu: educational web pages** | **190.17 million source pages across all 234 files are available.** | **Full-source duplicate inventory complete (100%).** Final biology-selected page count, text size and token total are not yet measured. Earlier retained candidates remain provisional. | Exact sorting and merging are next, followed by near-copy checks and further biology filtering. Further bulk scoring is paused; the filter has **not passed quality validation**.<br>Recent change: **+131.65 million rows inventoried**, completing full-source coverage. |

## Preparation stages

Remove exact duplicates before further expensive scoring, then check near-copies before final selection.

| Stage | Purpose | Current position |
|---|---|---|
| **1. Collect** | Download and verify original material | PMC downloading continues. Selected BioCollection and FineWeb-Edu files are available. |
| **2. Extract** | Convert source material into usable text and sequences, preserving source links | PMC extraction is partial; additional downloaded papers are being prepared for extraction. BioCollection and FineWeb-Edu records are available for processing. |
| **3. Remove duplicates** | Remove exact repeats and check near-identical copies within and across sources | BioCollection’s exact pass is complete. FineWeb-Edu’s full inventory is complete, with sorting and merging next. Near-copy and current cross-source coverage remain unfinished. |
| **4. Score and filter** | Select useful biological content and check filtering quality | Final quality selection remains unfinished. FineWeb-Edu candidates are provisional; its filter still needs to pass validation. |
| **5. Validate and package** | Confirm counts, exclusions, source permissions and final training exports | Record-count checks have advanced. Updated token accounting and final combined exports remain unfinished. |

**The combined training corpus is not yet released.** GB uses decimal units; token amounts are measured tokenizer counts. No model training is part of this corpus-preparation work.
