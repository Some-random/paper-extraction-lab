# STRIDE

[Biological pretraining review](../README.md)

Biological sequence post-training method reference

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [STRIDE](#token-counts-by-acquisition-route)<br>Supervised fine-tuning followed by reinforcement learning | Not reported · text | NR | NR | NR | NR | [Paper](https://github.com/daiheng-zhang/STRIDE) |

**Supervised fine-tuning followed by reinforcement learning — Not reported (text):** The source describes task datasets and edit trajectories, not a tokenizer-token budget by paper/web/reused-dataset route.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Training stage:** Supervised fine-tuning followed by reinforcement learning

**Source material and units:** The retained author README describes GFP and SMILES task data with explicit edit trajectories; these are task datasets rather than a full-paper literature corpus.

**Disclosure gaps:** Imported source metadata supplies no paper/web/database training-token budget. Task-specific post-training is not paper-corpus CPT.

## Primary sources

- [Official source repository recorded in the evaluation registry](https://github.com/daiheng-zhang/STRIDE)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
