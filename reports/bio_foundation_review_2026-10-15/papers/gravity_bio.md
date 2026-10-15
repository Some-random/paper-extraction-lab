# TheBioCollection / Gravity-bio

[Shared literature catalog](../README.md)

Biological multimodal foundation

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Annealing / continued training

**Source material and units:** **54.0B scientific text**: PubMed **48.8B**, bioRxiv **4.6B**, medRxiv **0.58B**, with rounding; Biological corpus **52.6B**: molecules **28.2B**, proteins **14.5B**, genomic sequences **7.1B**, cells/pathways **2.8B**. Also uses olmOCR science PDFs, DCLM-CC and EAI-DCLM replay

**Disclosure gaps:** The 52.6B headline **excludes** the scientific-literature text. Other replay token amounts NR; do not call 52.6B the full training mixture

## Datasets and amounts

[TheBioCollection / Gravity-bio, July 2026 v1](https://arxiv.org/html/2607.08803v1), Figure 2, Tables 1/4, §3.1

| Reported field | Retained source statement |
|---|---|
| Actual training stage | Annealing / continued training from Gravity-16B-A3B |
| Literature text | **54.0B scientific text**: PubMed **48.8B**, bioRxiv **4.6B**, medRxiv **0.58B**, with rounding |
| Web / other sources and amounts | Biological corpus **52.6B**: molecules **28.2B**, proteins **14.5B**, genomic sequences **7.1B**, cells/pathways **2.8B**. Also uses olmOCR science PDFs, DCLM-CC and EAI-DCLM replay |
| Disclosure limits | The 52.6B headline **excludes** the scientific-literature text. Other replay token amounts NR; do not call 52.6B the full training mixture |

## Source details and qualifications

TheBioCollection's Figure 2 also splits its 52.6B corpus into **33.8B free-text / 18.9B instruction stream**; rounded components sum to 52.7B. “Free-text” here includes rendered database records and tool-derived biological descriptions, not just journal articles or scraped webpages. Literature in Table 4 is counted separately. The inspected figure was read directly, not estimated from its arc sizes. [Primary report](https://arxiv.org/html/2607.08803v1)

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/html/2607.08803v1)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
