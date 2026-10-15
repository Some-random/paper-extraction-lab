# Biomed-Enriched

[Shared literature catalog](../README.md)

Text CPT curation study

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

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
