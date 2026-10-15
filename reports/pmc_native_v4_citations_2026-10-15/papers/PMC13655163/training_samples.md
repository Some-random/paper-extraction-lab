# Actual training-record previews

[Paper overview](README.md)

These records were produced by the pipeline; no model was trained. The text uses the cached Qwen-family tokenizer for a 2,048-token packing demonstration. A future training backbone needs its own tokenizer. Image segments have not been vision-tokenized.

## One complete text chunk

Record `PMC13655163:text001` · **1626 tokens** · 5 source fragment(s).

```text
GWAS analyses of 439 serum proteins (mapped to one UniProt ID) or protein groups (mapped to multiple UniProt IDs) levels were conducted using data from 15,035 participants from Generation Scotland. We observed 199,489 genome-wide significant (P < 1.2 × 10^(−10)) SNP associations with 398 (91%) of the proteins/protein groups. Following conditional analysis, 1553 independent signals were identified with the lead variant defined as the SNP with the lowest P-value within the given locus (Supplementary Data 1). 1199 of the significant pQTLs were found in uniquely mapped proteins (i.e, non-protein groups), 656 (54.7%) of which were cis (±1 Mb), and 543 (45.3%) trans (Fig. 1A). Over 40% of discovered pQTLs (404 cis and 200 trans) were associated with a single protein. Our results also indicated the presence of a pQTL hotspot within SERPINA1, with 17 independent signals generating 181 associations with 140 proteins. 71 proteins/protein groups had only one independent pQTL whilst 48 protein/protein groups had seven or more (Fig. 1B). When comparing effect size with minor allele frequency, a negative correlation (for cis loci: r_(Pearson) = −0.60, P = 1.0 × 10^(−64); for trans loci: r_(Pearson) = −0.72, P = 3.6 × 10^(−88)) between the log beta and the log MAF was observed (Fig. 1C). In general, for the same MAF, larger effect sizes were found with cis loci than with trans (Fig. 1C). An inverse association (r_(Pearson) = −0.15, P = 1.8 × 10^(−4)) was found between strength of cis pQTL and distance from transcription start site (Fig. 1D). The pQTL analysis was repeated to include a SNP-sex interaction term to test for sex differences in genetic effects. One significant association (P < 1.2 × 10^(−10)) was found: a cis locus in Ceruloplasmin (CP) (Supplementary Data 2). This locus remained significant after running a sensitivity analysis which included contraception as a covariate to determine if the signal was being driven by hormonal contraceptive use.

Genome-wide association studies to identify pQTLs for highly abundant proteins as measured by mass spectrometry. A The x-axis represents the chromosomal location of independent cis and trans pQTLs. The y-axis represents the position of the gene encoding the protein. Only uniquely mapped proteins are shown. Cis associations for proteins are marked by orange circles and trans associations (not linked to any protein targets) are marked by purple circles. B The number of independent pQTLs per protein (or protein group). C Association between the common logarithm of minor allele frequencies and the natural logarithm of absolute effect sizes for cis and trans pQTLs. Only uniquely mapped proteins are shown. Cis (orange circles and line); trans (purple circles and line). D Association between the strength of cis pQTL associations and their distance in kilobases (kb) from their respective transcription start sites. pQTL protein quantitative trait locus, kb kilobases. Source data are provided as a Source Data file.

The significant pQTLs discovered in our study were compared to three previous proteomics GWAS. These include two large-scale affinity-based proteomics GWAS using Olink Explore 3072 PEA in the UK Biobank [bib_ref]Plasma proteomic associations with genetics and health in the UK Biobank — Sun et al.[/bib_ref] and SomaScan v4 in the deCODE study [bib_ref]Large-scale plasma proteomics comparisons through genetics and disease associations — Eldjarn et al.[/bib_ref] , and a smaller-scale mass-spectrometry proteomics GWAS using the MS-based Seer Proteograph platform in the Tarkin study [bib_ref]A genome-wide association study of mass spectrometry proteomics using a nanoparticle enrichment platform — Suhre et al.[/bib_ref] . For all significant pQTLs in the current study, we performed lookup analyses in these studies, where the same protein was assessed and also demonstrated significant associations. We replicated 46 of 199 (23.12%), 64 of 275 (23.27%) and 10 of 25 (40%) pQTLs with the Sun et al. [bib_ref]Plasma proteomic associations with genetics and health in the UK Biobank — Sun et al.[/bib_ref] , Eldjarn et al. [bib_ref]Large-scale plasma proteomics comparisons through genetics and disease associations — Eldjarn et al.[/bib_ref] , and Suhre et al. [bib_ref]A genome-wide association study of mass spectrometry proteomics using a nanoparticle enrichment platform — Suhre et al.[/bib_ref] , studies, respectively (see Table 1). Effect sizes of the overlapping associations correlated highly between platforms (R_(Pearson) = 0.94 (MS:UKB [bib_ref]Plasma proteomic associations with genetics and health in the UK Biobank — Sun et al.[/bib_ref] )); 0.90 (MS:deCODE cohort [bib_ref]Large-scale plasma proteomics comparisons through genetics and disease associations — Eldjarn et al.[/bib_ref] ); 0.89 (MS:Tarkin [bib_ref]A genome-wide association study of mass spectrometry proteomics using a nanoparticle enrichment platform — Suhre et al.[/bib_ref] ) (Fig. 2). A list of the overlapping proteins-SNP associations can be found in Supplementary Data 3, 4 and 5.

Overlapping associations with comparator pQTL studies. Overlapping associations were defined as those where the genome-wide significant lead variant from the comparator study was within 1 Mb of the discovered lead variant, with a same direction effect size, and has an LD score of >0.6. “MS GWAS” refers to the current study. R denotes Pearson R, calculated using cor.test from the Statistics package in R. A 10 overlapping pQTLs with the Seer proteomics GWAS (Suhre et al. [bib_ref]A genome-wide association study of mass spectrometry proteomics using a nanoparticle enrichment platform — Suhre et al.[/bib_ref] ); B 64 overlapping pQTLs with the Icelandic SomaScan v4 platform GWAS (Eldjarn et al. [bib_ref]Large-scale plasma proteomics comparisons through genetics and disease associations — Eldjarn et al.[/bib_ref] ); C 46 overlapping pQTLs with the UK Biobank GWAS (Sun et al. [bib_ref]Plasma proteomic associations with genetics and health in the UK Biobank — Sun et al.[/bib_ref] ). Source data are provided as a Source Data file.

Comparison of discovery pQTLs with three comparator studies
```

