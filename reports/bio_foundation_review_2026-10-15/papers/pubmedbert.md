# PubMedBERT

[Biological pretraining review](../README.md)

Biomedical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Pretraining from scratch. **Starting checkpoint:** Random weights; BERT architecture. [Initialization evidence](https://arxiv.org/html/2007.15779v6)

Domain vocabulary and model are learned from biomedical text, rather than starting with a general BERT checkpoint.

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

**Backbone:** Random weights; BERT architecture

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
