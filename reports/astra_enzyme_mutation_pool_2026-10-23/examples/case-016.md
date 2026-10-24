# case-016 — triosephosphate_isomerase: mutation kinetic reasoning

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


Published variant(s): S211A/S211G.

Experimental evidence:
Published GAP-isomerization central values at pH 7.5 and 25 C, using total GAP: S211A kcat = 2800 s^-1, Km = 12 mM; S211G kcat = 7500 s^-1, Km = 1.8 mM. Both substitutions remove the serine side-chain hydroxyl; alanine retains a methyl side chain and glycine does not.

**Question:** At GAP concentrations well below both Km values, which comparison is supported?

- **A.** S211A has about 2.5-fold higher catalytic efficiency; the product of kcat and Km determines the rate ratio when GAP is well below Km.
- **B.** S211G has about 2.7-fold higher catalytic efficiency; the turnover ratio alone determines the rate ratio when GAP is well below Km.
- **C.** S211G has about 18-fold higher catalytic efficiency; removing the same hydroxyl group need not produce the same low-substrate functional effect.
- **D.** S211G has about 6.7-fold higher catalytic efficiency; the inverse Km ratio alone determines the rate ratio when GAP is well below Km.

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

Source-supported reference answer: **C**. No valid selected answer was available.

Scientific review: Source exclusion; not submitted to Astra.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- This reference overlaps a reserved source group. The candidate is retained for visibility and excluded from generation and the shortlist.

Source support:

- Table 1, GAP kcat and Km columns, S211A/S211G rows.
- Published GAP-isomerization central values at pH 7.5 and 25 C, using total GAP: S211A kcat = 2800 s^-1, Km = 12 mM; S211G kcat = 7500 s^-1, Km = 1.8 mM. Both substitutions remove the serine side-chain hydroxyl; alanine retains a methyl side chain and glycine does not.
- Table 1 and footnotes a-d.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. E165, Y208 and S211 match the paper labels.
- The canonical reference includes initiator methionine. The verified mature structural polymer omits it but retains canonical author numbering. No additional tags or scars are inferred.

Primary references:

- [Role of Loop-Clamping Side Chains in Catalysis by Triosephosphate Isomerase](https://pmc.ncbi.nlm.nih.gov/articles/PMC4694050/). Table 1 and footnotes a-d.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
