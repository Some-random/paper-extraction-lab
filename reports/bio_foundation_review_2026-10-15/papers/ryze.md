# Ryze

[Biological pretraining review](../README.md)

Biological document and training-data method reference

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [Ryze](#token-counts-by-acquisition-route)<br>SFT | Reported training-data budget · text | NR | NR | NR | 8.051591M | [§3.1](https://arxiv.org/html/2606.00902v1) |
| [Ryze](#token-counts-by-acquisition-route)<br>GRPO | Reported training-data budget · text | NR | NR | NR | 1.584412M | [§3.1](https://arxiv.org/html/2606.00902v1) |

**SFT — Reported training-data budget (text):** These are synthesized QA token budgets, not measured extracted-paper tokens. No compatible paper/web/reused-dataset partition is published for the generated sequences; they remain unallocated.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: 8.051591M.** Reported Qwen3-8B-tokenizer budget, §3.1.

**GRPO — Reported training-data budget (text):** These are synthesized QA token budgets, not measured extracted-paper tokens. No compatible paper/web/reused-dataset partition is published for the generated sequences; they remain unallocated.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: 1.584412M.** Reported Qwen3-8B-tokenizer budget, §3.1.

**Training stage:** Document extraction and training-data preparation reference

**Source material and units:** User-specified biological method paper. A paper/web/database token budget has not been normalized in this consolidation.

**Disclosure gaps:** The source repository and the published paper are distinct evidence. Repository capabilities do not establish the exact experiment configuration used in the paper.

## Primary sources

- [User-specified primary paper v1](https://arxiv.org/pdf/2606.00902v1)
- [Source repository recorded by the evaluation project](https://github.com/Chivier/Ryze)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
