# Native-paper collection

**Status: running** · Updated 2026-10-19T16:55:25-08:00 (fixed PST).

Process existing cluster XML first, then acquire up to **10,000 additional papers** whose identifiers are absent from the known cluster inventory.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 144,464 |
| Existing papers processed | 29,404 |
| New papers processed | 3 |
| New papers retained by biology rules | 3 |
| Metadata/parse rejections | 10 |
| Candidates skipped because already present | — |
| Raw processed tokens | 572,549,937 |
| Exact-unique processed tokens | 572,529,004 |
| Biology-selected tokens before exact deduplication | 333,213,265 |
| Biology-selected exact-unique tokens | 333,192,414 |
| New artifacts | 2.95 GiB / 32.00 GiB |
| Counted pipeline storage | 15.67 GiB / 200.00 GiB |
| Measured HTTP response bodies | 0.00 GiB |
| HTTP budget charged | 0.00 GiB / 8.00 GiB |

Job: 242193; scheduler: RUNNING; stage: Downloading and processing missing papers.

The worker has an original 24-hour allowance, two CPU cores and zero GPUs. It stops at the first time, download, storage or candidate limit. The shared free-space floor is 64.00 GiB.

Worker deadline: 2026-10-19T22:28:05-08:00 (fixed PST).

Monitor: watching.

Since the previous successful report: +413 existing papers; +3 new papers; +8,870,977 raw tokens; +8,870,977 exact-unique tokens; +5,362,692 biology-selected tokens; +52,000,670 artifact bytes; +742,673 HTTP response bytes.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report hourly, including while queued, and on status changes. A separate session monitor queues the requested hourly chat updates.
