**Storage and time before the 500-paper expansion**

The user confirmed **retain original figures; no model training**, and increased the target from 100 to **500 papers total**. Existing sources are reused. The original 50-paper batch is frozen and remains available.

| Scope | Estimated additional RustFS storage | Estimated wall time, one serial worker | GPU |
|---|---|---|---|
| 100 papers total, reusing eligible cached papers | **0.5–1 GiB**; 2 GiB would provide margin | **45–90 minutes** | None |
| 500 papers total, reusing eligible cached papers | **5–8 GiB planning allowance** | **6–10 hours** | None |

These are estimates, not completed-batch measurements. They include source PDFs/XML, original figure images, complete article tables, text/chunks, citation/context records and compact reports. They exclude new model weights, new OCR, generated figure descriptions, training and separate supplementary-file downloads. Supplements can be much larger and need their own budget.

**Measured basis**

- Existing 50 papers: **301,998,820 PDF bytes + 15,091,089 XML bytes**, 1,582 PDF pages and 382 source figures.
- The earlier acquisition/native stage took **38.2 minutes**, including debugging. A linear 500-paper projection is **6.37 hours** before figure-download latency. Reusing cached papers saves acquisition work.
- Existing source-image sample: **25 assets / 4,023,282 bytes** from three papers, about 157 KiB per image. At the earlier 7.64 figures/paper, 500 papers project to approximately **3,820 figure assets / 0.57 GiB**. Three selected papers do not establish the full image-size distribution.
- The three papers' per-paper native derivatives, excluding images and separate supplements, occupy **5,617,103 bytes**. Combined source, image and derivative linear projections give approximately **4.31 GiB from scratch**, before variation, retries and operational margin. The 5–8 GiB allowance is deliberately larger, rather than a claim that all 8 GiB will be used.
- CPU-only preflight parsed the actual 50 retained source XML files in **11.556 seconds**, preserving 382 figure and 34 table records. Network acquisition dominates the estimated runtime.
- The mount had approximately **195 GiB available** at preflight. The worker checks a **32 GiB free-space floor**, because other users can change shared usage.

**Firm run limits**

One document/network worker, two CPU threads, **zero GPUs**, **5 GiB downloaded response bodies**, **8 GiB logical batch artifacts**, and **10 hours cumulative runtime**. Resume does not reset the runtime allowance. A `STOP` file in the batch directory requests a graceful stop. Per-file limits: PDF 20 MiB, XML 5 MiB, image 8 MiB, PDF 60 pages; source tables may have up to 2,000 rows. Oversized or unresolved media are listed rather than silently treated as retained.

Raw reused files are hardlinked on the same filesystem, avoiding duplicate physical bytes. Logical budget accounting counts those links conservatively. Source PDFs/XML and figure hashes are retained. Bulk artifacts stay on RustFS; GitHub receives the comparison tables, resource estimate and compact paper manifest.

**Duplicate and scope preflight**

The existing 50 records have **zero duplicate PMCIDs, DOIs, normalized titles, PDF hashes or XML hashes**. All **100 stored PDF/XML hashes** were rechecked against the actual files. One cached medical-AI model-evaluation paper is excluded by the new model/extraction-method title filter, leaving **49 eligible sources to reuse** and approximately **451 new papers** to reach 500. This is a scope exclusion, not a duplicate. Biological experimental/computational methods remain eligible; LLM/extraction-method reports inform this project's recipe but are not acquisition targets.

The old 150-row preview bound blocked five of the 50 papers. A configurable row budget fixed that limit; all 50 source parses then passed, and the existing 10 regression tests passed. A separate three-paper pipeline smoke check uses cached sources/images and a **zero-byte network budget** before launch.

For comparison only, full olmOCR on the projected 500-paper / 15,820-page corpus would require approximately **53.1 GPU-hours of inference alone** at the previous measured 12.09 seconds/page, plus acquisition and overhead. That is not part of this run.

[Exact calculations and audit](scaling_estimate.json) · [Run configuration](../../config/pmc_native_500_2026-10-15.json) · [Additional foundation-model coverage](../bio_foundation_review_2026-10-15/coverage_update.md)
