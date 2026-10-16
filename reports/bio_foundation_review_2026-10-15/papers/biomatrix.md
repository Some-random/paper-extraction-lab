# BioMatrix

[Biological pretraining review](../README.md)

Biological multimodal foundation

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Continued pretraining. **Starting checkpoint:** Qwen3-1.7B / 4B. [Initialization evidence](https://arxiv.org/html/2606.22138v1)

The headline contains scientific sequences and structures as well as prose. It is not a count of extracted paper text.

**Data included in the overview amounts:** Biological modalities + general text. The 304.4B headline includes general text and biological modalities. At least 176.7B is dataset-derived, including 25.6B of FineWeb-Edu general text; the rest of this lower bound is molecule/protein data. The 127.7B in mixed-source buckets is not fully allocated by acquisition route.

## Authors and institutions

**Authors:** Qizhi Pei; Zhimeng Zhou; Yi Duan; Yiyang Zhao; Wei Li; Han Guo; Liang He; Chengping Li; Chang-Yu Hsieh; Conghui He; Rui Yan; Lijun Wu.

**Institutions:** Renmin University of China; Shanghai Artificial Intelligence Laboratory; Zhejiang University; Shanghai Innovation Institute; East China Normal University; Zhongguancun Academy; Wuhan University.

[Paper attribution](https://arxiv.org/html/2606.22138v1). Names and affiliations follow the reviewed paper version.

## Evidence assessment

**Our assessment: Limited.** Overlap unresolved; task-group SFT. This judges the evidence for the training/data claims, not institutional reputation or model size. It is a source-based review, not an independent replication.

**Strengths**

- Broad evaluation across 80 tasks covers sequences, structures, language and interactions.
- The paper provides a detailed data recipe and explicitly discusses failure modes and task-group tuning.

**Limitations**

- Section 11 explicitly states that no dedicated entity-level filtering separates CPT from SFT/evaluation; scores do not establish contamination-free generalization.
- Headline results use task-group-specific SFT variants; they should not be read as one unchanged final model succeeding across all tasks.
- The total mixes modalities, generated dataset descriptions and general replay; exact source-route and biological-only fractions are incompletely reported.

Evidence: [Reviewed paper: methods/results/limitations](https://arxiv.org/html/2606.22138v1)

## Existing-dataset sources

FineWeb-Edu; PubChem; UniRef50; UniProt/Swiss-Prot; UniProt/TrEMBL; RCSB PDB; AlphaFold DB; MolTextNet; PCQM4Mv2; PubChemQC; FineFineWeb; S2ORC; USPTO-Applications; BindingDB; STITCH; jglaser binding affinity; CrossDocked2020; AlphaSeq; PPIRef.

Named reused inputs relevant to the reviewed training stages. This is not necessarily exhaustive. A source name establishes provenance, not its token amount; unreported amounts remain NR. Directly collected PubMed/PMC text is described separately as online-paper input. [Source](https://arxiv.org/html/2606.22138v1)

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [BioMatrix](#token-counts-by-acquisition-route)<br>Multimodal CPT | Corpus · text + scientific sequences | NR | NR | ≥176.7B | 304.4B | [Fig. 3 / §3.1](https://arxiv.org/pdf/2606.22138v1#page=12) · [Data sources](https://arxiv.org/html/2606.22138v1#S3.SS1) |

**Multimodal CPT — Corpus (text + scientific sequences):** 304.4B covers text, molecules, proteins and cross-entity/interleaved data. Figure 3 and §3.1 establish at least 176.7B dataset-derived tokens. The 79.7B scientific-text and 48.0B cross-entity/interleaved buckets mix acquisition routes; the remaining 127.7B is not assigned to a route. The total is not biology-only.

- **Online Papers: NR.** Direct PubMed full articles are used, but their separate token count is NR.

- **Web Urls: NR.** Web-origin text comes through FineWeb-Edu/FineFineWeb; no separate direct-crawl token budget is established.

- **Existing Datasets: ≥176.7B.** FineWeb-Edu general text (25.6B), protein datasets (77.4B), and molecule datasets (73.7B) are explicitly dataset-derived. Scientific text and cross-entity/interleaved data include further reused inputs but their exact route shares are unreported. Calculation: (25.6 + 77.4 + 73.7) × 1000000000.

- **Total: 304.4B.** Total corpus in §3 / Figure 3.

**Training stage:** Multimodal CPT, then multitask SFT

**Backbone:** Qwen3-1.7B / 4B

**Source material and units:** 304.4B mixed tokens: FineWeb-Edu; FineFineWeb biology/chemistry/medicine/health; PubMed text; molecules, proteins, structures, and interactions.

**Acquisition and document processing:** Article text and S2ORC/abstract/patent sources; the reviewed paper does not provide a reproducible PDF conversion recipe.

**Cleaning and filtering:** BERN2 links literature entity mentions to molecule/protein representations. Database annotations and available sequence/structure views are serialized together.

**Training unit and mixture:** Shared discrete vocabulary and next-token prediction; 8,192-token context, one epoch. General text provides replay.

**Generated or augmented material:** Randomize optional database fields and their order; create sequence-only, structure-only and joint protein views; interleave text with SMILES/SELFIES/amino-acid sequences.

**Author-reported evidence:** Broad 80-task evaluation after task tuning.

**Disclosure gaps:** No dedicated entity-level CPT/evaluation decontamination; authors acknowledge overlap. 304.4B is not all paper text or unique papers.

**Source sections:** 3.1-3.2; 11 Limitations

## Source material

[BioMatrix](https://arxiv.org/html/2606.22138v1)

| Reported field | Retained source statement |
|---|---|
| Stage | Multimodal decoder CPT |
| Actual biological source material | Literature/web text, PubChem, UniProt/UniRef, PDB, interaction records and structure views |
| How the source becomes training data / relevant limitation | 304.4B mixed tokens. Combines experimental and predicted structures and includes generated descriptions; those are distinct provenance classes. A reproducible paper-PDF conversion recipe is not disclosed. |

## Datasets and amounts

[BioMatrix](https://arxiv.org/pdf/2606.22138v1#page=12), Qwen3 CPT, §3, Figure 3

| Reported field | Retained source statement |
|---|---|
| Paper or abstract text | Part of **79.7B scientific-text tokens**; exact paper share NR |
| Web-origin text | **25.6B FineWeb-Edu** general text; scientific web shares the 79.7B bucket with literature |
| Other data in this stage | Molecule-centric **73.7B**, protein-centric **77.4B**, cross-entity/interleaved **48.0B** |
| Reported total and disclosure limit | **304.4B tokens**, one epoch. The four main categories sum exactly; per-website and per-database budgets NR |

## Token budget breakdown

[BioMatrix Figure 3 and §3.1](https://arxiv.org/pdf/2606.22138v1#page=12)

| Reported field | Retained source statement |
|---|---|
| General text | 25.6B — FineWeb-Edu; existing dataset. |
| Protein data | 77.4B — UniRef50, RCSB PDB, UniProt/Swiss-Prot, UniProt/TrEMBL and AlphaFold DB; existing datasets, including derived sequence/structure/text representations. |
| Molecule data | 73.7B — PubChem, PCQM4Mv2, PubChemQC and MolTextNet; existing datasets. MolTextNet includes generated descriptions supplied by that dataset. |
| Scientific text | 79.7B — FineFineWeb plus PubMed article text; exact source-route shares NR. |
| Cross-entity / interleaved | 48.0B — publication text, reused corpora and interaction datasets; exact route shares NR. |
| Total | 304.4B = 25.6 + 77.4 + 73.7 + 79.7 + 48.0 billion tokens. |
| Existing-dataset lower bound | 176.7B = 25.6 + 77.4 + 73.7 billion tokens. It is a lower bound, not the full reused-dataset total. |
| Unallocated by route | 127.7B = 79.7 + 48.0 billion tokens. These are known mixed-source components, not absent tokens. |
| Correction | The earlier 25.6B lower bound counted FineWeb-Edu alone and omitted two explicitly dataset-derived top-level buckets. It is superseded by 176.7B. |

## Figure handling

[NatureLM](https://arxiv.org/html/2502.07527v2) / [BioMatrix](https://arxiv.org/pdf/2606.22138v1)

| Reported field | Retained source statement |
|---|---|
| Pixels used in training? | Their disclosed biological modalities are sequences / structures / text |
| Source captions / generated material | “Multimodal” here does not establish paper-figure training. Molecule/protein “captioning” can mean generating a biological description from a molecular/protein representation |

## Source details and qualifications

BioMatrix's scientific text uses FineFineWeb biology/chemistry/medicine/health and literature; its figure also names bioRxiv. No numeric paper/web split is supplied. Figure 3 subdivides protein tokens into **36.0B sequence / 38.5B structure / 2.9B other**; molecule tokens into **32.1B sequence / 17.6B structure / 24.0B other**; cross-entity tokens into **17.1B sequence / 11.4B structure / 19.5B other**. The “other” subdivisions should not be relabeled entirely as generated text. Sources include PubChem, UniRef/UniProt, PDB/AFDB, interaction datasets and GPT-generated MolTextNet descriptions; exact individual budgets remain NR. These modalities are biomolecular representations, not paper-figure pixels. [BioMatrix, Figure 3 and §3](https://arxiv.org/pdf/2606.22138v1#page=12)

**BioMatrix:** Continues Qwen3 on 304.4B tokens spanning literature/web text, PubChem records, protein sequences and structures, interactions and interleaved text/entities. It includes GPT-generated MolTextNet descriptions and computational structures as well as experimental PDB structures. Its TrEMBL branch explicitly removes literature citations and evidence codes. These provenance differences should remain visible in a scientific corpus. [§3.1–3.2](https://arxiv.org/html/2606.22138v1)

The existing-dataset lower bound was corrected from 25.6B to 176.7B after checking all Figure 3 categories against the source descriptions in §3.1.2–3.1.4. This changes the review’s allocation, not the paper’s reported total.

## Primary sources

- [BioMatrix report](https://arxiv.org/html/2606.22138v1)
- [Author repository](https://github.com/QizhiPei/BioMatrix)
- [Primary source retained from the existing review](https://arxiv.org/pdf/2606.22138v1#page=12)
- [Primary source retained from the existing review](https://arxiv.org/html/2502.07527v2)
- [Primary source retained from the existing review](https://arxiv.org/pdf/2606.22138v1)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
