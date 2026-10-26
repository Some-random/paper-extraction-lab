# 6. Separating membrane anchoring from topology

## Question

Protein sequence:

```text
MSSDFEGYEQDFAVLTAEITSKIARVPRLPPDEKKQMVANVEKQLEEARELLEQMDLEVREIPPQSRGMY
SNRMRSYKQEMGKLETDFKRSRIAYSDEVRNELLGDAGNSSENQRAHLLDNTERLERSSRRLEAGYQIAV
ETEQIGQEMLENLSHDREKIQRARDRLRDADANLGKSSRILTGMLRRIIQNRILLVILGIIVVIAILTAI
AFFVKGH
```

**Question:** Which overall membrane-association architecture best fits this protein sequence?

**Choices:**

- **A.** Peripheral membrane association without a membrane-spanning segment.
- **B.** A single C-terminal membrane anchor with a large upstream domain.
- **C.** Multiple membrane-spanning segments distributed throughout the protein.
- **D.** An N-terminal cleaved signal peptide followed by a soluble domain.

## Answer

**Answer: B.**

The sequence strongly supports a protein with one membrane anchor near its C terminus and a much larger region outside the bilayer. Its most conspicuous feature is ILLVILGIIVVIAILTAIAFFV at residues 193–214: a continuous 22-residue hydrophobic stretch followed by only KGH.

That combination of length, composition and position is appropriate for a membrane-spanning alpha helix. There are no charged residues within this stretch, whereas the surrounding protein contains many charged and polar residues. Placing such a long hydrophobic segment in the lipid bilayer provides a more coherent interpretation than the purely peripheral membrane association in A. Peripheral association can occur through interactions with lipids or other proteins, but does not by itself explain this pronounced hydrophobic tail.

The upstream region does not contain several comparable hydrophobic stretches. The sequence therefore supports one anchor rather than the multipass membrane bundle in C. Its C-terminal position also differs from the N-terminal cleaved signal peptide proposed in D. The anchor’s near-terminal position and very short following tail are also consistent with a tail-anchored architecture. This is an architectural assignment, not identification of the cellular machinery or route that inserts it.

Orientation is a separate, less certain inference. The RRIIQNR segment at residues 186–192 places several basic residues immediately before the candidate anchor. This agrees with the positive-inside tendency, in which positively charged flanks often occur on the cytosolic side of membrane-spanning helices. It therefore supports a cytosolic location for the large upstream region. However, a tendency is not a direct observation, and saying that a region lies outside the bilayer does not by itself identify which membrane side it occupies.

Residues 193–214 describe a hydrophobic-composition window, not a measured helix boundary. A structural boundary could differ slightly without changing the overall conclusion. The sequence alone does not establish the exact membrane-spanning endpoints, prove orientation, identify the insertion pathway or distinguish a Golgi, endosomal or other membrane destination. Confidence is strongest for the single C-terminal anchor and weaker for those more specific cellular assignments.

<details>
<summary>Sources and qualifications</summary>

Source identity: Vti1-rp2/Vti1a, [UniProt O89116](https://www.uniprot.org/uniprotkb/O89116/entry). The primary abstract supports a C-terminal anchor, cytoplasmic region and integral membrane behavior.

| Evidence | Residues | Interpretation |
|---|---|---|
| Hydrophobic composition of the supplied sequence | 193–214 | A continuous 22-residue hydrophobic stretch, followed by KGH. |
| UniProt annotated helical anchor | 193–213 | Annotated helix; V214 belongs to the following vesicular region. |
| UniProt topological domains | 1–192 cytoplasmic; 214–217 vesicular | Annotation-based orientation and residue partition. |

The [frozen UniProt record](../artifacts/example-06/frozen_uniprot_record.json) assigns all three topology features evidence code ECO:0000255 (sequence analysis). The RRIIQNR flank at residues 186–192 and the proposed cytosolic upstream region agree with that annotation. This agreement does not independently demonstrate residue-exact boundaries or orientation: the annotation itself is based on sequence analysis. An extramembrane assignment alone does not specify the cytoplasmic side. The answer’s confidence is therefore based on the anonymous sequence, with stronger evidence for the anchor than for orientation.

Primary reference: [A 29-kilodalton Golgi soluble N-ethylmaleimide-sensitive factor attachment protein receptor (Vti1-rp2) implicated in protein trafficking in the secretory pathway](https://pubmed.ncbi.nlm.nih.gov/9705316/). The abstract’s experimental cellular context supports the broad topology; it does not turn either sequence-based window into a measured membrane boundary.

</details>
