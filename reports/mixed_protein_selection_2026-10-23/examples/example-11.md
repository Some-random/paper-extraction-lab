# 11. Chromophore binding

## Question

Protein sequence:

```text
MVGLTTLFWLGAIGMLVGTLAFAWAGRDAGSGERRYYVTLVGISGIAAVAYVVMALGVGWVPVAERTVFA
PRYIDWILTTPLIVYFLGLLAGLDSREFGIVITLNTVVMLAGFAGAMVPGIERYALFGMGAVAFLGLVYY
LVGPMTESASQRSSGIKSLYVRLRNLTVILWAIYPFIWLLGPPGVALLTPTVDVALIVYLDLVTKVGFGF
IALDAAATLRAEHGESLAGVDTDAPAVAD
```


**Question:** Which chromophore-association mechanism is most consistent with this protein sequence?

**Choices:**

- **A.** Covalent bilin attachment to a cysteine in a large phytochrome photosensory domain.
- **B.** Noncovalent FMN binding in a soluble LOV-domain pocket.
- **C.** Formation of an internal GFP-like chromophore by cyclization of residues in a soluble beta-barrel.
- **D.** Retinal attachment through a Schiff-base linkage to a lysine in a membrane-embedded opsin.

## Answer

D is the most consistent choice: retinal attachment through a Schiff-base linkage to a lysine in a membrane-embedded opsin.

1. Overall sequence architecture
The 239-residue protein contains repeated long, hydrophobic-rich windows at residues 1–26, 36–64, 73–94, 98–121, 124–145, 166–190, and 194–219. Their distribution throughout the chain strongly favors a compact multipass membrane protein rather than a soluble chromophore-binding domain. These are illustrative sequence windows, not experimentally established helix boundaries. Nevertheless, this pattern is consistent with the seven-transmembrane-helical architecture typical of microbial opsins.

2. A plausible attachment residue
The late hydrophobic-rich segment at residues 194–219, VALIVYLDLVTKVGFGFIALDAAATL, contains Lys205. In opsins, retinal's aldehyde forms a covalent imine, or Schiff base, with a lysine side chain's ε-amino group. In microbial opsins, the attachment lysine lies in the final transmembrane helix. Thus, Lys205 has both suitable chemistry and an appropriate qualitative sequence location. The combination of membrane architecture and lysine position is more informative than lysine presence alone.

3. Comparison with the alternatives
A: The sequence contains no cysteine, so no cysteine is available for the specified bilin linkage. Its compact, membrane-rich architecture also does not support the large phytochrome photosensory module described in this choice.
B: Noncovalent FMN binding in a LOV domain requires a folded, predominantly soluble pocket. The extensive hydrophobic segments throughout this sequence instead favor a membrane-helical bundle.
C: GFP-like chromophore formation requires the soluble GFP β-barrel scaffold. Although GFP proteins can have a similar overall length, length alone is not diagnostic, and the repeated membrane-length hydrophobic regions argue strongly against that architecture.

Therefore, D best explains both the overall sequence organization and the candidate lysine attachment site, while the actual chromophore and covalent linkage remain inferred.

**Final answer: D**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

A primary abstract and experimental structure deposition support retinal attachment through Schiff-base chemistry. Seven membrane helices plus a lysine are compatible with this family but do not independently prove retinal attachment.

### Answer limitations

Sequence inspection does not demonstrate retinal occupancy, Schiff-base formation specifically at Lys205, or exact transmembrane-helix boundaries. Confidence is high for choosing among the supplied mechanisms, not for experimentally establishing the modification.

### References and source review

The following information was **not supplied to AI**.

Verified source identity: **Sensory rhodopsin-2** — [UniProt P42196](https://www.uniprot.org/uniprotkb/P42196/entry).

[Frozen UniProt annotation](../../astra_sequence_only_nine_2026-10-23/artifacts/case-008/uniprot_record.json), withheld from AI.

Source-supported answer: **D**. AI’s selected answer matches it.

Structural studies of this natural archaeal sensory rhodopsin establish a seven-helix membrane architecture surrounding retinal. The experimentally linked structure and paper identify attachment of retinal to Lys205, consistent with the Schiff-base mechanism in the correct answer.

Scientific review: Qualified chromophore-mechanism inference.

- Repeated hydrophobic regions, a late lysine and the absence of cysteine discriminate among these choices. They do not uniquely prove an opsin identity or retinal attachment.

Moderate biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- A seven-transmembrane pattern alone does not prove retinal binding: many unrelated receptors also cross membranes seven times. The microbial-opsin sequence pattern and conserved lysine provide the more specific connection.
- The selected sequence contains lysine at canonical position 205, but the covalent chromophore attachment is experimentally established, not demonstrated just by the presence of a lysine.
- Do not describe this microbial sensory rhodopsin as an animal G-protein-coupled receptor or infer a precise absorption wavelength from sequence inspection.

Papers and experimental references:

- [Crystal structure of sensory rhodopsin II at 2.4 angstroms: insights into color tuning and transducer interaction](https://pubmed.ncbi.nlm.nih.gov/11452084/). Primary structure paper identifies retinal/retinylidene Schiff-base chemistry in this sensory rhodopsin; its figure descriptions locate retinal attachment at Lys205. Review scope: Primary abstract and indexed figure description, checked against the experimental deposition; PMC full-text page opening encountered a browser challenge.
- [Sensory rhodopsin II experimental structure, PDB 1JGJ](https://www.rcsb.org/structure/1JGJ). Experimental deposition maps the protein to P42196 and explicitly lists retinal as a ligand. Review scope: Experimental deposition page, protein mapping and ligand list.
- [Molecular basis of transmembrane signalling by sensory rhodopsin II-transducer complex](https://pubmed.ncbi.nlm.nih.gov/12368857/). Independent primary structure study describes seven-helix retinal-containing microbial rhodopsins and the exact N. pharaonis SRII-HtrII complex. Review scope: Primary abstract.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.

[Original source records and unchanged AI output](../../astra_sequence_only_nine_2026-10-23/examples/case-008.md)

</details>
