# 9. Binding affinity versus valency and probe-induced clustering

## Question

Streptavidin is used to attach labels to biotinylated proteins. Compare these published observations. A4 is a tetramer of four active, His-tagged subunits; A1D3 is a tetramer containing one active and three binding-inactive subunits. The affinity measurements below use these tagged preparations, whereas the cellular comparison uses wild-type streptavidin versus A1D3.

| Preparation | Biotins bound per tetramer | Biotin Kd, mean ± SEM |
|---|---|---|
| A4 | 4 | (4.4 ± 1.1) × 10^-14 M |
| A1D3 | 1 | (4.8 ± 0.5) × 10^-14 M |

In cultured neurons expressing acceptor-peptide-tagged neuroligin-1, both fluorescent labels initially gave diffuse surface labeling. Two hours later, wild-type streptavidin produced strong clustering, whereas A1D3 labeling remained predominantly diffuse.

**Question:** Which explanation best reconciles the binding measurements with the cellular labeling pattern?

- **A.** A1D3 retains strong binding at its remaining site but has fewer sites for bridging labeled proteins; affinity and crosslinking capacity can therefore separate.
- **B.** A1D3 retains four-site bridging but has substantially weaker binding at every site; reduced occupancy therefore explains the predominantly diffuse labeling.
- **C.** A1D3 loses tetramer assembly and its neighboring-subunit support for binding; monomer formation therefore explains the reduced cellular clustering.
- **D.** A1D3 retains four functional binding sites because its Kd is similar to A4; the Kd measurement therefore establishes equivalent crosslinking capacity.

## Answer

A best reconciles the observations because binding affinity and binding valency are different properties.

Measured binding: A4 binds four biotins per tetramer, whereas A1D3 binds only one. Nevertheless, their biotin Kd values—(4.4 ± 1.1) × 10^-14 M and (4.8 ± 0.5) × 10^-14 M, respectively—are very similar. These measurements support retention of strong binding at A1D3’s remaining functional site, rather than substantial weakening of that site. Similar Kd values do not imply equal numbers of functional binding sites.

Biological mechanism: Kd describes equilibrium binding affinity. Crosslinking instead requires a reagent to engage at least two distinct target molecules simultaneously. Wild-type streptavidin has multiple functional biotin-binding sites and can therefore bridge biotinylated surface proteins. A1D3 remains tetrameric, but its single functional site cannot directly bridge two biotinylated proteins through biotin binding.

Connection to the cellular observations: Both labels can bind biotinylated neuroligin-1, explaining why both initially label the surface. The strong clustering observed after two hours with wild-type streptavidin is consistent with its multivalent crosslinking capacity. Predominantly diffuse A1D3 labeling is consistent with high-affinity attachment without direct bridging of separate labeled proteins.

Why the alternatives fail:
• B contradicts both the one-biotin-per-tetramer measurement and the similar measured affinities.
• C contradicts the stated tetrameric assembly of A1D3; reduced functional valency does not require monomer formation.
• D confuses affinity with valency. A similar Kd cannot establish four functional sites or equivalent crosslinking capacity, and the measured binding stoichiometry explicitly shows only one functional site in A1D3.

**Final answer: A**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Primary evidence

[A monovalent streptavidin with a single femtomolar biotin binding site](https://doi.org/10.1038/nmeth861) (2006).

- Table 1: bound-biotin stoichiometry; printed page 268
- Figure 3b and Results: biotin affinity; printed page 269
- Figure 4a and Results: initial versus two-hour AP-neuroligin-1 labeling; printed page 270

Table 1 establishes one bound biotin per A1D3 tetramer versus four for A4; Figure 3b gives comparable femtomolar site affinity. Figure 4a shows that the multivalent cellular label clusters tagged neuroligin whereas A1D3 does not to the same extent. Reduced capacity to bridge targets, rather than a large affinity loss or monomerization, reconciles these observations.

### Answer limitations

The affinity measurements compare tagged A4 and A1D3, whereas the neuronal experiment compares wild-type streptavidin with A1D3. The reported Kd values therefore do not directly establish wild-type affinity under cellular conditions or cellular binding kinetics. The labeling pattern is consistent with differential crosslinking capacity but does not directly reveal every molecular step of clustering.

### Source qualifications

- Canonical P22629 is the native 183-residue precursor, not the exact mature, tagged assayed subunit.
- A1D3 is monovalent but remains tetrameric. A4 affinity measurements involve His-tagged active subunits; the cellular multivalent comparison is wild-type streptavidin.
- No canonical-to-assay residue-number mapping or new mutation recipe is supplied.
- The neuronal target is a transfected acceptor-peptide-tagged neuroligin-1 construct; the observations do not establish universal effects on every native receptor.

### Evidence review

- Correctly separates equilibrium affinity, functional valency, oligomeric assembly and cellular clustering.
- Reproduces both Kd estimates and their errors correctly; treats them as comparable, without an unsupported claim of formal statistical equivalence.
- Correctly states that a single functional biotin-binding site cannot directly bridge two biotinylated targets through biotin binding, while the complex remains tetrameric.
- Connects the stated initially diffuse and two-hour divergent labeling patterns to multivalent bridging using appropriately qualified language.
- Explicitly distinguishes tagged A4 affinity measurements from wild-type cellular comparison and avoids inferring cellular binding kinetics from those Kd measurements.
- All three rejected alternatives are refuted by supplied measurements or the stated tetrameric construction.

Both the primary-source facts and this answer were reviewed by assistants. No material errors were found. This is not expert human validation or evidence of a training gain. Full author-copy PDFs were inspected; they are not redistributed here. No protein sequence, private gold label or full paper was supplied to the AI for this question.

[Exact generation request](request.json) · [Unchanged generated output](generated_output.json)

</details>
