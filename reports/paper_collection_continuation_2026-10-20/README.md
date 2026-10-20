# Native-paper collection

**Status: running** · Updated 2026-10-19T23:46:50-08:00 (fixed PST).

Continue downloading missing biological papers from the preserved identifier and exact-text deduplication ledger. Previously processed papers remain counted and are read in place. There is no fixed paper-count target or total runtime deadline; storage determines how far acquisition can continue.

Paper and token totals are cumulative across the prior run and this continuation; the continuation rows show only the additional work.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 152,488 |
| Existing papers processed | 29,404 |
| New papers processed | 8,003 |
| New papers retained by biology rules | 5,419 |
| Metadata/parse rejections | 90 |
| Candidates skipped because already present | 405 |
| Raw processed tokens | 684,637,005 |
| Exact-unique processed tokens | 684,616,072 |
| Biology-selected tokens before exact deduplication | 414,879,796 |
| Biology-selected exact-unique tokens | 414,858,945 |
| Papers processed during this continuation | 86 |
| Papers selected during this continuation | 51 |
| Raw tokens added during this continuation | 1,133,954 |
| Selected exact-unique tokens added during this continuation | 774,639 |
| Prior paper-run artifacts | 4.74 GiB |
| Continuation artifacts, including the copied index | 0.20 GiB |
| Combined paper-run artifacts | 4.93 GiB |
| Prior paper-run HTTP response bodies | 1.06 GiB |
| Continuation HTTP response bodies | 0.01 GiB |
| Combined paper-run HTTP response bodies | 1.08 GiB |
| Shared filesystem free space | 81.27 GiB |
| Pipeline storage including reserved reporting headroom | 18.17 GiB / 200.00 GiB |
| Counted pipeline storage | 18.16 GiB / 200.00 GiB |
| Measured HTTP response bodies | 0.01 GiB |
| HTTP budget charged | 0.01 GiB / 200.00 GiB |

Job: 243177; scheduler: RUNNING; stage: Downloading and processing missing papers.

One serial worker uses two CPU cores and zero GPUs. It preserves a shared-free-space floor of **64.00 GiB** and a total pipeline-data ceiling of **200.00 GiB**, including prior data, the copied index, new XML, parsed outputs, temporary writes and reserved reporting space. Allocation wall-time boundaries checkpoint and requeue the same job without resetting counters. Expanded-source exhaustion, a network safety ceiling or an explicit stop are reported separately.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report at its configured interval, including while queued, and on status changes. A separate session monitor queues the requested chat updates.
