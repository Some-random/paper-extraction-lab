# Galactica

[Shared literature catalog](../README.md)

Scientific model with disclosed biological data

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Decoder pretraining from scratch

**Source material and units:** Scientific papers plus biological/chemical records such as UniProt and PubChem

**Acquisition and document processing:** Serializes scientific data alongside text and citation titles. A broad science model with disclosed biological material, rather than a biology-only model.

## Source material

[Galactica](https://arxiv.org/pdf/2211.09085)

| Reported field | Retained source statement |
|---|---|
| Stage | Scientific decoder pretraining from scratch |
| Actual biological source material | Scientific papers plus biological/chemical records such as UniProt and PubChem |
| How the source becomes training data / relevant limitation | Serializes scientific data alongside text and citation titles. A broad science model with disclosed biological material, rather than a biology-only model. |

## Datasets and amounts

[Galactica](https://arxiv.org/pdf/2211.09085), science decoder from scratch, Tables 2/22–24

| Reported field | Retained source statement |
|---|---|
| Literature contribution | **88B tokens** from papers + abstracts, **83.0%** reported corpus share |
| Web / other dataset contribution | Filtered Common Crawl **1B**; reference material **7B** includes Wikipedia, StackExchange and educational websites/books; code **7B** |
| Quantitative limit | Knowledge bases **2B**, prompts **0.4B**, other **0.2B**; headline corpus **106B**, training **450B**, **4.25 epochs**. Rounded rows do not sum exactly to the headline |

## Citation handling

Galactica, scientific decoder pretraining from scratch

| Reported field | Retained source statement |
|---|---|
| Reported treatment | Represents citations with titles and author surnames between `[START_REF]` and `[END_REF]`. Reports better citation prediction with titles than IDs, alongside hallucination tradeoffs. This is a citation-representation precedent, not a CPT experiment. [§3.1.2](https://arxiv.org/pdf/2211.09085) |

## Source details and qualifications

Galactica explicitly discloses biological literature: **PMC 23B**, **PubMed abstracts 5B**, **bioRxiv 1B** tokens; these are components of the 88B literature bucket. Other listed literature: arXiv **35B**, Semantic Scholar full text **18B**, Semantic Scholar abstracts **4B**, plus smaller sources. Its biological knowledge bases include PubChem **1B**, UniProt **0.6B**, RefSeq **0.1B**, Ribosome **0.05B**, LIPID MAPS **0.03B**, Reactome **0.01B**. Biological material can also occur in broader sources, so this is not an exhaustive biological-total calculation. [Galactica, Tables 22/24](https://arxiv.org/pdf/2211.09085#page=42)

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/pdf/2211.09085)
- [Primary source retained from the existing review](https://arxiv.org/pdf/2211.09085#page=42)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
