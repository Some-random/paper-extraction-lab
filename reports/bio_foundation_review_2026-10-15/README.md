# Biological continued pretraining: data sources and token budgets

The comparison below focuses on **continued pretraining (CPT)**: starting with a pretrained model and training it further on domain data. Data-curation studies and released models appear together because both inform this choice.

Counts follow each paper’s reported budget and may include general text, other sciences and biological sequences. The **Source** column links to the paper and detailed notes.

**Direct web tokens** measures text from webpages or crawls collected directly by the reviewed study. Web text imported through FineWeb, C4 or FineFineWeb goes under **Existing-dataset tokens**. This is why direct-web counts are often 0 or unavailable even when web-origin text is used. Galactica is an exception with **≥700M** direct-web tokens from ScientificCC. **0** means no data through that route; **—** means the amount or split was not reported.

[Processing recipe](data_pipeline.md).

## Starter corpus: expected data and resources

**About 49.1B retained tokens; roughly 35–70B across sensitivity scenarios.** This forecasts what the available source inventories could yield after research selection and rough deduplication. It is not an already downloaded or processed corpus. Deduplication alone leaves about **116.5B**; the smaller research pool assumes further selection, especially retaining 15% of FineFineWeb biology text.

| Source content | Central retained-token estimate |
|---|---:|
| Papers: selected 55-journal PMC inventory | 4.2B |
| Web text imported from FineFineWeb biology | 11.6B |
| Biological database records imported from TheBioCollection | 33.3B |
| **Total** | **49.1B** |

The database row includes descriptions and annotations. A small prefix probe projects **1.5B protein-sequence tokens, 0.25B DNA/RNA tokens and 5.0B SMILES/InChI tokens** within this same pool. These modality projections are less certain than source inventories and must not be added to the total. General-text replay is additional; available-pool proportions do not prescribe training weights.

**Processing:** download native XML and dataset shards; extract text with source IDs and citation metadata; remove broken records and boilerplate; match paper identities, exact duplicates and verified near-duplicates; apply research/quality filters with human review, plus sequence/chemical validity checks; tokenize the retained pools and test sampling mixtures. PDFs needing OCR form a separate workload.

| Work | Planning time / resources |
|---|---|
| Native acquisition | 2–7 days, one serial fetcher; about 552k XML objects plus dataset shards |
| Normalize, clean and deduplicate | 3–10 days on 16 CPU cores, 128–256GiB RAM |
| Train/apply scorers and review | 150–600 A100 GPU-hours; 6–25 days on one GPU, plus 32–64 person-hours |
| Illustrative 7B mixture experiments | 400–1,200 A100 GPU-hours; 2–13 days with 4–8 GPUs |

**Storage:** allow **500–800GiB** for text/sequence processing. Retaining the projected paper PDFs and figures adds approximately **2.8TiB**, beyond that allowance. The current paper runner uses two CPU threads; the larger allocations above are planning scenarios. Rates are unbenchmarked, stages can overlap, and times exclude implementation, scheduler waits and full-paper OCR. [Source counts, retention assumptions and cost calculations](source_planning.md).

## Continued pretraining

Both tables are sorted **Strong → Solid → Mixed → Weak**, alphabetically within each rating.

