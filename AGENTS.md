# Paper extraction experiments

This project is authorized for local sample experiments extracting open papers
into structured evidence and grounded question/answer examples.

- Keep downloads and experiments sequential: one document/inference worker.
- Do not spawn agents. Use at most one GPU, and do not interrupt other users' jobs.
- Keep all new environments, inputs, model caches, and outputs in this project.
- Reuse the current local session; do not open SSH connections for this work.
- Preserve original PDFs/XML and their hashes; keep raw extraction alongside any
  normalized output. Give evidence page/bounding-box or XML element provenance.
- Generated answers and chart interpretations are hypotheses until checked
  against the source. Never silently repair numbers, units, sequences, or labels.
- Report actual methods executed separately from methods reviewed or planned.
- Tiny exploratory sample checks are diagnostics, not general benchmark scores.
- Report human-facing times in fixed PST (UTC-8).

## Corrected scope

The user clarified that Ryze and OLMo are method references, not extraction
targets. Benchmark actual biological research papers; exclude Ryze, LLaVA-Med,
and other extraction/model-method papers from the biology test corpus.
Run the competing extraction tools, including olmOCR, rather than treating a
documentation review as an experiment. Keep the same biology input pages and
source-based checks across tools. Preserve the earlier exploratory pilot, but
do not present its mixed-domain results as this corrected tool comparison.

## Selected extractor

The user selected olmOCR 2 as the primary PDF extractor. The default runner
uses allenai/olmOCR-2-7B-1025, with its revision pinned in config/extraction.json.
Retain the competing tools and their measured results for comparison. Publisher
XML remains an independent reference and must not enter OCR prompts. The current
runner uses the checkpoint and official page prompt; do not describe it as an
execution of the full official production pipeline.

## Corpus scope

The user confirmed including related journals as well as Cell, Nature and
Science. The initial, explicit 55-title availability inventory is defined in
config/pmc_cns_scope.json; do not present it as an exhaustive publisher census.
The October 13 survey counts metadata candidates, with six verified PDF/XML
download probes and no new OCR inference. Count XML/text availability separately
from actual PDF/media availability. Use the current official PMC S3 distribution
and retain version/license/hash provenance. The shared storage mount has limited
free space; do not launch a full-corpus download based solely on this inventory.

## Authorized overnight batch

The user authorized downloading and parsing a small biology corpus, with results
by tomorrow morning and limited storage/quota use. The active October 14 batch
is configured in `config/pmc_overnight_2026-10-14.json`: up to 50 papers, five
from each of ten CNS and related journals; 1,000 OCR pages; 2 GiB of new batch
artifacts; 1 GiB of downloaded response bodies; six hours of cumulative runtime.
Use one serial document/network/inference worker, two CPU threads, and GPU 0 only.
Reuse cached olmOCR 2 weights offline; no paid APIs, teacher synthesis or training.
Download through the existing Python 3.10 environment's HTTPS bridge, with TLS
verification intact; the GPU Python environment intermittently fails TLS.

The worker started at October 14 00:12:01 PST and must stop by 06:12:01 PST.
The assumed requested report deadline is October 14 08:00 PST (fixed UTC-8).
Do not reset the runtime allowance on resume. The shared-filesystem free-space
floor is 32 GiB. Temporary page rasters may be removed; keep original PDFs/XML,
metadata, hashes, raw OCR and per-paper context/evidence outputs. Report complete
OCR, partial OCR, deferred papers and XML-only parsing separately. Source-cell
lookup QA is diagnostic, and biological figure semantics remain unverified.

Live report and state are in `experiments/pmc_cns_biology_2026-10-14/`.
Creating that directory's `STOP` file requests a graceful stop after the current
bounded operation. A file lock prevents duplicate workers. Confirm the current
worker is absent before resuming; do not start another extraction process while
this batch is running, and do not interrupt another user's process.

The October 14 batch completed at 04:14 PST: 50 native parses, 37 complete OCR
papers, one partial paper, 12 deferred papers and 1,000 retained OCR pages.
There is no worker left running for this batch. The tracked compact summary
and paper manifest are in `reports/pmc_cns_biology_2026-10-14/`; original inputs
and raw outputs remain under the ignored experiment directory. Preserve both
the source files and the unmodified diagnostic results.

## Git identity and storage

The user explicitly selected `Dongwei <jdw19930725@gmail.com>` for this
project's Git commits. Use repository-local configuration on this shared host.
Track code, configuration and small reports. Keep papers, model weights,
environments, caches and bulk extraction artifacts on RustFS under the existing
ignore rules.

## Biological research production scope

