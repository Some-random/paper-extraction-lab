# Lingshu

[Shared literature catalog](../README.md)

Medical vision-language generalist

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

Historical medical context. Clinical-note acquisition is outside the biological research corpus scope.

**Training stage:** Shallow/deep alignment, SFT, RL

**Backbone:** Qwen2.5-VL 7B/32B

**Source material and units:** Collected medical image/text datasets plus synthetic caption, OCR-question, QA and reasoning data; general-domain caption/instruction data are mixed in.

**Acquisition and document processing:** PMC-derived image-caption datasets are training sources; its synthetic OCR examples are rendered questions, not a bulk article-PDF extraction recipe.

**Cleaning and filtering:** Remove images below 64 pixels; perceptual-hash duplicate filtering; caption length 10-1,024 tokens; MinHash-LSH instruction deduplication; evaluation overlap exclusion.

**Training unit and mixture:** Staged alignment before end-to-end instruction tuning.

**Generated or augmented material:** GPT-4o writes captions/QA/reasoning; Gemini reasoning answers must match known exam answers before 50K rendered OCR examples are retained.

**Author-reported evidence:** Broad medical VQA, text QA and report generation evaluations.

**Disclosure gaps:** Reasoning-answer consistency does not independently validate every intermediate claim. Clinical image results do not rank biological literature understanding.

**Source sections:** 2.1-2.3; Table 5

## Primary sources

- [Lingshu report](https://arxiv.org/html/2506.07044v1)
- [Author release organization](https://huggingface.co/lingshu-medical-mllm)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
