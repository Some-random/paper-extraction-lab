# BioLinkBERT

[Shared literature catalog](../README.md)

Biomedical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Encoder pretraining from scratch

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
