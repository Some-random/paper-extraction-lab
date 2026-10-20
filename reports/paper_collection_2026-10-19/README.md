# Native-paper collection

**Status: running** · Updated 2026-10-19T17:55:49-08:00 (fixed PST).

Process existing cluster XML first, then acquire up to **10,000 additional papers** whose identifiers are absent from the known cluster inventory.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 145,635 |
| Existing papers processed | 29,404 |
| New papers processed | 1,166 |
| New papers retained by biology rules | 782 |
| Metadata/parse rejections | 24 |
| Candidates skipped because already present | 53 |
| Raw processed tokens | 588,237,553 |
| Exact-unique processed tokens | 588,216,620 |
| Biology-selected tokens before exact deduplication | 344,589,326 |
| Biology-selected exact-unique tokens | 344,568,475 |
| New artifacts | 3.20 GiB / 32.00 GiB |
| Counted pipeline storage | 15.93 GiB / 200.00 GiB |
| Measured HTTP response bodies | 0.15 GiB |
| HTTP budget charged | 0.15 GiB / 8.00 GiB |

Job: 242193; scheduler: RUNNING; stage: Downloading and processing missing papers.

The worker has an original 24-hour allowance, two CPU cores and zero GPUs. It stops at the first time, download, storage or candidate limit. The shared free-space floor is 64.00 GiB.

Worker deadline: 2026-10-19T22:28:05-08:00 (fixed PST).

Monitor: watching.

Since the previous successful report: +0 existing papers; +779 new papers; +15,687,616 raw tokens; +15,687,616 exact-unique tokens; +11,376,061 biology-selected tokens; +273,011,900 artifact bytes; +161,852,254 HTTP response bytes.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report hourly, including while queued, and on status changes. A separate session monitor queues the requested hourly chat updates.
