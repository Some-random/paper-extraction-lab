# SciReasoner

[Biological pretraining review](../README.md)

Scientific model with biological data

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Continued pretraining. **Starting checkpoint:** Qwen3-1.7B / 8B. [Initialization evidence](https://arxiv.org/html/2509.21320v1)

Science-wide corpus with biological data; the 206B total is not entirely biological literature.

**Data included in the overview amounts:** Biology, chemistry, materials + other text. The 206B total and 166B named-dataset subtotal cover multiple sciences, not biology alone. The paper leaves 40B outside its enumerated components.

## Authors and institutions

**Authors:** Yizhou Wang; Chen Tang; Han Deng; Jiabei Xiao; Jiaqi Liu; Jianyu Wu; Jun Yao; Pengze Li; Encheng Su; Lintao Wang; Guohang Zhuang; Yuchen Ren; Ben Fei; Ming Hu; Xin Chen; Dongzhan Zhou; Junjun He; Xiangyu Yue; Zhenfei Yin; Jiamin Wu; Qihao Zheng; Yuhao Zhou; Huihui Xu; Chenglong Ma; Yan Lu; Wenlong Zhang; Chunfeng Song; Philip Torr; Shixiang Tang; Xinzhu Ma; Wanli Ouyang; Lei Bai.

**Institutions:** Shanghai Artificial Intelligence Laboratory; The University of Sydney; The Chinese University of Hong Kong; University of Oxford; University of Science and Technology of China; Beihang University; Fudan University; Shanghai Jiao Tong University.

[Paper attribution](https://arxiv.org/html/2509.21320v1). Names and affiliations follow the reviewed paper version.

## Evidence assessment

**Our assessment: Useful, limited.** CPT ablation; unresolved token accounting. This judges the evidence for the training/data claims, not institutional reputation or model size. It is a source-based review, not an independent replication.

**Strengths**

- Table 9 reports before/after pretraining results on ten tasks, beyond final-model leaderboard comparisons.

**Limitations**

- The five named source categories sum to 166B while the headline says 206B; the 40B difference is not reconciled.
- Final reasoning results also depend on SFT/RL, so the CPT ablation should not be generalized to every headline task.

Evidence: [Reviewed paper: methods/results/limitations](https://arxiv.org/html/2509.21320v1)

## Existing-dataset sources

UniRef50/90; RNAcentral; C4.

Named reused inputs relevant to the reviewed training stages. This is not necessarily exhaustive. A source name establishes provenance, not its token amount; unreported amounts remain NR. Directly collected PubMed/PMC text is described separately as online-paper input. [Source](https://arxiv.org/html/2509.21320v1)

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [SciReasoner](#token-counts-by-acquisition-route)<br>Scientific CPT | Corpus · text + scientific sequences | NR | NR | ≥166B | 206B | [§2 / Fig. 2](https://arxiv.org/html/2509.21320v1) |

**Scientific CPT — Corpus (text + scientific sequences):** The headline is 206B tokens. The five enumerated scientific-source components add to 166B; the source does not reconcile the remaining 40B. No residual is invented as a web or paper count.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: ≥166B.** Enumerated protein, chemistry, DNA, RNA and material dataset components only. Calculation: (55 + 50 + 30 + 26 + 5) × 1000000000.

- **Total: 206B.** Author-reported corpus headline; component discrepancy retained.

**Training stage:** Continued pretraining, then SFT and reasoning/RL

**Backbone:** Qwen3-1.7B / 8B

**Source material and units:** PubMed abstracts/scientific prose; exact literature-token share NR; Headline **206B**; prose gives proteins **55B**, chemistry **50B**, DNA **30B**, RNA **26B**, materials **5B**. Uses C4 general text. Later **40M SFT examples**, separate from CPT

**Disclosure gaps:** Five listed scientific categories sum to **166B**, not 206B. C4/source-text allocation is not separately reconciled; do not invent a 40B web allocation from the difference

## Datasets and amounts

[SciReasoner, September 2025 v1](https://arxiv.org/html/2509.21320v1), §2 / Figure 2

| Reported field | Retained source statement |
|---|---|
| Actual training stage | Qwen3 continued pretraining; later SFT/reasoning/RL |
| Literature text | PubMed abstracts/scientific prose; exact literature-token share NR |
| Web / other sources and amounts | Headline **206B**; prose gives proteins **55B**, chemistry **50B**, DNA **30B**, RNA **26B**, materials **5B**. Uses C4 general text. Later **40M SFT examples**, separate from CPT |
| Disclosure limits | Five listed scientific categories sum to **166B**, not 206B. C4/source-text allocation is not separately reconciled; do not invent a 40B web allocation from the difference |

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/html/2509.21320v1)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
