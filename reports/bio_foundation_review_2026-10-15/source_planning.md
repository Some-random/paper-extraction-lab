# Starter corpus: availability, retained tokens and storage

[Literature catalog](README.md) · [Processing recipe](data_pipeline.md)

**Working estimate: about 50B tokens in a research-focused starter pool, with a 35–70B sensitivity range.** Removing duplicates alone leaves a much broader **roughly 110–130B-token pool**, including consumer-health and clinical web text. Research selection and duplicate removal are different operations. These are explicit planning scenarios, not measured corpus yields or confidence intervals.

The starter covers three concrete blocks: the selected 55-journal PMC inventory, FineFineWeb biology, and TheBioCollection free text. General replay, instruction data, and unmeasured additions from other corpora are excluded.

## Source inventory and expected retention

Forecast columns use the existing pinned **Qwen-family extraction tokenizer**, with sample-based conversions for external token definitions. These are retained corpus tokens seen once, before training repetition.

| Source block | Source inventory | After rough deduplication, central case | After research selection and deduplication, central case | Research-pool sensitivity range |
|---|---|---:|---:|---:|
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

## Storage implied by this starter

Pinned source inventories show **15.93GB compressed** for TheBioCollection free-text files and **433.88GB** for the full FineFineWeb biology JSONL collection. These are current data-file sums, not repository-history storage. Serial shard processing avoids keeping the whole unfiltered web collection simultaneously.

The central 49.1B case needs **196GB / 183GiB as four-byte token IDs**. Probe-based UTF-8 estimates give about **143GiB of text**. Allow **500–800GiB** for selected raw inputs, canonical text, token IDs, metadata, deduplication indexes and bounded temporary outputs. This is an engineering allowance, not a measured peak; it excludes PDFs/figures, separate supplements, environments/model weights and training checkpoints.

**Preserving every paper PDF and figure needs a separate multi-TiB budget.** At the central scope-selected paper count, extrapolating the measured 454-paper sizes gives about **2.8TiB for PDFs and figures**, before XML and processed outputs. The current multi-view export layout projects to **3.6TiB for those papers alone**. Shared scratch had approximately **1.5TiB free on October 16, 2026 (PST)**. That snapshot supports a bounded text/sequence starter, but not every original asset in this larger scenario. Training deduplication does not authorize deleting preserved originals or automatically save their storage.

## Processing time and resource assumptions

**These are workload calculations with assumed throughput, not measured completion times.** The Slurm inventory lists 71 A100 80GB GPUs and eight B200 180GB GPUs; these are installed shared resources, not an allocation to this project. The CPU host has 144 logical CPUs and about 2TiB RAM. The current paper runner remains limited to two CPU threads and at most one GPU; native acquisition uses no GPU. The larger allocations below describe a possible processing campaign. No B200 speedup is assumed.

| Work | Input and calculation | Planning allowance |
|---|---|---|
| Native acquisition | About **450GB** of dataset shards plus **120GB** of candidate XML. At 20–100MB/s, transfer takes about **1.6–7.9 hours**. A serial fetcher requesting **552,024** XML objects adds **31–153 hours** if request overhead averages 0.2–1 second per object. | **2–7 days**, one serial network worker; no PDFs/figures in this timing. |
| Normalize, clean, deduplicate and tokenize | About **129B candidate tokens**, four token-equivalent passes, at an assumed aggregate **1–3M tokens/second** on **16 CPU cores**: approximately **48–144 hours**, before additional sorting/I/O/checks. | **3–10 days**, **128–256GiB RAM**, with disk-backed indexes and bounded intermediate files. The current two-thread runner is not this allocation. |
| Score paper/web candidates | About **83B candidate tokens after rough deduplication**, including text later rejected. A compact scorer at **50k–200k tokens/second/A100** costs **115–462 GPU-hours**. Database sequences and chemical records use representation-specific validity checks. | Included in the scoring allowance below. |
| Label examples and train the compact scorer | **20,000 passages × (2,048 input + 256 output tokens)**. Assuming **500–2,000 input tokens/second** and **20–80 generated tokens/second** costs **23–94 A100 GPU-hours**, plus **4–12 GPU-hours** for scorer training. Teacher size and batching must be benchmarked. | Combined labeling, scorer training and application: **150–600 A100 GPU-hours**, about **6–25 days on one GPU**. |
| Human review | **400 passages**, two independent reviewers, **2–4 minutes** per judgment, plus adjudication. Include rejected text and suspected extraction/deduplication errors. | **32–64 person-hours**. This is reviewer effort, not GPU runtime or a claim that all text is manually checked. |
| Initial mixture experiment campaign | **30 proxy runs** at 30M parameters and 3B training tokens each; then **three 7B CPT runs**, each for 1B training tokens: one baseline and two shortlisted recipes, one seed each. | Approximately **400–1,200 A100 GPU-hours** including a 25% allowance; **2–13 days with 4–8 GPUs**, excluding scheduler waits. |

Acquisition need not perform OCR when native XML is available. Dataset shard downloads take hours under these rates; the large number of serial XML requests drives the multi-day allowance. Bulk XML transfer or already cached objects could shorten it. PDF retrieval, figure preservation and OCR of papers without usable native text require a separate inventory and measured throughput before they can be added to this budget.

The mixture budget uses the approximate training-work formula **6 × parameters × training tokens**, divided by assumed effective A100 throughput. Small proxy runs assume **20–75 TFLOP/s per GPU**; sharded 7B runs assume **50–125 TFLOP/s per GPU**:

- Proxies: `30 × 6 × 30M × 3B` gives **60–225 A100 GPU-hours**.
- Target CPT comparisons: `3 × 6 × 7B × 1B` gives **280–700 A100 GPU-hours**.
- Combined, with 25% for evaluation, checkpoints and contingency: **425–1,156 GPU-hours**, rounded to **400–1,200** for planning.

The **30-run count and six candidate source/topic groups are our illustrative starting budget**. The 30M/3B proxy scale follows [OLMo 3's mixture search](https://arxiv.org/html/2512.13961v2#S3.SS4); [DCLM](https://arxiv.org/html/2406.11794v3) supports matched comparisons of processing recipes. Neither paper establishes the assumed cluster throughput or guarantees that this campaign is enough to select our final mixture. Close results require further runs or seeds, outside this initial allowance. Three target runs compare three recipes; they are not three seeds of the same recipe. Moving the target from 7B to 27B multiplies the target-run component by roughly 27/7; it does not multiply the proxy component.

The output of these experiments is a tested source/topic sampling policy, not a requirement to train once on all 49.1B retained tokens. Source-pool size, sampled training exposure and experiment budget are different quantities. Stages can overlap; implementation work, queue time, outages and the additional paper-asset/OCR workload prevent a defensible fixed end-to-end date at this point.

## Reproduction and refinement

[Scenario calculations](starter_corpus_estimate.json) · [Probe counts, versions and hashes](starter_corpus_probe.json)

Run `scripts/estimate_starter_budget.py` to reproduce the arithmetic offline from checked-in counts. `scripts/probe_starter_corpus.py` reproduces the bounded probe using `requests`, `tokenizers` and `zstandard`: one serial network/CPU worker, at most 64MiB of response bodies, with originals retained in ignored experiment storage. Cached inputs reproduce counts without network transfers.

A representative, token-weighted research-scope audit across web hosts and journals, followed by cross-source identity/hash/verified-overlap measurement, will replace the assumed retention percentages. Final counts require actual whole-corpus tokenization. This forecast is not a completed ingestion, deduplication run or learned mixture.
