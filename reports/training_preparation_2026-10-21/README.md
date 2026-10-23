# Biological data preparation and training sources

Corpus counts observed **2026-10-23 18:58 UTC** (11:58 PDT); source-link documentation and the completed reasoning audit were updated for this publication. Counts below are measured snapshots; running workers keep advancing. All sizes are decimal GB and token amounts are billions. Original inputs and earlier reports are preserved.

**Completed:** the selected TheBioCollection free-text release download and census; the corrected 166,027-paper local view; one bounded exact-deduplication pass; the 10,000-example sequence-MCQ dataset. **Still running:** broader PMC acquisition/parsing, five FineWeb-Edu classifier workers and near-copy candidate retrieval. Full-corpus filtering and near-copy removal are not complete.

## Immediate 10,000-example SFT work is separate

The current [public training dataset](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k) contains **10,000 generated QA examples, 1,910 distinct full protein sequences and 25 task types**. It uses source-bound **UniProt release 2026_03** annotations/references; GPT-6 Luna medium authored and separately judged the examples. Native Qwen targets include the visible worked explanation and a final A/B/C/D letter.

The current SFT does **not** consume all PMC text, the whole TheBioCollection free-text census, or the FineWeb-Edu retained corpus. Those larger collections are background preparation for later experiments. The current QA evidence is UniProt annotation/reference context; a reference link alone does not mean a full paper was read or that a specific claim was experimentally established there. The separate GPT-6 Luna medium reasoning-strength audit is complete: 521 of 10,000 examples were rated as strongly grounded in sequence evidence, 686 as partial links, 8,699 as annotation restatement or assumed identity, and 30 as inconsistent; two were uncertain and 62 ungraded. These are model judgments, not expert-human ground truth. [Current public training dataset](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k) · [Published attribution](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k/blob/main/attribution.jsonl).

**Source companion published October23:** [follow a real sequence → annotation → original paper](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k/blob/main/SOURCE_GUIDE.md), or [search the flat link table](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k/blob/main/provenance/sequence_paper_links.csv). All 10,000 sequence/annotation links were checked; 4,210 examples have selected-annotation PMIDs, 5,763 have other record-bibliography PMIDs only, and 27 have none. All 3,226 cited-paper records were checked: **261 original papers** with verified identifiers and permissive licenses are included as XML and readable text; the other 2,965 retain source links and explicit availability reasons. The papers were attached for traceability after generation: all 10,000 teacher packets used UniProt context and **zero full-paper text blocks**. The default training split and its bytes remain unchanged. Published source snapshot: `181c177733b15feac8abcafa6da652bf83dfbe4f`.

## Inspect the training examples and their papers

[Read three actual training examples alongside their source papers](PAPER_LINK_EXAMPLES.md). Each case includes the exact question, choices, selected answer, UniProt identity, source annotation, and a passage or figure in the linked original paper. These are training examples, not LiveProteinBench evaluation questions.

The source trail is **exact training sequence → frozen UniProt accession and sequence version → selected annotation or its enclosing evidence-bearing annotation → recorded PMID/DOI → matching original paper**. The links come from recorded source identifiers. Some leaf properties, such as an EC number, inherit citation evidence from their enclosing reaction annotation; the stored field pointers preserve that distinction.

The public [flat link table](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k/blob/main/provenance/sequence_paper_links.csv) explicitly labels `selected_annotation_citation` and `record_bibliography_only`. A record-wide bibliography reference is not evidence assigned to the particular training question. A citation may describe a specific experiment, a broad study, or a genome, rather than a paper dedicated to one protein. An annotation citation does not independently verify every sentence of a generated explanation.

The current 10,000 examples were generated from UniProt evidence packets. Full papers were attached afterward for provenance; the teacher did not receive full-paper text. The three linked examples have additionally been checked against original article text for this report. This does not represent a full-paper review of all 10,000 examples.

## Completed local paper-text view

**Main completed paper-text total: 6.308111 GB / 1.706050 billion measured tokens; 166,027/166,027 primary papers, zero remaining in this frozen view.**

The original census `243657` processed 165,638 papers: 50,591 reused native texts and 115,047 newly processed legacy texts. A later closed increment added 389 native papers. The correction job **`246417` completed** all 50,980 native checks, reusing 115,047 legacy primaries; 126 native text outputs changed, 50,854 were unchanged, and zero native checks failed or remain unresolved. It preserves preformatted content and one preferred primary per PMCID, with **no old biology/clinical keyword exclusion**. Correction artifacts: **0.640361 GB**; downloads during correction: **0 GB**. Stop reason: none.

