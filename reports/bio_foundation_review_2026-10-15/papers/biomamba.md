# BioMamba

[Biological pretraining review](../README.md)

Biomedical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Continued pretraining. **Starting checkpoint:** Mamba2 checkpoints, 130M–2.7B. [Initialization evidence](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/)

Reported packed sequence counts imply positions, not measured non-padding tokens or unique corpus size.

**Data included in the overview amounts:** Biomedical papers + general replay. The paper-derived stream is PubMed text. The existing-dataset component is C4 and Wikipedia general replay; all reported amounts here are inferred packed positions.

## Authors and institutions

**Authors:** Ling Yue; Mingzhi Zhu; Sixue Xing; Yunning Cao; Yanbo Wang; Vijil Chenthamarakshan; Shaowu Pan; Payel Das; Tianfan Fu.

**Institutions:** Rensselaer Polytechnic Institute; IBM Research; Jiaxing New Jies Thermal Power Co. Ltd.; North University of China; Nanjing University.

[Paper attribution](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/). Names and affiliations follow the reviewed paper version.

<a id="evidence-assessment"></a>

## Overall paper assessment

**Overall: Mixed.** A useful exploration of biomedical adaptation of Mamba, but predominantly incremental. Inconsistent corpus accounting and incomplete checkpoint availability reduce confidence in its reproducibility and overall completeness. This is our provisional technical judgment of the whole paper in its publication context, not an official review score or an independent replication.

**Contribution and originality:** Tests a relevant non-Transformer backbone in a biomedical setting; the adaptation method itself is conventional.

**Technical soundness:** Base/adapted comparisons and tokenizer control are sensible design choices.

**Evaluation:** Domain and general-capability checks add value; the findings remain tied to the selected tasks and scales.

**Reproducibility:** The author repository still describes future checkpoint release, and sequence-count/mix discrepancies need resolution.

**Clarity and limitations:** The overall recipe is understandable, but corpus and release statements should be more internally consistent.

Sources: [Reviewed paper: methods/results/limitations](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/) · [Author repository: checkpoint release status](https://github.com/lingyue404/BioMamba#model-checkpoints)

## Paper-text origins

**Direct paper sources:** PubMed/MEDLINE.

**Paper text via reused datasets:** No reused paper-text source established for this row.

This overview follows the published paper’s PubMed/MEDLINE corpus description. The current author repository additionally names processed PubMed inputs; different releases must not be assumed to share the same token counts. [Source](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/)

## Other modalities

The reviewed training stage uses ordinary text rather than separately represented images, biological sequences or 3D structure tokens.

Sources: [Reviewed paper: data and representations](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/)

## Existing-dataset sources

C4; English Wikipedia.

Named reused inputs relevant to the reviewed training stages. This is not necessarily exhaustive. A source name establishes provenance, not its token amount; unreported amounts remain NR. Directly collected PubMed/PMC text is described separately as online-paper input. [Source](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/)

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [BioMamba](#token-counts-by-acquisition-route)<br>CPT | Packed token positions · token positions | ≈434.176M | 0 | ≈86.016M | ≈520.192M | [Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/) |

**CPT — Packed token positions (token positions):** Derived from approximately 424K PubMed, 42K C4 and 42K Wikipedia sequences of length 1024. These are packed positions, not a measured count of non-padding content tokens. The source sequence proportions conflict with its nominal 80/10/10 mixture; the discrepancy is retained.

- **Online Papers: ≈434.176M.** PubMed packed positions; approximate source sequence count. Calculation: 424000 × 1024.

- **Web Urls: 0.** C4 and Wikipedia are named source corpora, not a newly described live crawl.

- **Existing Datasets: ≈86.016M.** C4 and Wikipedia packed positions. Calculation: (42000 + 42000) × 1024.

- **Total: ≈520.192M.** Total packed positions from the table, before any repeated epochs. Calculation: 508000 × 1024.

**Training stage:** CPT, then downstream SFT

**Backbone:** Mamba2 checkpoints, 130M–2.7B

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
