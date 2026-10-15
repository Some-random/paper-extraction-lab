**Executed biological-web corpus probe**

I retrieved **65,536 response-body bytes (64 KiB)** from a version-pinned FineFineWeb biology JSONL shard using a successful **HTTP 206 range request**, then reproduced parsing offline with the checked-in script. No source websites were crawled live. The first shard is **510,879,188 bytes**; it was not downloaded in full.

The prefix contains **8 complete records**, totaling **12,538 tokens according to the dataset's stored counts**, plus an incomplete terminal fragment that is excluded. The card does not identify that counting tokenizer; these are not measurements with our eventual training tokenizer. All original text stays in ignored RustFS experiment storage. The report publishes metadata, hashes and manual source-type decisions.

| Record | Original location | Stored tokens | Manual source type | Disposition for this project |
|---|---|---|---|---|
| 1 | [source URL](https://en.aazsante.fr/neurofibromatosis-symptoms-and-treatments-8670) | 761 | consumer health | Exclude from research-first pilot |
| 2 | [source URL](https://www.indonal.co.uk/produkt/indonal-man) | 765 | commercial supplement | Exclude: product promotion |
| 3 | [source URL](https://link.springer.com/article/10.1007%2Fs00253-016-7377-z) | 750 | publisher research abstract | Candidate literature; resolve DOI and deduplicate against paper corpus |
| 4 | [source URL](https://www.hindustantimes.com/health-and-fitness/go-check-do-you-have-the-binge-drinking-gene/story-6sdM5yTG0MK6FFCwaTejsN.html) | 578 | health news | Exclude from initial research-first pilot |
| 5 | [source URL](https://www.fldata.com/atp-testing-food-manu) | 658 | commercial explainer | Exclude from initial research-first pilot |
| 6 | [source URL](https://www.bkwrks.com/book/9781466582293) | 298 | book catalog | Exclude: description, not the book |
| 7 | [source URL](https://bobsdiabetes.blogspot.com/2012_01_15_archive.html) | 4518 | consumer health blog | Exclude from initial research-first pilot |
| 8 | [source URL](http://www.jove.com/keyword/endothelial+progenitor+cells) | 4210 | protocol keyword aggregation | Exclude aggregate from CPT; possible protocol URL discovery |

**What this result means**

A biology-labeled web collection is useful for discovering candidate text at scale, but contains research, news, product descriptions and consumer-health writing. One prefix record is a research abstract already accessible as literature; another aggregates protocol summaries. Deduplication and source-type selection are necessary before adding web text to our paper corpus. This sample is ordered and nonrandom; the seven exclusions are project-specific decisions, not an estimate of the collection's failure rate. **Zero records were admitted to a training dataset.**

The source `language_score` indicates language confidence, not scientific accuracy. No learned research-quality classifier, source-site crawl, GPU inference or model training ran. Initial access encountered a CDN TLS failure and the dataset preview API returned 404; a fresh resolver URL succeeded with TLS verification retained. The repeatable range script uses that route.

**Provenance and reproduction**

- Dataset: [m-a-p/FineFineWeb](https://huggingface.co/datasets/m-a-p/FineFineWeb).
- Inspected revision: `7fd92dc825a75cbff271a5a52eea0eda91a2c112`.
- File: `biology/biology_000000.jsonl`; response range `bytes 0-65535/510879188`.
- Prefix SHA-256: `c0700fce8bacb487d1ba88249f3c363cd4f18025989e0b95b42e24d13e83ae39`.
- [Complete record metadata, text hashes and manual decisions](web_sample.json).
- Local originals and parsed records: `experiments/biology_web_probe_2026-10-15/`.
- [Bounded acquisition / offline parsing script](../../scripts/sample_biology_web.py).

The actual fetch and the offline reproduction are reported separately in the JSON. To request a fresh 64KiB prefix into a new experiment directory:

```bash
.venv/bin/python scripts/sample_biology_web.py \
  --bytes 65536 --output experiments/biology_web_probe_next
```

This probe is a working acquisition diagnostic, not a comparison of extraction models or evidence that 12,538 tokens have passed training-data quality checks.
