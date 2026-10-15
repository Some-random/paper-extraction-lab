# Canonical Wnt induction by OTULIN prevents keratinocyte death and skin inflammation

Science Advances · **PMC13651886** · CC BY

[Back to all three papers](../../README.md) · [Cleaned article](article.md) · [All figures and their context](figures.md) · [Training-record examples](training_samples.md)

33 research paragraphs · 6 figures · 2 tables · 9 text chunks · 9 figure/table–context records.

These results use publisher XML and original figure files. Earlier PDF-only olmOCR output remains available [here](../../../pmc_cns_biology_2026-10-14/samples/PMC13651886/fullpaper_olmocr.md). No new OCR inference or model training was performed.

## Source-checked examples

### What forward qPCR primer is listed for mouse Axin2?

**Answer:** CTCACCCATTTACCCAGGACC

**Source excerpt:**

> CTCACCCATTTACCCAGGACC

Table row: **Axin2**. Column: **Forward primer**.

PDF page(s) containing all checked text literals: **4**.

Validation: exact source-cell lookup; not a reasoning benchmark. PDF checking is a text-presence check, not an independent answer-quality score.

<details>
<summary>Source XML provenance</summary>

`/article/body/sec[2]/sec[1]/table-wrap[1]/table/tbody/tr[1]/td[1]`

XML SHA-256: `81379a62b9eb5611267e6ad9a97dd18da95946f8bd523c1f4d870d209334a014`

</details>

### What reverse qPCR primer is listed for mouse Axin2?

**Answer:** GTTCCTGTCCCTCTGCTGAC

**Source excerpt:**

> GTTCCTGTCCCTCTGCTGAC

Table row: **Axin2**. Column: **Reverse primer**.

PDF page(s) containing all checked text literals: **4**.

Validation: exact source-cell lookup; not a reasoning benchmark. PDF checking is a text-presence check, not an independent answer-quality score.

<details>
<summary>Source XML provenance</summary>

`/article/body/sec[2]/sec[1]/table-wrap[1]/table/tbody/tr[1]/td[2]`

XML SHA-256: `81379a62b9eb5611267e6ad9a97dd18da95946f8bd523c1f4d870d209334a014`

</details>

### What concentration is listed for the cleaved caspase-3 antibody?

**Answer:** 1/500

**Source excerpt:**

> 1/500

Table row: **Cleaved caspase-3**. Column: **Concentration**.

PDF page(s) containing all checked text literals: **4**.

Validation: exact source-cell lookup; not a reasoning benchmark. PDF checking is a text-presence check, not an independent answer-quality score.

<details>
<summary>Source XML provenance</summary>

`/article/body/sec[2]/sec[1]/table-wrap[2]/table/tbody/tr[1]/td[1]`

XML SHA-256: `81379a62b9eb5611267e6ad9a97dd18da95946f8bd523c1f4d870d209334a014`

</details>

## Featured original figure and source context

## Fig. 1.

![Fig. 1. — original publisher figure](assets/sciadv.adz0181-f1.webp)

**Source caption:** Wnt signaling is down-regulated in OTULIN-deficient KCs. (A) Left: UMAP clustering of scRNA-seq data obtained from cells isolated from ∆^(Ker)OTULIN and control skin (12), highlighting the KC cluster. Right: GO enrichment analysis of genes significantly down-regulated in OTULIN-deficient KCs relative to control KCs. (B) Violin plots showing distribution of expression of the indicated Wnt target genes in scRNA-seq data of KCs from OTULIN^(FL/FL) and ∆^(Ker)OTULIN skin. (C) qPCR analysis for the indicated Wnt target genes on epidermal tail lysates of OTULIN^(FL/FL) and Δ^(Ker)OTULIN mice (aged 8 to 11 weeks). Data are means ±SEM, ^(∗)P < 0.05; ^(∗∗)P < 0.01; ^(∗∗∗)P < 0.001. (D) qPCR analysis for the indicated Wnt effector genes on epidermal tail lysates of OTULIN^(FL/FL) and Δ^(Ker)OTULIN mice. Data are means ± SEM, ^(∗)P < 0.05; ^(∗∗)P < 0.01; ^(∗∗∗)P < 0.001. Violin plots showing distribution of expression of the indicated genes in scRNA-seq data of HF KCs from OTULIN^(FL/FL) and ∆^(Ker)OTULIN skin. (E) Immunoblotting for nonphosphorylated (active) β-catenin and OTULIN in epidermal tail lysates from OTULIN^(FL/FL) and ∆^(Ker)OTULIN mice. α-Actin is shown as loading control. (F) Immunofluorescence images of LEF1 staining in OTULIN^(FL/FL) anagen skin and ∆^(Ker)OTULIN lesional skin. Top panels are hematoxylin and eosin (H&E)–stained skin sections from the same mice. Scale bars, 100 μm (top); 50 μm (bottom). (G) Violin plots showing distribution of expression of the indicated genes in scRNA-seq data of HF KCs from OTULIN^(FL/FL) and ∆^(Ker)OTULIN skin.

