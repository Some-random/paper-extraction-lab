# MMedLM / MMed-Llama 3

[Shared literature catalog](../README.md)

Multilingual medical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

Historical medical context. Clinical-note acquisition is outside the biological research corpus scope.

## Token counts by acquisition route

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [MMedLM / MMed-Llama 3](#token-counts-by-acquisition-route)<br>CPT | Corpus · text | NR | NR | NR | ≈25.5B | [Data construction](https://www.nature.com/articles/s41467-024-52417-z) |

**CPT — Corpus (text):** MMedC combines textbooks, websites and reused datasets. No route-specific token allocation is established. Books are not silently counted as papers or webpages.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: ≈25.5B.** MMedC corpus total; route split is not disclosed.

**Training stage:** CPT, then QA/rationale tuning

**Backbone:** InternLM, InternLM2, Llama 3 variants

**Source material and units:** MMedC: 25.5B corpus tokens in six languages from filtered general corpora, over 20K medical textbooks, medical websites, and existing medical text datasets.

**Acquisition and document processing:** Explicit PaddleOCR for textbook pages, retaining coordinates and ordering boxes left-to-right/top-to-bottom.

**Cleaning and filtering:** Remove cover, contents, and epilogue pages; select medical web/corpus sentences using medical keyword count and keyword-density thresholds.

**Training unit and mixture:** 2,048-token text chunks with 512-token overlap; next-token prediction. Corpus size and actual training budget must be distinguished.

**Generated or augmented material:** GPT-4 supplies QA rationales for MMedBench, followed by human verification; this is separate from textbook OCR.

**Author-reported evidence:** Multilingual QA, rationale, and corpus-component ablations; a small manual relevance check is not a broad OCR accuracy benchmark.

**Disclosure gaps:** Not all books and website content are redistributed; a book list is provided.

**Source sections:** Methods: corpus construction; Training details

## Primary sources

- [Published MMedLM paper](https://www.nature.com/articles/s41467-024-52417-z)
- [Author corpus card](https://huggingface.co/datasets/Henrychur/MMedC/blob/main/README.md)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
