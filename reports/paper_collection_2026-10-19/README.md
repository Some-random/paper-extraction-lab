# Native-paper collection

**Status: running** · Updated 2026-10-19T10:42:51-08:00 (fixed PST).

Process existing cluster XML first, then acquire up to **10,000 additional papers** whose identifiers are absent from the known cluster inventory.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 144,461 |
| Existing papers processed | 5,118 |
| New papers processed | 0 |
| New papers retained by biology rules | 0 |
| Metadata/parse rejections | 1 |
| Candidates skipped because already present | — |
| Raw processed tokens | 109,504,694 |
| Exact-unique processed tokens | 109,504,694 |
| Biology-selected tokens before exact deduplication | 67,539,401 |
| Biology-selected exact-unique tokens | 67,539,401 |
| New artifacts | 0.63 GiB / 32.00 GiB |
| Counted pipeline storage | 13.36 GiB / 200.00 GiB |
| Measured HTTP response bodies | 0.00 GiB |
| HTTP budget charged | 0.00 GiB / 8.00 GiB |

Job: 242193; scheduler: RUNNING; stage: Extracting existing XML papers.

The worker has an original 24-hour allowance, two CPU cores and zero GPUs. It stops at the first time, download, storage or candidate limit. The shared free-space floor is 64.00 GiB.

Worker deadline: 2026-10-19T22:28:05-08:00 (fixed PST).

Monitor: watching.

Since the previous successful report: +92 existing papers; +0 new papers; +2,051,057 raw tokens; +2,051,057 exact-unique tokens; +1,084,957 biology-selected tokens; +14,387,034 artifact bytes; +0 HTTP response bytes.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report hourly, including while queued, and on status changes. A separate session monitor queues the requested hourly chat updates.
