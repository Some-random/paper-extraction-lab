# BioBERT

[Biological pretraining review](../README.md)

Biomedical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Continued pretraining. **Starting checkpoint:** BERT. [Initialization evidence](https://arxiv.org/pdf/1901.08746)

The reviewed BioBERT models initialize from BERT trained on general text. The paper reports source words rather than a comparable token total.

**Data included in the overview amounts:** Biomedical paper text. The additional domain data is PubMed/PMC literature. The source does not supply a token count or a separate research-biology/clinical split.

## Authors and institutions

**Authors:** Jinhyuk Lee; Wonjin Yoon; Sungdong Kim; Donghyeon Kim; Sunkyu Kim; Chan Ho So; Jaewoo Kang.

**Institutions:** Korea University; Clova AI Research, NAVER.

[Paper attribution](https://arxiv.org/pdf/1901.08746). Names and affiliations follow the reviewed paper version.

## Evidence assessment

**Our assessment: Stronger controls.** Direct BERT/domain-corpus comparisons. This judges the evidence for the training/data claims, not institutional reputation or model size. It is a source-based review, not an independent replication.

**Strengths**

- Initializes from BERT and compares added PubMed/PMC corpora across NER, relation extraction and QA.
- Released models/code make the experimental recipe inspectable.

**Limitations**

- Encoder task results do not establish the same gains for modern generative multimodal CPT.
- The reported source sizes use words/documents; they do not supply the token split required by this review.

Evidence: [Reviewed paper: methods/results/limitations](https://arxiv.org/pdf/1901.08746)

## Existing-dataset sources

No separately reused dataset identified for this overview row.

Named reused inputs relevant to the reviewed training stages. This is not necessarily exhaustive. A source name establishes provenance, not its token amount; unreported amounts remain NR. Directly collected PubMed/PMC text is described separately as online-paper input. [Source](https://arxiv.org/pdf/1901.08746)

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [BioBERT](#token-counts-by-acquisition-route)<br>Encoder continued pretraining | Not reported · text | NR | NR | NR | NR | [Paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7703786/) |

**Encoder continued pretraining — Not reported (text):** The source reports words and training steps for different variants. Word counts are not tokenizer-token counts; no word-to-token multiplier is applied.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Training stage:** Encoder continued pretraining

**Backbone:** BERT

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
