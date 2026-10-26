# 9. Does a label reveal or change protein organization?

## Question

Published observations from a study of biotinylated neuroligin-1 on cultured neurons:

- Wild-type streptavidin has four functional biotin-binding sites. A1D3 is still a tetramer, but only one of its sites binds biotin.
- Tagged four-site and one-site preparations had similar soluble-biotin affinities. The cellular comparison used wild-type streptavidin and A1D3, so the affinity and cell experiments were not comparisons of exactly the same preparations.
- Both cellular labels initially appeared diffuse. Later, wild-type streptavidin labeling showed pronounced clustering while A1D3 labeling remained predominantly diffuse.

A collaborator concludes that the diffuse A1D3 image reveals native neuroligin organization and that similar soluble-biotin affinity makes further comparison unnecessary.

**Question:** Which initial comparison most directly tests a contribution from functional valency while accounting for differences in cellular target engagement and detection?

**Choices:**

- **A.** Compare one-, intermediate- and four-site probes at comparable measured initial target engagement, using an independently calibrated organization readout.
- **B.** Compare probe concentrations selected from soluble-biotin affinity estimates, using the original labeling images to quantify organization and initial target engagement.
- **C.** Compare preparations supplying equal total functional binding-site concentrations, using their matched initial surface fluorescence as the measure of target engagement.
- **D.** Compare the probes at equal tetramer concentrations, using identical imaging settings and the initially diffuse patterns as the baseline for organization.

## Answer

**Answer: A.**

The observations justify concern that the probe affects the observed pattern, but they do not establish which pattern represents native neuroligin organization. Similar affinity for soluble biotin controls only part of the problem. A tetramer with four active sites can connect separate biotinylated targets; an A1D3 tetramer has only one functional site and cannot make that same connection through multiple biotin-binding sites. This difference in functional valency remains even though both preparations are tetramers. Cellular target engagement and fluorophores per detected complex can also affect the image, and the affinity measurements did not use exactly the same preparations as the cellular comparison.

My first comparison would ask whether the organization pattern depends on functional valency after accounting for initial target engagement and detection. An intermediate-valency preparation could be informative here: a corresponding intermediate tendency to form clusters would support a valency-dependent contribution. A difference between multivalent and monovalent labels at comparable engagement would be consistent with probe-mediated crosslinking. If the apparent difference instead largely disappeared after accounting for engagement or detection, the original images would give weaker support for redistribution. Neither pattern alone would isolate every difference between the preparations, and matching initial engagement would not guarantee identical engagement later.

My second comparison would ask whether the organization agrees with an independent readout that has been evaluated for perturbation. If that readout also showed diffuse organization, the A1D3 image would gain support as a less perturbing representation. If it instead revealed clusters or a different organization, the diffuse A1D3 image could be missing a feature of the target distribution. Agreement is useful only to the extent that the independent method has different, understood biases; agreement between two perturbing methods is not sufficient validation.

A concentration-dependence comparison is another defensible priority, especially if the concern is whether clustering occurs only in a particular labeling regime. Its interpretation would still need to distinguish altered opportunities for crosslinking from altered target coverage and detection. Thus, the next evidence should resolve a specific competing explanation. The current results motivate testing probe-induced perturbation, while a native-state claim additionally needs a suitable independent baseline and attention to the perturbations introduced by that baseline.

A varies functional valency while directly addressing target engagement and detection. B substitutes soluble binding for cellular engagement; C substitutes supplied capacity and fluorescence for measured engagement; D leaves functional-site supply and engagement unequal. These other comparisons can be informative for different questions, but do not control the stated alternatives as directly.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 7, A–D restoration).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


[Howarth et al., A monovalent streptavidin with a single femtomolar biotin binding site](https://doi.org/10.1038/nmeth861) (2006): Table 1 and Figure 3 for stoichiometry and soluble binding; Figure 4 and accompanying Results for neuronal labeling and clustering.

Source qualification: [UniProt P22629](https://www.uniprot.org/uniprotkb/P22629/entry) is the native 183-residue streptavidin precursor from Streptomyces avidinii. It identifies the source protein, not the exact mature, engineered or tagged assayed subunit, and does not specify the A1D3 preparation.

[Historical independent-check status](../artifacts/example-09/independent_check.json). The earlier revision records a check assertion, but its standalone solver response and model metadata were not recovered. No independently verifiable blinded check of the current question is claimed.

The three observations are paraphrases of the published comparisons. The collaborator's claim and follow-up choices are hypothetical teaching material. No new comparison, result, native-state measurement, or experimental procedure is asserted. The answer offers conditional reasoning, not a unique experimental prescription.

This is a source-aware assistant revision responding to review feedback. It retains A–D choices and a complete worked answer. It is not a fresh teacher-model response or expert human validation, and training benefit has not been measured. Earlier versions remain in Git history and the existing revision artifacts.

</details>
