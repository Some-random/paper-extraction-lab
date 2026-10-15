**What foundation models do with paper figures**

A caption is normally written by the paper's authors. Recovering it from XML is extraction. Asking a VLM to explain the image creates a new interpretation. These should have different provenance fields.

Published per-model figure policies are now attached to each entry in the [shared catalog](README.md).

For some older text-only reports, exact caption-retention settings are not documented. I have not inferred that all retained captions, or that all removed them. Likewise, running a page-OCR VLM does not itself establish that the model read a multi-panel experiment correctly.

**Recommended representation for our biology corpus**

1. Retain the original whole-figure image, hash, article/version/license identifiers, figure ID and **full author caption**. Preserve panel labels and original resolution. A caption alone often omits details in the image.
2. Retain the Results/Methods paragraphs that explicitly cite that figure and their positions in the article. Keep their ordering and boundaries. Do not join distant passages as if they were contiguous source prose. Shared paragraphs can reference several figures.
3. For text-only CPT, use source text, captions, linked context and source-derived table serialization. Image paths alone teach no visual content. Avoid pretending the caption contains every plotted value or microscopy observation.
4. For a VLM, provide the actual pixels with the source text. Choose whole-figure and optional panel crops using the eventual model's resolution/token budget; verify that small labels remain readable. Preserve the whole figure even if crops are added. Panel segmentation is a derived operation, not a replacement source.
5. If a later task needs extra interpretation, add a separate `generated_visual_description` with model/prompt/version, image identity and verification status. Distinguish observed labels/shapes from the paper's interpretation. Read numerical chart data from the source spreadsheet/native table when supplied; never fill unreadable values by guessing.

This is a recommendation for our project, not a claim that every published model follows it. It makes real material available for both text and vision training, and leaves optional synthetic augmentation auditable.

The [current executed extraction](../pmc_native_v4_citations_2026-10-15/README.md) already retains **25 original figures**, source captions, explicit context links and ordered records. It also exports full source tables and two supplementary workbooks. We have not run figure-semantic inference, panel segmentation, VLM training or teacher-generated recaptioning. The choice of VLM and any new GPU work remain future implementation decisions.
