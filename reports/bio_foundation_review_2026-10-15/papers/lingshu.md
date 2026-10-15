# Lingshu

[Biological pretraining review](../README.md)

Medical vision-language generalist

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

Archived reference outside the current biological pretraining review.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [Lingshu](#token-counts-by-acquisition-route)<br>Shallow/deep alignment, SFT, RL | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2506.07044v1) |

**Shallow/deep alignment, SFT, RL — Not reported (text):** Counts of image-caption, QA and reasoning examples cannot be converted to tokenizer tokens without the actual sequences.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

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
