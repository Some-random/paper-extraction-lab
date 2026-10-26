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

D. Heme

The strongest assignment is a heme-containing cytochrome P450. The evidence is a combination of sequence features in the appropriate order, rather than the presence of a metal-binding amino acid by itself.

The most direct clue is FGHGHHVCLG at residues 338–347. It matches the P450-associated pattern FxxGxxxCxG, where x can be any residue. The cysteine in this pattern is Cys345. In P450 enzymes, the corresponding cysteine supplies a thiolate sulfur that coordinates the heme iron. This makes Cys345 a plausible axial ligand and connects the sequence pattern to a specific cofactor-binding chemistry. Coordination of heme iron should not be confused with a covalent bond attaching the heme group to the polypeptide.

Two other regions strengthen the family assignment. ECLR at residues 274–277 matches the characteristic P450 E-x-x-R pattern. This supports the P450 core architecture; it is not itself a direct heme-binding site. AGHETT at residues 235–240 contains an acidic residue and adjacent threonines consistent with the I-helix region involved in oxygen activation in many P450s. Calling it an I helix is a family-based structural inference, not an observed secondary structure. These regions precede the cysteine-containing signature in the expected sequence order, so they provide mutually consistent support.

An iron–sulfur protein is a reasonable alternative to consider when a sequence contains cysteines. However, cysteine presence alone does not distinguish an iron–sulfur ligand from a heme ligand or an unrelated cysteine. Here, the specific cysteine-containing signature together with the supporting P450 patterns explains the evidence better than a generic iron–sulfur assignment. Flavin-binding families are also diverse, so the argument should not be that one missing universal FAD or FMN motif rules them out.

The supported conclusion is a strong P450/heme hypothesis. The sequence does not demonstrate that the protein actually contains heme, identify its substrate or establish its reaction specificity and catalytic activity. Those are separate claims from recognizing a cofactor-binding family.

Among the choices, D is therefore the strongest assignment. C is a plausible alternative for a cysteine-containing protein, but the complete motif combination supports heme-thiolate P450 chemistry more specifically. A and B represent flavin cofactors; flavin-binding proteins are diverse, but neither assignment explains the observed P450-associated signatures as well. Their rejection rests on stronger positive evidence for heme, not on claiming a universal flavin-binding motif is absent.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 7, A–D restoration).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


The existing source review identifies the sequence as UniProt P53554. The primary structure supports heme and Cys345 coordination; the anonymous sequence does not independently reveal the biotin-biosynthesis substrate.

Primary reference: [Structural insights from a P450 carrier protein complex reveal how specificity is achieved in the P450BioI ACP complex](https://pmc.ncbi.nlm.nih.gov/articles/PMC2572933/), especially Active Site Architecture.

This is a source-aware assistant revision of the existing source-checked example into an open-response task. The original full sequence is unchanged. No new experiment, measurement or variant is proposed. The question uses only the anonymous sequence and standard family knowledge; the source identity and experimental findings remain in these review notes. No expert human validation or measured training benefit is claimed.

</details>
