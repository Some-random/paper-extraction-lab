# How biomedical foundation models turn literature and other biological data into training corpora

17 model families and three training-data studies, emphasizing scientific literature acquisition, post-extraction curation, continued pretraining, mixtures, structured biology, synthetic data, and training-value evidence. Medical generalists are identified separately from biological research models.

Targeted web searches, citation following, and reading primary papers, official technical reports, and author repositories. This is a broad targeted review, not an exhaustive systematic census or a common-protocol model leaderboard. Unknown details remain unknown.

This is a source review. Published model results below were not reproduced by our extraction experiment.

[Biology-focused models and real-data sources](biology_sources.md) is the current research scope: literature, figures, full tables, reusable corpora including Dolma/peS2o, and biological databases. Clinical-note recipes below remain historical review entries, not project data recommendations.

The newer [quantitative dataset breakdown](dataset_breakdown.md) gives per-source budgets, units, training-stage distinctions and disclosure gaps for that biological scope. See also [web acquisition](web_acquisition.md), the [executed eight-record web probe](web_sample.md), and [published figure-training recipes](figure_handling.md).

[Citation handling and CPT data sources](citations_and_cpt_sources.md) adds an audit of the three extracted biology samples, published citation-processing choices, and examples of native, structured, clinical and synthetic CPT data. [Audit counts and source hashes](citation_audit.json) are available separately.

## How to interpret the numbers

- Corpus tokens, training tokens consumed, distinct papers, abstracts, packed sequences, and image-caption pairs are different units. Counts across models overlap and must not be added.

- PMC-derived does not establish whether a model used XML, PDFs, or an upstream extraction. A missing OCR description is not evidence that OCR was never used upstream.

- Continued pretraining (CPT) means additional language-model training on a domain corpus. Instruction tuning (SFT) means training on task prompts and target responses. Older papers sometimes call both fine-tuning.

- A teacher's educational-quality score is a curation signal, not scientific truth or independently adjudicated extraction ground truth.

- Published benchmark numbers below are author-reported and protocol-specific. They are not measurements from our 50-paper extraction experiment.

- Clinical evidence ranking and exclusion of animal studies should not be copied into a corpus intended for biological research.

## Model families

### BioGPT

2022 · Biomedical text

**Training stage:** Pretraining from scratch; task-specific fine-tuning

**Backbone:** GPT-2-style decoder; original 347M model

**Corpus:** 15M PubMed records with both title and abstract, updated before 2021.

**PDF/XML/text route:** Download PubMed records from the official FTP distribution; title-plus-abstract text, rather than full paper PDFs.

**Cleaning/filtering:** Discard entries without an abstract. Learn an in-domain BPE vocabulary.

**Training unit and mixture:** Biomedical autoregressive pretraining; downstream tasks use task-specific prompts and target formats.

**Augmentation:** Full-paper OCR and a general replay mixture are not the reported core recipe.

**Reported evidence:** Evaluates relation extraction, QA, document classification, and generation; these evaluate the trained model, not PDF extraction accuracy.

**Limits or missing details:** Fifteen million records must not be described as fifteen million full-text papers.

**Where to check:** Pre-training method: Dataset and Vocabulary

