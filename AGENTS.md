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
