# General data preparation

Updated **October 23, 2026**. This report covers the general data collection; the protein question-answer dataset is documented separately.

## Source content and progress

| Source content | Total available in this source | Collected so far | Prepared so far | Current work |
|---|---:|---:|---|---|
| PMC research papers | 9.27 million papers | **700,888 papers** | About **290,000 converted to text**; about **410,000 awaiting conversion** | Downloading and text extraction continue |
| TheBioCollection: biological text, sequences, and molecular data | 37.23 million records in the selected release | All 37.23 million records | **92.61 GB; 36.98 billion tokens** | Filtering and duplicate checks remain |
| FineWeb-Edu: educational web pages | 190.17 million source pages | Source files downloaded | **1.75 million provisionally retained pages; 5.98 GB; 1.36 billion tokens** | Biology filtering and quality review continue |

## Preparation stages

| Stage | What it does | Progress |
|---|---|---|
| **1. Collect** | Download the original source material | Paper downloads continue; the selected reference and web sources are available |
| **2. Extract** | Turn source files into usable text and sequences | Paper conversion continues; the selected reference collection has been read and counted |
| **3. Score and filter** | Assess relevance and quality, then select useful material | Web relevance scoring and filtering are running; final quality approval is pending |
| **4. Remove duplicates** | Find repeated documents and near-identical copies | An initial exact-copy pass is complete; the full combined collection still needs duplicate checks |
| **5. Validate and package** | Check the selected data and assemble the final training files | Not yet complete |

**The final combined training collection is still being prepared.** GB uses decimal units; tokens are the text units used by language models.
