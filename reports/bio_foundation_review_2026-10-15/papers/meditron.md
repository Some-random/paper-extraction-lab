# MEDITRON

[Shared literature catalog](../README.md)

Medical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

Historical medical context. Clinical-note acquisition is outside the biological research corpus scope.

## Token counts by acquisition route

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [MEDITRON](#token-counts-by-acquisition-route)<br>CPT | Corpus: train split · text | 0 | 107M | 46.6B | ≈46.7B | [§2 / Table 1](https://arxiv.org/html/2311.16079v1) |

**CPT — Corpus: train split (text):** Table 1 reports the train split of the corpus, not an independently measured training-exposure total. Both papers and abstracts come from S2ORC. Reused-source total is the sum of the three named source amounts; rounded component totals differ slightly from the rounded headline.

- **Online Papers: 0.** The paper explicitly obtains full texts and abstracts through S2ORC, not a second direct collection.

- **Web Urls: 107M.** Directly gathered medical guidelines, Table 1.

- **Existing Datasets: 46.6B.** S2ORC full papers and abstracts plus RedPajama replay. Calculation: 40700000000 + 5480000000 + 420000000.

- **Total: ≈46.7B.** Rounded published train-split total, Table 1.

**Training stage:** CPT, then task-specific SFT

**Backbone:** Llama-2 7B/70B

**Source material and units:** GAP-Replay: 48.1B tokens including validation; approximately 5M full texts, 16.1M abstracts, 46K guidelines, and 420M general replay tokens.

**Acquisition and document processing:** S2ORC text and annotations; upstream GROBID table extraction is explicitly discussed. Guidelines have a separate scraping/cleaning path.

**Cleaning and filtering:** English/ID deduplication; remove author/bibliography sections. Keep figure/table captions, discard unreliable table bodies, expand citation and figure references with tagged short descriptions.

**Training unit and mixture:** Approximately 1% general replay; 2,048-token 7B and 4,096-token 70B contexts.

**Generated or augmented material:** Structured reference rewriting is not teacher-generated scientific reasoning.

**Author-reported evidence:** 7B trial Table 8: PMC 54.6; PMC+Replay 56.2; clinically upsampled PMC 54.7; GAP+Replay 58.9 average accuracy.

**Disclosure gaps:** Clinical upsampling is an ablation, not the final best recipe; filtering animal studies is inappropriate for a general biology corpus.

**Source sections:** 2; 7.2 Table 8; Appendix B.2-B.4

## Datasets and amounts

[MEDITRON](https://arxiv.org/html/2311.16079v1), Table 1

| Reported field | Retained source statement |
|---|---|
| Paper / abstract corpus | Full-text papers **40.7B**; abstracts **5.48B** training tokens |
| Web and reusable corpora | Web-acquired guidelines **0.107B**; general replay **0.420B** from RedPajama |
| Other corpus | No additional category in Table 1 |
| What the model actually samples | **46.7B train**, **1.4B validation**, reported separately. Rounded training components sum to 46.707B |

## Figure handling

[MEDITRON](https://arxiv.org/html/2311.16079v1), Appendix B.2

| Reported field | Retained source statement |
|---|---|
| Pixels used in training? | No |
| Source captions / generated material | Discards figure pixels and table bodies; **retains captions** with figure/table tags. Inline figure/table references include a caption fragment truncated to 12 words. This is source-caption processing, not a VLM-generated caption |

## Citation handling

MEDITRON, decoder CPT

| Reported field | Retained source statement |
|---|---|
| Reported treatment | Omits the bibliography from the training body but replaces inline citations with the cited title, capped at 12 words, plus first-author surname inside `[bib_ref]` tags. This is metadata substitution, not a generated scientific summary. [§2.2 and Appendix B.2.1](https://arxiv.org/html/2311.16079v1) |

## Primary sources

- [MEDITRON report](https://arxiv.org/html/2311.16079v1)
- [Official GAP-Replay and training repository](https://github.com/epfLLM/meditron)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
