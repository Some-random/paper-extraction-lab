# LOGOS

[Biological pretraining review](../README.md)

Scientific sequence and interaction model

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Continued pretraining. **Starting checkpoint:** Qwen3-8B; Llama 3.2-1B / 3B variants. [Initialization evidence](https://arxiv.org/html/2606.16905v1#S2.SS3)

The model inherits pretrained backbone and embedding weights. The 44.87B source headline is a scientific corpus across pretraining and post-training; it must not be described as a disclosed CPT-only budget.

**Data included in the overview amounts:** Biological, chemical and materials sequences. The 44.87B corpus includes scientific modalities beyond biology and spans pretraining/post-training; it is neither a biology-only prose count nor a disclosed CPT-only exposure.

## Authors and institutions

**Authors:** Mingyang Li; Yurou Liu; Jieping Ye; Bing Su; Ji-Rong Wen; Zheng Wang.

**Institutions:** Alibaba Group; Renmin University of China.

[Paper attribution](https://arxiv.org/html/2606.16905v1#S2.SS3). Names and affiliations follow the reviewed paper version.

## Evidence assessment

**Our assessment: Useful, limited.** Grammar/init ablations; stage totals mixed. This judges the evidence for the training/data claims, not institutional reputation or model size. It is a source-based review, not an independent replication.

**Strengths**

- Studies initialization, grammar components and cross-domain training rather than only reporting a final model.

**Limitations**

- The 44.87B corpus headline spans pretraining/post-training and is not a disclosed CPT-only exposure budget.
- Strong results on selected scientific generation tasks do not establish improved biological literature reasoning.

Evidence: [Reviewed paper: methods/results/limitations](https://arxiv.org/html/2606.16905v1#S2.SS3)

## Existing-dataset sources

UniRef90; OAS; PubChemQC.

Named reused inputs relevant to the reviewed training stages. This is not necessarily exhaustive. A source name establishes provenance, not its token amount; unreported amounts remain NR. Directly collected PubMed/PMC text is described separately as online-paper input. [Source](https://arxiv.org/html/2606.16905v1#S2.SS3)

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [LOGOS](#token-counts-by-acquisition-route)<br>Scientific pre-/post-training corpus | Corpus · scientific sequences | 0 | 0 | 44.87B | 44.87B | [§2 / Appendix A](https://arxiv.org/html/2606.16905v1) |

**Scientific pre-/post-training corpus — Corpus (scientific sequences):** The 44.87B corpus comprises serialized scientific sequences and interaction records drawn from named datasets; the source does not split this headline into separate pretraining and post-training budgets.

- **Online Papers: 0.** The described corpus comprises structured scientific dataset records, not a paper-text stream.

- **Web Urls: 0.** No direct webpage stream is included in this described corpus.

- **Existing Datasets: 44.87B.** Scientific sequence/interaction datasets serialized with the proposed grammar.

- **Total: 44.87B.** Combined corpus headline; not a stage-specific exposure total.

**Training stage:** Continued pretraining and post-training

**Backbone:** Qwen3-8B; Llama 3.2-1B / 3B variants

**Source material and units:** No large paper-text acquisition stage described; **44.87B** scientific-sequence/interaction tokens reported across protein, antibody, molecule, reaction, material, pocket and complex modalities

**Disclosure gaps:** Headline spans the described pre-/post-training data; exact stage-specific and paper/web splits NR. It is a structured-science recipe, not evidence of 44.87B extracted prose

## Datasets and amounts

[LOGOS, June 2026 v1](https://arxiv.org/html/2606.16905v1), Figure 2 / §2 / Appendix C

| Reported field | Retained source statement |
|---|---|
| Actual training stage | Scientific continued pretraining and post-training |
| Literature text | No large paper-text acquisition stage described |
| Web / other sources and amounts | **44.87B** scientific-sequence/interaction tokens reported across protein, antibody, molecule, reaction, material, pocket and complex modalities |
| Disclosure limits | Headline spans the described pre-/post-training data; exact stage-specific and paper/web splits NR. It is a structured-science recipe, not evidence of 44.87B extracted prose |

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/html/2606.16905v1)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
