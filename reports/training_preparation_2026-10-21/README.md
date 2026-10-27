# General data preparation

Updated **October 27, 08:38 UTC, 2026**. PMC downloading continues; the new parser is queued behind source-snapshot preparation. BioCollection has a usable local export with basic format checks, while its content-checking and benchmark-exclusion pass is running. FineWeb-Edu’s full-source exact pass, near-copy candidate search and candidate-pair verification are complete; applying the near-copy decisions and qualifying biology selection remain. The protein question-answer dataset is documented separately.

## Source content and progress

**Completion refers to the named processing stage, not a finished training corpus.** Recent changes compare with the preceding report from **October 26, 17:53 UTC**.

| Source content | Collection | Processing progress and measured content | Remaining work and recent change |
|---|---|---|---|
| **PMC research papers** | **3.00 million verified downloaded XML papers in the current batch**, with approximately **5.19 million targets still to check**. The broader inventory contains **9.27 million entries**; some do not offer accessible full text. | **1,164,222 papers processed; 51.41 GB of paper text; 13.234 billion measured tokens.** This main paper-text total remains **partial**. It uses one primary text per paper and includes all available full text without the old keyword filter. Newly downloaded papers enter this total after extraction. | Continue downloading; finish source snapshots and process the new batch, then complete duplicate removal, eligibility checks and packaging.<br>Recent change: **approximately 0.78 million more XML papers downloaded; the measured processed-text total is unchanged.** |
| **TheBioCollection: biological text, protein/DNA/RNA sequences and molecular representations** | **All 32 selected files downloaded and verified; 37.23 million source records.** | **36,900,545 retained records; 92.03 GB; 36.659 billion measured tokens.** Exact duplicate removal, token recounting, the prose near-copy pass and basic format checks are complete. The source-linked local streaming export has been tested on actual records from all 32 files. | Finish the native content-consistency and benchmark-exclusion pass, check prose relevance, then update the selected export. Protein/DNA/RNA variants are preserved; prose similarity checks do not establish sequence or homology deduplication.<br>Recent change: **token recount and basic export completed; deeper checks are running.** These do not establish scientific-quality validation. |
| **FineWeb-Edu: educational web pages** | **190.17 million source pages across all 234 files are available.** | **Full-source exact duplicate pass, near-copy candidate discovery and candidate-pair verification complete (100%).** All **100.89 million candidate pairs** have been checked. Near-copy removals have not yet been applied. Final biology-selected page count, text size and token total are not yet measured. Earlier retained candidates remain provisional. | Qualify and apply biology/content-quality selection; combine near-copy decisions with benchmark exclusions, then finish current cross-source checks and export. The historical standalone classifier and the latest content-filter pilot **failed their quality checks**. Further bulk filtering awaits a qualified replacement.<br>Recent change: **full exact comparison and near-copy evidence are now complete.** |

## Preparation stages

Remove exact duplicates before further expensive scoring, then check near-copies before final selection.

| Stage | Purpose | Current position |
|---|---|---|
| **1. Collect** | Download and verify original material | PMC downloading continues. Selected BioCollection and FineWeb-Edu files are available. |
| **2. Extract** | Convert source material into usable text and sequences, preserving source links | PMC extraction is partial; the new parser is queued behind source-snapshot preparation while downloading continues. BioCollection and FineWeb-Edu records are available for processing. |
| **3. Remove duplicates** | Remove exact repeats and check near-identical copies within and across sources | BioCollection’s exact pass and prose near-copy pass are complete. FineWeb-Edu’s exact pass and candidate-pair verification are complete; applying the near-copy decisions remains. Current cross-source coverage remains unfinished. |
| **4. Score and filter** | Select useful biological content and check filtering quality | BioCollection’s deeper content checks are running. FineWeb-Edu candidates are provisional; another content-filter revision is being tested after failed quality review. |
| **5. Validate and package** | Confirm counts, exclusions, source permissions and final training exports | BioCollection’s initial streaming export and measured token total are ready. Benchmark exclusions, updated selected exports and the final combined corpus remain unfinished. |

**The combined training corpus is not yet released.** GB uses decimal units; token amounts are measured tokenizer counts. No model training is part of this corpus-preparation work.
