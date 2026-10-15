**What foundation models do with paper figures**

A caption is normally written by the paper's authors. Recovering it from XML is extraction. Asking a VLM to explain the image creates a new interpretation. These should have different provenance fields.

| Published recipe | Pixels used in training? | Source captions / generated material |
|---|---|---|
| [BioGPT](https://arxiv.org/pdf/2210.10341) | No | Its pretraining source is titles and abstracts; it does not ingest the full paper's figures |
| [BioMedGPT-LM, PharMolix](https://arxiv.org/html/2308.09442v2) | No paper-image branch in the described CPT | Removes chart data from its S2ORC literature input. Subsequent molecule/protein encoders are not figure-image encoders |
| [MEDITRON](https://arxiv.org/html/2311.16079v1), Appendix B.2 | No | Discards figure pixels and table bodies; **retains captions** with figure/table tags. Inline figure/table references include a caption fragment truncated to 12 words. This is source-caption processing, not a VLM-generated caption |
| [peS2o](https://github.com/allenai/pes2o) | No | Full-text cleaning removes figures, tables and references. A cleaned text corpus cannot restore the original images |
| [NatureLM](https://arxiv.org/html/2502.07527v2) / [BioMatrix](https://arxiv.org/pdf/2606.22138v1) | Their disclosed biological modalities are sequences / structures / text | “Multimodal” here does not establish paper-figure training. Molecule/protein “captioning” can mean generating a biological description from a molecular/protein representation |
| [BiomedCLIP](https://arxiv.org/html/2303.00915) | Yes | Pairs original PMC figures with author captions for contrastive training; not a requirement to recaption them with a teacher VLM |
| [LLaVA-Med](https://arxiv.org/html/2306.00890) | Yes | First aligns image features to original captions. Later GPT-4 conversations are generated from caption/context text and kept as instruction data; the original method does not require GPT-4 to inspect the pixels |
| [PMC-InterCPT](https://arxiv.org/html/2606.01049v2) | Yes | Recovers missing captions from XML and interleaves figures with explicitly referring article passages. Text classifiers filter quality/relevance; the method explicitly prefers source-caption recovery to replacement generation |

For some older text-only reports, exact caption-retention settings are not documented. I have not inferred that all retained captions, or that all removed them. Likewise, running a page-OCR VLM does not itself establish that the model read a multi-panel experiment correctly.

**Recommended representation for our biology corpus**

1. Retain the original whole-figure image, hash, article/version/license identifiers, figure ID and **full author caption**. Preserve panel labels and original resolution. A caption alone often omits details in the image.
2. Retain the Results/Methods paragraphs that explicitly cite that figure and their positions in the article. Keep their ordering and boundaries. Do not join distant passages as if they were contiguous source prose. Shared paragraphs can reference several figures.
3. For text-only CPT, use source text, captions, linked context and source-derived table serialization. Image paths alone teach no visual content. Avoid pretending the caption contains every plotted value or microscopy observation.
4. For a VLM, provide the actual pixels with the source text. Choose whole-figure and optional panel crops using the eventual model's resolution/token budget; verify that small labels remain readable. Preserve the whole figure even if crops are added. Panel segmentation is a derived operation, not a replacement source.
5. If a later task needs extra interpretation, add a separate `generated_visual_description` with model/prompt/version, image identity and verification status. Distinguish observed labels/shapes from the paper's interpretation. Read numerical chart data from the source spreadsheet/native table when supplied; never fill unreadable values by guessing.

This is a recommendation for our project, not a claim that every published model follows it. It makes real material available for both text and vision training, and leaves optional synthetic augmentation auditable.

The [current executed extraction](../pmc_native_v4_citations_2026-10-15/README.md) already retains **25 original figures**, source captions, explicit context links and ordered records. It also exports full source tables and two supplementary workbooks. We have not run figure-semantic inference, panel segmentation, VLM training or teacher-generated recaptioning. The choice of VLM and any new GPU work remain future implementation decisions.
