# Available corpus and overall storage

[Literature catalog](README.md) · [Processing recipe](data_pipeline.md)

**Working estimate: about 50B tokens in a research-focused starter pool, with a 35–70B sensitivity range.** Removing duplicates alone leaves a much broader **roughly 110–130B-token pool**, including consumer-health and clinical web text. Research selection and duplicate removal are different operations. These are explicit planning scenarios, not measured corpus yields or confidence intervals.

## Paper coverage and dataset scope

**55 is the number of journals, not papers.** That initial journal inventory contains **552,024 candidate papers**. The broader [PMC inventory](../pmc_global_availability_2026-10-14.json), checked on October 14, contains **9,324,889 XML/text-mining candidates**. The journal subset is contained in this larger pool. We can collect beyond those journals; there is no 55-journal cap on the planned corpus.

The 49.1B central estimate below quantifies the initial journal subset plus two imported datasets. The additional research-biology yield from wider PMC coverage remains unmeasured; the inventory also includes clinical material and other subjects. Candidate counts do not certify that every object is downloadable. Other paper collections, including peS2o and S2ORC, can extend coverage, with their additional contribution counted after overlap is measured.

**FineFineWeb biology** is the biology portion of a released web-text dataset. **TheBioCollection** is a released collection of biological database records drawn from sources such as UniProt and PubChem, containing sequences, molecular representations, descriptions and annotations. Here we use its free-text stream, not its separate instruction stream.

General-text replay, instruction data and unmeasured additions from other corpora are excluded from the quantified estimate.

## Source inventory and expected retention

Forecast columns use the existing pinned **Qwen-family extraction tokenizer**, with sample-based conversions for external token definitions. These are retained corpus tokens seen once, before training repetition.

| Source block | Available inventory | After rough<br>deduplication | After research<br>selection + deduplication | Research-pool<br>range |
|:---|:---|---:|---:|---:|
| Direct paper text | **552,024 XML candidates** in the selected journal union | **6.0B** | **4.2B** | **1.8–11.0B** |
| Web-origin text imported from FineFineWeb | **86.99B source-counted tokens**; about **85.7B** after tokenizer conversion | **77.2B** | **11.6B** | **3.6–20.4B** |
| Database records imported from TheBioCollection | **33.8B Gravity-tokenizer free-text tokens**; about **37.0B** after conversion | **33.3B** | **33.3B** | **29.6–35.2B** |
| **Total** | | **116.5B** | **49.1B** | **35.0–66.6B** |

The [October 13 PMC inventory](../pmc_cns_availability_2026-10-13/availability.json) precedes biology/article-type filtering and object verification. The [whole-PMC inventory](../pmc_global_availability_2026-10-14.json) contains 9.32M XML candidates; it is an expansion option containing this journal subset, not a separate additive pool.

