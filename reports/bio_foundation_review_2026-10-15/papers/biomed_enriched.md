# Biomed-Enriched

[Biological pretraining review](../README.md)

Text CPT curation study

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Continued pretraining. **Starting checkpoint:** OLMo2-7B-stage1. [Initialization evidence](https://arxiv.org/html/2506.20331v1)

Curation variants are compared at the same 33.6B-token CPT budget. Clinical filtering results are source findings, not a prescription for a biology corpus.

**Data included in the overview amounts:** Biomedical paper text. PMC literature and its biomedical/clinical curation variants; this does not establish a research-biology-only token count.

## Authors and institutions

**Authors:** Rian Touchent; Nathan Godey; Eric de la Clergerie.

**Institutions:** Sorbonne Université; Inria Paris.

[Paper attribution](https://arxiv.org/html/2506.20331v1). Names and affiliations follow the reviewed paper version.

<a id="evidence-assessment"></a>

## Overall paper assessment

**Overall: Solid.** A solid, focused data-curation paper. Its controlled design and practical recipe are valuable, while modest average gains and biomedical-specific quality labels limit the breadth of its conclusions. This is our provisional technical judgment of the whole paper in its publication context, not an official review score or an independent replication.

**Contribution and originality:** A useful systematic application of paragraph labels, filtering and enrichment; mostly incremental rather than a new model principle.

**Technical soundness:** A coherent pipeline with comparable starting checkpoints and token budgets across variants.

**Evaluation:** Multiple variants expose tradeoffs; the small overall mean gain does not support a universally superior filter.

**Reproducibility:** The source data, labeling recipe and training budget are described; teacher-label quality is not human scientific validation.

**Clarity and limitations:** The pipeline is clear, but clinical and educational labels need contextual interpretation.

Sources: [Reviewed paper: methods/results/limitations](https://arxiv.org/html/2506.20331v1)

## Paper-text origins

**Direct paper sources:** PMC-OA XML.

**Paper text via reused datasets:** No reused paper-text source established for this row.

The study parses PMC Open Access XML directly and compares paragraph-level curation variants. [Source](https://arxiv.org/html/2506.20331v1)

## Other modalities

The reviewed training stage uses ordinary text rather than separately represented images, biological sequences or 3D structure tokens.

Sources: [Reviewed paper: data and representations](https://arxiv.org/html/2506.20331v1)

## Existing-dataset sources

No separately reused dataset identified for this overview row.

Named reused inputs relevant to the reviewed training stages. This is not necessarily exhaustive. A source name establishes provenance, not its token amount; unreported amounts remain NR. Directly collected PubMed/PMC text is described separately as online-paper input. [Source](https://arxiv.org/html/2506.20331v1)

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [Biomed-Enriched](#token-counts-by-acquisition-route)<br>Controlled CPT: each variant | Training exposure · text | 33.6B | 0 | 0 | 33.6B | [§3–4 / Table 2](https://arxiv.org/html/2506.20331v1) |

**Controlled CPT: each variant — Training exposure (text):** Each controlled variant receives 33.6B tokens from processed PMC-OA XML. This is per variant, not a sum over variants or the size of 4.5M original articles.

- **Online Papers: 33.6B.** Source-native PMC-OA article text, after the variant-specific curation.

- **Web Urls: 0.** The described controlled domain stream is PMC-OA article text.

- **Existing Datasets: 0.** The reviewed study parses source PMC-OA XML rather than importing a separately curated text corpus.

- **Total: 33.6B.** Fixed per-run training exposure.

**Training stage:** Controlled OLMo2-7B-stage1 CPT

**Backbone:** OLMo2-7B-stage1

**Source material and units:** Approximately 4.5M PMC-OA XML articles; 133M paragraphs after processing, minimum 64 tokens.

**Acquisition and document processing:** Explicit native XML parsing, without re-OCRing those articles.

**Cleaning and filtering:** Llama-3.1-70B labels 400K paragraphs for domain, type, educational quality and language; distill into XLM-RoBERTa-base. Educational subset keeps scores >=3/5.

**Training unit and mixture:** Equal 33.6B-token runs, 8,192-token context. Compare baseline, paragraph filtering, 10x clinical/case/language upsampling, metadata prefixes and combinations.

**Generated or augmented material:** Teacher-generated labels guide selection; original article text remains the training content.

**Author-reported evidence:** Table 3: BE-All mean 61.08 versus BE-Base 60.41 (+0.67 pp); BE-Clinical Professional Medicine 63.97 versus 59.93 (+4.04 pp); BE-Educational MedMCQA +1.17 pp.

**Disclosure gaps:** Clinical and educational variants do not improve every benchmark or overall average. LLM-label agreement is not human gold; no universal best filter is established.

**Source sections:** 3.1-3.3; 4; Table 3

## Primary sources

- [Biomed-Enriched paper](https://arxiv.org/html/2506.20331v1)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
