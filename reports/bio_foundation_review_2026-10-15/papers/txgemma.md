# TxGemma

[Shared literature catalog](../README.md)

Therapeutics multitask language model

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Task instruction tuning; conversational variants add general instructions

**Backbone:** Gemma 2, 2B/9B/27B

**Source material and units:** Approximately 7M training examples derived from Therapeutic Data Commons; classification, regression and generation.

**Acquisition and document processing:** Structured therapeutics tasks, not reported bulk scientific-PDF CPT.

**Cleaning and filtering:** Uses task datasets and their training partitions; not an extraction-quality recipe.

**Training unit and mixture:** Predict models are instruction tuned; Chat variants also train on general instructions.

**Generated or augmented material:** Represent biological/chemical inputs and targets as task prompts and answers.

**Author-reported evidence:** Useful example of additional biological training data; should not be cited as evidence for an OCR-then-raw-paper pipeline.

**Disclosure gaps:** A biomedical model label alone does not establish continued pretraining on full papers.

**Source sections:** Technical report: training data and model development

## Datasets and amounts

[TxGemma, April 2025 v1](https://arxiv.org/html/2504.06196v1), §2.1/2.2

| Reported field | Retained source statement |
|---|---|
| Actual training stage | **Instruction tuning**, not literature CPT |
| Literature text | Short biochemical contexts from TDC descriptions/literature; no full-paper corpus budget |
| Web / other sources and amounts | **7,080,338 training examples** across 66 TDC tasks; Predict training **67B consumed tokens / 12 epochs**. Chat mixes **30% therapeutic / 70% general instruction data** |
| Disclosure limits | Consumed tokens include repeated examples and prompting. Do not equate 67B with distinct paper text or extend the Chat mixture to Predict |

## Primary sources

- [Official technical report](https://storage.googleapis.com/research-media/txgemma/txgemma-report.pdf)
- [Official model overview](https://deepmind.google/models/gemma/txgemma/)
- [Primary source retained from the existing review](https://arxiv.org/html/2504.06196v1)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
