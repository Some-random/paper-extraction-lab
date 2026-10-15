# BioMedGPT-LM / BioMedGPT (PharMolix)

[Shared literature catalog](../README.md)

Biological multimodal language

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Literature CPT, then molecule/protein-text alignment

**Backbone:** Llama2-Chat-7B; BioMedGPT-10B adds biological encoders

**Source material and units:** 4.2M full-text S2ORC papers after filtering 5.5M biomedical candidates; over 26B text tokens.

**Acquisition and document processing:** S2ORC full text selected using PMC/PubMed IDs; no fresh PDF OCR implementation is specified.

**Cleaning and filtering:** Remove missing full texts, duplicate IDs, author information, reference citations, and chart data.

**Training unit and mixture:** Sentence-based chunks, 2,048-token context and autoregressive literature training; later align molecule graphs and protein sequences to the LLM.

**Generated or augmented material:** PubChemQA and UniProtQA turn database descriptions and annotations into templated questions. Invalid molecular graphs and very short descriptions are removed.

**Author-reported evidence:** Includes aligned versus unaligned biological-input baselines; not an experiment comparing OCR methods.

**Disclosure gaps:** Distinct from the similarly named vision-language BiomedGPT model. Random protein splits are weaker evidence of cross-family generalization.

**Source sections:** 3.1 Biomedical generative language model; 3.2 Multimodal fine-tuning

## Source material

[BioMedGPT-LM, PharMolix](https://arxiv.org/html/2308.09442v2)

| Reported field | Retained source statement |
|---|---|
| Stage | Decoder CPT |
| Actual biological source material | 4.2M biomedical full texts selected from S2ORC, over 26B tokens |
| How the source becomes training data / relevant limitation | ID deduplication, removes reference citations/author information/chart data, then sentence-based text chunks. Molecule/protein alignment happens separately. |

## Datasets and amounts

[BioMedGPT-LM, PharMolix](https://arxiv.org/html/2308.09442v2), Llama-2-Chat CPT, §3.1

| Reported field | Retained source statement |
|---|---|
| Paper or abstract text | **>26B tokens**, 4.2M full-text papers, selected from S2ORC |
| Web-origin text | No separately added web corpus described |
| Other data in this stage | Molecule/protein alignment is a later stage |
| Reported total and disclosure limit | >26B literature-corpus tokens; a source-specific consumed-token breakdown is NR |

## Figure handling

[BioMedGPT-LM, PharMolix](https://arxiv.org/html/2308.09442v2)

| Reported field | Retained source statement |
|---|---|
| Pixels used in training? | No paper-image branch in the described CPT |
| Source captions / generated material | Removes chart data from its S2ORC literature input. Subsequent molecule/protein encoders are not figure-image encoders |

## Citation handling

PharMolix BioMedGPT-LM, decoder CPT

| Reported field | Retained source statement |
|---|---|
| Reported treatment | Removes reference citations, author information and chart data before sentence-based chunking. [§3.1](https://arxiv.org/html/2308.09442v2) |

## Primary sources

- [BioMedGPT report](https://arxiv.org/html/2308.09442v2)
- [OpenBioMed author repository](https://github.com/PharMolix/OpenBioMed)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
