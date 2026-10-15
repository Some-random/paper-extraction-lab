# Actual training-record previews

[Paper overview](README.md)

These records were produced by the pipeline; no model was trained. The text uses the cached Qwen-family tokenizer for a 2,048-token packing demonstration. A future training backbone needs its own tokenizer. Image segments have not been vision-tokenized.

## One complete text chunk

Record `PMC13645648:text004` · **1809 tokens** · 8 source fragment(s).

```text
Our RNA-seq analysis confirmed that Lsp2 is expressed in the heads of adult female flies; however, other storage proteins, with the exception of Lsp1b, exhibited much lower levels of expression (Fig. 3a,b). Notably, ePR led to a significant decrease in Lsp2 transcript levels in both the head and the abdominal carcass of adult flies at day 2 (Fig. 3b and Supplementary Table 4). We further corroborated this downregulation by quantitative PCR with reverse transcription (qRT–PCR), which showed that Lsp2 transcript levels were reduced in female heads at both day 2 and day 7 after eclosion, but had recovered by day 30 (Fig. 3c and Extended Data Fig. 5a). Proteomic analysis further identified Lsp2 as one of the most abundant proteins in the adult head, and showed that its levels were decreased by ePR (Fig. 3d and Supplementary Table 5). We confirmed the reduction of Lsp2 protein in the head at day 2 by western blot analysis (Extended Data Fig. 5b,c).

Larval protein restriction decreases Lsp2 in early life stages. a, Experimental workflow for adult transcriptome and proteome analyses after ePR. b, Average read counts (in counts per million; CPM) of genes encoding storage proteins, from transcriptome analysis in Canton-S female flies at adult day 2. n = 4. c,d, Lsp2 abundance at the mRNA level quantified by qRT–PCR (c, n = 8) and Lsp2 abundance at the protein level quantified by proteome analysis (d) in the heads of Canton-S female flies at adult day 2. a.u., arbitrary unit. e–g, Representative fluorescence images (e) and quantification (f,g) of Lsp2–muGFP reporter activity in larvae (e), pupae (f) and adult female flies (e,g). Scale bars, 1 mm. n = 10 (larvae and adults) or 8 (pupae). h–j, Experimental scheme (h) and qRT–PCR analysis of Lsp2 after larva-specific knockdown of Lsp2 (i), Lsp1a (j) or Fbp2 (j) using the fat-body driver Cg-Gal4 with tub-Gal80^(ts). n = 4 (i), 5 (j, Fbp2^(RNAi)) or 6 (j, Lsp2^(RNAi), Lsp1a^(RNAi)). k, Intensities of light- and heavy-labelled Lsp2 protein in the heads of Canton-S female flies on the indicated days, on the basis of the in vivo pSILAC described in Fig. 2i. n = 4. Data are mean ± s.e.m. (c,d,f,g,i,j) or mean ± s.d. (k). Symbols represent biological replicates. Statistical significance was determined by two-tailed Student’s t-test (c,d,i), two-way ANOVA with Šídák’s multiple comparison test (f,g), one-way ANOVA with Dunnett’s multiple comparison test (j) or two-sided Welch’s t-test with Benjamini–Hochberg correction (k). Source data

To visualize Lsp2 protein dynamics with greater precision, we generated Lsp2-monomeric ultrastable green fluorescent protein (muGFP) knock-in flies using CRISPR–Cas9. As expected, Lsp2–muGFP was systemically detected during the late larval stage (Fig. 3e), with levels gradually declining throughout the pupal and early-adult stages (Fig. 3f,g). Notably, ePR further reduced Lsp2–muGFP intensity across all of these developmental stages (Fig. 3e–g).

Given the observed reduction in adult Lsp2 mRNA and protein levels, we first hypothesized that Lsp2 transcription might be constitutively downregulated from the larval stage onwards. However, Lsp2 mRNA expression remained unaffected by ePR during the wandering larval and early pupal stages, showing a significant decrease only from day 4 of the pupal stage (Extended Data Fig. 5d).

To test whether larval levels of Lsp2 protein directly influence subsequent expression in adulthood, we transiently knocked down Lsp2 in the larval fat body using the Cg-Gal4 driver combined with temperature-sensitive Gal80 (Gal80^(ts)). This larval-specific knockdown was sufficient to reduce Lsp2 mRNA expression in early adults (Fig. 3h,i). Notably, when we knocked down genes that encode other major storage proteins, including Larval serum protein 1α (Lsp1a) and Fat body protein 2 (Fbp2), using RNA interference (RNAi) lines previously verified for their specificity [bib_ref]A temporal allocation of amino acid resources ensures fitness and body allometry in Drosophila — Valzania et al.[/bib_ref] , Lsp2 expression in adult flies was significantly decreased (Fig. 3j). This manipulation did not cause apparent defects in fat-body development (Extended Data Fig. 5e–h). These results suggest the existence of a feed-forward regulatory mechanism that maintains storage-protein expression, a concept also demonstrated in the accompanying study [bib_ref]Lsp2 links mTORC1 to TOP mRNA translation and lifespan in Drosophila — Wang et al.[/bib_ref] .

We used a combination of in vivo pSILAC and ePR to study the turnover of Lsp2 protein in early adulthood. In control flies, Lsp2 at day 1 was predominantly light labelled (larva-derived), and was gradually replaced by heavy-labelled (adult-derived) Lsp2 over time (Fig. 3k and Supplementary Table 2). By day 6, the heavy-labelled fraction exceeded the light-labelled pool. As expected, the levels of light-labelled Lsp2 were significantly lower in ePR-flies across all time points (days 1, 2, 3 and 6), confirming a reduced carryover of larval protein reserves. Notably, the levels of heavy-labelled Lsp2 were also significantly lower in ePR-flies than they were in control flies during the first three days of adulthood (Fig. 3k), indicating that ePR suppresses both the legacy of larval Lsp2 and its de novo synthesis in early adulthood.

Collectively, these results support a model of ‘nutritional memory’ driven by ePR: protein restriction during larval development triggers a sustained reduction in Lsp2 at both the mRNA and the protein level that persists into adulthood. Because storage proteins constitute a crucial reservoir of amino acids for the synthesis of new proteins during the non-feeding pupal stage, the depletion of Lsp2 is likely to constrain the production of cytoRPs during metamorphosis. This deficit in cytoRPs is then carried over into early adulthood, in which it limits global translation capacity, potentially leading to lifespan extension. Furthermore, the observation that de novo Lsp2 synthesis remains suppressed in adult ePR-flies suggests that Lsp2 exerts other regulatory influences beyond its conventional role as an amino acid source during metamorphosis.

To test the functional contribution of Lsp2 to the phenotypes observed in ePR-flies, we performed fat-body-specific knockdown of Lsp2. We found that Lsp2 knockdown by RNAi throughout the larval and adult stages resulted in a lighter body colour, particularly in the abdominal pigmentation, mirroring the effect observed under ePR (Fig. 4a). Of note, knockdown of Lsp2 did not affect adult body weight in nutrient-rich conditions, but reduced it significantly in the context of a low-protein diet, suggesting that Lsp2 acts as a buffering system to maintain growth during limited protein intake (Fig. 4b). In contrast to ePR, Lsp2 knockdown did not significantly compromise early-adult female fecundity (Extended Data Fig. 6a,b) or ovariole number (Extended Data Fig. 6c), which indicates that the developmental and reproductive deficits induced by ePR are not mediated by Lsp2. In addition, abdominal insulin signalling was unaffected by Lsp2 knockdown (Extended Data Fig. 6d–g), whereas ATF4 activity was persistently increased during development (Extended Data Fig. 6h,i).
```

