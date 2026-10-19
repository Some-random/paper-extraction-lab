# Native-paper collection

**Status: running** · Updated 2026-10-19T14:44:55-08:00 (fixed PST).

Process existing cluster XML first, then acquire up to **10,000 additional papers** whose identifiers are absent from the known cluster inventory.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 144,461 |
| Existing papers processed | 22,416 |
| New papers processed | 0 |
| New papers retained by biology rules | 0 |
| Metadata/parse rejections | 7 |
| Candidates skipped because already present | — |
| Raw processed tokens | 425,326,230 |
| Exact-unique processed tokens | 425,305,323 |
| Biology-selected tokens before exact deduplication | 246,971,004 |
| Biology-selected exact-unique tokens | 246,950,153 |
| New artifacts | 2.21 GiB / 32.00 GiB |
| Counted pipeline storage | 14.94 GiB / 200.00 GiB |
| Measured HTTP response bodies | 0.00 GiB |
| HTTP budget charged | 0.00 GiB / 8.00 GiB |

Job: 242193; scheduler: RUNNING; stage: Extracting existing XML papers.

The worker has an original 24-hour allowance, two CPU cores and zero GPUs. It stops at the first time, download, storage or candidate limit. The shared free-space floor is 64.00 GiB.

Worker deadline: 2026-10-19T22:28:05-08:00 (fixed PST).

Monitor: watching.

Since the previous successful report: +3,561 existing papers; +0 new papers; +67,400,815 raw tokens; +67,400,815 exact-unique tokens; +34,929,886 biology-selected tokens; +348,232,235 artifact bytes; +0 HTTP response bytes.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report hourly, including while queued, and on status changes. A separate session monitor queues the requested hourly chat updates.
