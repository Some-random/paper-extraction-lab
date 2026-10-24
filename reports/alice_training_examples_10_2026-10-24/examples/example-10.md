# 10. What does a proximity-labeling ratio measure?

## Question

Cho and colleagues used split-TurboID targeted to contacts between the endoplasmic reticulum and mitochondria. They compared the recovered proteins with a reference made using full-length TurboID in the cytosol.

The contact-targeted samples were labeled for four hours; the cytosolic-reference samples for one minute. The authors chose these different durations because the enzymes had different activities. Under those conditions, the preparations gave comparable overall signals for biotinylated proteins.

Proteins were first compared with an omit-added-biotin control, then filtered using their contact-targeted/cytosolic-reference enrichment ratios. The latter threshold was calibrated using a reference list of cytosolic proteins and the paper's 10% false-discovery criterion.

Consider a hypothetical protein P that reproducibly exceeds the omit-biotin background but fails the cytosolic-reference filter. No protein-specific labeling kinetics or independent localization measurements are available for P.

**Question:** Which interpretation best explains what this comparison establishes?

- **A.** Dividing P's contact-targeted signal by 240 would compensate for the unequal labeling durations. The adjusted ratio could estimate its relative contact-encounter rate, although direct molecular binding would remain unproven.
- **B.** P failed a comparison of accumulated labeling under these conditions. A cytosolic pool could depress its ratio even if P visits contacts, and covalent labels can persist after movement; matching bulk signal does not calibrate P's labeling kinetics or contact occupancy.
- **C.** Matching overall labeling compensates for the enzymes' different activities. P's ratio can therefore estimate its relative contact occupancy; failure favors predominantly cytosolic localization, although brief visits to contacts would remain possible.
- **D.** Calibrating the threshold with cytosolic reference proteins supplies an error probability for each candidate. A passing protein would have at most a 10% probability of being a false contact hit; P's failure chiefly reflects insufficient statistical confidence rather than compartment-dependent labeling.

## Answer

B gives the interpretation supported by this comparison: P did not pass a condition-specific enrichment filter on accumulated labeling.

What is measured: proximity labeling produces covalent modifications on accessible proteins near an active enzyme. Recovery therefore reflects a history of labeling, rather than a direct count of how many molecules occupy a contact at the moment of collection. A protein can acquire a label during a visit and move elsewhere while retaining it. Label persistence is subject to protein turnover and other biological processes; it is not permanent by definition.

What the cytosolic reference adds: the comparison favors proteins recovered more strongly from contact-targeted labeling than from the cytosolic reference. A protein with both a contact-associated pool and a substantial cytosolic pool can be labeled in both conditions. Strong cytosolic-reference labeling can reduce its ratio even when genuine contact association occurs. The paper explicitly discusses loss of such dual-localized proteins through this filtering approach.

Why the unequal durations matter: four hours and one minute sample different histories of protein movement and enzyme exposure. The two preparations also use different enzyme forms and locations. Comparable overall biotinylation establishes a bulk comparison, not a separate calibration for each protein. Local accessibility, enzyme exposure, abundance, movement and potential saturation can all affect a particular protein's recovered signal.

A introduces an unsupported kinetic correction. Four hours is 240 minutes, but dividing the contact-targeted signal by 240 only estimates a rate under additional assumptions about linear signal accumulation and relevant enzyme activity. Those assumptions are not established for P. A simple time correction therefore cannot recover its encounter rate from these endpoints.

C extends bulk matching into an individual localization measurement. Equal total signal can arise from different distributions of labeling across proteins and time. It does not convert P's ratio into a fraction of molecules, or a fraction of time, at contacts.

D turns reference-set calibration into an individual error probability. The paper's cutoff uses recovery of specified reference false-positive proteins. That procedure does not assign a probability of incorrect localization to each candidate, and failing the filter is not itself an estimate of statistical confidence about P's compartment.

P's result is compatible with several biological histories. It does not establish absence from contacts, contact residence time, the size of a contact-associated pool, or direct molecular binding. The supported conclusion remains its failure to meet this particular relative-labeling criterion.

**Final answer: B**

<details>
<summary>Sources, evidence checks and limitations</summary>

**Source-supported answer: B.** The edited answer selects B and matches that reference.

### Primary evidence

[Split-TurboID enables contact-dependent proximity labeling in cells](https://doi.org/10.1073/pnas.1919528117) (2020).

- Results before Figure 4 and Figure 3F: different enzyme activities, four-hour versus one-minute labeling, and comparable overall biotinylation
- Figure 4A-C: labeling conditions and sequential omit-biotin/cytosolic-reference comparisons
- Methods, Generation of ER-Mitochondria Proteome Lists: reference-protein sets and false-discovery cutoffs
- Results before Validation of ER-Mitochondria Contact Orphans: reduced recovery of contact/cytosol dual-localized proteins

The published assay used different labeling durations to obtain comparable overall biotinylation and applied reference-based enrichment filters. The authors explicitly identify dual-localized contact/cytosol proteins as a source of lost recovery. P is an AI-created hypothetical case; its behavior is used to reason about the assay, not presented as a new observation from the paper.

### Answer limitations

- P is hypothetical. No identity, individual kinetics, localization measurement or numerical enrichment value is supplied.
- The question does not establish how much temporal integration, saturation or any other mechanism affected an actual protein. Those are relevant possibilities, not measured explanations for P.
- The ratio is an assay-condition-dependent enrichment measure; it is not a calibrated contact-occupancy fraction or encounter rate.
- The reference-set false-discovery criterion does not establish a per-protein posterior error probability.

### Source qualifications

- The enzymes differ in activity and spatial distribution. Matching bulk labeling does not establish matched protein-specific kinetics or equal-duration sampling.
- The original reported counts remain in the archived first version. They were removed from this question because selecting the answer should not depend on copying retained-list counts.
- The original paper used reference-protein false-discovery cutoffs, not a rule retaining exactly 97 proteins per replicate.
- Proximity enrichment does not establish direct binding, physical membrane tethering or exclusive localization.

### Evidence review and revision provenance

- The stem no longer tells the solver to name an excluded genuine protein or states the correct interpretation of unequal durations.
- All distractors preserve the reported observations. Their errors involve time normalization, bulk-to-protein calibration or reference-set-to-individual probability inference.
- An independent solver given only the final question selected B and found no material ambiguity.
- This is an experimental-interpretation exercise; its difficulty and training benefit have not been measured.

This question and explanation were AI-edited after source review. They are source-aware revisions, not unchanged teacher responses or a new blinded generation. Assistant review passed for the frozen revision; this is not expert human validation or evidence of a training gain. No new teacher API request was made for the revision.

[Revised question](../artifacts/example-10/revised_question.json) · [Revised answer and source label](../artifacts/example-10/revised_answer.json) · [Original earlier question and answer](../artifacts/example-10/original_presentation.md) · [Original generation request for the earlier question](../artifacts/example-10/request.json) · [Unchanged original output for the earlier question](../artifacts/example-10/generated_output.json) · [Revision record](../revision_v2.json)

</details>
