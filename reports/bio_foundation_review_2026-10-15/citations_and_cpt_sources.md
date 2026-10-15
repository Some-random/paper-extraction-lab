# Citations to earlier papers and sources for continued pretraining

Source review and read-only audit, October 14, 2026, fixed PST (UTC−8). This adds documentation and diagnostic counts; it does not implement citation-aware training or change the existing extraction outputs.

**Our current citation handling is incomplete.** Inline literature citation markers survive in the retained prose, while bibliography entries are excluded from the main training chunks. The pipeline currently exports explicit figure/table links, but does not export structured links from inline literature citations to cited-paper identifiers. A citation in a paragraph does not automatically download the cited paper or expose its contents to the model.

**What the three current samples contain**

| Citing paper | Source bibliography entries | Inline bibliography-marker XML elements, all regions |
|---|---:|---:|
| [PMC13651886: OTULIN/Wnt](../pmc_native_v3_preview_2026-10-15/papers/PMC13651886/article.md) | 49 | 92 |
| [PMC13655163: Scottish proteomics](../pmc_native_v3_preview_2026-10-15/papers/PMC13655163/article.md) | 82 | 120 |
| [PMC13645648: Lsp2/diet/lifespan](../pmc_native_v3_preview_2026-10-15/papers/PMC13645648/article.md) | 80 | 110 |
| Total | **211** | **322** |

These count per-document entries and XML marker elements, not unique cited works. A marker can refer to several bibliography entries; these totals include captions and other regions outside retained research prose. In this source audit, every explicitly listed bibliography `rid` had a matching document-local reference record. That checks internal XML linkage, not external paper identity or whether the reference supports the surrounding claim.

The 211 bibliography records remain in original XML and as excluded reference blocks in the structured exports. Some flattened reference blocks duplicate alternative citation representations; they are not a clean normalized bibliography. The previously reported **179 reference edges are figure/table edges only**. See the [machine-readable audit with source hashes](citation_audit.json), [parser](../../src/native_training.py), and [example structured export](../pmc_native_v3_preview_2026-10-15/papers/PMC13651886/extracted.json).

For a concrete example, OTULIN's source XML already provides this relationship:

```text
PMC13651886: inline marker 1
  → document-local ref R1
  → Hsu and Fuchs, Building and maintaining the skin (2022)
  → DOI 10.1101/cshperspect.a040840
  → PMID 34607830; PMCID PMC8977401
```

This information can be parsed directly. The source JATS `xref` links to an internal `ref` record; the record can carry external identifiers. It does not itself contain the cited paper's full text. [NLM JATS specification](https://jats.nlm.nih.gov/archiving/tag-library/1.4/element/xref.html)

**Published models make different choices**

