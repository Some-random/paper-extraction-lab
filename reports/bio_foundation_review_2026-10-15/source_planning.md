# Biological source planning

[Shared literature catalog](README.md)

Generated training material often reformats source documents, database facts, problems or simulations. It is derived material and should not displace the original evidence. Reformatting a publisher table or serializing a database entry is also different from asking a model to invent an explanation. Keep observed measurements, curated annotations, computed predictions and teacher-written text distinct.

For this project, the practical source order is:

1. Existing publisher XML/text, original figures, complete article tables and supplementary spreadsheets, with PDFs as retained originals and the fallback extraction source.
2. Relevant text records from reusable scientific corpora, such as S2ORC/peS2o or academic/domain subsets of a Dolma release. Preserve corpus IDs, source/version, document scope and deduplication identity. Already-cleaned text need not pass through OCR again.
3. Biological database exports that fit the model's intended abilities: protein sequences/annotations, molecule descriptions and structures, experimental structures and binding/assay data. Link records to literature using supplied identifiers where available. Distinguish predicted structures and automated annotations from experimental observations.
4. Only later, optional generated representations derived from retained source material. No teacher synthesis or synthetic training batch was run in the current implementation.

The first stage is executed for the three papers and the bounded supplement sample. Full external corpora and biological databases have not been downloaded by this change; the current work does not claim that they are already ingested or deduplicated. The existing 50-paper inputs and earlier OCR outputs remain intact on RustFS.

[Executed verification](../pmc_native_v4_citations_2026-10-15/verification.json) checked all 25 image hashes, preservation of all 218 main-article source cells, intact citation spans within the token bound, and every exported spreadsheet row against a second read of its original workbook. Ten regression tests passed. Twelve date-typed source cells are flagged and preserved in ISO form, with no inferred gene-name correction. These are source-consistency checks, not biological correctness scores or training comparisons.

The literature supports several successful mixtures; it does not establish one best biological paper/web/database percentage. First measure our retained material with the eventual backbone tokenizer, and record both (a) content origin: literature, web exposition, database or generated derivative and (b) delivery: PMC, peS2o, Dolma/FineFineWeb or direct fetch. Deduplicate across delivery routes before counting. Keep available tokens, sampled training tokens and repeated exposures as separate totals.

Our current three-paper pipeline already preserves the real research text, source tables/spreadsheets and original figures with captions/context. It has not trained a model, synthesized figure descriptions, or ingested the full external corpora in this table. The next acquisition routes are described in [web acquisition](web_acquisition.md), with [an actual 64KiB corpus probe](web_sample.md); [figure handling](figure_handling.md) explains the training representations.
