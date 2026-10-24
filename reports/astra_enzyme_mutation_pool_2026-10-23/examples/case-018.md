# case-018 — PTEN phosphatase: mutation substrate specificity

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

Reference protein sequence (P60484, full canonical wild-type backbone; coordinate reference only):

```text
MTAIIKEIVSRNKRRYQEDGFDLDLTYIYPNIIAMGFPAERLEGVYRNNIDDVVRFLDSKHKNHYKIYNL
CAERHYDTAKFNCRVAQYPFEDHNPPQLELIKPFCEDLDQWLSEDDNHVAAIHCKAGKGRTGVMICAYLL
HRGKFLKAQEALDFYGEVRTRDKKGVTIPSQRRYVYYYSYLLKNHLDYRPVALLFHKMMFETIPMFSGGT
CNPQFVVCQLKVKIYSSNSGPTRREDKFMYFEFPQPLPVCGDIKVEFFHKQNKMLKKDKMFHFWVNTFFI
PGPEETSEKVENGSLCDQEIDSICSIERADNDKEYLVLTLTKNDLDKANKDKANRYFSPNFKVKLYFTKT
VEEPSNPEASSSTSVTPDVSDNEPDHYRYSDTTDSDPENEPFDEDQHTQITKV
```


All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.

Published variants: Y138L.

Supplied experimental observations:
- A primary biochemical study compared wild-type PTEN and Y138L using PIP3 as a lipid substrate and phosphorylated poly(Glu,Tyr) as a protein-substrate preparation.
- Further kinetic analysis found Y138L lipid phosphatase activity essentially indistinguishable from wild type under the tested conditions.
- Against the phosphorylated protein substrate, Y138L activity was approximately 3% of wild type and was frequently undetectable.

**Question:** Which description of Y138L best fits both readouts?

- **A.** Y138L increases the protein-substrate reaction while preserving lipid activity, indicating preferential enhancement of protein dephosphorylation rather than selective loss of that activity.
- **B.** Y138L lowers both tested activities to approximately 3% of wild type, supporting a similar impairment across the lipid and protein-substrate reactions.
- **C.** Y138L preserves the tested protein-substrate activity while strongly reducing lipid activity, so its principal defect is selective loss of PIP3 processing.
- **D.** Y138L preserves the tested lipid activity while strongly reducing protein-substrate activity, so a single total-activity category would obscure the substrate-dependent effect.


## Astra’s worked solution

Y138L replaces the reference Tyr138 with leucine, removing an aromatic, hydroxyl-bearing side chain. That chemical change alone cannot determine which phosphatase reaction will be affected; the supplied assays provide the decisive evidence.

The two readouts must be considered separately:
- Lipid substrate: kinetic analysis found Y138L activity against PIP3 essentially indistinguishable from wild type under the tested conditions. This supports preservation of the tested lipid phosphatase activity.
- Protein-substrate preparation: activity against phosphorylated poly(Glu,Tyr) was approximately 3% of wild type, corresponding to roughly a 97% reduction, and was frequently undetectable. This supports a severe loss of the tested protein-substrate activity. Undetectability does not establish that activity is absolutely zero.

Different substrates impose different recognition and productive-positioning requirements on an enzyme. Consequently, retaining lipid dephosphorylation does not require retaining the protein-substrate reaction. Preserved PIP3 activity argues against uniform catalytic inactivation under these conditions, while the protein-substrate result demonstrates a strongly substrate-dependent impairment. A single total-activity label would conceal this distinction.

A is inconsistent with the reduced, rather than increased, protein-substrate activity. B incorrectly assigns the approximately 3% result to both substrates. C reverses the observed pattern. D correctly describes preserved tested lipid activity together with strongly reduced protein-substrate activity.

## Final answer

D

## Astra’s stated limitations

The conclusion applies to PIP3 and phosphorylated poly(Glu,Tyr) under the tested conditions, not necessarily to every physiological substrate. These readouts do not establish whether the protein-substrate defect arises from altered binding, productive substrate positioning, or catalytic chemistry, and they do not separately measure expression or stability.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PTEN phosphatase** — [UniProt P60484](https://www.uniprot.org/uniprotkb/P60484/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly separates preserved PIP3 activity from approximately 3% protein-substrate activity and computes the corresponding approximately 97% reduction.
- Correctly distinguishes frequently undetectable activity from a demonstrated absolute zero.
- Explains different substrate-recognition and positioning requirements without claiming that the precise microscopic cause was measured.

Source support:

- Figure 1e/f; Figure 2 and Supplementary Figure S2; Results following the initial mutant screen
- Y138L lipid activity is essentially indistinguishable from WT, whereas polyGluTyr-P activity is approximately 3% of WT and often undetectable.

Source qualifications:

- The answer applies to the tested substrates and conditions.
- Do not infer unchanged thermal stability or cellular expression from these activity readouts.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Mighell2018 Methods: NM_000314.6, corresponding 403-aa NP_000305; current canonical record cross-references NP_000305.3. Full paper-assay construct sequence still requires final replay before release.
- Figure 1d describes GST fusion production and tag removal. The exact full assay construct sequence has not been independently reconstructed.

Primary references:

- [Suppression of cellular proliferation and invasion by the concerted lipid and protein phosphatase activities of PTEN](https://pmc.ncbi.nlm.nih.gov/articles/PMC2816976/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
