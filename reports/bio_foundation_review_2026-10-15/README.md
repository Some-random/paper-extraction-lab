# Shared biological foundation-model literature catalog

This is the shared literature home for **paper-extraction-lab** and **bio-evaluation**. Each model or study has one page combining its paper links, datasets and amounts, document processing, filtering, augmentation, figure/citation handling and known gaps.

**31 model-family entries, 3 training-data studies, 3 reusable corpora and 4 method references.** These are catalog entries, not a count of distinct publications or an exhaustive census.

The previous source review, dataset breakdown and additional-coverage table are merged here. The entries below include TheBioCollection/Gravity-bio, NatureLM, BioMatrix, BioReason, BioReason-Pro, SciReasoner, LOGOS and the earlier models.

[Download the catalog as CSV](catalog.csv) · [Structured source registry](review.json)

[Token-count verification](token_budget_verification.json)

The tables report **token amounts for each acquisition category**, with separate rows for corpus size and training exposure where those are available. Extraction, filtering, original paper/example counts and further qualifications are in each linked model page.

## Token-count legend

- **Online-paper tokens:** paper/abstract text acquired directly from publication repositories or publishers, including their PDF, XML, LaTeX or bibliographic-text exports.
- **Web-URL tokens:** non-paper website content collected directly from live pages or raw web archives.
- **Existing-dataset tokens:** imported, already assembled corpora or datasets, including literature/web corpora and biological databases. For example, paper text imported through S2ORC or The Pile is counted here, not again under online papers. The route is assessed at the reviewed study's acquisition/curation stage; releasing a new corpus does not itself make all of its inputs existing-dataset tokens.
- **NR:** the category-specific token count is not disclosed or cannot be established from the inspected evidence; it is **not zero**. A known source without a separable token budget still receives NR.
- **0:** the described stage has no separate acquisition through that route. For example, an exclusively reused paper dataset has zero direct-paper tokens, even though its content is literature.
- **K / M / B / T:** thousand / million / billion / trillion tokens. **≈** denotes an approximate reported amount; **> / ≥** denotes a lower bound, not a complete category total.
- **Corpus** counts retained data; **training exposure** counts sampled tokens and may include repeated passes. Planned schedules are labeled **scheduled token positions**, not measured training exposure. **Text + image** totals remain labeled; image pairs, words, bytes and documents are never converted into token counts.
- A total can include unallocated, generated, code, book or private-source tokens. Missing category counts are not filled by subtracting known columns from the total. Counts from different rows/stages/models must not be added. Source-specific tokenizers and rounding remain unchanged.

