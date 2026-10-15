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
