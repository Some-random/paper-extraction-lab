# BioLinkBERT

[Biological pretraining review](../README.md)

Biomedical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Pretraining from scratch. **Starting checkpoint:** Random weights; BERT architecture. [Initialization evidence](https://arxiv.org/html/2203.15827#S6.SS1)

Section 6.1 explicitly trains BioLinkBERT base and large from scratch. The general-domain LinkBERT initialization described elsewhere is a different experiment.

**Data included in the overview amounts:** Biomedical abstracts. The training corpus is PubMed abstracts and their citation links. No comparable token total or nonclinical biology split is disclosed.

## Authors and institutions

**Authors:** Michihiro Yasunaga; Jure Leskovec; Percy Liang.

**Institutions:** Stanford University.

[Paper attribution](https://arxiv.org/html/2203.15827#S6.SS1). Names and affiliations follow the reviewed paper version.

## Evidence assessment

**Our assessment: Useful, limited.** Link ablations; biomedical transfer caveat. This judges the evidence for the training/data claims, not institutional reputation or model size. It is a source-based review, not an independent replication.

**Strengths**

- Ablates link sampling and document-relation objectives and reports biomedical downstream tasks.

**Limitations**

- The most detailed link-objective ablations are in the general-domain experiments; their exact gains should not be assumed for the biomedical variant.
- Public-benchmark improvements do not isolate citation extraction quality or establish leakage-free deployment.

Evidence: [Reviewed paper: methods/results/limitations](https://arxiv.org/html/2203.15827#S6.SS1)

## Existing-dataset sources

No separately reused dataset identified for this overview row.

Named reused inputs relevant to the reviewed training stages. This is not necessarily exhaustive. A source name establishes provenance, not its token amount; unreported amounts remain NR. Directly collected PubMed/PMC text is described separately as online-paper input. [Source](https://arxiv.org/html/2203.15827#S6.SS1)

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [BioLinkBERT](#token-counts-by-acquisition-route)<br>Encoder pretraining from scratch | Not reported · text | NR | NR | NR | NR | [Paper](https://aclanthology.org/2022.acl-long.551/) |

**Encoder pretraining from scratch — Not reported (text):** The 21GB PubMed corpus and proportions of training-instance types do not establish token counts or acquisition-category shares.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Training stage:** Encoder pretraining from scratch

**Backbone:** Random weights; BERT architecture

**Source material and units:** PubMed documents and citation links

**Acquisition and document processing:** Uses linked-document contexts plus masked-token and document-relation objectives. A source-relationship recipe, not a PDF extraction tool.

## Source material

[BioLinkBERT](https://aclanthology.org/2022.acl-long.551/)

| Reported field | Retained source statement |
|---|---|
| Stage | Encoder pretraining |
| Actual biological source material | PubMed documents and citation links |
| How the source becomes training data / relevant limitation | Uses linked-document contexts plus masked-token and document-relation objectives. A source-relationship recipe, not a PDF extraction tool. |

## Datasets and amounts

[BioLinkBERT](https://arxiv.org/html/2203.15827), encoder from scratch, §6.1

| Reported field | Retained source statement |
|---|---|
| Literature contribution | Same **21GB PubMed abstract corpus** as PubMedBERT, with citation links |
| Web / other dataset contribution | No separately added web/replay corpus in the biological recipe |
| Quantitative limit | Token count NR. Contiguous/random/citation-linked **instance types each one third**; these are not three different data sources. Both biological model sizes train from scratch |

## Citation handling

BioLinkBERT, encoder pretraining

| Reported field | Retained source statement |
|---|---|
| Reported treatment | Packs linked PubMed documents together and learns masked-token and document-relation objectives using citation links. This explicitly exploits cross-document relationships; it is not an ordinary decoder CPT recipe. [LinkBERT paper](https://aclanthology.org/2022.acl-long.551/) |

## Primary sources

- [Primary source retained from the existing review](https://aclanthology.org/2022.acl-long.551/)
- [Primary source retained from the existing review](https://arxiv.org/html/2203.15827)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
