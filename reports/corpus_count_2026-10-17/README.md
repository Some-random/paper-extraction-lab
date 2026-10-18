# Measured biological-corpus candidate tokens

Snapshot: 2026-10-17T20:54:38.389361-08:00 (fixed PST). Worker status: **running**.

Actual counts in the pinned counting tokenizer, without added special tokens. These are scanned candidate records; the full available biological corpus and its final retained total remain unmeasured.

| Content | Records scanned | Raw tokens | Tokens after exact deduplication | Complete files / inventory |
|:---|---:|---:|---:|---:|
| PMC local biology papers | 454 | 12,677,035 | 12,677,035 | 1 / 1 |
| FineFineWeb biology | 100,000 | 105,798,014 | 105,798,014 | 1 / 864 |
| TheBioCollection free-text stream | 301,500 | 299,316,189 | 299,270,025 | 0 / 32 |
| **Measured total** | **401,954** | **417,791,238** | **417,745,074** | |

## Modality partition of tokens after exact deduplication

| Explicit content | Tokens |
|:---|---:|
| protein | 12,292,583 |
| dna | 907,008 |
| rna | 1,714,216 |
| smiles | 10,683,482 |
| inchi | 34,327,520 |
| text or unclassified | 357,820,265 |

The modality rows sum to the deduplicated total. Only explicit sequence/molecule tags identify those spans; untagged sequences remain unclassified. Image pixels are retained in existing paper assets; vision-token counts are unknown.

## What this scan measures

- PMC is the frozen local collection, not a PMC-wide count. Each paper contributes its selected text, captions/notes and tables once; chunk and interleaved copies are excluded.
- FineFineWeb is imported web-origin text; TheBioCollection is imported database-record text. Both have acquisition route `existing_datasets`. Route and content totals are alternative breakdowns of the same records.
- Deduplication compares SHA-256 after whitespace collapse across all scanned sources, preserving case and punctuation. The first record in the frozen order supplies the unique tokens. Distinct annotations survive. Near duplicates and paper versions with different text remain unresolved.
- No biology/clinical scope classifier, quality filter, new OCR or training has run. A source's biology label is not validation of every record.
- Source coverage tracks all 87 inventoried families. A database appearing inside a bundle is not a separate measured export or an additional token total.

[Counting setup and commands](../../docs/corpus_counting.md) · [Processing recipe](../bio_foundation_review_2026-10-15/data_pipeline.md)

[Coverage of all 87 source families](source_coverage.md).
