# NatureLM

[Biological pretraining review](../README.md)

Biological and scientific multimodal foundation

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Continued pretraining. **Starting checkpoint:** Llama 3 8B / Mixtral 8×7B. [Initialization evidence](https://arxiv.org/html/2502.07527v2#S2.SS3)

The 8B and 8×7B models continue from existing checkpoints. The separate 1B model first trains on 300B SlimPajama text tokens, then receives scientific training; it is not trained on biology alone from its first step.

**Data included in the overview amounts:** Biology, chemistry, materials + general text. The complete 143.8B corpus is not biology-only. It includes 14.4B general text, several scientific modalities and cross-domain data; the existing-dataset lower bound also includes nonbiological materials.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [NatureLM](#token-counts-by-acquisition-route)<br>8B / 8×7B scientific CPT | Corpus · text + scientific sequences | NR | NR | ≥116.72B | 143.8B | [§2 / Table S1](https://arxiv.org/html/2502.07527v2) |

**8B / 8×7B scientific CPT — Corpus (text + scientific sequences):** Table S1 is a 143.8B scientific corpus, not a paper-only budget. Separate molecule/protein/DNA/RNA/material source datasets establish a reused-data lower bound. The 14.4B general-text and 12.7B interleaved buckets are not assigned to a route without evidence. The 4.0B interleaved-literature count is not assumed to be directly acquired paper tokens.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: ≥116.72B.** Known molecule, protein, DNA, RNA and materials components only. Calculation: (4.2 + 65.2 + 19.8 + 27.5 + 0.02) × 1000000000.

- **Total: 143.8B.** Published Table S1 total; component rounding differs by 0.02B.

**Training stage:** Scientific decoder continued pretraining for larger variants

**Backbone:** Llama 3 8B / Mixtral 8×7B

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

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
