# case-022 — Glucokinase / hexokinase-4: mutation chemistry and position dependence

**Assistant selection tier: moderate.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

Reference protein sequence (P35557, full canonical wild-type backbone; coordinate reference only):

```text
MLDDRARMEAAKKEKVEQILAEFQLQEEDLKKVMRRMQKEMDRGLRLETHEEASVKMLPTYVRSTPEGSE
VGDFLSLDLGGTNFRVMLVKVGEGEEGQWSVKTKHQMYSIPEDAMTGTAEMLFDYISECISDFLDKHQMK
HKKLPLGFTFSFPVRHEDIDKGILLNWTKGFKASGAEGNNVVGLLRDAIKRRGDFEMDVVAMVNDTVATM
ISCYYEDHQCEVGMIVGTGCNACYMEEMQNVELVEGDEGRMCVNTEWGAFGDSGELDEFLLEYDRLVDES
SANPGQQLYEKLIGGKYMGELVRLVLLRLVDENLLFHGEASEQLRTRGAFETRFVSQVESDTGDRKQIYN
ILSTLGLRPSTTDCDIVRRACESVSTRAAHMCSAGLAGVINRMRESRSEDVMRITVGVDGSVYKLHPSFK
ERFHASVRRLTPSCEITFIESEEGSGRGAALVSAVACKKACMLGQ
```


All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.

Published variants: D217N, E279Q.

Supplied experimental observations:
- D217N replaces an aspartate side chain with asparagine, and E279Q replaces glutamate with glutamine. Each removes a negatively charged carboxylate while preserving a similarly sized polar amide side chain.
- In a published pancreatic human glucokinase complementation assay, both D217N and E279Q show wild-type-like functional performance.
- The experiment does not report the behavior of every other acidic residue in the protein or establish identical kinetics in every glucose condition.

**Question:** Which generalization about sequence changes is justified by these two tested substitutions?

- **A.** Loss of an acidic side-chain charge is tolerated at these two tested positions; substitution effects therefore depend on position and the measured assay context.
- **B.** The wild-type-like outcome demonstrates preservation of side-chain charge, because the asparagine and glutamine replacements retain the negative carboxylate groups of the original residues.
- **C.** Both substitutions introduce positively charged side chains, so their wild-type-like performance demonstrates tolerance of a negative-to-positive charge reversal at the two tested positions.
- **D.** The two wild-type-like outcomes establish a position-independent rule: acidic-to-amide substitutions preserve glucokinase function equally wherever they occur within this protein under the tested conditions.


## Astra’s worked solution

A is the justified generalization.

Sequence and chemical observations: The reference contains Asp at position 217 and Glu at position 279. Asp and Glu have acidic carboxylate side chains; their respective replacements, Asn and Gln, have neutral polar amide side chains. These substitutions therefore neutralize a negative charge. They neither preserve that charge nor introduce a positive charge.

Experimental interpretation: Both variants show wild-type-like functional performance in the supplied pancreatic human glucokinase complementation assay. Thus, loss of the acidic side-chain charge is tolerated for these particular substitutions at these two positions in that measured context. This conclusion comes from the supplied functional observations, not from sequence inspection alone.

Mechanistic scope: Retaining similar side-chain size and polarity may help preserve some interactions, but the observations do not identify why these variants perform well. Acidic residues elsewhere can have different roles in local electrostatics, substrate interactions, catalysis, or structural stability. Consequently, the same type of chemical substitution need not have the same functional effect at another position. Likewise, wild-type-like complementation does not establish that every underlying molecular property or kinetic parameter is unchanged.

Discriminating the alternatives:
- B is chemically incorrect: Asn and Gln do not retain the original negatively charged carboxylate groups.
- C is chemically incorrect: these replacements are neutral amides, not positively charged side chains, so neither substitution is a negative-to-positive charge reversal.
- D overgeneralizes two position-specific observations into a rule for every acidic residue. The supplied evidence does not support that extrapolation.

A correctly limits the conclusion to the tested positions and assay context.

## Final answer

A

## Astra’s stated limitations

The supplied evidence concerns these two substitutions in a pancreatic human glucokinase complementation assay. It does not establish identical kinetics across glucose conditions, independently unchanged binding, expression or stability, or the effects of substitutions at other acidic residues.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Glucokinase / hexokinase-4** — [UniProt P35557](https://www.uniprot.org/uniprotkb/P35557/entry).

Source-supported reference answer: **A**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly describes acidic-to-neutral-amide side-chain changes and does not call either replacement positively charged.
- Correctly restricts the functional conclusion to the two tested positions and the assay context.
- Most of the chemistry and functional facts are already given in the question; the added interpretation is useful but not a newly inferred enzyme mechanism.

Source support:

- Figure 1B; Results validating the assay with common variants
- D217N and E279Q are described as WT-like in the yeast functional assay.

Source qualifications:

- WT-like complementation does not mean all microscopic constants are identical.
- No claim is made that these positions are universally nonessential across all cellular settings.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Gersing2023 Methods: pancreatic isoform ENST00000403799.8; same transcript is cross-referenced by current P35557-1. Paper also identifies P35557 isoform1 in its sequence analysis.
- Side-chain chemistry is standard biochemical interpretation of the exact mapped substitutions, not a claim that the paper measured side-chain charge.

Primary references:

- [A comprehensive map of human glucokinase variant activity](https://pmc.ncbi.nlm.nih.gov/articles/PMC10131484/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
