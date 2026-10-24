# case-014 — Glucokinase / hexokinase-4: mutation comparator interpretation

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

Published variants: F150S, D217N, E279Q.

Supplied experimental observations:
- In a primary study of pancreatic human glucokinase, the same yeast complementation assay compares wild type with several published variants.
- F150S gives lower growth-based functional performance than wild type.
- D217N and E279Q give approximately wild-type-like performance in that assay.
- No matched abundance measurement or purified-enzyme kinetic measurement for these three variants is supplied in this question.

**Question:** Which comparative conclusion follows from the data?

- **A.** D217N and E279Q perform below wild type like F150S, so the experiment groups all three substitutions together as reduced-function variants in this cellular assay.
- **B.** F150S performs worse than the two wild-type-like comparators; this cellular comparison does not distinguish altered abundance, folding or kinetics as its molecular cause.
- **C.** F150S performs worse because its protein abundance is directly measured as lower; the growth comparison independently excludes altered folding or kinetics as contributing causes.
- **D.** F150S performs better than D217N and E279Q in the cellular assay, placing it above the two comparators despite its non-conservative amino-acid substitution.


## Astra’s worked solution

The reported comparison directly supports B: F150S produces lower growth-based functional performance than wild type, whereas D217N and E279Q are approximately wild-type-like in the same yeast complementation assay. Thus, F150S performs worse than the two comparators in this cellular readout. No finer ranking between D217N and E279Q is established.

Glucokinase catalyzes ATP-dependent phosphorylation of glucose. Yeast complementation reports whether the expressed enzyme supports cellular function, rather than measuring an isolated molecular property. Reduced growth can reflect less protein, a smaller correctly folded or stable protein population, altered catalytic kinetics under cellular conditions, or combinations of these effects. The supplied observations do not distinguish those possibilities.

The reference sequence confirms that F150S is a chemically nonconservative substitution. Such a change could affect protein interactions or conformational behavior, but neither the residue identity nor the growth result proves a particular folding, abundance, or catalytic defect. Likewise, the acidic-to-amide substitutions in the two comparators cannot be assumed biochemically neutral merely because their growth performance is approximately wild-type-like.

A contradicts the reported performance of D217N and E279Q. C asserts an abundance measurement that was not supplied and unjustifiably excludes folding and kinetic contributions, which can coexist with abundance changes. D reverses the observed comparison. B alone preserves both the measured functional ranking and the uncertainty about its molecular cause.

## Final answer

B

## Astra’s stated limitations

The molecular cause of the F150S growth defect is unresolved because no matched abundance measurements or purified-enzyme kinetics are supplied. Approximately wild-type-like growth also does not establish identical biochemical behavior under other conditions.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Glucokinase / hexokinase-4** — [UniProt P35557](https://www.uniprot.org/uniprotkb/P35557/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly ranks F150S below the two near-wild-type comparators without inventing a finer D217N-versus-E279Q ranking.
- Residue identities and side-chain chemistry are correct; abundance, folding and kinetic explanations remain possibilities rather than measured causes.
- The main inference is reading the supplied assay comparison; the response does not establish a specific molecular mechanism.

Source support:

- Figure 1B; Results describing initial assay validation
- F150S is among the function-reducing test variants; D217N and E279Q are WT-like.

Source qualifications:

- No exact magnitude or confidence interval is invented from the qualitative comparison.
- The assay does not isolate protein abundance, folding stability, substrate affinity or turnover in this question.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Gersing2023 Methods: pancreatic isoform ENST00000403799.8; same transcript is cross-referenced by current P35557-1. Paper also identifies P35557 isoform1 in its sequence analysis.
- These are observed test-variant results, not imputed values from unmeasured variants.

Primary references:

- [A comprehensive map of human glucokinase variant activity](https://pmc.ncbi.nlm.nih.gov/articles/PMC10131484/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
