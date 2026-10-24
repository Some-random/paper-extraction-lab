# case-012 — adenylate_kinase: mutation kinetic reasoning

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


Published variant(s): R88A/R156K.

Experimental evidence:
Published central values: R88A kcat = 1.8 s^-1 and ATP Km = 120 micromolar; R156K kcat = 0.74 s^-1 and ATP Km = 52 micromolar. Compare equal active-enzyme concentrations with AMP held fixed and saturating. Use v/[E] = kcat[ATP]/(Km+[ATP]); no substrate inhibition is assumed in this comparison.

**Question:** How does the R88A-to-R156K rate ratio change from ATP far below both Km values to ATP far above both Km values?

- **A.** At low ATP, R88A is about 2.4 times faster; at saturating ATP, the variants are nearly equal in rate.
- **B.** At low ATP, R156K is about 2.3 times faster; at saturating ATP, R88A is about 2.4 times faster.
- **C.** At low ATP, R88A is about 2.4 times faster; at saturating ATP, R88A remains about 2.4 times faster.
- **D.** At low ATP, R88A is only about 1.05 times faster; at saturating ATP, R88A is about 2.4 times faster.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.


## Astra’s worked solution

The supplied reference has arginine at both reported mutation positions. The rate comparison follows from the supplied kinetic measurements, rather than from predicting effects of these substitutions from sequence.

Adenylate kinase catalyzes ATP + AMP ⇌ 2 ADP. With AMP fixed and saturating, use the stated ATP-dependent rate law. Equal active-enzyme concentrations cancel in the rate ratio. Writing S = [ATP] in micromolar:

R(S) = v_R88A/v_R156K = (1.8/0.74) × (52 + S)/(120 + S).

At ATP far below both Km values, v/[E] ≈ (kcat/Km)S. Thus the relevant quantities are ATP catalytic efficiencies:
• R88A: 1.8/120 = 0.0150 s^-1 µM^-1.
• R156K: 0.74/52 ≈ 0.01423 s^-1 µM^-1.

The low-ATP rate ratio is therefore 0.0150/0.01423 ≈ 1.054. R88A is only about 1.05 times faster. Its approximately 2.43-fold higher kcat is almost offset by its approximately 2.31-fold higher ATP Km. A lower Km alone does not establish a faster low-substrate rate, and Km should not automatically be interpreted as a binding dissociation constant.

At ATP far above both Km values, v/[E] approaches kcat. The rate ratio becomes 1.8/0.74 ≈ 2.43, so R88A is about 2.4 times faster.

The ratio therefore increases from approximately 1.05 at low ATP to approximately 2.4 at saturating ATP. A and C incorrectly assign a 2.4-fold advantage at low ATP; B incorrectly favors R156K at low ATP. The supplied measurements support D.

## Final answer

D

## Astra’s stated limitations

The conclusion uses the supplied central values and assumes saturating AMP, equal active-enzyme concentrations, and the stated Michaelis–Menten model without substrate inhibition. No measurement uncertainties are provided, so the approximately 5% low-ATP difference is not evidence of statistical significance. Sequence alone would not establish these kinetic effects.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **adenylate_kinase** — [UniProt P69441](https://www.uniprot.org/uniprotkb/P69441/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

Correct remapped answer D. Derives the full ratio R(S) = (1.8/0.74)*(52+S)/(120+S), then correctly obtains about 1.054 at low ATP and 2.432 at saturation. Keeps the equal-active-enzyme and saturating-AMP assumptions explicit. Correctly notes that the roughly 5% low-ATP difference is a central-value comparison rather than demonstrated statistical significance. Distractors are rejected using the appropriate kinetic regimes.

Source support:

- 2021 Figure 2c / Table S2; 2023 Table 1, R88A and R156K rows.
- Published central values: R88A kcat = 1.8 s^-1 and ATP Km = 120 micromolar; R156K kcat = 0.74 s^-1 and ATP Km = 52 micromolar. Compare equal active-enzyme concentrations with AMP held fixed and saturating. Use v/[E] = kcat[ATP]/(Km+[ATP]); no substrate inhibition is assumed in this comparison.
- Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.
- Table 1, footnote a.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. Published R36, R88, R123, R156 and R167 all match the reference residues.
- The prompt supplies the verified canonical reference and published mutation labels. No unreported affinity tag, cloning scar or exact expressed-construct extension is inferred.

Primary references:

- [Dynamic Connection between Enzymatic Catalysis and Collective Protein Motions](https://pmc.ncbi.nlm.nih.gov/articles/PMC8297476/). Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.

- [Mechanistic basis for a connection between the catalytic step and slow opening dynamics of adenylate kinase](https://pmc.ncbi.nlm.nih.gov/articles/PMC11779523/). Table 1, footnote a.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
