# case-024 — triosephosphate_isomerase: mutation kinetic reasoning

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


Published variant(s): Y208T/S211G.

Experimental evidence:
Published GAP-isomerization kcat values at pH 7.5 and 25 C: WT 8900 s^-1; Y208T 3700 s^-1; S211G 7500 s^-1; the experimentally measured double variant Y208T/S211G 520 s^-1. For this question, an independent fractional-effects model predicts kcat(double) = kcat(Y208T) * kcat(S211G) / kcat(WT).

**Question:** How does the observed double-variant turnover compare with that specified independence model?

- **A.** The model predicts about 2300 s^-1 by adding the two changes from WT; the observed value is about fourfold lower, indicating negative kinetic epistasis.
- **B.** The model predicts about 3100 s^-1; the observed value is about sixfold lower, indicating negative kinetic epistasis for turnover under these conditions.
- **C.** The model predicts about 3100 s^-1; the sixfold deficit establishes direct physical contact between the substituted residues as the mechanism of their interaction.
- **D.** The model predicts about 3100 s^-1; the observed value is about sixfold above that prediction, indicating positive kinetic epistasis for turnover.

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

Source-supported reference answer: **B**. No valid selected answer was available.

Scientific review: Source exclusion; not submitted to Astra.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- This reference overlaps a reserved source group. The candidate is retained for visibility and excluded from generation and the shortlist.

Source support:

- Table 1, GAP kcat column, WT/Y208T/S211G/Y208T-S211G rows.
- Published GAP-isomerization kcat values at pH 7.5 and 25 C: WT 8900 s^-1; Y208T 3700 s^-1; S211G 7500 s^-1; the experimentally measured double variant Y208T/S211G 520 s^-1. For this question, an independent fractional-effects model predicts kcat(double) = kcat(Y208T) * kcat(S211G) / kcat(WT).
- Table 1 and footnotes a-d.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. E165, Y208 and S211 match the paper labels.
- The canonical reference includes initiator methionine. The verified mature structural polymer omits it but retains canonical author numbering. No additional tags or scars are inferred.

Primary references:

- [Role of Loop-Clamping Side Chains in Catalysis by Triosephosphate Isomerase](https://pmc.ncbi.nlm.nih.gov/articles/PMC4694050/). Table 1 and footnotes a-d.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
