# Biological continued pretraining: data sources and token budgets

How biological foundation models turn research papers, web content and existing datasets into training data. The main comparison focuses on **continued pretraining (CPT)**: starting with a pretrained model and training it further on domain data. Data-curation studies and released models appear together because both inform this choice.

**These are reported source budgets, not uniformly biology-only token counts.** Some include clinical literature, general text, other sciences or non-text modalities. The “Data included” column identifies that scope. A paper’s full training total cannot be treated as a biology-only amount when that subset is not separately reported.

## Continued pretraining

Each row names the starting checkpoint and reports one clearly identified token budget. Unmarked rows show **dataset tokens before training repeats**. **† Training tokens** include repeated passes; **‡ token positions** can include padding or a planned schedule. The linked study pages retain the full counts and source qualifications.

| Model / starting checkpoint | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total reported tokens | Data included | Source |
|---|---:|---:|---:|---:|---|---|
| [Biomed-Enriched](papers/biomed_enriched.md)<br>OLMo2-7B-stage1<br>**Training tokens†** | 33.6B | 0 | 0 | 33.6B | Biomedical paper text | [§3–4 / Table 2](https://arxiv.org/html/2506.20331v1) |
| [BioMedGPT-LM](papers/biomedgpt.md)<br>Llama2-Chat-7B | 0 | 0 | >26B | >26B | Biomedical paper text | [§3.1](https://arxiv.org/html/2308.09442v2) |
| [BioMatrix](papers/biomatrix.md)<br>Qwen3-1.7B / 4B | NR | NR | ≥25.6B | 304.4B | Biological modalities + general text | [§3 / Fig. 3](https://arxiv.org/html/2606.22138v1) |
| [BioMamba](papers/biomamba.md)<br>Mamba2 checkpoints, 130M–2.7B<br>**Token positions‡** | ≈434.176M | 0 | ≈86.016M | ≈520.192M | Biomedical papers + general replay | [Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/) |
| [BioBERT](papers/biobert.md)<br>BERT | NR | NR | NR | NR | Biomedical paper text | [Paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7703786/) |
| [NatureLM](papers/naturelm.md)<br>Llama 3 8B / Mixtral 8×7B | NR | NR | ≥116.72B | 143.8B | Biology, chemistry, materials + general text | [§2 / Table S1](https://arxiv.org/html/2502.07527v2) |
| [TheBioCollection / Gravity-bio](papers/gravity_bio.md)<br>Gravity-16B-A3B, before annealing | ≥54B | NR | ≥52.6B | NR | Biological records + biomedical papers; replay extra | [Table 4](https://arxiv.org/html/2607.08803v1) · [§2 / Fig. 2](https://arxiv.org/html/2607.08803v1) |
| [SciReasoner](papers/scireasoner.md)<br>Qwen3-1.7B / 8B | NR | NR | ≥166B | 206B | Biology, chemistry, materials + other text | [§2 / Fig. 2](https://arxiv.org/html/2509.21320v1) |
| [LOGOS](papers/logos.md)<br>Qwen3-8B; Llama 3.2-1B / 3B variants | 0 | 0 | 44.87B | 44.87B | Biological, chemical and materials sequences | [§2 / Appendix A](https://arxiv.org/html/2606.16905v1) |
| [PMC-InterCPT / Beyond Captions](papers/pmc_intercpt.md)<br>Qwen3.5-2B / 4B-Base | NR | NR | NR | 9.63B | Biomedical paper text + image tokens | [Tables 1, 8–9](https://arxiv.org/html/2606.01049v2) |
| [How Post-Training Shapes Biological Reasoning](papers/bio_posttraining.md)<br>Qwen3-1.7B / 4B | NR | NR | NR | NR | Biology-labeled web subset | [Paper](https://arxiv.org/html/2606.16517v1) |

### Reading the counts

- **Online papers:** text acquired directly from publishers or publication repositories, including abstracts, XML, PDF and LaTeX.
- **Web URLs:** non-paper webpages acquired directly, including raw web archives.
- **Existing datasets:** reused corpora and biological databases. Paper text imported through S2ORC or The Pile belongs here; it is not counted twice. These columns describe **how the study obtained the data**, not just what the text discusses.
- **0** means the described data has no separate acquisition through that route. **NR** means the token amount is not reported or cannot be established. Neither a known source name nor a paper count supplies a missing token count.
- **Dataset size** counts the prepared corpus before training repeats. **Tokens used in training** counts consumption, including repeated passes: a 10B-token dataset read three times gives 30B training tokens, not 30B of distinct data. The former measures data volume; the latter measures how much training read it. For BioMedLM these figures are 34.6B and 300B.
- **M / B** mean million / billion; **≈** means approximate; **> / ≥** indicate a lower bound. Tokenizers differ. Sequence/image tokens and planned token positions are labeled explicitly. A total may include material without a disclosed category split.

**Scope examples:** BioMatrix’s 304.4B covers biological modalities and general text; the ≥25.6B identified in its existing-dataset column is FineWeb-Edu **general text**. BioMamba’s existing-dataset component is general replay. NatureLM and SciReasoner also cover sciences beyond biology. None of those whole-row totals is a verified biology-only budget.

Gravity-bio reports separate literature and biological-database components but not the full training mixture. LOGOS reports a corpus spanning pretraining and post-training; its CPT-only amount is not disclosed. BioMamba’s figure counts packed positions, including padding. Biomed-Enriched’s 33.6B is the training budget **per experimental variant**. PMC-InterCPT contributes a paper/figure curation method evaluated on medical and scientific tasks; it is not evidence that clinical filtering is appropriate for all biology.

## Pretraining from scratch: comparison

These models begin with randomly initialized weights and biological or scientific data, rather than adapting an existing checkpoint. They provide a comparison with CPT.

| Model / starting checkpoint | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total reported tokens | Data included | Source |
|---|---:|---:|---:|---:|---|---|
| [BioGPT](papers/biogpt.md)<br>Random weights; GPT-2-style architecture<br>**Token positions‡** | 104.8576B | 0 | 0 | 104.8576B | Biomedical abstracts | [Pretraining](https://arxiv.org/pdf/2210.10341) |
| [BioMedLM](papers/biomedlm.md)<br>Random weights; 2.7B GPT-style decoder | 0 | 0 | 34.6B | 34.6B | Biomedical papers | [§3.3](https://arxiv.org/html/2403.18421v1) |
| [PubMedBERT](papers/pubmedbert.md)<br>Random weights; BERT architecture | NR | NR | NR | NR | Biomedical paper text | [Paper](https://doi.org/10.1145/3458754) |
| [BioLinkBERT](papers/biolinkbert.md)<br>Random weights; BERT architecture | NR | NR | NR | NR | Biomedical abstracts | [Paper](https://aclanthology.org/2022.acl-long.551/) |
| [Galactica](papers/galactica.md)<br>Random weights; scientific decoder | ≥64.926B | ≥700M | ≥23.87B | ≈106B | Broad scientific corpus + general material | [Tables 1, 22–25](https://arxiv.org/html/2211.09085v1) |

BioGPT’s 104.8576B is calculated from its scheduled steps and batch size, not a measured unique corpus size. Galactica includes broad scientific material as well as biology. NatureLM’s 8B and 8×7B versions belong in the CPT table; its separate 1B model first undergoes general-text pretraining on SlimPajama before scientific training.

## Data preparation

The [data preparation pipeline](data_pipeline.md) brings paper, web and reused-dataset inputs into the same source-linked records, then applies content selection, deduplication and token counting. It distinguishes existing implementation from proposed web-processing work. See also the guides to [biological sources](source_planning.md), [web and reusable corpora](web_acquisition.md), [original figures and context](figure_handling.md), and [citation handling](citations_and_cpt_sources.md). [Supporting literature](background.md) covers source corpora, extraction pipelines, instruction tuning and representation learning.
