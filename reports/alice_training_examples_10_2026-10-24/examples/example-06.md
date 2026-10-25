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

A single near-C-terminal membrane anchor is strongly supported by ILLVILGIIVVIAILTAIAFF at residues 193–213, followed by only VKGH. Its length, hydrophobicity and lack of charged residues favor a bilayer-spanning helix over purely peripheral association. The much longer upstream region contains many charged and polar residues, without comparable hydrophobic stretches. The basic RRIIQNR flank is consistent with a cytosolic upstream region through the positive-inside tendency, but this orientation is less secure than the anchor prediction. These are sequence-based boundaries and topology inferences. The sequence does not establish the exact membrane boundary, insertion route or organelle destination.

## Assessment rubric

- Identifies the actual near-terminal hydrophobic stretch and short following tail as support for a single integral anchor.
- Contrasts an integral anchor with peripheral association using that sequence evidence, rather than assuming all membrane-associated proteins span the bilayer.
- Distinguishes strong anchor evidence from the weaker orientation inference; a cautious refusal to assign orientation is acceptable if explained.
- Does not infer Golgi/endosomal destination, exact measured boundaries or an insertion mechanism. Credit defensible alternatives that account for the hydrophobic segment and explain what evidence is missing.

<details>
<summary>Sources and review notes</summary>

The existing review identifies the sequence as Vti1-rp2/Vti1a, UniProt O89116. The primary abstract supports a C-terminal anchor, cytoplasmic region and integral membrane behavior. Residues 193–213 are corrected sequence-analysis coordinates, not membrane boundaries measured by that paper.

Primary reference: [A 29-kilodalton Golgi soluble N-ethylmaleimide-sensitive factor attachment protein receptor (Vti1-rp2) implicated in protein trafficking in the secretory pathway](https://pubmed.ncbi.nlm.nih.gov/9705316/). The prior review used the primary abstract retrieved in search results; direct page opening encountered a browser challenge.

This is a source-aware assistant revision of the existing source-checked example into an open-response task. The original full sequence is unchanged. No new experiment, measurement or variant is proposed. The question uses only the anonymous sequence and standard family knowledge; the source identity and experimental findings remain in these review notes. No expert human validation or measured training benefit is claimed.

</details>
