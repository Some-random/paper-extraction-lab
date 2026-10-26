# 4. Inferring a cofactor from a motif combination

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

**Answer: D.**

The strongest assignment is a heme-containing cytochrome P450. The evidence is a combination of sequence features in the appropriate order, rather than the presence of a metal-binding amino acid by itself.

The most direct clue is FGHGHHVCLG at residues 338–347. It matches the P450-associated pattern FxxGxxxCxG, where x can be any residue. The cysteine in this pattern is Cys345. In P450 enzymes, the corresponding cysteine supplies a thiolate sulfur that coordinates the heme iron. This makes Cys345 a plausible axial ligand and connects the sequence pattern to a specific cofactor-binding chemistry. The sequence predicts cysteine–iron coordination, not direct attachment of the porphyrin ring to the polypeptide.

Two other regions strengthen the family assignment. ECLR at residues 274–277 matches the characteristic P450 E-x-x-R pattern. This supports the P450 core architecture; it is not itself a direct heme-binding site. AGHETT at residues 235–240 contains an acidic residue and adjacent threonines consistent with the I-helix region involved in oxygen activation in many P450s. Calling it an I helix is a family-based structural inference, not an observed secondary structure. These regions precede the cysteine-containing signature in the expected sequence order, so they provide mutually consistent support.

An iron–sulfur cluster (C) is a reasonable alternative to consider when a sequence contains cysteines. However, cysteine presence alone does not distinguish an iron–sulfur ligand from a heme ligand or an unrelated cysteine. Here, the specific cysteine-containing signature together with the supporting P450 patterns explains the evidence better than a generic iron–sulfur assignment. FAD (A) and FMN (B) occur in diverse flavin-binding families, but neither assignment explains this combined P450 pattern as well. Their rejection rests on stronger positive evidence for heme, not on the absence of a supposed universal flavin-binding motif.

The supported conclusion is a strong P450/heme hypothesis. The sequence does not demonstrate that the protein actually contains heme, identify its substrate or establish its reaction specificity and catalytic activity. Those are separate claims from recognizing a cofactor-binding family.

<details>
<summary>Sources and qualifications</summary>

Source identity: biotin biosynthesis cytochrome P450, [UniProt P53554](https://www.uniprot.org/uniprotkb/P53554/entry). The primary structure supports heme and coordination by Cys345. Its substrate complex supplies experimental context for specificity; the anonymous sequence does not independently establish that substrate or the biotin-biosynthesis role.

Primary reference: [Structural insights from a P450 carrier protein complex reveal how specificity is achieved in the P450BioI ACP complex](https://pmc.ncbi.nlm.nih.gov/articles/PMC2572933/), especially Active Site Architecture.

The source supports the family/cofactor assignment. Actual heme occupancy and catalytic specificity are distinct from the sequence-based inference in the answer.

</details>
