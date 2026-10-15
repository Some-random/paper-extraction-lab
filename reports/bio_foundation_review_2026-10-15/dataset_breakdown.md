**Published data budgets: biological literature, web text and biological databases**

This covers the ten biology/science model families in the preceding [source review](biology_sources.md), with two additional literature-CPT recipes and three figure-training examples. A subsequent [coverage check](coverage_update.md) adds seven new or expanded biological training recipes, including TheBioCollection, SciReasoner, LOGOS and TxGemma. Sources are model reports and author documentation. The quantitative review, the [bounded web-corpus sample](web_sample.md), and our previously executed paper extraction are separate results.

B means billion and M means million. **NR means not separately reported in the inspected source, not zero.** Corpus tokens count an assembled corpus once; training tokens can count repeated exposures. Words, records, image tokens and text tokens are kept distinct. These are each author's tokenizer counts, not a common-tokenizer comparison. A paper downloaded inside an existing dataset is still paper-origin data: the acquisition route and content origin overlap.

**Decoder continued pretraining**

| Model / stage | Paper or abstract text | Web-origin text | Other data in this stage | Reported total and disclosure limit |
|---|---|---|---|---|
| [BioMedGPT-LM, PharMolix](https://arxiv.org/html/2308.09442v2), Llama-2-Chat CPT, §3.1 | **>26B tokens**, 4.2M full-text papers, selected from S2ORC | No separately added web corpus described | Molecule/protein alignment is a later stage | >26B literature-corpus tokens; a source-specific consumed-token breakdown is NR |
| [NatureLM](https://arxiv.org/html/2502.07527v2), science CPT of the 8B / 8×7B models, §2, Tables 1/S1 | **4.0B literature-derived interleaved tokens**, already included in 12.7B cross-domain; further literature may occur in the text bucket | Paper-versus-web split of the **14.4B text** bucket is NR | Molecules **4.2B**, proteins **65.2B**, DNA **19.8B**, RNA **27.5B**, materials **0.02B**, cross-domain **12.7B** | **143.8B corpus tokens** in Table S1; rounded components sum to 143.82B. Not 143.8B paper text |
| [BioMatrix](https://arxiv.org/pdf/2606.22138v1#page=12), Qwen3 CPT, §3, Figure 3 | Part of **79.7B scientific-text tokens**; exact paper share NR | **25.6B FineWeb-Edu** general text; scientific web shares the 79.7B bucket with literature | Molecule-centric **73.7B**, protein-centric **77.4B**, cross-entity/interleaved **48.0B** | **304.4B tokens**, one epoch. The four main categories sum exactly; per-website and per-database budgets NR |

NatureLM's 12.7B cross-domain bucket consists of interleaved literature **4.0B**, text–SMILES **3.0B**, text–protein **1.4B**, text–material **0.2B**, and DNA–protein **4.1B**. Do not add these to the 143.8B total again. Its 1B model first receives **300B SlimPajama text tokens**; that is a separate initialization phase. Later instruction tuning uses **5.1M pairs**, not an additional reported CPT token budget. [NatureLM, §2 and Tables 1/S1](https://arxiv.org/html/2502.07527v2)

BioMatrix's scientific text uses FineFineWeb biology/chemistry/medicine/health and literature; its figure also names bioRxiv. No numeric paper/web split is supplied. Figure 3 subdivides protein tokens into **36.0B sequence / 38.5B structure / 2.9B other**; molecule tokens into **32.1B sequence / 17.6B structure / 24.0B other**; cross-entity tokens into **17.1B sequence / 11.4B structure / 19.5B other**. The “other” subdivisions should not be relabeled entirely as generated text. Sources include PubChem, UniRef/UniProt, PDB/AFDB, interaction datasets and GPT-generated MolTextNet descriptions; exact individual budgets remain NR. These modalities are biomolecular representations, not paper-figure pixels. [BioMatrix, Figure 3 and §3](https://arxiv.org/pdf/2606.22138v1#page=12)

**Two literature-CPT recipes with unusually clear mixtures**

These are medically targeted models, included as quantitative precedents for mixing literature with other material, rather than recommendations to acquire clinical notes.

| Model | Paper / abstract corpus | Web and reusable corpora | Other corpus | What the model actually samples |
|---|---|---|---|---|
| [MEDITRON](https://arxiv.org/html/2311.16079v1), Table 1 | Full-text papers **40.7B**; abstracts **5.48B** training tokens | Web-acquired guidelines **0.107B**; general replay **0.420B** from RedPajama | No additional category in Table 1 | **46.7B train**, **1.4B validation**, reported separately. Rounded training components sum to 46.707B |
| [PMC-LLaMA](https://arxiv.org/html/2304.14454v3), §2 | 4.8M papers, **>75B corpus tokens** | RedPajama general replay; available replay corpus size NR | 30K textbooks, **4B corpus tokens** | Per-batch token ratio **books:papers:general = 15:4:1**, hence **75% / 20% / 5%**. Corpus availability is not the training mixture |

PMC-LLaMA defines one epoch as seeing the book tokens once and trains for five such epochs. It does not mean five passes over its >75B paper pool. I have not replaced the reported schedule with a falsely precise consumed-token estimate. [PMC-LLaMA, Combination / Knowledge Injection Training](https://arxiv.org/html/2304.14454v3)

**Other biology/science pretraining: do not silently label these decoder CPT**

| Model / actual stage | Literature contribution | Web / other dataset contribution | Quantitative limit |
|---|---|---|---|
| [BioMedLM](https://arxiv.org/html/2403.18421v1), decoder from scratch, §3.3 | The Pile's PubMed abstracts + PMC full articles: **34.6B corpus tokens combined** | No additional general web or database corpus in pretraining | **300B training tokens**, **8.67 passes**. Abstract/full-text token split NR; 300B is not distinct collected text |
| [BioGPT](https://arxiv.org/pdf/2210.10341), decoder from scratch, Pre-training Method / Experiments | **15M title-and-abstract records**, not full papers | Downloaded PubMed records; no other pretraining source described | Unique corpus token count NR. **200,000 × 524,288 = 104.8576B scheduled token positions**, calculated from the reported steps/global batch; includes repetitions and is not a distinct-corpus count |
| [BioBERT](https://arxiv.org/pdf/1901.08746), encoder CPT, Tables 1/2 and §4.2 | Available PubMed **4.5B words**; PMC **13.5B words** | Initial BERT already trained on Wikipedia **2.5B words** and BooksCorpus **0.8B words** | Words are not tokenizer tokens. v1.0 combined adaptation: **200K PubMed + 270K PMC steps**; v1.1: **1M PubMed steps**. Different variants use different subsets |
| [PubMedBERT](https://arxiv.org/html/2007.15779v6), encoder from scratch, §2.5/3.2 | Standard: **14M abstracts, 3.2B words, 21GB**. Added-PMC experiment: **16.8B words, 107GB total** | No general web replay in the standard recipe | Unique tokenizer-token count NR. Standard training **62,500 steps × 8,192 examples**; this example count is not a token count |
| [BioLinkBERT](https://arxiv.org/html/2203.15827), encoder from scratch, §6.1 | Same **21GB PubMed abstract corpus** as PubMedBERT, with citation links | No separately added web/replay corpus in the biological recipe | Token count NR. Contiguous/random/citation-linked **instance types each one third**; these are not three different data sources. Both biological model sizes train from scratch |
| [BioT5+](https://arxiv.org/html/2402.17810v2), encoder–decoder pretraining, §3 / Appendix B | PMC full text, PubMed/bioRxiv abstracts and entity-wrapped abstracts | **C4 web text**, PubChem/ZINC20 molecules, UniRef50 proteins, paired descriptions | Source token counts NR. **Eight tasks balanced by examples within each batch**; not evidence of eight equal token shares. **300K steps, 8×96 examples/batch, maximum input 512 tokens** |
| [Galactica](https://arxiv.org/pdf/2211.09085), science decoder from scratch, Tables 2/22–24 | **88B tokens** from papers + abstracts, **83.0%** reported corpus share | Filtered Common Crawl **1B**; reference material **7B** includes Wikipedia, StackExchange and educational websites/books; code **7B** | Knowledge bases **2B**, prompts **0.4B**, other **0.2B**; headline corpus **106B**, training **450B**, **4.25 epochs**. Rounded rows do not sum exactly to the headline |

BioT5+ does not publish enough information to convert its sampling scheme into “X billion paper tokens, Y billion web tokens.” Its text describes an addition of “28.8M full articles from PubMed”; I have not treated that ambiguous source description as a verified full-text count. This uncertainty does not affect the disclosed eight-task balancing scheme. [BioT5+, §3 / Appendix B](https://arxiv.org/html/2402.17810v2)

Galactica explicitly discloses biological literature: **PMC 23B**, **PubMed abstracts 5B**, **bioRxiv 1B** tokens; these are components of the 88B literature bucket. Other listed literature: arXiv **35B**, Semantic Scholar full text **18B**, Semantic Scholar abstracts **4B**, plus smaller sources. Its biological knowledge bases include PubChem **1B**, UniProt **0.6B**, RefSeq **0.1B**, Ribosome **0.05B**, LIPID MAPS **0.03B**, Reactome **0.01B**. Biological material can also occur in broader sources, so this is not an exhaustive biological-total calculation. [Galactica, Tables 22/24](https://arxiv.org/pdf/2211.09085#page=42)

**General corpus context: OLMo 3 and Dolma**

These are not measured biological mixtures. OLMo 3 does not disclose the biological-paper fraction of its PDF pool. The following numbers describe its general base-model data curriculum, not a prescription for our project. [OLMo 3, Tables 4/5](https://arxiv.org/html/2512.13961v2)

| OLMo 3 stage | Web sources | Literature / academic documents | Remaining sources | Reported total |
|---|---|---|---|---|
| Stage 1, Table 4 “6T Mix” | Common Crawl **4.51T**; FineMath **152B**; Wikipedia/Wikibooks **2.51B** | olmOCR science PDFs **805B**; arXiv **50.8B** | Stack-Edu code **409B** | **5.93T** sampled tokens, not the larger 9.31T available pool |
| Stage 2 midtraining, Table 5 “100B Mix” | HQ Common Crawl **22.4B**; STEM-heavy web **4.99B** | HQ olmOCR science PDFs **4.99B** | StackEdu FIM **10B**, plus separately enumerated synthetic math/code/QA/reasoning/instruction sources | **99.95B** sampled tokens; source-row rounding applies |

The original **Dolma** corpus reports **Common Crawl 2,479B; GitHub 411B; Reddit 89B; Semantic Scholar/peS2o 70B; Gutenberg 6B; Wikipedia/Wikibooks 4.3B**, approximately **3,059B total** with its stated tokenizer. This is a reusable dataset's composition, not a biology-only training run or the later Dolma 3 mix. Its academic component can be selected for biology; that selected amount is not given by the 70B headline. [Original Dolma, Table 1 / §8](https://arxiv.org/html/2402.00159)

**Figure-inclusive budgets**

| Model / dataset | Literature-derived amount | Treatment of figure content |
|---|---|---|
| [BiomedCLIP / PMC-15M](https://arxiv.org/html/2303.00915), Dataset / Modeling | **15,282,336 image–caption pairs**, collected from a 4.4M-article PMC snapshot | Original images plus source captions, contrastive image/text training. Pair counts are not text tokens |
| [LLaVA-Med](https://arxiv.org/html/2306.00890), §3 | **600K source image–caption pairs** for alignment; **60K instruction examples** in its larger instruction datasets | Alignment predicts original captions. GPT-4 generates later conversations using captions and, for 60K-IM, referring article text; this is a separate generated-data stage |
| [PMC-InterCPT](https://arxiv.org/html/2606.01049v2), Tables 8/9 | **9.63B combined text + image tokens** after resampling | Final token mixture: biomedical visual evidence **4.33B (45%)**; quantitative/table **2.89B (30%)**; mechanism/structure **1.93B (20%)**; auxiliary **0.48B (5%)** |

PMC-InterCPT's **15.41B-token pre-sampling pool** has **7.18B text / 8.23B image tokens**. That split must not be applied unchanged to its differently resampled 9.63B final corpus. It recovers author captions from XML and attaches explicitly referring context. Its Gemini/Qwen quality classifiers label text; they do not produce replacement figure captions. [PMC-InterCPT, Source-Grounded Recovery, Quality Classification, Tables 8/9](https://arxiv.org/html/2606.01049v2)

**What to use in this project**

The literature supports several successful mixtures; it does not establish one best biological paper/web/database percentage. First measure our retained material with the eventual backbone tokenizer, and record both (a) content origin: literature, web exposition, database or generated derivative and (b) delivery: PMC, peS2o, Dolma/FineFineWeb or direct fetch. Deduplicate across delivery routes before counting. Keep available tokens, sampled training tokens and repeated exposures as separate totals.

Our current three-paper pipeline already preserves the real research text, source tables/spreadsheets and original figures with captions/context. It has not trained a model, synthesized figure descriptions, or ingested the full external corpora in this table. The next acquisition routes are described in [web acquisition](web_acquisition.md), with [an actual 64KiB corpus probe](web_sample.md); [figure handling](figure_handling.md) explains the training representations.
