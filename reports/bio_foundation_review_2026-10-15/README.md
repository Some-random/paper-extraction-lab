# Biological continued pretraining: data sources and token budgets

The comparison below focuses on **continued pretraining (CPT)**: starting with a pretrained model and training it further on domain data. Data-curation studies and released models appear together because both inform this choice.

Counts follow each paper’s reported budget and may include general text, other sciences and biological sequences. The **Source** column links to the paper and detailed notes.

[Processing recipe](data_pipeline.md).

## Available data and overall storage

**The broader PMC inventory contains 9.32 million paper candidates.** The 55-journal inventory already contains **552,024 candidate papers**. The journal list is an initial subset, not a limit on collection. The broader inventory includes clinical and other material; its research-biology yield is still unmeasured.

**Available sources extend well beyond 50B; that estimate covers only a first subset.** [OLMo 3’s scientific PDF pool](https://arxiv.org/html/2512.13961v2#S3.SS4) reports **972B text tokens** across subjects. [OpenGenome2](https://huggingface.co/datasets/arcinstitute/opengenome2) provides **8.8T nucleotide positions** of biological sequence. A 1T-token corpus is therefore a plausible target when sequences are included. A deduplicated biology-only total in our tokenizer still needs to be measured; these published amounts use different units and overlap other sources.

**First quantified subset: about 49.1B retained tokens; roughly 35–70B across sensitivity scenarios.** This estimate covers the quantified journal subset and the two datasets below, not the whole PMC inventory. It is a forecast, not an already downloaded or processed corpus. Deduplication alone leaves about **116.5B**; the smaller research pool assumes further selection, especially retaining 15% of FineFineWeb biology text.

| Source content | Estimated tokens |
|:---|---:|
| Papers: 552,024 candidates in the initial journal subset | 4.2B |
| Web text imported from FineFineWeb biology | 11.6B |
| Biological database records imported from TheBioCollection | 33.3B |
| **Total** | **49.1B** |

**[TheBioCollection](https://huggingface.co/datasets/trillionlabs/TheBioCollection)** is a released collection of records from UniProt, PubChem and other biological databases: protein/DNA/RNA sequences, molecular representations, descriptions and annotations. This estimate uses its free-text stream, excluding its separate instruction dataset.

A small prefix probe projects **1.5B protein-sequence tokens, 0.25B DNA/RNA tokens and 5.0B SMILES/InChI tokens** within this same pool. These modality projections are less certain than source inventories and must not be added to the total. General-text replay is additional; available-pool proportions do not prescribe training weights.

**Overall storage: reserve about 4TiB for the first quantified subset.** The combined estimate is **3.3–3.6TiB**, including retained paper PDFs/figures, XML, dataset text, token IDs, metadata, indexes and working space. Each additional million retained papers adds roughly **7.2TiB** for PDFs and figures alone; a larger paper collection needs a larger storage allocation. At 1T retained tokens, four-byte token IDs alone occupy 3.64TiB, before text, originals and indexes. These projections exclude separate supplements and model/training files. [Inventories and storage assumptions](source_planning.md).

## Continued pretraining

Both tables are sorted **Strong → Solid → Mixed → Weak**, alphabetically within each rating.

| Model /<br>starting checkpoint | Paper tokens /<br>origin | Dataset tokens /<br>sources | Other modalities /<br>tokens | Total<br>tokens | Paper<br>assessment | Authors /<br>institutions | Source |
|:---|:---|:---|:---|:---|:---|:---|:---|
| BioBERT<br>BERT | —<br>PubMed abstracts; PMC full text | — | Text only | Not reported | **Strong**<br>Clear, well-executed foundational study | J. Lee et al.<br>Korea University; NAVER | [Paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7703786/)<br>[Notes](papers/biobert.md) |
| Biomed-Enriched<br>OLMo2-7B-stage1 | 33.6B<br>PMC-OA XML | 0 | Text only | 33.6B | **Solid**<br>Careful, useful; incremental contribution | R. Touchent et al.<br>Sorbonne; Inria | [Paper](https://arxiv.org/html/2506.20331v1)<br>[Notes](papers/biomed_enriched.md) |
| How Post-Training Shapes Biological Reasoning<br>Qwen3-1.7B / 4B | —<br>No direct paper stream in CPT | —<br>FineFineWeb | Text-only CPT; DNA/RNA/protein encoders used later | Not reported | **Solid**<br>Thoughtful empirical study; limited scope | L. Fesser, H. Zhang et al.<br>Harvard; Google | [Paper](https://arxiv.org/html/2606.16517v1)<br>[Notes](papers/bio_posttraining.md) |
| LOGOS<br>Qwen3-8B; Llama 3.2-1B / 3B variants | 0<br>No paper-text stream | 44.87B<br>UniRef90<br>OAS<br>PubChemQC | Seven-modality corpus: 44.87B<br>Combined pre/post-training corpus; per-modality split not reported. | 44.87B | **Solid**<br>Coherent representation idea; bounded validation | M. Li et al.<br>Alibaba; Renmin | [Paper](https://arxiv.org/html/2606.16905v1)<br>[Notes](papers/logos.md) |
| NatureLM<br>Llama 3 8B / Mixtral 8×7B | —<br>Repository not specified | ≥116.72B<br>PubChem<br>UniProt<br>Materials Project (+1) | Protein: 65.2B<br>DNA: 19.8B<br>RNA: 27.5B<br>Molecules: 4.2B<br>Materials: 20M<br>Cross-domain: 12.7B<br>Domain totals include associated text. | 143.8B | **Solid**<br>Ambitious and useful; uneven claim support | NatureLM team<br>Microsoft Research AI for Science | [Paper](https://arxiv.org/html/2502.07527v2)<br>[Notes](papers/naturelm.md) |
| PMC-InterCPT / Beyond Captions<br>Qwen3.5-2B / 4B-Base | —<br>PMC-OA XML | —<br>BIOMEDICA | Figure images: not reported<br>9.63B total combines text and images | 9.63B | **Solid**<br>Useful reconstruction method; modest added value | G. Zhu et al.<br>HK PolyU; Sun Yat-sen +2 | [Paper](https://arxiv.org/html/2606.01049v2)<br>[Notes](papers/pmc_intercpt.md) |
| TheBioCollection / Gravity-bio<br>Gravity-16B-A3B, before annealing | ≥54B<br>PubMed; bioRxiv; medRxiv | ≥52.6B<br>PubChem<br>UniProt<br>GENCODE (+9) | Molecules: 28.2B<br>Proteins: 14.5B<br>Genomics: 7.1B<br>Cells/pathways: 2.8B<br>Domain totals include associated text and records. | Not reported | **Solid**<br>Valuable corpus; external validation still needed | H. Seo, H. Hwang et al.<br>Trillion Labs; KAIST +3 | [Paper](https://arxiv.org/html/2607.08803v1)<br>[Notes](papers/gravity_bio.md) |
| BioMamba<br>Mamba2 checkpoints, 130M–2.7B | ≈434.176M<br>PubMed/MEDLINE | ≈86.016M<br>C4<br>English Wikipedia | Text only | ≈520.192M | **Mixed**<br>Reasonable adaptation study; reporting gaps | L. Yue et al.<br>RPI; IBM Research +3 | [Paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/)<br>[Notes](papers/biomamba.md) |
| BioMatrix<br>Qwen3-1.7B / 4B | —<br>PubMed; bioRxiv | ≥176.7B<br>FineWeb-Edu<br>PubChem<br>UniRef50 (+16) | Protein: 77.4B (1D 36B; 3D 38.5B; other 2.9B)<br>Molecule: 73.7B (1D 32.1B; 3D 17.6B; other 24B)<br>Cross-entity: 48B (1D 17.1B; 3D 11.4B; other 19.5B)<br>Domain totals include associated text; 1D = sequence, 3D = structure. | 304.4B<br>127.7B source split unknown | **Mixed**<br>Substantial engineering; overbroad validation claims | Q. Pei et al.<br>Renmin; Shanghai AI Lab +5 | [Paper](https://arxiv.org/pdf/2606.22138v1#page=12)<br>[Notes](papers/biomatrix.md) |
| BioMedGPT-LM<br>Llama2-Chat-7B | 0<br>via S2ORC (reused) | >26B<br>S2ORC | Text-only CPT; molecule/protein encoders used later | >26B | **Mixed**<br>Useful prototype; validation is narrow | Y. Luo et al.<br>Tsinghua AIR; PharMolix | [Paper](https://arxiv.org/html/2308.09442v2)<br>[Notes](papers/biomedgpt.md) |
| SciReasoner<br>Qwen3-1.7B / 8B | —<br>PubMed | ≥166B<br>UniRef50/90<br>RNAcentral<br>C4 | Protein: 55B<br>Chemistry: 50B<br>DNA: 30B<br>RNA: 26B<br>Materials: 5B<br>Domain totals; include associated text. | 206B | **Mixed**<br>Broad ambition; inconsistent reporting | Y. Wang et al.<br>Shanghai AI Lab; collaborators | [Paper](https://arxiv.org/html/2509.21320v1)<br>[Notes](papers/scireasoner.md) |

**Quality** considers contribution, technical soundness, evaluation, reproducibility and clarity. Strong = convincing contribution; Solid = worthwhile with limits; Mixed = substantial strengths and weaknesses; Weak = fundamental problems. These are provisional judgments explained in the notes.

### Reading the counts

- **Sources:** paper tokens come from publication repositories; dataset tokens come from imported corpora or databases. Paper text imported through S2ORC or The Pile belongs in existing datasets.
- **—** means an amount is unavailable or cannot be separated; **0** means no data through that route. Named sources can still have an unknown token count.
- **M / B** mean million / billion; **≈** means approximate; **> / ≥** indicate a lower bound. Full dataset lists, counting methods and qualifications are in **Notes**.

**Other modalities** are already included in the acquisition columns. **1D** means sequences; **3D** means structures. Domain and record totals can include annotations and text. Later-stage encoder inputs are identified separately.

**BioMatrix’s full corpus adds up: 105.3B text + 77.4B protein data + 73.7B molecule data + 48B cross-entity data = 304.4B.**

Of BioMatrix’s total, **176.7B** is identified as existing-dataset input. The other **127.7B** (79.7B scientific text + 48B cross-entity data) has no disclosed paper/web/dataset split. Those tokens are accounted for in the full composition; adding the modality column to the source columns would count them twice.

## Pretraining from scratch: comparison

These models begin with randomly initialized weights and biological or scientific data, rather than adapting an existing checkpoint. They provide a comparison with CPT.

| Model /<br>architecture | Paper tokens /<br>origin | Dataset tokens /<br>sources | Other modalities /<br>tokens | Total<br>tokens | Paper<br>assessment | Authors /<br>institutions | Source |
|:---|:---|:---|:---|:---|:---|:---|:---|
| BioLinkBERT<br>BERT architecture | —<br>PubMed abstracts | — | Text only | Not reported | **Strong**<br>Clear method; substantive ablations and results | M. Yasunaga et al.<br>Stanford | [Paper](https://aclanthology.org/2022.acl-long.551/)<br>[Notes](papers/biolinkbert.md) |
| PubMedBERT<br>BERT architecture | —<br>PubMed abstracts; PMC full text | — | Text only | Not reported | **Strong**<br>Focused question; systematic and useful analysis | Y. Gu, R. Tinn et al.<br>Microsoft Research | [Paper](https://doi.org/10.1145/3458754)<br>[Notes](papers/pubmedbert.md) |
| BioGPT<br>GPT-2-style architecture | 104.8576B<br>PubMed titles/abstracts | 0 | Text only | 104.8576B | **Solid**<br>Useful early decoder study; conventional method | R. Luo et al.<br>Microsoft Research; Peking | [Paper](https://arxiv.org/pdf/2210.10341)<br>[Notes](papers/biogpt.md) |
| BioMedLM<br>2.7B GPT-style decoder | 0<br>via The Pile PubMed components (reused) | 34.6B<br>The Pile: PubMed Central<br>The Pile: PubMed Abstracts | Text only | 34.6B | **Solid**<br>Transparent resource; limited methodological novelty | E. Bolton et al.<br>Stanford; Databricks | [Paper](https://arxiv.org/html/2403.18421v1)<br>[Notes](papers/biomedlm.md) |
| Galactica<br>scientific decoder | ≥64.926B<br>arXiv; PMC; PubMed abstracts (+6) | ≥23.87B<br>UniProt<br>PubChem<br>Papers with Code | Protein records: ≈600M<br>Molecule records: ≈1B<br>Genome records: ≈100M<br>Record totals include text; pure sequence/SMILES shares not reported. | ≈106B | **Mixed**<br>Substantial scientific LM; reliability claims weak | R. Taylor et al.<br>Meta AI | [Paper](https://arxiv.org/html/2211.09085v1)<br>[Notes](papers/galactica.md) |
