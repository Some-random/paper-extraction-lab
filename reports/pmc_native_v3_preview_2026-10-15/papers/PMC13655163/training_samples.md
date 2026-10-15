# Actual training-record previews

[Paper overview](README.md)

These records were produced by the pipeline; no model was trained. The text uses the cached Qwen-family tokenizer for a 2,048-token packing demonstration. A future training backbone needs its own tokenizer. Image segments have not been vision-tokenized.

## One complete text chunk

Record `PMC13655163:text000` · **1811 tokens** · 7 source fragment(s).

```text
Understanding the genetic architecture of the circulating proteome can help determine if a protein is causally linked to disease. Previous large-scale genome-wide association studies of proteins have mostly been conducted on pre-defined, targeted subsets of the proteome, and have often concentrated on low-abundance proteins, many of which don’t exert their main function in serum. Mass spectrometry-based proteomics facilitates the study of high-abundance proteins and their isoforms, focusing on proteins active in blood. In 15035 individuals from Generation Scotland, we perform genome-wide association studies of 439 highly abundant serum protein groups as identified and quantified by liquid chromatography tandem mass spectrometry. We identify 1553 independent SNP signals for 398 proteins (P < 1.2×10^(−10)). Two-sample Mendelian Randomisation analyses are applied to test if the 398 proteins with significant SNP signals are causally associated with 79 common causes of morbidity and mortality. We report putative causal associations between 13 proteins and 17 outcomes, including neuropsychiatric and cardiovascular conditions. Large-scale genome-wide analyses of the high-abundance proteome complement targeted approaches for the discovery of causal pathways of disease.

The circulating proteome can capture a readout of lifestyle and environmental exposures and inform disease risk prediction^(1). As a consequence, serum proteins are used as biomarkers in several conditions, such as cardiac Troponin I and T to indicate myocardial infarction^(2), cystatin C to indicate kidney dysfunction^(3), C-reactive protein to indicate inflammation^(4), or prostate-specific antigen as a marker of prostate cancer^(5). In addition to biomarker work, understanding the genetic architecture of blood-based proteins helps to determine causal disease mechanisms and identify drug targets^(6).

To date, large-scale studies have used targeted aptamer- or affinity-based platforms that can assess upwards of 3000 (Olink Explore 3072 panel) and 7000 (SomaLogic SomaScan assay) pre-defined proteins^(7–9). Genome-wide association studies (GWAS) of these proteins have helped to give mechanistic insights into multiple disease outcomes—including those where blood is not the primary tissue of interest^(10–13). However, affinity assay-based techniques have limitations. Quantification of functionally important, high-abundance serum proteins can be inaccurate due to signals exceeding the dynamic range of the array and the presence of different isoforms^(14). They are also limited by a pre-defined list of protein targets, off-target binding and interference caused by autoantibodies^(15), as well as lack of concordance across arrays^(16). In contrast, untargeted approaches for proteomics such as mass spectrometry are unbiased and yield comprehensive and granular coverage of the high-abundance proteome. This non-reliance on an epitope confers higher analytical specificity relative to affinity-based methods and enables direct interrogation of protein isoforms and peptide-level variation. When integrated with genomic data, this resolution facilitates direct mapping of genetic variation to specific peptides and proteins, offering a deeper mechanistic view of genotype-protein relationships. To date, only a small number of studies have performed GWAS on mass spectrometry-measured proteins. However, their sample sizes have been limited to under 3000 individuals^(9,17,18). This is an important limitation as GWAS typically require large sample sizes to achieve adequate statistical power to detect variants with small effect sizes.

Recently, we and others have developed an ultra-high-throughput mass spectrometry proteomic technology that can measure proteins and peptides in excess of 200 samples per day, while advances in sample processing and data analysis have increasingly mitigated the impact of problematic batch effects^(19). The application of this technology to large population biobanks will accelerate insights into the genetic control of the human proteome by providing an unprecedented scale and accuracy of protein quantification^(6).

Here, we characterise the genetic architecture of 439 mass spectrometry-measured proteins in 15,035 individuals from the Generation Scotland study. This study is 5–10 times larger than recently published GWAS of mass spectrometry proteomics^(9,17,18). First, we identify genetic variants that associate with mean differences in serum protein levels (i.e. protein quantitative trait loci, or pQTLs). Second, harnessing these data, we perform Mendelian Randomisation (MR) to explore causal associations between protein levels and 79 leading causes of morbidity and mortality^(20,21). Together, we leverage unbiased protein measurements to provide a catalogue of genetic influences on serum protein levels as well as detail their causal associations with prevalent disease states.

GWAS analyses of 439 serum proteins (mapped to one UniProt ID) or protein groups (mapped to multiple UniProt IDs) levels were conducted using data from 15,035 participants from Generation Scotland. We observed 199,489 genome-wide significant (P < 1.2 × 10^(−10)) SNP associations with 398 (91%) of the proteins/protein groups. Following conditional analysis, 1553 independent signals were identified with the lead variant defined as the SNP with the lowest P-value within the given locus (Supplementary Data 1). 1199 of the significant pQTLs were found in uniquely mapped proteins (i.e, non-protein groups), 656 (54.7%) of which were cis (±1 Mb), and 543 (45.3%) trans (Fig. 1A). Over 40% of discovered pQTLs (404 cis and 200 trans) were associated with a single protein. Our results also indicated the presence of a pQTL hotspot within SERPINA1, with 17 independent signals generating 181 associations with 140 proteins. 71 proteins/protein groups had only one independent pQTL whilst 48 protein/protein groups had seven or more (Fig. 1B). When comparing effect size with minor allele frequency, a negative correlation (for cis loci: r_(Pearson) = −0.60, P = 1.0 × 10^(−64); for trans loci: r_(Pearson) = −0.72, P = 3.6 × 10^(−88)) between the log beta and the log MAF was observed (Fig. 1C). In general, for the same MAF, larger effect sizes were found with cis loci than with trans (Fig. 1C). An inverse association (r_(Pearson) = −0.15, P = 1.8 × 10^(−4)) was found between strength of cis pQTL and distance from transcription start site (Fig. 1D). The pQTL analysis was repeated to include a SNP-sex interaction term to test for sex differences in genetic effects. One significant association (P < 1.2 × 10^(−10)) was found: a cis locus in Ceruloplasmin (CP) (Supplementary Data 2). This locus remained significant after running a sensitivity analysis which included contraception as a covariate to determine if the signal was being driven by hormonal contraceptive use.

Genome-wide association studies to identify pQTLs for highly abundant proteins as measured by mass spectrometry. A The x-axis represents the chromosomal location of independent cis and trans pQTLs. The y-axis represents the position of the gene encoding the protein. Only uniquely mapped proteins are shown. Cis associations for proteins are marked by orange circles and trans associations (not linked to any protein targets) are marked by purple circles. B The number of independent pQTLs per protein (or protein group). C Association between the common logarithm of minor allele frequencies and the natural logarithm of absolute effect sizes for cis and trans pQTLs. Only uniquely mapped proteins are shown. Cis (orange circles and line); trans (purple circles and line). D Association between the strength of cis pQTL associations and their distance in kilobases (kb) from their respective transcription start sites. pQTL protein quantitative trait locus, kb kilobases. Source data are provided as a Source Data file.
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
    "block_id": "PMC13655163:block0000",
    "source_xpath": "/article/front/article-meta/abstract[1]",
    "char_start": 0,
    "char_end": 1281
  },
  {
    "block_id": "PMC13655163:block0002",
    "source_xpath": "/article/body/sec[1]/p[1]",
    "char_start": 0,
    "char_end": 609
  },
  {
    "block_id": "PMC13655163:block0003",
    "source_xpath": "/article/body/sec[1]/p[2]",
    "char_start": 0,
    "char_end": 1743
  },
  {
    "block_id": "PMC13655163:block0004",
    "source_xpath": "/article/body/sec[1]/p[3]",
    "char_start": 0,
    "char_end": 519
  },
  {
    "block_id": "PMC13655163:block0005",
    "source_xpath": "/article/body/sec[1]/p[4]",
    "char_start": 0,
    "char_end": 777
  },
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
  }
]
```