### Article paragraphs explicitly referring to this figure

**RESULTS / Wnt signaling is down-regulated in OTULIN-deficient KCs**

> OTULIN was initially identified as a modulator of canonical Wnt signaling regulating embryonic angiogenesis (17). To determine whether OTULIN and linear (de)ubiquitination modulate Wnt responses in adult tissues, we analyzed Wnt signaling in the skin of mice with OTULIN-deficient KCs (∆^(Ker)OTULIN mice). We previously demonstrated that ∆^(Ker)OTULIN mice develop inflamed skin lesions that progress into well-differentiated squamous carcinomas (12, 13). Gene ontology (GO) enrichment analysis of our published single-cell RNA sequencing (scRNA-seq) dataset comparing total skin of wild-type (WT; Cre-negative OTULIN^(FL/FL)) and ∆^(Ker)OTULIN mice (12) revealed Wnt signaling as one of the top down-regulated GO terms in OTULIN-deficient KCs (Fig. 1A and fig. S1A). When probing expression levels of specific Wnt mediators in our scRNA-seq dataset, we indeed observed marked down-regulation in OTULIN-deficient KCs relative to control KCs (Fig. 1B). Quantitative polymerase chain reaction (qPCR) analysis of epidermal tail lysates confirmed the down-regulation of Wnt target genes in ∆^(Ker)OTULIN epidermis (Fig. 1C and Table 1). In agreement, expression levels of several members of the TCF/LEF family, key downstream mediators of canonical Wnt signaling, were also significantly reduced in ∆^(Ker)OTULIN epidermis (Fig. 1D). Immunoblotting for nonphosphorylated β-catenin, indicative of stabilized β-catenin and active Wnt signaling, confirmed reduced Wnt activation in epidermal tail lysates from ∆^(Ker)OTULIN relative to control mice (Fig. 1E). Wnt activation in KCs from adult skin is most prominent during the growth phase of HFs, also referred to as anagen, culminating in nuclear expression of LEF1 (20, 27). Immunofluorescence staining of anagen skin indicated nuclear LEF1 in WT HFs, whereas no nuclear LEF1 was observed in anagen-like HFs in lesional ∆^(Ker)OTULIN skin (Fig. 1F and Table 2). When probing HF cell populations (outer and inner layer, bulge and upper HF) of our scRNA-seq data for Wnt target gene expression, the down-regulation of Wnt target gene expression in OTULIN-deficient KCs was even more pronounced than in the total KC population (Fig. 1G). In addition to OTULIN, SHARPIN has also been implicated in stabilizing β-catenin (28). Therefore, we quantified expression levels of Wnt mediators and target genes in SHARPIN^(cpdm/cpdm) epidermis and control epidermis. Down-regulation of canonical Wnt signaling was observed in SHARPIN^(cpdm/cpdm) epidermis, supporting a role for linear ubiquitination in promoting Wnt signaling in adult KCs (fig. S1B). β-catenin also performs Wnt-independent roles at the plasma membrane (29). We assessed the levels of cytosolic β-catenin in OTULIN-deficient and control epidermis and observed higher levels in control epidermis, indicating that OTULIN promotes canonical Wnt signaling in the skin (fig. S1C). Together, these data demonstrate that OTULIN promotes canonical Wnt signaling in adult KCs.

<details>
<summary>Source XML provenance</summary>

`/article/body/sec[2]/sec[1]/p`

XML SHA-256: `81379a62b9eb5611267e6ad9a97dd18da95946f8bd523c1f4d870d209334a014`

</details>

**RESULTS / OTULIN regulates the stability of the survival factors TCF3 and TCF4**

