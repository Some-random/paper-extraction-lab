# 3. TurboID and miniTurbo: when more labeling weakens the time window

## Question

Reference protein: Escherichia coli BirA, the ancestral biotin ligase of TurboID and miniTurbo. The full canonical wild-type sequence is supplied only for coordinates; it is not the complete evolved or tagged assay construct.

Protein sequence:

```text
MKDNTVPLKLIALLANGEFHSGEQLGETLGMSRAAINKHIQTLRDWGVDVFTVPGKGYSLPEPIQLLNAK
QILGQLDGGSVAVLPVIDSTNQYLLDRIGELKSGDACIAEYQQAGRGRRGRKWFSPFGANLYLSMFWRLE
QGPAAAIGLSLVIGIVMAEVLRKLGADKVRVKWPNDLYLQDRKLAGILVELTGKTGDAAQIVIGAGINMA
MRRVEESVVNQGWITLQEAGINLDRNTLAAMLIRELRAALELFEQEGLAPYLSRWEKLDNFINRPVKLII
GDKEIFGISRGIDKQGALLLEQDGIIKPWMGGEISLRSAEK
```

Numbering uses the initial methionine as wild-type residue 1. Both evolved enzyme cores delete Ala146. miniTurbo additionally lacks wild-type residues 1-63. Thus wild-type Met241 corresponds to enzyme-core position 240 in TurboID and 177 in miniTurbo, before any added tags or linkers. The evolved backgrounds contain other substitutions; the sequence above does not represent either final variant.

Published observations:
- Screening found M241T potentially beneficial for labeling activity, and the substitution was included with other changes in TurboID.
- M241T was also tested in the miniTurbo background but was not retained because signal increased when added biotin was omitted.
- In the broader comparison, miniTurbo generally showed less labeling before biotin addition than TurboID, while TurboID generally gave greater labeling yield.

The purpose is to label neighboring proteins within a defined time window after biotin addition. The omit-added-biotin condition does not experimentally remove the biotin already present in cells.

**Question:** What is the most defensible interpretation of the M241T tradeoff for that time-window objective?

- **A.** The higher omit-biotin signal identifies stronger equilibrium biotin binding as the M241T mechanism; correcting added biotin concentration for that affinity difference should recover the original labeling window.
- **B.** Labeling before the intended start can use biotin already present and leave covalent marks on proteins. Greater total yield can therefore weaken temporal control; these observations do not identify which molecular step M241T changes or establish the same effect in every background.
- **C.** Protein-by-protein subtraction of the omit-biotin sample converts the later accumulated signal into labels acquired exclusively after biotin addition, because the same labeling chemistry operates in both samples.
- **D.** The difference between TurboID and miniTurbo identifies interaction with the deleted N-terminal domain as the source of the M241T tradeoff; the other evolved substitutions and expression differences need not contribute to that interpretation.

Interpret the published observations using the relevant biology. Explain the alternatives, then give one answer letter. Do not propose new variants or experimental procedures.

## Answer

B. Greater labeling yield can weaken control over when the labels were acquired.

A promiscuous biotin ligase uses biotin and ATP to produce an activated intermediate that can covalently label nearby proteins. Omitting added biotin does not establish that the cell contains no biotin. Signal generated before the intended start can therefore contribute to a later accumulated readout. A protein carrying a label need not have acquired it during the intended window; movement and turnover can further change the observed population.

This explains why the miniTurbo observation matters. M241T increased signal when added biotin was omitted, so excluding that substitution could favor temporal control even if including it increased total labeling. The choice of an enzyme variant depends on the measurement objective: maximal accumulated signal and a well-defined observation window are different objectives.

The observations do not identify the molecular step altered by M241T. More signal could reflect differences in the active enzyme population, substrate handling, intermediate production or release, or other context-dependent properties. It is not a measurement of an isolated affinity or catalytic constant, and the full-length and truncated evolved enzymes differ in more than their N-terminal domain.

A confuses an accumulated labeling endpoint with an equilibrium binding measurement. No measured affinity change is supplied, so the proposed affinity correction is unsupported.

B connects the covalent labeling chemistry to the timing problem while leaving the particular molecular mechanism and its generality unresolved.

C overstates what background subtraction establishes. Subtraction can help quantify differences between matched samples. It does not generally identify when each individual covalent mark was formed or guarantee an exclusively post-addition protein set. Estimating an incremental signal under a validated model is a narrower claim.

D assigns a unique causal interaction to the N-terminal deletion without isolating that change from the other substitutions and expression differences.

The supplied wild-type BirA sequence is a coordinate reference. It does not, by itself, predict this mutation's labeling tradeoff. The experimental observations and labeling chemistry support the inference.

Answer: B.

Final answer: B

<details>
<summary>Sources, evidence checks and limitations</summary>

**Source-supported answer: B.** The answer selects B and matches that reference.

### Primary evidence

[Efficient proximity labeling in living cells and organisms with TurboID](https://doi.org/10.1038/nbt.4201) (2018).

- Methods, Yeast display directed evolution, last two paragraphs: M241T activity observation, introduction with K194I/S263P into G3, and exclusion of M241T from miniTurbo because omit-biotin signal increased.
- Methods, Cloning: all ligase variants have wild-type A146 deleted.
- Supplementary Table 1: TurboID and miniTurbo genotype rows; miniTurbo retains wild-type span64-321 plus A146 deletion.
- Figure 2a-b and Discussion: yield versus pre-biotin-labeling tradeoff; miniTurbo temporal-control consideration.
- Supplementary Note2: biotin-AMP formation, release and covalent labeling; proposed mechanisms remain hypotheses.

The paper reports the M241T decision and the broader yield/background tradeoff. Covalent label accumulation explains why pre-window activity matters. The multiple-choice inference is AI-created; no new M241T measurements, fixed affinity change or causal epistasis map is claimed.

### Answer limitations

- A baseline control improves interpretation but cannot generally timestamp individual covalent marks after the fact.
- Protein movement and turnover can influence accumulated labeling; marks are not asserted permanent.
- The result applies to the reported backgrounds and conditions, not every cell, compartment or variant.

### Source qualifications

- The displayed sequence is native321-residue BirA, not TurboID, miniTurbo or a complete V5/NES fusion.
- All substitution labels retain native BirA coordinates even after deletions.
- A146 deletion gives n-1 for retained n>146 in TurboID; deletion1-63 plus146 gives n-64 for retained n>146 in miniTurbo. M241T is therefore core240 or177, respectively. Added fusion offsets are unknown here.
- The enzyme-core genotypes are supported by Supplementary Table1; canonical references are checked independently against official UniProt.
- The main-text methods describe the M241T miniTurbo result qualitatively without a numeric fold-change or isolated binding/turnover constants.
- The comparison does not isolate the N-terminal domain as the cause of context dependence; other substitutions, enzyme stability and expression can matter.

### Evidence checks and records

The answer was checked against the supplied observations and cited source evidence. These checks were performed by AI assistants, not expert human reviewers; training benefits have not been measured.

[Question, answer and source verification](../artifacts/example-03/source_verification.json) · [Creation and revision records](../revision_v4.json)

</details>