| Model and stage | Reported treatment |
|---|---|
| MEDITRON, decoder CPT | Omits the bibliography from the training body but replaces inline citations with the cited title, capped at 12 words, plus first-author surname inside `[bib_ref]` tags. This is metadata substitution, not a generated scientific summary. [§2.2 and Appendix B.2.1](https://arxiv.org/html/2311.16079v1) |
| PharMolix BioMedGPT-LM, decoder CPT | Removes reference citations, author information and chart data before sentence-based chunking. [§3.1](https://arxiv.org/html/2308.09442v2) |
| PMC-LLaMA, CPT textbook branch | Removes references and citations during textbook cleaning. The report does not establish that this same policy was applied to its entire paper corpus. [Dataset-I: Books](https://arxiv.org/html/2304.14454v3) |
| Galactica, scientific decoder pretraining from scratch | Represents citations with titles and author surnames between `[START_REF]` and `[END_REF]`. Reports better citation prediction with titles than IDs, alongside hallucination tradeoffs. This is a citation-representation precedent, not a CPT experiment. [§3.1.2](https://arxiv.org/pdf/2211.09085) |
| BioLinkBERT, encoder pretraining | Packs linked PubMed documents together and learns masked-token and document-relation objectives using citation links. This explicitly exploits cross-document relationships; it is not an ordinary decoder CPT recipe. [LinkBERT paper](https://aclanthology.org/2022.acl-long.551/) |

There is no universal published policy, and these studies do not establish a single best policy for our corpus. A model can learn citation-shaped text without retrieving evidence or verifying claims. Training on a citation context and title is also different from training on the cited full paper.

**PDF extraction, crawling and existing datasets describe different layers**

- PDF is an input format requiring extraction. Native XML, HTML, LaTeX and plain text are other formats.
- Crawling is one acquisition route. Bulk archives, database exports, APIs, direct downloads and private collections are other routes.
- An existing dataset is a packaging/provenance choice. It may already contain crawled HTML, extracted PDFs, XML-derived text, database records or synthetic examples.

For example, one paper could be downloaded as a PDF, extracted upstream into S2ORC, and then acquired by us as an existing dataset. These are overlapping descriptions of the same material. Our PMC native branch downloads XML and parses its structure directly; it does not require OCR.

Useful content categories for a CPT inventory are authored documents; web discussions/documentation/code; structured biological records and observations; clinical or other controlled-access records; and generated data. Track original origin, delivered format, acquisition route and transformations separately. General-domain replay is a role in the mixture, not an additional content origin.

**Concrete CPT recipes show the wider range**

- **OLMo 3:** Its roughly 100B-token midtraining mix contains 4.99B PDF-derived tokens, 27.39B web tokens, 10B StackEdu code tokens and substantial synthetic math, code, QA and reasoning data. Synthetic material is therefore used before the separate SFT/RL stages. [§3.5, Table 5](https://arxiv.org/html/2512.13961v2)
- **BioMatrix:** Continues Qwen3 on 304.4B tokens spanning literature/web text, PubChem records, protein sequences and structures, interactions and interleaved text/entities. It includes GPT-generated MolTextNet descriptions and computational structures as well as experimental PDB structures. Its TrEMBL branch explicitly removes literature citations and evidence codes. These provenance differences should remain visible in a scientific corpus. [§3.1–3.2](https://arxiv.org/html/2606.22138v1)
- **Me-LLaMA:** Mixes biomedical literature, credentialed-access MIMIC clinical notes and general-domain replay at 15:1:4 for CPT. Its instruction tuning is a separate stage. [Methods](https://www.nature.com/articles/s41746-025-01533-1)
- **PMC-LLaMA:** Samples textbook, paper and general-domain tokens at 15:4:1 for knowledge-injection CPT. Its UMLS prompts and generated QA explanations belong to the later instruction stage. [Dataset-I and Dataset-II](https://arxiv.org/html/2304.14454v3)

The download format does not determine the training stage. A synthetic QA example can be serialized as text for full-sequence next-token training, or used as an instruction/response pair with an answer-only loss. Report the actual objective, masking and mixture rather than inferring the stage from whether examples look like questions.

**Recommended next change for this project, not yet implemented**

Preserve a structured bibliography with document-scoped IDs, raw reference text, available title/author/year and DOI/PMID/PMCID. Export citation mentions with paragraph/XPath provenance and their target records; keep unresolved targets explicit. Prefer publisher identifiers over guessed title matches. The same work can appear as XML, PDF, abstract, preprint or dataset copy, so deduplicate by identity and text while retaining version information.

Build selectable training views from that retained structure: a clean prose view with markers removed and a self-contained view replacing markers with short cited titles/authors. The original-marker view remains available for comparison. Metadata preservation is useful even if one training view omits it. Compare training utility under equal token/compute budgets before choosing a citation policy; none of those training comparisons has been run here.

Only join cited full texts that are available within the chosen corpus/download budget. Recursive citation following can rapidly expand the corpus. Treat a citation as an attribution link, not an adjudicated support relation; a reference may be background, a method, a criticism or a conflicting result. Retrieval of source passages and verification of claim support require additional work beyond ordinary CPT.