## One figure/table–context record

Context segments keep source order. Figures/tables are attached only through explicit article references; shared context is emitted once in this record.

```json
{
  "id": "PMC13645648:interleaved006",
  "context_policy": "consecutive_source_paragraphs_in_same_section; explicit_xref_only",
  "source_xml_sha256": "592a9c913492a9d1cf3b650b8b3c68347bc691966831d0257b8dfb4837c8f320",
  "segments": [
    {
      "type": "text",
      "role": "article_context",
      "block_id": "PMC13645648:block0030",
      "text": "To test the functional contribution of Lsp2 to the phenotypes observed in ePR-flies, we performed fat-body-specific knockdown of Lsp2. We found that Lsp2 knockdown by RNAi throughout the larval and adult stages resulted in a lighter body colour, particularly in the abdominal pigmentation, mirroring the effect observed under ePR (Fig. 4a). Of note, knockdown of Lsp2 did not affect adult body weight in nutrient-rich conditions, but reduced it significantly in the context of a low-protein diet, suggesting that Lsp2 acts as a buffering system to maintain growth during limited protein intake (Fig. 4b). In contrast to ePR, Lsp2 knockdown did not significantly compromise early-adult female fecundity (Extended Data Fig. 6a,b) or ovariole number (Extended Data Fig. 6c), which indicates that the developmental and reproductive deficits induced by ePR are not mediated by Lsp2. In addition, abdominal insulin signalling was unaffected by Lsp2 knockdown (Extended Data Fig. 6d–g), whereas ATF4 activity was persistently increased during development (Extended Data Fig. 6h,i).",
      "source_xpath": "/article/body/sec[7]/p[1]"
    },
    {
      "type": "image",
      "visual_id": "PMC13645648:Fig4",
      "assets": [
        {
          "image": "assets/41586_2026_11031_Fig4_HTML.webp",
          "sha256": "e74a6bc1518d599c02f38934d62078cf3f27ec1d98d3c44cd829755aedc11612",
          "source_url": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13645648.1/41586_2026_11031_Fig4_HTML.webp?md5=ef739866ef6e9a57c6e38c918abdd72f"
        }
      ]
    },
    {
      "type": "text",
      "role": "source_caption",
      "visual_id": "PMC13645648:Fig4",
      "text": "Knockdown of Lsp2 suppresses early-adult translation and extends lifespan. a, Adult female flies at day 0 with Lsp2 knockdown using the fat-body driver Cg-Gal4. Scale bars, 1 mm. b, Body weight of female flies at day 1 with Lsp2 knockdown (r^(4)-Gal4). n = 30. c–f, Volcano (c,e) and box (d,f) plots showing differential protein abundance in larvae at 96 h AEL (c,d) or in white prepupae (e,f). CytoRPs and mitoRPs are highlighted in red and blue, respectively. n = 4,511 (all), 76 (cytoRPs) and 57 (mitoRPs) in d, and 6,921 (all), 85 (cytoRPs) and 71 (mitoRPs) in f. g, Experimental workflow for in vivo pSILAC combined with Lsp2 knockdown (KD). h, Intensities of heavy- and medium-labelled cytoRPs, mitoRPs, histones and Lsp2 in the heads of female flies at days 3 and 6. n = 4. a.u., arbitrary unit. i,j, Volcano (i) and box (j) plots showing differential protein abundance in the heads of adult female flies at day 4 after larval- and pupal-specific Lsp2 knockdown (Cg-Gal4, tub-Gal80^(ts)). n = 8,115 (all), 83 (cytoRPs) and 72 (mitoRPs). k,l, Representative immunoblot (k) and quantification (l) of protein synthesis in the heads of female flies at day 3–4 after larval- and pupal-specific Lsp2 knockdown. n = 3. m, Survival curves of female flies with larval-specific Lsp2 knockdown (Cg-Gal4, tub-Gal80^(ts)). n,o, Volcano (n) and box (o) plots showing differential protein abundance in adult heads at day 2 after adult-specific (day 0–2) Lsp2 knockdown. n = 8,114 (all), 83 (cytoRPs) and 72 (mitoRPs). p,q, Representative immunoblot (p) and quantification (q) of protein synthesis in the heads of female flies at day 2–3 after adult-specific (day 0–3) Lsp2 knockdown. n = 3. r, Survival curves and median lifespan (inset) of female flies after adult-specific Lsp2 knockdown using the inducible fat-body driver WBFB^(GS). RU486 (200 μM) was administered either during the first week or throughout adulthood. Error bars indicate 95% confidence intervals (r). Sample sizes (n) for lifespan experiments are indicated. Data are mean ± s.e.m. (b,l,q); mean ± s.d. (h); or box plots showing the median, quartiles and range (d,f,j,o). Symbols represent biological replicates. Statistical significance was determined by one-way ANOVA with Šídák’s multiple comparison test (b), two-sided Wilcoxon rank-sum test (c–f,i,j,n,o), two-sided Welch’s t-test with Benjamini–Hochberg correction (h), two-tailed Student’s t-test (l,q) or log-rank test (m,r). Source data",
      "source_xpath": "/article/body/sec[7]/p[1]/fig"
    },
    {
      "type": "image",
      "visual_id": "PMC13645648:Fig11",
      "assets": [
        {
          "image": "assets/41586_2026_11031_Fig11_ESM.webp",
          "sha256": "4e5949ec89a250d02f04970b90f49ec0c46c28a96ef078b354b58d29b9538935",
          "source_url": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13645648.1/41586_2026_11031_Fig11_ESM.webp?md5=562a90d72f456ccaebf42655caf91ddc"
        }
      ]
    },
    {
      "type": "text",
      "role": "source_caption",
      "visual_id": "PMC13645648:Fig11",
      "text": "Effects of Lsp2 knockdown on reproduction and nutritional signalling pathways. a, Daily fecundity of females from adult day 5 to 9 with larval-specific Lsp2 knockdown using fat body driver Cg-Gal4 combined with tub-Gal80^(ts). n = 10. b, Fecundity of female flies at adult day 4–5 with Lsp2 knockdown using fat body driver r^(4)-Gal4 combined with ePR. n = 10. c, Ovariole number per ovary in female flies at adult day 9 with Lsp2 knockdown using r^(4)-Gal4. n = 10. d–g, Representative immunoblots (d,f) and quantification (e,g) of Akt phosphorylation levels in adult abdominal carcasses of adult female flies with Lsp2 knockdown using fat body driver Cg-Gal4 (d,e) or Cg-Gal4 combined with tub-Gal80^(ts) (f,g). For transient manipulation (f,g), knockdown was performed during the larval stage. Samples were collected at adult day 2 (d,e) or day 6 (f,g). Antibodies used are anti-phosphorylated Akt (pAkt) and anti-histone H3 (loading control). n = 3. h,i, Quantification of ATF4 reporter (4E-BP^(intron)-dsRed) fluorescence in whole larvae and pupae (h) or adult abdomens (i) with Lsp2 knockdown using fat-body driver Cg-Gal4. n = 10. Data are presented as mean ± s.e.m. Symbols represent biological replicates. Statistical significance was determined by two-way ANOVA with Šídák’s multiple comparison test (a,h,i), one-way ANOVA with Šídák’s multiple comparison test (b), or a two-tailed Student’s t-test (c,e,g). Source data",
      "source_xpath": "/article/back/app-group/app/sec/p[6]/fig"
    },
    {
      "type": "text",
      "role": "article_context",
      "block_id": "PMC13645648:block0032",
      "text": "To characterize the organismal response to Lsp2 loss of function, we performed transcriptome, proteome and in vivo pSILAC analyses in Lsp2-RNAi flies. As expected, we observed a trend towards the transcriptional suppression of cytoRPs, whereas mitoRP genes remained unaffected (Supplementary Table 4). Proteomic analysis of Lsp2-knockdown flies revealed the suppression of both cytoRPs and metabolic proteins (Extended Data Fig. 7a–k and Supplementary Table 3), which is reminiscent of the effects of ePR. Unlike what is seen with ePR, mitoRPs are also downregulated by Lsp2-RNAi (Extended Data Fig. 7a,b,d,e), which is also reported in the accompanying paper [bib_ref]Lsp2 links mTORC1 to TOP mRNA translation and lifespan in Drosophila — Wang et al.[/bib_ref] . Notably, Lsp2 knockdown did not affect the levels of cytoRPs during the larval stage, but it reduced them by the prepupal stage, suggesting that the Lsp2-dependent regulation of cytoRPs begins during metamorphosis (Fig. 4c–f, Extended Data Fig. 8a–h and Supplementary Table 3). Consistent with this, in vivo pSILAC analysis revealed that larva-derived cytoRPs were decreased by Lsp2 knockdown, whereas adult-derived cytoRPs seemed instead to be increased (Fig. 4g,h, Extended Data Fig. 8i and Supplementary Table 2). This increase could be due to increased food intake or the compensatory incorporation of adult-derived amino acids. Lsp2 knockdown also decreased the levels of larva-derived mitoRPs (Fig. 4h). Therefore, its effect on the translation process might be more extensive than that of ePR.",
      "source_xpath": "/article/body/sec[7]/p[2]"
    },
    {
      "type": "image",
      "visual_id": "PMC13645648:Fig12",
      "assets": [
        {
          "image": "assets/41586_2026_11031_Fig12_ESM.webp",
          "sha256": "f61288df7c187b385b3b40d7e1aa2b7f64fba8deece0e34426a26f9d75116d40",
          "source_url": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13645648.1/41586_2026_11031_Fig12_ESM.webp?md5=cc19598dabbd3c6ee1bc151e94f094f2"
        }
      ]
    },
    {
      "type": "text",
      "role": "source_caption",
      "visual_id": "PMC13645648:Fig12",
      "text": "Comprehensive proteomic profiling of adult fly heads after Lsp2 knockdown. a–c, Differential protein abundance in adult female heads at day 2 following Lsp2 knockdown using the r^(4)-Gal4 driver, compared to the w^(CS) genetic control. Data are presented as a volcano plot (a), a corresponding box plot showing log_(2) fold changes for all proteins (n = 6258), cytoRPs (n = 82), and mitoRPs (n = 72) (b), and GO enrichment analysis of significantly downregulated proteins (c; P < 0.01 and log_(2) r^(4)>Lsp2^(RNAi) / w^(CS)>Lsp2^(RNAi) < −0.1). d–f, Differential protein abundance in adult female heads at day 2 following Lsp2 knockdown compared to the UAS-lacZ^(RNAi) control. Data include a volcano plot (d), a box plot for specific protein categories (e), and GO enrichment analysis of downregulated proteins (f; P < 0.01 and log_(2) r^(4)>Lsp2^(RNAi) / r^(4)>lacZ^(RNAi) < −0.1). g,h, Quality control metrics for the proteomic dataset, including the number of quantified proteins per sample (g) and the distribution of log_(2) protein intensities across replicates (h). The number of proteins quantified in each sample: Out of 6,778 total identified proteins, 6,258 proteins were consistently quantified across all six biological replicates in at least one condition and included in the analysis. The number of proteins included in the box plots corresponds to that shown in g. i, Relative abundance (log_(2) fold change) of averaged levels of Lsp2 and Gapdh1 (control) proteins derived from the proteomic dataset with Lsp2 knockdown using fat-body driver r^(4)-Gal4. Error bars indicate 95% confidence intervals. j,k, Pearson correlation matrix (j) and PCA plot (k) demonstrating high reproducibility among biological replicates. Data are presented as box plots (b,e,h) or as mean ± s.d. (i). Box plots in b,e show the median (centre line), the interquartile range (box), and the minimum and maximum values (whiskers). Box plots in h show the median (centre line), the interquartile range (box), and the smallest and largest values within 1.5× the interquartile range (whiskers). Values beyond the whiskers are shown as individual points. Symbols represent biological replicates. Statistical significance was determined by a two-sided Wilcoxon rank-sum test (a,b,d,e). Source data",
      "source_xpath": "/article/back/app-group/app/sec/p[7]/fig"
    },
    {
      "type": "image",
      "visual_id": "PMC13645648:Fig13",
      "assets": [
        {
          "image": "assets/41586_2026_11031_Fig13_ESM.webp",
          "sha256": "aedbcdf0fd2cb564d5761a843dcfe78240909cbc572a4c9eea51515167a42f24",
          "source_url": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13645648.1/41586_2026_11031_Fig13_ESM.webp?md5=96465248174ce4b6ab49ccfb688b6f29"
        }
      ]
    },
    {
      "type": "text",
      "role": "source_caption",
      "visual_id": "PMC13645648:Fig13",
      "text": "The effect of Lsp2 knockdown on proteome, translation, and lifespan. a–d, Quality control metrics for the larval proteome dataset, including the number of quantified proteins (a), distribution of log_(2) protein intensities (b), PCA plot (c) and Pearson correlation matrix (d) of individual biological replicates. Proteins quantified across all six replicates in at least one condition were included in the analysis. The number of proteins included in the box plots corresponds to that shown in a. e–h, Quality control metrics for the white prepupal proteome dataset, including the number of quantified proteins (e), log_(2) protein intensities (f), PCA plot (g) and Pearson correlation matrix (h). The number of proteins included in the box plots corresponds to that shown in e. i, Multi-scatter plots showing the correlation of log_(2) (heavy/medium) ratios between biological replicates, demonstrating high experimental reproducibility. j,k, Representative immunoblot (j) and quantification (k) of protein synthesis (SUnSET assay) in the heads of female flies at day 2–3 with Lsp2-knockdown using fat-body driver Cg-Gal4. Anti-puromycin antibody is used. n = 3. l, Survival curves of female flies with Lsp2 knockdown using fat-body driver Cg-Gal4 or control (w^(CS)). Cg-Gal4 is backcrossed to w^(CS) for eight generations. m,n, Survival curves (m) and median lifespan (n) of female flies with Lsp2 knockdown using fat-body driver r^(4)-Gal4 or control (w^(CS)) combined with ePR. r^(4)-Gal4 is backcrossed to w^(CS) for eight generations. Error bars in n represent 95% confidence intervals. Sample sizes (n) for lifespan experiments are indicated within the respective panels. Data are presented as box plots (b,f) or as mean ± s.e.m. (k). Box plots in b,f show the median (centre line), the interquartile range (box), and the smallest and largest values within 1.5× the interquartile range (whiskers). Values beyond the whiskers are shown as individual points. Symbols represent biological replicates. Statistical significance was determined by a two-tailed Student’s t-test (k) or a log-rank test (l–n). Source data",
      "source_xpath": "/article/back/app-group/app/sec/p[8]/fig"
    },
    {
      "type": "text",
      "role": "article_context",
      "block_id": "PMC13645648:block0033",
      "text": "Like ePR-flies, Lsp2 knockdown flies exhibited suppressed translation activity in early adulthood (Extended Data Fig. 8j,k). Consistently, knockdown of Lsp2 extended the adult lifespan of female flies (Extended Data Fig. 8l–n). The lifespan extension observed with Lsp2-RNAi was comparable with that induced by ePR, and ePR did not further increase lifespan when combined with Lsp2-RNAi (Extended Data Fig. 8m,n), which suggests that the two manipulations share a mechanism of lifespan extension. Together, these findings indicate that Lsp2 has a central role in mediating the effects of ePR on adult translation and lifespan, but not growth, fecundity or insulin signalling.",
      "source_xpath": "/article/body/sec[7]/p[3]"
    },
    {
      "type": "text",
      "role": "article_context",
      "block_id": "PMC13645648:block0034",
      "text": "Although Lsp2 knockdown and ePR are likely to share their mechanism of lifespan extension, whether early-life Lsp2 alone is sufficient to regulate lifespan remains unclear. Depleting larva-derived Lsp2 by using Gal80^(ts) (Cg^(ts)>Lsp2^(RNAi)) reduced both cytoRP levels and translation activity in early adulthood (Fig. 4i–l, Extended Data Fig. 9a–d and Supplementary Table 3), and was sufficient to extend female lifespan (Fig. 4m and Extended Data Fig. 9e). To exclude potential genetic background issues, we generated a pGnmt-GeneSwitch (pGnmt^(GS)) fly line by using the promoter sequence of the metabolic gene Gnmt, which is highly expressed in fat bodies [bib_ref]Necrosis-driven systemic immune response alters SAM metabolism through the FOXO–GNMT axis — Obata et al.[/bib_ref] . Crossing this line with UAS-GFP confirmed that the expression of pGnmt^(GS) was almost entirely confined to adipose tissue and was RU486-inducible (Extended Data Fig. 9f,g). As expected, knocking down Lsp2 in larvae using pGnmt^(GS) decreased translation in female flies (Extended Data Fig. 9h,i) and extended the lifespan of both males and females (Extended Data Fig. 9j,k), although the suppression of translation was weaker than that seen with the Cg^(ts) driver (70% versus 47% of control). It is possible that, because wandering larvae were not fed RU486-containing food, the phenotype was not as strong as that achieved by Lsp2 knockdown throughout the larval to pupal stages. Nevertheless, these results prove that decreasing Lsp2 levels only in the larval stage suppresses protein translation and extends lifespan.",
      "source_xpath": "/article/body/sec[7]/p[4]"
    },
    {
      "type": "image",
      "visual_id": "PMC13645648:Fig14",
      "assets": [
        {
          "image": "assets/41586_2026_11031_Fig14_ESM.webp",
          "sha256": "6bd365ab410a1f79eefdb3ba7bfc202023ccf26f0d3fabfab3a9b45cb87ec94d",
          "source_url": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13645648.1/41586_2026_11031_Fig14_ESM.webp?md5=227654d95540e826ce648d510dde3011"
        }
      ]
    },
    {
      "type": "text",
      "role": "source_caption",
      "visual_id": "PMC13645648:Fig14",
      "text": "Effects of time-restricted Lsp2 knockdown on proteome and lifespan. a–d, Quality control metrics for the proteomic dataset of heads of adult female flies at day 4 with larval and pupal-specific Lsp2 knockdown using fat-body driver Cg-Gal4 combined with tub-Gal80^(ts). Data include the number of quantified proteins (a), distribution of log_(2) protein intensities (b), PCA plot (c) and Pearson correlation matrix (d). The number of proteins included in the box plots corresponds to that shown in a. e, Survival curves of female flies with larval-specific Lsp2 knockdown using fat-body driver Cg-Gal4 combined with tub-Gal80^(ts). UAS-lacZ^(RNAi) and UAS-Lsp2^(RNAi) are backcrossed to w^(CS) flies for eight generations. f,g, Representative fluorescence images of whole larvae (f) and larval fat body (g) showing RU486-induced GFP expression using the pGnmt^(GS) driver. Scale bar = 1 mm. The similar result was repeatedly obtained at least twice. h,i, Representative immunoblot (h) and quantification (i) of protein synthesis (SUnSET assay) in the heads of female flies at day 2–3 with larval-specific Lsp2 knockdown using larval fat-body driver pGnmt^(GS). Anti-puromycin antibody is used. n = 3. j,k, Survival curves of female (j) or male (k) flies with larval-specific Lsp2 knockdown using larval fat-body driver pGnmt^(GS). l–o, Quality control metrics for the proteomic dataset of adult female heads at day 2 with adult-specific Lsp2 knockdown (day 0–2) using fat-body driver Cg-Gal4 combined with tub-Gal80^(ts). Data include the number of quantified proteins (l), distribution of log_(2) protein intensities (m), PCA plot (n) and Pearson correlation matrix (o). The number of proteins included in the box plots corresponds to that shown in l. p, Survival curves of male flies with adult-specific Lsp2 knockdown using adult fat-body driver WBFB^(GS) during the first week of adulthood. Sample sizes (n) for lifespan experiments are indicated within the respective panels. Data are presented as box plots (b,m) or as mean ± s.e.m. (i). Box plots in b,m show the median (centre line), the interquartile range (box), and the smallest and largest values within 1.5× the interquartile range (whiskers). Values beyond the whiskers are shown as individual points. Symbols represent biological replicates. Statistical significance was determined by a log-rank test (e,j,k,p) or a two-tailed Student’s t-test (i). Source data",
      "source_xpath": "/article/back/app-group/app/sec/p[9]/fig"
    },
    {
      "type": "text",
      "role": "article_context",
      "block_id": "PMC13645648:block0035",
      "text": "Considering that larval Lsp2 regulates adult Lsp2 expression through a feed-forward response (Fig. 3h–j), it remained possible that decreasing Lsp2 protein specifically during the early adult stage could be sufficient to suppress translation capacity and extend lifespan. To test this possibility, we performed early-adult-specific Lsp2 knockdown in the adult fat body. Notably, proteome analysis suggested that cytoRPs were not decreased by adult-specific Lsp2 knockdown (Fig. 4n,o, Extended Data Fig. 9l–o and Supplementary Table 3). In this experiment, the decrease in Lsp2 was not as strong as that seen with developmental Lsp2 knockdown, further confirming that larval carryover Lsp2 is still present in early adulthood (Fig. 4n). However, this manipulation resulted in a marked decrease in translation (Fig. 4p,q). This indicates that Lsp2 protein in early adulthood regulates translation independently of cytoRP abundance. In the control-diet condition, fat-body-specific knockdown of Lsp2 restricted to the first week of adulthood using WBFB-GeneSwitch (WBFB^(GS)) significantly extended female lifespan (Fig. 4r; 8% ethanol versus 8% 1 week RU486 (hereafter, RU)). Early-adult Lsp2 knockdown also extended lifespan in male flies (Extended Data Fig. 9p). Treating flies with RU for their entire adult life led to an increase in lifespan that was similar to that observed with 1 week RU (Fig. 4r; 8% 1 week RU versus 8% RU). There was no statistical significance between adult-lifelong Lsp2 knockdown (8% RU) and early-adult-specific Lsp2 knockdown (8% 1 week RU), although median lifespan for the 8% RU condition (67 days) was greater than that for the 8%-1-week-RU condition (63 days) (Fig. 4r). As expected, ePR alone extended female lifespan in the absence of RU feeding (Fig. 4r; 8% ethanol versus 1% ethanol), and adult-lifelong Lsp2 knockdown did not extend lifespan any further (Fig. 4r; 1% ethanol versus 1% RU), which suggests that ePR extends lifespan via Lsp2. By contrast, when ePR was combined with early-adult-specific Lsp2 knockdown, lifespan was shortened (Fig. 4r; 1% ethanol versus 1% 1 week RU). We assume that the combination of ePR and transient suppression of Lsp2 during early adulthood renders flies susceptible to the life-shortening effects of Lsp2 that emerge later in life once Lsp2 expression is restored.",
      "source_xpath": "/article/body/sec[7]/p[5]"
    },
    {
      "type": "image",
      "visual_id": "PMC13645648:Fig3",
      "assets": [
        {
          "image": "assets/41586_2026_11031_Fig3_HTML.webp",
          "sha256": "cf705f7a32399fb3eb2e0555a8e9b940bba20ce7c91a99d537e58f2404db0b27",
          "source_url": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13645648.1/41586_2026_11031_Fig3_HTML.webp?md5=10c13a599db2d0fccf9f8b409161018b"
        }
      ]
    },
    {
      "type": "text",
      "role": "source_caption",
      "visual_id": "PMC13645648:Fig3",
      "text": "Larval protein restriction decreases Lsp2 in early life stages. a, Experimental workflow for adult transcriptome and proteome analyses after ePR. b, Average read counts (in counts per million; CPM) of genes encoding storage proteins, from transcriptome analysis in Canton-S female flies at adult day 2. n = 4. c,d, Lsp2 abundance at the mRNA level quantified by qRT–PCR (c, n = 8) and Lsp2 abundance at the protein level quantified by proteome analysis (d) in the heads of Canton-S female flies at adult day 2. a.u., arbitrary unit. e–g, Representative fluorescence images (e) and quantification (f,g) of Lsp2–muGFP reporter activity in larvae (e), pupae (f) and adult female flies (e,g). Scale bars, 1 mm. n = 10 (larvae and adults) or 8 (pupae). h–j, Experimental scheme (h) and qRT–PCR analysis of Lsp2 after larva-specific knockdown of Lsp2 (i), Lsp1a (j) or Fbp2 (j) using the fat-body driver Cg-Gal4 with tub-Gal80^(ts). n = 4 (i), 5 (j, Fbp2^(RNAi)) or 6 (j, Lsp2^(RNAi), Lsp1a^(RNAi)). k, Intensities of light- and heavy-labelled Lsp2 protein in the heads of Canton-S female flies on the indicated days, on the basis of the in vivo pSILAC described in Fig. 2i. n = 4. Data are mean ± s.e.m. (c,d,f,g,i,j) or mean ± s.d. (k). Symbols represent biological replicates. Statistical significance was determined by two-tailed Student’s t-test (c,d,i), two-way ANOVA with Šídák’s multiple comparison test (f,g), one-way ANOVA with Dunnett’s multiple comparison test (j) or two-sided Welch’s t-test with Benjamini–Hochberg correction (k). Source data",
      "source_xpath": "/article/body/sec[6]/p[2]/fig"
    }
  ],
  "status": "source_linked_candidate; not a validated image interpretation or generated reasoning trace"
}
```

