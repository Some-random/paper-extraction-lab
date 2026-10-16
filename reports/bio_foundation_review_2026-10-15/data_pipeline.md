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

> [!IMPORTANT]
> **Human annotation: bulk labels can be automated; human review is part of our validation plan.**
>
> - **Training labels:** FineWeb-Edu generates them with an LLM. DCLM's main classifiers use labels derived from reference-corpus membership. Neither requires people to label the entire training pool.
> - **Published human study:** DCLM separately collected three judgments per document on 499 documents. This tests human agreement; it is separate from the main classifier-training labels.
> - **Our biological review:** have domain reviewers inspect samples of both retained and rejected text, incorrect scorer decisions, extracted numbers and suspicious duplicate merges. Record which material was reviewed and what errors were found.
> - **What establishes usefulness:** review checks the meaning and fidelity of the data; the controlled training experiments in stage 6 measure whether a filter improves the model.

Separate **biology relevance** from **information value**. Relevance asks whether a passage concerns the research biology we want. Information value asks whether it contains useful methods, results, mechanisms or explanations, with enough context to understand them. Neither score establishes that the science is correct.

Start with a representative sample from all three sources. A capable LLM can label it through prompting, without new training. Use those labels to train a cheaper scorer, checking its predictions on a held-out set of teacher-labeled examples. Compare it with direct LLM scoring before choosing the large-scale approach.

Store a short supporting passage or source offset with each decision so a reviewer can inspect it. **That evidence is an audit trail, not an extra score.** Keep agreement with teacher labels, human-review errors and downstream training gains as separate measurements.

**References:** [FineWeb-Edu, §4](https://arxiv.org/html/2406.17557v1#S4) used model-generated labels for both scorer training and validation; validation therefore measured agreement with its teacher. [DCLM, §4.4 and Appendix M](https://arxiv.org/html/2406.11794v3) used reference-corpus versus web-sample labels for its main classifiers and separately studied human judgments on 499 documents. Human agreement did not reliably predict training gains; this does not establish that human checks of biological correctness or extraction fidelity are dispensable.

**6. Test the recipe, choose the mixture and produce the final corpus.**

The studies below answer different parts of the mixing problem. Their experiment counts cover the reported research programs, not just mixture-weight trials.

**DCLM — compare processing recipes and test whether additional sources help.**

- **What changes:** extraction, deduplication, quality filters and source composition. Its 416 baseline experiments span several compute scales, with training settings fixed within each scale.
- **Actual mixing comparison:** train on filtered Common Crawl alone, then compare a mixture of 67% Common Crawl and 33% Wikipedia, books, Stack Exchange, arXiv and GitHub. Repeat this for several Common Crawl variants. Appendix L also applies the quality filter to the added sources.
- **How choices are judged:** downstream task scores. The added sources help some weaker web corpora but do not improve DCLM-baseline. This directly tests the value of adding those sources rather than assuming curated additions will help.

**OpenThoughts3 — rank sources, then compare combinations and later processing choices.**

- **Source screening:** test 27 code, 21 math and 14 science question sources. Main comparisons use 31,600 examples per configuration and fine-tune the same Qwen2.5-7B-Instruct starting model.
- **Actual mixing search:** rank sources from those experiments. For each domain, choose the top N sources, with N = 1, 2, 4, 8 or 16; sample 31,600/N questions from each. Total example count stays fixed, and sources within a candidate mixture have equal shares.
- **What follows:** carry the selected approach into experiments on filtering, deduplication, multiple answers and teachers. Selection uses the average across eight development benchmarks; separate benchmarks are reserved for final evaluation. The reported 1,000-plus experiments cover this wider pipeline.

**OLMo 3 — learn continuous mixture weights from proxy training runs.**

- **What receives weights:** source collections and topic partitions, including 24 web topics. Within-topic quality upsampling is handled separately from source/topic mixing.
- **Actual search:** sample many weight vectors around the natural data proportions. Train a 30M-parameter proxy model for 3B tokens on each mixture, then fit a regression for each task predicting loss from the weights.
- **How weights are chosen:** optimize predicted average task loss under constraints on available tokens and repeated passes. Its conditional mixing procedure preserves an existing mixture's internal proportions while testing added or changed components, allowing late-arriving PDF data to be incorporated without rebuilding the entire search.

**Marin / Datakit, September 2026 — jointly weight topic and quality buckets.**

- **What receives weights:** documents from different sources are grouped into 40 topics and five quality bands, making 200 buckets. Quality scores organize the pool rather than immediately discarding its lower-scoring portion; band thresholds depend on content type.
- **Actual search:** the report describes over 1,000 small proxy experiments, followed by regression from bucket weights to evaluation performance. Both proxy training budgets and bucket sizes are scaled so repeated exposure resembles the intended large run.
- **Validation:** compare the optimized mixture with token-proportional sampling across a ladder of larger models before the main run. The important transfer is the treatment of quality, topic and repetition as linked sampling decisions.

For this corpus, apply that experimental structure as follows:

- **Define meaningful source pools.** Keep PMC papers, other paper collections, individual web collections and reused datasets distinguishable. Following Marin's organization, retain topic and quality labels so content from different sources can contribute to the same biological bucket. Preserve source provenance for accounting. The three acquisition routes remain reporting categories rather than the only units receiving weights.
- **Screen sources and processing recipes.** Compare individual source contributions, source subsets, filtering methods and deduplication settings in matched smaller runs. Include an unchanged baseline and compare whole pipelines as well as individual components, because a filter's effect can depend on the source and deduplication policy.
- **Search mixture weights.** Use OpenThoughts3-style source screening to narrow candidate combinations. Compare those with a token-proportional baseline, then use OLMo/Marin-style proxy runs and a fitted predictor for a broader weight search. Track the number of passes through each bucket; a small high-quality bucket cannot supply an unlimited share without repetition. Retain explicit general-text replay weights.
- **Confirm on the intended checkpoint.** Re-run the strongest recipes with the target CPT model and budget, check more than one seed, and report per-task results and uncertainty. Include biological development tasks, general-capability checks and held-out language-modeling loss. Keep final test data and their near-duplicates out of both recipe selection and training.

Hold the model, tokenizer, optimizer settings and training budget fixed within each matched comparison. Track the actual sampled tokens, repeated exposure and retained corpus size so a gain cannot be explained simply by one run seeing more data. Smaller runs screen the search; target-checkpoint confirmation determines the final choice.

At the end of this stage, fix the recipe and package the corpus. Report retained tokens and training exposure separately for **online papers, web URLs and existing datasets**, plus modality breakdowns over the same records. Keep general-text replay separate. These counts accompany the finalized corpus.

**References:** [DCLM, §§3–4 and Appendix L](https://arxiv.org/html/2406.11794v3); [OpenThoughts3, §§4.1–4.6](https://arxiv.org/html/2506.04178v2#S4); [OLMo 3, §3.4.4](https://arxiv.org/html/2512.13961v2#S3.SS4.SSS4); [Marin / Datakit: Curating 25 Trillion Tokens for LLM Pretraining](https://openathena.ai/blog/marin-data-pipeline-overview/), published September 11, 2026. The corpus-specific search above combines these techniques; it is not a reproduction of any one study's full experiment schedule.
