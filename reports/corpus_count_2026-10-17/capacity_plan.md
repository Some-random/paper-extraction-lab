# Paper availability, storage and download plan

Checked October 18, 2026. **2,327 selected papers are already local. PMC currently
returns 9,339,471 text-mining candidates.** The latter includes clinical material
and other article types; the unique, usable biological-paper total across all
repositories remains unmeasured.

## Available text and records

| Collection | Available inventory | Full raw download | Candidate tokens in the counting tokenizer, estimated |
|:---|:---|---:|---:|
| PMC | 9.34M text-mining candidates | About 1.17 TiB of XML, using the new-paper sample | About 127B if every candidate had the sample's mean length |
| [FineFineWeb biology](https://huggingface.co/datasets/m-a-p/FineFineWeb) | 864 JSONL shards; publisher reports 86.99B tokens | **433.884 GB / 404.086 GiB**, exact pinned release | About **89.75B** |
| [TheBioCollection free-text](https://huggingface.co/datasets/trillionlabs/TheBioCollection) | 32 compressed shards; publisher reports 33.8B Gravity-tokenizer tokens | **15.931 GB / 14.837 GiB**, exact pinned release | About **36.99B** |
| **These three components** | Overlap and biological retention unresolved | Online releases alone: **449.815 GB / 418.923 GiB** | **About 254B in this planning scenario** |

The online token estimates multiply tokens per stored byte in completed pilot
shards by the exact release bytes: four web shards and three database shards.
These prefixes are not random samples. The 254B scenario adds those estimates
to a full-PMC extrapolation; it is not a measured unique biology corpus.
TheBioCollection includes descriptions, annotations, sequences and molecular
representations. Its separate instruction stream is outside this plan.

The [complete source inventory](../bio_foundation_review_2026-10-15/source_inventory.md)
covers all 87 named families, including 15 literature families. PubMed, bioRxiv,
medRxiv, arXiv, ChemRxiv, OSF, ACL Anthology, PubAg, S2ORC/Semantic Scholar,
peS2o, BIOMEDICA, OLMo science PDFs, Pile PubMed and USPTO patents are additional
or overlapping paper pools. Their unique biological contributions beyond PMC
have not been counted; their mixed-domain totals cannot simply be added.

## Storage to prepare training data

| Paper collection | XML + compressed parsed document + canonical text + uint32 token IDs | Working capacity allowance |
|:---|---:|---:|
| 100,000 papers | About **30 GiB** | About **40 GiB** |
| 1 million papers | About **301 GiB** | About **400 GiB** |
| All 9.34M PMC candidates | About **2.74 TiB** | About **3–4 TiB** |

These scenarios use the **1,873 newly selected papers**: 502,367,447 bytes of
native artifacts and 25,508,508 candidate tokens, averaging 268 KB and 13,619
tokens per paper. They exclude PDFs, figure binaries and supplements. The older
PDF-and-figure sample implied about **7.2 TiB per million papers**, or roughly
**67 TiB** for the full PMC candidate pool, before extracted training files.
Neither paper sample is representative of every PMC article.

For the **two online releases**, raw files plus one uint32 token-ID copy give
**449.8 GB + 507.0 GB = 956.8 GB**, before indexes and working space. Reserve
roughly **1.1–1.3 TiB** for that workflow. Stream compressed records during
processing rather than keep a second fully decompressed text copy.

Fully materializing both online releases plus the entire PMC text scenario therefore
calls for roughly **4–5 TiB of data storage**. Model weights and checkpoints
need their own capacity. Shared scratch had about **585 GiB free** at this check.

## Bounded storage alternative

**Use a proposed 200 GiB ceiling for this pipeline's data footprint.** This includes
the existing counted pilot, newly downloaded source copies, retained records,
indexes and all temporary files. Existing shared cluster inputs are read in place;
the plan does not duplicate or delete them. Historical experiments outside this
pipeline, environments and model caches are separate existing footprints.

| Allocation | Maximum |
|:---|---:|
| Preserved pilot and compact audit metadata | 32 GiB |
| Future raw staging cache | 16 GiB |
| Extraction and temporary/atomic output copies | 16 GiB |
| New catalog/deduplication indexes and sorting spill | 40 GiB |
| Retained compressed corpus, including original XML for retained papers | 80 GiB |
| Headroom | 16 GiB |
| **Total** | **200 GiB** |

Stream one source shard or bounded paper batch at a time. Decompress while
reading, tokenize in memory, and accumulate counts without saving every token
ID. A compact record catalog stores source/revision/shard/row, content hash,
token count and processing decisions. The pilot's verbose per-record SQLite
layout is not assumed to fit at full scale. Global deduplication signatures,
external sorting and concurrent output copies must fit their allocations too.

Before each bounded operation, reserve its worst-case writes against both the
category allocation and total ceiling, and maintain at least 64 GiB free on the
shared filesystem. Future run-owned disposable dataset staging files may leave
the cache only after source checksum, committed processing checkpoint and any
retained-output checks succeed. Preserve historical originals, shared files,
newly retained paper XML and final training shards. When an allocation fills,
pause; continuing requires space or a verified durable destination. No external
destination has been configured.

**Counting all candidates does not require holding their complete token-ID
array. Keeping the entire corpus locally does require enough durable storage.**
The 253.93B-token scenario would occupy **1.016 TB / 946 GiB in uint32 IDs alone**.
Neither the complete training pack nor every original PMC XML is claimed to fit
within 200 GiB. Under this ceiling, retain a selected corpus that fits, or consume
versioned source shards through a bounded stream. Completing a full preserved
paper archive would require a separate durable destination. Compression can
reduce retained text, but its size must be measured; no full-corpus compression
ratio is assumed.

The [machine-readable policy](../../config/corpus_storage_policy.json) records
these limits. It is a design for a new bounded runner, not an extension of the
expired pilot. The metadata reconciliation has run; no full download, deletion,
training or new long-running counting job has been launched.

## Estimation and acquisition

1. **Freeze the manifest.** For released datasets, sum exact file sizes and pin
   the revision/checksums. The existing counting configuration already does
   this for all 896 online shards. For papers, use the official PMC inventory
   and per-version metadata to select one usable version and its XML URL.
2. **Improve the estimate with dispersed samples.** Sample shards across each
   release and papers across topic/year/source groups; measure tokens, source
   bytes, retained bytes and overlap separately. Weight by the full inventory.
   Use held-out human scope/quality checks to estimate biological retention.
   Current prefix/selected-paper scenarios do not provide that retention rate.
3. **Download in stages.** Finish TheBioCollection free-text first, then process
   FineFineWeb biology shards and expand PMC XML in bounded batches. FineFineWeb
   already supplies page text and original URLs; a new crawl of every URL is
   unnecessary. XML-backed papers can be parsed without OCR. Keep source,
   version, license and hash provenance; deduplicate before training packing.
4. **Use measured retained counts for training storage.** Four-byte token IDs
   cost `retained_tokens × 4`; add raw inputs, indexes and scratch. The current
   counts do not establish scope/quality retention or cross-source near overlap.

[PMC distribution documentation](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/)
describes the current S3 inventory and per-article XML access. Individual files
replace the former baseline XML/TXT bundles. The inventory lists metadata
objects; XML size must be obtained separately or estimated from measured papers.

## Preview and start the online downloads

From the repository root, with `hf` installed in a project-local environment:

```bash
hf download trillionlabs/TheBioCollection \
  --repo-type dataset \
  --revision df09ee34ae7f9f00cc1290862f83fdb542f2ea35 \
  --include 'data/free_text_stream/*.jsonl.zst' \
  --local-dir inputs/training/biocollection \
  --max-workers 1 --dry-run

hf download m-a-p/FineFineWeb \
  --repo-type dataset \
  --revision 7fd92dc825a75cbff271a5a52eea0eda91a2c112 \
  --include 'biology/*.jsonl' \
  --local-dir inputs/training/finefineweb \
  --max-workers 1 --dry-run
```

`--dry-run` reports the files and download bytes. Removing it starts the selected
download. These commands select the full releases and do not impose the pilot's
expired storage/runtime limits; use a new bounded run for unattended acquisition.
Validate resulting bytes and SHA-256 against the frozen manifest before import.
The [official Hugging Face guide](https://huggingface.co/docs/huggingface_hub/en/guides/download)
documents pinned revisions, file filters, dry runs and resumable local folders.

[Measured inputs and calculations](capacity_plan.json).
