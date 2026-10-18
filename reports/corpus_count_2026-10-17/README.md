# Measured biological-corpus candidate tokens

Snapshot: 2026-10-17T21:52:20.058652-08:00 (fixed PST). Worker status: **running**.

Actual counts in the pinned counting tokenizer, without added special tokens. These are scanned candidate records; the full available biological corpus and its final retained total remain unmeasured.

| Content | Records scanned | Raw tokens | Tokens after exact deduplication | Complete files / inventory |
|:---|---:|---:|---:|---:|
| PMC papers (local + new XML) | 525 | 11,493,019 | 11,493,019 | 72 / 72 |
| FineFineWeb biology | 100,000 | 105,798,014 | 105,798,014 | 1 / 864 |
| TheBioCollection free-text stream | 850,146 | 844,194,374 | 843,888,793 | 0 / 32 |
| **Measured total** | **950,671** | **961,485,407** | **961,179,826** | |

## Modality partition of tokens after exact deduplication

| Explicit content | Tokens |
|:---|---:|
| protein | 34,471,826 |
| dna | 2,541,367 |
| rna | 4,820,693 |
| smiles | 30,081,667 |
| inchi | 96,747,949 |
| text or unclassified | 792,516,324 |

The modality rows sum to the deduplicated total. Only explicit sequence/molecule tags identify those spans; untagged sequences remain unclassified. Existing paper image assets remain preserved; newly acquired XML retains source media URLs while binary media are deferred. Vision-token counts are unknown.

## What this scan measures

- PMC contains the initial selected collection and any new native-XML acquisitions, not a PMC-wide count. Each paper contributes its selected text, captions/notes and tables once; chunk and interleaved copies are excluded.
- FineFineWeb is imported web-origin text; TheBioCollection is imported database-record text. Both have acquisition route `existing_datasets`. Route and content totals are alternative breakdowns of the same records.
- Deduplication compares SHA-256 after whitespace collapse across all scanned sources, preserving case and punctuation. The first record in the frozen order supplies the unique tokens. Distinct annotations survive. Near duplicates and paper versions with different text remain unresolved.
- No biology/clinical scope classifier, quality filter, new OCR or training has run. A source's biology label is not validation of every record.
- Source coverage tracks all 87 inventoried families. A database appearing inside a bundle is not a separate measured export or an additional token total.

[Counting setup and commands](../../docs/corpus_counting.md) · [Processing recipe](../bio_foundation_review_2026-10-15/data_pipeline.md)

## Paper expansion

Target: **5,000 new papers** from broad PMC topic/year searches. New papers counted: **65**. Paper phase: **acquiring_native_papers**. The native-XML phase has up to three hours and 3 GiB of downloads within the original shared run limits, followed by resumed web/database counting.

Acquired candidates excluded by explicit clinical-title checks: **6 papers / 61,951 tokens**. They remain in raw candidate counts with an exclusion status and do not count toward the selected-paper target. This title screen is not a complete biology/clinical classifier.

**Paper-count correction:** the initial 12,677,035-token local-paper count included duplicated caption/table views. The corrected 454-paper view has **10,609,606 tokens**. Original inputs and superseded ledger rows are preserved in a correction audit.

[Coverage of all 87 source families](source_coverage.md).