[BioGPT paper](https://academic.oup.com/bib/article/23/6/bbac409/6713511) · [Microsoft implementation](https://github.com/microsoft/BioGPT)

### BioMedLM

2024 report; 2022 model release · Biomedical text

**Training stage:** Pretraining from scratch; task-specific fine-tuning

**Backbone:** 2.7B GPT-style decoder

**Corpus:** The Pile's PubMed abstracts and full-article subsets: 34.6B corpus tokens. Training consumes 300B tokens, or 8.67 passes.

**PDF/XML/text route:** Uses an already assembled text corpus; no newly specified PDF/OCR workflow in the model report.

**Cleaning/filtering:** Selection of biomedical Pile components and a biomedical BPE tokenizer.

**Training unit and mixture:** 1,024-token sequences; entirely biomedical pretraining rather than a general replay mix.

**Augmentation:** The core pretraining dataset is source text, not teacher-written summaries of every paper.

**Reported evidence:** A controlled 125M tokenizer experiment reports MedQA 33.05 to 34.98 over five seeds; the full model is evaluated after task tuning.

**Limits or missing details:** 300B is tokens consumed, not the size of a unique-paper corpus. Upstream extraction quality is not measured by the reported QA scores.

**Where to check:** 3.2 Tokenizer; 3.3 Pre-training

[BioMedLM report](https://arxiv.org/html/2403.18421v1) · [Official checkpoint](https://huggingface.co/stanford-crfm/BioMedLM)

### PMC-LLaMA

2023/2024 · Biomedical/medical text

**Training stage:** CPT knowledge injection, then SFT

**Backbone:** LLaMA; final report includes 13B model

**Corpus:** 4.8M PMC-ID-selected S2ORC papers, over 75B tokens; 30K textbooks yielding approximately 4B tokens.

**PDF/XML/text route:** Papers arrive through S2ORC. Textbook text is extracted from PDFs; a specific OCR engine is not identified in the reviewed method.

**Cleaning/filtering:** Textbook deduplication and removal of URLs, author lists, contents, references, citations, and figure/table mentions.

**Training unit and mixture:** Batch token ratio is BOOKS:PAPERS:GENERAL = 15:4:1; RedPajama supplies general replay.

**Augmentation:** SFT adds GPT-4 instruction paraphrases, ChatGPT-generated QA explanations, and UMLS entity/relationship prompts; 202M instruction tokens.

**Reported evidence:** Includes component ablations and medical QA evaluation.

**Limits or missing details:** The large paper corpus does not mean papers dominate the sampled training mixture. Early paper-only 7B versions differ from the later recipe.

**Where to check:** Dataset-I and Dataset-II

[PMC-LLaMA paper](https://arxiv.org/html/2304.14454v3) · [Author repository](https://github.com/chaoyi-wu/PMC-LLaMA)

### BioMistral

2024 · Biomedical/medical text

**Training stage:** CPT; evaluation with few-shot prompts and SFT

**Backbone:** Mistral-7B-Instruct-v0.1

**Corpus:** 3B-token sample of the commercial-use PMC-OA subset; approximately 1.47M reported documents, 98.75% English.

**PDF/XML/text route:** Raw article text from PMC-OA; the paper does not specify a reproducible PDF-versus-XML conversion engine.

**Cleaning/filtering:** License-based selection, prioritizing non-English documents, then filling the token budget with English documents.

**Training unit and mixture:** 1.5 epochs; EOS-delimited packing into 2,048-token sequences without padding. General capability retention is also explored through weight merging with the original model.

**Augmentation:** No teacher-written expansion is required for its core PMC CPT stage.

**Reported evidence:** Few-shot Table 2 averages: plain BioMistral 50.3 versus parent 51.2; SLERP-merged variant 55.4. Adaptation is not uniformly beneficial.

**Limits or missing details:** The reported document count is not independently verified as distinct complete papers.

**Where to check:** 3.1-3.3; Table 2; Appendix C

[BioMistral paper](https://arxiv.org/html/2402.10373v3) · [Author repository](https://github.com/BioMistral/BioMistral)

### MEDITRON

2023 · Medical text

**Training stage:** CPT, then task-specific SFT

**Backbone:** Llama-2 7B/70B

**Corpus:** GAP-Replay: 48.1B tokens including validation; approximately 5M full texts, 16.1M abstracts, 46K guidelines, and 420M general replay tokens.

**PDF/XML/text route:** S2ORC text and annotations; upstream GROBID table extraction is explicitly discussed. Guidelines have a separate scraping/cleaning path.

**Cleaning/filtering:** English/ID deduplication; remove author/bibliography sections. Keep figure/table captions, discard unreliable table bodies, expand citation and figure references with tagged short descriptions.

**Training unit and mixture:** Approximately 1% general replay; 2,048-token 7B and 4,096-token 70B contexts.

**Augmentation:** Structured reference rewriting is not teacher-generated scientific reasoning.

**Reported evidence:** 7B trial Table 8: PMC 54.6; PMC+Replay 56.2; clinically upsampled PMC 54.7; GAP+Replay 58.9 average accuracy.

**Limits or missing details:** Clinical upsampling is an ablation, not the final best recipe; filtering animal studies is inappropriate for a general biology corpus.

**Where to check:** 2; 7.2 Table 8; Appendix B.2-B.4

[MEDITRON report](https://arxiv.org/html/2311.16079v1) · [Official GAP-Replay and training repository](https://github.com/epfLLM/meditron)

### Me-LLaMA

2024 preprint; 2025 published report · Biomedical and clinical text

**Training stage:** CPT, general medical SFT, optional task SFT

**Backbone:** Llama-2 13B/70B

**Corpus:** 129B-token mixture: Pile biomedical articles/abstracts, deidentified MIMIC-III/IV/CXR notes, and RedPajama general text.

**PDF/XML/text route:** Inherits Pile text; no new paper OCR engine is established by the model methods.

**Cleaning/filtering:** Domain selection and use of deidentified clinical sources; article extraction details largely inherited from upstream datasets.

**Training unit and mixture:** BIOMEDICAL:CLINICAL:GENERAL = 15:1:4; one CPT epoch.

**Augmentation:** 214,595 SFT samples combine literature, notes, guidelines, knowledge graphs and general instructions; distinct from the raw CPT mixture.

**Reported evidence:** Tests six task types over 12 datasets and ablates CPT versus instruction tuning; instruction tuning is often the stronger immediate zero-shot intervention.

**Limits or missing details:** Clinical data and checkpoints have access agreements. This is not an unrestricted public biology-only corpus.

**Where to check:** Methods: Mixed continual pre-training dataset; model development; Data availability

[Published Me-LLaMA report](https://www.nature.com/articles/s41746-025-01533-1) · [Earlier primary preprint](https://arxiv.org/abs/2402.12749)

### MMedLM / MMed-Llama 3

2024 · Multilingual medical text

**Training stage:** CPT, then QA/rationale tuning

**Backbone:** InternLM, InternLM2, Llama 3 variants

**Corpus:** MMedC: 25.5B corpus tokens in six languages from filtered general corpora, over 20K medical textbooks, medical websites, and existing medical text datasets.

**PDF/XML/text route:** Explicit PaddleOCR for textbook pages, retaining coordinates and ordering boxes left-to-right/top-to-bottom.

**Cleaning/filtering:** Remove cover, contents, and epilogue pages; select medical web/corpus sentences using medical keyword count and keyword-density thresholds.

**Training unit and mixture:** 2,048-token text chunks with 512-token overlap; next-token prediction. Corpus size and actual training budget must be distinguished.

**Augmentation:** GPT-4 supplies QA rationales for MMedBench, followed by human verification; this is separate from textbook OCR.

**Reported evidence:** Multilingual QA, rationale, and corpus-component ablations; a small manual relevance check is not a broad OCR accuracy benchmark.

**Limits or missing details:** Not all books and website content are redistributed; a book list is provided.

**Where to check:** Methods: corpus construction; Training details

[Published MMedLM paper](https://www.nature.com/articles/s41467-024-52417-z) · [Author corpus card](https://huggingface.co/datasets/Henrychur/MMedC/blob/main/README.md)

### BioMedGPT-LM / BioMedGPT (PharMolix)

2023/2024 · Biological multimodal language

**Training stage:** Literature CPT, then molecule/protein-text alignment

**Backbone:** Llama2-Chat-7B; BioMedGPT-10B adds biological encoders

**Corpus:** 4.2M full-text S2ORC papers after filtering 5.5M biomedical candidates; over 26B text tokens.

**PDF/XML/text route:** S2ORC full text selected using PMC/PubMed IDs; no fresh PDF OCR implementation is specified.

**Cleaning/filtering:** Remove missing full texts, duplicate IDs, author information, reference citations, and chart data.

**Training unit and mixture:** Sentence-based chunks, 2,048-token context and autoregressive literature training; later align molecule graphs and protein sequences to the LLM.

**Augmentation:** PubChemQA and UniProtQA turn database descriptions and annotations into templated questions. Invalid molecular graphs and very short descriptions are removed.

**Reported evidence:** Includes aligned versus unaligned biological-input baselines; not an experiment comparing OCR methods.

**Limits or missing details:** Distinct from the similarly named vision-language BiomedGPT model. Random protein splits are weaker evidence of cross-family generalization.

**Where to check:** 3.1 Biomedical generative language model; 3.2 Multimodal fine-tuning

[BioMedGPT report](https://arxiv.org/html/2308.09442v2) · [OpenBioMed author repository](https://github.com/PharMolix/OpenBioMed)

### BioT5 / BioT5+

2023/2024 · Biological multimodal language

**Training stage:** Multimodal denoising pretraining and multitask tuning

**Backbone:** T5-family encoder-decoder; smaller than 7B-scale LLMs

**Corpus:** PMC full text, PubMed/bioRxiv abstracts, C4, PubChem molecules, UniRef50 proteins, and biomolecule-description pairs.

**PDF/XML/text route:** Uses literature text and biomolecular databases; no identified new PDF-OCR engine.

**Cleaning/filtering:** BERN2 entity recognition/linking; BioT5+ retains linked entities with confidence above 0.9 and excludes downstream molecules/proteins from specified pretraining pairs.

**Training unit and mixture:** Nine pretraining tasks include masked-span denoising and bidirectional biomolecule-text translation, rather than only causal next-token prediction.

**Augmentation:** Append canonical SELFIES/IUPAC or FASTA representations to mentions in scientific prose; deterministic database enrichment rather than invented experimental claims.

**Reported evidence:** Ablates additional literature, IUPAC information, and numeric tokenization on biomolecular tasks.

**Limits or missing details:** Appendix E's 28.8M PubMed full-article claim is unresolved against source/abstract descriptions; do not use it as a verified downloadable PDF count.

**Where to check:** 3.2-3.4; Appendices C and E

[BioT5+ paper](https://arxiv.org/html/2402.17810v2) · [Author repository](https://github.com/QizhiPei/BioT5)

### BioMatrix

2026 preprint · Biological multimodal foundation

**Training stage:** Multimodal CPT, then multitask SFT

**Backbone:** Qwen3 1.7B/4B

**Corpus:** 304.4B mixed tokens: FineWeb-Edu; FineFineWeb biology/chemistry/medicine/health; PubMed text; molecules, proteins, structures, and interactions.

**PDF/XML/text route:** Article text and S2ORC/abstract/patent sources; the reviewed paper does not provide a reproducible PDF conversion recipe.

**Cleaning/filtering:** BERN2 links literature entity mentions to molecule/protein representations. Database annotations and available sequence/structure views are serialized together.

**Training unit and mixture:** Shared discrete vocabulary and next-token prediction; 8,192-token context, one epoch. General text provides replay.

**Augmentation:** Randomize optional database fields and their order; create sequence-only, structure-only and joint protein views; interleave text with SMILES/SELFIES/amino-acid sequences.

**Reported evidence:** Broad 80-task evaluation after task tuning.

**Limits or missing details:** No dedicated entity-level CPT/evaluation decontamination; authors acknowledge overlap. 304.4B is not all paper text or unique papers.

**Where to check:** 3.1-3.2; 11 Limitations

[BioMatrix report](https://arxiv.org/html/2606.22138v1) · [Author repository](https://github.com/QizhiPei/BioMatrix)

### BioMamba

2026 published report · Biomedical text

**Training stage:** CPT, then downstream SFT

**Backbone:** Mamba2, 130M through 2.7B

**Corpus:** PubMed MEDLINE abstracts with C4 and English Wikipedia; approximately 508K packed 1,024-token sequences in the reported final corpus.

**PDF/XML/text route:** Abstract text; these are not 508K newly OCRed PDFs.

**Cleaning/filtering:** Tokenization/filtering/shuffling; fixed held-out language-model sets and a separate small-model mixture pilot.

**Training unit and mixture:** Reported target PubMed:C4:WIKIPEDIA mixture 80:10:10; three epochs. Table sequence counts are approximate and do not reproduce that percentage exactly.

**Augmentation:** General-text replay; core CPT does not require teacher-generated paper summaries.

**Reported evidence:** Tokenizer-controlled base/adapted comparisons; general MCQ scores within ±3 percentage points and C4 perplexity changes at most 0.17 in reported comparisons.

**Limits or missing details:** Paper claims released checkpoints; inspected author README still says forthcoming and uses a different license. Verify availability before planning reproduction.

**Where to check:** Materials and Methods; Table 1; public author README

[Published BioMamba paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/) · [Author repository inspected](https://github.com/lingyue404/BioMamba)

### MedFound

2025 · Clinical generalist

**Training stage:** Medical pretraining, diagnostic SFT, preference alignment

**Backbone:** Released 7B and 176B variants

**Corpus:** Medical text and real-world clinical records.

**PDF/XML/text route:** A specific full-paper PDF/OCR route was not verified in the accessible material.

**Cleaning/filtering:** Corpus engineering details should be checked in the complete methods/supplement before adopting them.

**Training unit and mixture:** Medical corpus pretraining followed by diagnosis-focused training; not equivalent to a pure research-literature CPT recipe.

**Augmentation:** Self-bootstrapped diagnostic chain-of-thought and preference alignment are explicitly described at the program level.

**Reported evidence:** Clinical diagnosis, external and rare-disease evaluation, and physician comparisons.

**Limits or missing details:** Limited methods access in this review; do not infer cleaning thresholds, exact corpus counts or extraction software. Clinical records limit full data reproducibility.

**Where to check:** Abstract; accessible code/data availability; official repository

[Published MedFound paper](https://www.nature.com/articles/s41591-024-03416-6) · [Author repository](https://github.com/medfound/medfound)

### MedGemma

2025 report version reviewed · Medical vision-language generalist

**Training stage:** Vision enhancement, pretraining, teacher distillation, RL

**Backbone:** Gemma 3 family

**Corpus:** Medical imaging/report pairs and medical QA, with original SigLIP/Gemma general mixtures for replay. Table 1 lists 41,853 PMC single-panel image-caption examples.

**PDF/XML/text route:** PMC contributes figure-caption data, not a stated OCR pass over every full article.

**Cleaning/filtering:** Restrict PMC-OA component to single-panel medical images; exclude PathVQA/MedVQA for identified quality issues.

**Training unit and mixture:** Joint medical/general multimodal training; medical image and text capabilities are developed across distinct stages.

**Augmentation:** Large instruction-tuned teacher supplies responses/logits; approximately 200K synthetic medical questions generated using five seed questions per prompt.

**Reported evidence:** Medical QA, imaging/report generation and clinical-text evaluations; these do not establish full scientific-PDF extraction accuracy.

**Limits or missing details:** Internal image data and teacher details prevent full end-to-end reproduction. This entry is not a review of every later MedGemma version.

**Where to check:** 2 Data; 3 Model development; Table 1

[MedGemma technical report](https://arxiv.org/html/2507.05201v3)

### Lingshu

2025 · Medical vision-language generalist

**Training stage:** Shallow/deep alignment, SFT, RL

**Backbone:** Qwen2.5-VL 7B/32B

**Corpus:** Collected medical image/text datasets plus synthetic caption, OCR-question, QA and reasoning data; general-domain caption/instruction data are mixed in.

**PDF/XML/text route:** PMC-derived image-caption datasets are training sources; its synthetic OCR examples are rendered questions, not a bulk article-PDF extraction recipe.

**Cleaning/filtering:** Remove images below 64 pixels; perceptual-hash duplicate filtering; caption length 10-1,024 tokens; MinHash-LSH instruction deduplication; evaluation overlap exclusion.

**Training unit and mixture:** Staged alignment before end-to-end instruction tuning.

**Augmentation:** GPT-4o writes captions/QA/reasoning; Gemini reasoning answers must match known exam answers before 50K rendered OCR examples are retained.

**Reported evidence:** Broad medical VQA, text QA and report generation evaluations.

**Limits or missing details:** Reasoning-answer consistency does not independently validate every intermediate claim. Clinical image results do not rank biological literature understanding.

**Where to check:** 2.1-2.3; Table 5

[Lingshu report](https://arxiv.org/html/2506.07044v1) · [Author release organization](https://huggingface.co/lingshu-medical-mllm)

### Hulu-Med

2025 · Medical vision-language generalist

**Training stage:** Alignment, medical CPT, mixed-modality SFT

**Backbone:** Open LLM decoder with patch-based vision encoder

**Corpus:** 16.7M samples: 9M medical multimodal, 4.9M medical text, 1.3M general multimodal and 1.5M general text.

**PDF/XML/text route:** Uses public medical datasets, including literature-derived resources; sample count is not a distinct-paper count.

**Cleaning/filtering:** Dataset-specific processing and synthetic enrichment; the counts describe mixed text, images, volumes and videos.

**Training unit and mixture:** 2D alignment and CPT precede joint text/2D/3D/video instruction tuning; general data are included.

**Augmentation:** Expand captions, create new long captions/VQA, multilingual reasoning and surgical-video annotations.

**Reported evidence:** Tests 30 benchmarks and ablates long-caption and reasoning augmentation; does not compare PDF text extractors.

**Limits or missing details:** Clinical breadth should not be treated as proof that every scientific figure interpretation is grounded.

**Where to check:** Results: data and training; Methods; Extended Tables 4-6

[Hulu-Med report](https://arxiv.org/html/2510.08668v1) · [Author repository](https://github.com/ZJUI-AI4H/Hulu-Med)

### InfiMed-Foundation

2025 · Medical vision-language generalist

**Training stage:** Multimodal CPT and three-stage SFT

**Backbone:** 1.7B/4B foundation-model variants

**Corpus:** Approximately 25B general multimodal plus 5B medical pretraining tokens.

**PDF/XML/text route:** Curates existing medical caption/instruction datasets rather than documenting a new full-paper PDF extraction engine.

**Cleaning/filtering:** Sample 500 examples per dataset; score accuracy, language, completeness, image relevance, and practicality from 1-5 using GPT-o3 and manual review. Reject some whole sources, including PMC-OA in this recipe.

**Training unit and mixture:** Multimodal packing toward 4,096 tokens; reduce visual tokens during CPT; three SFT stages include cross-dataset balancing.

**Augmentation:** Uses curated reasoning/instruction datasets; quality scoring is distinct from reconstructing article evidence.

**Reported evidence:** Medical generalist evaluation and stage ablations.

**Limits or missing details:** Discarding a particular PMC-OA image-caption dataset does not show that all PMC XML literature is poor training data. Dataset-level scoring cannot adjudicate every retained example.

**Where to check:** 3 Data collection and evaluation; 4 Training

[InfiMed-Foundation report](https://arxiv.org/html/2509.22261v1)

### TxGemma

2025 · Therapeutics multitask language model

**Training stage:** Task instruction tuning; conversational variants add general instructions

**Backbone:** Gemma 2, 2B/9B/27B

**Corpus:** Approximately 7M training examples derived from Therapeutic Data Commons; classification, regression and generation.

**PDF/XML/text route:** Structured therapeutics tasks, not reported bulk scientific-PDF CPT.

**Cleaning/filtering:** Uses task datasets and their training partitions; not an extraction-quality recipe.

**Training unit and mixture:** Predict models are instruction tuned; Chat variants also train on general instructions.

**Augmentation:** Represent biological/chemical inputs and targets as task prompts and answers.

**Reported evidence:** Useful example of additional biological training data; should not be cited as evidence for an OCR-then-raw-paper pipeline.

**Limits or missing details:** A biomedical model label alone does not establish continued pretraining on full papers.

**Where to check:** Technical report: training data and model development

[Official technical report](https://storage.googleapis.com/research-media/txgemma/txgemma-report.pdf) · [Official model overview](https://deepmind.google/models/gemma/txgemma/)

## Training-data studies

### Biomed-Enriched

2025 preprint · Text CPT curation study

**Training stage:** Controlled OLMo2-7B-stage1 CPT

**Backbone:** OLMo2-7B-stage1

**Corpus:** Approximately 4.5M PMC-OA XML articles; 133M paragraphs after processing, minimum 64 tokens.

**PDF/XML/text route:** Explicit native XML parsing, without re-OCRing those articles.

**Cleaning/filtering:** Llama-3.1-70B labels 400K paragraphs for domain, type, educational quality and language; distill into XLM-RoBERTa-base. Educational subset keeps scores >=3/5.

**Training unit and mixture:** Equal 33.6B-token runs, 8,192-token context. Compare baseline, paragraph filtering, 10x clinical/case/language upsampling, metadata prefixes and combinations.

**Augmentation:** Teacher-generated labels guide selection; original article text remains the training content.

**Reported evidence:** Table 3: BE-All mean 61.08 versus BE-Base 60.41 (+0.67 pp); BE-Clinical Professional Medicine 63.97 versus 59.93 (+4.04 pp); BE-Educational MedMCQA +1.17 pp.

**Limits or missing details:** Clinical and educational variants do not improve every benchmark or overall average. LLM-label agreement is not human gold; no universal best filter is established.

**Where to check:** 3.1-3.3; 4; Table 3

[Biomed-Enriched paper](https://arxiv.org/html/2506.20331v1)

### PMC-InterCPT / Beyond Captions

2026 preprint, v2 · Multimodal CPT curation study

**Training stage:** CPT with a fixed downstream SFT stage

**Backbone:** Qwen3.5 2B/4B; cross-architecture validation

**Corpus:** PMC/BIOMEDICA figures, captions and article-native context; final 9.63B-token corpus.

**PDF/XML/text route:** Recover captions from PMC XML and attach body text only through article-native figure references.

**Cleaning/filtering:** Repair disconnected context, deduplicate text, prune unsupported non-primary images; Gemini labels relevance/quality, distilled Qwen3-1.7B classifiers filter; benchmark decontamination.

**Training unit and mixture:** Interleaved image-caption-context sequences; final evidence-token allocation 45% biomedical visuals, 30% quantitative evidence, 20% mechanistic structure, 5% auxiliary context.

**Augmentation:** Source reconstruction rather than invented replacement captions. Quality annotators see text, not images; do not treat labels as image-grounding judgments.

**Reported evidence:** Token-matched raw-data control plus identical SFT: +1.46 medical-average and +3.11 general/scientific-average points on Qwen3.5-4B.

**Limits or missing details:** Preprint findings, not independently reproduced here. Reported gains compare to raw CPT; versus SFT-only, general/scientific improvement is only +0.07 points.

**Where to check:** Method; Tables 1-2; Appendix B-C

[Beyond Captions v2](https://arxiv.org/html/2606.01049v2)

### How Post-Training Shapes Biological Reasoning Models

2026 preprint · Biological CPT/SFT/RL study

**Training stage:** Stage-wise biological adaptation experiments

**Backbone:** Qwen3 1.7B/4B; additional backbone/biological encoder comparisons

**Corpus:** FineFineWeb biology: first 200K documents train, next 5K evaluation; downstream DNA/RNA/protein reasoning data.

**PDF/XML/text route:** Biology web text for CPT, not a scientific-PDF OCR study.

**Cleaning/filtering:** Inherits upstream web filtering; no additional benchmark-specific CPT decontamination.

**Training unit and mixture:** Text-only causal CPT at maximum 1,024 tokens, one epoch; later biological encoder alignment, SFT and GRPO are separate stages.

**Augmentation:** Reuses biologically grounded task supervision; study varies stage allocation rather than generating a replacement corpus for every article.

**Reported evidence:** CPT often improves later adaptation; longer SFT can improve in-distribution results while degrading biological out-of-distribution performance.

**Limits or missing details:** Limited task families; stage-allocation comparison is not fully FLOP-matched; scores evaluate final answers, not the correctness of intermediate reasoning.

**Where to check:** 4.3; Limitations; Appendix B.2

[Biological post-training study](https://arxiv.org/html/2606.16517v1) · [Author repository](https://github.com/mims-harvard/bio-posttrain)

## Proposed project experiments — not executed by this literature review

### Native source baseline

Use the current PMC XML as the primary source; preserve ordered sections, captions, table bodies, units, figure-reference links and provenance. Group manuscript versions and duplicates before splitting. Use targeted olmOCR only where source text or page-only information is missing.

Existing XML avoids unnecessary OCR cost; retained structure supports both readable text and later multimodal/entity enrichment.

### Filter validation before deletion

Score paragraphs for corruption, topic, section/type and educational value separately. Audit samples with human source checks; retain scores and rejection reasons. Do not use a clinical-utility score to eliminate experimental biology.

Quality labels measure different properties, and reported clinical/educational filters have task-dependent gains.

### Matched training-value ablation

If training is subsequently authorized, compare clean raw article text, scored/selected text, and text with source-linked figure or entity enrichment using the same backbone, token budget, general replay and downstream SFT. Include a no-CPT baseline and report both domain improvements and general retention.

An OCR/XML agreement score alone cannot show that a corpus improves a foundation model. The current 50-paper batch is an engineering diagnostic, not sufficient evidence for broad training gains.

### Protected biological evaluation

Split at paper/version groups before augmentation; protect held-out papers and benchmark items. For sequence tasks add entity/family/species or time-based splits. Measure extraction fidelity against audited sources separately from trained-model performance and synthetic-answer support.

An XML silver reference, a teacher's quality label, a generated answer and an independent held-out target answer serve different roles.

[Structured review catalog](review.json) · [Actual three-paper extraction results](../pmc_native_v3_preview_2026-10-15/README.md)