## One figure/table–context record

Context segments keep source order. Figures/tables are attached only through explicit article references; shared context is emitted once in this record.

```json
{
  "id": "PMC13655163:interleaved000",
  "context_policy": "consecutive_source_paragraphs_in_same_section; explicit_xref_only",
  "source_xml_sha256": "97e641a7dc4d071addad7783390ce524d62b1987d247f4508e3f9bd712d83784",
  "segments": [
    {
      "type": "text",
      "role": "article_context",
      "block_id": "PMC13655163:block0006",
      "text": "GWAS analyses of 439 serum proteins (mapped to one UniProt ID) or protein groups (mapped to multiple UniProt IDs) levels were conducted using data from 15,035 participants from Generation Scotland. We observed 199,489 genome-wide significant (P < 1.2 × 10^(−10)) SNP associations with 398 (91%) of the proteins/protein groups. Following conditional analysis, 1553 independent signals were identified with the lead variant defined as the SNP with the lowest P-value within the given locus (Supplementary Data 1). 1199 of the significant pQTLs were found in uniquely mapped proteins (i.e, non-protein groups), 656 (54.7%) of which were cis (±1 Mb), and 543 (45.3%) trans (Fig. 1A). Over 40% of discovered pQTLs (404 cis and 200 trans) were associated with a single protein. Our results also indicated the presence of a pQTL hotspot within SERPINA1, with 17 independent signals generating 181 associations with 140 proteins. 71 proteins/protein groups had only one independent pQTL whilst 48 protein/protein groups had seven or more (Fig. 1B). When comparing effect size with minor allele frequency, a negative correlation (for cis loci: r_(Pearson) = −0.60, P = 1.0 × 10^(−64); for trans loci: r_(Pearson) = −0.72, P = 3.6 × 10^(−88)) between the log beta and the log MAF was observed (Fig. 1C). In general, for the same MAF, larger effect sizes were found with cis loci than with trans (Fig. 1C). An inverse association (r_(Pearson) = −0.15, P = 1.8 × 10^(−4)) was found between strength of cis pQTL and distance from transcription start site (Fig. 1D). The pQTL analysis was repeated to include a SNP-sex interaction term to test for sex differences in genetic effects. One significant association (P < 1.2 × 10^(−10)) was found: a cis locus in Ceruloplasmin (CP) (Supplementary Data 2). This locus remained significant after running a sensitivity analysis which included contraception as a covariate to determine if the signal was being driven by hormonal contraceptive use.",
      "source_xpath": "/article/body/sec[2]/sec[1]/p"
    },
    {
      "type": "image",
      "visual_id": "PMC13655163:Fig1",
      "assets": [
        {
          "image": "assets/41467_2026_76474_Fig1_HTML.webp",
          "sha256": "8285693636e299f40730029c9d7f99ed9d57d6640ef6297d9e1928d7bd85ea44",
          "source_url": "https://pmc-oa-opendata.s3.amazonaws.com/PMC13655163.1/41467_2026_76474_Fig1_HTML.webp?md5=6a7228699e30731663fac6fee9c97f61"
        }
      ]
    },
    {
      "type": "text",
      "role": "source_caption",
      "visual_id": "PMC13655163:Fig1",
      "text": "Genome-wide association studies to identify pQTLs for highly abundant proteins as measured by mass spectrometry. A The x-axis represents the chromosomal location of independent cis and trans pQTLs. The y-axis represents the position of the gene encoding the protein. Only uniquely mapped proteins are shown. Cis associations for proteins are marked by orange circles and trans associations (not linked to any protein targets) are marked by purple circles. B The number of independent pQTLs per protein (or protein group). C Association between the common logarithm of minor allele frequencies and the natural logarithm of absolute effect sizes for cis and trans pQTLs. Only uniquely mapped proteins are shown. Cis (orange circles and line); trans (purple circles and line). D Association between the strength of cis pQTL associations and their distance in kilobases (kb) from their respective transcription start sites. pQTL protein quantitative trait locus, kb kilobases. Source data are provided as a Source Data file.",
      "source_xpath": "/article/body/sec[2]/sec[1]/p/fig"
    }
  ],
  "status": "source_linked_candidate; not a validated image interpretation or generated reasoning trace"
}
```

## Exact text-fragment provenance

```json
[
  {
    "block_id": "PMC13655163:block0006",
    "source_xpath": "/article/body/sec[2]/sec[1]/p",
    "char_start": 0,
    "char_end": 1975
  },
  {
    "block_id": "PMC13655163:block0007",
    "source_xpath": "/article/body/sec[2]/sec[1]/p/fig/caption",
    "char_start": 0,
    "char_end": 1020
  },
  {
    "block_id": "PMC13655163:block0008",
    "source_xpath": "/article/body/sec[2]/sec[2]/p",
    "char_start": 0,
    "char_end": 2071
  },
  {
    "block_id": "PMC13655163:block0009",
    "source_xpath": "/article/body/sec[2]/sec[2]/p/fig/caption",
    "char_start": 0,
    "char_end": 1038
  },
  {
    "block_id": "PMC13655163:block0010",
    "source_xpath": "/article/body/sec[2]/sec[2]/p/table-wrap/caption",
    "char_start": 0,
    "char_end": 59
  }
]
```
