# peS2o

[Biological pretraining review](../README.md)

Reusable academic text corpus

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [peS2o](#token-counts-by-acquisition-route)<br>v2 corpus curation | Corpus · whitespace tokens | 0 | 0 | ≈42.01B | ≈42.01B | [v2 key facts](https://github.com/allenai/pes2o) |

**v2 corpus curation — Corpus (whitespace tokens):** The source explicitly reports whitespace-separated tokens. This is retained as that token definition, not converted to BPE/model tokens. S2ORC and S2AG are reused inputs.

- **Online Papers: 0.** The corpus is derived from existing S2ORC/S2AG inputs.

- **Web Urls: 0.** No directly crawled webpage source in the described v2 corpus.

- **Existing Datasets: ≈42.01B.** Source-reported v2 whitespace-separated token total.

- **Total: ≈42.01B.** Not comparable to a model-token count without retokenization.

**Training stage:** Corpus curation

**Source material and units:** peS2o is an already cleaned and packaged language-model corpus derived from S2ORC and Semantic Scholar abstracts. Its v2 training split lists **8,242,162 full-text-derived records and 30,569,017 title/abstract-derived records**. Thus, approximately 39M documents must not be described as 39M full-text papers. Its full-text branch uses GROBID-derived text and removes figures, tables and references. This saves extraction/curation work for text training but cannot replace source assets for our multimodal records. [Author documentation and exact split counts](https://github.com/allenai/pes2o)

**Acquisition and document processing:** Full-text cleaning removes figures, tables and references. A cleaned text corpus cannot restore the original images

## Figure handling

[peS2o](https://github.com/allenai/pes2o)

| Reported field | Retained source statement |
|---|---|
| Pixels used in training? | No |
| Source captions / generated material | Full-text cleaning removes figures, tables and references. A cleaned text corpus cannot restore the original images |

## Source details and qualifications

peS2o is an already cleaned and packaged language-model corpus derived from S2ORC and Semantic Scholar abstracts. Its v2 training split lists **8,242,162 full-text-derived records and 30,569,017 title/abstract-derived records**. Thus, approximately 39M documents must not be described as 39M full-text papers. Its full-text branch uses GROBID-derived text and removes figures, tables and references. This saves extraction/curation work for text training but cannot replace source assets for our multimodal records. [Author documentation and exact split counts](https://github.com/allenai/pes2o)

## Primary sources

- [Primary source retained from the existing review](https://github.com/allenai/pes2o)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
