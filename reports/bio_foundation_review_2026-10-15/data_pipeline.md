# Processing recipe for biological continued pretraining

[Model and dataset comparison](README.md)

The goal is to turn papers, web pages and existing datasets into a useful biological training corpus. This is a proposed recipe: the references explain which techniques we are borrowing, and the biological adaptations explain how we would use them here.

**1. Extract useful content while preserving the original.**

- **Papers:** use publisher XML when available; use olmOCR 2 for PDFs. Keep sections in reading order, equations, tables, original figures, captions and the paragraphs referring to them. Preserve numbers, units and links to the source locations.
- **Web pages:** extract the main article, tables and relevant images from HTML. Separate navigation, advertisements and cookie notices from the actual content.
- **Existing datasets:** import records in their native structure. Keep descriptions alongside protein/DNA/RNA sequences, molecular representations and structures, with dataset versions and source IDs.

Keep raw files alongside extracted records. Extraction should recover the content, rather than replace a paper with an LLM summary. Figure pixels remain separate assets linked to their captions and surrounding text.

Method basis: [olmOCR 2](https://arxiv.org/html/2510.19817v1) for PDF extraction; [S2ORC](https://aclanthology.org/2020.acl-main.447/) for structured papers and citation/figure/table links; [FineWeb](https://arxiv.org/html/2406.17557v1#S3.SS2) for extracting useful text from raw HTML. Retaining the original assets and preferring available XML are our source-preservation choices.

**2. Use consistent metadata, meaningful boundaries and readable citations.**

Keep **source, dataset/version, document ID, topic, modality and original location** as metadata on every record. These tags let us filter, mix and count the corpus. They do not all need to appear in the text the model reads.

In training content, preserve section boundaries and clearly mark where a protein sequence, molecule or other representation begins and ends. The exact delimiters must fit the chosen model and tokenizer; adding reserved tokens requires corresponding tokenizer and embedding changes.

For papers, replace opaque citation markers such as `[12]` with the **cited title plus first author/et al.** when the bibliography resolves them. Keep the original marker and full bibliography in metadata. Leave unresolved citations identifiable instead of inventing a title. This makes a passage more interpretable when it is separated from its bibliography.

Method basis: [Galactica](https://arxiv.org/html/2211.09085v1#S3.SS1.SSS2) compared title-based citation identifiers with opaque IDs; [NatureLM](https://arxiv.org/html/2502.07527v2#S2.SS1) uses explicit boundaries for scientific representations. Title-plus-first-author rendering is our chosen adaptation, not a proven optimal CPT format.

**3. Detect broken records and boilerplate with explicit checks.**

- **Broken extraction:** flag empty output, failed pages, abnormal character corruption, repeated OCR loops, or missing content visible in the original. Compare sampled text, numbers and table cells with the source. Retry extraction or exclude the damaged portion while retaining the original and the reason.
- **Boilerplate:** identify recurring navigation, cookie notices, publisher headers and footers using HTML structure, page position and repeated text. Remove those spans from training content.
- **Valid technical material:** equations, dense tables and biological sequences need their own checks. Symbol-heavy text is not automatically broken. Validate sequence alphabets, molecular syntax and table structure separately.

Method basis: [Dolma](https://arxiv.org/html/2402.00159v1#S3.SS1) supplies explicit filtering and repetition checks; olmOCR 2 supplies source-based extraction tests. We would adapt the rules to biological content rather than copy general-web thresholds unchanged.

**4. Deduplicate across all three acquisition routes.**

First match document identities, such as DOI and source IDs. Then compare exact content hashes and near-duplicate text to find mirrors, repeated crawls and papers imported through another dataset. Keep the most complete reliable copy, while preserving its alternative source locations.

Use modality-specific identities for biological records. Similar proteins are not automatically duplicates, and a shared methods paragraph does not make two whole papers identical. Preserve meaningful sequence variants and publication-version differences.

Method basis: Dolma's document- and paragraph-level deduplication. The cross-source identity matching and biological exceptions are adaptations for this corpus.

**5. Build a scorer whose labels have a clear meaning.**

Separate **biology relevance** from **information value**. Relevance asks whether a passage concerns the research biology we want. Information value asks whether it contains useful methods, results, mechanisms or explanations, with enough context to understand them. Neither score establishes that the science is correct.

Start with a representative sample from all three sources. A capable LLM can label it through prompting, without new training. Have humans review examples and disagreements, then hold out an independently reviewed set to measure errors. Include difficult cases such as technical methods, short captions and material near the biology/clinical boundary.

For larger-scale scoring, compare direct LLM labeling with a smaller model trained on the reviewed labels. Select the scorer by measured accuracy and cost; do not prescribe an architecture in advance. Store a short supporting passage or source offset so reviewers can inspect a decision. **That evidence is an audit trail, not an extra score or automatically generated training content.**

Method basis: [FineWeb-Edu](https://arxiv.org/html/2406.17557v1#S4) demonstrates LLM annotations followed by a trained scorer. Its school-level educational rubric would need replacement for research biology. [DCLM](https://arxiv.org/html/2406.11794v3) compares filtering approaches through downstream training results, rather than assuming an LLM judge is best.

**6. Choose filters and mixing ratios through controlled experiments.**

Group the retained data by source, biological topic and modality. Compare candidate source combinations, filtering thresholds and token sampling ratios. Keep the starting checkpoint, training-token budget and other training settings fixed so that differences can be attributed to the data choice. Measure biological capabilities on development tasks and monitor general-capability retention; reserve final tests until the recipe is fixed.

[OLMo 3](https://arxiv.org/html/2512.13961v2#S3.SS4.SSS4) provides the main precedent for controlled source/topic mixing and quality-aware sampling. [OpenThoughts3](https://arxiv.org/html/2506.04178v2#S4) adds a useful experimental pattern across source selection, filtering and teacher choice: test each ingredient, retain improvements, and check their combination. Its results also show that more sources or more filtering need not help.

OpenThoughts3 studies **reasoning supervised fine-tuning (SFT)**. We can borrow that experimental discipline across our pipeline, but its question-difficulty filters, multiple generated answers and answer-filtering results do not establish what works for raw-paper CPT. Those techniques belong in a separately evaluated reasoning-data recipe if we use them.

**7. Freeze the recipe, package the records and count the tokens.**

Once the comparisons support a recipe, fix the extraction settings, filters, scorer, source weights and training tokenizer. Package records with clear document boundaries and preserved context.

Report retained tokens separately for **online papers, web URLs and existing datasets**, assigning each retained record to one acquisition route. Report modality breakdowns over that same corpus, without adding them again. Keep general-text replay separate from biological data. Also record tokens actually consumed during training, since repeating a record increases training exposure without increasing the unique retained corpus.

This accounting follows the distinction between available data pools and sampled training mixtures in OLMo 3. It makes the final question concrete: how much usable biological data comes from each source, and how much of it does the model actually see?
