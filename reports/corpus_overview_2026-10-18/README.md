# Biological training data: what we have and what is available

October 18, 2026. **Our pilot has counted 4.962B candidate tokens. Existing cluster web data contains an estimated 22.9B biology-focused tokens, alongside additional uncounted papers and databases. The three quantified online collections support a planning scenario of about 254B candidate tokens.** These amounts overlap and cannot be added into a unique biological total.

M = million; B = billion. GB and TB are decimal storage units; GiB and TiB are binary units. Unless explicitly marked as source-reported units, token amounts use the same pinned Qwen-family counting tokenizer.

## Overall inventory

| Availability | Collection / content | Tokens | Storage |
|:---|:---|:---|:---|
| **Our pilot** | **All counted sources, after exact deduplication** | **4.962B candidates** | **13.66 GB** across the counting run and initial paper collection, including outputs and indexes |
| Our pilot, included above | 2,327 selected papers | 36.1M | 5.32 GB in paper run directories; initial PDFs/figures retained, expansion mainly XML/text |
| Our pilot, included above | FineFineWeb biology: 400,000 web documents | 421.8M | 2.04 GB raw JSONL |
| Our pilot, included above | TheBioCollection: 4.54M scanned database records | 4.504B after exact deduplication | 1.99 GB compressed input; fourth downloaded shard partly counted |
| **Already on cluster** | **SmolLM FineWeb-Edu-Dedup: biology-focused documents within the general web cache** | **22.9B estimated; 95% sampling interval 10.2–35.6B** | **550.07 GB apparent cache size**, across subjects; some sampled pages are unreadable |
| Already on cluster | FineWeb-Edu 10BT: biology-focused subset | 1.05B estimated; interval 0.45–1.65B; overlaps the larger cache | 28.52 GB full cache, across subjects |
| Already on cluster | PMC / Europe PMC paper XML cache: 26,303 files | Uncounted | 4.17 GB XML |
| Already on cluster | Older PubMed/PMC article corpus | Uncounted | 3.17 GB compressed |
| Already on cluster | PubMed sentence/relation annotations; another view of the older corpus | Uncounted; overlapping article content | 2.03 GB compressed |
| Already on cluster | Filtered PubMed abstracts | Uncounted | 0.229 GB TSV |
| Already on cluster | Older parsed literature sentences | Uncounted; biological scope unresolved | 8.65 GB SQL |
| Already on cluster | UniProt annotation export: protein names, organisms, genes, GO and taxonomy | Uncounted | 0.531 GB TSV |
| Already on cluster | UniRef50 / UniRef90: protein annotations and sequences, release 2024_02 | Uncounted; resolutions overlap | 32.88 / 69.38 GB compressed XML |
| Already on cluster | Biomni: 103 biological tables, ontologies and experimental files | Uncounted; mixed tables, measurements and descriptions | 31.36 GB |
| Already on cluster | Biological networks: 37 gene/protein/pathway payloads | Uncounted; graph records require serialization | 26.99 GB |
| Already on cluster, secondary priority | UniRef50/90/100 protein FASTA | Uncounted; overlapping sequence representations | 164.99 GB compressed, combined |
| **Listed cluster stores above** | **File footprint, excluding our pilot** | **Unique biology total unmeasured** | **922.98 GB apparent bytes**; includes overlapping representations |
| On cluster, conditional reuse | Web of Science abstracts / PaleoDeepDive papers, figures and SQL | Uncounted; biological subset also unresolved | 14.28 GB abstracts / paper collection not fully inventoried |
| **Full online collection** | **PMC text-mining candidates** | **127.2B candidate scenario** | **About 1.28 TB XML**; about **3.01 TB** with parsed/canonical copies and uint32 token IDs |
| Full online collection | FineFineWeb biology: 864 shards | 89.75B candidate scenario; publisher reports 86.99B in its tokenizer | 433.88 GB raw; about 792.89 GB raw + token IDs |
| Full online collection | TheBioCollection free-text: 32 shards of biological descriptions, annotations, sequences and molecules | 36.99B candidate scenario; publisher reports 33.8B in its tokenizer | 15.93 GB compressed; about 163.88 GB raw + token IDs |
| **These three full collections** | **PMC + FineFineWeb + TheBioCollection** | **253.93B candidate scenario, before cross-source deduplication and scope/quality filtering** | **About 3.97 TB** for source/native artifacts + IDs; reserve **4–5 TiB working capacity** |
| Broader online pool | OLMo 3 / olmOCR scientific PDFs, across subjects | 972B source-reported tokens; biological share unmeasured | Not inventoried here |
| Broader online pool, secondary priority | OpenGenome2 genomic sequence collection | 8.8T reported nucleotide positions; common text-tokenizer count unknown | Not inventoried here |
| Other registered sources | Remaining contributions across the complete 87-family source register | Additional unique biological tokens unmeasured | Not fully inventoried |

