# SciReasoner

[Biological pretraining review](../README.md)

Scientific model with biological data

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Continued pretraining. **Starting checkpoint:** Qwen3-1.7B / 8B. [Initialization evidence](https://arxiv.org/html/2509.21320v1)

Science-wide corpus with biological data; the 206B total is not entirely biological literature.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [SciReasoner](#token-counts-by-acquisition-route)<br>Scientific CPT | Corpus · text + scientific sequences | NR | NR | ≥166B | 206B | [§2 / Fig. 2](https://arxiv.org/html/2509.21320v1) |

**Scientific CPT — Corpus (text + scientific sequences):** The headline is 206B tokens. The five enumerated scientific-source components add to 166B; the source does not reconcile the remaining 40B. No residual is invented as a web or paper count.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: ≥166B.** Enumerated protein, chemistry, DNA, RNA and material dataset components only. Calculation: (55 + 50 + 30 + 26 + 5) × 1000000000.

- **Total: 206B.** Author-reported corpus headline; component discrepancy retained.

**Training stage:** Continued pretraining, then SFT and reasoning/RL

**Backbone:** Qwen3-1.7B / 8B

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
