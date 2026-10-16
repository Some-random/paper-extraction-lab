# Processing recipe for biological continued pretraining

[Model and dataset comparison](README.md)

The goal is to turn papers, web pages and existing datasets into a useful biological training corpus. This is a proposed recipe: the references explain which techniques we are borrowing, and the biological adaptations explain how we would use them here.

**1. Extract useful content while preserving the original.**

- **Papers:** use publisher XML when available; use olmOCR 2 for PDFs. Keep sections in reading order, equations, tables, original figures, captions and the paragraphs referring to them. Preserve numbers, units and links to the source locations. **Example:** [Highly accurate protein structure prediction with AlphaFold](https://pmc.ncbi.nlm.nih.gov/articles/PMC8371605/): retain the methods and results, with each figure linked to its caption and discussion.
- **Web pages:** extract the main article, tables and relevant images from HTML. Separate navigation, advertisements and cookie notices from the actual content. **Example:** [Addgene's CRISPR guide](https://www.addgene.org/guides/crispr/): retain explanations of Cas enzymes and guide RNAs, diagrams and glossary entries; remove site menus and shopping links.
- **Existing datasets:** import records in their native structure. Keep descriptions alongside protein/DNA/RNA sequences, molecular representations and structures, with dataset versions and source IDs. **Example:** a UniProtKB/Swiss-Prot release, including [P69905, hemoglobin subunit alpha](https://rest.uniprot.org/uniprotkb/P69905.json): retain the amino-acid sequence, function, organism and accession. This is a database import even when retrieved through an API.

Keep raw files alongside extracted records. Extraction should recover the content, rather than replace a paper with an LLM summary. Figure pixels remain separate assets linked to their captions and surrounding text.

**References:** [olmOCR 2](https://arxiv.org/html/2510.19817v1) for PDF extraction; [S2ORC](https://aclanthology.org/2020.acl-main.447/) for structured papers and citation/figure/table links; [FineWeb](https://arxiv.org/html/2406.17557v1#S3.SS2) for extracting useful text from raw HTML. Retaining the original assets and preferring available XML are our source-preservation choices.

**2. Use consistent metadata, meaningful boundaries and readable citations.**

Keep **source, dataset/version, document ID, topic, modality and original location** as metadata on every record. These tags let us filter, mix and count the corpus. They do not all need to appear in the text the model reads.

In training content, preserve section boundaries and clearly mark where a protein sequence, molecule or other representation begins and ends. The exact delimiters must fit the chosen model and tokenizer; adding reserved tokens requires corresponding tokenizer and embedding changes.

For papers, replace opaque citation markers such as `[12]` with the **cited title plus first author/et al.** when the bibliography resolves them. Keep the original marker and full bibliography in metadata. Leave unresolved citations identifiable instead of inventing a title. This makes a passage more interpretable when it is separated from its bibliography.

**References:** [Galactica](https://arxiv.org/html/2211.09085v1#S3.SS1.SSS2) compared title-based citation identifiers with opaque IDs; [NatureLM](https://arxiv.org/html/2502.07527v2#S2.SS1) uses explicit boundaries for scientific representations. We use title-plus-first-author rendering for this corpus.

**3. Detect broken records and boilerplate with explicit checks.**

- **Broken extraction:** flag empty output, failed pages, abnormal character corruption, repeated OCR loops, or missing content visible in the original. Compare sampled text, numbers and table cells with the source. Retry extraction or exclude the damaged portion while retaining the original and the reason.
- **Boilerplate:** identify recurring navigation, cookie notices, publisher headers and footers using HTML structure, page position and repeated text. Remove those spans from training content.
- **Valid technical material:** equations, dense tables and biological sequences need their own checks. Symbol-heavy text is not automatically broken. Validate sequence alphabets, molecular syntax and table structure separately.

**References:** [Dolma](https://arxiv.org/html/2402.00159v1#S3.SS1) supplies explicit filtering and repetition checks; [olmOCR 2](https://arxiv.org/html/2510.19817v1) supplies source-based extraction tests. We adapt the rules to biological content, including separate handling of tables and sequences.

**4. Deduplicate across all three acquisition routes.**

First match document identities, such as DOI and source IDs. Then compare exact content hashes and near-duplicate text to find mirrors, repeated crawls and papers imported through another dataset. Keep the most complete reliable copy, while preserving its alternative source locations.

Use modality-specific identities for biological records. Similar proteins are not automatically duplicates, and a shared methods paragraph does not make two whole papers identical. Preserve meaningful sequence variants and publication-version differences.

**References:** [Dolma](https://arxiv.org/html/2402.00159v1#S3.SS1) for document- and paragraph-level deduplication. Cross-source identity matching and preservation of biological variants adapt these techniques to this corpus.

**5. Build a scorer whose labels have a clear meaning.**

Separate **biology relevance** from **information value**. Relevance asks whether a passage concerns the research biology we want. Information value asks whether it contains useful methods, results, mechanisms or explanations, with enough context to understand them. Neither score establishes that the science is correct.

Start with a representative sample from all three sources. A capable LLM can label it through prompting, without new training. Use those labels to train a cheaper scorer, checking its predictions on a held-out set of teacher-labeled examples. Compare it with direct LLM scoring before choosing the large-scale approach.

A small human audit can check whether the labels mean what we intended, especially for technical methods, captions and borderline topics. This is an additional check we can use for biology, not a requirement of the FineWeb-Edu recipe. Store a short supporting passage or source offset so reviewers can inspect a decision. **That evidence is an audit trail, not an extra score.** Whether the filter actually improves learning is tested in stage 6.

**References:** [FineWeb-Edu, §4](https://arxiv.org/html/2406.17557v1#S4) used Llama-3-70B-Instruct to label 460,000 examples, with 410,000 for scorer training and 50,000 for validation; both sets used model-generated labels. [DCLM, §4.4 and Appendix M](https://arxiv.org/html/2406.11794v3) trained filters using labels derived from selected reference corpora versus web samples. It separately collected three human judgments per document for 499 documents from 16 annotators. That study found that agreement with human judgments did not reliably predict downstream training performance.

**6. Test the recipe, choose the mixture and produce the final corpus.**

Keep records tagged by **source** (papers, web or imported datasets), **topic** (for example, genomics or cell biology) and **modality** (text, protein sequence or structure). This lets us change how much of each kind the model sees and identify where a gain comes from.

Run experiments in stages: compare candidate sources; compare filtering choices while holding the mixture fixed; then compare mixing ratios with the selected filters. Keep the starting checkpoint, tokenizer, optimizer settings and total training-token budget the same within each comparison. Test the combined recipe after selecting the individual components.

**Example: a text-CPT mixing experiment.** These are illustrative budgets, not measured corpus sizes or a selected training budget. Existing-dataset text could come from a biological subset of peS2o; sequence records would be tested as a separate modality component.

| Trial | Paper text | Web text | Existing-dataset text | General-text replay | Total |
|---|---:|---:|---:|---:|---:|
| A: paper-heavy baseline | 600M | 100M | 100M | 200M | 1B |
| B: more web text | 400M | 300M | 100M | 200M | 1B |
| C: more imported text | 400M | 100M | 300M | 200M | 1B |

Trial B asks whether replacing 200M paper tokens with web tokens helps; C asks the same about imported text. Evaluate all three on the same biological development tasks, and check whether general capabilities deteriorate. Repeat promising comparisons across seeds, then choose the mixture with the best supported tradeoff. Keep a separate final test set untouched during selection.

Use the same logic for filtering: for example, compare retaining all eligible biological text with retaining the top 80% or top 50% by a candidate score, while holding the source mixture and training budget fixed. Record any repeated sampling so a smaller retained pool is not mistaken for more unique data.

At the end of this stage, fix the recipe and package the corpus. Report retained tokens and training exposure separately for **online papers, web URLs and existing datasets**, plus modality breakdowns over the same records. Keep general-text replay separate. These counts accompany the finalized corpus.

**References:** [OLMo 3](https://arxiv.org/html/2512.13961v2#S3.SS4.SSS4) for source/topic mixing, quality-aware sampling and token budgets; [OpenThoughts3](https://arxiv.org/html/2506.04178v2#S4) for its staged experiments over source selection, mixing, filtering, deduplication, answer sampling and teacher selection. We take its approach of testing components, selecting useful choices and evaluating their combined recipe.
