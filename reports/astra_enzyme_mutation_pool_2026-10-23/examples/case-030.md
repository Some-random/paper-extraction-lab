# case-030 — Glucokinase / hexokinase-4: mutation kinetic mechanism comparison

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

Published variants: A456V, W99R.

Supplied experimental observations:
- A primary transient-kinetic study of published human glucokinase variants describes glucose recognition as an initial enzyme-glucose association followed by a conformational isomerization that favors the active form.
- For A456V, the study reports acceleration of the initial glucose-binding step to the glucose-free enzyme.
- For W99R, the study reports facilitation of the subsequent isomerization toward the active form.
- Both variants concern the same glucokinase reaction; these observations do not introduce a new substrate or reaction product.

**Question:** What mechanistic lesson follows from comparing A456V and W99R?

- **A.** A456V facilitates active-form isomerization whereas W99R accelerates initial glucose association, separating the variants by assigning their measured effects to different steps of this pathway.
- **B.** Both variants accelerate initial glucose association with the glucose-free enzyme, so their functional gains arise from a common effect before the conformational isomerization step.
- **C.** The variants affect different steps in the same binding and conformational pathway, so similar functional gains need not arise from the same microscopic mechanism.
- **D.** Both variants facilitate the subsequent active-form isomerization, so their functional gains arise from a common conformational effect after the initial glucose-association step has occurred.


## Astra’s worked solution

The supplied transient-kinetic evidence separates glucose recognition into two microscopic steps:

E + glucose ⇌ E·glucose ⇌ E*·glucose

Here, E denotes glucose-free glucokinase, the first transition is initial glucose association, and the second is the subsequent conformational isomerization toward the active form, E*.

The reported effects map differently onto this pathway:
- A456V accelerates initial glucose binding to the glucose-free enzyme—the first step.
- W99R facilitates the subsequent isomerization toward the active form—the second step.

Thus, initial substrate association and conversion of the bound enzyme into an active conformation are distinct opportunities to enhance function. Similar functional gains need not reflect the same microscopic mechanism: one variant can accelerate glucose association, while another facilitates the conformational transition that follows. These observations concern the same glucokinase reaction and do not imply a new substrate, a new product, or faster chemical catalysis itself.

Choice C states this lesson correctly. A reverses the experimental assignments. B incorrectly assigns both reported effects to initial association, whereas W99R is associated with the later isomerization. D incorrectly assigns both effects to isomerization, whereas A456V is reported to accelerate initial association. The sequence establishes the variant identities; the supplied kinetic observations establish the mechanistic distinction.

## Final answer

C

## Astra’s stated limitations

The kinetic assignments come from the supplied experimental observations, not from sequence alone. They do not establish that either variant affects only one step, quantify overall turnover or equilibrium glucose affinity, or identify a unique structural cause. The canonical sequence supplies reference coordinates, not complete assay-construct sequences.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Glucokinase / hexokinase-4** — [UniProt P35557](https://www.uniprot.org/uniprotkb/P35557/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly assigns A456V to initial glucose association and W99R to the later active-form isomerization.
- The two-step reversible pathway accurately organizes the supplied kinetic observations.
- Distinguishes binding and conformational changes from chemical catalysis, avoids exclusive one-step claims, and does not invent kinetic constants or structural causes.

Source support:

- Primary abstract, Results describing transient kinetic analysis
- The abstract groups A456V with variants accelerating initial glucose binding and W99R with variants facilitating isomerization to the active form.

Source qualifications:

- Do not infer identical catalytic-efficiency ratios, abundance changes or glucose responses from these qualitative findings.
- The full paper-specific purified construct has not been replayed; numbering matches the canonical human reference.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Gersing2023 Methods: pancreatic isoform ENST00000403799.8; same transcript is cross-referenced by current P35557-1. Paper also identifies P35557 isoform1 in its sequence analysis.
- This case is based on verified qualitative findings in the primary abstract. No uninspected figure/table number or unreported kinetic constant is assigned.

Primary references:

- [Biochemical basis of glucokinase activation and the regulation by glucokinase regulatory protein in naturally occurring mutations](https://pubmed.ncbi.nlm.nih.gov/17082186/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
