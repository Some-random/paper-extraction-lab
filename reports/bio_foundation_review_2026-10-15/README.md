# Shared biological foundation-model literature catalog

This is the shared literature home for **paper-extraction-lab** and **bio-evaluation**. Each model or study has one page combining its paper links, datasets and amounts, document processing, filtering, augmentation, figure/citation handling and known gaps.

**31 model-family entries, 3 training-data studies, 3 reusable corpora and 4 method references.** These are catalog entries, not a count of distinct publications or an exhaustive census.

The previous source review, dataset breakdown and additional-coverage table are merged here. The entries below include TheBioCollection/Gravity-bio, NatureLM, BioMatrix, BioReason, BioReason-Pro, SciReasoner, LOGOS and the earlier models.

[Download the catalog as CSV](catalog.csv) · [Structured source registry](review.json)

Reported corpus size, training exposure, words, examples and image tokens retain their original units. **NR means not separately reported, not zero.** Source discrepancies and paper versions remain explicit. This consolidation reuses existing evidence; it is not a fresh search or a model benchmark.

## Biological research and science models

| Model / study / corpus | Stage | Data summary |
|---|---|---|
| [BioGPT](papers/biogpt.md) | Pretraining from scratch; task-specific fine-tuning | 15M PubMed records with both title and abstract, updated before 2021. |
| [BioMedLM](papers/biomedlm.md) | Pretraining from scratch; task-specific fine-tuning | The Pile's PubMed abstracts and full-article subsets: 34.6B corpus tokens. Training consumes 300B tokens, or 8.67 passes. |
| [BioMedGPT-LM / BioMedGPT (PharMolix)](papers/biomedgpt.md) | Literature CPT, then molecule/protein-text alignment | 4.2M full-text S2ORC papers after filtering 5.5M biomedical candidates; over 26B text tokens. |
| [BioT5 / BioT5+](papers/biot5plus.md) | Multimodal denoising pretraining and multitask tuning | PMC full text, PubMed/bioRxiv abstracts, C4, PubChem molecules, UniRef50 proteins, and biomolecule-description pairs. |
| [BioMatrix](papers/biomatrix.md) | Multimodal CPT, then multitask SFT | 304.4B mixed tokens: FineWeb-Edu; FineFineWeb biology/chemistry/medicine/health; PubMed text; molecules, proteins, structures, and interactions. |
| [BioMamba](papers/biomamba.md) | CPT, then downstream SFT | PubMed MEDLINE abstracts with C4 and English Wikipedia; approximately 508K packed 1,024-token sequences in the reported final corpus. |
| [TxGemma](papers/txgemma.md) | Task instruction tuning; conversational variants add general instructions | Approximately 7M training examples derived from Therapeutic Data Commons; classification, regression and generation. |
| [BioBERT](papers/biobert.md) | Encoder continued pretraining | PubMed abstracts and PMC full text |
| [PubMedBERT](papers/pubmedbert.md) | Encoder pretraining from scratch | PubMed abstracts; additional PMC experiments |
| [BioLinkBERT](papers/biolinkbert.md) | Encoder pretraining from scratch | PubMed documents and citation links |
| [NatureLM](papers/naturelm.md) | Scientific decoder continued pretraining for larger variants | Literature, database descriptions, small molecules, proteins, DNA/RNA and cross-domain pairs |
| [Galactica](papers/galactica.md) | Decoder pretraining from scratch | Scientific papers plus biological/chemical records such as UniProt and PubChem |
| [TheBioCollection / Gravity-bio](papers/gravity_bio.md) | Annealing / continued training | 54.0B scientific text: PubMed 48.8B, bioRxiv 4.6B, medRxiv 0.58B, with rounding; Biological corpus 52.6B: molecules 28.2B, proteins 14.5B, genomic sequences 7.1B, cells/pathways 2.8B. Also uses olmOCR science PDFs, DCLM-CC and… |
| [SciReasoner](papers/scireasoner.md) | Continued pretraining, then SFT and reasoning/RL | PubMed abstracts/scientific prose; exact literature-token share NR; Headline 206B; prose gives proteins 55B, chemistry 50B, DNA 30B, RNA 26B, materials 5B. Uses C4 general text. Later 40M SFT examples, separate from CPT |
| [LOGOS](papers/logos.md) | Continued pretraining and post-training | No large paper-text acquisition stage described; 44.87B scientific-sequence/interaction tokens reported across protein, antibody, molecule, reaction, material, pocket and complex modalities |
| [Tx-LLM](papers/txllm.md) | Instruction tuning | Manually written 2–3-sentence contexts informed by dataset descriptions and literature; TxT: 709 component datasets / 66 tasks, derived from TDC |
| [BioReason](papers/bioreason.md) | DNA-encoder/LLM supervised adaptation; selected GRPO | Not a paper-corpus CPT experiment; Full task datasets before splitting: 1,449 KEGG reasoning records, 50,083 coding variants, 36,088 non-SNV variants. Claude-generated reasoning; GPT-4o question paraphrases |
| [BiomedCLIP / PMC-15M](papers/biomedclip.md) | Contrastive image-text pretraining | 15,282,336 image–caption pairs, collected from a 4.4M-article PMC snapshot |
| [LLaVA-Med](papers/llava_med.md) | Image-caption alignment, then instruction tuning | 600K source image–caption pairs for alignment; 60K instruction examples in its larger instruction datasets |
| [BioReason-Pro](papers/bioreason_pro.md) | Supervised adaptation on synthetic reasoning, followed by reinforcement learning | UniProt-curated protein records with GO annotations, InterPro domains, STRING interactions and structural context; the author release describes 133,492 curated proteins, not full papers. |
| [ProtST](papers/protst.md) | Protein/text representation learning; published supervised and zero-shot task evaluations | Imported evaluation references identify learned protein/text encoders and task-specific heads. A paper-extraction/CPT budget was not established in those notes. |

