# case-006 — Glucokinase / hexokinase-4: mutation effect and measurement scope

**Assistant selection tier: strong.** Generation status: `completed`.

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

Published variants: W99R.

Supplied experimental observations:
- A published human glucokinase study used a yeast complementation assay in which growth depends on the supplied human enzyme supporting glucose metabolism.
- Under the same tested glucose condition, the W99R variant supports greater growth than wild-type glucokinase.
- These observations are a cellular functional readout. The supplied comparison does not separately measure enzyme concentration, turnover number and glucose-binding constants.

**Question:** What does this result show, and what remains unresolved by this readout alone?

- **A.** W99R reduces glucokinase-associated function in this assay; greater growth therefore indicates weaker glucose metabolism rather than improved complementation by the human enzyme.
- **B.** W99R improves functional performance through a measured increase in purified-enzyme turnover; the growth ratio supplies that kinetic ratio independently of protein abundance.
- **C.** W99R improves functional performance through a measured increase in enzyme abundance; the growth ratio supplies that abundance ratio independently of microscopic enzyme kinetics.
- **D.** W99R improves functional performance in this assay; the growth comparison does not separate changes in enzyme abundance from changes in microscopic kinetic steps.


## Astra’s worked solution

The supported conclusion is improved functional performance in this assay, with the mechanism unresolved.

Glucokinase phosphorylates glucose to glucose-6-phosphate using ATP. In the supplied yeast complementation assay, growth depends on the human enzyme supporting glucose metabolism. W99R produces greater growth than wild type under the same tested glucose condition, so it provides stronger functional complementation.

However, growth is an integrated cellular outcome, not a direct measurement of purified-enzyme kinetics or protein abundance. Improved complementation could result from more functional enzyme being present, altered activity per enzyme molecule at the tested glucose concentration, or both. Expression, folding and stability can affect functional enzyme abundance; substrate interactions, conformational transitions and catalytic steps can affect per-molecule performance. None of these possible mechanisms is individually established by the reported growth comparison or by the W99R substitution itself.

Furthermore, growth need not be proportional to enzymatic flux. Therefore, a growth ratio cannot be interpreted as either a turnover-number ratio or an enzyme-abundance ratio. Testing one glucose condition also does not determine glucose-binding constants.

A reverses the functional interpretation of the supplied complementation result. B incorrectly claims that purified-enzyme turnover was measured independently of abundance. C incorrectly claims that abundance was measured independently of kinetics. D correctly states both the improved assay performance and the unresolved distinction between abundance and microscopic kinetic effects.

## Final answer

D

## Astra’s stated limitations

The supplied readout does not separately measure enzyme abundance, expression, stability, turnover number or glucose-binding constants. It establishes improved complementation under the tested glucose condition, not a unique molecular mechanism or an effect that necessarily generalizes to other conditions.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Glucokinase / hexokinase-4** — [UniProt P35557](https://www.uniprot.org/uniprotkb/P35557/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly reads greater W99R complementation under the tested condition.
- Explains why cellular growth need not scale linearly with enzymatic flux and cannot determine abundance or turnover ratios.
- Possible abundance, folding and kinetic contributions are presented as alternatives rather than claimed measurements.

Source support:

- Figure 1B and Results validating the yeast complementation assay
- W99R has higher activity than WT in the initial growth assay; F150S/R191W/G223S/G261R reduce function, while D217N/E279Q are WT-like.

Source qualifications:

- A higher growth readout is not itself a measured purified-enzyme turnover number.
- No clinical outcome or variant design recommendation follows from this question.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Gersing2023 Methods: pancreatic isoform ENST00000403799.8; same transcript is cross-referenced by current P35557-1. Paper also identifies P35557 isoform1 in its sequence analysis.
- The assay uses pancreatic glucokinase, ENST00000403799.8, and the paper identifies P35557 isoform 1. No exact kcat is supplied by Figure 1B.

Primary references:

- [A comprehensive map of human glucokinase variant activity](https://pmc.ncbi.nlm.nih.gov/articles/PMC10131484/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
