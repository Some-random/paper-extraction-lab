# LLaVA-Med

[Shared literature catalog](../README.md)

Biomedical vision-language model

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

## Token counts by acquisition route

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [LLaVA-Med](#token-counts-by-acquisition-route)<br>Figure-caption alignment | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2306.00890) |
| [LLaVA-Med](#token-counts-by-acquisition-route)<br>Instruction tuning | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2306.00890) |

**Figure-caption alignment — Not reported (text):** The reported 600K alignment pairs and 60K instruction samples are not token counts. The two stages remain separate rows.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Instruction tuning — Not reported (text):** The reported 600K alignment pairs and 60K instruction samples are not token counts. The two stages remain separate rows.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Training stage:** Image-caption alignment, then instruction tuning

**Source material and units:** **600K source image–caption pairs** for alignment; **60K instruction examples** in its larger instruction datasets

**Acquisition and document processing:** First aligns image features to original captions. Later GPT-4 conversations are generated from caption/context text and kept as instruction data; the original method does not require GPT-4 to inspect the pixels

## Datasets and amounts

[LLaVA-Med](https://arxiv.org/html/2306.00890), §3

| Reported field | Retained source statement |
|---|---|
| Literature-derived amount | **600K source image–caption pairs** for alignment; **60K instruction examples** in its larger instruction datasets |
| Treatment of figure content | Alignment predicts original captions. GPT-4 generates later conversations using captions and, for 60K-IM, referring article text; this is a separate generated-data stage |

## Figure handling

[LLaVA-Med](https://arxiv.org/html/2306.00890)

| Reported field | Retained source statement |
|---|---|
| Pixels used in training? | Yes |
| Source captions / generated material | First aligns image features to original captions. Later GPT-4 conversations are generated from caption/context text and kept as instruction data; the original method does not require GPT-4 to inspect the pixels |

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/html/2306.00890)

## Related evaluation notes

- [Evaluation project: published comparisons and native-protocol requirements](https://github.com/Some-random/bio-evaluation/blob/main/reports/PUBLISHED_BENCHMARK_COMPARISONS_2026-10-15.md)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
