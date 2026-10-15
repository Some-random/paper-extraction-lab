**Paper acquisition paused at the user's request: 295/500 ready**

The download worker is stopped and its STOP file remains present. On October 15 the user asked to do downloading later and first consolidate foundation-model papers and related information. The shared literature home is the [foundation-model catalog](../bio_foundation_review_2026-10-15/README.md).

[Paper manifest](papers.csv) · [Exact summary and resource counters](summary.json)

Retained completed papers: **295**, including **49** reused sources and **246** newly acquired papers. Their outputs include **2,058 original figure images**, **342 main-article tables**, and **6,932,658 text tokens**. This batch uses publisher XML parsing and source figure downloads, with zero GPUs and no new OCR or training.

The first run stopped at 03:53 PST after connection failures; its candidate_pool_exhausted label did not establish exhaustion of available PMC papers. A short user-authorized continuation checked a SOCKS-compatible HTTPS client and was then stopped at the user's request before another paper was accepted. Partial source downloads remain preserved. See the [continuation record](resumption.md) and [checks](resumption_checks.json).

Cumulative response bodies: **1.95 GiB / 5 GiB**. Logical artifacts: **2.80 GiB / 8 GiB**. Bulk PDFs/XML, original images and extracted files remain on RustFS in each manifest row's source_directory. The original 50-paper experiment remains unchanged.