FineFineWeb's [author card](https://huggingface.co/datasets/m-a-p/FineFineWeb) supplies its biology total and describes upstream exact/MinHash deduplication. We assume only **additional** removal within our inputs and across routes. TheBioCollection's [author card](https://huggingface.co/datasets/trillionlabs/TheBioCollection) distinguishes **33.8B free-text tokens** from **18.9B instruction tokens**. The free-text stream contains sequences, molecular representations, database annotations and tool-computed descriptions; its full size is not a pure sequence count.

## Assumptions behind the forecast

| Quantity | Low | Central | High |
|---|---:|---:|---:|
| Tokens per paper | 8,000 | 12,000 | 23,334 |
| Paper tokens retained after research-scope selection | 50% | 70% | 90% |
| Paper tokens retained after additional deduplication | 80% | 90% | 95% |
| FineFineWeb biology tokens retained after research-scope selection | 5% | 15% | 25% |
| Web tokens retained after additional deduplication | 85% | 90% | 95% |
| Database-record tokens retained after additional deduplication | 80% | 90% | 95% |

**Selection and deduplication percentages are assumptions, not observed success rates.** In particular, no representative measurement establishes that 15% of FineFineWeb biology is suitable research content. The wide range exposes that uncertainty. Our web probe calibrates tokenization only; it does not establish research yield. Database records are assumed within research scope for this estimate; further validity/provenance filtering reduces that row.

The 454-paper batch averages 23,334 extracted tokens per paper. Those journal-balanced, length-capped, citation-expanded papers are not representative of the full inventory. We therefore use an assumed 12,000 tokens centrally rather than extrapolating their mean universally.

Central calculations:

- **Papers:** 552,024 × 12,000 × 70% scope retention × 90% dedup retention = **4.17B**.
- **Web:** 86.99B × 0.9857 tokenizer conversion × 15% scope retention × 90% dedup retention = **11.58B**.
- **Database records:** 33.8B × 1.0957 tokenizer conversion × 90% dedup retention = **33.33B**.

## Acquisition categories and actual modalities

In the central research case, direct paper acquisition supplies **4.2B tokens (8.5%)**. Existing datasets supply **44.9B (91.5%)**: **11.6B web-origin text** plus **33.3B database records**. New direct web crawling supplies **0 tokens** in this initial plan. Imported webpage text retains its web origin while remaining an existing-dataset acquisition.

A bounded probe inspected **2,048 free-text records across prefixes of all 32 TheBioCollection shards** and **108 FineFineWeb records across eight shard prefixes**. Both Gravity and the pinned local tokenizer counted the database records; the web comparison used stored token counts. Input reads totaled about **25MB**, including a tokenizer file. No full shard, model weights, model inference or training was run.

**Prefixes are convenience samples.** They establish neither population proportions nor whole-corpus duplicate rates. This modality projection is conditional on their token proportions being representative and retention affecting those portions similarly:

| What the model reads | Central token projection | Share of the same 49.1B pool |
|---|---:|---:|
| Paper/web prose, database descriptions, annotations and remaining text | **42.4B** | **86.3%** |
| Tagged protein sequences | **1.5B** | **3.0%** |
| Tagged DNA/RNA sequences | **0.25B** | **0.5%** |
| Tagged SMILES/InChI | **5.0B** | **10.2%** |

These are the same records as the source table; do not add modality counts to source counts. Untagged sequence strings in paper/web prose are not separately identified. The database probe found protein sequences at 4.4% and DNA/RNA sequences at 0.75% of its token positions. Protein-domain records contain substantial additional annotations. Different sampling or additional raw UniRef/RNAcentral would change this mix. Available-pool shares do not prescribe training sampling weights.

## Preventing double counting

- PMC, S2ORC, peS2o and Dolma academic text can contain the same works. The estimate grants **zero unmeasured incremental tokens** to the latter three. Count their new contributions only after identifier/content matching.
- TheBioCollection already uses UniProt, PubChem and other databases. Do not add their complete raw exports again. Distinct new sequences, measurements and annotations can contribute after representation-aware comparison.
- NatureLM/BioMatrix training budgets do not establish an equally sized downloadable corpus available to us.
- Resolve web publication mirrors to the literature identity index. Similar entities with different useful annotations or relations are not generic duplicate text.

## Overall storage

**Reserve approximately 4TiB for the quantified initial corpus, including preserved paper PDFs and figures.** Its combined working estimate is **3.3–3.6TiB**. This is a capacity estimate for the initial subset and two datasets; extending paper coverage requires more space.

| Included material | Basis of the estimate |
|:---|:---|
| Original paper PDFs and figures | Approximately 2.8TiB for the central scope-selected paper set, extrapolated from 454 local papers. |
| XML, dataset text, token IDs, metadata, indexes and bounded working files | 500–800GiB allowance, including about 183GiB of token IDs and 143GiB of canonical text. |
| **Combined working estimate** | **3.3–3.6TiB; round up to a 4TiB initial allocation.** |

The two components are included in the combined total, not additional to it. The estimate excludes separately downloaded supplements, model weights, environments and training checkpoints. It assumes serial dataset-shard processing rather than keeping every unfiltered shard and every intermediate representation at once.

**For expansion, budget roughly 7.2TiB of PDFs and figures per additional million retained papers**, before their XML, extracted text and indexes. This scales the measured file sizes, not the biological yield of the broader 9.32M-candidate inventory. File sizes can vary by journal and article type. Training-text deduplication does not remove the obligation to preserve originals.

For reproducibility, the source inventories contain **15.93GB compressed** of TheBioCollection free-text files and **433.88GB** of FineFineWeb biology JSONL. Keeping the current redundant multi-view paper export layout would use more space than the canonical-text design assumed above. Shared scratch had approximately **1.4TiB free on October 16, 2026 (PST)**, below the proposed 4TiB initial allocation.

## Reproduction and refinement

[Scenario calculations](starter_corpus_estimate.json) · [Probe counts, versions and hashes](starter_corpus_probe.json)

Run `scripts/estimate_starter_budget.py` to reproduce the arithmetic offline from checked-in counts. `scripts/probe_starter_corpus.py` reproduces the bounded probe using `requests`, `tokenizers` and `zstandard`: one serial network/CPU worker, at most 64MiB of response bodies, with originals retained in ignored experiment storage. Cached inputs reproduce counts without network transfers.

A representative, token-weighted research-scope audit across web hosts and journals, followed by cross-source identity/hash/verified-overlap measurement, will replace the assumed retention percentages. Final counts require actual whole-corpus tokenization. This forecast is not a completed ingestion, deduplication run or learned mixture.
