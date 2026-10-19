# Native-paper collection

**Status: running** · Updated 2026-10-19T12:43:20-08:00 (fixed PST).

Process existing cluster XML first, then acquire up to **10,000 additional papers** whose identifiers are absent from the known cluster inventory.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 144,461 |
| Existing papers processed | 14,616 |
| New papers processed | 0 |
| New papers retained by biology rules | 0 |
| Metadata/parse rejections | 4 |
| Candidates skipped because already present | — |
| Raw processed tokens | 287,822,871 |
| Exact-unique processed tokens | 287,801,978 |
| Biology-selected tokens before exact deduplication | 176,283,306 |
| Biology-selected exact-unique tokens | 176,262,455 |
| New artifacts | 1.56 GiB / 32.00 GiB |
| Counted pipeline storage | 14.29 GiB / 200.00 GiB |
| Measured HTTP response bodies | 0.00 GiB |
| HTTP budget charged | 0.00 GiB / 8.00 GiB |

Job: 242193; scheduler: RUNNING; stage: Extracting existing XML papers.

The worker has an original 24-hour allowance, two CPU cores and zero GPUs. It stops at the first time, download, storage or candidate limit. The shared free-space floor is 64.00 GiB.

Worker deadline: 2026-10-19T22:28:05-08:00 (fixed PST).

Monitor: watching.

Since the previous successful report: +4,838 existing papers; +0 new papers; +82,083,051 raw tokens; +82,083,009 exact-unique tokens; +47,792,472 biology-selected tokens; +444,308,939 artifact bytes; +0 HTTP response bytes.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report hourly, including while queued, and on status changes. A separate session monitor queues the requested hourly chat updates.
