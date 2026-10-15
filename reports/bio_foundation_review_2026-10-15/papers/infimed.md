# InfiMed-Foundation

[Shared literature catalog](../README.md)

Medical vision-language generalist

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

Historical medical context. Clinical-note acquisition is outside the biological research corpus scope.

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
