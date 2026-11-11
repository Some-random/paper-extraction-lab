**General data preparation — observed through November 2, 2026**

| Source | Available data | Average length | Remaining work |
|---|---|---:|---|
| **PMC papers** | **9.09M** paper texts; **390.5 GB**; **99.7B** tokens. Cleanup retained **8.52M** papers and set aside **551K** for review. | **11K tokens per paper** | Reconciliation and eligibility checks remain. |
| **BioCollection** | **36.6M** selected records; **91.6 GB**; **36.5B** tokens. Exact duplicates and candidate near-copies were checked. | **995 tokens per record** | Further checks across sources and quality validation remain. |
| **FineWeb-Edu** | **190.2M** pages processed; **11.8M** provisionally retained as biology; **40.2 GB**; **9.14B** tokens. | **775 tokens per retained page** | Biology labels remain provisional; the standalone classifier failed its quality check. |

Average lengths are approximate, calculated from each source’s reported total tokens divided by its reported number of texts. The sources used different tokenizers, so the averages are not directly comparable.

**Preparation stages:** collection, text extraction, duplicate checks, scoring and filtering, then validation and packaging. The individual source snapshots have reached different stages; a combined training corpus has not been released. Sizes are decimal GB and token counts are measured.
