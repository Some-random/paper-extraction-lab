# InfiMed-Foundation

[Biological pretraining review](../README.md)

Medical vision-language generalist

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

Archived reference outside the current biological pretraining review.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [InfiMed-Foundation](#token-counts-by-acquisition-route)<br>Multimodal pretraining | Corpus · text + image | 0 | 0 | ≈30B | ≈30B | [§3.1 / Pretraining](https://arxiv.org/html/2509.22261v1) |

**Multimodal pretraining — Corpus (text + image):** Section 3.1 imports public medical datasets and general multimodal datasets including DataComp, CCS, OBELICS and MMC4. The approximately 25B general and 5B medical tokens therefore belong to reused datasets; these content domains are not additional acquisition routes.

- **Online Papers: 0.** The described pretraining corpus imports datasets rather than a separate direct-paper collection.

- **Web Urls: 0.** Web-origin images/text arrive through named existing datasets, not a new direct crawl.

- **Existing Datasets: ≈30B.** General multimodal and medical datasets together. Calculation: 25000000000 + 5000000000.

- **Total: ≈30B.** Sum of the two reported approximate corpus amounts. Calculation: 25000000000 + 5000000000.

**Training stage:** Multimodal CPT and three-stage SFT

**Backbone:** 1.7B/4B foundation-model variants

**Source material and units:** Approximately 25B general multimodal plus 5B medical pretraining tokens.

**Acquisition and document processing:** Curates existing medical caption/instruction datasets rather than documenting a new full-paper PDF extraction engine.

**Cleaning and filtering:** Sample 500 examples per dataset; score accuracy, language, completeness, image relevance, and practicality from 1-5 using GPT-o3 and manual review. Reject some whole sources, including PMC-OA in this recipe.

**Training unit and mixture:** Multimodal packing toward 4,096 tokens; reduce visual tokens during CPT; three SFT stages include cross-dataset balancing.

**Generated or augmented material:** Uses curated reasoning/instruction datasets; quality scoring is distinct from reconstructing article evidence.

**Author-reported evidence:** Medical generalist evaluation and stage ablations.

**Disclosure gaps:** Discarding a particular PMC-OA image-caption dataset does not show that all PMC XML literature is poor training data. Dataset-level scoring cannot adjudicate every retained example.

**Source sections:** 3 Data collection and evaluation; 4 Training

## Primary sources

- [InfiMed-Foundation report](https://arxiv.org/html/2509.22261v1)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
