# case-028 — adenylate_kinase: mutation kinetic reasoning

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


Published variant(s): R167A.

Experimental evidence:
The primary study reports WT kcat = 330 s^-1 with Mg2+ and 0.0075 s^-1 without Mg2+. The published R167A variant has kcat = 2.4 s^-1 in the Mg2+-containing kinetic comparison. These are reported turnover measurements; they are not Mg2+ binding-affinity measurements.

**Question:** Which quantitative and biological comparison is supported by these observations?

- **A.** Mg2+ removal causes about a 44,000-fold loss and R167A about a 140-fold loss; cofactor presence does not replace the missing residue contribution.
- **B.** Mg2+ removal causes about a 44,000-fold loss and R167A about a 140-fold loss; these turnover ratios also give the corresponding binding-affinity losses.
- **C.** Mg2+ removal causes about a 44,000-fold loss and R167A about a 140-fold loss; sufficiently high ATP must therefore restore R167A to WT turnover.
- **D.** Mg2+ removal causes about a 140-fold loss, while R167A with Mg2+ causes about a 44,000-fold loss; the residue substitution is the larger defect.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.


## Astra’s worked solution

Both fold-loss calculations use WT turnover with Mg2+, 330 s^-1, as the reference.

1. Mg2+ removal from WT: 330 / 0.0075 = 44,000-fold lower turnover.
2. R167A in the Mg2+-containing comparison: 330 / 2.4 = 137.5-fold lower turnover, approximately 140-fold.

Thus, R167A retains only about 0.73% of WT turnover despite Mg2+ being present. Under these assay conditions, the cofactor does not replace the contribution lost upon substituting Arg167.

Biologically, adenylate kinase catalyzes ATP + AMP ⇌ 2 ADP. Mg2+ commonly assists phosphoryl-transfer reactions by coordinating nucleotide phosphates, organizing reacting groups, and stabilizing charge. An arginine side chain can contribute electrostatic stabilization or active-site organization; alanine lacks its positively charged group. These are plausible mechanisms for the residue's contribution, not proof of a particular contact or catalytic role at position 167. The direct experimental observation is the substantial turnover deficit in the Mg2+-containing mutant assay.

The alternatives differ as follows:
- A gives both correct ratios and the supported conclusion that Mg2+ presence does not restore WT turnover to R167A.
- B incorrectly equates turnover losses with binding-affinity losses. kcat measures catalytic turnover, whereas binding affinity requires separate binding information; their ratios are not interchangeable.
- C incorrectly asserts obligatory rescue by ATP. Increasing substrate occupancy does not, by itself, remove a lower catalytic turnover limit, and no ATP-dependent rescue is reported.
- D reverses the two quantitative effects: Mg2+ removal produces the approximately 44,000-fold loss, while R167A with Mg2+ produces the approximately 140-fold loss.

Answer: A.

## Final answer

A

## Astra’s stated limitations

The turnover measurements do not establish binding affinities, protein stability, or the precise catalytic step affected by R167A. The conclusion about incomplete compensation by Mg2+ applies to the supplied Mg2+-containing comparison.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **adenylate_kinase** — [UniProt P69441](https://www.uniprot.org/uniprotkb/P69441/entry).

Source-supported reference answer: **A**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

Correct remapped answer A. Calculates 44000-fold loss without Mg2+ and 137.5-fold loss for R167A with Mg2+, plus about 0.73% retained mutant turnover. Correctly confines the lack of compensation to the supplied Mg2+-containing comparison. General phosphate-coordination and electrostatic explanations are labeled plausible rather than experimentally established Arg167 contacts. Does not confuse turnover ratios with affinities or assert an unmeasured ATP-rescue result.

Source support:

- 2021 main-text Mg2+ paragraph and Figure S9; arginine data in Figure 2c / Table S2, reproduced in 2023 Table 1.
- The primary study reports WT kcat = 330 s^-1 with Mg2+ and 0.0075 s^-1 without Mg2+. The published R167A variant has kcat = 2.4 s^-1 in the Mg2+-containing kinetic comparison. These are reported turnover measurements; they are not Mg2+ binding-affinity measurements.
- Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.
- Table 1, footnote a.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. Published R36, R88, R123, R156 and R167 all match the reference residues.
- The prompt supplies the verified canonical reference and published mutation labels. No unreported affinity tag, cloning scar or exact expressed-construct extension is inferred.

Primary references:

- [Dynamic Connection between Enzymatic Catalysis and Collective Protein Motions](https://pmc.ncbi.nlm.nih.gov/articles/PMC8297476/). Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.

- [Mechanistic basis for a connection between the catalytic step and slow opening dynamics of adenylate kinase](https://pmc.ncbi.nlm.nih.gov/articles/PMC11779523/). Table 1, footnote a.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
