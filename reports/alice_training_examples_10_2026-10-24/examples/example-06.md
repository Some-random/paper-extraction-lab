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

The sequence strongly supports a protein with one membrane anchor near its C terminus and a much larger region outside the bilayer. Its most conspicuous feature is ILLVILGIIVVIAILTAIAFFV at residues 193–214: a continuous 22-residue hydrophobic stretch followed by only KGH.

That combination of length, composition and position is appropriate for a membrane-spanning alpha helix. There are no charged residues within this stretch, whereas the surrounding protein contains many charged and polar residues. Placing such a long hydrophobic segment in the lipid bilayer provides a more coherent interpretation than treating the entire protein as a soluble domain that associates only peripherally with a membrane. Peripheral association can occur through interactions with lipids or other proteins, but does not by itself explain this pronounced hydrophobic tail.

The upstream region does not contain several comparable hydrophobic stretches. The sequence therefore supports one anchor rather than a multipass membrane bundle. The anchor’s near-terminal position and very short following tail are also consistent with a tail-anchored architecture. This is an architectural assignment, not identification of the cellular machinery or route that inserts it.

Orientation is a separate, less certain inference. The RRIIQNR segment at residues 186–192 places several basic residues immediately before the candidate anchor. This agrees with the positive-inside tendency, in which positively charged flanks often occur on the cytosolic side of membrane-spanning helices. It therefore supports a cytosolic location for the large upstream region. However, a tendency is not a direct observation, and saying that a region lies outside the bilayer does not by itself identify which membrane side it occupies.

Residues 193–214 describe a hydrophobic-composition window, not a measured helix boundary. A structural boundary could differ slightly without changing the overall conclusion. The sequence alone does not establish the exact membrane-spanning endpoints, prove orientation, identify the insertion pathway or distinguish a Golgi, endosomal or other membrane destination. Confidence is strongest for the single C-terminal anchor and weaker for those more specific cellular assignments.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


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
