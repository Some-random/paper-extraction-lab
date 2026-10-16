# PubMedBERT

[Biological pretraining review](../README.md)

Biomedical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Paper year:** 2020. First public paper/preprint release; not the checkpoint release or latest revision. [Publication date](https://arxiv.org/abs/2007.15779).

**Training approach:** Pretraining from scratch. **Architecture:** BERT architecture. [Initialization evidence](https://arxiv.org/html/2007.15779v6)

Domain vocabulary and model are learned from biomedical text, rather than starting with a general BERT checkpoint.

**Data included in the overview amounts:** Biomedical paper text. The reviewed PubMed/PMC sources are biomedical. Neither a comparable token total nor a nonclinical research-biology split is established here.

## Authors and institutions

**Authors:** Yu Gu; Robert Tinn; Hao Cheng; Michael Lucas; Naoto Usuyama; Xiaodong Liu; Tristan Naumann; Jianfeng Gao; Hoifung Poon.

**Institutions:** Microsoft Research.

[Paper attribution](https://arxiv.org/html/2007.15779v6). Names and affiliations follow the reviewed paper version.

<a id="evidence-assessment"></a>

## Overall paper assessment

**Overall: Strong.** A strong empirical paper: it poses a clear question about domain-specific pretraining, studies important design choices systematically and supplies a useful benchmark and model. The conclusions are persuasive within biomedical encoder NLP. This is our provisional technical judgment of the whole paper in its publication context, not an official review score or an independent replication.

**Contribution and originality:** Combines a substantive domain-pretraining question with a reusable benchmark and model.

**Technical soundness:** Vocabulary, initialization and pretraining choices are tied directly to the hypothesis under study.

**Evaluation:** Multiple tasks and ablations provide a stronger overall case than a single headline score.

**Reproducibility:** Public artifacts and detailed settings make the work usable, though the review still lacks comparable corpus-token totals.

**Clarity and limitations:** A focused presentation makes the scope and design tradeoffs understandable.

Sources: [Reviewed paper: methods/results/limitations](https://arxiv.org/html/2007.15779v6)

## Paper-text origins

**Direct paper sources:** PubMed abstracts; PMC full text.

**Paper text via reused datasets:** No reused paper-text source established for this row.

PubMed abstracts are the main corpus; additional PMC full-text experiments are separately discussed. Their document/word sizes are not converted to token counts here. [Source](https://arxiv.org/html/2007.15779v6)

## Other modalities

The reviewed training stage uses ordinary text rather than separately represented images, biological sequences or 3D structure tokens.

Sources: [Reviewed paper: data and representations](https://arxiv.org/html/2007.15779v6)

## Existing-dataset sources

No separately reused dataset identified for this overview row.

Named reused inputs relevant to the reviewed training stages. This is not necessarily exhaustive. A source name establishes provenance, not its token amount; unreported amounts remain NR. Directly collected PubMed/PMC text is described separately as online-paper input. [Source](https://arxiv.org/html/2007.15779v6)

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [PubMedBERT](#token-counts-by-acquisition-route)<br>Encoder pretraining from scratch | Not reported · text | NR | NR | NR | NR | [Paper](https://doi.org/10.1145/3458754) |

**Encoder pretraining from scratch — Not reported (text):** The source reports abstracts, words and bytes. Training examples and maximum sequence length do not establish realized tokenizer-token counts.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Training stage:** Encoder pretraining from scratch

**Backbone:** BERT architecture

**Source material and units:** PubMed abstracts; additional PMC experiments

**Acquisition and document processing:** Builds an in-domain vocabulary. The paper tests abstracts versus adding full texts; this is a literature-representation model, not a vision model.

## Source material

[PubMedBERT](https://doi.org/10.1145/3458754)

| Reported field | Retained source statement |
|---|---|
| Stage | Encoder pretraining from scratch |
| Actual biological source material | PubMed abstracts; additional PMC experiments |
| How the source becomes training data / relevant limitation | Builds an in-domain vocabulary. The paper tests abstracts versus adding full texts; this is a literature-representation model, not a vision model. |

## Datasets and amounts

[PubMedBERT](https://arxiv.org/html/2007.15779v6), encoder from scratch, §2.5/3.2

| Reported field | Retained source statement |
|---|---|
| Literature contribution | Standard: **14M abstracts, 3.2B words, 21GB**. Added-PMC experiment: **16.8B words, 107GB total** |
| Web / other dataset contribution | No general web replay in the standard recipe |
| Quantitative limit | Unique tokenizer-token count NR. Standard training **62,500 steps × 8,192 examples**; this example count is not a token count |

## Primary sources

- [Primary source retained from the existing review](https://doi.org/10.1145/3458754)
- [Primary source retained from the existing review](https://arxiv.org/html/2007.15779v6)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
