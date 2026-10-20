# Native-paper collection

**Status: running** · Updated 2026-10-20T07:45:17-08:00 (fixed PST).

Continue downloading missing biological papers from the preserved identifier and exact-text deduplication ledger. Previously processed papers remain counted and are read in place. There is no fixed paper-count target or total runtime deadline; storage determines how far acquisition can continue.

Paper and token totals are cumulative across the prior run and this continuation; the continuation rows show only the additional work.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 163,149 |
| Existing papers processed | 29,404 |
| New papers processed | 18,630 |
| New papers retained by biology rules | 12,659 |
| Metadata/parse rejections | 204 |
| Candidates skipped because already present | 978 |
| Raw processed tokens | 831,178,918 |
| Exact-unique processed tokens | 831,157,985 |
| Biology-selected tokens before exact deduplication | 522,519,854 |
| Biology-selected exact-unique tokens | 522,499,003 |
| Papers processed during this continuation | 10,713 |
| Papers selected during this continuation | 7,291 |
| Raw tokens added during this continuation | 147,675,867 |
| Selected exact-unique tokens added during this continuation | 108,414,697 |
| Prior paper-run artifacts | 4.74 GiB |
| Continuation artifacts, including the copied index | 2.56 GiB |
| Combined paper-run artifacts | 7.30 GiB |
| Prior paper-run HTTP response bodies | 1.06 GiB |
| Continuation HTTP response bodies | 1.42 GiB |
| Combined paper-run HTTP response bodies | 2.48 GiB |
| Shared filesystem free space | 106.75 GiB |
| Pipeline storage including reserved reporting headroom | 20.54 GiB / 200.00 GiB |
| Counted pipeline storage | 20.52 GiB / 200.00 GiB |
| Measured HTTP response bodies | 1.42 GiB |
| HTTP budget charged | 1.42 GiB / 200.00 GiB |

Job: 243177; scheduler: RUNNING; stage: Downloading and processing missing papers.

One serial worker uses two CPU cores and zero GPUs. It preserves a shared-free-space floor of **64.00 GiB** and a total pipeline-data ceiling of **200.00 GiB**, including prior data, the copied index, new XML, parsed outputs, temporary writes and reserved reporting space. Allocation wall-time boundaries checkpoint and requeue the same job without resetting counters. Expanded-source exhaustion, a network safety ceiling or an explicit stop are reported separately.

Monitor: watching.

Since the previous successful report: +0 existing papers; +2,394 new papers; +49,138,785 raw tokens; +49,138,785 exact-unique tokens; +36,279,088 biology-selected tokens; +847,390,273 artifact bytes; +504,276,388 HTTP response bytes.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report at its configured interval, including while queued, and on status changes. A separate session monitor queues the requested chat updates.
