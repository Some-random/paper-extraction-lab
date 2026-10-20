# Native-paper collection

**Status: running** · Updated 2026-10-19T20:56:43-08:00 (fixed PST).

Process existing cluster XML first, then acquire up to **10,000 additional papers** whose identifiers are absent from the known cluster inventory.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 150,091 |
| Existing papers processed | 29,404 |
| New papers processed | 5,610 |
| New papers retained by biology rules | 3,810 |
| Metadata/parse rejections | 72 |
| Candidates skipped because already present | 285 |
| Raw processed tokens | 651,484,104 |
| Exact-unique processed tokens | 651,463,171 |
| Biology-selected tokens before exact deduplication | 390,807,790 |
| Biology-selected exact-unique tokens | 390,786,939 |
| New artifacts | 4.22 GiB / 32.00 GiB |
| Counted pipeline storage | 16.94 GiB / 200.00 GiB |
| Measured HTTP response bodies | 0.76 GiB |
| HTTP budget charged | 0.76 GiB / 8.00 GiB |

Job: 242193; scheduler: RUNNING; stage: Downloading and processing missing papers.

The worker has an original 24-hour allowance, two CPU cores and zero GPUs. It stops at the first time, download, storage or candidate limit. The shared free-space floor is 64.00 GiB.

Worker deadline: 2026-10-19T22:28:05-08:00 (fixed PST).

Monitor: watching.

Since the previous successful report: +0 existing papers; +984 new papers; +20,670,015 raw tokens; +20,670,015 exact-unique tokens; +14,946,928 biology-selected tokens; +358,080,006 artifact bytes; +213,197,350 HTTP response bytes.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report hourly, including while queued, and on status changes. A separate session monitor queues the requested hourly chat updates.
