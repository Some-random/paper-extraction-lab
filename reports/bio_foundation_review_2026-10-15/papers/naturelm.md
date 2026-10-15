# NatureLM

[Shared literature catalog](../README.md)

Biological and scientific multimodal foundation

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Scientific decoder continued pretraining for larger variants

**Source material and units:** Literature, database descriptions, small molecules, proteins, DNA/RNA and cross-domain pairs

**Acquisition and document processing:** Approximately 143B mixed tokens; BERN2 links literature mentions to molecular/protein representations. Structured sequence data is a major part of the corpus. Exact PDF-conversion settings are not disclosed.

## Source material

[NatureLM](https://arxiv.org/html/2502.07527v2)

| Reported field | Retained source statement |
|---|---|
| Stage | Scientific decoder CPT for its larger models |
| Actual biological source material | Literature, database descriptions, small molecules, proteins, DNA/RNA and cross-domain pairs |
| How the source becomes training data / relevant limitation | Approximately 143B mixed tokens; BERN2 links literature mentions to molecular/protein representations. Structured sequence data is a major part of the corpus. Exact PDF-conversion settings are not disclosed. |

## Datasets and amounts

[NatureLM](https://arxiv.org/html/2502.07527v2), science CPT of the 8B / 8×7B models, §2, Tables 1/S1

| Reported field | Retained source statement |
|---|---|
| Paper or abstract text | **4.0B literature-derived interleaved tokens**, already included in 12.7B cross-domain; further literature may occur in the text bucket |
| Web-origin text | Paper-versus-web split of the **14.4B text** bucket is NR |
| Other data in this stage | Molecules **4.2B**, proteins **65.2B**, DNA **19.8B**, RNA **27.5B**, materials **0.02B**, cross-domain **12.7B** |
| Reported total and disclosure limit | **143.8B corpus tokens** in Table S1; rounded components sum to 143.82B. Not 143.8B paper text |

## Figure handling

[NatureLM](https://arxiv.org/html/2502.07527v2) / [BioMatrix](https://arxiv.org/pdf/2606.22138v1)

| Reported field | Retained source statement |
|---|---|
| Pixels used in training? | Their disclosed biological modalities are sequences / structures / text |
| Source captions / generated material | “Multimodal” here does not establish paper-figure training. Molecule/protein “captioning” can mean generating a biological description from a molecular/protein representation |

## Source details and qualifications

NatureLM's 12.7B cross-domain bucket consists of interleaved literature **4.0B**, text–SMILES **3.0B**, text–protein **1.4B**, text–material **0.2B**, and DNA–protein **4.1B**. Do not add these to the 143.8B total again. Its 1B model first receives **300B SlimPajama text tokens**; that is a separate initialization phase. Later instruction tuning uses **5.1M pairs**, not an additional reported CPT token budget. [NatureLM, §2 and Tables 1/S1](https://arxiv.org/html/2502.07527v2)

## Primary sources

- [Primary source retained from the existing review](https://arxiv.org/html/2502.07527v2)
- [Primary source retained from the existing review](https://arxiv.org/pdf/2606.22138v1)

## Related evaluation notes

- [Evaluation project: published comparisons and native-protocol requirements](https://github.com/Some-random/bio-evaluation/blob/main/reports/PUBLISHED_BENCHMARK_COMPARISONS_2026-10-15.md)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