> To investigate how linear ubiquitination of β-catenin influences KC survival, we focused on two Wnt target genes, Tcf3 and Tcf4, previously shown to protect cells from death by cooperative functioning with β-catenin to drive transcription (22, 34, 35). Tcf3 and Tcf4 were significantly suppressed in OTULIN-deficient mouse KCs (Fig. 1D). Previous studies demonstrated that genetic ablation of Tcf3/4 in KCs results in a marked increase of dying cells in neonatal mouse epidermis (34). Immunoblotting for TCF3 revealed a reduction in protein expression in OTULIN-deficient primary mouse KCs relative to WT KCs (Fig. 6A). Proteasome inhibition stabilized TCF3 in both WT and OTULIN-deficient cells, indicating that TCF3 stability is regulated by K48-linked ubiquitination in KCs. Both Wnt-repressive and Wnt-activating properties have been attributed to TCF3/4 (34). TCF3 expression in primary KCs strongly correlated with the levels of activated β-catenin levels, suggesting that TCF3 functions as a Wnt activator under these conditions (Fig. 6A). Consistently, Tcf3 and Tcf4 levels were reduced in epidermal lysates obtained from ∆^(Ker)OTULIN skin relative to control epidermis, and no significant difference in Tcf3 or Tcf4 levels was observed between control epidermis and epidermis from ∆^(Ker)OTULIN ΔNβcat mice (Fig. 6B). These findings indicate that the protection from cell death observed in KCs from ∆^(Ker)OTULIN ΔNβcat mice relative to ∆^(Ker)OTULIN mice could be linked to altered TCF3/4 expression levels. To test this hypothesis, OTULIN KD HaCaTs were reconstituted with TCF3 by lentiviral transduction (fig. S4A). Reconstitution of TCF3 significantly reduced TNF cytotoxicity in OTULIN KD cells; however, cell death in these reconstituted KCs remained higher than in control KCs (Fig. 6C). This indicates that TCF3/4 contribute to the cellular response to TNF, with evidence suggesting a modulatory, rather than exclusively protective, role in cell viability. Immunofluorescence staining for TCF4 in tail whole mounts of control mice confirmed TCF4 expression in adult normal HFs (36), whereas no TCF4 could be observed in ∆^(Ker)OTULIN skin (Fig. 6D). In contrast, TCF4 expression in the tail epidermis of ∆^(Ker)OTULIN ΔNβcat mice was comparable to that observed in control mice. Notably, co-staining for TCF4 with cleaved caspase-3 revealed that TCF4-expressing KCs were not undergoing apoptosis, as no double-stained cells were observed (Fig. 6D).

<details>
<summary>Source XML provenance</summary>

`/article/body/sec[2]/sec[6]/p[1]`

XML SHA-256: `81379a62b9eb5611267e6ad9a97dd18da95946f8bd523c1f4d870d209334a014`

</details>

<details>
<summary>Source XML provenance</summary>

`/article/body/sec[2]/sec[1]/fig`

XML SHA-256: `81379a62b9eb5611267e6ad9a97dd18da95946f8bd523c1f4d870d209334a014`

</details>

## Source tables

[Read all source tables with merged cells and notes](tables.md).

## Checks and limitations

Source links checked: 45 figure/table-reference edges. Table cells with source XPaths: 146. Unresolved figure/table references: 0.

These are structural/provenance checks. The examples were checked against source text; they are not independently human-adjudicated gold labels. Figure semantics and model-training benefit have not been measured. See [provenance and image checksums](provenance.json).

## Attribution

Authors: Kim Lecomte, Pieter Hertens, Virginie Wylleman, Annagiada Toniolo, Febe Roelandt, Fleur Boone, Maarten Ciers, Lien Verboom, Katrien Staes, Geert van Loo, Esther Hoste.

[Original article](https://pmc.ncbi.nlm.nih.gov/articles/PMC13651886/) · [Original PDF](https://pmc-oa-opendata.s3.amazonaws.com/PMC13651886.1/PMC13651886.1.pdf?md5=32582d7f44efc799cd17ff56f85a4719) · [Original XML](https://pmc-oa-opendata.s3.amazonaws.com/PMC13651886.1/PMC13651886.1.xml?md5=7cf5e1877e967283fba2253723de5c14).

License: **CC BY**. Figures, captions and source excerpts are attributed to the original authors; original figure credits are retained.

https://creativecommons.org/licenses/by/4.0/This is an open-access article distributed under the terms of the Creative Commons Attribution license, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.