The user selected citation title/author expansion directly, without a policy
comparison. Preserve full source titles and all supplied authors as metadata;
render title plus first author/et al. in training text. Preserve prior outputs.
Prioritize real biological literature, source figures/tables/supplements and
biological databases before synthetic augmentation. Clinical notes are outside
this project's research scope. Include reusable corpora such as Dolma and
peS2o in source planning; distinguish corpus versions from processing toolkits.

## Authorized native-source expansion

The user explicitly confirmed retaining original figures, no model training,
and expanded the target to 500 papers total. The new native-only batch is
configured in `config/pmc_native_500_2026-10-15.json`: reuse eligible cached
PDF/XML, retain source images/captions/referring paragraphs and full article
tables, with cited titles/authors. No new OCR, VLM inference, synthetic captions,
teacher API, training, web crawl or separate supplementary-file download.
Use one serial document/network worker, two CPU threads and zero GPUs. Stop
at 500 papers, 5 GiB response-body downloads, 8 GiB logical artifacts, ten
cumulative hours or a 32 GiB shared-filesystem free-space floor. Preserve the
old batch and its expired budget. The new batch has its own lock/state/STOP
file; resuming does not reset its runtime allowance. Publish compact reports
and manifests to GitHub; bulk source and extraction artifacts stay on RustFS.

On October 15, the user explicitly asked to keep going after the first run
stopped at 295 papers during a network outage. The recorded continuation in
the same config uses the unused 5h 33m 36s of the original ten-hour worker
allowance, with a fixed cutoff of October 15 17:31:13 PST. Preserve original
timestamps and cumulative 5 GiB download / 8 GiB artifact counters; do not
extend this cutoff on another resume. `resumption_launch.json` records the
new PID. The HTTPS bridge now uses existing requests[socks] for the supplied
SOCKS proxy; bounded backoff retries the pending request before advancing.
Persistent outages must be reported as network_unavailable, not candidate
exhaustion. All other native-only, serial and zero-GPU constraints still apply.

The user subsequently said to do downloading later and prioritize aggregating
foundation-model papers and related information. The resumed download worker
has stopped via its STOP file; leave it stopped. Consolidate literature in
`reports/bio_foundation_review_2026-10-15/review.json`, with generated Markdown
pages and CSV in that same directory. This is the extraction project's
literature home. Update existing model entries instead of starting separate
coverage-update tables. Biological evaluation has a separate private home at
`https://github.com/Some-random/bio-evaluation`; keep its protocols, benchmark
cases, labels and raw runs there.

## Literature table token counts

The user explicitly requires numeric token amounts for three acquisition
categories in the main catalog: online papers, web URLs, and existing datasets.
Do not replace token amounts with paper/example counts, dataset names, or a
combined "processing and reported amounts" column. Keep processing details on
the model pages. `review.json` stores `token_budgets`; the renderer generates
the main tables, detailed allocation notes and numeric CSV from those records.
Separate corpus amounts, sampled/consumed training exposure and scheduled or
packed token positions. Preserve tokenizer/modality definitions, primary-source
citations, calculation notes and lower bounds. `NR` is not zero. Do not turn
word/document counts or maximum sequence lengths into invented token totals.
Avoid counting imported paper/web text twice: classify it at the reviewed
study's acquisition/curation stage, and retain its original content description
on the model page. A missing category split stays explicit even when the total
is known. Source-reported totals may include generated or other unallocated
material and need not equal the known category subtotals.

## Presentation and continued-pretraining scope

The user wants the main review ready to share and focused on biological CPT.
Merge CPT curation studies (including Biomed-Enriched) with CPT models. Name
each starting checkpoint and distinguish random-initialized models in a
separate from-scratch comparison. Keep instruction-only training, representation
learning and general extraction recipes in supporting references. Medical and
clinical models from the earlier broad review remain archived, outside the
main comparison; do not copy clinical filtering priorities into biology.

Show one explicitly selected token budget per model/study in the main tables,
with a plain-language label distinguishing dataset size, training consumption
and scheduled/packed positions. Preserve all original budgets on study pages
and in the registry. Do not put CSV/registry download links, verification logs,
maintenance instructions or private evaluation navigation on the shared page.
Keep them in maintenance documentation. These requirements change presentation
and scope, not the pause on corpus acquisition or the prohibition on training.

The user also clarified that acquisition-route counts must not be mistaken for
biology-only counts. Label general replay, clinical literature, other sciences
and non-text modalities explicitly. Preserve reported totals, but do not call a
mixed total biological tokens without a supported subset calculation. Remove
the vague main-table "What is counted" column; label exceptional training
exposure and token-position rows directly, with content scope visible.

