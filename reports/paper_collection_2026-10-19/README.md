# Native-paper collection

**Status: stopped** · Updated 2026-10-19T22:28:11-08:00 (fixed PST).

Process existing cluster XML first, then acquire up to **10,000 additional papers** whose identifiers are absent from the known cluster inventory.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 152,402 |
| Existing papers processed | 29,404 |
| New papers processed | 7,917 |
| New papers retained by biology rules | 5,368 |
| Metadata/parse rejections | 89 |
| Candidates skipped because already present | 403 |
| Raw processed tokens | 683,503,051 |
| Exact-unique processed tokens | 683,482,118 |
| Biology-selected tokens before exact deduplication | 414,105,157 |
| Biology-selected exact-unique tokens | 414,084,306 |
| New artifacts | 4.74 GiB / 32.00 GiB |
| Counted pipeline storage | 17.46 GiB / 200.00 GiB |
| Measured HTTP response bodies | 1.06 GiB |
| HTTP budget charged | 1.06 GiB / 8.00 GiB |

Job: 242193; scheduler: COMPLETED; stage: Downloading and processing missing papers.

The worker has an original 24-hour allowance, two CPU cores and zero GPUs. It stops at the first time, download, storage or candidate limit. The shared free-space floor is 64.00 GiB.

Worker deadline: 2026-10-19T22:28:05-08:00 (fixed PST).

Run detail: runtime_limit.

Monitor: stopped (worker_terminal).

Since the previous successful report: +0 existing papers; +559 new papers; +11,383,732 raw tokens; +11,383,732 exact-unique tokens; +8,256,154 biology-selected tokens; +199,271,638 artifact bytes; +118,654,514 HTTP response bytes.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report hourly, including while queued, and on status changes. A separate session monitor queues the requested hourly chat updates.