## Exact text-fragment provenance

```json
[
  {
    "block_id": "PMC13645648:block0023",
    "source_xpath": "/article/body/sec[6]/p[2]",
    "char_start": 0,
    "char_end": 957
  },
  {
    "block_id": "PMC13645648:block0024",
    "source_xpath": "/article/body/sec[6]/p[2]/fig/caption",
    "char_start": 0,
    "char_end": 1550
  },
  {
    "block_id": "PMC13645648:block0025",
    "source_xpath": "/article/body/sec[6]/p[3]",
    "char_start": 0,
    "char_end": 449
  },
  {
    "block_id": "PMC13645648:block0026",
    "source_xpath": "/article/body/sec[6]/p[4]",
    "char_start": 0,
    "char_end": 382
  },
  {
    "block_id": "PMC13645648:block0027",
    "source_xpath": "/article/body/sec[6]/p[5]",
    "char_start": 0,
    "char_end": 1152
  },
  {
    "block_id": "PMC13645648:block0028",
    "source_xpath": "/article/body/sec[6]/p[6]",
    "char_start": 0,
    "char_end": 839
  },
  {
    "block_id": "PMC13645648:block0029",
    "source_xpath": "/article/body/sec[6]/p[7]",
    "char_start": 0,
    "char_end": 852
  },
  {
    "block_id": "PMC13645648:block0030",
    "source_xpath": "/article/body/sec[7]/p[1]",
    "char_start": 0,
    "char_end": 1074
  }
]
```
