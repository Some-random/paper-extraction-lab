# case-021 — Biotin ligase: single substitution characterization

**Assistant selection tier: strong.** Generation status: `completed`.

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
G3Δ, published intermediate: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V; deletions delete 1–63, delete 146–146.
miniTurbo: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V, K194I; deletions delete 1–63, delete 146–146.

Supplied assay observations:
- Supplementary Table 1 defines miniTurbo as G3Δ with one additional substitution, K194I in the reference numbering.
- The published cellular screening reports higher labeling activity for this change without increased signal when exogenous biotin is omitted.

**Question:** Which characterization combines the controlled sequence difference and the two readouts correctly?

- **A.** The added K194I substitution raises both activity and the no-added-biotin signal in G3Δ, producing a measured background tradeoff.
- **B.** The added K194I substitution raises activity in the G3Δ background without increasing the measured no-added-biotin signal.
- **C.** The compared enzyme cores differ at multiple internal sites, associating the higher activity with combined substitutions rather than the stated single difference.
- **D.** The added K194I substitution lowers the no-added-biotin signal but leaves the measured activity at the G3Δ level.


## Astra’s worked solution

The controlled comparison is miniTurbo versus G3Δ, not either variant versus canonical wild type. Both variants share all 11 substitutions listed for G3Δ and both deletions, covering reference positions 1–63 and position 146. miniTurbo has exactly one additional enzyme-core substitution: K194I. Thus, although both variants differ substantially from wild type, they differ from each other at only this one retained position.

The supplied cellular screening reports two distinct outcomes: adding K194I increases labeling activity, while the measured signal does not increase when exogenous biotin is omitted. The no-added-biotin condition is an operational background readout; it does not imply that cells contain no endogenous biotin. Likewise, an absence of increased signal does not establish zero background or a background reduction.

These observations directly support B: K194I raises activity in the G3Δ background without increasing the measured no-added-biotin signal.

A incorrectly asserts an increased background signal. C mistakes shared differences from wild type for differences between the compared cores. D contradicts the observed activity increase and additionally asserts a background reduction that is not supplied. The justified conclusion is therefore improved cellular labeling performance without an observed background increase, rather than a demonstrated change in any particular catalytic or binding mechanism.

## Final answer

B

## Astra’s stated limitations

These qualitative cellular readouts do not establish a molecular mechanism or distinguish effects on intrinsic catalysis from expression, stability, or other determinants of labeling. The conclusion applies to K194I in the G3Δ background under the supplied screening conditions, not necessarily to other backgrounds or assay constructs.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Biotin ligase** — [UniProt P06709](https://www.uniprot.org/uniprotkb/P06709/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly distinguishes the single difference between G3Δ and miniTurbo from their many shared differences relative to canonical wild type.
- Jointly interprets increased activity and unchanged no-added-biotin signal, without equating unchanged background with zero or reduced background.
- Keeps the conclusion specific to the tested background and cellular assay.

Source support:

- Supplementary Table 1; Methods subsection on miniTurbo evolution; final/intermediate variant comparison in Figure 1e–g
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- Published screening describes this comparison qualitatively; no unreported numerical effect size is supplied.
- Correction concerns Supplementary Tables 2–7; variant definitions here use Supplementary Table 1 and the stated main/supplementary figures.

Primary references:

- [Efficient proximity labeling in living cells and organisms with TurboID](https://pmc.ncbi.nlm.nih.gov/articles/PMC6126969/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
