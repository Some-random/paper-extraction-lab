# PMC-LLaMA

[Biological pretraining review](../README.md)

Biomedical/medical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

Archived reference outside the current biological pretraining review.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [PMC-LLaMA](#token-counts-by-acquisition-route)<br>Knowledge-injection CPT | Corpus · text | 0 | 0 | >75B | NR | [Dataset-I](https://arxiv.org/html/2304.14454v3) |

**Knowledge-injection CPT — Corpus (text):** Papers arrive through S2ORC. The separate approximately 4B textbook tokens are outside the three requested routes and are not mislabeled as paper tokens. RedPajama token amount is NR, so the full reused-dataset amount is only lower-bounded.

- **Online Papers: 0.** Reported scientific papers were selected from the existing S2ORC corpus.

- **Web Urls: 0.** No direct webpage collection is described for this stage.

- **Existing Datasets: >75B.** S2ORC alone exceeds 75B tokens; RedPajama adds an undisclosed amount.

- **Total: NR.** No complete distinct-corpus token total including the selected RedPajama corpus is disclosed.

**Training stage:** CPT knowledge injection, then SFT

**Backbone:** LLaMA; final report includes 13B model

**Source material and units:** 4.8M PMC-ID-selected S2ORC papers, over 75B tokens; 30K textbooks yielding approximately 4B tokens.

**Acquisition and document processing:** Papers arrive through S2ORC. Textbook text is extracted from PDFs; a specific OCR engine is not identified in the reviewed method.

**Cleaning and filtering:** Textbook deduplication and removal of URLs, author lists, contents, references, citations, and figure/table mentions.

**Training unit and mixture:** Batch token ratio is BOOKS:PAPERS:GENERAL = 15:4:1; RedPajama supplies general replay.

**Generated or augmented material:** SFT adds GPT-4 instruction paraphrases, ChatGPT-generated QA explanations, and UMLS entity/relationship prompts; 202M instruction tokens.

**Author-reported evidence:** Includes component ablations and medical QA evaluation.

**Disclosure gaps:** The large paper corpus does not mean papers dominate the sampled training mixture. Early paper-only 7B versions differ from the later recipe.

**Source sections:** Dataset-I and Dataset-II

## Datasets and amounts

[PMC-LLaMA](https://arxiv.org/html/2304.14454v3), §2

| Reported field | Retained source statement |
|---|---|
| Paper / abstract corpus | 4.8M papers, **>75B corpus tokens** |
| Web and reusable corpora | RedPajama general replay; available replay corpus size NR |
| Other corpus | 30K textbooks, **4B corpus tokens** |
| What the model actually samples | Per-batch token ratio **books:papers:general = 15:4:1**, hence **75% / 20% / 5%**. Corpus availability is not the training mixture |

## Citation handling

PMC-LLaMA, CPT textbook branch

| Reported field | Retained source statement |
|---|---|
| Reported treatment | Removes references and citations during textbook cleaning. The report does not establish that this same policy was applied to its entire paper corpus. [Dataset-I: Books](https://arxiv.org/html/2304.14454v3) |

## Source details and qualifications

PMC-LLaMA defines one epoch as seeing the book tokens once and trains for five such epochs. It does not mean five passes over its >75B paper pool. I have not replaced the reported schedule with a falsely precise consumed-token estimate. [PMC-LLaMA, Combination / Knowledge Injection Training](https://arxiv.org/html/2304.14454v3)

**PMC-LLaMA:** Samples textbook, paper and general-domain tokens at 15:4:1 for knowledge-injection CPT. Its UMLS prompts and generated QA explanations belong to the later instruction stage. [Dataset-I and Dataset-II](https://arxiv.org/html/2304.14454v3)

## Primary sources

- [PMC-LLaMA paper](https://arxiv.org/html/2304.14454v3)
- [Author repository](https://github.com/chaoyi-wu/PMC-LLaMA)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
