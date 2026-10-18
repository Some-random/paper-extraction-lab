# Running the corpus census

[Measured counts](../reports/corpus_count_2026-10-17/README.md) · [Processing recipe](../reports/bio_foundation_review_2026-10-15/data_pipeline.md)

The census counts the actual text we read in one fixed tokenizer, keeping raw
tokens and tokens after exact deduplication separate. Literature extrapolations
remain separate from these measurements.

## Inputs and first run

The frozen [configuration](../config/corpus_count_2026-10-17.json) includes:

| Input | Frozen inventory | What is counted |
|:---|:---|:---|
| PMC biology papers | 454 existing papers plus a target of 5,000 new XML papers | Title, selected article blocks, captions/notes and source tables, once per paper. |
| FineFineWeb biology | 864 complete JSONL shards | Original text, retaining URLs, global IDs and source-reported token counts as provenance. |
| TheBioCollection free-text stream | 32 complete compressed shards | Original text, including annotations and explicitly tagged biological strings. Instructions are excluded. |

The remote inventories together contain **449,815,029,022 stored bytes** (about
419 GiB). This is an input-file size, not a token count. The first run has an
**8 GiB download reservation budget, 16 GiB artifact budget and 12-hour fixed
deadline**, with a 32 GiB free-space floor. It uses two allocated CPU cores, one
worker and zero GPUs. Restarting does not reset these limits.

The current run stores raw shards and its ledger under the project's ignored
experiment directory on shared scratch. The historical RustFS filesystem path
is unavailable in this environment; this run does not rely on it.

PMC is a selected collection, not a representative sample or a PMC-wide census.
The initial local selection has **10,609,606 candidate tokens across 454 papers**.
This corrects the first 12,677,035-token result: captions and tables already in
the parser's block stream had also been added from its visual views. The
canonical adapter now adds each source view once, with a regression check using
actual JATS parsing. Title/serialization boundaries can still make its total
differ from packed-chunk totals. Original inputs and superseded ledger rows
remain in `corrections/local_paper_caption_table_audit.json`; this correction
does not alter web/database counts.

The [paper-expansion plan](../config/corpus_count_pmc_expansion_2026-10-17.json)
adds broad PMC searches over four biological topic groups and five publication
year ranges. The searches have no journal restriction. Research articles,
reviews, methods articles and brief reports are eligible, with title/abstract
biology markers and source/body checks. Query subsets are a convenience
collection, not a representative sample of all biological literature.
Explicit clinical-care/trial/device titles are screened out. A few acquired
candidates identified during the initial audit remain preserved in raw counts
with `excluded_scope` status; they do not count toward the selected-paper
target or enter its selected set. This title screen is not a complete scope
classifier.

The paper phase targets **5,000 additional papers**, stopping sooner at three
hours or 3 GiB of paper-related response bytes. Both sit **inside** the original
12-hour/8-GiB-download/16-GiB-artifact run limits. It then resumes existing
web/database cursors. Prioritizing paper acquisition changes the earlier
8–10B-token pilot forecast, which assumed continuous released-shard scanning;
that forecast is no longer a commitment for this schedule.

The worker retrieves official PMC version metadata and native XML, verifies the
metadata MD5 and its own SHA-256, expands source citations, retains full table
structure and writes compressed source-linked parsed documents. PMCID/DOI
checks prevent reimporting the initial collection. New files are registered
transactionally as append-only ledger extensions; the initial manifest remains
frozen. Rejections retain available source/metadata and their reason.

Existing PDFs and image assets remain preserved. New acquisitions retain media
URLs and figure captions; binary PDFs/media/supplements are deferred for the
bounded text census. No new OCR, model inference or training is performed.

Remote shards follow a frozen interleaved source order. Complete raw files are
retained with pinned release, size and LFS SHA-256. The deadline may leave a
shard partly counted; the report shows that explicitly. Earlier prefix probes
are not substituted for full-shard measurements.

## Record accounting

Every record has a source, acquisition route, content category and modality
partition. These are different views of the **same tokens**, not additive pools.
FineFineWeb is acquired through **existing datasets**, with content category
**web text**. TheBioCollection is also acquired through **existing datasets**,
with category **database records**. Direct PMC acquisition is **online papers**.
No direct HTML crawl is included in these inputs; a database API is still a
dataset import.

The cached Qwen-family tokenizer is checked against its SHA-256 and adds no
special tokens. It is a common counting reference, not a final backbone choice.
Every full-record token is assigned once using its starting character offset:

