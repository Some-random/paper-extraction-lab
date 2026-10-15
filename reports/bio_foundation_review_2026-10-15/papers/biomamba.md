# BioMamba

[Shared literature catalog](../README.md)

Biomedical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** CPT, then downstream SFT

**Backbone:** Mamba2, 130M through 2.7B

**Source material and units:** PubMed MEDLINE abstracts with C4 and English Wikipedia; approximately 508K packed 1,024-token sequences in the reported final corpus.

**Acquisition and document processing:** Abstract text; these are not 508K newly OCRed PDFs.

**Cleaning and filtering:** Tokenization/filtering/shuffling; fixed held-out language-model sets and a separate small-model mixture pilot.

**Training unit and mixture:** Reported target PubMed:C4:WIKIPEDIA mixture 80:10:10; three epochs. Table sequence counts are approximate and do not reproduce that percentage exactly.

**Generated or augmented material:** General-text replay; core CPT does not require teacher-generated paper summaries.

**Author-reported evidence:** Tokenizer-controlled base/adapted comparisons; general MCQ scores within ±3 percentage points and C4 perplexity changes at most 0.17 in reported comparisons.

**Disclosure gaps:** Paper claims released checkpoints; inspected author README still says forthcoming and uses a different license. Verify availability before planning reproduction.

**Source sections:** Materials and Methods; Table 1; public author README

## Datasets and amounts

[BioMamba, 2026 published report](https://spj.science.org/doi/10.34133/hds.0454), Table 1 / Methods; [author repository](https://github.com/lingyue404/BioMamba)

| Reported field | Retained source statement |
|---|---|
| Actual training stage | Mamba2 continued pretraining |
| Literature text | PubMed abstracts, nominal **80%** |
| Web / other sources and amounts | C4 **10%**, Wikipedia **10%**, nominal mixture; approximately **508K × 1,024 sequence positions**, three epochs |
| Disclosure limits | Table also gives approximately **424K / 42K / 42K sequences**, implying about **83.5% / 8.3% / 8.3%**, inconsistent with nominal proportions. Approximately **0.520B corpus positions / 1.56B three-epoch positions** are derived, not reported distinct tokens |

## Source details and qualifications

BioMamba's downstream clinical-note experiments are outside our data scope. The literature-CPT mixture is included because it directly addresses abstracts versus general replay. The 2026 published Mamba2 recipe should not be silently conflated with numbers from the earlier 2024 BioMamba preprint. The table retains the source's internal count/proportion discrepancy rather than repairing it. [Published report](https://spj.science.org/doi/10.34133/hds.0454)

## Primary sources

- [Published BioMamba paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/)
- [Author repository inspected](https://github.com/lingyue404/BioMamba)
- [Primary source retained from the existing review](https://spj.science.org/doi/10.34133/hds.0454)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
