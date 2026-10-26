# 5. Recognizing repeated calcium-binding loops

## Question

Protein sequence:

```text
MPFHPVTAALMYRGIYTVPNLLSEQRPVDIPEDELEEIREAFKVFDRDGNGFISKQELGTAMRSLGYMPN
EVELEVIIQRLDMDGDGQVDFEEFVTLLGPKLSTSGIPEKFHGTDFDTVFWKCDMQKLTVDELKRLLYDT
FCEHLSMKDIENIIMTEEESHLGTAEECPVDVETCSNQQIRQTCVRKSLICAFAIAFIISVMLIAANQVL
RSGMK
```

What ion-binding architecture is supported by the likely soluble region of this sequence? Cite the relevant segments and explain why their arrangement is more informative than acidic composition alone. Contrast your interpretation with a nonspecific acidic region, and distinguish the prediction from properties that require experimental evidence.

## Answer

The likely soluble region supports an EF-hand calcium-binding architecture, with two particularly convincing candidate loops. They are DRDGNGFISKQE at residues 46–57 and DMDGDGQVDFEE at residues 82–93.

An EF hand contains a calcium-binding loop of about 12 residues between two helices. The informative feature here is the arrangement of potential ligands within each loop. In DRDGNGFISKQE, positions 1, 3 and 5 are Asp, Asp and Asn. In DMDGDGQVDFEE, those positions are all Asp. Both loops have glycine at position 6 and glutamate at position 12. Asp, Asn and Glu provide oxygen-containing groups compatible with calcium coordination. Glycine can accommodate the tight loop geometry, while the terminal glutamate commonly contributes its carboxylate to calcium binding. The repeated positional pattern is therefore chemically and structurally coherent.

This is stronger evidence than high acidic content alone. A nonspecific acidic region could interact with positively charged ions, but acidity does not specify a calcium-binding fold. Two separate segments with the same ligand-compatible positions, loop length and conserved glycine are more suggestive of repeated binding modules than an arbitrary Asp/Glu-rich stretch would be. The interpretation depends on their organization, not simply on counting negative charges.

The candidate loops lie well upstream of the hydrophobic near-terminal sequence LICAFAIAFIISVMLIAA. That distribution is consistent with a soluble binding region attached to a membrane through a C-terminal anchor. It helps place the proposed ion-binding loops outside the hydrophobic segment, but does not establish membrane orientation or the protein’s cellular destination.

The sequence supports candidate EF hands; it does not directly demonstrate their three-dimensional fold or prove that both bind ions under physiological conditions. Nor does it measure calcium affinity, calcium-versus-magnesium selectivity, occupancy or a calcium-dependent conformational change. In particular, recognizing these two loops does not justify claiming four functional calcium-binding sites. The architecture prediction and the biochemical properties of its sites require different evidence.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


The existing review identifies the sequence as human CaBP7, UniProt Q86V35. The primary abstract and experimental deposition support two high-affinity N-terminal calcium sites. The NMR construct omits the full canonical C-terminal region. Those experimental facts are withheld from the student input; they do not make affinity or selectivity readable from the anonymous sequence.

Primary references: [Solution NMR structure of the Ca2+-bound N-terminal domain of CaBP7: a regulator of Golgi trafficking](https://pubmed.ncbi.nlm.nih.gov/22989873/) and [experimental structure PDB 2LV7](https://www.rcsb.org/structure/2LV7). The prior review used the primary abstract and deposition; it was not a new full-text review.

This is a source-aware assistant revision of the existing source-checked example into an open-response task. The original full sequence is unchanged. No new experiment, measurement or variant is proposed. The question uses only the anonymous sequence and standard family knowledge; the source identity and experimental findings remain in these review notes. No expert human validation or measured training benefit is claimed.

</details>