## Training-data and curation studies

| Model / study / corpus | Stage | Data summary |
|---|---|---|
| [Biomed-Enriched](papers/biomed_enriched.md) | Controlled OLMo2-7B-stage1 CPT | Approximately 4.5M PMC-OA XML articles; 133M paragraphs after processing, minimum 64 tokens. |
| [PMC-InterCPT / Beyond Captions](papers/pmc_intercpt.md) | CPT with a fixed downstream SFT stage | PMC/BIOMEDICA figures, captions and article-native context; final 9.63B-token corpus. |
| [How Post-Training Shapes Biological Reasoning Models](papers/bio_posttraining.md) | Stage-wise biological adaptation experiments | FineFineWeb biology: first 200K documents train, next 5K evaluation; downstream DNA/RNA/protein reasoning data. |

## Reusable corpora

| Model / study / corpus | Stage | Data summary |
|---|---|---|
| [S2ORC](papers/s2orc.md) | Corpus construction | S2ORC means Semantic Scholar Open Research Corpus. It aggregates research metadata and machine-readable academic text, including citation and figure/table mentions, across publishers and archives. The original 2020 release… |
| [peS2o](papers/pes2o.md) | Corpus curation | peS2o is an already cleaned and packaged language-model corpus derived from S2ORC and Semantic Scholar abstracts. Its v2 training split lists 8,242,162 full-text-derived records and 30,569,017 title/abstract-derived records.… |
| [Dolma](papers/dolma.md) | Corpus construction | The original Dolma corpus reports Common Crawl 2,479B; GitHub 411B; Reddit 89B; Semantic Scholar/peS2o 70B; Gutenberg 6B; Wikipedia/Wikibooks 4.3B, approximately 3,059B total with its stated tokenizer. This is a reusable… |

## Method context

General recipes are identified separately; their whole PDF/token pools are not treated as biological-literature budgets.

| Model / study / corpus | Stage | Data summary |
|---|---|---|
| [OLMo 3](papers/olmo3.md) | Pretraining and midtraining | General model data: 5.93T sampled tokens in the reported stage-1 mix and 99.95B in stage-2 midtraining. Biological-paper allocation is not separately reported. |
| [UniGenX](papers/unigenx.md) | Scientific sequence/coordinate generation | Scientific sequence/coordinate data; inspected v1 covers molecule/material experiments. See version-specific source notes. |
| [Ryze](papers/ryze.md) | Document extraction and training-data preparation reference | User-specified biological method paper. A paper/web/database token budget has not been normalized in this consolidation. |
| [STRIDE](papers/stride.md) | Supervised fine-tuning followed by reinforcement learning | The retained author README describes GFP and SMILES task data with explicit edit trajectories; these are task datasets rather than a full-paper literature corpus. |

## Medical context retained from earlier review

Retained as historical references. Clinical-note acquisition is outside this project’s biological research scope.

| Model / study / corpus | Stage | Data summary |
|---|---|---|
| [PMC-LLaMA](papers/pmc_llama.md) | CPT knowledge injection, then SFT | 4.8M PMC-ID-selected S2ORC papers, over 75B tokens; 30K textbooks yielding approximately 4B tokens. |
| [BioMistral](papers/biomistral.md) | CPT; evaluation with few-shot prompts and SFT | 3B-token sample of the commercial-use PMC-OA subset; approximately 1.47M reported documents, 98.75% English. |
| [MEDITRON](papers/meditron.md) | CPT, then task-specific SFT | GAP-Replay: 48.1B tokens including validation; approximately 5M full texts, 16.1M abstracts, 46K guidelines, and 420M general replay tokens. |
| [Me-LLaMA](papers/me_llama.md) | CPT, general medical SFT, optional task SFT | 129B-token mixture: Pile biomedical articles/abstracts, deidentified MIMIC-III/IV/CXR notes, and RedPajama general text. |
| [MMedLM / MMed-Llama 3](papers/mmedlm.md) | CPT, then QA/rationale tuning | MMedC: 25.5B corpus tokens in six languages from filtered general corpora, over 20K medical textbooks, medical websites, and existing medical text datasets. |
| [MedFound](papers/medfound.md) | Medical pretraining, diagnostic SFT, preference alignment | Medical text and real-world clinical records. |
| [MedGemma](papers/medgemma.md) | Vision enhancement, pretraining, teacher distillation, RL | Medical imaging/report pairs and medical QA, with original SigLIP/Gemma general mixtures for replay. Table 1 lists 41,853 PMC single-panel image-caption examples. |
| [Lingshu](papers/lingshu.md) | Shallow/deep alignment, SFT, RL | Collected medical image/text datasets plus synthetic caption, OCR-question, QA and reasoning data; general-domain caption/instruction data are mixed in. |
| [Hulu-Med](papers/hulu_med.md) | Alignment, medical CPT, mixed-modality SFT | 16.7M samples: 9M medical multimodal, 4.9M medical text, 1.3M general multimodal and 1.5M general text. |
| [InfiMed-Foundation](papers/infimed.md) | Multimodal CPT and three-stage SFT | Approximately 25B general multimodal plus 5B medical pretraining tokens. |

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
