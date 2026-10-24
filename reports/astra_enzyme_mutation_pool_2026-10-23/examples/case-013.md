# case-013 — Biotin ligase: published variant tradeoff

**Assistant selection tier: moderate.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

Reference protein sequence (canonical wild-type backbone; coordinate reference only):

```text
MKDNTVPLKLIALLANGEFHSGEQLGETLGMSRAAINKHIQTLRDWGVDVFTVPGKGYSLPEPIQLLNAK
QILGQLDGGSVAVLPVIDSTNQYLLDRIGELKSGDACIAEYQQAGRGRRGRKWFSPFGANLYLSMFWRLE
QGPAAAIGLSLVIGIVMAEVLRKLGADKVRVKWPNDLYLQDRKLAGILVELTGKTGDAAQIVIGAGINMA
MRRVEESVVNQGWITLQEAGINLDRNTLAAMLIRELRAALELFEQEGLAPYLSRWEKLDNFINRPVKLII
GDKEIFGISRGIDKQGALLLEQDGIIKPWMGGEISLRSAEK
```


Reference: P06709. All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded. The sequence is not the complete tagged assay construct.

Published variant identities:
TurboID: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V, K194I, M241T, S263P; deletions delete 146–146.
miniTurbo: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V, K194I; deletions delete 1–63, delete 146–146.

Supplied assay observations:
- The published cellular comparison finds miniTurbo less active overall than TurboID.
- miniTurbo also produces less labeling before exogenous biotin addition. The variants differ at multiple positions and in N-terminal-domain retention.

**Question:** A dataset annotation must distinguish induced labeling strength from control over when labeling begins. Which annotation is best supported?

- **A.** miniTurbo reduces pre-addition labeling but also lowers overall activity, separating temporal-background control from the strongest labeling signal.
- **B.** miniTurbo provides stronger overall labeling than TurboID, at the cost of more labeling before exogenous biotin addition.
- **C.** miniTurbo reduces pre-addition labeling while maintaining the same overall labeling activity as TurboID after biotin addition.
- **D.** Both variants have the same pre-addition labeling, while miniTurbo has lower overall activity following exogenous biotin addition.


## Astra’s worked solution

A is supported by both supplied observations: miniTurbo has lower overall cellular labeling activity than TurboID, and it produces less labeling before exogenous biotin addition. The annotation must preserve both findings rather than treating reduced background as evidence of equally strong or stronger induced labeling.

Mechanistically, biotin-dependent proximity-labeling enzymes can use biotin already available in cells. Therefore, before exogenous biotin addition does not necessarily mean before any labeling can occur. Reduced pre-addition labeling supports lower temporal background, whereas overall labeling strength is a separate performance dimension. This does not demonstrate an absolute off state or a particular activation speed.

The sequence definitions also prevent a single-change causal interpretation. miniTurbo lacks canonical residues 1–63, which TurboID retains, and their substitution sets differ. The cellular observations therefore compare complete variants with multiple differences; they do not isolate the effect of the N-terminal deletion or any individual substitution.

The alternatives fail as follows:
- B reverses both observations, claiming stronger overall labeling and more pre-addition labeling for miniTurbo.
- C correctly states reduced pre-addition labeling but replaces the reported activity reduction with an unsupported claim of equal activity after addition.
- D retains the lower-activity distinction but contradicts the observed reduction in pre-addition labeling.

Thus A correctly separates miniTurbo's lower pre-addition background from TurboID's stronger overall labeling activity.

## Final answer

A

## Astra’s stated limitations

The observations are qualitative cellular comparisons. They do not establish zero pre-addition labeling, a better induced-to-background ratio, or precise switching kinetics. They also cannot separate contributions from catalysis, biotin binding, expression, stability, or assay-construct context, nor assign the differences to a particular mutation or deletion. The reference sequence is not the complete tagged assay construct.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Biotin ligase** — [UniProt P06709](https://www.uniprot.org/uniprotkb/P06709/entry).

Source-supported reference answer: **A**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly preserves both the lower overall activity and lower pre-addition labeling findings.
- Explains endogenous biotin and avoids claiming zero background, a superior induced/background ratio, or isolated causality from a multimutant comparison.
- The answer is mainly a careful synthesis of two explicitly supplied qualitative observations.

Source support:

- Figure 2a–b; Supplementary Figure 6; accompanying Results
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- This compares published multimutant variants; it does not isolate a single causal substitution.
- Correction concerns Supplementary Tables 2–7; variant definitions here use Supplementary Table 1 and the stated main/supplementary figures.

Primary references:

- [Efficient proximity labeling in living cells and organisms with TurboID](https://pmc.ncbi.nlm.nih.gov/articles/PMC6126969/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
