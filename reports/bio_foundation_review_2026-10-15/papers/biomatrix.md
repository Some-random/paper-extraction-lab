# BioMatrix

[Shared literature catalog](../README.md)

Biological multimodal foundation

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Multimodal CPT, then multitask SFT

**Backbone:** Qwen3 1.7B/4B

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

## Figure handling

[NatureLM](https://arxiv.org/html/2502.07527v2) / [BioMatrix](https://arxiv.org/pdf/2606.22138v1)

| Reported field | Retained source statement |
|---|---|
| Pixels used in training? | Their disclosed biological modalities are sequences / structures / text |
| Source captions / generated material | “Multimodal” here does not establish paper-figure training. Molecule/protein “captioning” can mean generating a biological description from a molecular/protein representation |

## Source details and qualifications

BioMatrix's scientific text uses FineFineWeb biology/chemistry/medicine/health and literature; its figure also names bioRxiv. No numeric paper/web split is supplied. Figure 3 subdivides protein tokens into **36.0B sequence / 38.5B structure / 2.9B other**; molecule tokens into **32.1B sequence / 17.6B structure / 24.0B other**; cross-entity tokens into **17.1B sequence / 11.4B structure / 19.5B other**. The “other” subdivisions should not be relabeled entirely as generated text. Sources include PubChem, UniRef/UniProt, PDB/AFDB, interaction datasets and GPT-generated MolTextNet descriptions; exact individual budgets remain NR. These modalities are biomolecular representations, not paper-figure pixels. [BioMatrix, Figure 3 and §3](https://arxiv.org/pdf/2606.22138v1#page=12)

**BioMatrix:** Continues Qwen3 on 304.4B tokens spanning literature/web text, PubChem records, protein sequences and structures, interactions and interleaved text/entities. It includes GPT-generated MolTextNet descriptions and computational structures as well as experimental PDB structures. Its TrEMBL branch explicitly removes literature citations and evidence codes. These provenance differences should remain visible in a scientific corpus. [§3.1–3.2](https://arxiv.org/html/2606.22138v1)

## Primary sources

- [BioMatrix report](https://arxiv.org/html/2606.22138v1)
- [Author repository](https://github.com/QizhiPei/BioMatrix)
- [Primary source retained from the existing review](https://arxiv.org/pdf/2606.22138v1#page=12)
- [Primary source retained from the existing review](https://arxiv.org/html/2502.07527v2)
- [Primary source retained from the existing review](https://arxiv.org/pdf/2606.22138v1)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
