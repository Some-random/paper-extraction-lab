# NatureLM

[Biological pretraining review](../README.md)

Biological and scientific multimodal foundation

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Paper year:** 2025. First public paper/preprint release; not the checkpoint release or latest revision. [Publication date](https://arxiv.org/abs/2502.07527).

**Training approach:** Continued pretraining. **Starting checkpoint:** Llama 3 8B / Mixtral 8×7B. [Initialization evidence](https://arxiv.org/html/2502.07527v2#S2.SS3)

The 8B and 8×7B models continue from existing checkpoints. The separate 1B model first trains on 300B SlimPajama text tokens, then receives scientific training; it is not trained on biology alone from its first step.

**Data included in the overview amounts:** Biology, chemistry, materials + general text. The complete 143.8B corpus is not biology-only. It includes 14.4B general text, several scientific modalities and cross-domain data; the existing-dataset lower bound also includes nonbiological materials.

## Authors and institutions

**Authors:** NatureLM team (credited group; individual author list in the paper).

**Institutions:** Microsoft Research AI for Science.

[Paper attribution](https://arxiv.org/html/2502.07527v2#S2.SS3). Names and affiliations follow the reviewed paper version.

<a id="evidence-assessment"></a>

## Overall paper assessment

**Overall: Solid.** A solid, ambitious scientific-model paper with a valuable representation and data-integration effort. The breadth is a strength, but varying backbones, post-training and heterogeneous tasks make some sweeping conclusions harder to assess. This is our provisional technical judgment of the whole paper in its publication context, not an official review score or an independent replication.

**Contribution and originality:** Combines language with several natural-science sequence types and cross-domain examples at meaningful scale.

**Technical soundness:** The shared vocabulary and training stages are coherent; the 1B and larger variants have different initialization histories.

**Evaluation:** Multiple domains and model sizes are informative, but they do not isolate each ingredient of the complete recipe.

**Reproducibility:** Data distributions and training settings are documented; some source-specific allocations and experimental details remain less complete.

**Clarity and limitations:** Examples make the broad design accessible, while some aggregate claims need more narrowly matched comparisons.

Sources: [Reviewed paper: methods/results/limitations](https://arxiv.org/html/2502.07527v2#S2.SS3)

## Paper-text origins

**Direct paper sources:** No direct source established for this row.

**Paper text via reused datasets:** No reused paper-text source established for this row.

The source describes scientific literature and entity-interleaved text, but the inspected pretraining section does not identify an auditable repository-by-repository paper allocation. PubMed mentions in related-work comparisons are not taken as evidence of NatureLM acquisition. [Source](https://arxiv.org/html/2502.07527v2#S2.SS3)

## Other modalities

Table S1 gives scientific-domain token buckets. These overlap the source-route totals: they are not additional data. The cross-domain bucket interleaves representations and text, and must not be treated as a disjoint acquisition route.

| Representation / domain | Reported tokens | Count definition |
|---|---:|---|
| Protein domain | 65.2B | Table S1 protein-domain tokens. |
| DNA domain | 19.8B | Table S1 DNA-domain tokens. |
| RNA domain | 27.5B | Table S1 RNA-domain tokens. |
| Small-molecule domain | 4.2B | Table S1 small-molecule domain; uses molecular string representations. |
| Material domain | 20M | Table S1 material-domain tokens. |
| Cross-domain text/sequence examples | 12.7B | Mixed text and scientific representations; not a pure non-text total. |

Sources: [Table S1 / §2.1](https://arxiv.org/html/2502.07527v2)

## Existing-dataset sources

PubChem; UniProt; Materials Project; NCBI resources.

Named reused inputs relevant to the reviewed training stages. This is not necessarily exhaustive. A source name establishes provenance, not its token amount; unreported amounts remain NR. Directly collected PubMed/PMC text is described separately as online-paper input. [Source](https://arxiv.org/html/2502.07527v2#S2.SS3)

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [NatureLM](#token-counts-by-acquisition-route)<br>8B / 8×7B scientific CPT | Corpus · text + scientific sequences | NR | NR | ≥116.72B | 143.8B | [§2 / Table S1](https://arxiv.org/html/2502.07527v2) |

**8B / 8×7B scientific CPT — Corpus (text + scientific sequences):** Table S1 is a 143.8B scientific corpus, not a paper-only budget. Separate molecule/protein/DNA/RNA/material source datasets establish a reused-data lower bound. The 14.4B general-text and 12.7B interleaved buckets are not assigned to a route without evidence. The 4.0B interleaved-literature count is not assumed to be directly acquired paper tokens.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: ≥116.72B.** Known molecule, protein, DNA, RNA and materials components only. Calculation: (4.2 + 65.2 + 19.8 + 27.5 + 0.02) × 1000000000.

- **Total: 143.8B.** Published Table S1 total; component rounding differs by 0.02B.

**Training stage:** Scientific decoder continued pretraining for larger variants

**Backbone:** Llama 3 8B / Mixtral 8×7B

**Source material and units:** Literature, database descriptions, small molecules, proteins, DNA/RNA and cross-domain pairs

**Acquisition and document processing:** Approximately 143B mixed tokens; BERN2 links literature mentions to molecular/protein representations. Structured sequence data is a major part of the corpus. Exact PDF-conversion settings are not disclosed.

## Source material

[NatureLM](https://arxiv.org/html/2502.07527v2)

| Reported field | Retained source statement |
|---|---|
| Stage | Scientific decoder CPT for its larger models |
| Actual biological source material | Literature, database descriptions, small molecules, proteins, DNA/RNA and cross-domain pairs |
| How the source becomes training data / relevant limitation | Approximately 143B mixed tokens; BERN2 links literature mentions to molecular/protein representations. Structured sequence data is a major part of the corpus. Exact PDF-conversion settings are not disclosed. |

## Datasets and amounts

[NatureLM](https://arxiv.org/html/2502.07527v2), science CPT of the 8B / 8×7B models, §2, Tables 1/S1

| Reported field | Retained source statement |
|---|---|
| Paper or abstract text | **4.0B literature-derived interleaved tokens**, already included in 12.7B cross-domain; further literature may occur in the text bucket |
| Web-origin text | Paper-versus-web split of the **14.4B text** bucket is NR |
| Other data in this stage | Molecules **4.2B**, proteins **65.2B**, DNA **19.8B**, RNA **27.5B**, materials **0.02B**, cross-domain **12.7B** |
| Reported total and disclosure limit | **143.8B corpus tokens** in Table S1; rounded components sum to 143.82B. Not 143.8B paper text |

## Figure handling

[NatureLM](https://arxiv.org/html/2502.07527v2) / [BioMatrix](https://arxiv.org/pdf/2606.22138v1)

| Reported field | Retained source statement |
|---|---|
| Pixels used in training? | Their disclosed biological modalities are sequences / structures / text |
| Source captions / generated material | “Multimodal” here does not establish paper-figure training. Molecule/protein “captioning” can mean generating a biological description from a molecular/protein representation |

## Source details and qualifications

NatureLM's 12.7B cross-domain bucket consists of interleaved literature **4.0B**, text–SMILES **3.0B**, text–protein **1.4B**, text–material **0.2B**, and DNA–protein **4.1B**. Do not add these to the 143.8B total again. Its 1B model first receives **300B SlimPajama text tokens**; that is a separate initialization phase. Later instruction tuning uses **5.1M pairs**, not an additional reported CPT token budget. [NatureLM, §2 and Tables 1/S1](https://arxiv.org/html/2502.07527v2)

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/html/2502.07527v2)
- [Primary source retained from the existing review](https://arxiv.org/pdf/2606.22138v1)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
