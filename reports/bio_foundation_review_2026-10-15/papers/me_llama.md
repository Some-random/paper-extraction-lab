# Me-LLaMA

[Shared literature catalog](../README.md)

Biomedical and clinical text

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

Historical medical context. Clinical-note acquisition is outside the biological research corpus scope.

## Token counts by acquisition route

| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |
|---|---|---:|---:|---:|---:|---|
| [Me-LLaMA](#token-counts-by-acquisition-route)<br>CPT | Corpus · text | 0 | 0 | 129B | 129B | [Methods](https://www.nature.com/articles/s41746-025-01533-1) |

**CPT — Corpus (text):** The published recipe imports Pile biomedical text, MIMIC clinical datasets and RedPajama general text. The entire 129B mixture is therefore reused-dataset material under the acquisition-route definition; its content is mixed.

- **Online Papers: 0.** Literature is imported from The Pile rather than separately counted as direct acquisition.

- **Web Urls: 0.** General content arrives through RedPajama rather than a newly reported crawl.

- **Existing Datasets: 129B.** Pile + MIMIC + RedPajama combined corpus.

- **Total: 129B.** Published pretraining dataset total.

**Training stage:** CPT, general medical SFT, optional task SFT

**Backbone:** Llama-2 13B/70B

**Source material and units:** 129B-token mixture: Pile biomedical articles/abstracts, deidentified MIMIC-III/IV/CXR notes, and RedPajama general text.

**Acquisition and document processing:** Inherits Pile text; no new paper OCR engine is established by the model methods.

**Cleaning and filtering:** Domain selection and use of deidentified clinical sources; article extraction details largely inherited from upstream datasets.

**Training unit and mixture:** BIOMEDICAL:CLINICAL:GENERAL = 15:1:4; one CPT epoch.

**Generated or augmented material:** 214,595 SFT samples combine literature, notes, guidelines, knowledge graphs and general instructions; distinct from the raw CPT mixture.

**Author-reported evidence:** Tests six task types over 12 datasets and ablates CPT versus instruction tuning; instruction tuning is often the stronger immediate zero-shot intervention.

**Disclosure gaps:** Clinical data and checkpoints have access agreements. This is not an unrestricted public biology-only corpus.

**Source sections:** Methods: Mixed continual pre-training dataset; model development; Data availability

## Source details and qualifications

**Me-LLaMA:** Mixes biomedical literature, credentialed-access MIMIC clinical notes and general-domain replay at 15:1:4 for CPT. Its instruction tuning is a separate stage. [Methods](https://www.nature.com/articles/s41746-025-01533-1)

## Primary sources

- [Published Me-LLaMA report](https://www.nature.com/articles/s41746-025-01533-1)
- [Earlier primary preprint](https://arxiv.org/abs/2402.12749)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.
