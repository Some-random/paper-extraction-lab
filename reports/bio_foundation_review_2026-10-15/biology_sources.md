# Biological research models and the real data behind them

This is the project's corrected focus: biological research literature, source figures, complete tables and supplements, reusable text corpora, and biological sequence/structure/assay databases. Clinical-note corpora are outside this scope. Published recipes below are source reviews, not experiments reproduced here.

For source amounts and training mixtures, see the [per-model quantitative breakdown](dataset_breakdown.md). The [web acquisition guide](web_acquisition.md), [64KiB web-corpus probe](web_sample.md), and [figure-handling review](figure_handling.md) address the next acquisition and representation decisions.

**What is already implemented**

The [v4 three-paper pipeline](../pmc_native_v4_citations_2026-10-15/README.md) expands bibliography markers to full cited titles plus first author/et al. It preserves all source-supplied authors and identifiers in structured records. It checks all 322 source citation-marker elements, including 12 numeric ranges, across 211 bibliography entries. One web resource has no author supplied; the output says so rather than inventing one. The selected policy is implemented directly, without a comparison experiment.

For tables, the XML branch reads the actual source cells, headers, notes and merged spans. All four main-article tables are complete: 15×3 and 21×5 for OTULIN, and 9×4 and 8×5 for the proteomics paper, including header rows. A merged group value appears once, with covered slots pointing to its source cell.

Main-article XML does not include every separate spreadsheet's contents. We inventoried [41 supplementary files, including 33 XLSX files](../pmc_native_v4_citations_2026-10-15/supplements/README.md). Two original Lsp2 workbooks were fully parsed: nine worksheets, 35,468 nonempty source rows and 184,530 populated cells. Full TSV files preserve worksheet row numbers and column coordinates; each displayed 20-row excerpt is explicitly a preview. Original workbooks total 1,927,008 bytes and passed official media-manifest checksums. The 11,889,596-byte pSILAC intensity workbook is explicitly deferred under the 8 MiB per-file sample bound. Other unparsed supplements remain listed.

For figures, the branch retains original publisher images, source captions and the paragraphs that explicitly cite them. It emits ordered image/text/table records using those source links. The 25 existing figure images are reused byte-for-byte. Source figure records do not constitute a new interpretation of plots, microscopy, blots or diagrams. Pure-text CPT sees text and table serialization; using figure pixels requires a vision-language training model. These records have not been vision-tokenized or used for training.

**S2ORC, peS2o and Dolma are different objects**

