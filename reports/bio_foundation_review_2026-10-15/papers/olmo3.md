# OLMo 3

[Shared literature catalog](../README.md)

General foundation-model method reference

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

## Token counts by acquisition route

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [OLMo 3](#token-counts-by-acquisition-route)<br>Pretraining: available 9T pool | Corpus pool · text | 993.4B | 8.14T | 174.79B | ≈9.31T | [Table 4](https://arxiv.org/html/2512.13961v2) |
| [OLMo 3](#token-counts-by-acquisition-route)<br>Pretraining: final 6T mix | Sampled training mix · text | 855.8B | 4.51T | 563.51B | ≈5.93T | [Table 4](https://arxiv.org/html/2512.13961v2) |
| [OLMo 3](#token-counts-by-acquisition-route)<br>Midtraining | Sampled training mix · text | 4.99B | 27.39B | ≥10B | 99.95B | [Table 5](https://arxiv.org/html/2512.13961v2) |

**Pretraining: available 9T pool — Corpus pool (text):** General-science/model data, not a biological-only budget. The paper-building and raw Common Crawl pipelines are direct acquisition. Stack-Edu, FineMath and encyclopedia source corpora are reused inputs. Totals preserve published rounding.

- **Online Papers: 993.4B.** olmOCR science PDFs and arXiv. Calculation: (972 + 21.4) × 1000000000.

- **Web Urls: 8.14T.** Raw Common Crawl input after curation.

- **Existing Datasets: 174.79B.** Stack-Edu, FineMath and Wikipedia/Wikibooks. Calculation: (137 + 34.1 + 3.69) × 1000000000.

- **Total: ≈9.31T.** Rounded 9T pool total.

**Pretraining: final 6T mix — Sampled training mix (text):** General-science/model tokens, not biological-paper tokens. Repetition/upsampling is already reflected in the 6T mix; do not add this row to the available pool.

- **Online Papers: 855.8B.** Sampled science PDFs and arXiv. Calculation: (805 + 50.8) × 1000000000.

- **Web Urls: 4.51T.** Sampled Common Crawl webpage tokens.

- **Existing Datasets: 563.51B.** Sampled Stack-Edu, FineMath and Wikipedia/Wikibooks. Calculation: (409 + 152 + 2.51) × 1000000000.

- **Total: ≈5.93T.** Rounded published 6T-mix total.

**Midtraining — Sampled training mix (text):** The total includes generated math, code and instruction material. Only the clearly separated direct PDF/web streams and the 10B reused StackEdu-FIM component are allocated here; other reused inputs add to the existing-dataset lower bound.

- **Online Papers: 4.99B.** High-quality science PDF component.

- **Web Urls: 27.39B.** High-quality Common Crawl plus STEM-heavy crawl. Calculation: (22.4 + 4.99) × 1000000000.

- **Existing Datasets: ≥10B.** StackEdu-FIM component alone; this is not the complete reused-source budget.

- **Total: 99.95B.** Published complete midtraining mix.

**Training stage:** Pretraining and midtraining

**Source material and units:** General model data: 5.93T sampled tokens in the reported stage-1 mix and 99.95B in stage-2 midtraining. Biological-paper allocation is not separately reported.

**Disclosure gaps:** The biological-paper fraction of the PDF pool is not separately disclosed. Its full PDF budget is not a biological-paper budget.

## Datasets and amounts

Stage 1, Table 4 “6T Mix”

| Reported field | Retained source statement |
|---|---|
| Web sources | Common Crawl **4.51T**; FineMath **152B**; Wikipedia/Wikibooks **2.51B** |
| Literature / academic documents | olmOCR science PDFs **805B**; arXiv **50.8B** |
| Remaining sources | Stack-Edu code **409B** |
| Reported total | **5.93T** sampled tokens, not the larger 9.31T available pool |

Stage 2 midtraining, Table 5 “100B Mix”

| Reported field | Retained source statement |
|---|---|
| Web sources | HQ Common Crawl **22.4B**; STEM-heavy web **4.99B** |
| Literature / academic documents | HQ olmOCR science PDFs **4.99B** |
| Remaining sources | StackEdu FIM **10B**, plus separately enumerated synthetic math/code/QA/reasoning/instruction sources |
| Reported total | **99.95B** sampled tokens; source-row rounding applies |

## Source details and qualifications

OLMo 3 is a general model. Its report explicitly identifies biology among the topics in its Gemini reasoning-trace source, but does not give a separately measured natural biology-literature allocation. It replaced the previous peS2o component with a new academic PDF pool. We therefore do not present its whole PDF token count as a biological-paper count or its general mix as a biology-specific data recipe. [§3.4.2 and Appendix A.3](https://arxiv.org/html/2512.13961v2)

**OLMo 3:** Its roughly 100B-token midtraining mix contains 4.99B PDF-derived tokens, 27.39B web tokens, 10B StackEdu code tokens and substantial synthetic math, code, QA and reasoning data. Synthetic material is therefore used before the separate SFT/RL stages. [§3.5, Table 5](https://arxiv.org/html/2512.13961v2)

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/html/2512.13961v2)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
