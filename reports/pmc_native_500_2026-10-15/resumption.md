The user authorized continuing the 500-paper batch on October 15. The worker
resumed at **11:57:37 PST**, starting from **295 completed papers**. Its fixed
cutoff is **17:31:13 PST** on October 15, using the unused 5h 33m 36s of the
original ten-hour worker allowance. Original timestamps, sources and cumulative
download/storage counters remain intact; the limits remain 5 GiB response-body
downloads, 8 GiB logical artifacts and a 32 GiB filesystem free-space floor.

The first run stopped at 03:53 PST after transient request failures consumed
the attempted candidate list. It retried requests twice, two seconds apart,
then skipped the paper. That was inadequate for a sustained outage. The
candidate_pool_exhausted label did not establish a shortage of eligible papers.

The current environment supplies a socks5h proxy. The old urllib client failed
to retrieve a PMC S3 metadata listing; the SOCKS-compatible client retrieved
the same listing and the official PMC reuse policy successfully. The HTTPS
bridge now uses the already-installed requests[socks], with TLS verification
and streaming byte limits intact. This establishes the current compatibility
problem; it does not prove what caused each earlier connection-refused event.

The worker now waits 30, 60, 120, 240, then at most 300 seconds between failed
logical request attempts, retrying the same source object. It checks the stop
file and resource/deadline limits during waits. A persistent outage beyond
the 30-minute request recovery budget stops the batch with network_unavailable.
Non-retryable HTTP responses, such as missing objects, remain explicit source
rejections. The completed 295 papers are skipped on resume.

Fifteen regression tests passed, including outage recovery, persistent outage
status, unchanged byte counters and fixed continuation deadlines. Connectivity
checks are recorded in [resumption_checks.json](resumption_checks.json).

This expansion parses publisher JATS XML for article text, full main-article
tables, citations, captions and explicit figure references. It retains original
PDFs and figure images from the official PMC distribution. It runs no new OCR,
model inference or training, and uses one document worker, two CPU threads and
zero GPUs. Earlier olmOCR experiments remain separately retained.

Paywall status, public reading access and text-mining permission are different.
The [PMC Open Access Subset policy](https://pmc.ncbi.nlm.nih.gov/tools/openftlist/)
explains that not every publicly readable PMC article permits automated text
mining and reuse. This batch selects open-access records with a PDF candidate
flag and verifies actual distributed PDF/XML objects and figure assets. OCR
requires an already accessible PDF or image; it cannot unlock a paywall.

The [October 13 inventory](../pmc_cns_availability_2026-10-13/availability.csv)
found **490,354 OA-plus-PDF metadata candidates** across the explicitly selected
55 related titles, or **187,791 excluding Scientific Reports**. Those are
metadata candidates, not verified downloads or a biology-only research count.
They do not measure the number of inaccessible or paywalled papers. We have
not performed a complete publisher-versus-access census.
