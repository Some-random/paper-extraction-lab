# 2. Adenylate kinase: a conservative substitution can impair catalysis

## Question

Wild-type protein: Adenylate kinase (Escherichia coli K-12).
Full canonical wild-type sequence, numbered from the initial methionine as residue 1:

```text
MRIILLGAPGAGKGTQAQFIMEKYGIPQISTGDMLRAAVKSGSELGKQAKDIMDAGKLVTDELVIALVKE
RIAQEDCRNGFLLDGFPRTIPQADAMKEAGINVDYVLEFDVPDELIVDRIVGRRVHAPSGRVYHVKFNPP
KVEGKDDVTGEELTTRKDDQEETVRKRLVEYHQMTAPLIGYYSKEAEAGNTKYAKVDGTKPVAEVRADLE
KILG
```


Published variant(s): R156K.

Experimental evidence:
Published ATP-dependent kinetic measurements (central values; kcat in s^-1, ATP Km in micromolar):
WT: kcat 330, Km 71.
R156K: kcat 0.74, Km 52.
Arginine and lysine both normally carry a positive side-chain charge near neutral pH.

**Question:** Which interpretation best explains why calling R156K a conservative substitution does not establish functional conservation?

**Choices:**

- **A.** The lower ATP Km compensates for the turnover loss, so R156K should retain near-WT catalytic efficiency when ATP is limiting.
- **B.** The lower ATP Km establishes stronger equilibrium ATP binding, so the turnover defect must arise entirely from slower product release.
- **C.** The roughly 450-fold turnover loss with a modest Km shift shows that retaining positive charge need not preserve residue-specific catalytic performance.
- **D.** The roughly 450-fold turnover loss directly measures a 450-fold reduction in correctly folded protein, while catalysis by the folded molecules remains unchanged.

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.

## Answer

The best interpretation is C: chemical similarity does not guarantee functional conservation.

1. Quantitative evidence
The turnover decrease is:
330 / 0.74 ≈ 446-fold.
Thus, R156K has roughly 450-fold lower reported kcat than WT. In contrast, its ATP Km decreases only modestly:
52 / 71 ≈ 0.73,
a decrease of about 27%.

At ATP concentrations well below both Km values, with other assay conditions fixed, the rate per enzyme is approximately (kcat/Km)[ATP]. The relevant catalytic efficiencies are:
• WT: 330/71 ≈ 4.65 s^-1 μM^-1.
• R156K: 0.74/52 ≈ 0.0142 s^-1 μM^-1.

The mutant therefore retains only about 0.31% of WT ATP-dependent catalytic efficiency, a roughly 327-fold loss. The modest Km decrease does not compensate for the turnover defect, ruling out A.

2. Why a charge-conserving substitution can strongly impair function
Arginine and lysine are both normally positively charged near neutral pH, making this substitution conservative in a broad chemical classification. However, arginine's guanidinium group and lysine's terminal ammonium group differ in geometry, charge distribution, and hydrogen-bonding arrangements. In an enzyme, these differences can affect substrate positioning, transition-state stabilization, or conformational steps during turnover. These are general mechanistic possibilities, not specific interactions established for residue 156 by the supplied sequence. The observed kinetic loss nevertheless demonstrates that preserving positive charge does not preserve this variant's catalytic performance.

3. Why the other interpretations are unsupported
B incorrectly equates Km with an equilibrium dissociation constant. Even in the simple mechanism E + S ⇌ ES → E + P, Km = (koff + kcat)/kon, whereas Kd = koff/kon. Consequently, a lower Km can accompany slower turnover without stronger equilibrium binding. Adenylate kinase has a more complex, multisubstrate catalytic cycle, so the ATP Km likewise cannot automatically be interpreted as ATP binding affinity. Nothing supplied identifies slower product release as the sole cause of the turnover loss.

D incorrectly treats kcat as a direct measurement of folding. A lower reported kcat can reflect changes in chemistry or other turnover-limiting steps; depending on enzyme normalization, an inactive fraction can also affect apparent turnover. These measurements do not establish a 450-fold reduction in correctly folded protein or unchanged catalysis by the folded molecules.

Thus, the strong turnover defect with only a modest Km shift supports C.

**Final answer: C**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

Primary full-text Results and a kinetic table support the reported measurements and fold-change calculations. General side-chain chemistry helps interpret them; a specific structural cause is not established by the table.

### Answer limitations

The conclusion applies to the supplied ATP-dependent kinetic measurements. Neither the sequence nor these kinetic parameters uniquely identify the affected microscopic step, establish equilibrium ATP affinity, or quantify the folded or active protein fraction.

### References and source review

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to AI remain visible above.

Source identity: **adenylate_kinase** — [UniProt P69441](https://www.uniprot.org/uniprotkb/P69441/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

Correct remapped answer C. Correctly calculates about 446-fold lower turnover, about 327-fold lower ATP-dependent catalytic efficiency, and a 27% Km decrease. Connects the shared positive charge to different guanidinium/ammonium geometry and hydrogen bonding without claiming specific Arg156 contacts were observed. Correctly distinguishes Km from Kd, and treats changes in chemistry, conformational steps, product release and active fraction as possibilities rather than measured causes.

Source support:

- 2021 Figure 2c / Table S2; 2023 Table 1, WT and R156K rows.
- Published ATP-dependent kinetic measurements (central values; kcat in s^-1, ATP Km in micromolar):
WT: kcat 330, Km 71.
R156K: kcat 0.74, Km 52.
Arginine and lysine both normally carry a positive side-chain charge near neutral pH.
- Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.
- Table 1, footnote a.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. Published R36, R88, R123, R156 and R167 all match the reference residues.
- The prompt supplies the verified canonical reference and published mutation labels. No unreported affinity tag, cloning scar or exact expressed-construct extension is inferred.

Primary references:

- [Dynamic Connection between Enzymatic Catalysis and Collective Protein Motions](https://pmc.ncbi.nlm.nih.gov/articles/PMC8297476/). Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.

- [Mechanistic basis for a connection between the catalytic step and slow opening dynamics of adenylate kinase](https://pmc.ncbi.nlm.nih.gov/articles/PMC11779523/). Table 1, footnote a.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.

[Original source records and unchanged AI output](../../astra_enzyme_mutation_pool_2026-10-23/examples/case-004.md)

</details>
