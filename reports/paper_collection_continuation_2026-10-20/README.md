# Native-paper collection

**Status: running** · Updated 2026-10-20T03:44:11-08:00 (fixed PST).

Continue downloading missing biological papers from the preserved identifier and exact-text deduplication ledger. Previously processed papers remain counted and are read in place. There is no fixed paper-count target or total runtime deadline; storage determines how far acquisition can continue.

Paper and token totals are cumulative across the prior run and this continuation; the continuation rows show only the additional work.

| Measure | Current amount |
|:--|--:|
| Existing native XML available | 29,414 papers |
| Known PMC identifiers checked before acquisition | 156,330 |
| Existing papers processed | 29,404 |
| New papers processed | 11,833 |
| New papers retained by biology rules | 8,033 |
| Metadata/parse rejections | 132 |
| Candidates skipped because already present | 608 |
| Raw processed tokens | 737,432,060 |
| Exact-unique processed tokens | 737,411,127 |
| Biology-selected tokens before exact deduplication | 453,438,343 |
| Biology-selected exact-unique tokens | 453,417,492 |
| Papers processed during this continuation | 3,916 |
| Papers selected during this continuation | 2,665 |
| Raw tokens added during this continuation | 53,929,009 |
| Selected exact-unique tokens added during this continuation | 39,333,186 |
| Prior paper-run artifacts | 4.74 GiB |
| Continuation artifacts, including the copied index | 1.06 GiB |
| Combined paper-run artifacts | 5.79 GiB |
| Prior paper-run HTTP response bodies | 1.06 GiB |
| Continuation HTTP response bodies | 0.52 GiB |
| Combined paper-run HTTP response bodies | 1.59 GiB |
| Shared filesystem free space | 154.10 GiB |
| Pipeline storage including reserved reporting headroom | 19.03 GiB / 200.00 GiB |
| Counted pipeline storage | 19.02 GiB / 200.00 GiB |
| Measured HTTP response bodies | 0.52 GiB |
| HTTP budget charged | 0.52 GiB / 200.00 GiB |

Job: 243177; scheduler: RUNNING; stage: Downloading and processing missing papers.

One serial worker uses two CPU cores and zero GPUs. It preserves a shared-free-space floor of **64.00 GiB** and a total pipeline-data ceiling of **200.00 GiB**, including prior data, the copied index, new XML, parsed outputs, temporary writes and reserved reporting space. Allocation wall-time boundaries checkpoint and requeue the same job without resetting counters. Expanded-source exhaustion, a network safety ceiling or an explicit stop are reported separately.

Monitor: watching.

Since the previous successful report: +0 existing papers; +1,626 new papers; +32,995,552 raw tokens; +32,995,552 exact-unique tokens; +24,204,231 biology-selected tokens; +578,326,410 artifact bytes; +343,772,137 HTTP response bytes.

Original XML is read in place when already present. New XML, structured sections, tables, captions, citation metadata and canonical text are retained. Exact-text duplicate removal and the initial biology selection are reported separately; biology selection is a keyword heuristic, not a reviewed quality score. Counts use the pinned extraction-reference tokenizer.

Identifier checks cover the inventoried accessible cluster sources. Figures, PDFs, supplements and genomic downloads are outside this batch.

An independent monitor refreshes this report at its configured interval, including while queued, and on status changes. A separate session monitor queues the requested chat updates.
