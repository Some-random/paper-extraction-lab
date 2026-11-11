# Protein mid-training: data and comparison

Updated November 11, 2026. The goal is to continue training Qwen3.5-4B on protein-related material and compare how different data mixtures affect its loss on held-out text.

## Overall source collections

Figures are from the November 2, 2026 snapshot. GB uses decimal units.

| Overall source collection | Available material | Average length |
|---|---|---:|
| **Swiss-Prot** | **575.7K** reviewed records; **0.942 GB compressed**. **574K** remain after exact-match exclusions. | **6.35K Qwen tokens per record**, measured across the 100K saved candidates. |
| **PMC papers** | **9.09M** paper texts; **390.5 GB**; **99.7B tokens**. Cleanup retained **8.52M** papers and set aside **551K** for review. | **11K tokens per paper** |
| **BioCollection** | **36.6M** selected records; **91.6 GB**; **36.5B tokens**. | **995 tokens per record** |
| **FineWeb-Edu** | **190.2M** pages processed; **11.8M** provisionally selected as biology; **40.2 GB**; **9.14B tokens**. | **775 tokens per selected page** |

The Swiss-Prot compressed size is for the full 575.7K-record snapshot; the size of the 574K subset has not been measured. Its token average is for the 100K saved candidates. The other averages are approximate, calculated from each source's reported total tokens and number of texts. The source workflows used different tokenizers, so the averages are not directly comparable to one another or to the Qwen-tokenized selection below.

## Selected source data

| Source | Material selected for the first comparison | Average selected record length |
|---|---|---:|
| **Swiss-Prot** | **10K** reviewed protein records, including sequences and annotations | **6.49K Qwen tokens** |
| **BioCollection** | **10K** biological database records | **1.10K Qwen tokens** |
| **PMC** | **10K** protein-related papers | **11.79K Qwen tokens** |
| **FineWeb-Edu** | **10K** provisionally selected protein-related web pages | **362 Qwen tokens** |

These averages describe the selected originals and use the Qwen3.5-4B tokenizer. The Swiss-Prot average counts the whole structured record, including annotations, markup and sequence; it is not the length of the sequence alone. BioCollection has 9,998 selected records, rounded to 10K.

The 10K per source was a starting target for the initial comparison, not the total available. Swiss-Prot selection stopped when it reached the target; it did not scan all of Swiss-Prot for this selection. Records were selected for relevant annotations and sequences, with exact matches to a held-out sequence set excluded.

## Comparison

- **Original text:** Two mixes are prepared. The equal mix assigns 25% of training tokens to each of the four sources. The other assigns 30% each to Swiss-Prot, BioCollection and PMC, and 10% to FineWeb-Edu. The two training jobs and the original-model loss evaluation are queued and can start automatically.
- **Rewrites:** Compare rewritten material with original material once the rewrite approach is agreed. Rewrite jobs are stopped. The model should see the protein sequence and be instructed not to change it.
- **Measurement:** Compare the original and trained Qwen3.5-4B models using next-token loss on text held out from training. The prepared data targets an 80% training, 10% validation and 10% test split, with related records grouped together when forming the splits.
- **Document length:** The queued original-text preparation splits records into chunks of at most 8,192 tokens. The broader choice of how to handle long papers and short records for mid-training remains to be discussed.
