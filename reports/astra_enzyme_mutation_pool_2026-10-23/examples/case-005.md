# case-005 — Biotin ligase: mutation effect timecourse interpretation

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
BioID, paper construct definition: substitutions R118G; deletions delete 146–146.
TurboID: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V, K194I, M241T, S263P; deletions delete 146–146.

Supplied assay observations:
- Expression-normalized cellular blot comparisons report nearly comparable biotinylated product for TurboID at 10 minutes and older ligases including BioID at 18 hours.
- Quantitation excludes the ligase self-biotinylation band. These are cellular product endpoints, not purified-enzyme turnover measurements.

**Question:** Which interpretation correctly combines the timing and readout information?

- **A.** Normalizing the cellular endpoints converts the 108-fold duration difference into a direct measurement of the purified turnover-number ratio.
- **B.** Expression normalization makes the comparison time-matched, so both variants reach the reported product endpoint after the same accumulation window.
- **C.** TurboID accumulates similar normalized product sooner; the cellular endpoint comparison does not directly measure the purified turnover-number ratio.
- **D.** TurboID appears faster because the normalized product signal includes only the ligase self-biotinylation band rather than nearby-protein labeling.


## Astra’s worked solution

C correctly distinguishes faster cellular product accumulation from a purified-enzyme kinetic measurement.

The supplied observation is that TurboID at 10 minutes produces nearly comparable expression-normalized biotinylated product to older ligases, including BioID, at 18 hours. Since 18 hours equals 1,080 minutes, the accumulation windows differ by 1,080/10 = 108-fold. Thus, TurboID reaches a similar reported product endpoint in a much shorter interval under the cellular assay conditions.

Expression normalization adjusts the comparison for measured ligase abundance; it does not change the elapsed labeling times or turn endpoint signals into turnover numbers. Covalent biotinylation products accumulate over time, and their cellular abundance can depend on substrate accessibility, effective enzyme activity, and product persistence. A purified turnover number, kcat, instead describes catalytic turnovers per active enzyme per unit time under defined kinetic conditions. The supplied endpoint comparison does not directly measure that parameter or its ratio between variants. Even dividing endpoint signal by elapsed time would not by itself establish a purified kcat ratio.

The alternatives fail for distinct reasons:
- A incorrectly treats the 108-fold duration difference as a directly measured purified turnover-number ratio.
- B incorrectly equates expression normalization with time matching; the windows remain 10 minutes and 18 hours.
- D contradicts the stated quantitation: the ligase self-biotinylation band was excluded, so the quantified signal is not exclusively self-labeling.

Therefore, the supported interpretation is faster accumulation of comparable normalized non-self cellular biotinylation product, without a direct purified-turnover inference.

## Final answer

C

## Astra’s stated limitations

These cellular endpoints do not establish a purified turnover-number ratio or identify which sequence changes cause faster labeling. The supplied canonical sequence is a coordinate reference, not the complete tagged assay construct.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Biotin ligase** — [UniProt P06709](https://www.uniprot.org/uniprotkb/P06709/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly distinguishes a 108-fold endpoint-duration difference from an intrinsic turnover-number ratio.
- Expression normalization and exclusion of self-biotinylation are handled correctly.
- The decisive distinction is already stated in the supplied observations, so the question is relatively easy evidence reading despite a useful explanation.

Source support:

- Figure 2a–b; normalization in Figure 1g; accompanying Results
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- Do not translate elapsed-time ratios into an unmeasured catalytic constant.
- Correction concerns Supplementary Tables 2–7; variant definitions here use Supplementary Table 1 and the stated main/supplementary figures.

Primary references:

- [Efficient proximity labeling in living cells and organisms with TurboID](https://pmc.ncbi.nlm.nih.gov/articles/PMC6126969/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
