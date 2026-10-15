# Tx-LLM

[Biological pretraining review](../README.md)

Therapeutics multitask language model

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [Tx-LLM](#token-counts-by-acquisition-route)<br>Instruction tuning | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2406.06316v1) |

**Instruction tuning — Not reported (text):** The reported 709 component datasets and 66 tasks do not establish the number of training tokens. Inherited PaLM-2 pretraining is outside this adaptation row.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Training stage:** Instruction tuning

**Source material and units:** Manually written 2–3-sentence contexts informed by dataset descriptions and literature; TxT: **709 component datasets / 66 tasks**, derived from TDC

**Disclosure gaps:** Paper/web token split NR. Dataset/task counts are not token counts; inherited PaLM-2 data are outside this adaptation-stage budget

## Datasets and amounts

[Tx-LLM, June 2024 v1](https://arxiv.org/html/2406.06316v1), §3

| Reported field | Retained source statement |
|---|---|
| Actual training stage | Therapeutic instruction tuning of PaLM-2 |
| Literature text | Manually written 2–3-sentence contexts informed by dataset descriptions and literature |
| Web / other sources and amounts | TxT: **709 component datasets / 66 tasks**, derived from TDC |
| Disclosure limits | Paper/web token split NR. Dataset/task counts are not token counts; inherited PaLM-2 data are outside this adaptation-stage budget |

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/html/2406.06316v1)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