The shared paper/web/dataset processing design is documented in
`reports/bio_foundation_review_2026-10-15/data_pipeline.md`. It is a design that
builds on implemented native-paper work; the web adapter, calibrated filters and
global cross-route deduplication are not claimed as already implemented. Keep
those statuses explicit and keep acquisition paused until the user resumes it.

## Fresh 500-paper acquisition

The user subsequently asked to start crawling all 500 papers after the review
update, without counting earlier acquisition work. This supersedes the pause
for this new run only. Use `config/pmc_native_fresh_500_2026-10-15.json`, with
separate output/report directories and no prior source or asset seeding. Earlier
batches remain preserved. Count 500 accepted, within-run unique papers using
the same ten-journal scope, 50 per journal. The new bounded allowance is ten
hours, 5 GiB response bodies and 8 GiB artifacts; enforce the configured fixed
cutoff and 32 GiB free-space floor. Run one serial document worker on two CPU
threads and zero GPUs. Retain PDFs/XML, native text, source figures/tables and
citations; no new OCR, inference, training or separate supplement acquisition.
Publish compact progress/final manifests, with bulk artifacts kept locally.

## Attribution, dataset names and paper assessment

The user requests compact existing-dataset names alongside token amounts and
two additional overview columns: authors/institutions and overall paper quality.
Store credits, named input datasets and source-based
assessments in the same review registry. Use first-author/group names and short
institution names in the table, with fuller source information on study pages.
Assess experimental controls, overlap/leakage, reproducibility and support for
claims; do not use institution prestige as a quality score. Each assessment
needs strengths, limitations and primary-source links and must not imply an
independent replication. Record numerical corrections explicitly: BioMatrix's
existing-dataset lower bound is 176.7B from 25.6B general text, 77.4B protein
data and 73.7B molecular data, replacing the incomplete 25.6B-only bound.

The user clarified that narrow evidence-strength ratings do not answer the
quality question. Assess the whole paper in its publication context, including
contribution/originality, technical soundness, evaluation, reproducibility and
clarity. Use an explained qualitative judgment rather than an invented numeric
score; keep earlier evidence assessments in the registry as historical records.
Name the publication repositories beneath online-paper amounts, distinguishing
direct acquisition from paper text imported through datasets. Add an overview
column for other modalities, with detailed sequence, structure and image counts
where supported. Modality describes the same data as acquisition route: never
add these amounts again. Distinguish pure sequence tokens from domain buckets
that include annotations, and distinguish counted CPT inputs from later encoder
or instruction-tuning inputs.

The user wants authors/institutions near the end of the overview table, after
data quantities and quality. Sort both CPT and from-scratch tables by overall
paper quality, with alphabetical ties rather than an implied ranking within a
rating. Show numeric modality counts directly in the overview, retain NR for
unknowns, and distinguish source-record/domain amounts from pure sequence
amounts. Make BioMatrix's complete 304.4B corpus composition and its 127.7B
unresolved acquisition-route allocation visible; modality counts overlap the
source-route counts and must never be added to them.

The user subsequently requested a simpler overview: remove dagger markers and
their training-token/position footnotes, consolidate row links into the Source
column, and avoid repeated NR labels. Use one Paper link and one Notes link per
row, with source names, dataset names, ratings and modality counts as plain
text. Render unavailable category amounts as a dash, unknown totals as "Not
reported", and explain the dash once. Preserve zeros, all numeric amounts and
the full count-basis definitions on study pages and in the registry. Do not
claim that the resulting unmarked amounts all represent unique corpus tokens.

The user clarified that the requested update is to the processing diagram,
not to the dataset/model explanation page. Keep the diagram, concrete actions,
relevant papers together in
`reports/bio_foundation_review_2026-10-15/data_pipeline.md`. The catalog README
remains the model/data comparison, with a single link to the processing page.
Do not insert the extraction plan into the catalog or confuse planned steps
with implemented extraction.

The user wants this page to be the figure itself: put processing explanations,
including how filtering scores are obtained and applied, inside the diagram.
Use paper names in the nodes, not numbered reference markers. Remove detailed
sections below the figure and remove implementation-status labels such as
"next", "to build" and "pending" from the diagram. Present it as a processing
recipe, not a report of executed work. Preserve actual execution state in the
existing experiment reports. Attribute the 400k teacher-labeling example and
the educational-score threshold to Biomed-Enriched; do not present educational
value as a scientific-validity score or apply prose scoring to non-text data.