- Content inside explicit `<protein>`, `<dna>`, `<rna>`, `<smiles>` and `<inchi>`
  tags receives that modality. Literal tag boundaries stay in the remainder.
- Everything else is **text or unclassified**, including untagged sequences.
- These categories sum exactly to full-record tokens. Tagged character counts
  are separate and are never added to tokenizer tokens.

An indexed SHA-256 comparison after whitespace collapse finds duplicate records
across files and sources, preserving case and punctuation. The first occurrence
contributes unique tokens; all occurrences contribute raw tokens. Unique source
attribution follows this frozen first-occurrence policy. Distinct annotations
and paper versions remain when their text differs.

These are **candidate counts after exact deduplication**. Near-duplicate removal,
biology/clinical scope selection and quality filtering need separate recorded
decisions; those output counts remain unknown. A biology-labelled release does
not certify every row: FineFineWeb biology includes medical material.

## Checkpoints and coverage

The ignored experiment directory contains the canonical `local_papers.jsonl`,
complete shards and resumable `.part` downloads under `raw/`, and `counts.sqlite3`.
The database stores per-record measurements, hashes and provenance; counters and
resume cursors commit atomically. `state.json` holds cumulative limits and the
original deadline. A file lock prevents a second worker.

A restart skips committed rows. Compressed files are decompressed from the
start to reach the cursor; committed text is not retokenized. Config/tokenizer
changes cannot silently reuse the ledger. Invalid/checksum-failing/oversized
inputs stop with an error rather than disappear from the denominator.

The summary tracks all **87 inventoried source families**. It distinguishes
scanned records, queued sources, missing adapters/release inventories, upstream
databases and secondary raw-modality/general-replay pools. Presence inside a
bundle does not establish coverage of a whole independent database release.
Only scanning every frozen shard completes a released-source count; unscanned
contributions stay unknown.

Local reports update about every 30 seconds, plus file boundaries and shutdown.
The batch launcher also publishes a concise [progress page](../reports/corpus_count_2026-10-17/progress.md)
to GitHub at startup, every hour and immediately on a normal stop, completion or
handled error. Updates show the active stage/file, counts gained since the
previous update, paper/web/database totals and download/artifact storage.
The interval baseline persists across worker restarts. `progress_events.jsonl`
and `progress_state.json` retain the reporting history in the ignored run
directory; `progress_delivery.json` records the last GitHub publication result.

Publication commits only the generated report files, preserving unrelated
staged and unstaged edits. It refuses to push unrelated unpublished commits or
publish from a different branch. Transport failures are logged without stopping
the census. GitHub contains the last successful push, not a live worker connection.
An in-process reporter cannot report a killed process or lost node; there is no
independent heartbeat monitor configured. These reports do not send chat
notifications. Scheduled chat delivery requires a separate supported scheduler.

## Commands

Run from the repository root. The existing `.review-venv` supplies dependencies
listed in `requirements-counting.txt`. Preparation has already frozen the
configuration and refuses to overwrite it:

```bash
.review-venv/bin/python scripts/prepare_corpus_count.py
```

Count local inputs only, or resume the full bounded worker:

```bash
.review-venv/bin/python scripts/run_corpus_count.py --local-only
.review-venv/bin/python scripts/run_corpus_count.py
```

For an authorized new/resumable run, add `--publish-progress` to enable hourly
GitHub publication outside the batch launcher. The existing October 17 pilot
has finished at its original deadline; reporting changes do not restart it or
extend its budget.

Reserve the two CPU cores for a longer run:

```bash
sbatch scripts/run_corpus_count.sbatch
```

Run one worker at a time. Request a graceful stop with:

```bash
touch experiments/corpus_count_2026-10-17/STOP
```

Remove that file only when intentionally resuming. Limits/deadline still apply.
Use a new reviewed run configuration for a larger budget or changed release;
do not overwrite the frozen inputs.

## Expanding the census

Add full PubMed abstracts, other paper collections and native database exports
through the same record schema. Each adapter needs a versioned inventory, clear
text serialization and identifiers for overlap checks. Parent databases and
derived bundles remain distinguishable; their reported training budgets cannot
be added together.

Use measured throughput and index growth to budget the remaining scan. Follow
exact deduplication with near-duplicate candidates and verified overlap or
containment, preserving removal decisions. Scope and quality audits receive
their own retained-token counters. The resulting table is **raw → exact-unique
→ near-unique → in-scope → quality-retained tokens**, by source, content and
modality. Model mixing and training are separate from this census.
