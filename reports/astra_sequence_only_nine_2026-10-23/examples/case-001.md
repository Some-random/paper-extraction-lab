# case-001 — modified residue

Astra received only the student question below and the shared system instructions. Protein identity, gold answer, annotations and papers were withheld.

## Student question

Protein sequence:

```text
MTVSIQMAGNLWKVHVKAGDQIEKGQEVAILESMKMEIPIVADRSGIVKEVKKKEGDFVNEGDVLLELSN
STQ
```

Task: modified residue

Which residue is the most plausible attachment site for a biotin or lipoate group? Number the first amino acid as residue 1.

- **A.** Lysine at position 35
- **B.** Lysine at position 52
- **C.** Lysine at position 17
- **D.** Lysine at position 24

The sequence is line-wrapped for readability; the exact original prompt is retained in `questions.jsonl` and the request artifact.

## Astra’s worked solution

The most plausible site is A: lysine at position 35.

Biotin and lipoate are covalently attached through an amide bond to the side-chain ε-amino group of selected lysines in carrier domains. All four choices therefore have the appropriate residue chemistry; their surrounding sequences provide the useful distinction.

Counting the initial methionine as residue 1, residues 31–40 are LESMKMEIPI. Lys35 lies between Met34 and Met36, producing an MKM motif. This methionine-flanked lysine context is characteristic of the acceptor region in many biotin-carrier domains. It is the strongest positive clue for the attachment site in the supplied sequence.

Comparison with the alternatives:
- B, Lys52: residues 50–55 are EVKKKE. Lys52 begins a three-lysine cluster, but a cluster of lysines is not itself a biotin/lipoate attachment signal.
- C, Lys17: residues 15–19 are HVKAG, without the characteristic MKM context.
- D, Lys24: residues 22–26 are IEKGQ, likewise without that context.

Cofactor attachment depends on recognition of the folded carrier domain, so absence of MKM does not categorically exclude a lysine, especially for lipoylation. Nevertheless, Lys35 has a recognizable biotin-acceptor-like sequence context that the alternatives lack, making it the best-supported choice.

## Final answer

A

## Astra’s stated limitations

The sequence strongly favors one candidate site but does not establish that modification actually occurs. The MKM context is particularly suggestive of biotinylation, not a universal motif for both biotin and lipoate attachment. Cofactor identity and lysine accessibility cannot be established conclusively from this sequence alone.

Confidence reported by Astra: high.

## Post-generation verification

The following information was **not supplied to Astra**.

Verified source identity: **Biotin/lipoyl attachment protein** — [UniProt C0H419](https://www.uniprot.org/uniprotkb/C0H419/entry).

[Frozen UniProt annotation](../artifacts/case-001/uniprot_record.json), withheld from Astra.

Source-supported answer: **A**. Astra’s selected answer matches it.

The primary study identified a natural 73-amino-acid protein from Bacillus subtilis. It characterized both unmodified and biotin-modified forms by solution NMR and placed the attached biotin on Lys35. The canonical sequence also has lysines at all four proposed answer positions, so the correct site is not established merely by checking that the residue is a lysine.

Scientific review: Qualified modification-site inference.

- MKM is a useful biotin-carrier clue, not a universal attachment rule for biotin or lipoate. The explanation retains that limitation.
- Primary biotin-carrier work supports the motif heuristic and folded-domain recognition: https://doi.org/10.1042/bj3290589 . The BLAP paper independently supports Lys35.
- The source modification was demonstrated during heterologous expression; native modification is not established.

Moderate biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- Biotin and lipoate modification were demonstrated when the protein was expressed in E. coli; the native modification in B. subtilis remains unknown.
- The exact modification site requires family knowledge or experimental evidence. An explanation must not pretend that any isolated lysine or short motif proves modification.
- The source record is a complete reviewed 73-residue protein, not a truncated construct; the mature-chain annotation removes the initial methionine.

Papers and experimental references:

- [Identification and solution structures of a single domain biotin/lipoyl attachment protein from Bacillus subtilis.](https://pubmed.ncbi.nlm.nih.gov/16699181/). Primary abstract describes the natural 73-residue protein, modification in E. coli and NMR-supported biotin attachment at Lys35. Review scope: Primary abstract retrieved through Europe PMC; cached UniProt record and complete-sequence annotation inspected.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.
