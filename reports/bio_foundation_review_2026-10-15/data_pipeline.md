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

Run one duplicate index across papers, web pages and imported datasets. Comparing each source only with itself would miss a paper that also appears in a reused corpus.

- **Find identity matches:** normalize DOI, PMID and PMCID fields and group matching records. IDs identify candidate copies; compare their content and versions before discarding anything.
- **Find exact text copies:** create a comparison copy with standardized whitespace and line endings, preserving numbers, units, case and biological symbols. Compute its SHA-256 hash. Equal hashes identify equal comparison text even when filenames or URLs differ; preserve the original files.
- **Find near-copies:** split text into overlapping five-token windows. Use MinHash and locality-sensitive hashing to find candidate pairs without comparing every document with every other document. Then check the actual overlap: Jaccard similarity is shared windows divided by all distinct windows. Also check containment, which detects when a shorter record is mostly contained in a longer one.
- **Separate whole-document from passage duplication:** a mirrored article may be redundant as a whole; a repeated methods paragraph does not make two papers duplicates. Paragraph hashes and repeated-substring detection identify the shared spans. Any removal policy must preserve enough context to read the remaining document.
- **Choose a representative and retain provenance:** for verified copies of the same version, keep the extraction with the best completeness and fidelity. Record all source locations, overlap measurements and the keep/remove decision. Retain revisions with changed results as linked versions.

For example, a publisher PDF, its PMC XML and a compatible copy imported through peS2o can become one training text with three recorded origins. A newer revision with changed measurements remains distinct. For proteins and molecules, use accession/version and representation-specific checks; an identical sequence with different useful annotations is not automatically redundant.

Set overlap thresholds using reviewed duplicate and non-duplicate examples, including revised papers and shared protocols. Test aggressive versus conservative deduplication in stage 6 rather than treating one similarity threshold as universally correct.

**References:** [Dolma](https://arxiv.org/html/2402.00159v1#S3.SS1) for document/paragraph deduplication; [DCLM, Appendix K](https://arxiv.org/html/2406.11794v3) for comparisons of MinHash, suffix arrays and Bloom-filter approaches; [OLMo 3](https://arxiv.org/html/2512.13961v2#S3.SS4.SSS1) for a concrete exact-hash, MinHash/Jaccard and repeated-substring pipeline. The identity checks, containment checks and version-preservation policy adapt these techniques to this corpus.

**5. Build a scorer whose labels have a clear meaning.**

Separate **biology relevance** from **information value**. Relevance asks whether a passage concerns the research biology we want. Information value asks whether it contains useful methods, results, mechanisms or explanations, with enough context to understand them. Neither score establishes that the science is correct.

Start with a representative sample from all three sources. A capable LLM can label it through prompting, without new training. Use those labels to train a cheaper scorer, checking its predictions on a held-out set of teacher-labeled examples. Compare it with direct LLM scoring before choosing the large-scale approach.

A new manually labeled training corpus is not required to produce these scores. That does not establish that human review is unnecessary. For this biological corpus, use targeted expert checks of extracted numbers, duplicate decisions and scorer labels, especially methods, captions and borderline topics, before fixing the processing rules. This is our proposed validation step, not a claim about what FineWeb-Edu required. Store a short supporting passage or source offset so reviewers can inspect a decision. **That evidence is an audit trail, not an extra score.** Whether the filter actually improves learning is tested in stage 6.

**References:** [FineWeb-Edu, §4](https://arxiv.org/html/2406.17557v1#S4) used model-generated labels for both scorer training and validation; validation therefore measured agreement with its teacher. [DCLM, §4.4 and Appendix M](https://arxiv.org/html/2406.11794v3) used reference-corpus versus web-sample labels for its main classifiers and separately studied human judgments on 499 documents. Human agreement did not reliably predict training gains; this does not establish that human checks of biological correctness or extraction fidelity are dispensable.

**6. Test the recipe, choose the mixture and produce the final corpus.**

The research precedent is a systematic search over data recipes, with smaller experiments used to select candidates for larger validation runs:

| Study | What its experiments actually did |
|---|---|
| **DCLM** | Reported 416 baseline experiments across data-processing choices and compute scales. A fixed recipe at each scale made dataset comparisons meaningful; one scale used a 1.4B-parameter model and 28.8B training tokens. |
| **OpenThoughts3** | Ran over 1,000 controlled experiments. Its main comparisons generated 31,600 examples per configuration and fine-tuned the same starting model. It ranked sources, tested mixtures of the top 1, 2, 4, 8 and 16 sources, and compared filtering, deduplication, answer sampling and teachers. |
| **OLMo 3** | Sampled many mixture weights and trained 30M-parameter proxy models for 3B tokens each. It fitted models predicting task performance from mixture weights, then searched for good weights subject to available-data and repetition constraints. |

For this corpus, apply that experimental structure as follows:

- **Define meaningful source pools.** Keep PMC papers, other paper collections, individual web collections and reused datasets distinguishable. Subdivide by biological topic, modality and quality tier where useful. The three acquisition routes remain the reporting categories; they are too coarse to be the only units of mixture optimization.
- **Screen sources and processing recipes.** Compare individual source contributions, source subsets, filtering methods and deduplication settings in matched smaller runs. Include an unchanged baseline and compare whole pipelines as well as individual components, because a filter's effect can depend on the source and deduplication policy.
- **Search mixture weights.** Use the source-screening results to select candidate combinations, then test multiple allocations across their source/topic/quality pools. Include source-removal tests to measure marginal contribution. For a larger search, use OLMo-style proxy runs and a fitted predictor to propose weights, then verify those proposals in actual training runs. Cap repeated sampling and retain explicit general-text replay weights.
- **Confirm on the intended checkpoint.** Re-run the strongest recipes with the target CPT model and budget, check more than one seed, and report per-task results and uncertainty. Include biological development tasks, general-capability checks and held-out language-modeling loss. Keep final test data and their near-duplicates out of both recipe selection and training.

Hold the model, tokenizer, optimizer settings and training budget fixed within each matched comparison. Track the actual sampled tokens, repeated exposure and retained corpus size so a gain cannot be explained simply by one run seeing more data. Smaller runs screen the search; target-checkpoint confirmation determines the final choice.

At the end of this stage, fix the recipe and package the corpus. Report retained tokens and training exposure separately for **online papers, web URLs and existing datasets**, plus modality breakdowns over the same records. Keep general-text replay separate. These counts accompany the finalized corpus.

**References:** [DCLM, §§3–4](https://arxiv.org/html/2406.11794v3) for controlled comparisons across scales; [OpenThoughts3, §4](https://arxiv.org/html/2506.04178v2#S4) for staged configuration searches; [OLMo 3, §3.4.4](https://arxiv.org/html/2512.13961v2#S3.SS4.SSS4) for proxy-model mixture optimization. The corpus-specific search above combines these techniques; it is not a reproduction of any one paper's full experiment schedule.
