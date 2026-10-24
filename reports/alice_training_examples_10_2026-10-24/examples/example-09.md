# 9. Testing whether a protein label changes its target

## Question

Streptavidin is used to label biotinylated proteins. A4 is a tetramer of four active, His-tagged subunits; A1D3 is a tetramer containing one active and three binding-inactive subunits. The affinity measurements below use these tagged preparations, whereas the cellular comparison uses wild-type streptavidin versus A1D3.

| Preparation | Biotins bound per tetramer | Biotin Kd, mean ± SEM |
|---|---|---|
| A4 | 4 | (4.4 ± 1.1) × 10^-14 M |
| A1D3 | 1 | (4.8 ± 0.5) × 10^-14 M |

In cultured neurons expressing acceptor-peptide-tagged neuroligin-1, both fluorescent labels initially gave diffuse surface labeling. Two hours later, wild-type streptavidin produced strong clustering, whereas A1D3 labeling remained predominantly diffuse.

A colleague argues: "Because the soluble-biotin affinities are similar, the two labels should be interchangeable for observing neuroligin's native organization once the amount of initial labeling is matched."

In each proposed follow-up, the chosen matching strategy would be followed by tracking neuroligin organization with the same independent readout that does not link target molecules together. These are thought-experiment comparisons, not additional experiments reported in the paper.

**Question:** Which matching strategy most directly tests whether the labels differently perturb neuroligin organization?

- **A.** Match the measured fraction of neuroligin molecules initially occupied by each preparation.
- **B.** Measure soluble-biotin binding in the neuronal assay medium, then choose probe concentrations giving the same predicted occupancy in that soluble-binding measurement.
- **C.** Match the total concentration of functional biotin-binding sites supplied by the two preparations.
- **D.** Match the initial surface fluorescence intensity using the same imaging settings, without separately calibrating fluorophores per bound complex.

## Answer

A is the most direct comparison because it matches initial target engagement, rather than a proxy for it.

The biological question is whether the label changes the organization of the protein being observed. Before comparing later organization, the two treatments should engage comparable fractions of neuroligin molecules. Measuring that fraction directly addresses this variable. The shared independent readout then helps distinguish redistribution of neuroligin from differences in how the streptavidin probes themselves appear.

Why occupancy matters: soluble-biotin affinity, the number of available binding sites and the number of occupied target molecules are different quantities. Several active sites grouped on one tetramer can connect biotins on different targets. The same number of active sites distributed among separate monovalent tetramers does not create that connection through biotin binding. Thus, equal initial target coverage can coexist with different capacities to reorganize targets.

If the two labels produce different later organization at matched initial target occupancy, that would support differential probe-induced perturbation. It would not by itself prove that every observed cluster arose through direct bridging, or identify which treatment best reproduces an unlabeled native state.

Why the other matching strategies are less direct:

B addresses a real evidence gap: the printed affinity measurements use tagged A4, while the cell experiment uses wild-type streptavidin. Measuring soluble-biotin binding in the relevant medium would improve that comparison. However, predicted occupancy in a soluble-binding measurement is not measured occupancy of membrane-bound neuroligin. Surface geometry, accessibility, multivalent attachment and the labeling history can change how the probes engage cellular targets. A comparable equilibrium affinity also does not establish identical binding kinetics.

C matches the supply of functional sites. It does not establish how many neuroligin molecules are occupied. It also leaves the sites grouped differently: four on a multivalent complex versus one on each monovalent complex. Equal binding capacity supplied to cells therefore does not remove the biological distinction of interest.

D matches an optical signal. Fluorescence counts fluorophores, rather than target molecules directly. Differences in fluorophores per bound complex, or in the number of targets engaged by each complex, can produce the same intensity with different target coverage. Using identical imaging settings does not supply those missing calibrations.

The distinction is between matching the actual biological variable and matching a convenient measurement related to it. All four strategies can be useful; A most directly controls initial target engagement for the stated comparison.

**Final answer: A**

<details>
<summary>Sources, evidence checks and limitations</summary>

**Source-supported answer: A.** The edited answer selects A and matches that reference.

### Primary evidence

[A monovalent streptavidin with a single femtomolar biotin binding site](https://doi.org/10.1038/nmeth861) (2006).

- Table 1, printed page 268: bound-biotin stoichiometry for A4 and A1D3
- Figure 3b and Results, printed page 269: soluble-biotin affinity measurements
- Figure 4a and Results, printed page 270: initially diffuse and later divergent neuroligin labeling
- Introduction and Discussion: distinction between strong biotin binding and multivalent target crosslinking

The paper supports the affinity, binding-site counts and neuronal labeling observations. Its distinction between affinity and multivalent crosslinking motivates the revised question. The occupancy-matched comparison and independent readout are AI-created follow-up reasoning, not an additional experiment or result reported by the authors.

### Answer limitations

- This is a proposed comparison. No occupancy-matched follow-up or independent-readout outcome is asserted to have been measured.
- An independent readout must itself avoid linking or substantially perturbing the targets. No particular implementation is assumed.
- Matched occupancy can test differential perturbation, but does not establish which condition reproduces native organization; a suitable independent baseline would be needed.
- The comparison does not isolate every difference between preparations or prove the molecular origin of every cluster.

### Source qualifications

- The affinity data compare tagged A4 with A1D3. The published neuronal experiment compares wild-type streptavidin with A1D3; that distinction is explicit in the question.
- A1D3 is monovalent and tetrameric. Functional valency, oligomeric assembly, equilibrium affinity and target occupancy are separate properties.
- The question concerns transfected acceptor-peptide-tagged neuroligin-1. It does not claim the same outcome for every native receptor.

### Evidence review and revision provenance

- All four strategies share the same downstream organization readout; no option is singled out merely by measuring that endpoint.
- Rejected choices are compatible with the printed observations. They rely on soluble binding, supplied site concentration or fluorescence as an insufficiently calibrated proxy for occupied targets.
- An independent solver given only the final question selected A and found no material ambiguity.
- Question difficulty and benefit for model training have not been measured.

This question and explanation were AI-edited after source review. They are source-aware revisions, not unchanged teacher responses or a new blinded generation. Assistant review passed for the frozen revision; this is not expert human validation or evidence of a training gain. No new teacher API request was made for the revision.

[Revised question](../artifacts/example-09/revised_question.json) · [Revised answer and source label](../artifacts/example-09/revised_answer.json) · [Original earlier question and answer](../artifacts/example-09/original_presentation.md) · [Original generation request for the earlier question](../artifacts/example-09/request.json) · [Unchanged original output for the earlier question](../artifacts/example-09/generated_output.json) · [Revision record](../revision_v2.json)

</details>
