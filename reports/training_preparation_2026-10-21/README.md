**General data preparation — observed through November 2, 2026**

| Source | Current result | Remaining work |
|---|---|---|
| **PMC papers** | The October 30 verified snapshot contains **9,090,547 paper texts**, **390.511 decimal GB** and **99.711 billion tokens**. Cleanup retained **8,519,207 papers** and preserved **550,634 unresolved papers** for review. | The main download queue is practically complete; reconciliation and eligibility checks remain. |
| **BioCollection** | **36,642,380 selected records**, **91.558 decimal GB** and **36.451 billion tokens**. Exact duplicates and candidate near-copies have been checked. | Further cross-source checks and quality validation remain. |
| **FineWeb-Edu** | All **190,168,005 local pages** were processed. The biology filter provisionally retained **11,795,871 pages**, **40.163 decimal GB** and **9.139 billion tokens**. A separate deduplicated view is available. | The biology labels remain provisional; the standalone BERT quality gate failed. |

**Preparation stages:** collection, text extraction, duplicate checks, scoring and filtering, then validation and packaging. The individual source snapshots have reached different stages; a combined training corpus has not been released. Sizes are decimal GB and token counts are measured.
