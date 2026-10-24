# case-010 — PTEN phosphatase: mutation substrate specificity

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

Published variants: G129E.

Supplied experimental observations:
- A primary purified-protein study measured phosphate release from two PTEN substrates: the phosphoinositide lipid PIP3 and a phosphorylated poly(Glu,Tyr) protein-substrate preparation.
- Compared with wild type, G129E shows approximately 90% less activity against PIP3, but retains activity against the phosphorylated poly(Glu,Tyr) substrate.
- The report does not supply a universal claim about every possible protein substrate or a direct measurement of folding stability.

**Question:** Which conclusion is best supported by this substrate comparison?

- **A.** G129E preferentially impairs the protein-substrate reaction, while lipid dephosphorylation remains near the wild-type level under the measured conditions.
- **B.** G129E eliminates detectable activity on both tested substrates, supporting broad catalytic loss rather than separation of the measured substrate activities.
- **C.** G129E strongly impairs lipid dephosphorylation while retaining measured protein-substrate activity, showing that the two substrate activities can be affected differently.
- **D.** G129E preserves lipid dephosphorylation; its lower PIP3 signal measures reduced enzyme abundance, whereas the protein-substrate assay directly measures folding stability.


## Astra’s worked solution

C is directly supported by the substrate comparison. Approximately 90% less PIP3 activity means that G129E retains roughly 10% of the wild-type activity in that lipid-substrate assay: a strong impairment, not preservation and not necessarily complete abolition. In contrast, activity remains detectable against the phosphorylated poly(Glu,Tyr) preparation. Thus, the mutation affects the two measured substrate reactions differently. The supplied description does not quantify how closely the retained protein-substrate activity matches wild type.

The sequence provides a mechanistically relevant context: Gly129 lies in the phosphatase active-site loop containing catalytic Cys124 and Arg130. Replacing glycine with a larger acidic glutamate side chain could alter substrate accommodation or local active-site chemistry, allowing different effects on lipid and protein-substrate processing. This is a plausible interpretation, not a demonstrated structural mechanism; the assay observations, rather than sequence alone, establish the differential activities.

A reverses the observed substrate effects. B contradicts the retained protein-substrate activity and the reported residual PIP3 activity. D incorrectly describes lipid dephosphorylation as preserved and misidentifies the assay readouts: phosphate release measures substrate dephosphorylation, not enzyme abundance or folding stability. Therefore, C is the supported conclusion.

## Final answer

C

## Astra’s stated limitations

The conclusion applies to the two tested substrates under the reported assay conditions. Retained activity on phosphorylated poly(Glu,Tyr) does not establish unchanged activity on every protein substrate. The observations do not directly measure folding stability, enzyme abundance, substrate binding, or the precise catalytic step affected.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PTEN phosphatase** — [UniProt P60484](https://www.uniprot.org/uniprotkb/P60484/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly converts approximately 90% less lipid activity into approximately 10% residual activity, while not inventing a quantitative protein-substrate value.
- Correctly identifies substrate-dependent functional separation and restricts the claim to the tested substrates.
- The bulky acidic substitution in the active-site loop is offered as a plausible interpretation, not a demonstrated structure or precise kinetic mechanism.

Source support:

- Figure 1A; Results paragraph comparing purified WT, C124S and G129E on PIP3 and polyGluTyr
- G129E reduces lipid phosphatase activity by approximately 90% while retaining activity against polyGluTyr.

Source qualifications:

- Retained polyGluTyr activity does not prove every physiological protein substrate is processed normally.
- No causal structural mechanism or folding-stability value is measured in this question.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Mighell2018 Methods: NM_000314.6, corresponding 403-aa NP_000305; current canonical record cross-references NP_000305.3. Full paper-assay construct sequence still requires final replay before release.
- The qualitative retention of polyGluTyr activity is supported; do not invent an exact percentage for that substrate.

Primary references:

- [The lipid phosphatase activity of PTEN is critical for its tumor supressor function](https://pmc.ncbi.nlm.nih.gov/articles/PMC24850/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