The user subsequently rejected the dense diagram, hard-coded XLM-RoBERTa
choice and emphasis on Ryze. After requesting a text outline first, the user
authorized a shorter diagram version and asked to draw on OpenThoughts3 across
the recipe. Use two readable SVG figures on the processing page, with paper
names inside the relevant blocks. Preserve the distinction between directly
supported source techniques and our biological-CPT adaptations. OpenThoughts3
supports controlled source/filter/teacher comparisons; its reasoning-SFT
question difficulty, answer sampling and answer filtering results do not prove
benefits for raw-paper CPT. Keep model selection empirical, use reviewed labels
and held-out checks for scoring, and choose mixes by controlled training gains.
This is documentation of a proposed recipe, not authorization to run training.

The user then requested text instead of flowcharts, with more explanation so
the recipe is readable. This supersedes the figure-only and two-SVG presentation
instructions above. Keep a concise prose walkthrough in `data_pipeline.md`,
with the relevant named papers beside each step. Explain extraction, metadata
versus model-visible tags, citation expansion, explicit cleaning and duplicate
checks, scorer labeling/training/validation, mixing experiments and token
accounting. Preserve the OpenThoughts3 reasoning-SFT versus biological-CPT
distinction. The catalog should link to it as the "Processing recipe".

The user further requested bold "References:" labels and a link for every
paper named in each reference paragraph, including repeated olmOCR 2 mentions.
Include concrete linked examples for paper, web and existing-dataset inputs.
Distinguish FineWeb-Edu's teacher-generated training/validation labels from
DCLM's separate human-annotation study; our human audit is an optional addition.
Describe OpenThoughts3 through its useful staged curation experiments without
repeated limitation or training-stage caveats. Make the mixing experiments
concrete, with explicitly illustrative budgets, fixed controls and decisions.
Finish the pipeline at stage 6; fold packaging and token accounting into that
stage instead of keeping a separate stage 7. Explain mixing in the chat as well
as updating the page. These are documentation changes, not training permission.

The user rejected the three-run A/B/C mixture example as an inadequate account
of actual practice. Replace it with the documented DCLM/OpenThoughts3 experiment
designs and OLMo 3 proxy-model mixture search. Explain concrete deduplication
operations: comparison normalization, exact hashes, MinHash/LSH candidates,
verified overlap and containment, span versus document decisions, and version
preservation. Distinguish the absence of a required new manually labeled scorer
training set from the unsupported claim that human review is unnecessary.
Targeted expert checks are our proposed biological-corpus validation step.

The user wants human annotation/review to be visually prominent within the
filtering stage. Use a short GitHub callout distinguishing automatic training
labels, published human studies and our planned biological review. Expand the
mixing discussion into separate readable profiles for DCLM, OpenThoughts3,
OLMo 3 and Marin, explaining the units mixed, experiment controls, search and
selection procedure. Marin's September 2026 Datakit report is a primary method
reference for topic-by-quality buckets, repetition-aware proxy experiments and
validation against proportional sampling at larger scales. Attribute that
report specifically rather than merging it with the earlier Marin 8B recipe.

The user then rejected the leftover paragraph about finalizing, packaging and
reporting counts at the end of stage 6. Remove that paragraph rather than moving
or paraphrasing it again. Explain the output of mixing directly: source/topic
sampling weights, within-topic quality upsampling rules and the resulting text
stream consumed by training. Use OLMo 3's actual Table 4 mixture as a concrete
example, not another hypothetical A/B/C experiment. Keep token-budget records
in the catalog unchanged; this is an explanation of the published recipe.

The user requests the same concrete-output explanation for OpenThoughts3.
Show the released 1.2M-example dataset, its 850k math / 250k code / 100k science
composition, and the 75k selected question entries with 16 teacher responses
per entry. Distinguish training examples from unique questions and tokens.
Attribute the domain allocation to the earlier OpenThoughts2 mixture, as stated
in the paper, rather than presenting it as learned token weights.

## Latest overview presentation

The user now wants the sparse direct-web column and its explanation removed
from the shared overview. Preserve those counts in the registry, detailed
study pages and numeric export. Use shorter wrapped table headers, consistent
left alignment for mixed text/count cells and separate lines for dataset names.
Make the processing page's six stages level-two headings, with method profiles
under stage 6 at level three. Keep processing explanations on that page; the
overview links to it without repeating the recipe or model runtime estimates.

Make paper availability explicit: 55 means journals, containing 552,024 paper
candidates; the broader PMC inventory has 9,324,889 candidates. The journal list
does not limit future collection. The 49.1B-token central forecast quantifies
only the initial subset and two datasets, not the whole PMC inventory. Briefly
explain TheBioCollection as biological database records, including sequences,
molecular representations and annotations. Present a combined storage budget
for the initial corpus, with assumptions and expansion costs in source planning.

The user now wants other-modality counts before total tokens in both overview
tables. The small starter forecast must not stand in for the full available
source inventory: distinguish larger released scientific-text and genomic
pools, their native counting units and unmeasured overlaps. BioReason's CPT
classification was a question only; do not move it into the CPT table on that
basis. Its reviewed DNA-LLM experiments use SFT and selected GRPO.