This completed view is frozen. The live PMC acquisition below overlaps it through native upgrades, so its counts are **not added** to this total. Exact/near-copy outputs created from older derivatives require a source-bound refresh before they represent the corrected view. Completed correction and source binding (local artifact: `experiments/native_paper_preformat_reprocessing_2026-10-22/summary.json`).

## Broader PMC download and parsing

**Job `247554`: RUNNING**, using the versioned batched/durable XML downloader and parser. Its official **2026-10-21T01-00Z** snapshot inventory is complete: **9,273,077 distinct PMCIDs / 9,433,710 versions**. The target is one available preferred native XML per PMCID, retaining version/license metadata; PDFs, media and supplement binaries are outside this download phase. This is broader paper coverage, not a claim that every paper is biological or clinically excluded.

At the recorded checkpoint it has acquired **520,077 XML papers** (58.580690 GB of XML), including **518,927 new distinct PMCIDs** and **1,150 upgrades of known text**; **1,895 matching native XMLs were reused**. It has parsed **121,553 records** into **5.456156 GB / 1.397525 billion measured tokens**, a **partial, overlapping increment**.

Current pending-acquisition status: **8,750,990 records**. Downloaded/pending-parse backlog: **398,517 records**. Four sources are in `pending_source_error` and one in `pending_retry`; these are unresolved, not successful parses. No stop reason is recorded. Network response bodies: **at least 59.283963 GB** (accounting upper bound **59.745409 GB**); compact state reports current phase artifacts **28.651812 GB**. These are different measures and are not summed. Live compact state (local artifact: `experiments/pmc_full_inventory_acquisition_2026-10-21/state.json`) · Batched-resume handoff (local artifact: `experiments/pmc_batched_resume_2026-10-22/handoff/`).

## TheBioCollection free-text release

**Download `245955`: COMPLETED. Census `246214`: COMPLETED.** Both stopped normally. The exact source is **`trillionlabs/TheBioCollection`**, revision **`df09ee34ae7f9f00cc1290862f83fdb542f2ea35`**, selected files `data/free_text_stream/free_text_stream_part_000001.jsonl.zst` through `...000032.jsonl.zst`.

All **32/32 selected shards** have size and SHA256 verification: **15.931043 GB compressed**. Four shards were reused, 28 newly downloaded (**13.940080 GB**). Census counted **37,227,086 records**, **92.610788 GB of record text / 36.978441 billion measured tokens**, with no remaining shard. These totals include biological annotation prose, sequences and molecular representations. Literal protein-tagged content contributes **2.771413 GB / 1.517683 billion tokens**; the split is based on source tags, not semantic validation or distinct protein counts.

This completes **that pinned free_text_stream snapshot**, not every BioCollection configuration, later release or all biological sequence databases. The separate instruction stream is not in this census; it was sampled separately for earlier supervised pilots. Whole-release exact uniqueness, sequence deduplication and production-quality acceptance have not been established; `production_released=false`. Verified files and original paths (local artifact: `experiments/biocollection_acquisition_2026-10-21/verified_manifest.json`) · Final census (local artifact: `experiments/biocollection_processing_2026-10-21/summary.json`).

## FineWeb-Edu filtering

The source is the existing **SmolLM FineWeb-Edu-Dedup** cache, pinned revision `3ba9d605774198c5868892d7a8deda78031a781f`: **234 Parquet shards / 190,168,005 source rows**. It is distinct from original FineWeb and FineFineWeb. Processing applies coarse recall, then pretrained BERT biology and NLI clinical classifiers over document windows. This is **classifier inference, not training**.

Five current workers **`247556`, `247557`, `247558`, `247559`, `247560` are RUNNING**, each on one RTX8000 in validated FP32 mode. They cover the exact disjoint remainder after the prior closed **15,823,208-row** prefix. So far they add **12,751,982 accounted source rows** and **701,651 provisional retained records**, measuring **2.512181 GB / 0.574269 billion tokens**.

