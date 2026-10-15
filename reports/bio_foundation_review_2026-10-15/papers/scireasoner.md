# SciReasoner

[Shared literature catalog](../README.md)

Scientific model with biological data

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Continued pretraining, then SFT and reasoning/RL

**Source material and units:** PubMed abstracts/scientific prose; exact literature-token share NR; Headline **206B**; prose gives proteins **55B**, chemistry **50B**, DNA **30B**, RNA **26B**, materials **5B**. Uses C4 general text. Later **40M SFT examples**, separate from CPT

**Disclosure gaps:** Five listed scientific categories sum to **166B**, not 206B. C4/source-text allocation is not separately reconciled; do not invent a 40B web allocation from the difference

## Datasets and amounts

[SciReasoner, September 2025 v1](https://arxiv.org/html/2509.21320v1), §2 / Figure 2

| Reported field | Retained source statement |
|---|---|
| Actual training stage | Qwen3 continued pretraining; later SFT/reasoning/RL |
| Literature text | PubMed abstracts/scientific prose; exact literature-token share NR |
| Web / other sources and amounts | Headline **206B**; prose gives proteins **55B**, chemistry **50B**, DNA **30B**, RNA **26B**, materials **5B**. Uses C4 general text. Later **40M SFT examples**, separate from CPT |
| Disclosure limits | Five listed scientific categories sum to **166B**, not 206B. C4/source-text allocation is not separately reconciled; do not invent a 40B web allocation from the difference |

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/html/2509.21320v1)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