The user requests paper years beside model names. Use sourced first-public
paper/preprint years in `publication`, retaining later-version and checkpoint
release distinctions in the notes. Group raw sequences and structures as a
secondary collection priority; prioritize papers, biological web text and
annotated database records for this text-based CPT project. This is a project
choice, not an established ranking of intrinsic training value. Retire the
old 50B/15%-web-retention scenario as the overview forecast. Show the broader
PMC archive (about 12.5M records), the 9.32M text-mining candidates and the
552,024-paper journal subset distinctly. Treat full-PMC token extrapolations
as pre-filtering scenarios, not measured retained biological counts.

The user rejected the public overview's archive-count and journal-subset
bookkeeping paragraph. Remove that narrative from the shared page. They want
an aggregation across all sources rather than a few examples. Maintain the
complete named-source register and aggregate table, preserving overlap and
unit distinctions. Do not label a subtotal from measurable families as the
complete biological-corpus total while other contributions remain unmeasured.

Place the available-training-data summary last in the overview, after both the
continued-pretraining and from-scratch comparisons. Present what existing papers
did first, then conclude with the overall available-data picture.

## Authorized actual corpus counting

On October 17 the user requested setting up the data pipeline and starting
actual counts. Use the frozen `config/corpus_count_2026-10-17.json`: the existing
454-paper exports, 864 pinned FineFineWeb biology shards and 32 pinned
TheBioCollection free-text shards. This is a new bounded CPU census, not a
resumption of expired paper-acquisition jobs. Keep one worker, two CPU cores,
zero GPUs, no inference or training. Its cumulative limits are 12 hours from
first launch, 8 GiB reserved downloads, 16 GiB new artifacts and a 32 GiB
free-space floor. Do not reset them on restart. Preserve raw shards and hashes;
use a locked transactional ledger. Publish measured candidate/exact-unique
counts separately from estimates, near-dedup/scope/quality retention and
unscanned source totals. Route/content/modality are alternative breakdowns;
do not add them together. Keep all evaluation jobs and old batch files untouched.

On October 17 the user then asked to process more papers. The frozen extension
plan `config/corpus_count_pmc_expansion_2026-10-17.json` targets 5,000 new native
PMC XML papers from broad topic/year searches, without the original journal
restriction. Give this paper phase up to three hours and 3 GiB of response
bytes inside the original census's cumulative limits, then resume the stored
web/database cursors. One worker/lock/ledger, two CPU cores and zero GPUs still
apply. Record all version/license/checksum/source provenance, citations, table
structure and media URLs. New binary PDF/media/supplement acquisition is deferred
for the text census; original assets remain preserved. This supersedes the
454-paper-only scope for this census, not the limits on expired older jobs.

The initial canonical paper adapter mistakenly appended caption/table views
already present in its article blocks. Preserve the superseded 12,677,035-token
result in the correction audit, and use the corrected **10,609,606** tokens for
the initial 454 papers. This correction does not change the web/database counts.
Acquired source files are appended transactionally without rewriting the base
manifest; a registered extension plan/checksum and explicit correction marker
prevent silent changes on restart. The earlier 8–10B pilot-token forecast must
be reconsidered after prioritizing paper acquisition.

The new-paper adapter screens explicit clinical-care/trial/device titles.
Already acquired examples caught in the startup audit retain their raw counts,
source files and `excluded_scope` status, but do not count toward the selected
new-paper target and must not enter the selected-paper set. This transparent
title screen is not claimed as a complete biology/clinical scope classifier.

## Long-running task updates

The user requests hourly updates during long-running work. Report the active
stage, papers/records and tokens gained since the previous update, cumulative
paper/web/database counts, downloads and artifact storage, and any errors or
blocking conditions. Give a final update promptly when work finishes or stops;
do not leave the user believing a stopped worker is still running. Persist the
cadence across restarts. While a conversation is active, provide these updates
in the conversation as well. State the actual delivery mechanism for unattended
jobs: saved files and GitHub commits alone are not proactive chat notifications.
This reporting preference does not authorize extending expired run budgets,
starting training, acquiring more data, or touching evaluation work.

## Existing cluster data and biological-share verification

On October 18 the user requested searching existing cluster downloads, then
verifying their biological share. The private inventory and source locations
are under `experiments/cluster_data_inventory_2026-10-18/`; keep other users'
cluster paths out of public reports. Read shared sources in place without
modifying their files. Do not reuse licensed central catalogs contrary to
their explicit local access conditions.

