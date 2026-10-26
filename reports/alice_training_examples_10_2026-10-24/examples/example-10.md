# 10. What does exclusion from a proximity-labeling list mean?

## Question

Cho and colleagues compared proteins recovered by contact-targeted split-TurboID at endoplasmic reticulum–mitochondria contacts with proteins recovered using a cytosolic TurboID reference. The preparations used different labeling durations because their activities differed; overall labeling signals were comparable. The comparison measures accumulated labeling under those conditions.

Proteins were first compared with a no-added-biotin control and then filtered for enrichment in contact-targeted labeling relative to the cytosolic reference.

Consider a hypothetical protein P that reproducibly passes the no-added-biotin comparison but fails the contact-versus-cytosol enrichment filter. There are no independent localization measurements, protein-specific labeling kinetics, or functional measurements for P.

A collaborator proposes prioritizing proteins that passed both filters and deferring P because follow-up resources are limited. There is no independent evidence that P is especially important to this project's biological question.

**Question:** Given the stated resource limit and lack of independent evidence prioritizing P, which recommendation best follows the available evidence?

**Choices:**

- **A.** Follow up P first because passing the no-added-biotin comparison establishes contact association; treat the second filter as a measure of detection sensitivity.
- **B.** Prioritize the passing proteins and provisionally defer P; reconsider its priority if independent localization or functional evidence makes it relevant to the project.
- **C.** Defer P until its enrichment ratio is converted into contact occupancy; use that quantity to decide whether its contact-associated pool merits functional study.
- **D.** Follow up P first because failure of the cytosolic-reference filter identifies a dual-localized protein; treat that inferred pool as evidence of a missed contact function.

## Answer

**Answer: B.**

With limited resources and no independent reason to prioritize P, I would provisionally follow the collaborator's priority and defer it. That is a practical ranking of candidates, not a conclusion that P is absent from contacts or biologically unimportant. Passing both filters provides the passing candidates with stronger support under this particular selection scheme. It does not make the filtered list a complete inventory of proteins relevant to the biological process.

The two comparisons answer different questions. P's recovery exceeds the no-added-biotin background, so it passes that first selection step. It nevertheless fails the required enrichment relative to the cytosolic reference. The second result establishes insufficient relative enrichment under the sampled conditions. It does not identify the reason: the ratio depends on recovery in both the contact-targeted condition and the reference condition.

One compatible explanation is that P has a substantial cytosolic pool as well as a genuine contact-associated pool. Recovery from the cytosolic population can reduce relative enrichment even if some P is present at contacts. Another is that P has little or no contact association in this setting, making deferral biologically appropriate as well as practical. Differences in accessibility to labeling or in the labeling history could also contribute. These remain possible explanations; no protein-specific evidence supplied here selects among them. Comparable overall labeling does not provide a separate calibration of P's recovery, kinetics or occupancy.

Independent localization evidence would address whether P is found at contacts, in the cytosol, or in more than one compartment under relevant conditions. Evidence about function would address a separate question: whether P contributes to the process the project aims to understand. A small contact-associated pool could be functionally important, while a readily detected contact-associated protein need not be a key functional factor. Neither localization nor proximity labeling alone establishes direct molecular binding or functional necessity.

My priority would change if independent evidence linked P to the relevant contact-associated process, supported a meaningful contact-localized pool, or suggested that this filtering scheme systematically misses the kind of protein the project seeks. A different project objective could also justify following up P despite its failed filter. Without such a reason, deferral is reasonable, provided the record states the actual basis: P currently has weaker support from this assay's enrichment criterion, not a demonstrated lack of biological relevance.

B makes an evidence-based priority decision without claiming biological absence or unimportance. A promotes background-control passage into localization evidence. C assumes an unavailable occupancy calibration. D treats one possible explanation as an established result and then infers function.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 7, A–D restoration).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


[Cho et al., Split-TurboID enables contact-dependent proximity labeling in cells](https://doi.org/10.1073/pnas.1919528117) (2020): Figure 3F and Results before Figure 4 for unequal-duration bulk matching; Figure 4 and Methods, Generation of ER–Mitochondria Proteome Lists, for sequential filtering; Results before Validation of ER–Mitochondria Contact Orphans for loss of dual-localized proteins.

Source qualification: [UniProt P06709](https://www.uniprot.org/uniprotkb/P06709/entry) is native Escherichia coli BirA, the ancestral reference backbone. It is not the complete evolved split-TurboID fragments or their tags, localization elements and dimerization domains.

[Historical independent-check status](../artifacts/example-10/independent_check.json). The earlier revision records a check assertion, but its standalone solver response and model metadata were not recovered. No independently verifiable blinded check of the current question is claimed.

The assay description is source-derived. P, the collaborator's proposal, and the prioritization discussion are hypothetical. The paper does not supply P's identity, localization, function, or labeling kinetics. Exact durations and the reference-set false-discovery criterion were removed because this item requires no valid protein-specific quantitative calculation. Relative enrichment remains useful for its intended filtering role.

This is a source-aware assistant revision responding to review feedback, not a fresh teacher-model response or expert human validation. No new experiments or outcomes are claimed, and training benefit has not been measured. Earlier questions, answers, and generation records remain in Git history and existing artifacts.

</details>
