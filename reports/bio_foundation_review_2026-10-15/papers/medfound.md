# MedFound

[Shared literature catalog](../README.md)

Clinical generalist

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

Historical medical context. Clinical-note acquisition is outside the biological research corpus scope.

## Token counts by acquisition route

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [MedFound](#token-counts-by-acquisition-route)<br>Medical pretraining, diagnostic SFT, preference alignment | Not reported · text | NR | NR | NR | NR | [Paper](https://www.nature.com/articles/s41591-024-03416-6) |

**Medical pretraining, diagnostic SFT, preference alignment — Not reported (text):** Available source notes do not establish a source-category token split. Clinical/private material is not silently assigned to a public acquisition route.

- **Online Papers: NR.** No separate direct-paper token amount is established for this row.

- **Web Urls: NR.** No separate directly collected webpage token amount is established for this row.

- **Existing Datasets: NR.** No separate reused-dataset token amount is established for this row.

- **Total: NR.** A tokenizer-token total is not established for this row.

**Training stage:** Medical pretraining, diagnostic SFT, preference alignment

**Backbone:** Released 7B and 176B variants

**Source material and units:** Medical text and real-world clinical records.

**Acquisition and document processing:** A specific full-paper PDF/OCR route was not verified in the accessible material.

**Cleaning and filtering:** Corpus engineering details should be checked in the complete methods/supplement before adopting them.

**Training unit and mixture:** Medical corpus pretraining followed by diagnosis-focused training; not equivalent to a pure research-literature CPT recipe.

**Generated or augmented material:** Self-bootstrapped diagnostic chain-of-thought and preference alignment are explicitly described at the program level.

**Author-reported evidence:** Clinical diagnosis, external and rare-disease evaluation, and physician comparisons.

**Disclosure gaps:** Limited methods access in this review; do not infer cleaning thresholds, exact corpus counts or extraction software. Clinical records limit full data reproducibility.

**Source sections:** Abstract; accessible code/data availability; official repository

## Primary sources

- [Published MedFound paper](https://www.nature.com/articles/s41591-024-03416-6)
- [Author repository](https://github.com/medfound/medfound)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
