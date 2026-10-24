# 10. Background controls, compartment references and dual localization

## Question

Split-TurboID was used to label proteins near contacts between the endoplasmic reticulum (ER) and mitochondria in human cells. Its fragments were attached separately to the ER membrane and the outer mitochondrial membrane. Nearby proteins were recovered for mass spectrometry. The authors used these sequential comparisons:

| Stage | Reference sample | Proteins retained in two independent +rapamycin replicates |
|---|---|---|
| Filter 1 | Split-TurboID with added biotin omitted | 607 and 619 |
| Filter 2 | Full-length TurboID in the cytosol, after filter 1 | 97 and 97 |
| Intersection of the filtered replicates | Both replicates | 67 |

Split-TurboID samples were labeled for four hours; full-length TurboID samples for one minute. These are enrichment comparisons under the published conditions, not equal-duration catalytic-rate measurements.

**Question:** What does the cytosolic-reference filter add, and what kind of genuine contact-associated protein could it exclude?

- **A.** It removes biotin-independent capture rather than cytosolic labeling; therefore a protein present in both contact sites and cytosol should always be retained.
- **B.** It favors contact-site labeling over cytosolic labeling; therefore a genuine contact-associated protein may be lost if it also labels strongly in the cytosol.
- **C.** It favors general cytosolic labeling over contact-site labeling; therefore abundant cytosolic proteins should become more prominent in the final contact-site list.
- **D.** It identifies direct binding between the two organelle membranes; therefore a retained protein is established as a physical tether that holds those membranes together.

## Answer

B is correct: the cytosolic-reference filter favors contact-site labeling over general cytosolic labeling, but can exclude genuine contact-associated proteins that also label strongly in the cytosol.

Reported observations: The no-added-biotin comparison retained 607 and 619 proteins. The subsequent cytosolic-reference comparison reduced these lists to 97 proteins each, with 67 shared between replicates. These numbers document progressively more selective enrichment and reproducibility criteria; they do not establish that every excluded protein was a false positive.

What each filter adds: TurboID biotinylates nearby accessible proteins, so recovery reflects proximity-dependent labeling as well as factors such as protein abundance and exposure to the enzyme. Filter 1 addresses background recovery present without added biotin, including nonspecific capture and pre-existing biotinylation. It does not by itself establish contact-site specificity. Filter 2 adds a spatial-enrichment criterion: candidates must be preferentially labeled by contact-targeted split-TurboID relative to cytosolic full-length TurboID. It therefore reduces inclusion of proteins that are readily labeled in the general cytosolic environment.

Potential genuine exclusion: A peripheral contact-associated protein could have both a contact-localized pool and a substantial soluble cytosolic pool. Alternatively, it could visit contacts only transiently. If its cytosolic-reference labeling is strong, its genuine contact-site signal may not be sufficiently enriched to pass filter 2. Such a protein is not necessarily absent from contacts; it fails the relative-enrichment criterion.

Assay interpretation: Split-TurboID labeling lasted four hours, whereas full-length TurboID labeling lasted one minute. The filter compares enrichment under those specific conditions, not equal-duration catalytic rates. Proximity labeling also does not demonstrate direct molecular binding or a functional membrane-tethering role.

Why the other choices fail: A confuses the cytosolic-reference filter with the no-added-biotin control and incorrectly guarantees retention of dual-localized proteins. C reverses the direction of enrichment. D mistakes proximity evidence for proof of direct binding and physical tethering.

**Final answer: B**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Primary evidence

[Split-TurboID enables contact-dependent proximity labeling in cells](https://doi.org/10.1073/pnas.1919528117) (2020).

- Figure 3A and Results: complementary fragments targeted to opposing organelle membranes
- Figure 4A: four-hour split-TurboID versus one-minute full-length TurboID labeling
- Figure 4B: 607/619 after filter 1, 97/97 after filter 2, and 67 intersected +rapamycin hits
- Figure 4B–C and Results, printed page 12147: omit-biotin versus cytosolic references
- Results, printed page 12147, paragraph before Validation of ER–Mitochondria Contact Orphans: reduced recovery of dual-localized contact/cytosol proteins

Figure 4B contrasts added-biotin labeling with the omit-biotin baseline, then contrasts contact-site labeling with a cytosolic TurboID reference. The second comparison selects relative contact enrichment rather than generic labeling strength. The Results explicitly explain that ratiometric filtering can remove genuine proteins dual-localized to contacts and cytosol. Proximity labeling alone does not identify direct tethers.

### Answer limitations

Individual protein enrichments and filtering thresholds are not provided, so the identities and number of genuine contact-associated proteins excluded cannot be determined. The unequal labeling durations also prevent interpreting these comparisons as measurements of intrinsic catalytic rates.

### Source qualifications

- P06709 is the canonical native BirA backbone used for private source-exclusion screening, not the complete evolved split-TurboID fragments with tags, localization elements and dimerization domains.
- The question interprets an already published assay and filtering comparison; it supplies neither novel variants nor engineering instructions.
- Enrichment and specificity depend on the reported conditions; the unequal labeling times do not support a direct catalytic-rate comparison.
- Surviving proteins are proximity-enriched candidates. Neither membership nor absence establishes direct binding, membrane tethering or exclusive localization.
- The displayed counts are the +rapamycin replicate filtering path only; they are not the full union of +rapamycin and omit-rapamycin datasets.

### Evidence review

- Correctly reproduces the +rapamycin path 607/619 to 97/97 and intersection 67, without conflating excluded proteins with false positives.
- Correctly separates omit-added-biotin background comparison from cytosolic-reference spatial enrichment.
- Correctly explains the documented loss of genuine contact/cytosol dual-localized proteins through a relative enrichment threshold.
- Labels a transient-contact scenario as a possible exclusion mechanism, not a paper-measured example.
- Correctly preserves the four-hour split versus one-minute full-length caveat and does not infer intrinsic catalytic rates.
- Correctly distinguishes proximity enrichment from direct physical binding or functional tether proof.
- Correctly rejects A, C and D without requiring hidden source facts.

Both the primary-source facts and this answer were reviewed by assistants. No material errors were found. This is not expert human validation or evidence of a training gain. Full author-copy PDFs were inspected; they are not redistributed here. No protein sequence, private gold label or full paper was supplied to the AI for this question.

[Exact generation request](request.json) · [Unchanged generated output](generated_output.json)

</details>
