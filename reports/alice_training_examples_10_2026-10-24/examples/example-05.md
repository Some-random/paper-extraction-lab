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

Two candidate EF-hand calcium-binding loops are DRDGNGFISKQE at residues 46–57 and DMDGDGQVDFEE at 82–93. Both place oxygen-donating residues at positions 1, 3 and 5, glycine at 6, and glutamate at 12, supporting a repeated calcium-binding architecture. A generally acidic region could also attract ions, but would not explain these repeated positional patterns as well. The motifs lie upstream of a strongly hydrophobic near-terminal region, consistent with a soluble binding domain and membrane anchor. Sequence does not measure calcium affinity, ion selectivity, occupancy or how many sites are functional, and it does not directly demonstrate the EF-hand fold.

## Assessment rubric

- Proposes EF-hand calcium binding and identifies both actual 12-residue segments, explaining at least two relevant positional features.
- Explains why repeated ligand-compatible patterns support more than a generic acidic-composition claim.
- Uses the near-terminal hydrophobic region only as architectural context, without assigning an experimentally established topology.
- Does not infer affinity, selectivity, occupancy or four functional sites from sequence. Credit a reasoned tentative assignment or alternative if it addresses both loops and distinguishes evidence from speculation.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency and rubric review. No independently documented blinded solver test or expert human validation is claimed for the current question.


The existing review identifies the sequence as human CaBP7, UniProt Q86V35. The primary abstract and experimental deposition support two high-affinity N-terminal calcium sites. The NMR construct omits the full canonical C-terminal region. Those experimental facts are withheld from the student input; they do not make affinity or selectivity readable from the anonymous sequence.

Primary references: [Solution NMR structure of the Ca2+-bound N-terminal domain of CaBP7: a regulator of Golgi trafficking](https://pubmed.ncbi.nlm.nih.gov/22989873/) and [experimental structure PDB 2LV7](https://www.rcsb.org/structure/2LV7). The prior review used the primary abstract and deposition; it was not a new full-text review.

This is a source-aware assistant revision of the existing source-checked example into an open-response task. The original full sequence is unchanged. No new experiment, measurement or variant is proposed. The question uses only the anonymous sequence and standard family knowledge; the source identity and experimental findings remain in these review notes. No expert human validation or measured training benefit is claimed.

</details>
