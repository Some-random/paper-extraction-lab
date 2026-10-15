# TheBioCollection / Gravity-bio

[Biological pretraining review](../README.md)

Biological multimodal foundation

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Continued pretraining. **Starting checkpoint:** Gravity-16B-A3B, before annealing. [Initialization evidence](https://arxiv.org/html/2607.08803v1#S3.SS1)

The overview shows lower bounds from two separate known corpus components. Neither their sum nor either component alone is the full annealing mixture or consumed training budget.

**Data included in the overview amounts:** Biological records + biomedical papers; replay extra. The displayed components are 52.6B biological database-derived tokens and approximately 54B biomedical literature tokens. Additional science/web replay is not quantified; the literature amount is not split into research biology versus clinical medicine.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [TheBioCollection / Gravity-bio](#token-counts-by-acquisition-route)<br>Biological corpus component | Corpus · text + scientific sequences | 0 | 0 | 52.6B | 52.6B | [§2 / Fig. 2](https://arxiv.org/html/2607.08803v1) |
| [TheBioCollection / Gravity-bio](#token-counts-by-acquisition-route)<br>Scientific-literature component | Corpus · text | ≈54B | 0 | 0 | ≈54B | [Table 4](https://arxiv.org/html/2607.08803v1) |
| [TheBioCollection / Gravity-bio](#token-counts-by-acquisition-route)<br>Full annealing mixture | Training exposure · text | NR | NR | NR | NR | [§3.1](https://arxiv.org/html/2607.08803v1) |
| [TheBioCollection / Gravity-bio](#token-counts-by-acquisition-route)<br>Known corpus components for biological annealing | Known corpus components · text + scientific sequences | ≥54B | NR | ≥52.6B | NR | [Table 4](https://arxiv.org/html/2607.08803v1) · [§2 / Fig. 2](https://arxiv.org/html/2607.08803v1) |

**Biological corpus component — Corpus (text + scientific sequences):** This row covers TheBioCollection biological database-derived corpus, including its derived feature/task representations. It excludes the separate scientific-literature corpus and other replay material.

- **Online Papers: 0.** The biological corpus component contains database-derived records; its separate literature component is the next row.

- **Web Urls: 0.** No separate directly gathered webpage stream is included in this component.

- **Existing Datasets: 52.6B.** Biological source databases and their derived record/task representations.

- **Total: 52.6B.** Published biological corpus size.

**Scientific-literature component — Corpus (text):** This is the separately reported 54.0B PubMed/bioRxiv/medRxiv literature component, not the complete annealing mixture. Additional olmOCR-PDF and web replay amounts are NR.

- **Online Papers: ≈54B.** Published Table 4 literature total; rounded source rows are 48.8B, 4.6B and 0.58B.

- **Web Urls: 0.** This component contains named scientific article repositories only.

- **Existing Datasets: 0.** This row is the directly sourced scientific-literature component, excluding the separate reused replay datasets.

- **Total: ≈54B.** Table 4 total, not total model exposure.

**Full annealing mixture — Training exposure (text):** The complete exposure and source-route allocation are NR. The two corpus-component sizes above cannot be added and presented as the complete training budget.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Known corpus components for biological annealing — Known corpus components (text + scientific sequences):** Overview of separate, non-overlapping known literature and biological-database corpus components. Each amount is only a lower bound on its route in the full mixture; additional replay amounts and total consumed tokens are not disclosed.

- **Online Papers: ≥54B.** The separately reported scientific-literature component is approximately 54B tokens; additional science-PDF replay is not quantified. The displayed lower bound retains the source rounding.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: ≥52.6B.** The biological-database corpus contributes 52.6B tokens; additional reused replay amounts are undisclosed.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Training stage:** Annealing / continued training

**Backbone:** Gravity-16B-A3B, before annealing

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
