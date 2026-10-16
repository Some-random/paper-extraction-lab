# BioMedLM

[Biological pretraining review](../README.md)

Biomedical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Pretraining from scratch. **Starting checkpoint:** Random weights; 2.7B GPT-style decoder. [Initialization evidence](https://arxiv.org/html/2403.18421v1)

Trained on the PubMed components of The Pile. The 34.6B-token corpus is consumed for 8.67 passes, totaling 300B training tokens.

**Data included in the overview amounts:** Biomedical papers. The corpus consists of The Pile PubMed Abstracts/PubMed Central components. This is a biomedical-literature count; it does not isolate nonclinical biological research.

## Authors and institutions

**Authors:** Elliot Bolton; Abhinav Venigalla; Michihiro Yasunaga; David Hall; Betty Xiong; Tony Lee; Roxana Daneshjou; Jonathan Frankle; Percy Liang; Michael Carbin; Christopher D. Manning.

**Institutions:** Stanford University; Databricks.

[Paper attribution](https://arxiv.org/html/2403.18421v1). Names and affiliations follow the reviewed paper version.

<a id="evidence-assessment"></a>

## Overall paper assessment

**Overall: Solid.** A solid and transparent model/resource report. It demonstrates the practicality of a smaller specialized model and describes its budget clearly, but the methodological contribution and controlled evidence at the headline model scale are limited. This is our provisional technical judgment of the whole paper in its publication context, not an official review score or an independent replication.

**Contribution and originality:** Offers an openly inspectable specialized model and a useful study of scale and domain tokenization.

**Technical soundness:** The architecture and training recipe are conventional and sufficiently concrete.

**Evaluation:** The five-seed tokenizer study is useful but smaller than the headline model; most full-model results follow task tuning.

**Reproducibility:** Corpus and consumed-token totals, training settings and released weights are useful for reproducibility.

**Clarity and limitations:** The report is relatively clear about size, passes and task formatting; comparisons must retain their tuning conditions.

Sources: [Reviewed paper: methods/results/limitations](https://arxiv.org/html/2403.18421v1)

## Paper-text origins

**Direct paper sources:** No direct source established for this row.

**Paper text via reused datasets:** The Pile PubMed components.

PubMed abstracts and PMC full articles are reused through The Pile. Their 34.6B-token corpus belongs in the existing-dataset column. [Source](https://arxiv.org/html/2403.18421v1)

## Other modalities

The reviewed training stage uses ordinary text rather than separately represented images, biological sequences or 3D structure tokens.

Sources: [Reviewed paper: data and representations](https://arxiv.org/html/2403.18421v1)

## Existing-dataset sources

The Pile: PubMed Central; The Pile: PubMed Abstracts.

Named reused inputs relevant to the reviewed training stages. This is not necessarily exhaustive. A source name establishes provenance, not its token amount; unreported amounts remain NR. Directly collected PubMed/PMC text is described separately as online-paper input. [Source](https://arxiv.org/html/2403.18421v1)

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [BioMedLM](#token-counts-by-acquisition-route)<br>Pretraining | Corpus · text | 0 | 0 | 34.6B | 34.6B | [§3.3](https://arxiv.org/html/2403.18421v1) |
| [BioMedLM](#token-counts-by-acquisition-route)<br>Pretraining | Training exposure · text | 0 | 0 | 300B | 300B | [§3.3](https://arxiv.org/html/2403.18421v1) |

**Pretraining — Corpus (text):** The Pile PubMed subsets are reused datasets; their literature content is not counted again as directly acquired papers. Corpus and repeated training exposure are separate.

- **Online Papers: 0.** No direct acquisition: the reported data are imported from The Pile.

- **Web Urls: 0.** The source says training uses exclusively the biomedical Pile subsets.

- **Existing Datasets: 34.6B.** The Pile PubMed abstracts and full articles, corpus.

- **Total: 34.6B.** Reported in §3.3; 34.6B available and 300B consumed are different quantities.

**Pretraining — Training exposure (text):** The Pile PubMed subsets are reused datasets; their literature content is not counted again as directly acquired papers. Corpus and repeated training exposure are separate.

- **Online Papers: 0.** No direct acquisition: the reported data are imported from The Pile.

- **Web Urls: 0.** The source says training uses exclusively the biomedical Pile subsets.

- **Existing Datasets: 300B.** The Pile PubMed abstracts and full articles, training exposure.

- **Total: 300B.** Reported in §3.3; 34.6B available and 300B consumed are different quantities.

**Training stage:** Pretraining from scratch; task-specific fine-tuning

**Backbone:** Random weights; 2.7B GPT-style decoder

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
