# 5. Recognizing repeated calcium-binding loops

## Question

Protein sequence:

```text
MPFHPVTAALMYRGIYTVPNLLSEQRPVDIPEDELEEIREAFKVFDRDGNGFISKQELGTAMRSLGYMPN
EVELEVIIQRLDMDGDGQVDFEEFVTLLGPKLSTSGIPEKFHGTDFDTVFWKCDMQKLTVDELKRLLYDT
FCEHLSMKDIENIIMTEEESHLGTAEECPVDVETCSNQQIRQTCVRKSLICAFAIAFIISVMLIAANQVL
RSGMK
```

**Question:** Which binding role is most consistent with the soluble region of this protein?

**Choices:**

- **A.** Binding calcium through EF-hand domains.
- **B.** Binding zinc through C2H2 zinc-finger domains.
- **C.** Binding heme within a peroxidase domain.
- **D.** Binding FAD within an oxidoreductase domain.

## Answer

**Answer: A.**

The likely soluble region supports an EF-hand calcium-binding architecture, with two particularly convincing candidate loops. They are DRDGNGFISKQE at residues 46–57 and DMDGDGQVDFEE at residues 82–93.

An EF hand contains a calcium-binding loop of about 12 residues between two helices. The informative feature here is the arrangement of potential ligands within each loop. In DRDGNGFISKQE, positions 1, 3 and 5 are Asp, Asp and Asn. In DMDGDGQVDFEE, those positions are all Asp. Both loops have glycine at position 6 and glutamate at position 12. Asp, Asn and Glu provide oxygen-containing groups compatible with calcium coordination. Glycine can accommodate the tight loop geometry, while the terminal glutamate commonly contributes its carboxylate to calcium binding. The repeated positional pattern is therefore chemically and structurally coherent.

This is stronger evidence than high acidic content alone. A nonspecific acidic region could interact with positively charged ions, but acidity does not specify a calcium-binding fold. Two separate segments with the same ligand-compatible positions, loop length and conserved glycine are more suggestive of repeated binding modules than an arbitrary Asp/Glu-rich stretch would be. The interpretation depends on their organization, not simply on counting negative charges.

The candidate loops lie well upstream of the hydrophobic near-terminal sequence LICAFAIAFIISVMLIAA. That distribution is consistent with a soluble binding region attached to a membrane through a C-terminal anchor. It helps place the proposed ion-binding loops outside the hydrophobic segment, but does not establish membrane orientation or the protein’s cellular destination.

B would require the characteristic Cys/His arrangement of a C2H2 zinc finger; scattered cysteines and histidines do not supply that architecture. The heme- and FAD-binding roles in C and D likewise do not explain the two repeated ligand-compatible loop patterns as directly as the EF-hand assignment.

The sequence supports candidate EF hands; it does not directly demonstrate their three-dimensional fold or prove that both bind ions under physiological conditions. Nor does it measure calcium affinity, calcium-versus-magnesium selectivity, occupancy or a calcium-dependent conformational change. The architecture prediction and the biochemical properties of its sites require different evidence.

<details>
<summary>Sources and qualifications</summary>

Source identity: human calcium-binding protein 7 (CaBP7), [UniProt Q86V35](https://www.uniprot.org/uniprotkb/Q86V35/entry). The primary abstract and experimental deposition support two high-affinity N-terminal calcium sites. The NMR construct omits the full canonical C-terminal region.

Primary references: [Solution NMR structure of the Ca2+-bound N-terminal domain of CaBP7: a regulator of Golgi trafficking](https://pubmed.ncbi.nlm.nih.gov/22989873/) and [experimental structure PDB 2LV7](https://www.rcsb.org/structure/2LV7).

Those experimental findings support the EF-hand assignment, but affinity, ion selectivity and calcium-dependent structural changes cannot be read directly from the anonymous sequence. The complete sequence’s proposed membrane anchor is outside the NMR construct.

</details>
