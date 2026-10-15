**How to obtain biological web text**

There are three practical routes. For this storage-limited project, start with small selections from existing corpora and use a focused crawl to fill specific gaps. These are acquisition instructions; only the [64KiB FineFineWeb probe](web_sample.md) was executed in this update.

| Route | How we obtain the URLs/text | Useful when |
|---|---|---|
| Reuse a processed web corpus | Download/stream selected shards; retain each record's original URL and crawl metadata | We need scale without recrawling and reparsing the web |
| Reuse archived HTML | Query Common Crawl's URL index for chosen hosts/paths; retrieve selected WARC records and parse HTML | Existing processed text lost needed structure, or we need our own extraction/filtering |
| Crawl selected live sites | Start from sitemaps, RSS, API/export listings and curated seed URLs; follow only approved domains/paths | We need recent or specialist material absent from the corpus |

**Existing biological web data**

[FineFineWeb's author card](https://huggingface.co/datasets/m-a-p/FineFineWeb) lists **86.99B biology tokens / 83,759,301 records**, and **28.52B chemistry tokens / 33,015,312 records**. These are dataset-wide reported counts, not the amount BioMatrix selected. The card does not identify the counting tokenizer. Its files are partitioned by domain; at inspected revision `7fd92dc825a75cbff271a5a52eea0eda91a2c112`, biology has 864 JSONL shards. Records contain text, original URL, crawl date, Common Crawl archive path, language score, existing token count and a corpus ID.

The actual probe found a publisher abstract, a protocol keyword aggregation, consumer-health material, commercial pages and a blog in just eight biology-labeled records. Therefore a biology topic label or language score is not a research-quality filter. Keep source-type selection and text-quality assessment separate from topic classification. [Probe, complete metadata and manual dispositions](web_sample.md)

[FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) is another processed Common Crawl source, useful for general educational replay. [Dolma](https://arxiv.org/html/2402.00159) mixes several origins; an appropriate biological academic/web selection may be domain data, not merely replay. [peS2o](https://github.com/allenai/pes2o) supplies cleaned academic text. The same PMC article can occur in multiple datasets, so deduplicate by DOI/PMCID and normalized content rather than adding their headline sizes.

For JSONL shards, an HTTP byte-range probe is a cheap way to inspect a file. It is a **prefix**, not a random sample. The provided [sample script](../../scripts/sample_biology_web.py) requests a hard-bounded range, requires HTTP 206, preserves raw bytes and parses only complete records. It does not download the full ~511MB first biology shard. Later, select and process a bounded number of full shards or stream with a chosen document/byte budget; streaming still transfers bytes and consumes some buffers. [Hugging Face streaming documentation](https://huggingface.co/docs/datasets/stream)

**Archived HTML without a new crawl**

Common Crawl stores original responses in **WARC**, metadata in **WAT**, and extracted plain text in **WET**. Its [URL index](https://index.commoncrawl.org/) accepts host/path patterns. Select a crawl snapshot, query a specific domain/path, filter successful HTML responses, and use the returned filename, offset and length to retrieve the matching WARC record with an HTTP `Range` request. Decompress/parse that record, then run our HTML extractor. This is different from fetching the source site live. Do not fetch an entire multi-gigabyte archive to read a few pages. For large multi-domain selection use the columnar index rather than hammering the URL lookup endpoint. [Official access and format guide](https://commoncrawl.org/get-started)

**A focused live crawler**

For our first crawl I would use **one serial fetcher**, a site/path allowlist, explicit document/byte limits, and a saved frontier. Source discovery can use a site's `robots.txt` sitemap declarations, sitemap indexes, RSS/Atom feeds, collections, database export/API records and links already present in retained literature. A DOI resolves a paper; it is not permission or a guarantee of downloadable full text.

Use [Scrapy](https://docs.scrapy.org/en/latest/topics/settings.html) for the crawl queue, retry/backoff, rate limits and response handling; [Trafilatura](https://trafilatura.readthedocs.io/en/latest/crawls.html) for URL discovery and main-text extraction. A sensible initial Scrapy configuration is:

```python
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 2
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
DOWNLOAD_MAXSIZE = 2 * 1024 * 1024
```

These settings are illustrative, not a complete crawler or a global quota enforcement mechanism. The runner must separately count total response bytes and accepted documents, stop at the configured budget and persist its frontier. Honor longer site crawl delays and server backoff. Use a browser only for pages whose main content truly requires JavaScript; ordinary HTML acquisition and parsing need no GPU. [Scrapy settings](https://docs.scrapy.org/en/latest/topics/settings.html), [Trafilatura operation](https://trafilatura.readthedocs.io/en/latest/crawls.html)

For every fetched page, keep `url`, final URL, fetch time, status, content type, body hash, compressed raw HTML, extracted text, parser/version, source-type labels, license information when supplied and rejection reasons. Save source images/captions when needed. Remove menus and boilerplate while preserving headings, lists, tables, scientific notation and useful links. Run exact and near-duplicate detection, biological relevance and quality filters, then tokenize with the actual training backbone. Measure the tokens **after** these filters, and report rejected as well as retained amounts.

**PMC and biological databases have a better acquisition route**

For PMC papers, use the current official [PMC Article Datasets](https://pmc.ncbi.nlm.nih.gov/tools/textmining/) and cloud/API services; the existing pipeline already uses the current distribution. The old OA Web Service was retired in August 2026. Systematic crawling of PMC article HTML is not its supported retrieval route. XML, images and supplementary files provide more structure than generic web extraction. [Current PMC documentation](https://pmc.ncbi.nlm.nih.gov/tools/developers/)

Similarly, acquire UniProt/PubChem/PDB records through their official export/API routes when using their structured biological data. Do not scrape their rendered webpages merely because they have URLs. Web exposition, paper text and serialized database records should remain separate provenance classes even when all were transferred over HTTPS.
