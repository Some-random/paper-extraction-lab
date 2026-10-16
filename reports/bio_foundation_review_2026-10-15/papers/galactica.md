# Galactica

[Biological pretraining review](../README.md)

Scientific model with disclosed biological data

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Pretraining from scratch. **Starting checkpoint:** Random weights; scientific decoder. [Initialization evidence](https://arxiv.org/html/2211.09085v1)

A broad scientific model with disclosed biological sources, not a biology-only model. The approximately 106B-token corpus and 450B training exposure are different quantities.

**Data included in the overview amounts:** Broad scientific corpus + general material. The headline includes several sciences, reference material and other text. Its entire dataset or training exposure must not be labeled biological tokens.

## Authors and institutions

**Authors:** Ross Taylor; Marcin Kardas; Guillem Cucurull; Thomas Scialom; Anthony Hartshorn; Elvis Saravia; Andrew Poulton; Viktor Kerkez; Robert Stojnic.

**Institutions:** Meta AI.

[Paper attribution](https://arxiv.org/html/2211.09085v1). Names and affiliations follow the reviewed paper version.

<a id="evidence-assessment"></a>

## Overall paper assessment

**Overall: Mixed.** A substantial scientific-language-model study with useful scaling and representation experiments. As an overall paper it is mixed: the system effort is valuable, but factual reliability and the interaction of corpus, scale and prompt pretraining leave broad use claims less convincing. This is our provisional technical judgment of the whole paper in its publication context, not an official review score or an independent replication.

**Contribution and originality:** A broad scientific language model with explicit citation and scientific-sequence representations is a substantial resource effort.

**Technical soundness:** The unified token-stream approach is coherent; prompt pretraining adds an additional factor beyond corpus choice.

**Evaluation:** Scaling and citation analyses are informative, while generated scientific text can still be unreliable.

**Reproducibility:** Detailed corpus appendices help; reproducing large-model behavior and isolating data effects remains demanding.

**Clarity and limitations:** The appendices are useful, but fluent scientific generation and reliable scientific assistance require different evidence.

Sources: [Reviewed paper: methods/results/limitations](https://arxiv.org/html/2211.09085v1)

## Paper-text origins

**Direct paper sources:** arXiv; PMC; PubMed abstracts; bioRxiv; OSF; medRxiv; ACL; PubAg abstracts; ChemRxiv.

**Paper text via reused datasets:** Semantic Scholar full text; Semantic Scholar abstracts.

Table 22 identifies the paper sources. Semantic Scholar imports remain existing-dataset input; the other named publication sources contribute to the reviewed direct-paper lower bound. [Source](https://arxiv.org/html/2211.09085v1)

## Other modalities

The paper describes protein, DNA and SMILES tokenization. Table 24 gives rounded record-level source budgets for UniProt, PubChem and RefSeq, including associated text and metadata. These are not pure modality-token counts; those shares remain NR. All are already included in the acquisition-route totals.

| Representation / domain | Reported tokens | Count definition |
|---|---:|---|
| Protein sequences | NR | Present; separate modality-token total NR. |
| DNA sequences | NR | Present in the described tokenization; separate modality-token total NR. |
| Molecular SMILES | NR | Present; separate modality-token total NR. |
| UniProt protein records | ≈600M | Table 24 source-record total, including annotations and text; not a pure protein-sequence count. |
| PubChem molecule records | ≈1B | Table 24 source-record total, including text and properties; not a pure SMILES count. |
| RefSeq genome records | ≈100M | Table 24 RefSeq Genome source-record total; not an independently separated DNA-only amount. |

Sources: [§2.1 / Table 24](https://arxiv.org/html/2211.09085v1)

## Existing-dataset sources

UniProt; PubChem; Papers with Code.

Named reused inputs relevant to the reviewed training stages. This is not necessarily exhaustive. A source name establishes provenance, not its token amount; unreported amounts remain NR. Directly collected PubMed/PMC text is described separately as online-paper input. [Source](https://arxiv.org/html/2211.09085v1)

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [Galactica](#token-counts-by-acquisition-route)<br>Scientific pretraining | Corpus · text + scientific sequences | ≥64.926B | ≥700M | ≥23.87B | ≈106B | [Tables 1, 22–25](https://arxiv.org/html/2211.09085v1) |
| [Galactica](#token-counts-by-acquisition-route)<br>Scientific pretraining | Training exposure · text + scientific sequences | NR | NR | NR | 450B | [§5.1](https://arxiv.org/html/2211.09085v1) |

**Scientific pretraining — Corpus (text + scientific sequences):** These are lower bounds from explicitly separable sources, summed at the published rounded precision. Direct repository sources are separated from Semantic Scholar imports. The 88B literature headline includes both routes and is not counted twice. Other reference, code and prompt material remains unallocated.

- **Online Papers: ≥64.926B.** arXiv, PMC, PubMed abstracts, bioRxiv, OSF, medRxiv, ACL, PubAg abstracts and ChemRxiv; Table 22. Additional academic PDFs from Common Crawl are not included in this lower bound. Calculation: (35 + 23 + 5 + 1 + 0.428 + 0.176 + 0.150 + 0.105 + 0.067) × 1000000000.

- **Web Urls: ≥700M.** ScientificCC webpages, Table 25, only. Other reference websites do not have a fully verified route allocation here.

- **Existing Datasets: ≥23.87B.** Semantic Scholar full texts/abstracts plus the individual knowledge-base rows; further reused inputs are not assigned here. Calculation: (18 + 4 + 1 + 0.6 + 0.1 + 0.07 + 0.05 + 0.03 + 0.01 + 0.01) × 1000000000.

- **Total: ≈106B.** Rounded published complete-corpus headline.

**Scientific pretraining — Training exposure (text + scientific sequences):** The paper reports 450B training tokens. No acquisition-route exposure split is reported; multiplying rounded corpus shares by 4.25 would create unreported values.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: 450B.** Reported training exposure, §5.1.

**Training stage:** Decoder pretraining from scratch

**Backbone:** Random weights; scientific decoder

**Source material and units:** Scientific papers plus biological/chemical records such as UniProt and PubChem

**Acquisition and document processing:** Serializes scientific data alongside text and citation titles. A broad science model with disclosed biological material, rather than a biology-only model.

## Source material

[Galactica](https://arxiv.org/pdf/2211.09085)

| Reported field | Retained source statement |
|---|---|
| Stage | Scientific decoder pretraining from scratch |
| Actual biological source material | Scientific papers plus biological/chemical records such as UniProt and PubChem |
| How the source becomes training data / relevant limitation | Serializes scientific data alongside text and citation titles. A broad science model with disclosed biological material, rather than a biology-only model. |

## Datasets and amounts

[Galactica](https://arxiv.org/pdf/2211.09085), science decoder from scratch, Tables 2/22–24

| Reported field | Retained source statement |
|---|---|
| Literature contribution | **88B tokens** from papers + abstracts, **83.0%** reported corpus share |
| Web / other dataset contribution | Filtered Common Crawl **1B**; reference material **7B** includes Wikipedia, StackExchange and educational websites/books; code **7B** |
| Quantitative limit | Knowledge bases **2B**, prompts **0.4B**, other **0.2B**; headline corpus **106B**, training **450B**, **4.25 epochs**. Rounded rows do not sum exactly to the headline |

## Citation handling

Galactica, scientific decoder pretraining from scratch

| Reported field | Retained source statement |
|---|---|
| Reported treatment | Represents citations with titles and author surnames between `[START_REF]` and `[END_REF]`. Reports better citation prediction with titles than IDs, alongside hallucination tradeoffs. This is a citation-representation precedent, not a CPT experiment. [§3.1.2](https://arxiv.org/pdf/2211.09085) |

## Source details and qualifications

Galactica explicitly discloses biological literature: **PMC 23B**, **PubMed abstracts 5B**, **bioRxiv 1B** tokens; these are components of the 88B literature bucket. Other listed literature: arXiv **35B**, Semantic Scholar full text **18B**, Semantic Scholar abstracts **4B**, plus smaller sources. Its biological knowledge bases include PubChem **1B**, UniProt **0.6B**, RefSeq **0.1B**, Ribosome **0.05B**, LIPID MAPS **0.03B**, Reactome **0.01B**. Biological material can also occur in broader sources, so this is not an exhaustive biological-total calculation. [Galactica, Tables 22/24](https://arxiv.org/pdf/2211.09085#page=42)

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/pdf/2211.09085)
- [Primary source retained from the existing review](https://arxiv.org/pdf/2211.09085#page=42)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
