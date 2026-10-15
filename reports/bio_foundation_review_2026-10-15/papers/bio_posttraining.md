# How Post-Training Shapes Biological Reasoning Models

[Biological pretraining review](../README.md)

Biological CPT/SFT/RL study

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Continued pretraining. **Starting checkpoint:** Qwen3-1.7B / 4B. [Initialization evidence](https://arxiv.org/html/2606.16517v1)

Only the biological-web CPT stage is relevant to this overview. Encoder alignment, SFT and reinforcement learning are distinct later stages.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [How Post-Training Shapes Biological Reasoning Models](#token-counts-by-acquisition-route)<br>Biological-web continued pretraining | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2606.16517v1) |

**Biological-web continued pretraining — Not reported (text):** CPT uses 200K FineFineWeb biology documents and a 1,024-token maximum. Neither a realized token total nor acquisition-route token amounts are disclosed. Later encoder alignment, SFT and GRPO are separate stages.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Training stage:** Stage-wise biological adaptation experiments

**Backbone:** Qwen3-1.7B / 4B

**Source material and units:** FineFineWeb biology: first 200K documents train, next 5K evaluation; downstream DNA/RNA/protein reasoning data.

**Acquisition and document processing:** Biology web text for CPT, not a scientific-PDF OCR study.

**Cleaning and filtering:** Inherits upstream web filtering; no additional benchmark-specific CPT decontamination.

**Training unit and mixture:** Text-only causal CPT at maximum 1,024 tokens, one epoch; later biological encoder alignment, SFT and GRPO are separate stages.

**Generated or augmented material:** Reuses biologically grounded task supervision; study varies stage allocation rather than generating a replacement corpus for every article.

**Author-reported evidence:** CPT often improves later adaptation; longer SFT can improve in-distribution results while degrading biological out-of-distribution performance.

**Disclosure gaps:** Limited task families; stage-allocation comparison is not fully FLOP-matched; scores evaluate final answers, not the correctness of intermediate reasoning.

**Source sections:** 4.3; Limitations; Appendix B.2

## Primary sources

- [Biological post-training study](https://arxiv.org/html/2606.16517v1)
- [Author repository](https://github.com/mims-harvard/bio-posttrain)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
