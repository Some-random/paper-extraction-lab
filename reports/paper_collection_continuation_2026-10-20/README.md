# Native-paper collection

**Status: running** · Updated 2026-10-20T01:43:29-08:00 (fixed PST).

Continue downloading missing biological papers from the preserved identifier and exact-text deduplication ledger. Previously processed papers remain counted and are read in place. There is no fixed paper-count target or total runtime deadline; storage determines how far acquisition can continue.

Paper and token totals are cumulative across the prior run and this continuation; the continuation rows show only the additional work.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 153,930 |
| Existing papers processed | 29,404 |
| New papers processed | 9,442 |
| New papers retained by biology rules | 6,407 |
| Metadata/parse rejections | 102 |
| Candidates skipped because already present | 472 |
| Raw processed tokens | 704,436,508 |
| Exact-unique processed tokens | 704,415,575 |
| Biology-selected tokens before exact deduplication | 429,234,112 |
| Biology-selected exact-unique tokens | 429,213,261 |
| Papers processed during this continuation | 1,525 |
| Papers selected during this continuation | 1,039 |
| Raw tokens added during this continuation | 20,933,457 |
| Selected exact-unique tokens added during this continuation | 15,128,955 |
| Prior paper-run artifacts | 4.74 GiB |
| Continuation artifacts, including the copied index | 0.52 GiB |
| Combined paper-run artifacts | 5.25 GiB |
| Prior paper-run HTTP response bodies | 1.06 GiB |
| Continuation HTTP response bodies | 0.20 GiB |
| Combined paper-run HTTP response bodies | 1.27 GiB |
| Shared filesystem free space | 169.97 GiB |
| Pipeline storage including reserved reporting headroom | 18.49 GiB / 200.00 GiB |
| Counted pipeline storage | 18.48 GiB / 200.00 GiB |
| Measured HTTP response bodies | 0.20 GiB |
| HTTP budget charged | 0.20 GiB / 200.00 GiB |

Job: 243177; scheduler: RUNNING; stage: Downloading and processing missing papers.

One serial worker uses two CPU cores and zero GPUs. It preserves a shared-free-space floor of **64.00 GiB** and a total pipeline-data ceiling of **200.00 GiB**, including prior data, the copied index, new XML, parsed outputs, temporary writes and reserved reporting space. Allocation wall-time boundaries checkpoint and requeue the same job without resetting counters. Expanded-source exhaustion, a network safety ceiling or an explicit stop are reported separately.

Monitor: watching.

Since the previous successful report: +0 existing papers; +1,017 new papers; +20,432,065 raw tokens; +20,432,065 exact-unique tokens; +14,817,651 biology-selected tokens; +357,731,662 artifact bytes; +211,466,236 HTTP response bytes.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report at its configured interval, including while queued, and on status changes. A separate session monitor queues the requested chat updates.
