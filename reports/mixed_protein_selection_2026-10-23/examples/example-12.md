# 12. Post-translational modification chemistry

## Question

Protein sequence:

```text
MAGCAARAPPGSEARLSLATFLLGASVLALPLLTRAGLQGRTGLALYVAGLNALLLLLYRPPRYQIAIRA
CFLGFVFGCGTLLSFSQSSWSHFGWYMCSLSLFHYSEYLVTAVNNPKSLSLDSFLLNHSLEYTVAALSSW
LEFTLENIFWPELKQITWLSVTGLLMVVFGECLRKAAMFTAGSNFNHVVQNEKSDTHTLVTSGVYAWFRH
PSYVGWFYWSIGTQVMLCNPICGVSYALTVWRFFRDRTEEEEISLIHFFGEEYLEYKKRVPTGLPFIKGV
KVDL
```


**Question:** Which biochemical transformation is most consistent with this protein sequence?

**Choices:**

- **A.** SAM-dependent methylation of the terminal carboxyl group of a prenylated cysteine on a protein substrate.
- **B.** Proteolytic removal of the three residues following a prenylated cysteine in a C-terminal CaaX motif.
- **C.** ATP-dependent phosphorylation of serine hydroxyl groups on protein substrates.
- **D.** ATP-dependent attachment of biotin to a lysine side chain on a protein substrate.

## Answer

The most defensible choice is A: SAM-dependent methylation of the terminal carboxyl group of a prenylated cysteine.

1. Sequence architecture. This 284-residue protein contains repeated hydrophobic regions, including residues 16–34 (LSLATFLLGASVLALPLLT), 43–59 (GLALYVAGLNALLLLLY), 156–173 (ITWLSVTGLLMVVFGECL), and 213–241 (YVGWFYWSIGTQVMLCNPICGVSYALTVW). Their distribution supports a compact multipass membrane protein rather than a predominantly soluble enzyme. These are illustrative hydrophobic intervals, not established transmembrane-helix boundaries.

2. Family-level evidence. The C-terminal portion contains RHPSY at residues 209–213, matching an RHPxY pattern, and paired glutamates within EEYLEY at residues 261–266. In combination with the multipass architecture, these fit the RHP-containing and acidic C-terminal regions associated with ICMT/Ste14-family isoprenylcysteine carboxyl methyltransferases. The combination is more informative than either a short motif or hydrophobicity alone; it does not independently prove SAM binding or catalysis.

3. Biochemical interpretation. ICMT acts after a CaaX protein has been prenylated and its final three residues have been removed. That processing exposes the prenylated cysteine as the protein's terminal residue. ICMT transfers a methyl group from S-adenosylmethionine (SAM) to the terminal carboxylate oxygen, converting –COO− into the methyl ester –COOCH3 and producing S-adenosylhomocysteine. The modification is on the carboxyl group, not on the prenylated sulfur. A membrane-embedded enzyme is well suited to recognizing a lipid-modified protein substrate.

4. Comparison with the alternatives.
• B describes RCE1-type CaaX proteolysis, the processing step preceding ICMT-mediated methylation. RCE1 is also a multipass membrane enzyme, so membrane architecture alone does not exclude B. The ICMT-like C-terminal sequence features are the main reason to favor A.
• C requires an ATP-dependent protein-kinase catalytic domain. Conventional serine kinases have a substantial globular kinase fold; the extensively hydrophobic architecture here does not support such a domain. A kinase can be membrane-associated, but membrane anchoring is different from having hydrophobic segments distributed throughout nearly the entire catalytic protein.
• D describes biotin-protein ligase activity, which proceeds through ATP-dependent formation of biotinyl-AMP followed by attachment to lysine. Such enzymes require a globular adenylating catalytic domain, not the membrane-rich ICMT-like architecture observed here.

Thus, A best integrates the observed architecture, the C-terminal family-associated features, and the chemistry of prenylated-protein processing.

**Final answer: A**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

The full primary kinetic article supports SAM-dependent methylation of the terminal prenylcysteine carboxyl group, distinct from prior proteolysis. Supporting motif-study passages describe patterns shared with other families, so sequence identification remains qualified.

### Answer limitations

This is a sequence-based family assignment, not direct evidence of catalytic activity. Hydrophobicity alone cannot distinguish ICMT from the membrane CaaX protease RCE1. The C-terminal sequence features favor ICMT, but do not establish individual catalytic residues, membrane topology, or cellular localization.

### References and source review

The following information was **not supplied to AI**.

Verified source identity: **Protein-S-isoprenylcysteine O-methyltransferase** — [UniProt O60725](https://www.uniprot.org/uniprotkb/O60725/entry).

[Frozen UniProt annotation](../../astra_sequence_only_nine_2026-10-23/artifacts/case-009/uniprot_record.json), withheld from AI.

Source-supported answer: **A**. AI’s selected answer matches it.

The original human ICMT study establishes an active endoplasmic-reticulum membrane enzyme. A subsequent primary kinetic study of recombinant human ICMT explicitly shows that SAM supplies a methyl group to the terminal carboxyl group of a prenylated cysteine, producing a methyl ester. This directly supports the methylation answer and distinguishes it from CaaX-tail cleavage.

Scientific review: Qualified enzyme-family inference.

- The explanation uses family-associated sequence features and correctly distinguishes methylation from the preceding CaaX proteolysis step. It does not infer enzyme identity from hydrophobicity alone.
- Primary work supports the RHPxY–hydrophobic–EE pattern and includes human ICMT: https://pmc.ncbi.nlm.nih.gov/articles/PMC55642/ . Related membrane enzyme families also share it, so the pattern is not uniquely diagnostic.

Moderate biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- A multipass membrane topology does not, by itself, identify SAM use, methyltransferase activity or the prenylcysteine substrate. The explanation must show legitimate family recognition or acknowledge the inference limit.
- ICMT methylates the newly exposed terminal carboxyl group after another enzyme removes the three residues following the prenylated cysteine. It is not the CaaX endoprotease.
- Do not mistake a CaaX motif on a substrate protein for a catalytic motif that must occur at the end of ICMT itself.

Papers and experimental references:

- [Mammalian prenylcysteine carboxyl methyltransferase is in the endoplasmic reticulum](https://pubmed.ncbi.nlm.nih.gov/9614111/). Primary human cloning and characterization study establishes enzymatic activity and ER localization of mammalian ICMT. Review scope: Primary PubMed abstract retrieved in search results; direct page opening encountered a browser challenge.
- [Analysis of the kinetic mechanism of recombinant human isoprenylcysteine carboxylmethyltransferase (Icmt)](https://link.springer.com/article/10.1186/1471-2091-5-19). Primary human-enzyme study explicitly identifies SAM as methyl donor and terminal prenylcysteine carboxyl methyl ester as product. It distinguishes preceding Rce1 cleavage from ICMT methylation. Review scope: Full primary article, abstract Results and Background paragraphs on CaaX processing.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.

[Original source records and unchanged AI output](../../astra_sequence_only_nine_2026-10-23/examples/case-009.md)

</details>
