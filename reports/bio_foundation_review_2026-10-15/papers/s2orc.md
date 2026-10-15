# S2ORC

[Biological pretraining review](../README.md)

Reusable academic corpus

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [S2ORC](#token-counts-by-acquisition-route)<br>S2ORC-SciBERT filtered subset | Corpus · source-reported tokens | 16.4B | 0 | 0 | 16.4B | [§5](https://aclanthology.org/2020.acl-main.447.pdf) |
| [S2ORC](#token-counts-by-acquisition-route)<br>Full archive | Author-estimated corpus · source-reported tokens | NR | NR | NR | ≈40B | [Appendix E](https://aclanthology.org/2020.acl-main.447.pdf) |

**S2ORC-SciBERT filtered subset — Corpus (source-reported tokens):** Section 5 reports 16.4B tokens after scispaCy tokenization and filtering of parsed paper full text. This subset must not be confused with the entire S2ORC archive. Appendix E gives a slightly different rounded 16.5B description; the main-section value is retained.

- **Online Papers: 16.4B.** The S2ORC authors parse and filter source paper full texts for this demonstration.

- **Web Urls: 0.** This subset is filtered paper full text, not a non-paper webpage stream.

- **Existing Datasets: 0.** The row describes S2ORC corpus construction, not a downstream model importing S2ORC.

- **Total: 16.4B.** Section 5 pretraining subset.

**Full archive — Author-estimated corpus (source-reported tokens):** Appendix E estimates 25B full-body tokens and 15B abstract tokens. The total is an author estimate; the acquisition route of every abstract cannot be partitioned from this statement.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: ≈40B.** Sum of the two author-estimated source components. Calculation: 25000000000 + 15000000000.

**Training stage:** Corpus construction

**Source material and units:** S2ORC means **Semantic Scholar Open Research Corpus**. It aggregates research metadata and machine-readable academic text, including citation and figure/table mentions, across publishers and archives. The original 2020 release reported 81.1M paper records, with structured full text for 8.1M open-access papers; those are historical snapshot counts, not current availability. It is a corpus, not an OCR model. [Original S2ORC paper](https://aclanthology.org/2020.acl-main.447/)

## Source details and qualifications

S2ORC means **Semantic Scholar Open Research Corpus**. It aggregates research metadata and machine-readable academic text, including citation and figure/table mentions, across publishers and archives. The original 2020 release reported 81.1M paper records, with structured full text for 8.1M open-access papers; those are historical snapshot counts, not current availability. It is a corpus, not an OCR model. [Original S2ORC paper](https://aclanthology.org/2020.acl-main.447/)

## Primary sources

- [Primary source retained from the existing review](https://aclanthology.org/2020.acl-main.447/)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
