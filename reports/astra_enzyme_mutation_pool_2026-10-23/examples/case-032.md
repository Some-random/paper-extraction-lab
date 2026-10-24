# case-032 — triosephosphate_isomerase: mutation kinetic reasoning

**Assistant selection tier: held.** Generation status: `not_dispatched_source_hold`.

Hold/status note: Overlap with reserved evaluation/development sources; not submitted to Astra.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

Wild-type protein: Triosephosphate isomerase (Saccharomyces cerevisiae).
Full canonical wild-type sequence, numbered from the initial methionine as residue 1:

```text
MARTFFVGGNFKLNGSKQSIKEIVERLNTASIPENVEVVICPPATYLDYSVSLVKKPQVTVGAQNAYLKA
SGAFTGENSVDQIKDVGAKWVILGHSERRSYFHEDDKFIADKTKFALGQGVGVILCIGETLEEKKAGKTL
DVVERQLNAVLEEVKDWTNVVVAYEPVWAIGTGLAATPEDAQDIHASIRKFLASKLGDKAASELRILYGG
SANGSNAVTFKDKADVDGFLVGGASLKPEFVDIINSRN
```


Published variant(s): Y208F.

Experimental evidence:
Published pH-dependent inhibitor-binding analysis estimates pKa = 10.4 for E165 in the WT TIM complex with the intermediate analogue phosphoglycolate trianion (PGA), and pKa = 6.3 for the corresponding Y208F complex. These pKa values refer specifically to the inhibitor-bound enzyme. For the simple protonation equilibrium in this question, protonated fraction = 1/(1+10^(pH-pKa)).

**Question:** At pH 8.0, which interpretation of these experimentally fitted pKa values is correct?

- **A.** WT is about 0.4% protonated and Y208F about 98%; the protonated fractions are obtained by subtracting the higher-pKa and lower-pKa populations from unity.
- **B.** WT is about 99.6% protonated and Y208F about 2%; these same fractions also establish E165 protonation in the free enzyme and true catalytic intermediate.
- **C.** WT is about 2% protonated and Y208F about 99.6%; the mutation therefore increases proton retention by E165 in the specified inhibitor-bound state.
- **D.** WT is about 99.6% protonated and Y208F about 2%; changing the protein environment can strongly alter E165 protonation in the specified inhibitor-bound state.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.


## Astra’s worked solution

No valid structured solution is recorded. This candidate remains in the catalog.

Returned model text, if any, is preserved below without editing.

```text

```

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **triosephosphate_isomerase** — [UniProt P00942](https://www.uniprot.org/uniprotkb/P00942/entry).

Source-supported reference answer: **D**. No valid selected answer was available.

Scientific review: Source exclusion; not submitted to Astra.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- This reference overlaps a reserved source group. The candidate is retained for visibility and excluded from generation and the shortlist.

Source support:

- Table 1, WT yeast and Y208F rows; Figure 2 and associated inhibitor-complex interpretation.
- Published pH-dependent inhibitor-binding analysis estimates pKa = 10.4 for E165 in the WT TIM complex with the intermediate analogue phosphoglycolate trianion (PGA), and pKa = 6.3 for the corresponding Y208F complex. These pKa values refer specifically to the inhibitor-bound enzyme. For the simple protonation equilibrium in this question, protonated fraction = 1/(1+10^(pH-pKa)).
- Table 1 (yeast WT and Y208F rows), Figure 2, and discussion of inhibitor-bound E165 protonation.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. E165, Y208 and S211 match the paper labels.
- The canonical reference includes initiator methionine. The verified mature structural polymer omits it but retains canonical author numbering. No additional tags or scars are inferred.

Primary references:

- [Enzyme Architecture: Amino Acid Side-Chains That Function To Optimize the Basicity of the Active Site Glutamate of Triosephosphate Isomerase](https://pmc.ncbi.nlm.nih.gov/articles/PMC6037162/). Table 1 (yeast WT and Y208F rows), Figure 2, and discussion of inhibitor-bound E165 protonation.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
