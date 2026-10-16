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

<a id="evidence-assessment"></a>

## Overall paper assessment

**Overall: Mixed.** An ambitious scientific reasoning system with useful experiments, including a CPT ablation. Overall confidence is reduced by unreconciled data quantities and the difficulty of attributing broad claims across many training stages and tasks. This is our provisional technical judgment of the whole paper in its publication context, not an official review score or an independent replication.

**Contribution and originality:** Extends multimodal scientific training into reasoning-oriented tasks across several disciplines.

**Technical soundness:** The multi-stage recipe is plausible, but interacting CPT, SFT and RL components complicate causal interpretation.

**Evaluation:** Selected before/after CPT results are useful; they are narrower evidence than the complete final-model task suite.

**Reproducibility:** Named data sources and code links help, while the 206B headline versus 166B enumerated components remains unresolved.

**Clarity and limitations:** The large scope creates reporting complexity, with important numerical statements needing reconciliation.

Sources: [Reviewed paper: methods/results/limitations](https://arxiv.org/html/2509.21320v1)

## Paper-text origins

**Direct paper sources:** PubMed.

**Paper text via reused datasets:** No reused paper-text source established for this row.

The paper identifies PubMed abstracts/scientific prose. It does not separate the paper token total from other scientific and general data. [Source](https://arxiv.org/html/2509.21320v1)

## Other modalities

The reported scientific-domain buckets include sequence and associated representation/text data. The five figures sum to 166B; the 206B headline leaves 40B unreconciled. They must not be treated as pure sequence-token counts or added to acquisition totals.

| Representation / domain | Reported tokens | Count definition |
|---|---:|---|
| Protein domain | 55B | Reported category volume; not a separately measured pure-sequence total. |
| Chemistry domain | 50B | Includes molecular strings/representations and associated content. |
| DNA domain | 30B | Reported domain bucket. |
| RNA domain | 26B | Reported domain bucket. |
| Materials domain | 5B | Reported domain bucket. |

Sources: [Reviewed paper: data and representations](https://arxiv.org/html/2509.21320v1)

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
