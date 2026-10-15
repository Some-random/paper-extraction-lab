# BioT5 / BioT5+

[Shared literature catalog](../README.md)

Biological multimodal language

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Multimodal denoising pretraining and multitask tuning

**Backbone:** T5-family encoder-decoder; smaller than 7B-scale LLMs

**Source material and units:** PMC full text, PubMed/bioRxiv abstracts, C4, PubChem molecules, UniRef50 proteins, and biomolecule-description pairs.

**Acquisition and document processing:** Uses literature text and biomolecular databases; no identified new PDF-OCR engine.

**Cleaning and filtering:** BERN2 entity recognition/linking; BioT5+ retains linked entities with confidence above 0.9 and excludes downstream molecules/proteins from specified pretraining pairs.

**Training unit and mixture:** Nine pretraining tasks include masked-span denoising and bidirectional biomolecule-text translation, rather than only causal next-token prediction.

**Generated or augmented material:** Append canonical SELFIES/IUPAC or FASTA representations to mentions in scientific prose; deterministic database enrichment rather than invented experimental claims.

**Author-reported evidence:** Ablates additional literature, IUPAC information, and numeric tokenization on biomolecular tasks.

**Disclosure gaps:** Appendix E's 28.8M PubMed full-article claim is unresolved against source/abstract descriptions; do not use it as a verified downloadable PDF count.

**Source sections:** 3.2-3.4; Appendices C and E

## Source material

[BioT5+](https://arxiv.org/html/2402.17810v2)

| Reported field | Retained source statement |
|---|---|
| Stage | T5-style biological pretraining, then task tuning |
| Actual biological source material | PMC text, PubMed/bioRxiv abstracts, PubChem, ZINC20, UniRef50 and paired descriptions |
| How the source becomes training data / relevant limitation | Mixes text with molecule/protein sequences and entity-linked text. Denoising and bidirectional translation objectives; not ordinary decoder CPT. |

## Datasets and amounts

[BioT5+](https://arxiv.org/html/2402.17810v2), encoder–decoder pretraining, §3 / Appendix B

| Reported field | Retained source statement |
|---|---|
| Literature contribution | PMC full text, PubMed/bioRxiv abstracts and entity-wrapped abstracts |
| Web / other dataset contribution | **C4 web text**, PubChem/ZINC20 molecules, UniRef50 proteins, paired descriptions |
| Quantitative limit | Source token counts NR. **Eight tasks balanced by examples within each batch**; not evidence of eight equal token shares. **300K steps, 8×96 examples/batch, maximum input 512 tokens** |

## Source details and qualifications

BioT5+ does not publish enough information to convert its sampling scheme into “X billion paper tokens, Y billion web tokens.” Its text describes an addition of “28.8M full articles from PubMed”; I have not treated that ambiguous source description as a verified full-text count. This uncertainty does not affect the disclosed eight-task balancing scheme. [BioT5+, §3 / Appendix B](https://arxiv.org/html/2402.17810v2)

## Primary sources

- [BioT5+ paper](https://arxiv.org/html/2402.17810v2)
- [Author repository](https://github.com/QizhiPei/BioT5)

## Related evaluation notes

- [Evaluation project: published comparisons and native-protocol requirements](https://github.com/Some-random/bio-evaluation/blob/main/reports/PUBLISHED_BENCHMARK_COMPARISONS_2026-10-15.md)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