The bounded CPU-only probability sample in
`experiments/biology_share_2026-10-18/plan.json` selects two uniform rows from
each of 234 SmolLM FineWeb-Edu-Dedup shards and four from each of 14 FineWeb-Edu
10BT shards. Preserve its seed, full document samples and selected failures.
No new corpus downloads, GPU jobs, training or evaluation work is authorized.
Semantic assistant labels are model judgments, not human expert annotation.
Report biology, clinical/health, mixed and other separately, using token and
shard-population weights with sampling uncertainty.

The earlier cache-presence inventory was not an integrity check: payload reads
identified zero-filled data pages and 31 failed selected locations across 23
larger-cache files. Do not silently resample or classify failures as other.
Estimate the readable-content domain with original inclusion weights and
explicit zero domain contributions for unreadable rows, not invented lengths.
Keep any 200-shard allocation-based subset check explicit and avoid projecting
readable-domain fractions onto the reported full 220B total. The two web pools
overlap and their biological token estimates must not be added.

## Reconcile existing sources and bound storage

The user requested reconciling existing cluster copies with remaining downloads,
explaining Biomni's overlapping database resources, and restricting peak storage.
The metadata-only manifest join is implemented in
`scripts/reconcile_corpus_inventory.py`; public aggregate/shard results are under
`reports/corpus_overview_2026-10-18/`, with detailed paper paths kept under ignored
experiments. Match release/revision/path/hash at file level and namespace/ID/
version/content at record level. Matching size is not checksum validation, and
equal biological entity IDs do not make different annotations or assays duplicates.

The proposed new-run policy is `config/corpus_storage_policy.json`: 200 GiB of
pipeline data including the counted pilot, staged inputs, retained compressed
outputs, indexes and temporary copies, plus a 64 GiB shared-free-space floor.
It has not launched or changed any acquisition worker. Preserve existing originals
and shared files; retain original XML for new retained papers, and pause on
capacity rather than deleting archived sources or final outputs. A full 254B-token
uint32 pack alone needs about 1.02 TB, so do not claim it fits in the bounded
workspace. Keep processing explanations on `data_pipeline.md` and resource
allocations in the capacity plan; no old run budget is extended by this request.

## Authorized short 4B throughput benchmark

On October 18 the user accepted the proposed short training-throughput benchmark
and requested total cluster GPU counts. This authorizes a separate bounded
diagnostic with the pinned Qwen3-4B architecture, random initialization and
synthetic fixed-shape tokens: BF16 forward/backward, FP32 AdamW states, no model
checkpoint saving, no biological capability claims and no full training run.
Use `config/training_throughput_2026-10-18.json`. Request GPUs only through SLURM;
leave all existing jobs, including the user's evaluation jobs, untouched. A short
single-GPU baseline and up to one eight-GPU follow-up are in scope. Each
allocation is limited to 20 minutes (maximum eight GPUs); cap new environment
and benchmark artifacts at 16 GiB and keep them in this project. The benchmark
scope supersedes the old no-training/one-GPU restrictions for this diagnostic
only. Report queued, running and measured states accurately; do not infer
measured multinode efficiency from a single-node result.

The first held requests were cancelled after CPU validation timed out; they
used no GPU time. A bounded repair preflight passed with bytecode writes
disabled. Preserve the cancelled attempts and failure history. Use B200 for
both replacement allocations: the A100 scheduler previews proposed preempting
other jobs, while the B200 previews did not. GPU runtime limits are unchanged.

Run `scripts/watch_training_throughput.py --publish` alongside this diagnostic.
It checks only recorded benchmark job IDs and publishes hourly while queued or
running, including unchanged waiting, and promptly on state changes. It stops
after known work is terminal or its persisted seven-day deadline. Keep its
status/history under the ignored run directory; publish the sanitized report.
This is GitHub reporting, not a configured proactive notification into chat.
While the conversation is active, also report status here. Never describe a
failed, cancelled or stopped job as still running or waiting.

## Matched two-B200 versus eight-A100 test

The user explicitly requested starting these two configurations. This replaces
the queued eight-B200 follow-up; preserve its manifest and cancel only that
obsolete owned request. Use `scripts/run_matched_training_throughput.sbatch`
and the updated `config/training_throughput_2026-10-18.json`. Both allocations
use the same 4B architecture, 4,096-token context, 32 sequences / 131,072 tokens
per optimizer update, BF16 compute and FP32 AdamW. Test microbatches 1, 2 and 4
with matching accumulation inside each allocation. Keep all profile results;
only a fully completed matched profile can win the throughput comparison.

Each allocation is limited to 20 minutes; the suite itself is limited to 17
minutes and does not reset on restart. Both allocations together use at most
3.33 new GPU-hours. Admit them sequentially, at most eight GPUs at once. Keep
the existing 16 GiB environment/artifact cap. No additional acquisition, model
checkpoint saving, full training or evaluation changes are authorized.

