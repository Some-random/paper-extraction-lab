# case-026 — PTEN phosphatase: mutation assay context and sensitivity

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

Reference protein sequence (P60484, full canonical wild-type backbone; coordinate reference only):

```text
MTAIIKEIVSRNKRRYQEDGFDLDLTYIYPNIIAMGFPAERLEGVYRNNIDDVVRFLDSKHKNHYKIYNL
CAERHYDTAKFNCRVAQYPFEDHNPPQLELIKPFCEDLDQWLSEDDNHVAAIHCKAGKGRTGVMICAYLL
HRGKFLKAQEALDFYGEVRTRDKKGVTIPSQRRYVYYYSYLLKNHLDYRPVALLFHKMMFETIPMFSGGT
CNPQFVVCQLKVKIYSSNSGPTRREDKFMYFEFPQPLPVCGDIKVEFFHKQNKMLKKDKMFHFWVNTFFI
PGPEETSEKVENGSLCDQEIDSICSIERADNDKEYLVLTLTKNDLDKANKDKANRYFSPNFKVKLYFTKT
VEEPSNPEASSSTSVTPDVSDNEPDHYRYSDTTDSDPENEPFDEDQHTQITKV
```


All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.

Published variants: D92N.

Supplied experimental observations:
- A published PTEN study reports that D92N resembles wild type in its yeast growth-rescue readout.
- The same paper notes that a PIP3 fluorescence reporter and an in-vitro phosphatase assay detect only partial activity for D92N.
- Growth rescue is a downstream cellular phenotype; reporter and biochemical assays read out other aspects of PTEN function. No quantitative calibration converting one assay into the others is provided.

**Question:** What is the most defensible interpretation of this apparent disagreement?

- **A.** The growth-rescue result establishes fully wild-type phosphatase activity in the direct assays, because downstream growth provides a calibrated measure of enzymatic rate.
- **B.** Partial phosphatase function can support wild-type-like growth; the downstream rescue result therefore does not establish fully wild-type activity in the other assays.
- **C.** The assays give a common quantitative activity estimate: wild-type-like growth and partial biochemical activity are interchangeable once expressed relative to their wild-type controls.
- **D.** The reporter and biochemical assays establish complete loss of phosphatase activity, so wild-type-like growth must occur without any residual activity from D92N.


## Astra’s worked solution

B is the most defensible interpretation: partial phosphatase function can support wild-type-like growth, so growth rescue does not establish fully wild-type activity in other assays.

Sequence context: The reference confirms Asp at position 92. Asp92 lies in PTEN’s catalytic-loop region, and replacing its carboxylate with an asparagine amide can alter catalytic chemistry. However, this sequence-based mechanistic consideration does not determine the magnitude of the activity change or establish complete inactivation.

Experimental observations: D92N resembles wild type in yeast growth rescue, whereas the PIP3 fluorescence reporter and in-vitro phosphatase assay report partial activity. These are distinct endpoints. The reporter reflects a cellular PIP3-related state, the biochemical assay assesses phosphatase function under its assay conditions, and growth is a downstream cellular phenotype rather than a direct measurement of enzymatic rate.

Mechanistic interpretation: The relationship between phosphatase function and growth need not be linear. For example, residual activity could exceed the threshold needed for near-maximal growth rescue, even while reporter and biochemical measurements remain detectably below wild type. Such a threshold or saturation effect is a compatible explanation, not a quantitatively established mechanism here. Consequently, the supplied results need not be contradictory.

Discriminating the choices: A incorrectly treats growth as a calibrated measure of enzymatic activity. C incorrectly assumes that normalization to each assay’s own wild-type control makes different readouts quantitatively interchangeable; normalization does not eliminate their different response relationships. D contradicts the supplied description of partial activity, which is not complete loss. B preserves the distinction between residual phosphatase function and its downstream growth consequence without claiming more than the evidence supports.

## Final answer

B

## Astra’s stated limitations

No quantitative relationship between growth, reporter output and biochemical activity is supplied. The observations do not establish an exact residual catalytic rate or uniquely explain why growth appears wild-type-like. The canonical sequence establishes residue numbering, not the complete assay constructs.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PTEN phosphatase** — [UniProt P60484](https://www.uniprot.org/uniprotkb/P60484/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly separates the downstream growth phenotype from PIP3 reporter and biochemical endpoints.
- Uses a residual-activity threshold or saturation relationship as an explicitly hypothetical explanation, rather than asserting a measured mechanism.
- Does not assert the paper's proposed deamidation explanation as established and does not infer an exact residual catalytic rate.

Source support:

- Discussion paragraph on the Asp92 discrepancy and D92N
- D92N appears WT-like in growth rescue but partially functional in PIP3 fluorescence or in-vitro phosphatase assays.

Source qualifications:

- The question does not determine an exact kinetic rate or which assay is universally superior.
- Deamidation is not established by these observations and must not be asserted as the demonstrated cause.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Mighell2018 Methods: NM_000314.6, corresponding 403-aa NP_000305; current canonical record cross-references NP_000305.3. Full paper-assay construct sequence still requires final replay before release.
- The paper proposes deamidation as a possible explanation, rather than establishing it. No mechanism of deamidation is required or taught as a fact here.

Primary references:

- [A Saturation Mutagenesis Approach to Understanding PTEN Lipid Phosphatase Activity and Genotype-Phenotype Relationships](https://pmc.ncbi.nlm.nih.gov/articles/PMC5986715/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
