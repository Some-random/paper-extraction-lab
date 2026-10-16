# Biological source inventory and collection priorities

[Literature catalog](README.md) · [Processing recipe](data_pipeline.md)

**The collection scope is the broader biological literature and its supporting databases. The earlier 50B scenario covered only a narrow subset and no longer serves as our overall estimate.** Prioritize research papers, biology web text and annotated database records. Group raw sequences and structures into one secondary pool for now.

## How large is the paper inventory?

| Inventory | Article records / candidates | Meaning |
|:---|---:|:---|
| [PMC archive](https://pmc.ncbi.nlm.nih.gov/) | **About 12.5M** | Current rounded archive total, checked October 16, 2026. Biomedical and life-science literature; not all records belong to the bulk text-mining subsets. |
| [Broader PMC text-mining inventory](../pmc_global_availability_2026-10-14.json) | **9,324,889** | October 14 metadata-query candidates from open-access and author-manuscript collections, excluding embargoes. Object availability and biological scope still need checking. |
| [Initial 55-journal subset](../pmc_cns_availability_2026-10-13/availability.json) | **552,024** | A selected subset of the above, not the total number of papers we can collect. |

These inventories are nested; do not add them. The planned scope is not capped at 55 journals. Research-biology selection will distinguish the material relevant to this project from clinical and other content.

Using the **full 9.32M-candidate inventory** gives the following gross-text scenarios:

| Assumed tokens per paper | Candidate text volume |
|---:|---:|
| 8,000 | **74.6B** |
| 12,000 | **111.9B** |
| 23,334 | **217.6B** |

These are input-volume scenarios before scope filtering and deduplication, not retained biology counts. The 23,334 figure is the mean of our 454-paper, journal-balanced and length-capped sample; it is not representative of the whole archive. The other lengths are assumptions. This supports planning around tens to hundreds of billions of candidate paper tokens, rather than extrapolating only the 552k subset.

Other paper collections can add coverage. [OLMo 3's PDF pool](https://arxiv.org/html/2512.13961v2#S3.SS4) reports **972B tokens across subjects**, and [S2ORC](https://aclanthology.org/2020.acl-main.447/) and [peS2o](https://github.com/allenai/pes2o) supply overlapping literature. Their incremental research-biology contribution is unmeasured. OLMo's released topic groups, such as Health and Science/Math/Technology, do not provide an exact biology-only total. The whole 972B cannot be assigned to biology.

## Web text and annotated database records

| Source | Published source amount | Local-tokenizer proxy, before our filtering/deduplication |
|:---|---:|---:|
| [FineFineWeb biology](https://huggingface.co/datasets/m-a-p/FineFineWeb) | **86.99B tokens** | **85.7B** |
| [TheBioCollection free-text stream](https://huggingface.co/datasets/trillionlabs/TheBioCollection) | **33.8B tokens** | **37.0B** |

The source amounts use different tokenizers. The local proxies use the pinned Qwen-family extraction tokenizer and small convenience-sample conversion ratios: 0.9857 for web text and 1.0957 for database records. Their combined proxy is about **122.8B tokens before our additional filtering and cross-source deduplication**. It is not a measured retained corpus.

The previous **15% research-retention assumption for FineFineWeb biology was unmeasured**. It has been retired from the current overview rather than replaced with another arbitrary percentage. Biology labels establish a candidate subject area; representative review must establish research relevance and quality. FineFineWeb already applies upstream exact/MinHash deduplication, so our additional removal should account for that.

The 86.99B figure is one released biology-labelled collection, not a ceiling on all biological web text. The same source card lists **14.26B agronomy tokens** and **28.52B chemistry tokens** as additional candidate slices; their relevant biological portions and overlap still need measurement. We do not count those whole slices as biology automatically.

TheBioCollection contains records from UniProt, PubChem and other biological databases: descriptions and annotations linked to sequences, molecular representations and other fields. Its free-text stream is separate from its instruction stream. **The full 33.8B is not annotation-only text or pure sequence.** Prioritizing it means retaining the useful linked records, not relabelling all its tokens as prose.

## Raw sequences and structures: grouped, secondary priority

Group standalone genomic, protein and structure exports under **raw biological representations** for collection planning. For example, [OpenGenome2](https://huggingface.co/datasets/arcinstitute/opengenome2) contains approximately **8.8T biological nucleotide positions**, available as FASTA and processed JSONL. Protein and structure resources such as UniRef and PDB belong to this group when imported without accompanying descriptive records.

Keep native sequence/residue/structure units in provenance, but do not invent a combined language-model-token total from incompatible units. OpenGenome2's biological content can support a very large sequence corpus; it does not establish an equally large biological-prose corpus. Sequence windows and different representations can overlap.

**This is our project priority, not a claim that raw sequences are inherently less valuable.** For the immediate text-based CPT objective, papers and annotated records directly provide mechanisms, functions, experimental observations and entity-to-description links. The effect of adding more raw sequence is a training-mixture question. We retain the option to use it later.

The same source can contribute to both forms: an annotated UniProt record can contain a protein sequence. Its sequence does not become extra corpus material just because it is also available in a raw sequence export. Likewise, do not add the complete BioMatrix, NatureLM and SciReasoner training budgets; they reuse many underlying sources.

## Storage for the broader collection

Storage must follow the selected papers and token volume. The former **4TiB** allowance applied only to the small starter scenario; it is not a budget for the broader inventory.

| Storage component | Scaling basis |
|:---|:---|
| Token IDs | **373GiB per 100B tokens**, or **3.64TiB per 1T tokens**, using uint32 IDs. |
| Original paper PDFs and figures | Approximately **7.2TiB per million retained papers**, extrapolated from the measured 454-paper sample. |
| Canonical text, XML, metadata, indexes and temporary files | Additional to token IDs and paper assets; depends on representations, retention and which intermediate files are kept. |

If all 9.32M candidates had the sample's average PDF/figure footprint, those assets alone would occupy about **67TiB**. This is a whole-candidate-pool storage scenario, not a recommendation to download all papers or a measured biological-corpus size. Scope selection can reduce the number of retained papers substantially.

The currently inventoried downloads include **433.88GB** for FineFineWeb biology JSONL and **15.93GB compressed** for TheBioCollection free text. Serial shard processing avoids keeping all unfiltered input and every intermediate representation at once. Shared scratch had about **1.4TiB free on October 16, 2026 (PST)**. Separate supplements, model weights and training files are outside the text/source estimates above.

## Evidence and reproducibility

[Source counts and scenario calculations](starter_corpus_estimate.json) · [PMC homepage snapshot](pmc_archive_snapshot.json) · [Tokenizer-probe counts, versions and hashes](starter_corpus_probe.json)

The probe inspected 2,048 TheBioCollection records from prefixes of 32 shards and 108 FineFineWeb records from eight shard prefixes. These are convenience samples, not a probability sample or a measurement of whole-corpus duplicate rates. They calibrate tokenization only.

Run `scripts/estimate_starter_budget.py` to reproduce the arithmetic. Its old 35–70B subset scenarios remain explicitly marked as superseded for provenance; they do not determine the new overview. Final retained counts require biological-scope review, cross-source identity/content matching and tokenization over the selected records.