Hold the requests until the CPU admission helper observes spare GPU/CPU/memory
capacity and a scheduler preview without proposed preemptions, then bind the
checked node and release only the recorded owned request. This is not atomic
with the scheduler and cannot eliminate every race. The admission helper has
a persisted seven-day deadline; it must report expiry and leave unstarted jobs
held rather than silently extend the wait. Continue hourly status publication.

The user then explicitly added four-B200 and eight-B200 allocations. Keep the
two-B200 and eight-A100 requests, extend the same admission allowlist to all four
owned requests, and preserve its original start/deadline and job states. All
four use the same matched batch and profile sweep. Each retains the 20-minute
wall limit; the four together cost at most 7.33 GPU-hours and still admit only
one allocation at a time, at most eight GPUs concurrently. Queued requests use
no GPU time. No unrelated jobs or full training runs are authorized by this.

The benchmark remains Qwen3-4B-Base's architecture with random weights.
Proteo-R1's official checkpoint config identifies Qwen3-4B-Instruct-2507 as its
language backbone. Core tensor dimensions match, while context/RoPE settings
and weights differ. Preserve the sourced comparison in
`config/proteor1_backbone_reference.json`; do not describe the language-only
throughput benchmark as a benchmark of the full Proteo-R1 system.

## Normal scheduler queue replaces the extra admission gate

The user objected to the idle-only holds. Remove that extra gate and stop the
admission helper; the prior gate instructions above are superseded. Let Slurm
apply its normal scheduling and preemption rules. Do not manually stop, change
or cancel other users' jobs or any evaluation work. Two B200s and eight A100s
use regular `il`; four and eight B200s require `il-lo` under the current two-B200
regular-queue cap. Set ordinary job niceness, retain all four owned requests,
and use afterany dependencies in the order two B200s, eight A100s, four B200s,
eight B200s. This preserves one allocation at a time and the existing maximum
of eight concurrent benchmark GPUs. Keep every 20-minute wall limit, the same
matched workload and the 7.33 GPU-hour combined limit. Restart only the hourly
status watcher, preserving its cadence and deadline. GPU count is not a blanket
guarantee against preemption; do not claim `il-lo` jobs are protected.

## Reuse-first paper collection

The user explicitly resumed paper acquisition on October 18 and asked for a
reasonable batch without downloading papers already on this cluster. The new
run is `config/paper_collection_2026-10-19.json`; earlier expired runs remain
stopped and their originals/results stay preserved. First index all known
full-text paper IDs, including the older article archive's body-bearing records,
then read the existing native XML in place and acquire up to 10,000 absent
selected papers. Abstract-only records do not block full-text acquisition.
Frozen private catalogs record source paths, IDs, sizes, timestamps and hashes;
never publish other users' paths or bulk article text.

Use one serial worker, two CPU cores and zero GPUs, with a fixed 24-hour
deadline, 8 GiB of HTTP response bodies, 32 GiB of new artifacts, a 64 GiB
shared-free-space floor and the overall 200 GiB pipeline-data ceiling. Include
indexes, original new XML, compressed parsed/canonical text and temporary copies
in the run budget. Preserve license/version/hash/XML provenance, citations,
tables, captions and media URLs. This phase does not download PDF/image/figure/
supplement binaries or genomes and does not run OCR or training. Known IDs and
exact text hashes are separate checks; do not claim near-duplicate filtering,
human-validated biology labels or complete knowledge of every cluster disk.

Publish compact progress hourly while queued or running and promptly on failure
or completion using the independent paper watcher. Serialize all automatic Git
publication through `experiments/report_publication.lock`, preserving unrelated
staged and unstaged edits. GitHub reports are not automatic chat notifications.

## Hourly updates in the current chat

The user explicitly requests hourly updates in this conversation, including
while jobs are queued and when they stop or fail. The installed CLI supports
`codex queue --thread UUID --message TEXT`; use the private configured current
thread ID to queue narrowly scoped, read-only status checks. Do not open another
interactive session, resume the conversation elsewhere, change its model, or
send updates to another person. Preserve cadence and the original monitor
deadline across restarts. Report queue acceptance separately from actual chat
delivery; delivery requires the local Codex app-server/session to remain
available. Never claim that GitHub publication alone satisfies this request.

`scripts/run_status_updates.sbatch` runs the paper reporter, throughput reporter
and chat timer in a dedicated one-CPU, zero-GPU Slurm allocation. It uses the
same host as the existing local Codex server. Restart failed reporter children
within their original deadlines, without resetting worker budgets. Private
thread IDs, launch records and timer state remain in ignored experiments.

