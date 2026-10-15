# BioBERT

[Shared literature catalog](../README.md)

Biomedical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Encoder continued pretraining

**Source material and units:** PubMed abstracts and PMC full text

**Acquisition and document processing:** Continues BERT's masked-language-model training on biomedical literature. Relevant precedent for domain adaptation, with a different objective from a decoder LLM.

## Source material

[BioBERT](https://pmc.ncbi.nlm.nih.gov/articles/PMC7703786/)

| Reported field | Retained source statement |
|---|---|
| Stage | Encoder continued pretraining |
| Actual biological source material | PubMed abstracts and PMC full text |
| How the source becomes training data / relevant limitation | Continues BERT's masked-language-model training on biomedical literature. Relevant precedent for domain adaptation, with a different objective from a decoder LLM. |

## Datasets and amounts

[BioBERT](https://arxiv.org/pdf/1901.08746), encoder CPT, Tables 1/2 and §4.2

| Reported field | Retained source statement |
|---|---|
| Literature contribution | Available PubMed **4.5B words**; PMC **13.5B words** |
| Web / other dataset contribution | Initial BERT already trained on Wikipedia **2.5B words** and BooksCorpus **0.8B words** |
| Quantitative limit | Words are not tokenizer tokens. v1.0 combined adaptation: **200K PubMed + 270K PMC steps**; v1.1: **1M PubMed steps**. Different variants use different subsets |

## Primary sources

- [Primary source retained from the existing review](https://pmc.ncbi.nlm.nih.gov/articles/PMC7703786/)
- [Primary source retained from the existing review](https://arxiv.org/pdf/1901.08746)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
