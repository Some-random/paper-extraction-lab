# Native-paper collection

**Status: running** · Updated 2026-10-19T18:56:04-08:00 (fixed PST).

Process existing cluster XML first, then acquire up to **10,000 additional papers** whose identifiers are absent from the known cluster inventory.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 147,211 |
| Existing papers processed | 29,404 |
| New papers processed | 2,740 |
| New papers retained by biology rules | 1,868 |
| Metadata/parse rejections | 38 |
| Candidates skipped because already present | 136 |
| Raw processed tokens | 611,521,212 |
| Exact-unique processed tokens | 611,500,279 |
| Biology-selected tokens before exact deduplication | 361,608,712 |
| Biology-selected exact-unique tokens | 361,587,861 |
| New artifacts | 3.57 GiB / 32.00 GiB |
| Counted pipeline storage | 16.30 GiB / 200.00 GiB |
| Measured HTTP response bodies | 0.37 GiB |
| HTTP budget charged | 0.37 GiB / 8.00 GiB |

Job: 242193; scheduler: RUNNING; stage: Downloading and processing missing papers.

The worker has an original 24-hour allowance, two CPU cores and zero GPUs. It stops at the first time, download, storage or candidate limit. The shared free-space floor is 64.00 GiB.

Worker deadline: 2026-10-19T22:28:05-08:00 (fixed PST).

Monitor: watching.

Since the previous successful report: +0 existing papers; +1,086 new papers; +23,283,659 raw tokens; +23,283,659 exact-unique tokens; +17,019,386 biology-selected tokens; +399,173,969 artifact bytes; +238,475,069 HTTP response bytes.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report hourly, including while queued, and on status changes. A separate session monitor queues the requested hourly chat updates.
