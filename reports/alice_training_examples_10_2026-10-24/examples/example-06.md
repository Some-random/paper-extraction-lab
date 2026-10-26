# 6. Separating membrane anchoring from topology

## Question

Protein sequence:

```text
MSSDFEGYEQDFAVLTAEITSKIARVPRLPPDEKKQMVANVEKQLEEARELLEQMDLEVREIPPQSRGMY
SNRMRSYKQEMGKLETDFKRSRIAYSDEVRNELLGDAGNSSENQRAHLLDNTERLERSSRRLEAGYQIAV
ETEQIGQEMLENLSHDREKIQRARDRLRDADANLGKSSRILTGMLRRIIQNRILLVILGIIVVIAILTAI
AFFVKGH
```

Infer this protein’s membrane-association architecture from the sequence. Identify the strongest evidence for an integral anchor rather than peripheral association, and explain how confidently you can assign the orientation of the large upstream region. What cellular information remains unresolved?

## Answer

A single near-C-terminal membrane anchor is strongly supported by the continuous hydrophobic stretch ILLVILGIIVVIAILTAIAFFV at residues 193–214, followed by KGH. This composition-based 22-residue call favors a bilayer-spanning helix over purely peripheral association; it is not an exact membrane-boundary measurement. The much longer upstream region is rich in charged and polar residues, without comparable hydrophobic stretches. The basic RRIIQNR flank at 186–192 supports a cytosolic upstream region through the positive-inside tendency, although assigning a membrane side is less secure than identifying the anchor. The sequence does not establish exact helix boundaries, insertion route or organelle destination.

## Assessment rubric

- Identifies the actual near-terminal hydrophobic stretch and short following tail as support for a single integral anchor.
- Accepts a justified approximate span ending at 213 or 214; distinguishing a hydrophobic-composition call from a precise helix boundary matters more than one-residue agreement.
- Contrasts an integral anchor with peripheral association using that sequence evidence, rather than assuming all membrane-associated proteins span the bilayer.
- Distinguishes strong anchor evidence from the weaker orientation inference; a cautious refusal to assign orientation is acceptable if explained.
- Does not infer Golgi/endosomal destination, exact measured boundaries or an insertion mechanism. Credit defensible alternatives that account for the hydrophobic segment and explain what evidence is missing.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency and rubric review. No independently documented blinded solver test or expert human validation is claimed for the current question.


Source identity: Vti1-rp2/Vti1a, [UniProt O89116](https://www.uniprot.org/uniprotkb/O89116/entry). The primary abstract supports a C-terminal anchor, cytoplasmic region and integral membrane behavior.

Two boundary descriptions are legitimate and should not be conflated:

| Quantity | Residues | Interpretation |
|---|---|---|
| Composition-based hydrophobic call in the reference answer | 193–214 | A continuous 22-residue hydrophobic stretch, with KGH following it. |
| UniProt annotated helical anchor | 193–213 | Annotated helix; V214 is assigned to the following vesicular region. |
| UniProt topological domains | 1–192 cytoplasmic; 214–217 vesicular | Annotation-based orientation and residue partition. |

The frozen UniProt record assigns all three topology features evidence code ECO:0000255 (sequence analysis). The RRIIQNR flank at 186–192 and the proposed cytosolic upstream region agree with that annotation. This is a source-consistency check, not independent experimental confirmation of a residue-exact boundary or proof that the current answer was produced blind. An extramembrane assignment alone does not specify the cytoplasmic side. The current reference answer remains a source-aware revision; its confidence must reflect the anonymous student input.

[Frozen UniProt record](../artifacts/example-06/frozen_uniprot_record.json) · [Final-review disposition](../final_review_v1.json). The historical coordinate-edit record is preserved; this clarification supersedes treating the one-residue composition/annotation difference as a sequence error.

Primary reference: [A 29-kilodalton Golgi soluble N-ethylmaleimide-sensitive factor attachment protein receptor (Vti1-rp2) implicated in protein trafficking in the secretory pathway](https://pubmed.ncbi.nlm.nih.gov/9705316/). The prior review used the primary abstract retrieved in search results; direct page opening encountered a browser challenge.

This is a source-aware assistant revision of the existing source-checked example into an open-response task. The original full sequence is unchanged. No new experiment, measurement or variant is proposed. The question uses only the anonymous sequence and standard family knowledge; the source identity and experimental findings remain in these review notes. No expert human validation or measured training benefit is claimed.

</details>
