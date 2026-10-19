# Native-paper collection

**Status: running** · Updated 2026-10-19T10:41:04-08:00 (fixed PST).

Process existing cluster XML first, then acquire up to **10,000 additional papers** whose identifiers are absent from the known cluster inventory.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 144,461 |
| Existing papers processed | 5,026 |
| New papers processed | 0 |
| New papers retained by biology rules | 0 |
| Metadata/parse rejections | 1 |
| Candidates skipped because already present | — |
| Raw processed tokens | 107,453,637 |
| Exact-unique processed tokens | 107,453,637 |
| Biology-selected tokens before exact deduplication | 66,454,444 |
| Biology-selected exact-unique tokens | 66,454,444 |
| New artifacts | 0.62 GiB / 32.00 GiB |
| Counted pipeline storage | 13.34 GiB / 200.00 GiB |
| Measured HTTP response bodies | 0.00 GiB |
| HTTP budget charged | 0.00 GiB / 8.00 GiB |

Job: 242193; scheduler: RUNNING; stage: Extracting existing XML papers.

The worker has an original 24-hour allowance, two CPU cores and zero GPUs. It stops at the first time, download, storage or candidate limit. The shared free-space floor is 64.00 GiB.

Worker deadline: 2026-10-19T22:28:05-08:00 (fixed PST).

Monitor: not_running (supervisor_restart_pending).

Since the previous successful report: +1,244 existing papers; +0 new papers; +27,392,597 raw tokens; +27,392,597 exact-unique tokens; +17,291,846 biology-selected tokens; +143,887,595 artifact bytes; +0 HTTP response bytes.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report hourly, including while queued, and on status changes. These are GitHub updates; automatic chat notifications are not configured.
