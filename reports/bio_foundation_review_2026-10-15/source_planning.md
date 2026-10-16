# Corpus totals and counting assumptions

[Literature catalog](README.md) · [Complete source inventory](source_inventory.md)

## Quantified candidate subtotal

| Component | Candidate token equivalents |
|:---|---:|
| Paper text | 74.6–217.6B |
| Biology web text | 85.7B |
| Biological database records | 37.0B |
| **Subtotal with quantitative support** | **197.4–340.4B** |
| Additional unique contributions from the remaining sources | **Unmeasured** |
| **Complete, deduplicated biological-corpus total** | **Not established** |

The complete source inventory covers **87 source families** from the non-archived biological studies and source corpora in the review, plus the documented upstream inputs of TheBioCollection and OpenGenome2. Alias names, repackaged corpora and parent datasets are consolidated. Source coverage is complete for these named inputs; quantitative coverage is not complete. We do not interpret unmeasured contributions as zero.

## Calculation

**Paper text:** the [PMC text-mining inventory](../pmc_global_availability_2026-10-14.json) contains 9,324,889 metadata candidates. Assuming 8,000–23,334 tokens per candidate gives **74,599,112,000–217,586,959,926 tokens**. These per-paper lengths are planning assumptions, not a representative measured distribution. The high figure equals the mean in a 454-paper journal-balanced, length-capped local sample. The result includes candidate material that could be rejected by biological-scope filtering.

**Web text:** [FineFineWeb biology](https://huggingface.co/datasets/m-a-p/FineFineWeb) reports 86.99B source-tokenizer tokens. Multiplying by the measured convenience-probe conversion of 0.98566284 gives approximately **85.7B local-tokenizer tokens** before our additional selection and deduplication. No 15% retention assumption is applied.

**Database records:** [TheBioCollection free-text stream](https://huggingface.co/datasets/trillionlabs/TheBioCollection) reports 33.8B source-tokenizer tokens. Multiplying by the convenience-probe conversion of 1.09571455 gives approximately **37.0B local-tokenizer tokens**. This counts the released bundle once. It includes descriptions, annotations, molecular representations and sequences; it is not annotation-only prose. The separate instruction stream is excluded.

Adding those three components gives **197.4–340.4B candidate token equivalents**. This arithmetic is reproducible, but it is not a full-corpus measurement and does not establish a biology-only unique total.

## Treatment of all other sources

- **Overlapping literature:** PubMed abstracts, bioRxiv, medRxiv, arXiv, ChemRxiv, OSF, PubAg, S2ORC, peS2o, The Pile PubMed components, BIOMEDICA and the OLMo PDF collection are all registered. Their genuinely new biological content relative to the counted paper component has not been measured. Their full published budgets are not added wholesale.
- **Underlying biological databases:** every named input in the reviewed papers and TheBioCollection source table is registered. A source contributing to TheBioCollection is not necessarily fully represented there. Its incremental records remain unmeasured, rather than being assigned either zero or its complete raw-export size.
- **Task and paired-data collections:** the register includes BioT5, ProtST, BioReason, BioReason-Pro, Tx-LLM/TxGemma, UniGenX and STRIDE inputs. Instruction examples, repeated training exposure and test sets are not counted as fresh CPT corpus tokens.
- **General replay and other sciences:** C4, Wikipedia, FineWeb-Edu, DCLM and other mixed-domain inputs are listed separately. Their full nonbiological amounts are excluded from the biological total.

The [complete source table](source_inventory.md) provides a row for every consolidated family, its referring studies, evidence and counting treatment.

## Raw sequences and structures

Raw biological representations remain a secondary collection priority. [OpenGenome2](https://huggingface.co/datasets/arcinstitute/opengenome2) reports **8.8T nucleotide positions**, while other raw protein and structure contributions are not yet harmonized. Its component genome collections are not added again. Nucleotide positions, amino-acid residues, structures and text-token counts are distinct units; the 8.8T is not added to the text/record subtotal.

## Storage

Token IDs require **373GiB per 100B tokens**, or **3.64TiB per 1T tokens**, with uint32 storage. The 197.4–340.4B quantified candidate subtotal corresponds to approximately **0.72–1.24TiB of token IDs alone**. Canonical text, original files, metadata, indexes and temporary files are additional.

Preserving paper PDFs and figures adds approximately **7.2TiB per million retained papers**, extrapolating from the measured 454-paper sample. This is a storage scaling estimate, not a biological retention estimate. Separate supplements, model weights and training files are outside these data estimates.

## Reproducibility

[Machine-readable source register and arithmetic](starter_corpus_estimate.json) · [Tokenizer-probe counts and hashes](starter_corpus_probe.json)

Run `scripts/estimate_starter_budget.py`, then `scripts/render_foundation_catalog.py`. The first script builds the complete source register from the review and the documented bundled inputs, rejects unmapped source names, and computes the subtotal from distinct components. Old subset scenarios remain only as explicitly superseded provenance in the calculation record.
