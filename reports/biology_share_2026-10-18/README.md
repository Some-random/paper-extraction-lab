# Biological share of existing web data

A stratified random sample covers all 234 shards of the larger local cache and all 14 shards of the smaller copy. 493 full documents were readable and reviewed; 31 selected locations failed to decode. The results below count tokens in biology-focused documents, before quality filtering and deduplication.

## Token shares in readable content

| Local corpus | Biology | Clinical / health | Mixed / uncertain | Other |
|:---|---:|---:|---:|---:|
| SmolLM FineWeb-Edu-Dedup | 12.2% (6.0–18.5%) | 16.6% (11.4–21.7%) | 7.1% (0.8–13.3%) | 64.1% (55.9–72.4%) |
| FineWeb-Edu 10BT | 10.9% (2.0–19.9%) | 16.6% (3.0–30.3%) | 23.7% (0.0–58.9%) | 48.7% (21.0–76.4%) |

Parentheses show approximate 95% sampling intervals. All values use the same pinned counting tokenizer.

## Estimated biological token amounts

| Source frame | Reviewed / selected documents | Estimated biology tokens |
|:---|---:|---:|
| SmolLM FineWeb-Edu-Dedup, readable domain | 437 / 468 | 22.9B (10.2–35.6B) |
| FineWeb-Edu 10BT, readable domain | 56 / 56 | 1.1B (0.4–1.7B) |
| Larger cache, 200 allocation-eligible shards only | 400 / 400 | 19.0B (7.3–30.7B) |

**The corpora overlap: do not add their token estimates.** The source-provided published 220B total is not treated as a verified, fully readable local corpus.

## Local cache completeness

The larger cache has 234 filenames and 550.1 GB of apparent file sizes, but some selected data-page headers are zero-filled and cannot be decoded. The 31 failed sampled locations span 23 files. These remain in the original probability sample with zero contributions to the readable-content domain; they are not classified as other. Separately, a metadata rule fixed before annotation identifies 200 shards with at least 99% allocation (469.8 GB apparent size). All 400 selected records in that subset decoded. This is a subset check, not full-file integrity verification.

## How the estimate was made

- Random seed 2026101801; two uniform rows without replacement per large-corpus shard and four per small-corpus shard. Shard row counts and selected row indices come from frozen Parquet metadata.
- Every readable document received a semantic primary label: biology, clinical/health, other or mixed. Biology includes biological education and mechanisms; patient care, clinical outcomes and health advice are separate.
- A blind second model review checked 60 records; the 1 observed label disagreement was adjudicated. A further 7 high-influence documents received independent review, with 2 further disagreements adjudicated. These are model/assistant judgments, not human expert annotations.
- Weight each observation by shard rows divided by sampled rows. Estimate totals with these weights and token shares as ratios of weighted token totals. Intervals use stratified finite-population variance and a delta-method ratio approximation.
- Mixed-inclusive results, source-token counts, missing-data sensitivity and the allocation-eligible subset are recorded in the summary. Mixed is definition uncertainty; sampling intervals do not include systematic annotation error.
- This measures domain share, not scientific correctness, training usefulness or final retained tokens. No new corpus downloads, cluster GPU jobs or model training were needed.

[Sample measurements and labels](observations.csv) · [Sampling code](../../scripts/sample_cluster_biology_share.py) · [Estimator](../../src/biology_share.py)
