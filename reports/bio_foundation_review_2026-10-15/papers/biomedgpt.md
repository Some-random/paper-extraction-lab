# BioMedGPT-LM / BioMedGPT (PharMolix)

[Biological pretraining review](../README.md)

Biological multimodal language

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Paper year:** 2023. First public paper/preprint release; not the checkpoint release or latest revision. [Publication date](https://arxiv.org/abs/2308.09442).

**Training approach:** Continued pretraining. **Starting checkpoint:** Llama2-Chat-7B. [Initialization evidence](https://arxiv.org/html/2308.09442v2)

This row covers the literature CPT stage, before molecule/protein alignment.

**Data included in the overview amounts:** Biomedical paper text. The literature CPT amount covers the selected biomedical S2ORC text, not a separately labeled nonclinical biology subset.

## Authors and institutions

**Authors:** Yizhen Luo; Jiahuan Zhang; Siqi Fan; Kai Yang; Yushuai Wu; Mu Qiao; Zaiqing Nie.

**Institutions:** Institute for AI Industry Research, Tsinghua University; PharMolix.

[Paper attribution](https://arxiv.org/html/2308.09442v2). Names and affiliations follow the reviewed paper version.

<a id="evidence-assessment"></a>

## Overall paper assessment

**Overall: Mixed.** An interesting early multimodal biomedical prototype, with a plausible integration of literature and biological encoders. The experimental scope and generalization checks are too narrow to establish a broadly reliable biomedical foundation model. This is our provisional technical judgment of the whole paper in its publication context, not an official review score or an independent replication.

**Contribution and originality:** Connects a literature-adapted language model with molecule/protein inputs in a practically useful architecture.

**Technical soundness:** The alignment design is reasonable, but several training stages make attribution of gains difficult.

**Evaluation:** Alignment comparisons are informative; random protein splits and limited task coverage weaken broad generalization claims.

**Reproducibility:** An author implementation exists, but corpus choices, alignment and task tuning all matter for reproducing the end result.

**Clarity and limitations:** The model stages are understandable; the similarly named vision-language model must not be conflated with this work.

Sources: [Reviewed paper: methods/results/limitations](https://arxiv.org/html/2308.09442v2)

## Paper-text origins

**Direct paper sources:** No direct source established for this row.

**Paper text via reused datasets:** S2ORC.

Biomedical paper text is imported through S2ORC; the >26B tokens are allocated to existing datasets, not direct online-paper acquisition. [Source](https://arxiv.org/html/2308.09442v2)

## Other modalities

The counted >26B literature CPT stage is text-only. Molecule/protein encoders enter in subsequent alignment and multimodal variants; their features are not included as counted text tokens.

| Representation / domain | Reported tokens | Count definition |
|---|---:|---|
| Later molecule/protein encoder features | NR | Later-stage features, not token counts in the literature CPT row. |

Sources: [Reviewed paper: data and representations](https://arxiv.org/html/2308.09442v2)

## Existing-dataset sources

S2ORC.

Named reused inputs relevant to the reviewed training stages. This is not necessarily exhaustive. A source name establishes provenance, not its token amount; unreported amounts remain NR. Directly collected PubMed/PMC text is described separately as online-paper input. [Source](https://arxiv.org/html/2308.09442v2)

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [BioMedGPT-LM / BioMedGPT (PharMolix)](#token-counts-by-acquisition-route)<br>Literature CPT | Corpus · text | 0 | 0 | >26B | >26B | [§3.1](https://arxiv.org/html/2308.09442v2) |

**Literature CPT — Corpus (text):** This row covers BioMedGPT-LM literature CPT only. Later molecule/protein alignment is not folded into the literature count.

- **Online Papers: 0.** The 4.2M papers are selected from S2ORC, not independently downloaded for this recipe.

- **Web Urls: 0.** The literature-CPT stage describes S2ORC paper text only.

- **Existing Datasets: >26B.** Biomedical S2ORC subset.

- **Total: >26B.** Reported literature corpus lower bound.

**Training stage:** Literature CPT, then molecule/protein-text alignment

**Backbone:** Llama2-Chat-7B

**Source material and units:** 4.2M full-text S2ORC papers after filtering 5.5M biomedical candidates; over 26B text tokens.

**Acquisition and document processing:** S2ORC full text selected using PMC/PubMed IDs; no fresh PDF OCR implementation is specified.

**Cleaning and filtering:** Remove missing full texts, duplicate IDs, author information, reference citations, and chart data.

**Training unit and mixture:** Sentence-based chunks, 2,048-token context and autoregressive literature training; later align molecule graphs and protein sequences to the LLM.

**Generated or augmented material:** PubChemQA and UniProtQA turn database descriptions and annotations into templated questions. Invalid molecular graphs and very short descriptions are removed.

**Author-reported evidence:** Includes aligned versus unaligned biological-input baselines; not an experiment comparing OCR methods.

**Disclosure gaps:** Distinct from the similarly named vision-language BiomedGPT model. Random protein splits are weaker evidence of cross-family generalization.

**Source sections:** 3.1 Biomedical generative language model; 3.2 Multimodal fine-tuning

## Source material

[BioMedGPT-LM, PharMolix](https://arxiv.org/html/2308.09442v2)

| Reported field | Retained source statement |
|---|---|
| Stage | Decoder CPT |
| Actual biological source material | 4.2M biomedical full texts selected from S2ORC, over 26B tokens |
| How the source becomes training data / relevant limitation | ID deduplication, removes reference citations/author information/chart data, then sentence-based text chunks. Molecule/protein alignment happens separately. |

## Datasets and amounts

[BioMedGPT-LM, PharMolix](https://arxiv.org/html/2308.09442v2), Llama-2-Chat CPT, §3.1

| Reported field | Retained source statement |
|---|---|
| Paper or abstract text | **>26B tokens**, 4.2M full-text papers, selected from S2ORC |
| Web-origin text | No separately added web corpus described |
| Other data in this stage | Molecule/protein alignment is a later stage |
| Reported total and disclosure limit | >26B literature-corpus tokens; a source-specific consumed-token breakdown is NR |

## Figure handling

[BioMedGPT-LM, PharMolix](https://arxiv.org/html/2308.09442v2)

| Reported field | Retained source statement |
|---|---|
| Pixels used in training? | No paper-image branch in the described CPT |
| Source captions / generated material | Removes chart data from its S2ORC literature input. Subsequent molecule/protein encoders are not figure-image encoders |

## Citation handling

PharMolix BioMedGPT-LM, decoder CPT

| Reported field | Retained source statement |
|---|---|
| Reported treatment | Removes reference citations, author information and chart data before sentence-based chunking. [§3.1](https://arxiv.org/html/2308.09442v2) |

## Primary sources

- [BioMedGPT report](https://arxiv.org/html/2308.09442v2)
- [OpenBioMed author repository](https://github.com/PharMolix/OpenBioMed)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
