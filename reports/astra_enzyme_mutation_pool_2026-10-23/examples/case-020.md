# case-020 — adenylate_kinase: mutation kinetic reasoning

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

Wild-type protein: Adenylate kinase (Escherichia coli K-12).
Full canonical wild-type sequence, numbered from the initial methionine as residue 1:

```text
MRIILLGAPGAGKGTQAQFIMEKYGIPQISTGDMLRAAVKSGSELGKQAKDIMDAGKLVTDELVIALVKE
RIAQEDCRNGFLLDGFPRTIPQADAMKEAGINVDYVLEFDVPDELIVDRIVGRRVHAPSGRVYHVKFNPP
KVEGKDDVTGEELTTRKDDQEETVRKRLVEYHQMTAPLIGYYSKEAEAGNTKYAKVDGTKPVAEVRADLE
KILG
```


Published variant(s): R36A/R123A.

Experimental evidence:
Published ATP-dependent measurements: WT kcat = 330 s^-1, ATP Km = 71 micromolar; R36A kcat = 55 s^-1, Km = 89 micromolar; R123A kcat = 0.28 s^-1, Km = 110 micromolar. Both substitutions replace one arginine with alanine in the same enzyme.

**Question:** Which explanation is most consistent with the very different effects of these two nominally similar charge-removing substitutions?

- **A.** Both substitutions primarily change protein stability; their residual turnover values directly quantify the fraction of properly folded enzyme in each sample.
- **B.** Their different positions can make distinct catalytic contributions; removing the same side-chain charge need not produce similar effects on turnover.
- **C.** R123A primarily weakens equilibrium ATP binding rather than catalytic performance; its modest ATP Km increase accounts for the large turnover decrease.
- **D.** Their catalytic contributions become equivalent after correcting turnover for ATP Km; the different half-saturation concentrations fully explain their different turnover ceilings.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.


## Astra’s worked solution

The supplied sequence confirms that both substitutions replace arginine, but at different positions. Arg-to-Ala removes the guanidinium group, including its electrostatic and hydrogen-bonding capabilities, and substantially reduces side-chain size. Identical substitution chemistry therefore does not imply identical functional consequences.

Quantitative comparison:

| Enzyme | kcat (s^-1) | ATP Km (µM) | kcat/Km (M^-1 s^-1) |
|---|---:|---:|---:|
| WT | 330 | 71 | 4.65 × 10^6 |
| R36A | 55 | 89 | 6.18 × 10^5 |
| R123A | 0.28 | 110 | 2.55 × 10^3 |

R36A decreases turnover by 330/55 = 6-fold. R123A decreases turnover by 330/0.28 ≈ 1,180-fold and turns over approximately 196-fold more slowly than R36A. In contrast, their ATP Km values are only about 1.25-fold and 1.55-fold the WT value. Thus, the striking difference is in turnover capacity, not ATP half-saturation.

For the fitted Michaelis–Menten ATP dependence at fixed other assay conditions, v/[E] = kcat[ATP]/(Km + [ATP]). Increasing ATP approaches the turnover ceiling kcat; changing Km changes how that ceiling is approached, not its height. Moreover, Km is a kinetic parameter and is not generally equal to the equilibrium dissociation constant Kd. Consequently, the modest Km increase cannot explain R123A's approximately thousand-fold decrease in kcat as simply weaker equilibrium ATP binding.

Adenylate kinase catalyzes phosphoryl transfer in ATP + AMP ⇌ 2 ADP. Depending on their three-dimensional positions, arginine residues can contribute differently to nucleotide positioning, transition-state electrostatics, or formation of catalytically competent conformations. The results are consistent with Arg123 making a substantially more consequential contribution to the turnover cycle under these conditions. They do not establish which microscopic step is affected: steady-state kcat can reflect chemistry, conformational changes, and product release.

The alternatives fail for distinct reasons:
• A: Turnover ratios are not direct measurements of folded fractions. That interpretation would require unsupported assumptions that the only defect is loss of active molecules and that the remaining active molecules retain WT turnover.
• C: Km is not an equilibrium-binding measurement, and its modest increase cannot account for the greatly reduced ATP-saturated turnover ceiling.
• D: kcat/Km is a low-ATP catalytic-efficiency measure, not a correction that makes turnover ceilings equivalent. These efficiencies still differ by approximately 243-fold between R36A and R123A.

Therefore, the most consistent explanation is that the same charge-removing substitution has different consequences because the two positions make different functional contributions. Answer: B.

## Final answer

B

## Astra’s stated limitations

The measurements support different effects on catalytic turnover but do not identify the precise atomic roles of Arg36 and Arg123, isolate the rate-limiting step, or establish protein-folding fractions. ATP Km alone does not determine equilibrium ATP affinity.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **adenylate_kinase** — [UniProt P69441](https://www.uniprot.org/uniprotkb/P69441/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

Correct remapped answer B. Correctly converts the efficiencies to M^-1 s^-1 and calculates 6-fold versus about 1180-fold WT turnover losses, about 196-fold difference in mutant turnover and about 243-fold difference in mutant catalytic efficiencies. Explains why half-saturation changes do not determine the turnover ceiling. Gives plausible position-specific catalytic roles while explicitly declining to identify exact contacts, folded fractions or a microscopic rate-limiting step.

Source support:

- 2021 Figure 2c / Table S2; 2023 Table 1, WT, R36A and R123A rows.
- Published ATP-dependent measurements: WT kcat = 330 s^-1, ATP Km = 71 micromolar; R36A kcat = 55 s^-1, Km = 89 micromolar; R123A kcat = 0.28 s^-1, Km = 110 micromolar. Both substitutions replace one arginine with alanine in the same enzyme.
- Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.
- Table 1, footnote a.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. Published R36, R88, R123, R156 and R167 all match the reference residues.
- The prompt supplies the verified canonical reference and published mutation labels. No unreported affinity tag, cloning scar or exact expressed-construct extension is inferred.

Primary references:

- [Dynamic Connection between Enzymatic Catalysis and Collective Protein Motions](https://pmc.ncbi.nlm.nih.gov/articles/PMC8297476/). Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.

- [Mechanistic basis for a connection between the catalytic step and slow opening dynamics of adenylate kinase](https://pmc.ncbi.nlm.nih.gov/articles/PMC11779523/). Table 1, footnote a.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
