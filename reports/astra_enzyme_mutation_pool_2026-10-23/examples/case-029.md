# case-029 — Biotin ligase: deletion effect substrate controls

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
G3, published intermediate: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V; deletions delete 146–146.
G3Δ, published intermediate: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V; deletions delete 1–63, delete 146–146.

Supplied assay observations:
- G3Δ removes reference residues 1–63 from the G3 enzyme core and retains the listed internal substitutions.
- G3 gives labeling without exogenous biotin in regular medium; the signal disappears in biotin-depleted medium. The G3Δ comparison shows reduced pre-addition labeling.

**Question:** Which interpretation integrates the deletion comparison with the substrate-depletion control?

- **A.** G3 retains its ordinary-medium labeling after biotin depletion, placing the deletion-associated signal change outside the substrate-dependent background.
- **B.** The N-terminal deletion leaves pre-addition labeling unchanged, so substrate depletion is the only supplied condition that reduces the signal.
- **C.** The G3 versus G3Δ comparison isolates internal A146 deletion while both variants retain the same N-terminal domain.
- **D.** Ambient biotin supports pre-addition labeling by G3, and the published N-terminal deletion reduces that signal in the tested comparison.


## Astra’s worked solution

D integrates both supplied observations.

The substrate-depletion control shows that G3 labeling depends on available biotin: labeling occurs in regular medium without exogenous biotin, but disappears in biotin-depleted medium. “Without exogenous biotin” therefore does not mean “without biotin.” Ambient biotin in the regular-medium condition can supply the substrate needed for pre-addition labeling.

The variant comparison addresses a different issue: the magnitude of that pre-addition signal. G3 and G3Δ share all listed internal substitutions and the deletion at reference position 146. G3Δ additionally lacks reference residues 1–63 and shows reduced pre-addition labeling. Thus, the supplied comparison supports an association between the N-terminal deletion and reduced background labeling under the tested conditions; it does not identify a particular binding or catalytic mechanism.

The alternatives conflict with the supplied facts:
- A incorrectly says G3 labeling persists after biotin depletion; the signal disappears.
- B incorrectly says the N-terminal deletion leaves labeling unchanged; the comparison shows a reduction.
- C incorrectly identifies the isolated change as the internal A146 deletion and says both variants retain the same N-terminal region. The internal deletion is shared, whereas residues 1–63 are removed only in G3Δ.

Therefore, ambient biotin supports G3 pre-addition labeling, and the published N-terminal deletion reduces that signal in the tested comparison.

## Final answer

D

## Astra’s stated limitations

The observations establish substrate dependence and reduced labeling in the deletion comparison, but not the molecular mechanism of that reduction. They do not distinguish altered biotin binding or catalytic activity from differences in enzyme abundance or stability, nor show that G3Δ eliminates background labeling entirely. The reference sequence excludes assay tags and fusions.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Biotin ligase** — [UniProt P06709](https://www.uniprot.org/uniprotkb/P06709/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly uses biotin depletion to distinguish no added biotin from absence of available substrate.
- Compares the distinguishing N-terminal deletion against the shared internal deletion and substitutions.
- Explains the reduced background phenotype without inventing a binding constant, altered catalytic mechanism or complete elimination of background.

Source support:

- Supplementary Figure 3e; Supplementary Table 1
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- This cellular phenotype does not supply a measured binding constant or uniquely establish the molecular cause of the deletion effect.
- Correction concerns Supplementary Tables 2–7; variant definitions here use Supplementary Table 1 and the stated main/supplementary figures.

Primary references:

- [Efficient proximity labeling in living cells and organisms with TurboID](https://pmc.ncbi.nlm.nih.gov/articles/PMC6126969/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
