# BioMistral

[Shared literature catalog](../README.md)

Biomedical/medical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

Historical medical context. Clinical-note acquisition is outside the biological research corpus scope.

## Token counts by acquisition route

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [BioMistral](#token-counts-by-acquisition-route)<br>CPT | Corpus · text | 3B | 0 | 0 | 3B | [§3.1](https://arxiv.org/html/2402.10373v3) |

**CPT — Corpus (text):** The paper selects 3B tokens of raw PMC-OA article text. Its target of 1.5 epochs is not substituted for a measured consumed-token count.

- **Online Papers: 3B.** PMC-OA source articles; the source does not specify a reproducible PDF-versus-XML converter.

- **Web Urls: 0.** The reported adaptation corpus is the selected PMC-OA article text.

- **Existing Datasets: 0.** PMC-OA source acquisition is assigned to online papers; no separately curated imported training corpus is described.

- **Total: 3B.** Selected corpus, §3.1.

**Training stage:** CPT; evaluation with few-shot prompts and SFT

**Backbone:** Mistral-7B-Instruct-v0.1

**Source material and units:** 3B-token sample of the commercial-use PMC-OA subset; approximately 1.47M reported documents, 98.75% English.

**Acquisition and document processing:** Raw article text from PMC-OA; the paper does not specify a reproducible PDF-versus-XML conversion engine.

**Cleaning and filtering:** License-based selection, prioritizing non-English documents, then filling the token budget with English documents.

**Training unit and mixture:** 1.5 epochs; EOS-delimited packing into 2,048-token sequences without padding. General capability retention is also explored through weight merging with the original model.

**Generated or augmented material:** No teacher-written expansion is required for its core PMC CPT stage.

**Author-reported evidence:** Few-shot Table 2 averages: plain BioMistral 50.3 versus parent 51.2; SLERP-merged variant 55.4. Adaptation is not uniformly beneficial.

**Disclosure gaps:** The reported document count is not independently verified as distinct complete papers.

**Source sections:** 3.1-3.3; Table 2; Appendix C

## Primary sources

- [BioMistral paper](https://arxiv.org/html/2402.10373v3)
- [Author repository](https://github.com/BioMistral/BioMistral)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