**Storage already found is not storage still needed.** The 922.98 GB is held in existing cluster locations and can be read in place. It is a subtotal of the listed stores, not a census of every cluster disk. The larger web cache's apparent size includes incomplete payloads; its allocated blocks occupy about 510.40 GB. The web-storage cells describe whole mixed-domain caches, not isolated biological subsets. Additional NCBI genomic FASTA, indexed UniRef copies and older project experiments are outside this subtotal.

The 13.66 GB pilot footprint includes about 8.93 GB in the counting run plus 4.73 GB in its initial paper collection. Source rows omit shared counting indexes and other run files, so their storage cells do not sum to the total. Environments, model caches and older experiments are excluded. Four-byte IDs for the pilot's counted tokens would occupy another 19.85 GB if written; that packed copy has not been created.

## How much is biological text?

The pilot's **4.962B** contains **4.064B text or unclassified tokens** and **0.898B explicitly tagged protein, DNA, RNA, SMILES and InChI tokens**. Untagged sequence content may remain unclassified. TheBioCollection's full-release estimate likewise includes sequences and molecular representations; a complete modality split is not yet counted. Neither total is a verified amount of retained biological prose.

The cluster web estimate counts whole biology-focused documents and keeps clinical/health and mixed documents separate. A stratified random sample selected 524 locations; 493 full documents were readable and reviewed. Labels are assistant judgments, not human expert annotation. The intervals describe sampling uncertainty and exclude systematic labeling error. The 22.9B estimate covers currently readable content; it does not project onto an assumed complete 220B-token cache. [Biological-share measurements](../biology_share_2026-10-18/README.md).

## What the full collection would require

**The defensible quantified planning subtotal is about 254B candidate tokens, with 4–5 TiB of working storage for those three collections.** It does not establish 254B usable biological tokens or a complete ceiling on available data. The paper scenario scales the selected-paper mean to the PMC inventory; the two released-dataset scenarios scale completed prefix shards by exact release bytes. These are planning assumptions, not representative retention estimates.

Our pilot is nested inside these online collections. The two cluster web caches overlap each other and can overlap FineFineWeb. Paper imports, UniRef representations and TheBioCollection's upstream databases overlap as well. A unique biological grand total requires counting and cross-source deduplication; unknown contributions remain unknown rather than zero.

**Current shared scratch free space: about 584 GiB at this check**, shared with other users and not reserved. The 4–5 TiB allowance covers text/record preparation, including one uint32 ID copy, indexes and working room. It excludes model weights/checkpoints, the separate large cluster web cache, raw genomic expansion, full PDFs, figure binaries and supplements. PDF/figure retention at full PMC scale would require a much larger budget.

[Measured pilot](../corpus_count_2026-10-17/README.md) · [Storage calculations and pinned releases](../corpus_count_2026-10-17/capacity_plan.md) · [Complete source register](../bio_foundation_review_2026-10-15/source_inventory.md) · [Processing recipe](../bio_foundation_review_2026-10-15/data_pipeline.md).

Full-release sources: [PMC distribution](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/), [FineFineWeb](https://huggingface.co/datasets/m-a-p/FineFineWeb), [TheBioCollection](https://huggingface.co/datasets/trillionlabs/TheBioCollection), [OLMo 3 science data](https://arxiv.org/html/2512.13961v2#S3.SS4), [OpenGenome2](https://huggingface.co/datasets/arcinstitute/opengenome2). Web of Science and PaleoDeepDive have explicit local reuse conditions and are not included in the reusable subtotal. Source files elsewhere on the cluster remain unmodified.