## Biological research and science models

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [BioGPT](papers/biogpt.md#token-counts-by-acquisition-route)<br>Pretraining | Corpus · text | NR | 0 | 0 | NR | [Pretraining](https://arxiv.org/pdf/2210.10341) |
| [BioGPT](papers/biogpt.md#token-counts-by-acquisition-route)<br>Pretraining | Scheduled token positions · token positions | 104.8576B | 0 | 0 | 104.8576B | [Pretraining](https://arxiv.org/pdf/2210.10341) |
| [BioMedLM](papers/biomedlm.md#token-counts-by-acquisition-route)<br>Pretraining | Corpus · text | 0 | 0 | 34.6B | 34.6B | [§3.3](https://arxiv.org/html/2403.18421v1) |
| [BioMedLM](papers/biomedlm.md#token-counts-by-acquisition-route)<br>Pretraining | Training exposure · text | 0 | 0 | 300B | 300B | [§3.3](https://arxiv.org/html/2403.18421v1) |
| [BioMedGPT-LM / BioMedGPT (PharMolix)](papers/biomedgpt.md#token-counts-by-acquisition-route)<br>Literature CPT | Corpus · text | 0 | 0 | >26B | >26B | [§3.1](https://arxiv.org/html/2308.09442v2) |
| [BioT5 / BioT5+](papers/biot5plus.md#token-counts-by-acquisition-route)<br>Multimodal denoising pretraining and multitask tuning | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2402.17810v2) |
| [BioMatrix](papers/biomatrix.md#token-counts-by-acquisition-route)<br>Multimodal CPT | Corpus · text + scientific sequences | NR | NR | ≥25.6B | 304.4B | [§3 / Fig. 3](https://arxiv.org/html/2606.22138v1) |
| [BioMamba](papers/biomamba.md#token-counts-by-acquisition-route)<br>CPT | Packed token positions · token positions | ≈434.176M | 0 | ≈86.016M | ≈520.192M | [Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/) |
| [TxGemma](papers/txgemma.md#token-counts-by-acquisition-route)<br>27B-Predict SFT | Training exposure · text | 0 | 0 | 67B | 67B | [Model fine-tuning](https://arxiv.org/html/2504.06196v1) |
| [BioBERT](papers/biobert.md#token-counts-by-acquisition-route)<br>Encoder continued pretraining | Not reported · text | NR | NR | NR | NR | [Paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7703786/) |
| [PubMedBERT](papers/pubmedbert.md#token-counts-by-acquisition-route)<br>Encoder pretraining from scratch | Not reported · text | NR | NR | NR | NR | [Paper](https://doi.org/10.1145/3458754) |
| [BioLinkBERT](papers/biolinkbert.md#token-counts-by-acquisition-route)<br>Encoder pretraining from scratch | Not reported · text | NR | NR | NR | NR | [Paper](https://aclanthology.org/2022.acl-long.551/) |
| [NatureLM](papers/naturelm.md#token-counts-by-acquisition-route)<br>8B / 8×7B scientific CPT | Corpus · text + scientific sequences | NR | NR | ≥116.72B | 143.8B | [§2 / Table S1](https://arxiv.org/html/2502.07527v2) |
| [Galactica](papers/galactica.md#token-counts-by-acquisition-route)<br>Scientific pretraining | Corpus · text + scientific sequences | ≥64.926B | ≥700M | ≥23.87B | ≈106B | [Tables 1, 22–25](https://arxiv.org/html/2211.09085v1) |
| [Galactica](papers/galactica.md#token-counts-by-acquisition-route)<br>Scientific pretraining | Training exposure · text + scientific sequences | NR | NR | NR | 450B | [§5.1](https://arxiv.org/html/2211.09085v1) |
| [TheBioCollection / Gravity-bio](papers/gravity_bio.md#token-counts-by-acquisition-route)<br>Biological corpus component | Corpus · text + scientific sequences | 0 | 0 | 52.6B | 52.6B | [§2 / Fig. 2](https://arxiv.org/html/2607.08803v1) |
| [TheBioCollection / Gravity-bio](papers/gravity_bio.md#token-counts-by-acquisition-route)<br>Scientific-literature component | Corpus · text | ≈54B | 0 | 0 | ≈54B | [Table 4](https://arxiv.org/html/2607.08803v1) |
| [TheBioCollection / Gravity-bio](papers/gravity_bio.md#token-counts-by-acquisition-route)<br>Full annealing mixture | Training exposure · text | NR | NR | NR | NR | [§3.1](https://arxiv.org/html/2607.08803v1) |
| [SciReasoner](papers/scireasoner.md#token-counts-by-acquisition-route)<br>Scientific CPT | Corpus · text + scientific sequences | NR | NR | ≥166B | 206B | [§2 / Fig. 2](https://arxiv.org/html/2509.21320v1) |
| [LOGOS](papers/logos.md#token-counts-by-acquisition-route)<br>Scientific pre-/post-training corpus | Corpus · scientific sequences | 0 | 0 | 44.87B | 44.87B | [§2 / Appendix A](https://arxiv.org/html/2606.16905v1) |
| [Tx-LLM](papers/txllm.md#token-counts-by-acquisition-route)<br>Instruction tuning | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2406.06316v1) |
| [BioReason](papers/bioreason.md#token-counts-by-acquisition-route)<br>DNA-encoder/LLM supervised adaptation; selected GRPO | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2505.23579v2) |
| [BiomedCLIP / PMC-15M](papers/biomedclip.md#token-counts-by-acquisition-route)<br>Contrastive image-text pretraining | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2303.00915) |
| [LLaVA-Med](papers/llava_med.md#token-counts-by-acquisition-route)<br>Figure-caption alignment | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2306.00890) |
| [LLaVA-Med](papers/llava_med.md#token-counts-by-acquisition-route)<br>Instruction tuning | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2306.00890) |
| [BioReason-Pro](papers/bioreason_pro.md#token-counts-by-acquisition-route)<br>Supervised adaptation on synthetic reasoning, followed by reinforcement learning | Not reported · text | NR | NR | NR | NR | [Paper](https://www.biorxiv.org/content/10.64898/2026.03.19.712954v1) |
| [ProtST](papers/protst.md#token-counts-by-acquisition-route)<br>Protein/text representation learning; published supervised and zero-shot task evaluations | Not reported · text | NR | NR | NR | NR | [Paper](https://proceedings.mlr.press/v202/xu23t/xu23t.pdf) |

## Training-data and curation studies

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [Biomed-Enriched](papers/biomed_enriched.md#token-counts-by-acquisition-route)<br>Controlled CPT: each variant | Training exposure · text | 33.6B | 0 | 0 | 33.6B | [§3–4 / Table 2](https://arxiv.org/html/2506.20331v1) |
| [PMC-InterCPT / Beyond Captions](papers/pmc_intercpt.md#token-counts-by-acquisition-route)<br>Context-grounded CPT | Resampled corpus · text + image | NR | NR | NR | 9.63B | [Tables 1, 8–9](https://arxiv.org/html/2606.01049v2) |
| [How Post-Training Shapes Biological Reasoning Models](papers/bio_posttraining.md#token-counts-by-acquisition-route)<br>Stage-wise biological adaptation experiments | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2606.16517v1) |

## Reusable corpora

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [S2ORC](papers/s2orc.md#token-counts-by-acquisition-route)<br>S2ORC-SciBERT filtered subset | Corpus · source-reported tokens | 16.4B | 0 | 0 | 16.4B | [§5](https://aclanthology.org/2020.acl-main.447.pdf) |
| [S2ORC](papers/s2orc.md#token-counts-by-acquisition-route)<br>Full archive | Author-estimated corpus · source-reported tokens | NR | NR | NR | ≈40B | [Appendix E](https://aclanthology.org/2020.acl-main.447.pdf) |
| [peS2o](papers/pes2o.md#token-counts-by-acquisition-route)<br>v2 corpus curation | Corpus · whitespace tokens | 0 | 0 | ≈42.01B | ≈42.01B | [v2 key facts](https://github.com/allenai/pes2o) |
| [Dolma](papers/dolma.md#token-counts-by-acquisition-route)<br>Original corpus construction | Corpus · text | 0 | 2.281T | 778.3B | ≈3.059T | [Table 1 / §3](https://arxiv.org/html/2402.00159v1) |

## Method context

General recipes are identified separately; their whole PDF/token pools are not treated as biological-literature budgets.

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [OLMo 3](papers/olmo3.md#token-counts-by-acquisition-route)<br>Pretraining: available 9T pool | Corpus pool · text | 993.4B | 8.14T | 174.79B | ≈9.31T | [Table 4](https://arxiv.org/html/2512.13961v2) |
| [OLMo 3](papers/olmo3.md#token-counts-by-acquisition-route)<br>Pretraining: final 6T mix | Sampled training mix · text | 855.8B | 4.51T | 563.51B | ≈5.93T | [Table 4](https://arxiv.org/html/2512.13961v2) |
| [OLMo 3](papers/olmo3.md#token-counts-by-acquisition-route)<br>Midtraining | Sampled training mix · text | 4.99B | 27.39B | ≥10B | 99.95B | [Table 5](https://arxiv.org/html/2512.13961v2) |
| [UniGenX](papers/unigenx.md#token-counts-by-acquisition-route)<br>Scientific sequence/coordinate generation | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2503.06687v1) |
| [Ryze](papers/ryze.md#token-counts-by-acquisition-route)<br>SFT | Reported training-data budget · text | NR | NR | NR | 8.051591M | [§3.1](https://arxiv.org/html/2606.00902v1) |
| [Ryze](papers/ryze.md#token-counts-by-acquisition-route)<br>GRPO | Reported training-data budget · text | NR | NR | NR | 1.584412M | [§3.1](https://arxiv.org/html/2606.00902v1) |
| [STRIDE](papers/stride.md#token-counts-by-acquisition-route)<br>Supervised fine-tuning followed by reinforcement learning | Not reported · text | NR | NR | NR | NR | [Paper](https://github.com/daiheng-zhang/STRIDE) |

## Medical context retained from earlier review

Retained as historical references. Clinical-note acquisition is outside this project’s biological research scope.

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [PMC-LLaMA](papers/pmc_llama.md#token-counts-by-acquisition-route)<br>Knowledge-injection CPT | Corpus · text | 0 | 0 | >75B | NR | [Dataset-I](https://arxiv.org/html/2304.14454v3) |
| [BioMistral](papers/biomistral.md#token-counts-by-acquisition-route)<br>CPT | Corpus · text | 3B | 0 | 0 | 3B | [§3.1](https://arxiv.org/html/2402.10373v3) |
| [MEDITRON](papers/meditron.md#token-counts-by-acquisition-route)<br>CPT | Corpus: train split · text | 0 | 107M | 46.6B | ≈46.7B | [§2 / Table 1](https://arxiv.org/html/2311.16079v1) |
| [Me-LLaMA](papers/me_llama.md#token-counts-by-acquisition-route)<br>CPT | Corpus · text | 0 | 0 | 129B | 129B | [Methods](https://www.nature.com/articles/s41746-025-01533-1) |
| [MMedLM / MMed-Llama 3](papers/mmedlm.md#token-counts-by-acquisition-route)<br>CPT | Corpus · text | NR | NR | NR | ≈25.5B | [Data construction](https://www.nature.com/articles/s41467-024-52417-z) |
| [MedFound](papers/medfound.md#token-counts-by-acquisition-route)<br>Medical pretraining, diagnostic SFT, preference alignment | Not reported · text | NR | NR | NR | NR | [Paper](https://www.nature.com/articles/s41591-024-03416-6) |
| [MedGemma](papers/medgemma.md#token-counts-by-acquisition-route)<br>Vision enhancement, pretraining, teacher distillation, RL | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2507.05201v3) |
| [Lingshu](papers/lingshu.md#token-counts-by-acquisition-route)<br>Shallow/deep alignment, SFT, RL | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2506.07044v1) |
| [Hulu-Med](papers/hulu_med.md#token-counts-by-acquisition-route)<br>Alignment, medical CPT, mixed-modality SFT | Not reported · text | NR | NR | NR | NR | [Paper](https://arxiv.org/html/2510.08668v1) |
| [InfiMed-Foundation](papers/infimed.md#token-counts-by-acquisition-route)<br>Multimodal pretraining | Corpus · text + image | 0 | 0 | ≈30B | ≈30B | [§3.1 / Pretraining](https://arxiv.org/html/2509.22261v1) |

## Acquisition and representation guides

- [Biological source planning and provenance](source_planning.md)
- [Web acquisition and reusable web corpora](web_acquisition.md)
- [Executed eight-record web-corpus probe](web_sample.md)
- [Original figures, captions and context](figure_handling.md)
- [Citation provenance and the historical three-paper audit](citations_and_cpt_sources.md)
- [Current three-paper extraction outputs](../pmc_native_v4_citations_2026-10-15/README.md)
- [Paused 500-paper acquisition batch](../pmc_native_500_2026-10-15/README.md)

## Maintenance

Update the existing entry in [review.json](review.json), then run ` .venv/bin/python scripts/render_foundation_catalog.py ` from the project root. The Markdown pages and CSV are generated views of that one registry. Add source versions and disclosure gaps to the same entry instead of creating another “coverage update” table. Evaluation protocols and raw runs retain their original project provenance and link here for literature notes.
