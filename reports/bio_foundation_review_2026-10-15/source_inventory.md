# Complete source inventory

[Biological pretraining review](README.md)

This register consolidates 87 source families named in the biological review and the documented inputs of TheBioCollection and OpenGenome2. Aliases and overlapping releases are grouped. It is a complete register of the named inputs in scope, not a claim that all their token amounts or unique contributions have been measured.

**— means the additional token contribution is unmeasured, not zero.** The overview subtotal counts only the three components with a common-tokenizer estimate. A source appearing inside TheBioCollection is not evidence that the whole external database has been included or that importing it separately would add nothing.

## Paper sources

| Source family | Counted amount / role | Referencing studies or collection | Source |
|:---|:---|:---|:---|
| ACL Anthology | —. Biological subset unresolved; mostly other research fields. | Galactica | [Paper](https://arxiv.org/pdf/2211.09085) · [Paper](https://arxiv.org/pdf/2211.09085#page=42) |
| arXiv | —. Biological subset and overlap with paper imports unresolved. | Galactica | [Paper](https://arxiv.org/pdf/2211.09085) · [Paper](https://arxiv.org/pdf/2211.09085#page=42) |
| BIOMEDICA | —. PMC-derived text and image-caption records; text overlaps PMC. | PMC-InterCPT / Beyond Captions | [Paper](https://arxiv.org/html/2606.01049v2) |
| bioRxiv | —. Partly overlaps published versions and imported scientific corpora; incremental amount unmeasured. | BioMatrix; BioT5 / BioT5+; Galactica; TheBioCollection / Gravity-bio | [Paper](https://arxiv.org/html/2402.17810v2) · [Paper](https://arxiv.org/html/2502.07527v2) |
| ChemRxiv | —. Biologically relevant subset and overlap unresolved. | Galactica | [Paper](https://arxiv.org/pdf/2211.09085) · [Paper](https://arxiv.org/pdf/2211.09085#page=42) |
| medRxiv | —. Research-biology subset and incremental overlap unresolved. | Galactica; TheBioCollection / Gravity-bio | [Paper](https://arxiv.org/html/2607.08803v1) · [Paper](https://arxiv.org/pdf/2211.09085) |
| OLMo 3 / olmOCR science PDFs | 972B across all subjects; biology-only amount —. 972B total across subjects; biology-only and incremental tokens unmeasured. | OLMo 3 | [Paper](https://arxiv.org/html/2512.13961v2#S3.SS4) |
| OSF | —. Biologically relevant subset and overlap unresolved. | Galactica | [Paper](https://arxiv.org/pdf/2211.09085) · [Paper](https://arxiv.org/pdf/2211.09085#page=42) |
| peS2o | —. Derived from Semantic Scholar/S2ORC; not additive to its full parent corpus. | peS2o | [Repository](https://github.com/allenai/pes2o) |
| PubAg | —. Agricultural research; incremental overlap unresolved. | Galactica | [Paper](https://arxiv.org/pdf/2211.09085) · [Paper](https://arxiv.org/pdf/2211.09085#page=42) |
| PubMed / MEDLINE abstracts | —. Abstracts overlap PMC and multiple imported corpora; incremental amount unmeasured. | BioBERT; BioGPT; BioLinkBERT; BioMamba; BioMatrix; BioMedLM; BioT5 / BioT5+; Galactica; TheBioCollection / Gravity-bio; PubMedBERT; SciReasoner | [Source](https://huggingface.co/stanford-crfm/BioMedLM) · [Source](https://academic.oup.com/bib/article/23/6/bbac409/6713511) |
| PubMed Central | 74.6B–217.6B. Count the current PMC scenario once; older PMC imports overlap. | BioBERT; Biomed-Enriched; BiomedCLIP / PMC-15M; BioMedLM; BioT5 / BioT5+; Galactica; PMC-InterCPT / Beyond Captions; PubMedBERT | [Source](https://huggingface.co/stanford-crfm/BioMedLM) · [Paper](https://arxiv.org/html/2007.15779v6) |
| S2ORC / Semantic Scholar | —. Overlaps PMC, preprints, peS2o and the OLMo PDF collection. | BioMatrix; BioMedGPT-LM / BioMedGPT (PharMolix); Galactica; S2ORC | [Source](https://aclanthology.org/2020.acl-main.447/) · [Paper](https://arxiv.org/html/2308.09442v2) |
| The Pile PubMed components | —. Older repackaging of PMC and PubMed; not an additional copy of the corpus. | BioMedLM | [Source](https://huggingface.co/stanford-crfm/BioMedLM) · [Paper](https://arxiv.org/html/2403.18421v1) |
| USPTO patent applications | —. Biological subset unresolved; reaction datasets below are derived records. | BioMatrix | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.22138v1) |

## Web sources

| Source family | Counted amount / role | Referencing studies or collection | Source |
|:---|:---|:---|:---|
| FineFineWeb biology | 85.7B. Count the biology-labelled collection once; do not add its parent FineWeb again. | How Post-Training Shapes Biological Reasoning Models; BioMatrix | [Source](https://huggingface.co/datasets/m-a-p/FineFineWeb) · [Paper](https://arxiv.org/html/2502.07527v2) |

## Biological database and task records

| Source family | Counted amount / role | Referencing studies or collection | Source |
|:---|:---|:---|:---|
| AlphaFold DB | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection; predicted structures overlap UniProt entities. | BioMatrix; TheBioCollection / Gravity-bio; Input to TheBioCollection | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.22138v1) |
| BindingDB | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection; extra coverage beyond the bundle unmeasured. | BioMatrix; TheBioCollection / Gravity-bio; Input to TheBioCollection | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.22138v1) |
| Cell Ontology | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| CELLxGENE | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| ChEMBL | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection; overlaps other molecular sources. | TheBioCollection / Gravity-bio; Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1) · [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| ClinVar | —. Variant records used in BioReason; scope and overlap unresolved. | BioReason | [Paper](https://arxiv.org/html/2505.23579v2) |
| COSMIC | —. Variant records used in BioReason; reusable subset and token count unresolved. | BioReason | [Paper](https://arxiv.org/html/2505.23579v2) |
| CrossDocked2020 | —. Protein-ligand complex records; relation to PDB-based sources unresolved. | BioMatrix | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.22138v1) |
| dbSNP | —. Variant records used in BioReason. | BioReason | [Paper](https://arxiv.org/html/2505.23579v2) |
| DGIdb | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| DRKG | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| DrugBank | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection; access and reusable subset may differ. | TheBioCollection / Gravity-bio; Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1) · [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| ENCODE | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection; assay records may overlap other resources. | TheBioCollection / Gravity-bio; Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1) · [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| GENCODE | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection; annotations are distinct from raw genome strings. | TheBioCollection / Gravity-bio; Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1) · [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| Gene Ontology / GOA | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection and protein annotation corpora. | BioReason-Pro; Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) · [Repository](https://github.com/bowang-lab/BioReason-Pro) |
| GeneRIF | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection; linked to NCBI Gene. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| GEOM-Drugs | —. Molecular conformers; do not count each representation as a new molecule. | UniGenX | [Paper](https://arxiv.org/html/2503.06687v1) · [Repository](https://github.com/UniGenX-Team/UniGenX) |
| gnomAD | —. Variant-frequency records used in BioReason. | BioReason | [Paper](https://arxiv.org/html/2505.23579v2) |
| Hetionet | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| HuBMAP | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| Human Protein Atlas | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| InterPro | —. Protein-domain annotations used in BioReason-Pro. | BioReason-Pro | [Repository](https://github.com/bowang-lab/BioReason-Pro) · [Source](https://www.biorxiv.org/content/10.64898/2026.03.19.712954v1) |
| J. Glaser binding-affinity dataset | —. Binding records; overlap with BindingDB and structural sources unresolved. | BioMatrix | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.22138v1) |
| JUMP Cell Painting | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| KEGG | —. Pathway records used in BioReason; reusable subset and token count unresolved. | BioReason | [Paper](https://arxiv.org/html/2505.23579v2) |
| LINCS L1000 | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| Mega-MolEdit | —. Molecular-edit training examples used by STRIDE; derivative task data. | STRIDE | [Repository](https://github.com/daiheng-zhang/STRIDE) |
| MISATO | —. Molecular-dynamics and protein-ligand records in later UniGenX repository support. | UniGenX | [Paper](https://arxiv.org/html/2503.06687v1) · [Repository](https://github.com/UniGenX-Team/UniGenX) |
| MolOpt-Instructions | —. Test reference in STRIDE; excluded from the training inventory total. | STRIDE | [Repository](https://github.com/daiheng-zhang/STRIDE) |
| MolTextNet | —. Molecule-description pairs; overlap with PubChem unresolved. | BioMatrix | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.22138v1) |
| NCBI Gene | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| OMIM | —. Variant/gene records used in BioReason; reusable subset and token count unresolved. | BioReason | [Paper](https://arxiv.org/html/2505.23579v2) |
| OmniPath | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| Open-AlphaSeq | —. Protein interaction measurements; incremental token count unmeasured. | BioMatrix | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.22138v1) |
| Other NCBI resources | —. The model report does not enumerate a precise reusable release. | NatureLM | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/pdf/2606.22138v1) |
| PCQM4Mv2 | —. Molecular-property records; PubChem-derived entities and additional labels. | BioMatrix | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.22138v1) |
| PPIRef | —. Protein-interface records; overlaps PDB entities. | BioMatrix | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.22138v1) |
| ProtDescribe | —. Swiss-Prot-derived protein descriptions used in ProtST; overlaps UniProt. | ProtST | [Paper](https://proceedings.mlr.press/v202/xu23t/xu23t.pdf) |
| Protein Data Bank | Represented in TheBioCollection; additional coverage —. PDB/RCSB are the same source family; contributes to TheBioCollection. | BioMatrix; TheBioCollection / Gravity-bio; Input to TheBioCollection | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.22138v1) |
| PubChem | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection and many model corpora; extra coverage beyond the bundle unmeasured. | BioMatrix; BioT5 / BioT5+; Galactica; TheBioCollection / Gravity-bio; NatureLM; Input to TheBioCollection | [Paper](https://arxiv.org/html/2402.17810v2) · [Paper](https://arxiv.org/html/2502.07527v2) |
| PubChemQC | —. PubChem-derived quantum-chemistry records; extra coverage unmeasured. | BioMatrix; LOGOS | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.16905v1) |
| QM9 / GEOM-QM9 | —. Molecular conformers and properties; QM9 and its GEOM views overlap. | UniGenX | [Paper](https://arxiv.org/html/2503.06687v1) · [Repository](https://github.com/UniGenX-Team/UniGenX) |
| Reactome | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection. | Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| Rfam | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection and OpenGenome2. | Input to TheBioCollection; Input to OpenGenome2 | [Source](https://huggingface.co/datasets/arcinstitute/opengenome2) · [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| RNAcentral | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection and OpenGenome2; avoid counting both complete exports. | SciReasoner; Input to TheBioCollection; Input to OpenGenome2 | [Source](https://huggingface.co/datasets/arcinstitute/opengenome2) · [Paper](https://arxiv.org/html/2509.21320v1) |
| STITCH | —. Interaction records; overlap with other interaction sources unresolved. | BioMatrix | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.22138v1) |
| STRING | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection and BioReason-Pro. | BioReason-Pro; Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1#S2) · [Repository](https://github.com/bowang-lab/BioReason-Pro) |
| TAPE GFP fluorescence | —. Sequence/function measurements used by STRIDE. | STRIDE | [Repository](https://github.com/daiheng-zhang/STRIDE) |
| TheBioCollection free-text stream | 37.0B. Count the free-text release once, excluding its separate instruction stream. | TheBioCollection / Gravity-bio | [Source](https://huggingface.co/datasets/trillionlabs/TheBioCollection) |
| Therapeutics Data Commons | —. Task collections used in Tx-LLM/TxGemma; repeated training tokens are not source size. | TxGemma; Tx-LLM | [Paper](https://arxiv.org/html/2406.06316v1) · [Paper](https://arxiv.org/html/2504.06196v1) |
| UniProt / UniRef | Represented in TheBioCollection; additional coverage —. Swiss-Prot, TrEMBL and UniRef clusterings overlap; contributes to TheBioCollection. | BioMatrix; BioReason-Pro; BioT5 / BioT5+; Galactica; TheBioCollection / Gravity-bio; LOGOS; NatureLM; ProtST; SciReasoner; Input to TheBioCollection | [Paper](https://arxiv.org/html/2402.17810v2) · [Paper](https://arxiv.org/html/2502.07527v2) |
| USPTO-50K reactions | Represented in TheBioCollection; additional coverage —. Contributes to TheBioCollection; derived from patents. | TheBioCollection / Gravity-bio; Input to TheBioCollection | [Paper](https://arxiv.org/html/2607.08803v1) · [Paper](https://arxiv.org/html/2607.08803v1#S2) |
| ZINC20 | —. Molecule records used in BioT5; overlap with other molecular sources unresolved. | BioT5 / BioT5+ | [Paper](https://arxiv.org/html/2402.17810v2) · [Repository](https://github.com/QizhiPei/BioT5) |

## Raw sequences and structures

| Source family | Counted amount / role | Referencing studies or collection | Source |
|:---|:---|:---|:---|
| Ensembl | Represented in OpenGenome2; additional coverage —. An upstream component of OpenGenome2. | Input to OpenGenome2 | [Source](https://huggingface.co/datasets/arcinstitute/opengenome2) |
| EPDnew | Represented in OpenGenome2; additional coverage —. An upstream component of OpenGenome2. | Input to OpenGenome2 | [Source](https://huggingface.co/datasets/arcinstitute/opengenome2) |
| GTDB | Represented in OpenGenome2; additional coverage —. An upstream component of OpenGenome2; not additive to its complete release. | Input to OpenGenome2 | [Source](https://huggingface.co/datasets/arcinstitute/opengenome2) |
| IMG/PR | Represented in OpenGenome2; additional coverage —. An upstream component of OpenGenome2. | Input to OpenGenome2 | [Source](https://huggingface.co/datasets/arcinstitute/opengenome2) |
| IMG/VR | Represented in OpenGenome2; additional coverage —. An upstream component of OpenGenome2. | Input to OpenGenome2 | [Source](https://huggingface.co/datasets/arcinstitute/opengenome2) |
| MGD metagenomes | Represented in OpenGenome2; additional coverage —. An upstream component of OpenGenome2. | Input to OpenGenome2 | [Source](https://huggingface.co/datasets/arcinstitute/opengenome2) |
| NCBI genome assemblies | Represented in OpenGenome2; additional coverage —. An upstream component of OpenGenome2. | Input to OpenGenome2 | [Source](https://huggingface.co/datasets/arcinstitute/opengenome2) |
| Observed Antibody Space | —. Antibody sequence pool; no common-tokenizer total established. | LOGOS | [Paper](https://arxiv.org/html/2606.16905v1) |
| OpenGenome2 | 8.8T nucleotide positions; separate from text subtotal. 8.8T biological nucleotide positions; not a count in the text tokenizer. | Evo 2 | [Source](https://huggingface.co/datasets/arcinstitute/opengenome2) |

## General replay and other sciences

| Source family | Counted amount / role | Referencing studies or collection | Source |
|:---|:---|:---|:---|
| C4 | —. General web replay; the biological fraction is unmeasured. | BioMamba; BioT5 / BioT5+; SciReasoner | [Paper](https://arxiv.org/html/2402.17810v2) · [Paper](https://arxiv.org/html/2509.21320v1) |
| DCLM-CC | —. General web replay, overlapping other Common Crawl derivatives. | TheBioCollection / Gravity-bio | [Paper](https://arxiv.org/html/2607.08803v1) |
| Dolma | —. Mixed-domain corpus; academic component overlaps peS2o. | Dolma | [Paper](https://arxiv.org/html/2402.00159) · [Paper](https://arxiv.org/html/2512.13961v2) |
| EAI-DCLM | —. General web replay; biological fraction unmeasured. | TheBioCollection / Gravity-bio | [Paper](https://arxiv.org/html/2607.08803v1) |
| English Wikipedia | —. General replay; biological subset unmeasured. | BioMamba | [Repository](https://github.com/lingyue404/BioMamba) · [Source](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/) |
| FineWeb-Edu | —. General educational text, overlapping the parent FineWeb collection. | BioMatrix | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/html/2606.22138v1) |
| Materials Project | —. Materials science outside the biological corpus. | NatureLM | [Paper](https://arxiv.org/html/2502.07527v2) · [Paper](https://arxiv.org/pdf/2606.22138v1) |
| MP-20 / Carbon-24 / MPTS-52 | —. Crystal/materials tasks in UniGenX; outside the biological total. | UniGenX | [Paper](https://arxiv.org/html/2503.06687v1) · [Repository](https://github.com/UniGenX-Team/UniGenX) |
| Papers with Code | —. General ML resource; biological subset unmeasured. | Galactica | [Paper](https://arxiv.org/pdf/2211.09085) · [Paper](https://arxiv.org/pdf/2211.09085#page=42) |

[Aggregate calculation and definitions](source_planning.md).
