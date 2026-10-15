# BioMedLM

[Shared literature catalog](../README.md)

Biomedical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Pretraining from scratch; task-specific fine-tuning

**Backbone:** 2.7B GPT-style decoder

**Source material and units:** The Pile's PubMed abstracts and full-article subsets: 34.6B corpus tokens. Training consumes 300B tokens, or 8.67 passes.

**Acquisition and document processing:** Uses an already assembled text corpus; no newly specified PDF/OCR workflow in the model report.

**Cleaning and filtering:** Selection of biomedical Pile components and a biomedical BPE tokenizer.

**Training unit and mixture:** 1,024-token sequences; entirely biomedical pretraining rather than a general replay mix.

**Generated or augmented material:** The core pretraining dataset is source text, not teacher-written summaries of every paper.

**Author-reported evidence:** A controlled 125M tokenizer experiment reports MedQA 33.05 to 34.98 over five seeds; the full model is evaluated after task tuning.

**Disclosure gaps:** 300B is tokens consumed, not the size of a unique-paper corpus. Upstream extraction quality is not measured by the reported QA scores.

**Source sections:** 3.2 Tokenizer; 3.3 Pre-training

## Source material

[BioMedLM](https://arxiv.org/html/2403.18421v1)

| Reported field | Retained source statement |
|---|---|
| Stage | Decoder pretraining from scratch |
| Actual biological source material | The Pile's PubMed abstract and PMC full-article subsets; 34.6B corpus tokens |
| How the source becomes training data / relevant limitation | Reuses assembled text. Its 300B consumed tokens include repeated passes; no new reproducible OCR workflow is specified in the model report. |

## Datasets and amounts

[BioMedLM](https://arxiv.org/html/2403.18421v1), decoder from scratch, §3.3

| Reported field | Retained source statement |
|---|---|
| Literature contribution | The Pile's PubMed abstracts + PMC full articles: **34.6B corpus tokens combined** |
| Web / other dataset contribution | No additional general web or database corpus in pretraining |
| Quantitative limit | **300B training tokens**, **8.67 passes**. Abstract/full-text token split NR; 300B is not distinct collected text |

## Primary sources

- [BioMedLM report](https://arxiv.org/html/2403.18421v1)
- [Official checkpoint](https://huggingface.co/stanford-crfm/BioMedLM)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
