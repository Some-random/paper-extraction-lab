# BioReason

[Biological pretraining review](../README.md)

Biological multimodal reasoning model

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [BioReason](#token-counts-by-acquisition-route)<br>DNA-encoder/LLM supervised adaptation; selected GRPO | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2505.23579v2) |

**DNA-encoder/LLM supervised adaptation; selected GRPO — Not reported (text):** The reported KEGG and variant record counts are not tokenizer tokens. Generated rationales are a separate derivative, with no disclosed token split here.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Training stage:** DNA-encoder/LLM supervised adaptation; selected GRPO

**Source material and units:** Not a paper-corpus CPT experiment; Full task datasets before splitting: **1,449 KEGG reasoning records**, **50,083 coding variants**, **36,088 non-SNV variants**. Claude-generated reasoning; GPT-4o question paraphrases

**Disclosure gaps:** These are not training-split counts or paper counts. Token budget NR. Structured biological evidence and generated rationales have different provenance

## Datasets and amounts

[BioReason, August 2025 v2](https://arxiv.org/html/2505.23579v2), §4/5

| Reported field | Retained source statement |
|---|---|
| Actual training stage | DNA-encoder/LLM supervised adaptation, selected GRPO |
| Literature text | Not a paper-corpus CPT experiment |
| Web / other sources and amounts | Full task datasets before splitting: **1,449 KEGG reasoning records**, **50,083 coding variants**, **36,088 non-SNV variants**. Claude-generated reasoning; GPT-4o question paraphrases |
| Disclosure limits | These are not training-split counts or paper counts. Token budget NR. Structured biological evidence and generated rationales have different provenance |

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/html/2505.23579v2)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