Adding that live increment once to the closed prefix gives a **provisional running total** of **28,575,190/190,168,005 accounted source rows; 161,592,815 remain**. Provisional retained web text: **1,701,938 records / 5.809677 GB / 1.317970 billion measured tokens**. **1,899,000 accounted rows remain source-unknown**, so accounted does not mean successfully classified. This is not yet a completed canonical export, accepted biological corpus or production release. Current workers report no stop reason. Exact jobs and ownership (local artifact: `experiments/web_biology_full_continuation_2026-10-22/jobs.json`) · Five worker checkpoints (local artifact: `experiments/web_biology_full_continuation_2026-10-22/workers/`).

The original coarse-recall job **`244396` completed with `source_read_errors`**: 176,447,005 readable rows and 13,721,000 unknown rows. Its 110,895,015 candidates / 647.690455 GB are **recall candidates**, not semantically accepted biology. Candidate tokenizer totals were **not measured**. A separate repair download **`247562` completed**, preserving the originals and verifying **34/34 files / 80.259587 GB compressed**. Repair text/token sizes are **not measured**; these recovered inputs still require a versioned filtering/reconciliation pass. Repair receipt (local artifact: `experiments/web_biology_source_repair_2026-10-22/download_summary_v1.json`).

The standalone BERT inference job **`244442` completed**, but its **`filter_quality_gate` failed**: `no_precision_qualified_rule`, zero selected precision-qualified rules, and calibration token-recall gate false; **`production_released=false`**. The separate offline BERT **`244442` + NLI clinical `244390`** combination is **`pilot_audit_passed`**, with **60 documents** audited: **91.67% document precision** (document-only Wilson95 **81.93–96.39%**) and **94.34% token precision**. Joint stop reason: none; full-corpus filtering complete: false; production released: false. This joint pilot does not replace the failed standalone gate. A later independent diagnostic of 50 retained texts found **86.00% document precision** (document-only Wilson95 **73.81–93.05%**) and **93.75% token precision**. These are assistant reviews, not expert-human ground truth. Quality evidence (local artifact: `experiments/corpus_review_2026-10-21/accepted_diagnostic_summary.json`).

## Exact duplicates and near copies

**Exact-deduplication job `246353` completed** the frozen combined snapshot: **1,166,314 input records → 1,166,308 representatives**, omitting six redundant paper copies from the keep view and deleting no source. It covers **166,027 older paper derivatives plus 1,000,287 earlier provisional web records**. This bounded pass excludes later PMC/FineWeb increments and precedes the completed native-paper correction. It does not establish whole-corpus uniqueness. Exact manifest summary (local artifact: `experiments/canonical_exact_followon_2026-10-22/exact_summary.json`).

**Near-copy job `246237`: RUNNING, candidate retrieval.** Its still older frozen snapshot has **750,715 records** (165,638 papers + 585,077 web records). Index construction is complete; **72,858 candidate pairs** are recorded so far, with **0 proposed containment edges**. Retrieval and verification are incomplete; **near-copy removal is not done**, and no automatic source omissions occurred. This pass searches finite shared-span/containment evidence, not every possible paraphrase or edited near-copy. Live near-copy state (local artifact: `experiments/full_corpus_near_continuation_2026-10-21/state.json`).

## What remains

1. Finish broader PMC acquisition and its growing parse backlog; preserve explicit unreadable/changed-source cases.
2. Finish the disjoint FineWeb-Edu classifier ranges, then separately process/reconcile recovered corrupt source files and validate a fresh accepted sample.
3. Refresh exact hashes against corrected/current paper and web snapshots; finish candidate verification and review any proposed near-copy omissions.
4. Create source/family-grouped splits and benchmark-overlap checks before a broader corpus experiment; pin the actual selected mixture and measured tokenizer totals. Completed download/census does not equal a ready training corpus.
5. Keep the immediate 10,000-QA SFT and reasoning audit separate from these bulk-corpus steps. No claim of improved model quality is made here.

No defensible unique grand total is produced by adding PMC, BioCollection and web token counts: these sources and successive snapshots can overlap. Shared free space at the PMC observation was **618.197418 GB**, not reserved capacity.

The corpus observation above is preserved locally as `reports/training_preparation_2026-10-21/observation_20261023T185803Z.json`; its SHA256 is `4c2ef6daf3d88415b95d07b9d332f32dcfef73b4ee5808ac1f3689743deb48a3`. Local artifact paths identify retained cluster evidence and are not public download links. This GitHub publication changes documentation only; training data, jobs, and budgets are unchanged. Scheduled two-hour updates remain off.
