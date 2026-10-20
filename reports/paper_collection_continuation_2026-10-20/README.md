# Native-paper collection

**Status: running** · Updated 2026-10-19T23:42:55-08:00 (fixed PST).

Process existing cluster XML first, then acquire up to **— additional papers** whose identifiers are absent from the known cluster inventory.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 152,440 |
| Existing papers processed | 29,404 |
| New papers processed | 7,955 |
| New papers retained by biology rules | 5,390 |
| Metadata/parse rejections | 89 |
| Candidates skipped because already present | 404 |
| Raw processed tokens | 684,004,443 |
| Exact-unique processed tokens | 683,983,510 |
| Biology-selected tokens before exact deduplication | 414,416,461 |
| Biology-selected exact-unique tokens | 414,395,610 |
| New artifacts | 0.19 GiB / 182.04 GiB |
| Counted pipeline storage | 18.14 GiB / 200.00 GiB |
| Measured HTTP response bodies | 0.00 GiB |
| HTTP budget charged | 0.00 GiB / 200.00 GiB |

Job: 243177; scheduler: RUNNING; stage: Downloading and processing missing papers.

The worker has an original —-hour allowance, two CPU cores and zero GPUs. It stops at the first time, download, storage or candidate limit. The shared free-space floor is 64.00 GiB.

Monitor: watching.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report hourly, including while queued, and on status changes. A separate session monitor queues the requested hourly chat updates.
