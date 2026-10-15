**Biological source batch: 295 of 500 papers ready**

The 500-paper target is **not complete**. The serial worker stopped at **03:53 PST on October 15, 2026**, after repeated connection failures. Of the 295 completed papers, **49** reused eligible sources from the previous batch and **246** were newly acquired. No document worker is currently running.

The worker's recorded status is `candidate_pool_exhausted`: it exhausted the attempted candidate list, including **1,404 attempts that failed with Connection refused**. This does **not** mean that PMC has no more eligible papers. The original runtime deadline was **09:27 PST on October 15**; it has passed and was not reset. Status checked 2026-10-15T11:28:25.809225-08:00 (fixed PST, UTC-8).

[All 295 papers: manifest](papers.csv) · [Exact counts, limits and diagnostics](summary.json) · [Original storage/time estimate](scaling_estimate.md)

| Retained output | Count |
|---|---:|
| Papers with source PDF/XML and extraction files | 295 |
| Source PDF pages | 9,274 |
| Original figure image assets | 2,058 |
| Figure records without assets | 0 |
| Recorded media download failures | 0 |
| Main-article tables | 342 |
| Source table cells | 51,195 |
| Extracted text tokens, using the configured tokenizer | 6,932,658 |
| Text chunks, at most 2,048 tokens each | 3,976 |

The batch downloaded **1.95 GiB** of response bodies and recorded **2.80 GiB** of logical artifacts, below its 5 GiB / 8 GiB caps. Hardlinked cached inputs are included in logical artifact size. It used **zero GPUs** and ran no new OCR, model inference or training.

All 295 papers have source PDF/XML/metadata, structured document and validation JSON, extracted article Markdown, original figures with captions, text chunks and interleaved records. Full main-article table TSVs and source citation/context records are retained. Required output files were checked locally. These are structural/provenance checks against publisher XML, not independent biological correctness or OCR accuracy evaluation. Source bibliography metadata is incomplete in some entries: 960 references lack titles and 725 lack authors; missing fields were not invented.

Full PDFs/XML, source images and bulk extracted results remain on RustFS in each manifest row's `source_directory`. GitHub contains the compact report and manifest. Separate supplementary files were not downloaded.
