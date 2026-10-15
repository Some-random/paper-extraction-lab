# PMC-InterCPT / Beyond Captions

[Biological pretraining review](../README.md)

Multimodal CPT curation study

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training approach:** Continued pretraining. **Starting checkpoint:** Qwen3.5-2B / 4B-Base. [Initialization evidence](https://arxiv.org/html/2606.01049v2)

Paper/figure curation study with a fixed downstream SFT stage. Its empirical target includes medical tasks; its clinical evidence priorities are not the biological research collection policy.

## Token counts by acquisition route

| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [PMC-InterCPT / Beyond Captions](#token-counts-by-acquisition-route)<br>Context-grounded CPT | Resampled corpus · text + image | NR | NR | NR | 9.63B | [Tables 1, 8–9](https://arxiv.org/html/2606.01049v2) |

**Context-grounded CPT — Resampled corpus (text + image):** The 9.63B total combines text and image tokens after resampling. Existing BIOMEDICA material is repaired with article-native context; the contribution of direct XML versus imported material is not separately tokenized in the paper.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: 9.63B.** Combined text-and-image token count; not 9.63B text tokens.

**Training stage:** CPT with a fixed downstream SFT stage

**Backbone:** Qwen3.5-2B / 4B-Base

**Source material and units:** PMC/BIOMEDICA figures, captions and article-native context; final 9.63B-token corpus.

**Acquisition and document processing:** Recover captions from PMC XML and attach body text only through article-native figure references.

**Cleaning and filtering:** Repair disconnected context, deduplicate text, prune unsupported non-primary images; Gemini labels relevance/quality, distilled Qwen3-1.7B classifiers filter; benchmark decontamination.

**Training unit and mixture:** Interleaved image-caption-context sequences; final evidence-token allocation 45% biomedical visuals, 30% quantitative evidence, 20% mechanistic structure, 5% auxiliary context.

**Generated or augmented material:** Source reconstruction rather than invented replacement captions. Quality annotators see text, not images; do not treat labels as image-grounding judgments.

**Author-reported evidence:** Token-matched raw-data control plus identical SFT: +1.46 medical-average and +3.11 general/scientific-average points on Qwen3.5-4B.

**Disclosure gaps:** Preprint findings, not independently reproduced here. Reported gains compare to raw CPT; versus SFT-only, general/scientific improvement is only +0.07 points.

**Source sections:** Method; Tables 1-2; Appendix B-C

## Datasets and amounts

[PMC-InterCPT](https://arxiv.org/html/2606.01049v2), Tables 8/9

| Reported field | Retained source statement |
|---|---|
| Literature-derived amount | **9.63B combined text + image tokens** after resampling |
| Treatment of figure content | Final token mixture: biomedical visual evidence **4.33B (45%)**; quantitative/table **2.89B (30%)**; mechanism/structure **1.93B (20%)**; auxiliary **0.48B (5%)** |

## Figure handling

[PMC-InterCPT](https://arxiv.org/html/2606.01049v2)

| Reported field | Retained source statement |
|---|---|
| Pixels used in training? | Yes |
| Source captions / generated material | Recovers missing captions from XML and interleaves figures with explicitly referring article passages. Text classifiers filter quality/relevance; the method explicitly prefers source-caption recovery to replacement generation |

## Source details and qualifications

PMC-InterCPT's **15.41B-token pre-sampling pool** has **7.18B text / 8.23B image tokens**. That split must not be applied unchanged to its differently resampled 9.63B final corpus. It recovers author captions from XML and attaches explicitly referring context. Its Gemini/Qwen quality classifiers label text; they do not produce replacement figure captions. [PMC-InterCPT, Source-Grounded Recovery, Quality Classification, Tables 8/9](https://arxiv.org/html/2606.01049v2)

## Primary sources

- [Beyond Captions v2](https://arxiv.org/html/2606.01049v2)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
