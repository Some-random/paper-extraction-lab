# Actual training-record previews

[Paper overview](README.md)

These records were produced by the pipeline; no model was trained. The text uses the cached Qwen-family tokenizer for a 2,048-token packing demonstration. A future training backbone needs its own tokenizer. Image segments have not been vision-tokenized.

## One complete text chunk

Record `PMC13651886:text001` · **1743 tokens** · 5 source fragment(s).

```text
OTULIN was initially identified as a modulator of canonical Wnt signaling regulating embryonic angiogenesis (17). To determine whether OTULIN and linear (de)ubiquitination modulate Wnt responses in adult tissues, we analyzed Wnt signaling in the skin of mice with OTULIN-deficient KCs (∆^(Ker)OTULIN mice). We previously demonstrated that ∆^(Ker)OTULIN mice develop inflamed skin lesions that progress into well-differentiated squamous carcinomas (12, 13). Gene ontology (GO) enrichment analysis of our published single-cell RNA sequencing (scRNA-seq) dataset comparing total skin of wild-type (WT; Cre-negative OTULIN^(FL/FL)) and ∆^(Ker)OTULIN mice (12) revealed Wnt signaling as one of the top down-regulated GO terms in OTULIN-deficient KCs (Fig. 1A and fig. S1A). When probing expression levels of specific Wnt mediators in our scRNA-seq dataset, we indeed observed marked down-regulation in OTULIN-deficient KCs relative to control KCs (Fig. 1B). Quantitative polymerase chain reaction (qPCR) analysis of epidermal tail lysates confirmed the down-regulation of Wnt target genes in ∆^(Ker)OTULIN epidermis (Fig. 1C and Table 1). In agreement, expression levels of several members of the TCF/LEF family, key downstream mediators of canonical Wnt signaling, were also significantly reduced in ∆^(Ker)OTULIN epidermis (Fig. 1D). Immunoblotting for nonphosphorylated β-catenin, indicative of stabilized β-catenin and active Wnt signaling, confirmed reduced Wnt activation in epidermal tail lysates from ∆^(Ker)OTULIN relative to control mice (Fig. 1E). Wnt activation in KCs from adult skin is most prominent during the growth phase of HFs, also referred to as anagen, culminating in nuclear expression of LEF1 (20, 27). Immunofluorescence staining of anagen skin indicated nuclear LEF1 in WT HFs, whereas no nuclear LEF1 was observed in anagen-like HFs in lesional ∆^(Ker)OTULIN skin (Fig. 1F and Table 2). When probing HF cell populations (outer and inner layer, bulge and upper HF) of our scRNA-seq data for Wnt target gene expression, the down-regulation of Wnt target gene expression in OTULIN-deficient KCs was even more pronounced than in the total KC population (Fig. 1G). In addition to OTULIN, SHARPIN has also been implicated in stabilizing β-catenin (28). Therefore, we quantified expression levels of Wnt mediators and target genes in SHARPIN^(cpdm/cpdm) epidermis and control epidermis. Down-regulation of canonical Wnt signaling was observed in SHARPIN^(cpdm/cpdm) epidermis, supporting a role for linear ubiquitination in promoting Wnt signaling in adult KCs (fig. S1B). β-catenin also performs Wnt-independent roles at the plasma membrane (29). We assessed the levels of cytosolic β-catenin in OTULIN-deficient and control epidermis and observed higher levels in control epidermis, indicating that OTULIN promotes canonical Wnt signaling in the skin (fig. S1C). Together, these data demonstrate that OTULIN promotes canonical Wnt signaling in adult KCs.

Wnt signaling is down-regulated in OTULIN-deficient KCs. (A) Left: UMAP clustering of scRNA-seq data obtained from cells isolated from ∆^(Ker)OTULIN and control skin (12), highlighting the KC cluster. Right: GO enrichment analysis of genes significantly down-regulated in OTULIN-deficient KCs relative to control KCs. (B) Violin plots showing distribution of expression of the indicated Wnt target genes in scRNA-seq data of KCs from OTULIN^(FL/FL) and ∆^(Ker)OTULIN skin. (C) qPCR analysis for the indicated Wnt target genes on epidermal tail lysates of OTULIN^(FL/FL) and Δ^(Ker)OTULIN mice (aged 8 to 11 weeks). Data are means ±SEM, ^(∗)P < 0.05; ^(∗∗)P < 0.01; ^(∗∗∗)P < 0.001. (D) qPCR analysis for the indicated Wnt effector genes on epidermal tail lysates of OTULIN^(FL/FL) and Δ^(Ker)OTULIN mice. Data are means ± SEM, ^(∗)P < 0.05; ^(∗∗)P < 0.01; ^(∗∗∗)P < 0.001. Violin plots showing distribution of expression of the indicated genes in scRNA-seq data of HF KCs from OTULIN^(FL/FL) and ∆^(Ker)OTULIN skin. (E) Immunoblotting for nonphosphorylated (active) β-catenin and OTULIN in epidermal tail lysates from OTULIN^(FL/FL) and ∆^(Ker)OTULIN mice. α-Actin is shown as loading control. (F) Immunofluorescence images of LEF1 staining in OTULIN^(FL/FL) anagen skin and ∆^(Ker)OTULIN lesional skin. Top panels are hematoxylin and eosin (H&E)–stained skin sections from the same mice. Scale bars, 100 μm (top); 50 μm (bottom). (G) Violin plots showing distribution of expression of the indicated genes in scRNA-seq data of HF KCs from OTULIN^(FL/FL) and ∆^(Ker)OTULIN skin.

List of mouse-specific qPCR primers.

Table 1.
Gene	Forward primer	Reverse primer
Axin2	CTCACCCATTTACCCAGGACC	GTTCCTGTCCCTCTGCTGAC
Ctnnb	CACAGCTCCTTCCCTGAGTG	GCCCTCATCTAGCGTCTCAG
Bmp4	CCTGCAGCGATCCAGTCTCT	ACTACGGAATGGCTCCATT
Gja1	CCAAGGAGTTCCACCACTTTG	CCATGTCTGGGCACCTCTCT
Id2	CTGGGCAAGACGATCATCCTT	CCCTTCTGAGCTTATGTCGAATG
Lef1	GAT CCC CTT CAA GGA CGA AG	GGC TTG TCT GAC CAC CTC AT
Lgr5	TCTTCACCTCCTACCTGGACCT	GGCGTAGTCTGCTATGTGGTGT
Lrp6	CTGAATGCTGACAACAGGACCTG	GACGTTCCGAAGGCTGTGGATA
Tcf3	CCATGCTAGGTGACGGCTCTTC	GCGAGCCATTAACCTCAGATCC
Tcf4	CCTCCAATCCTTCAACTCCTGTG	TCCAAACGGTCTTCGATTCGGC
Tcf7	ATCCTTGATGCTGGGATTCTG	CTTCTCTTGCCTTGGGTTCTG
Hprt1	AGTGTTGGATACAGGCCAGAC	CGTGATTCAAATCCCTGAAGT
Matrin3	TGG ACC AAG AGG AAA TCT GG	TGA ACA ACT CGG CTG GTT TC
Eef1a1	TCGCCTTGGACGTTCTTTT	GTGGACTTGCCGGAATCTAC


List of antibodies.
```

