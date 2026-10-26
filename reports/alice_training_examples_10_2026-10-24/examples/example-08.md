# 8. Judging a chromophore-binding hypothesis

## Question

Protein sequence:

```text
MVGLTTLFWLGAIGMLVGTLAFAWAGRDAGSGERRYYVTLVGISGIAAVAYVVMALGVGWVPVAERTVFA
PRYIDWILTTPLIVYFLGLLAGLDSREFGIVITLNTVVMLAGFAGAMVPGIERYALFGMGAVAFLGLVYY
LVGPMTESASQRSSGIKSLYVRLRNLTVILWAIYPFIWLLGPPGVALLTPTVDVALIVYLDLVTKVGFGF
IALDAAATLRAEHGESLAGVDTDAPAVAD
```

What chromophore-binding mechanism would you prioritize as a hypothesis for this sequence, and why? Identify evidence from the overall architecture and a candidate attachment residue. Compare that hypothesis with a soluble chromophore-binding protein, and distinguish compatibility from proof of chromophore attachment.

## Answer

A retinal-binding microbial opsin is a plausible leading hypothesis. The reasoning combines the protein’s overall membrane-rich architecture with the position and chemistry of a candidate attachment lysine; neither feature is sufficient alone.

Long hydrophobic regions occur throughout this compact 239-residue sequence, rather than being confined to one terminal anchor. Illustrative windows occur at residues 1–26, 36–64, 73–94, 98–121, 124–145, 166–190 and 194–219. Their distribution is consistent with a compact bundle of membrane-spanning helices, including the seven-helix architecture characteristic of microbial opsins. These are approximate sequence windows, not experimentally established helix boundaries or a demonstrated count of seven helices.

The late hydrophobic region, VALIVYLDLVTKVGFGFIALDAAATL at residues 194–219, contains Lys205. In a retinal-binding opsin, retinal’s aldehyde can form an imine, or Schiff base, with the lysine side chain’s amino group. The corresponding attachment lysine in microbial opsins lies in the final membrane helix. Lys205 therefore has compatible chemistry and a qualitatively appropriate position within the proposed membrane architecture. Its relevance comes from that context, not simply from finding a lysine somewhere in the protein.

A soluble chromophore-binding protein is a meaningful alternative. A soluble LOV-domain protein can bind FMN, for example, but its folded pocket would need to accommodate the chromophore within a largely soluble domain. The many long hydrophobic regions here fit a membrane bundle substantially better than that overall architecture. Likewise, protein length alone would not justify a GFP-like soluble beta-barrel interpretation. The distribution of hydrophobicity is more discriminating than size.

The strongest conclusion from direct inspection is that this is likely a multipass membrane protein. The retinal/opsin interpretation is a more specific hypothesis that draws on family knowledge. Other membrane proteins can also contain several helices and lysines, so these observations do not uniquely prove opsin identity. They also do not demonstrate retinal occupancy, a Schiff-base linkage specifically at Lys205, an absorption wavelength or sensory rather than transport function. Those claims go beyond the anonymous sequence evidence.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


The existing review identifies the sequence as sensory rhodopsin II, UniProt P42196. Experimental structures establish retinal binding and the Lys205 linkage; the student must not treat those withheld findings as observations available from sequence alone. This microbial protein should not be labeled an animal G-protein-coupled receptor.

Primary references: [Crystal structure of sensory rhodopsin II at 2.4 angstroms: insights into color tuning and transducer interaction](https://pubmed.ncbi.nlm.nih.gov/11452084/), [experimental structure PDB 1JGJ](https://www.rcsb.org/structure/1JGJ), and [Molecular basis of transmembrane signalling by sensory rhodopsin II-transducer complex](https://pubmed.ncbi.nlm.nih.gov/12368857/). The prior review used primary abstracts, an indexed figure description and the experimental deposition; full-text opening encountered a browser challenge.

This is a source-aware assistant revision of the existing source-checked example into an open-response task. The original full sequence is unchanged. No new experiment, measurement or variant is proposed. The question uses only the anonymous sequence and standard family knowledge; the source identity and experimental findings remain in these review notes. No expert human validation or measured training benefit is claimed.

</details>
