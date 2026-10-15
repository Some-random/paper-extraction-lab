# Dolma

[Biological pretraining review](../README.md)

Reusable general text corpus

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [Dolma](#token-counts-by-acquisition-route)<br>Original corpus construction | Corpus · text | 0 | 2.281T | 778.3B | ≈3.059T | [Table 1 / §3](https://arxiv.org/html/2402.00159v1) |

**Original corpus construction — Corpus (text):** Table 1 distinguishes 2,281B directly processed Common Crawl tokens from 198B reused C4 tokens. Earlier prose grouping these as 2,479B web-origin tokens described content origin, not acquisition route. This table separates them. Original Dolma is not Dolma 3.

- **Online Papers: 0.** Academic text is imported through peS2o rather than counted again as direct papers.

- **Web Urls: 2.281T.** Direct Common Crawl processing, Table 1.

- **Existing Datasets: 778.3B.** The Stack, C4, Pushshift Reddit, peS2o, Project Gutenberg and Wikipedia/Wikibooks. Calculation: (411 + 198 + 89 + 70 + 6 + 4.3) × 1000000000.

- **Total: ≈3.059T.** Rounded published total; component sum is 3,059.3B.

**Training stage:** Corpus construction

**Source material and units:** The original **Dolma** corpus reports **Common Crawl 2,479B; GitHub 411B; Reddit 89B; Semantic Scholar/peS2o 70B; Gutenberg 6B; Wikipedia/Wikibooks 4.3B**, approximately **3,059B total** with its stated tokenizer. This is a reusable dataset's composition, not a biology-only training run or the later Dolma 3 mix. Its academic component can be selected for biology; that selected amount is not given by the 70B headline. [Original Dolma, Table 1 / §8](https://arxiv.org/html/2402.00159)

## Source details and qualifications

The original **Dolma** corpus reports **Common Crawl 2,479B; GitHub 411B; Reddit 89B; Semantic Scholar/peS2o 70B; Gutenberg 6B; Wikipedia/Wikibooks 4.3B**, approximately **3,059B total** with its stated tokenizer. This is a reusable dataset's composition, not a biology-only training run or the later Dolma 3 mix. Its academic component can be selected for biology; that selected amount is not given by the 70B headline. [Original Dolma, Table 1 / §8](https://arxiv.org/html/2402.00159)

Dolma is both a **dataset family** and a **curation toolkit**. The original dataset mixes web text, scientific publications, code, books and other authored text, and uses peS2o for its academic component. Reusing a suitable subset is an important acquisition route, not merely a source of general replay. For our research goal, in-domain selection and deduplication against directly acquired papers matter. The toolkit supplies processing machinery; installing it does not acquire the corpus. Dolma 3 is a later corpus family, so version and constituent source must be recorded. [Dolma paper, §8](https://arxiv.org/html/2402.00159) · [Dataset/toolkit distinction](https://github.com/allenai/dolma) · [Dolma 3 in the OLMo 3 report](https://arxiv.org/html/2512.13961v2)

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/html/2402.00159)
- [Primary source retained from the existing review](https://github.com/allenai/dolma)
- [Primary source retained from the existing review](https://arxiv.org/html/2512.13961v2)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