S2ORC means **Semantic Scholar Open Research Corpus**. It aggregates research metadata and machine-readable academic text, including citation and figure/table mentions, across publishers and archives. The original 2020 release reported 81.1M paper records, with structured full text for 8.1M open-access papers; those are historical snapshot counts, not current availability. It is a corpus, not an OCR model. [Original S2ORC paper](https://aclanthology.org/2020.acl-main.447/)

peS2o is an already cleaned and packaged language-model corpus derived from S2ORC and Semantic Scholar abstracts. Its v2 training split lists **8,242,162 full-text-derived records and 30,569,017 title/abstract-derived records**. Thus, approximately 39M documents must not be described as 39M full-text papers. Its full-text branch uses GROBID-derived text and removes figures, tables and references. This saves extraction/curation work for text training but cannot replace source assets for our multimodal records. [Author documentation and exact split counts](https://github.com/allenai/pes2o)

Dolma is both a **dataset family** and a **curation toolkit**. The original dataset mixes web text, scientific publications, code, books and other authored text, and uses peS2o for its academic component. Reusing a suitable subset is an important acquisition route, not merely a source of general replay. For our research goal, in-domain selection and deduplication against directly acquired papers matter. The toolkit supplies processing machinery; installing it does not acquire the corpus. Dolma 3 is a later corpus family, so version and constituent source must be recorded. [Dolma paper, §8](https://arxiv.org/html/2402.00159) · [Dataset/toolkit distinction](https://github.com/allenai/dolma) · [Dolma 3 in the OLMo 3 report](https://arxiv.org/html/2512.13961v2)

The older phrase “institutional collections” meant organization-owned records such as internal laboratory measurements; it did not mean public curated datasets like Dolma. Those categories were too broad for this project. Here, source planning explicitly includes public reusable corpora as well as original publisher data.

**A broader, biology-focused model table**

This table compares disclosed source recipes for understanding the literature; it does not schedule model-training comparisons. Scratch pretraining, decoder CPT and encoder objectives are labeled separately.

| Foundation model | Stage | Actual biological source material | How the source becomes training data / relevant limitation |
|---|---|---|---|
| [BioGPT](https://academic.oup.com/bib/article/23/6/bbac409/6713511) | Decoder pretraining from scratch | 15M PubMed title/abstract records | Downloads PubMed records, removes entries lacking abstracts, then autoregressive training. These are not full paper PDFs. |
| [BioMedLM](https://arxiv.org/html/2403.18421v1) | Decoder pretraining from scratch | The Pile's PubMed abstract and PMC full-article subsets; 34.6B corpus tokens | Reuses assembled text. Its 300B consumed tokens include repeated passes; no new reproducible OCR workflow is specified in the model report. |
| [BioBERT](https://pmc.ncbi.nlm.nih.gov/articles/PMC7703786/) | Encoder continued pretraining | PubMed abstracts and PMC full text | Continues BERT's masked-language-model training on biomedical literature. Relevant precedent for domain adaptation, with a different objective from a decoder LLM. |
| [PubMedBERT](https://doi.org/10.1145/3458754) | Encoder pretraining from scratch | PubMed abstracts; additional PMC experiments | Builds an in-domain vocabulary. The paper tests abstracts versus adding full texts; this is a literature-representation model, not a vision model. |
| [BioLinkBERT](https://aclanthology.org/2022.acl-long.551/) | Encoder pretraining | PubMed documents and citation links | Uses linked-document contexts plus masked-token and document-relation objectives. A source-relationship recipe, not a PDF extraction tool. |
| [BioMedGPT-LM, PharMolix](https://arxiv.org/html/2308.09442v2) | Decoder CPT | 4.2M biomedical full texts selected from S2ORC, over 26B tokens | ID deduplication, removes reference citations/author information/chart data, then sentence-based text chunks. Molecule/protein alignment happens separately. |
| [BioT5+](https://arxiv.org/html/2402.17810v2) | T5-style biological pretraining, then task tuning | PMC text, PubMed/bioRxiv abstracts, PubChem, ZINC20, UniRef50 and paired descriptions | Mixes text with molecule/protein sequences and entity-linked text. Denoising and bidirectional translation objectives; not ordinary decoder CPT. |
| [NatureLM](https://arxiv.org/html/2502.07527v2) | Scientific decoder CPT for its larger models | Literature, database descriptions, small molecules, proteins, DNA/RNA and cross-domain pairs | Approximately 143B mixed tokens; BERN2 links literature mentions to molecular/protein representations. Structured sequence data is a major part of the corpus. Exact PDF-conversion settings are not disclosed. |
| [BioMatrix](https://arxiv.org/html/2606.22138v1) | Multimodal decoder CPT | Literature/web text, PubChem, UniProt/UniRef, PDB, interaction records and structure views | 304.4B mixed tokens. Combines experimental and predicted structures and includes generated descriptions; those are distinct provenance classes. A reproducible paper-PDF conversion recipe is not disclosed. |
| [Galactica](https://arxiv.org/pdf/2211.09085) | Scientific decoder pretraining from scratch | Scientific papers plus biological/chemical records such as UniProt and PubChem | Serializes scientific data alongside text and citation titles. A broad science model with disclosed biological material, rather than a biology-only model. |

OLMo 3 is a general model. Its report explicitly identifies biology among the topics in its Gemini reasoning-trace source, but does not give a separately measured natural biology-literature allocation. It replaced the previous peS2o component with a new academic PDF pool. We therefore do not present its whole PDF token count as a biological-paper count or its general mix as a biology-specific data recipe. [§3.4.2 and Appendix A.3](https://arxiv.org/html/2512.13961v2)

**Real material first**

Generated training material often reformats source documents, database facts, problems or simulations. It is derived material and should not displace the original evidence. Reformatting a publisher table or serializing a database entry is also different from asking a model to invent an explanation. Keep observed measurements, curated annotations, computed predictions and teacher-written text distinct.

For this project, the practical source order is:

1. Existing publisher XML/text, original figures, complete article tables and supplementary spreadsheets, with PDFs as retained originals and the fallback extraction source.
2. Relevant text records from reusable scientific corpora, such as S2ORC/peS2o or academic/domain subsets of a Dolma release. Preserve corpus IDs, source/version, document scope and deduplication identity. Already-cleaned text need not pass through OCR again.
3. Biological database exports that fit the model's intended abilities: protein sequences/annotations, molecule descriptions and structures, experimental structures and binding/assay data. Link records to literature using supplied identifiers where available. Distinguish predicted structures and automated annotations from experimental observations.
4. Only later, optional generated representations derived from retained source material. No teacher synthesis or synthetic training batch was run in the current implementation.

The first stage is executed for the three papers and the bounded supplement sample. Full external corpora and biological databases have not been downloaded by this change; the current work does not claim that they are already ingested or deduplicated. The existing 50-paper inputs and earlier OCR outputs remain intact on RustFS.

[Executed verification](../pmc_native_v4_citations_2026-10-15/verification.json) checked all 25 image hashes, preservation of all 218 main-article source cells, intact citation spans within the token bound, and every exported spreadsheet row against a second read of its original workbook. Ten regression tests passed. Twelve date-typed source cells are flagged and preserved in ISO form, with no inferred gene-name correction. These are source-consistency checks, not biological correctness scores or training comparisons.
