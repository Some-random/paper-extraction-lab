# case-008 — triosephosphate_isomerase: mutation kinetic reasoning

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


Published variant(s): Y208F/Y208A.

Experimental evidence:
Published GAP-isomerization values at pH 7.5 and 25 C (Km based on total GAP): WT kcat = 8900 s^-1, Km = 1.0 mM; Y208A kcat = 740 s^-1, Km = 2.9 mM; Y208F kcat = 13 s^-1, Km = 2.4 mM. Tyrosine-to-phenylalanine removes the phenolic hydroxyl while retaining an aromatic ring; tyrosine-to-alanine also removes that ring.

**Question:** What is the most defensible lesson from comparing the two published substitutions?

- **A.** Y208F turns over about 57 times more slowly than Y208A despite similar Km values; a structurally closer substitution need not have a smaller functional effect.
- **B.** Removing the same hydroxyl produces equivalent catalytic effects; the different turnover values directly establish different folded-protein fractions rather than different catalytic behavior.
- **C.** Retaining the aromatic ring preserves WT catalytic chemistry; the lower Y208F turnover therefore reflects only a loss of equilibrium substrate-binding affinity.
- **D.** Y208F is more catalytically efficient than Y208A because its smaller Km more than compensates for its lower turnover ceiling under substrate-limited conditions.

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

Source-supported reference answer: **A**. No valid selected answer was available.

Scientific review: Source exclusion; not submitted to Astra.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- This reference overlaps a reserved source group. The candidate is retained for visibility and excluded from generation and the shortlist.

Source support:

- Table 1, GAP columns, WT/Y208A/Y208F rows and footnotes a-d.
- Published GAP-isomerization values at pH 7.5 and 25 C (Km based on total GAP): WT kcat = 8900 s^-1, Km = 1.0 mM; Y208A kcat = 740 s^-1, Km = 2.9 mM; Y208F kcat = 13 s^-1, Km = 2.4 mM. Tyrosine-to-phenylalanine removes the phenolic hydroxyl while retaining an aromatic ring; tyrosine-to-alanine also removes that ring.
- Table 1 and footnotes a-d.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. E165, Y208 and S211 match the paper labels.
- The canonical reference includes initiator methionine. The verified mature structural polymer omits it but retains canonical author numbering. No additional tags or scars are inferred.

Primary references:

- [Role of Loop-Clamping Side Chains in Catalysis by Triosephosphate Isomerase](https://pmc.ncbi.nlm.nih.gov/articles/PMC4694050/). Table 1 and footnotes a-d.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