## Throughput verification after the timeout

The user explicitly requests checking the failed eight-A100 run and verifying
whether setup or training implementation explains the B200 rate. Use
`config/training_throughput_check_2026-10-19.json` for two additional bounded
allocations: two B200s and eight A100s, 20 minutes each, at most 3.333 additional
GPU-hours. Keep one benchmark allocation at a time and at most eight GPUs.
Preserve earlier results and the queued four/eight-B200 requests. Use normal
Slurm scheduling; no idle-only admission gate or changes to evaluation work.

Record per-rank startup phases and stack diagnostics. Time setup, warmup,
training and the separate CUDA profiling step independently. Keep the same
4B architecture, 4,096-token context and 131,072 input positions per optimizer
update. Compare the original baseline with explicitly labeled checkpointing
and sharding variants; a tuned result is not a matched baseline hardware
comparison. Reuse installed packages and synthetic inputs, with no model
weight download or saved training checkpoint. New launch manifests and job
outputs stay in the existing throughput registry so hourly reports and chat
updates include them automatically. Measure the existing environment footprint
in CPU preflight, rather than traversing the entire shared environment while
holding a GPU allocation.

## Authorized B200 optimization sweep

On October 19 the user explicitly asked to try all useful B200 training
optimizations from the reviewed literature. This authorizes a new bounded sweep
in `config/b200_optimization_2026-10-19.json`: one two-B200 allocation of at most
two hours (four additional GPU-hours), with a persistent 110-minute suite budget.
Keep benchmark allocations sequential and retain the earlier A100/four/eight-B200
requests and results. Use ordinary Slurm scheduling; briefly wiring dependencies
is not an idle-capacity admission gate. Leave evaluation work untouched.

Use new runner/suite files and an isolated `.b200-opt-venv` overlay. Preserve the
original environment and frozen runner used by earlier queued jobs. CPU package
and API preflight may install compatible binary wheels within 16 GiB of new
environment/cache data, including at most 4 GiB of compiler caches. Keep logs and
results within 256 MiB and shared free space above 64 GiB. Do not build large
packages from source or download/save model weights. Paper acquisition retains
its separate original limits and deadline.

Test available BF16 attention backends, fused/chunked losses and pointwise
kernels, compilation, FSDP2, checkpointing/sharding variants, and native FP8/MXFP8
training. Include native FP4 or activation/optimizer compression only where a
compatible executable training implementation is available; record incompatible
research integrations explicitly rather than substituting BF16 or emulation.
Hold the Qwen3-4B architecture, 4,096-token context and global batch of 32
sequences fixed. Compare individual changes before selected combinations, reject
failed numerical checks, preserve every failure, and report the original baseline
separately from the fastest validated optimized profile. Synthetic throughput and
numerical smoke checks do not establish biological quality or long-run stability.

Register new job IDs in the existing throughput registry so the existing hourly
GitHub and same-chat monitors include the sweep without resetting their deadlines.

## Sustained verification, capacity-limited collection and two-hour updates

On October 20 the user requested the same optimization work on eight A100s and
questioned extrapolating a few timed seconds to an hour. Use new versioned GPU
runner/suite files, preserving frozen earlier runners. One new eight-A100
allocation is limited to two hours (16 additional GPU-hours), including short
compatible probes followed by baseline and winner confirmations with at least
600 timed seconds each. Use pinned Qwen3-4B architecture and tokenizer, real
paper text, context 4,096 and 32 sequences per optimizer update. Count actual
data loading and transfer within the timed interval, record startup and compile
warmup separately, and distinguish random-initialized throughput from CPT
quality. Keep numerical checks, resource guards and sequential GPU allocations;
leave the queued four/eight-B200 requests and evaluation work preserved.

The user explicitly requested continuing paper downloads until reasonable space
is insufficient. A new versioned continuation may clone the stopped October 19
ledger and reuse existing sources in place. Its cumulative stop conditions are
the 64 GiB shared-free-space reserve and 200 GiB combined pipeline-data ceiling,
including originals, indexes, outputs and temporary copies. The old expired
24-hour, 10,000-paper and 8 GiB HTTP allowances are historical, not continuation
stop conditions. Keep one serial two-CPU, zero-GPU native-XML worker; preserve
all old sources/results. Checkpoint and requeue only its own allocation when
needed rather than resetting capacity counters or claiming completion.

The user changed routine reporting to every two hours in this same chat and on
GitHub, superseding all hourly cadence instructions above. Preserve the original
monitor deadline and accepted-update history across restarts. Still report
completion, failure or capacity stops promptly; queue acceptance alone does not
prove that a chat update was displayed.