## One figure/table–context record

Context segments keep source order. Figures/tables are attached only through explicit article references; shared context is emitted once in this record.

```json
{
  "id": "PMC13651886:interleaved000",
  "context_policy": "consecutive_source_paragraphs_in_same_section; explicit_xref_only",
  "source_xml_sha256": "81379a62b9eb5611267e6ad9a97dd18da95946f8bd523c1f4d870d209334a014",
  "segments": [
    {
      "type": "text",
      "role": "article_context",
      "block_id": "PMC13651886:block0004",
      "text": "OTULIN was initially identified as a modulator of canonical Wnt signaling regulating embryonic angiogenesis (17). To determine whether OTULIN and linear (de)ubiquitination modulate Wnt responses in adult tissues, we analyzed Wnt signaling in the skin of mice with OTULIN-deficient KCs (∆^(Ker)OTULIN mice). We previously demonstrated that ∆^(Ker)OTULIN mice develop inflamed skin lesions that progress into well-differentiated squamous carcinomas (12, 13). Gene ontology (GO) enrichment analysis of our published single-cell RNA sequencing (scRNA-seq) dataset comparing total skin of wild-type (WT; Cre-negative OTULIN^(FL/FL)) and ∆^(Ker)OTULIN mice (12) revealed Wnt signaling as one of the top down-regulated GO terms in OTULIN-deficient KCs (Fig. 1A and fig. S1A). When probing expression levels of specific Wnt mediators in our scRNA-seq dataset, we indeed observed marked down-regulation in OTULIN-deficient KCs relative to control KCs (Fig. 1B). Quantitative polymerase chain reaction (qPCR) analysis of epidermal tail lysates confirmed the down-regulation of Wnt target genes in ∆^(Ker)OTULIN epidermis (Fig. 1C and Table 1). In agreement, expression levels of several members of the TCF/LEF family, key downstream mediators of canonical Wnt signaling, were also significantly reduced in ∆^(Ker)OTULIN epidermis (Fig. 1D). Immunoblotting for nonphosphorylated β-catenin, indicative of stabilized β-catenin and active Wnt signaling, confirmed reduced Wnt activation in epidermal tail lysates from ∆^(Ker)OTULIN relative to control mice (Fig. 1E). Wnt activation in KCs from adult skin is most prominent during the growth phase of HFs, also referred to as anagen, culminating in nuclear expression of LEF1 (20, 27). Immunofluorescence staining of anagen skin indicated nuclear LEF1 in WT HFs, whereas no nuclear LEF1 was observed in anagen-like HFs in lesional ∆^(Ker)OTULIN skin (Fig. 1F and Table 2). When probing HF cell populations (outer and inner layer, bulge and upper HF) of our scRNA-seq data for Wnt target gene expression, the down-regulation of Wnt target gene expression in OTULIN-deficient KCs was even more pronounced than in the total KC population (Fig. 1G). In addition to OTULIN, SHARPIN has also been implicated in stabilizing β-catenin (28). Therefore, we quantified expression levels of Wnt mediators and target genes in SHARPIN^(cpdm/cpdm) epidermis and control epidermis. Down-regulation of canonical Wnt signaling was observed in SHARPIN^(cpdm/cpdm) epidermis, supporting a role for linear ubiquitination in promoting Wnt signaling in adult KCs (fig. S1B). β-catenin also performs Wnt-independent roles at the plasma membrane (29). We assessed the levels of cytosolic β-catenin in OTULIN-deficient and control epidermis and observed higher levels in control epidermis, indicating that OTULIN promotes canonical Wnt signaling in the skin (fig. S1C). Together, these data demonstrate that OTULIN promotes canonical Wnt signaling in adult KCs.",
      "source_xpath": "/article/body/sec[2]/sec[1]/p"
    },
    {
      "type": "image",
      "visual_id": "PMC13651886:F1",
      "assets": [
        {
          "image": "assets/sciadv.adz0181-f1.webp",
          "sha256": "0870b4bc8fcfcdca16c069c3d506fe0d22c1c6220960b71a7fb44083a7bb3940",
          "source_url": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13651886.1/sciadv.adz0181-f1.webp?md5=d85d9681aaf013aafb05d01490ab0f32"
        }
      ]
    },
    {
      "type": "text",
      "role": "source_caption",
      "visual_id": "PMC13651886:F1",
      "text": "Wnt signaling is down-regulated in OTULIN-deficient KCs. (A) Left: UMAP clustering of scRNA-seq data obtained from cells isolated from ∆^(Ker)OTULIN and control skin (12), highlighting the KC cluster. Right: GO enrichment analysis of genes significantly down-regulated in OTULIN-deficient KCs relative to control KCs. (B) Violin plots showing distribution of expression of the indicated Wnt target genes in scRNA-seq data of KCs from OTULIN^(FL/FL) and ∆^(Ker)OTULIN skin. (C) qPCR analysis for the indicated Wnt target genes on epidermal tail lysates of OTULIN^(FL/FL) and Δ^(Ker)OTULIN mice (aged 8 to 11 weeks). Data are means ±SEM, ^(∗)P < 0.05; ^(∗∗)P < 0.01; ^(∗∗∗)P < 0.001. (D) qPCR analysis for the indicated Wnt effector genes on epidermal tail lysates of OTULIN^(FL/FL) and Δ^(Ker)OTULIN mice. Data are means ± SEM, ^(∗)P < 0.05; ^(∗∗)P < 0.01; ^(∗∗∗)P < 0.001. Violin plots showing distribution of expression of the indicated genes in scRNA-seq data of HF KCs from OTULIN^(FL/FL) and ∆^(Ker)OTULIN skin. (E) Immunoblotting for nonphosphorylated (active) β-catenin and OTULIN in epidermal tail lysates from OTULIN^(FL/FL) and ∆^(Ker)OTULIN mice. α-Actin is shown as loading control. (F) Immunofluorescence images of LEF1 staining in OTULIN^(FL/FL) anagen skin and ∆^(Ker)OTULIN lesional skin. Top panels are hematoxylin and eosin (H&E)–stained skin sections from the same mice. Scale bars, 100 μm (top); 50 μm (bottom). (G) Violin plots showing distribution of expression of the indicated genes in scRNA-seq data of HF KCs from OTULIN^(FL/FL) and ∆^(Ker)OTULIN skin.",
      "source_xpath": "/article/body/sec[2]/sec[1]/fig"
    },
    {
      "type": "table",
      "visual_id": "PMC13651886:T1",
      "text_tsv": "Gene\tForward primer\tReverse primer\nAxin2\tCTCACCCATTTACCCAGGACC\tGTTCCTGTCCCTCTGCTGAC\nCtnnb\tCACAGCTCCTTCCCTGAGTG\tGCCCTCATCTAGCGTCTCAG\nBmp4\tCCTGCAGCGATCCAGTCTCT\tACTACGGAATGGCTCCATT\nGja1\tCCAAGGAGTTCCACCACTTTG\tCCATGTCTGGGCACCTCTCT\nId2\tCTGGGCAAGACGATCATCCTT\tCCCTTCTGAGCTTATGTCGAATG\nLef1\tGAT CCC CTT CAA GGA CGA AG\tGGC TTG TCT GAC CAC CTC AT\nLgr5\tTCTTCACCTCCTACCTGGACCT\tGGCGTAGTCTGCTATGTGGTGT\nLrp6\tCTGAATGCTGACAACAGGACCTG\tGACGTTCCGAAGGCTGTGGATA\nTcf3\tCCATGCTAGGTGACGGCTCTTC\tGCGAGCCATTAACCTCAGATCC\nTcf4\tCCTCCAATCCTTCAACTCCTGTG\tTCCAAACGGTCTTCGATTCGGC\nTcf7\tATCCTTGATGCTGGGATTCTG\tCTTCTCTTGCCTTGGGTTCTG\nHprt1\tAGTGTTGGATACAGGCCAGAC\tCGTGATTCAAATCCCTGAAGT\nMatrin3\tTGG ACC AAG AGG AAA TCT GG\tTGA ACA ACT CGG CTG GTT TC\nEef1a1\tTCGCCTTGGACGTTCTTTT\tGTGGACTTGCCGGAATCTAC",
      "source_xpath": "/article/body/sec[2]/sec[1]/table-wrap[1]"
    },
    {
      "type": "text",
      "role": "source_caption",
      "visual_id": "PMC13651886:T1",
      "text": "List of mouse-specific qPCR primers.",
      "source_xpath": "/article/body/sec[2]/sec[1]/table-wrap[1]"
    },
    {
      "type": "table",
      "visual_id": "PMC13651886:T2",
      "text_tsv": "Antibody\tConcentration\tManufacture\tCatalog number\tApplication\nCleaved caspase-3 [rowspan=2, colspan=1]\t1/500 [rowspan=2, colspan=1]\tCell Signaling Technology [rowspan=2, colspan=1]\t9661 [rowspan=2, colspan=1]\tImmunohistochemistry\n[merged from r1c0]\t[merged from r1c1]\t[merged from r1c2]\t[merged from r1c3]\tImmunofluorescence\nCleaved caspase-8\t1/500\tCell Signaling Technology\t9429\tImmunofluorescence\nKi67\t1/300\tInvitrogen\t14-5698-82\tImmunohistochemistry\nTcf4\t1/100\tSanta Cruz Biotechnology\tSC166699\tImmunofluorescence\nLef1\t1/200\tCell Signaling Technology\t2230S\tImmunofluorescence\nK10\t1/500\tInvitrogen\tMA5-42858\tImmunofluorescence\nK14\t1/500\tSanta Cruz Biotechnology\tsc53253\tImmunofluorescence\nTcf3\t1/500\tCell Signaling\t2883\tWestern blotting\nβ-Catenin\t1/2000\tBD Biosciences\t610153\tWestern blotting\nNon-P-β-catenin\t1/1000\tMerck\t05-665\tWestern blotting\nM1 Ubq\t1/2000 or 1/10 000\tSigma-Aldrich\tZRB2114-4X25UL (clone 1E3)\tWestern blotting\nOTULIN\t1/1000\tCell Signaling Technology\t14127\tWestern blotting\nHOIP\t1/1000\tGift of R. Damgaard\t\tWestern blotting\nSHARPIN\t1/1000\tProteintech\t14626-1-AP\tWestern blotting\nCaspase-3\t1/1000\tCell Signaling Technology\t9662\tWestern blotting\nACTIN-HRP\t1/10000\tSanta Cruz Biotechnology Biotechnology\tsc-47778\tWestern blotting\nAnti-rabbit HRP\t1/2500\tAmersham\tNA931\tWestern blotting\nAnti-mouse HRP\t1/2500\tAmersham\tNA934\tWestern blotting\nAnti-goat HRP\t1/2500\tAmersham\tSc-2354\tWestern blotting",
      "source_xpath": "/article/body/sec[2]/sec[1]/table-wrap[2]"
    },
    {
      "type": "text",
      "role": "source_caption",
      "visual_id": "PMC13651886:T2",
      "text": "List of antibodies.",
      "source_xpath": "/article/body/sec[2]/sec[1]/table-wrap[2]"
    }
  ],
  "status": "source_linked_candidate; not a validated image interpretation or generated reasoning trace"
}
```

## Exact text-fragment provenance

```json
[
  {
    "block_id": "PMC13651886:block0004",
    "source_xpath": "/article/body/sec[2]/sec[1]/p",
    "char_start": 0,
    "char_end": 2971
  },
  {
    "block_id": "PMC13651886:block0005",
    "source_xpath": "/article/body/sec[2]/sec[1]/fig/caption",
    "char_start": 0,
    "char_end": 1577
  },
  {
    "block_id": "PMC13651886:block0006",
    "source_xpath": "/article/body/sec[2]/sec[1]/table-wrap[1]/caption",
    "char_start": 0,
    "char_end": 36
  },
  {
    "block_id": "PMC13651886:block0007",
    "source_xpath": "/article/body/sec[2]/sec[1]/table-wrap[1]",
    "char_start": 0,
    "char_end": 759
  },
  {
    "block_id": "PMC13651886:block0008",
    "source_xpath": "/article/body/sec[2]/sec[1]/table-wrap[2]/caption",
    "char_start": 0,
    "char_end": 19
  }
]
```
