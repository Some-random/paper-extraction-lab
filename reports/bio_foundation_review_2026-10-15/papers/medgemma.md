# MedGemma

[Shared literature catalog](../README.md)

Medical vision-language generalist

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

Historical medical context. Clinical-note acquisition is outside the biological research corpus scope.

## Token counts by acquisition route

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [MedGemma](#token-counts-by-acquisition-route)<br>Vision enhancement, pretraining, teacher distillation, RL | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2507.05201v3) |

**Vision enhancement, pretraining, teacher distillation, RL — Not reported (text):** The source reports image/sample counts, including PMC figure-caption samples; these are not token counts. The medical/general token split is not disclosed here.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Training stage:** Vision enhancement, pretraining, teacher distillation, RL

**Backbone:** Gemma 3 family

**Source material and units:** Medical imaging/report pairs and medical QA, with original SigLIP/Gemma general mixtures for replay. Table 1 lists 41,853 PMC single-panel image-caption examples.

**Acquisition and document processing:** PMC contributes figure-caption data, not a stated OCR pass over every full article.

**Cleaning and filtering:** Restrict PMC-OA component to single-panel medical images; exclude PathVQA/MedVQA for identified quality issues.

**Training unit and mixture:** Joint medical/general multimodal training; medical image and text capabilities are developed across distinct stages.

**Generated or augmented material:** Large instruction-tuned teacher supplies responses/logits; approximately 200K synthetic medical questions generated using five seed questions per prompt.

**Author-reported evidence:** Medical QA, imaging/report generation and clinical-text evaluations; these do not establish full scientific-PDF extraction accuracy.

**Disclosure gaps:** Internal image data and teacher details prevent full end-to-end reproduction. This entry is not a review of every later MedGemma version.

**Source sections:** 2 Data; 3 Model development; Table 1

## Primary sources

- [MedGemma technical report](https://arxiv.org/html/2507.05201v3)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
