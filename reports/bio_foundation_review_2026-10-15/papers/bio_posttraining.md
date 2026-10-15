# How Post-Training Shapes Biological Reasoning Models

[Shared literature catalog](../README.md)

Biological CPT/SFT/RL study

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

## Token counts by acquisition route

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [How Post-Training Shapes Biological Reasoning Models](#token-counts-by-acquisition-route)<br>Stage-wise biological adaptation experiments | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2606.16517v1) |

**Stage-wise biological adaptation experiments — Not reported (text):** The reported 200K training documents and 1,024-token maximum are not a realized token total. No multiplication by the maximum length is used.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Training stage:** Stage-wise biological adaptation experiments

**Backbone:** Qwen3 1.7B/4B; additional backbone/biological encoder comparisons

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

## Related evaluation notes

- [Evaluation project: published comparisons and native-protocol requirements](https://github.com/Some-random/bio-evaluation/blob/main/reports/PUBLISHED_BENCHMARK_COMPARISONS_2026-10-15.md)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