| Model / starting checkpoint | Online-paper tokens / origin | Direct web tokens | Existing-dataset tokens | Total reported tokens | Other modalities / tokens | Overall paper assessment | Authors / institutions | Source |
|---|---:|---:|---:|---:|---|---|---|---|
| BioBERT<br>BERT | —<br>PubMed abstracts; PMC full text | — | — | Not reported | Text only | **Strong**<br>Clear, well-executed foundational study | J. Lee et al.<br>Korea University; NAVER | [Paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7703786/) · [Notes](papers/biobert.md) |
| Biomed-Enriched<br>OLMo2-7B-stage1 | 33.6B<br>PMC-OA XML | 0 | 0 | 33.6B | Text only | **Solid**<br>Careful, useful; incremental contribution | R. Touchent et al.<br>Sorbonne; Inria | [Paper](https://arxiv.org/html/2506.20331v1) · [Notes](papers/biomed_enriched.md) |
| How Post-Training Shapes Biological Reasoning<br>Qwen3-1.7B / 4B | —<br>No direct paper stream in CPT | — | —<br>FineFineWeb | Not reported | Text-only CPT; DNA/RNA/protein encoders used later | **Solid**<br>Thoughtful empirical study; limited scope | L. Fesser, H. Zhang et al.<br>Harvard; Google | [Paper](https://arxiv.org/html/2606.16517v1) · [Notes](papers/bio_posttraining.md) |
| LOGOS<br>Qwen3-8B; Llama 3.2-1B / 3B variants | 0<br>No paper-text stream | 0 | 44.87B<br>UniRef90; OAS; PubChemQC | 44.87B | Seven-modality corpus: 44.87B<br>Combined pre/post-training corpus; per-modality split not reported. | **Solid**<br>Coherent representation idea; bounded validation | M. Li et al.<br>Alibaba; Renmin | [Paper](https://arxiv.org/html/2606.16905v1) · [Notes](papers/logos.md) |
| NatureLM<br>Llama 3 8B / Mixtral 8×7B | —<br>Repository not specified | — | ≥116.72B<br>PubChem; UniProt; Materials Project (+1) | 143.8B | Protein: 65.2B<br>DNA: 19.8B<br>RNA: 27.5B<br>Molecules: 4.2B<br>Materials: 20M<br>Cross-domain: 12.7B<br>Domain totals include associated text. | **Solid**<br>Ambitious and useful; uneven claim support | NatureLM team<br>Microsoft Research AI for Science | [Paper](https://arxiv.org/html/2502.07527v2) · [Notes](papers/naturelm.md) |
| PMC-InterCPT / Beyond Captions<br>Qwen3.5-2B / 4B-Base | —<br>PMC-OA XML | — | —<br>BIOMEDICA | 9.63B | Figure images: not reported<br>9.63B total combines text and images | **Solid**<br>Useful reconstruction method; modest added value | G. Zhu et al.<br>HK PolyU; Sun Yat-sen +2 | [Paper](https://arxiv.org/html/2606.01049v2) · [Notes](papers/pmc_intercpt.md) |
| TheBioCollection / Gravity-bio<br>Gravity-16B-A3B, before annealing | ≥54B<br>PubMed; bioRxiv; medRxiv | — | ≥52.6B<br>PubChem; UniProt; GENCODE (+9) | Not reported | Molecules: 28.2B<br>Proteins: 14.5B<br>Genomics: 7.1B<br>Cells/pathways: 2.8B<br>Domain totals include associated text and records. | **Solid**<br>Valuable corpus; external validation still needed | H. Seo, H. Hwang et al.<br>Trillion Labs; KAIST +3 | [Paper](https://arxiv.org/html/2607.08803v1) · [Notes](papers/gravity_bio.md) |
| BioMamba<br>Mamba2 checkpoints, 130M–2.7B | ≈434.176M<br>PubMed/MEDLINE | 0 | ≈86.016M<br>C4; English Wikipedia | ≈520.192M | Text only | **Mixed**<br>Reasonable adaptation study; reporting gaps | L. Yue et al.<br>RPI; IBM Research +3 | [Paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13635941/) · [Notes](papers/biomamba.md) |
| BioMatrix<br>Qwen3-1.7B / 4B | —<br>PubMed; bioRxiv | — | ≥176.7B<br>FineWeb-Edu; PubChem; UniRef50 (+16) | 304.4B<br>127.7B source split unknown | Protein: 77.4B (1D 36B; 3D 38.5B; other 2.9B)<br>Molecule: 73.7B (1D 32.1B; 3D 17.6B; other 24B)<br>Cross-entity: 48B (1D 17.1B; 3D 11.4B; other 19.5B)<br>Domain totals include associated text; 1D = sequence, 3D = structure. | **Mixed**<br>Substantial engineering; overbroad validation claims | Q. Pei et al.<br>Renmin; Shanghai AI Lab +5 | [Paper](https://arxiv.org/pdf/2606.22138v1#page=12) · [Notes](papers/biomatrix.md) |
| BioMedGPT-LM<br>Llama2-Chat-7B | 0<br>via S2ORC (reused) | 0 | >26B<br>S2ORC | >26B | Text-only CPT; molecule/protein encoders used later | **Mixed**<br>Useful prototype; validation is narrow | Y. Luo et al.<br>Tsinghua AIR; PharMolix | [Paper](https://arxiv.org/html/2308.09442v2) · [Notes](papers/biomedgpt.md) |
| SciReasoner<br>Qwen3-1.7B / 8B | —<br>PubMed | — | ≥166B<br>UniRef50/90; RNAcentral; C4 | 206B | Protein: 55B<br>Chemistry: 50B<br>DNA: 30B<br>RNA: 26B<br>Materials: 5B<br>Domain totals; include associated text. | **Mixed**<br>Broad ambition; inconsistent reporting | Y. Wang et al.<br>Shanghai AI Lab; collaborators | [Paper](https://arxiv.org/html/2509.21320v1) · [Notes](papers/scireasoner.md) |

**Quality** considers contribution, technical soundness, evaluation, reproducibility and clarity. Strong = convincing contribution; Solid = worthwhile with limits; Mixed = substantial strengths and weaknesses; Weak = fundamental problems. These are provisional judgments explained in the notes.

### Reading the counts

- **Sources:** online papers are acquired directly from publication repositories; direct web tokens come from other directly collected webpages or crawls; existing datasets are imported corpora or databases. Paper text imported through S2ORC or The Pile belongs in existing datasets.
- **—** means an amount is unavailable or cannot be separated; **0** means no data through that route. Named sources can still have an unknown token count.
- **M / B** mean million / billion; **≈** means approximate; **> / ≥** indicate a lower bound. Full dataset lists, counting methods and qualifications are in **Notes**.

**Other modalities** are already included in the acquisition columns. **1D** means sequences; **3D** means structures. Domain and record totals can include annotations and text. Later-stage encoder inputs are identified separately.

**BioMatrix’s full corpus adds up: 105.3B text + 77.4B protein data + 73.7B molecule data + 48B cross-entity data = 304.4B.**

Of BioMatrix’s total, **176.7B** is identified as existing-dataset input. The other **127.7B** (79.7B scientific text + 48B cross-entity data) has no disclosed paper/web/dataset split. Those tokens are accounted for in the full composition; adding the modality column to the source columns would count them twice.

## Pretraining from scratch: comparison

These models begin with randomly initialized weights and biological or scientific data, rather than adapting an existing checkpoint. They provide a comparison with CPT.

| Model / architecture | Online-paper tokens / origin | Direct web tokens | Existing-dataset tokens | Total reported tokens | Other modalities / tokens | Overall paper assessment | Authors / institutions | Source |
|---|---:|---:|---:|---:|---|---|---|---|
| BioLinkBERT<br>BERT architecture | —<br>PubMed abstracts | — | — | Not reported | Text only | **Strong**<br>Clear method; substantive ablations and results | M. Yasunaga et al.<br>Stanford | [Paper](https://aclanthology.org/2022.acl-long.551/) · [Notes](papers/biolinkbert.md) |
| PubMedBERT<br>BERT architecture | —<br>PubMed abstracts; PMC full text | — | — | Not reported | Text only | **Strong**<br>Focused question; systematic and useful analysis | Y. Gu, R. Tinn et al.<br>Microsoft Research | [Paper](https://doi.org/10.1145/3458754) · [Notes](papers/pubmedbert.md) |
| BioGPT<br>GPT-2-style architecture | 104.8576B<br>PubMed titles/abstracts | 0 | 0 | 104.8576B | Text only | **Solid**<br>Useful early decoder study; conventional method | R. Luo et al.<br>Microsoft Research; Peking | [Paper](https://arxiv.org/pdf/2210.10341) · [Notes](papers/biogpt.md) |
| BioMedLM<br>2.7B GPT-style decoder | 0<br>via The Pile PubMed components (reused) | 0 | 34.6B<br>The Pile: PubMed Central; The Pile: PubMed Abstracts | 34.6B | Text only | **Solid**<br>Transparent resource; limited methodological novelty | E. Bolton et al.<br>Stanford; Databricks | [Paper](https://arxiv.org/html/2403.18421v1) · [Notes](papers/biomedlm.md) |
| Galactica<br>scientific decoder | ≥64.926B<br>arXiv; PMC; PubMed abstracts (+6) | ≥700M | ≥23.87B<br>UniProt; PubChem; Papers with Code | ≈106B | Protein records: ≈600M<br>Molecule records: ≈1B<br>Genome records: ≈100M<br>Record totals include text; pure sequence/SMILES shares not reported. | **Mixed**<br>Substantial scientific LM; reliability claims weak | R. Taylor et al.<br>Meta AI | [Paper](https://arxiv.org/html/2211.09085v1) · [Notes](papers/galactica.md) |
