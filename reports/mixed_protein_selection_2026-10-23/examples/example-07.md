# 7. Distinguishing heme from other cofactors

## Question

Protein sequence:

```text
MTIASSTASSEFLKNPYSFYDTLRAVHPIYKGSFLKYPGWYVTGYEETAAILKDARFKVRTPLPESSTKY
QDLSHVQNQMMLFQNQPDHRRLRTLASGAFTPRTTESYQPYIIETVHHLLDQVQGKKKMEVISDFAFPLA
SFVIANIIGVPEEDREQLKEWAASLIQTIDFTRSRKALTEGNIMAVQAMAYFKELIQKRKRHPQQDMISM
LLKGREKDKLTEEEAASTCILLAIAGHETTVNLISNSVLCLLQHPEQLLKLRENPDLIGTAVEECLRYES
PTQMTARVASEDIDICGVTIRQGEQVYLLLGAANRDPSIFTNPDVFDITRSPNPHLSFGHGHHVCLGSSL
ARLEAQIAINTLLQRMPSLNLADFEWRYRPLFGFRALEELPVTFE
```


**Question:** Which cofactor is most strongly supported by this protein sequence?

**Choices:**

- **A.** FAD
- **B.** FMN
- **C.** A four-iron four-sulfur cluster
- **D.** Heme

## Answer

D. Heme is the most strongly supported cofactor.

The decisive evidence is a coherent combination of cytochrome P450 sequence signatures, rather than simply the presence of cysteine or histidine residues.

1. Heme-binding signature: residues 338–347 are FGHGHHVCLG. This matches FxxGxxxCxG, where x denotes any residue. In P450 proteins, the cysteine at this motif position supplies the axial sulfur ligand to the heme iron. Thus, Cys345 is a strong candidate for a heme-ligating cysteine. This is the most direct cofactor-related clue.

2. Supporting P450 core signature: residues 274–277 are ECLR, matching the characteristic E-x-x-R motif associated with the P450 K helix. This motif supports the fold assignment; it is not itself a direct metal-binding motif.

3. Supporting catalytic-region signature: residues 235–240 are AGHETT. Its acidic residue and adjacent threonines are consistent with the conserved I-helix region used in oxygen activation by many P450 enzymes. Assigning this segment to an I helix is an inference from the motif context, not an observed secondary structure.

These features occur in the expected sequence order: the I-helix-like segment, the E-x-x-R motif, and then the cysteine-containing heme-binding loop toward the C terminus. Together they strongly support a P450-family protein, whose defining prosthetic group is heme.

Comparison with the alternatives:
- A. FAD and B. FMN: flavin-binding proteins are diverse, so neither cofactor can be excluded merely by the absence of one universal motif. Nevertheless, the observed combination specifically supports a P450 heme-binding domain, not a flavin-binding assignment.
- C. A four-iron four-sulfur cluster: cysteines can ligate iron–sulfur clusters, but cysteine presence alone is insufficient evidence. Here the key cysteine occurs in a characteristic heme-thiolate signature reinforced by two other P450-associated motifs.
- D. Heme: directly explains the predicted cysteine–iron coordination and the overall motif combination, making it the most defensible choice.

**Final answer: D**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

Primary structural Results directly support heme, its coordinating cysteine and the catalytic-region facts. Assigning a family from sequence remains an inference; exact catalytic properties require experiments.

### Answer limitations

This is a sequence-based cofactor prediction, not direct evidence of bound heme. The sequence does not establish actual cofactor occupancy, substrate specificity, or catalytic reaction.

### References and source review

The following information was **not supplied to AI**.

Verified source identity: **Biotin biosynthesis cytochrome P450** — [UniProt P53554](https://www.uniprot.org/uniprotkb/P53554/entry).

[Frozen UniProt annotation](../../astra_sequence_only_nine_2026-10-23/artifacts/case-004/uniprot_record.json), withheld from AI.

Source-supported answer: **D**. AI’s selected answer matches it.

The primary structural study visualizes the enzyme with its carrier-protein-bound substrate above an active-site heme. It identifies Cys345 as the proximal sulfur ligand to the heme iron. These observations directly support heme as the cofactor.

Scientific review: Strong sequence-based explanation.

- The cysteine heme-ligand signature, ExxR motif and I-helix-like region form a coherent P450-family argument. Actual heme occupancy and substrate specificity remain unmeasured.

Strong biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- A cysteine by itself does not prove heme binding; the relevant sequence context and protein-family evidence matter.
- Do not claim that the paper demonstrates a covalent bond attaching the heme group to the polypeptide. The inspected text describes a cysteine thiolate ligand coordinating heme iron.
- Identifying the cofactor does not establish the exact substrate, reaction specificity or biotin-biosynthesis role from the anonymous sequence alone.

Papers and experimental references:

- [Structural insights from a P450 Carrier Protein complex reveal how specificity is achieved in the P450BioI ACP complex.](https://pmc.ncbi.nlm.nih.gov/articles/PMC2572933/). The structure and Active Site Architecture section directly establish heme and the coordinating Cys345 residue. Review scope: Primary full-text paper, abstract, structural Results and Active Site Architecture section inspected.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.

[Original source records and unchanged AI output](../../astra_sequence_only_nine_2026-10-23/examples/case-004.md)

</details>
