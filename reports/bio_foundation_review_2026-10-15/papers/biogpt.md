# BioGPT

[Shared literature catalog](../README.md)

Biomedical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Pretraining from scratch; task-specific fine-tuning

**Backbone:** GPT-2-style decoder; original 347M model

**Source material and units:** 15M PubMed records with both title and abstract, updated before 2021.

**Acquisition and document processing:** Download PubMed records from the official FTP distribution; title-plus-abstract text, rather than full paper PDFs.

**Cleaning and filtering:** Discard entries without an abstract. Learn an in-domain BPE vocabulary.

**Training unit and mixture:** Biomedical autoregressive pretraining; downstream tasks use task-specific prompts and target formats.

**Generated or augmented material:** Full-paper OCR and a general replay mixture are not the reported core recipe.

**Author-reported evidence:** Evaluates relation extraction, QA, document classification, and generation; these evaluate the trained model, not PDF extraction accuracy.

**Disclosure gaps:** Fifteen million records must not be described as fifteen million full-text papers.

**Source sections:** Pre-training method: Dataset and Vocabulary

## Source material

[BioGPT](https://academic.oup.com/bib/article/23/6/bbac409/6713511)

| Reported field | Retained source statement |
|---|---|
| Stage | Decoder pretraining from scratch |
| Actual biological source material | 15M PubMed title/abstract records |
| How the source becomes training data / relevant limitation | Downloads PubMed records, removes entries lacking abstracts, then autoregressive training. These are not full paper PDFs. |

## Datasets and amounts

[BioGPT](https://arxiv.org/pdf/2210.10341), decoder from scratch, Pre-training Method / Experiments

| Reported field | Retained source statement |
|---|---|
| Literature contribution | **15M title-and-abstract records**, not full papers |
| Web / other dataset contribution | Downloaded PubMed records; no other pretraining source described |
| Quantitative limit | Unique corpus token count NR. **200,000 × 524,288 = 104.8576B scheduled token positions**, calculated from the reported steps/global batch; includes repetitions and is not a distinct-corpus count |

## Figure handling

[BioGPT](https://arxiv.org/pdf/2210.10341)

| Reported field | Retained source statement |
|---|---|
| Pixels used in training? | No |
| Source captions / generated material | Its pretraining source is titles and abstracts; it does not ingest the full paper's figures |

## Primary sources

- [BioGPT paper](https://academic.oup.com/bib/article/23/6/bbac409/6713511)
- [Microsoft implementation](https://github.com/microsoft/BioGPT)
- [Primary source retained from the existing review](https://arxiv.org/pdf/2210.10341)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
