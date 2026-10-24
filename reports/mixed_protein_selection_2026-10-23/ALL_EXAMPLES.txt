# All 12 mixed protein-reasoning examples

# general-001 — Covalent modification of a particular lysine

[Original example and artifacts](../astra_sequence_only_nine_2026-10-23/examples/case-001.md)

# case-001 — modified residue

Astra received only the student question below and the shared system instructions. Protein identity, gold answer, annotations and papers were withheld.

## Student question

Protein sequence:

```text
MTVSIQMAGNLWKVHVKAGDQIEKGQEVAILESMKMEIPIVADRSGIVKEVKKKEGDFVNEGDVLLELSN
STQ
```

Task: modified residue

Which residue is the most plausible attachment site for a biotin or lipoate group? Number the first amino acid as residue 1.

- **A.** Lysine at position 35
- **B.** Lysine at position 52
- **C.** Lysine at position 17
- **D.** Lysine at position 24

The sequence is line-wrapped for readability; the exact original prompt is retained in `questions.jsonl` and the request artifact.

## Astra’s worked solution

The most plausible site is A: lysine at position 35.

Biotin and lipoate are covalently attached through an amide bond to the side-chain ε-amino group of selected lysines in carrier domains. All four choices therefore have the appropriate residue chemistry; their surrounding sequences provide the useful distinction.

Counting the initial methionine as residue 1, residues 31–40 are LESMKMEIPI. Lys35 lies between Met34 and Met36, producing an MKM motif. This methionine-flanked lysine context is characteristic of the acceptor region in many biotin-carrier domains. It is the strongest positive clue for the attachment site in the supplied sequence.

Comparison with the alternatives:
- B, Lys52: residues 50–55 are EVKKKE. Lys52 begins a three-lysine cluster, but a cluster of lysines is not itself a biotin/lipoate attachment signal.
- C, Lys17: residues 15–19 are HVKAG, without the characteristic MKM context.
- D, Lys24: residues 22–26 are IEKGQ, likewise without that context.

Cofactor attachment depends on recognition of the folded carrier domain, so absence of MKM does not categorically exclude a lysine, especially for lipoylation. Nevertheless, Lys35 has a recognizable biotin-acceptor-like sequence context that the alternatives lack, making it the best-supported choice.

## Final answer

A

## Astra’s stated limitations

The sequence strongly favors one candidate site but does not establish that modification actually occurs. The MKM context is particularly suggestive of biotinylation, not a universal motif for both biotin and lipoate attachment. Cofactor identity and lysine accessibility cannot be established conclusively from this sequence alone.

Confidence reported by Astra: high.

## Post-generation verification

The following information was **not supplied to Astra**.

Verified source identity: **Biotin/lipoyl attachment protein** — [UniProt C0H419](https://www.uniprot.org/uniprotkb/C0H419/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-001/uniprot_record.json), withheld from Astra.

Source-supported answer: **A**. Astra’s selected answer matches it.

The primary study identified a natural 73-amino-acid protein from Bacillus subtilis. It characterized both unmodified and biotin-modified forms by solution NMR and placed the attached biotin on Lys35. The canonical sequence also has lysines at all four proposed answer positions, so the correct site is not established merely by checking that the residue is a lysine.

Scientific review: Qualified modification-site inference.

- MKM is a useful biotin-carrier clue, not a universal attachment rule for biotin or lipoate. The explanation retains that limitation.
- Primary biotin-carrier work supports the motif heuristic and folded-domain recognition: https://doi.org/10.1042/bj3290589 . The BLAP paper independently supports Lys35.
- The source modification was demonstrated during heterologous expression; native modification is not established.

Moderate biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- Biotin and lipoate modification were demonstrated when the protein was expressed in E. coli; the native modification in B. subtilis remains unknown.
- The exact modification site requires family knowledge or experimental evidence. An explanation must not pretend that any isolated lysine or short motif proves modification.
- The source record is a complete reviewed 73-residue protein, not a truncated construct; the mature-chain annotation removes the initial methionine.

Papers and experimental references:

- [Identification and solution structures of a single domain biotin/lipoyl attachment protein from Bacillus subtilis.](https://pubmed.ncbi.nlm.nih.gov/16699181/). Primary abstract describes the natural 73-residue protein, modification in E. coli and NMR-supported biotin attachment at Lys35. Review scope: Primary abstract retrieved through Europe PMC; cached UniProt record and complete-sequence annotation inspected.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.


---

# general-002 — Locating repeated sequence motifs

[Original example and artifacts](../astra_sequence_only_nine_2026-10-23/examples/case-002.md)

# case-002 — motif position

Astra received only the student question below and the shared system instructions. Protein identity, gold answer, annotations and papers were withheld.

## Student question

Protein sequence:

```text
MSRHSRLQRQVLSLYRDLLRAGRGKPGAEARVRAEFRQHAGLPRSDVLRIEYLYRRGRRQLQLLRSGHAT
AMGAFVRPRAPTGEPGGVGCQPDDGDSPRNPHDSTGAPETRPDGR
```

Task: motif position

At which two residue ranges does the exact tripeptide LYR occur in this sequence? Number the first amino acid as residue 1.

- **A.** Residues 15–17 and 54–56
- **B.** Residues 14–16 and 53–55
- **C.** Residues 16–18 and 55–57
- **D.** Residues 13–15 and 52–54

The sequence is line-wrapped for readability; the exact original prompt is retained in `questions.jsonl` and the request artifact.

## Astra’s worked solution

Number the initial M as residue 1 and search for consecutive L–Y–R residues (leucine–tyrosine–arginine).

Residues 11–20 are VLSLYRDLLR: L is at 14, Y at 15, and R at 16. Thus the first match is 14–16.

Residues 51–60 are EYLYRRGRRQ: L is at 53, Y at 54, and R at 55. Thus the second match is 53–55. There are no other exact LYR occurrences.

Therefore, B is correct. Relative to the correct ranges, A shifts both windows one residue forward, C shifts them two residues forward, and D shifts them one residue backward.

## Final answer

B

## Astra’s stated limitations

None for this exact sequence-matching task; no functional or structural inference is needed.

Confidence reported by Astra: high.

## Post-generation verification

The following information was **not supplied to Astra**.

Verified source identity: **Succinate dehydrogenase assembly factor 1, mitochondrial** — [UniProt A6NFY7](https://www.uniprot.org/uniprotkb/A6NFY7/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-002/uniprot_record.json), withheld from Astra.

Source-supported answer: **B**. Astra’s selected answer matches it.

The displayed sequence contains LYR exactly twice, at residues 14–16 and 53–55 using one-based numbering. The primary paper independently discusses those same two motifs. Its interaction experiments show that the first motif helps recruit the HSC20 iron-sulfur transfer machinery.

Scientific review: Supported sequence-indexing control.

- Both LYR occurrences and all distractor offsets are correct. This teaches exact indexing, with little biological inference; it is not counted as a deep biological example.

Exact-indexing control; limited biological depth

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- Finding the two motif positions is directly checkable from the sequence. Assigning their biological roles requires additional knowledge.
- The two identical tripeptides are not functionally interchangeable: experiments distinguish the first motif from the second, and neighboring residues matter.
- The pilot motif-location question does not independently test whether the model understands mitochondrial assembly or protein interactions.

Papers and experimental references:

- [Disease-Causing SDHAF1 Mutations Impair Transfer of Fe-S Clusters to SDHB.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4749439/). The primary paper maps both LYR motifs and reports interaction assays distinguishing the HSC20-binding first motif from the second. Review scope: Primary abstract via Europe PMC and primary paper Results/Figure 2 text available in web search; exact motif positions independently replayed against the canonical sequence.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.


---

# general-003 — Recognizing multiple membrane-spanning segments

[Original example and artifacts](../astra_sequence_only_nine_2026-10-23/examples/case-003.md)

# case-003 — transmembrane

Astra received only the student question below and the shared system instructions. Protein identity, gold answer, annotations and papers were withheld.

## Student question

Protein sequence:

```text
MKRLKAYLKDGINVAAVMCLGDTISQFFFDKKSLDEWDAGRTLRFGIVGLVFVGPTLRRWYHFLESRVPK
TYSPMRRGVTKMLVDQTLFAPPFTMAMSFLVPLSNGEPIDRIRQRILDSYLSILVRNYMLWPAAQMLNFR
FVPLGYQVLYAQFIALVWNCYLSMILNS
```

Task: transmembrane

Which overall membrane architecture best fits this protein sequence?

- **A.** A soluble protein with no membrane-spanning segments
- **B.** A secreted soluble protein with a cleaved N-terminal signal peptide and no additional membrane-spanning segments
- **C.** A compact multipass alpha-helical membrane protein with several membrane-spanning segments
- **D.** A single-pass alpha-helical membrane protein

The sequence is line-wrapped for readability; the exact original prompt is retained in `questions.jsonl` and the request artifact.

## Astra’s worked solution

C is the most defensible overall fit: a compact multipass alpha-helical membrane protein.

A membrane-spanning alpha helix usually contains roughly 18–25 predominantly hydrophobic residues. Multiple such regions separated by short charged or polar intervals favor a multipass architecture, whereas one isolated hydrophobic segment favors a single-pass protein.

Here, hydrophobic-rich blocks recur across the sequence:
• 12–29: INVAAVMCLGDTISQFFF
• 43–64: LRFGIVGLVFVGPTLRRWYHFL
• 82–103: MLVDQTLFAPPFTMAMSFLVPL
• 141–166: FVPLGYQVLYAQFIALVWNCYLSMIL

The C-terminal block is the strongest candidate: it is long, contains many nonpolar residues, and lacks Asp, Glu, Lys and Arg. The earlier blocks alternate with charged/polar-rich intervals at 30–42, 65–81 and 104–119. That repeated pattern is consistent with membrane-embedded helices connected by short loops.

These are candidate regions, not four established transmembrane helices. Asp22, Arg58–Arg59 and Pro91–Pro92 illustrate why the internal assignments are less secure. Polar or charged residues can occur in membrane helices, and prolines can introduce kinks, but these interruptions reduce confidence in a simple visual topology assignment.

Comparison of the choices:
• A is disfavored by the long C-terminal hydrophobic region together with the repeated internal nonpolar-rich blocks.
• B would require an N-terminal signal peptide followed by an otherwise soluble protein. Even if the N terminus were a signal peptide, the substantial downstream hydrophobic regions would still need explaining; a purely secreted soluble architecture is therefore less convincing.
• D is the closest alternative because the C-terminal region is the clearest membrane-spanning candidate. However, a single-pass model would require the earlier hydrophobic-rich blocks to be accommodated within a soluble domain or as non-spanning membrane contacts. Their recurrence and intervening charged intervals favor a multipass interpretation instead.
• C best accommodates the overall distribution of hydrophobic and charged regions, without requiring an exact helix count to be inferred.

## Final answer

C

## Astra’s stated limitations

This is a qualitative sequence-based architecture prediction. Several internal hydrophobic-rich regions are interrupted by charged residues or prolines, so they cannot all be assigned confidently as full membrane spans. The exact helix count, boundaries, membrane orientation and N-terminal processing are not established.

Confidence reported by Astra: moderate.

## Post-generation verification

The following information was **not supplied to Astra**.

Verified source identity: **Mitochondrial inner membrane protein Mpv17** — [UniProt Q9V492](https://www.uniprot.org/uniprotkb/Q9V492/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-003/uniprot_record.json), withheld from Astra.

Source-supported answer: **C**. Astra’s selected answer matches it.

Microscopy in the primary study supports mitochondrial localization, and recordings after insertion into lipid bilayers demonstrate channel activity. Multiple hydrophobic stretches and source topology predictions support the broad multipass membrane-protein answer.

Scientific review: Qualified membrane-architecture inference.

- Repeated hydrophobic regions favor a multipass architecture among these choices. Charged residues and prolines weaken exact helix assignments; the explanation explicitly acknowledges that.
- The frozen UniProt annotation lists four spans while the paper predicts five. The question deliberately asks only broad architecture.

Moderate biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- The paper predicts five transmembrane segments with AlphaFold and DeepTMHMM, whereas the frozen UniProt record annotates four. The pilot therefore uses broad multipass topology rather than treating an exact helix count as established.
- Membrane localization and channel activity are experimental findings; the detailed topology in this source is predicted.
- Hydrophobic stretches support membrane insertion but do not alone prove mitochondrial targeting, channel selectivity, metabolite specificity or precise helix boundaries.

Papers and experimental references:

- [Drosophila Mpv17 forms an ion channel and regulates energy metabolism.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10558772/). The primary study reports mitochondrial colocalization and membrane channel activity; Figure 1 and Results label the detailed topology as a prediction. Review scope: Primary abstract and full-text XML from Europe PMC; Figure 1, topology Results and Discussion inspected.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.


---

# general-004 — Distinguishing heme from other cofactors

[Original example and artifacts](../astra_sequence_only_nine_2026-10-23/examples/case-004.md)

# case-004 — cofactor

Astra received only the student question below and the shared system instructions. Protein identity, gold answer, annotations and papers were withheld.

## Student question

Protein sequence:

```text
MTIASSTASSEFLKNPYSFYDTLRAVHPIYKGSFLKYPGWYVTGYEETAAILKDARFKVRTPLPESSTKY
QDLSHVQNQMMLFQNQPDHRRLRTLASGAFTPRTTESYQPYIIETVHHLLDQVQGKKKMEVISDFAFPLA
SFVIANIIGVPEEDREQLKEWAASLIQTIDFTRSRKALTEGNIMAVQAMAYFKELIQKRKRHPQQDMISM
LLKGREKDKLTEEEAASTCILLAIAGHETTVNLISNSVLCLLQHPEQLLKLRENPDLIGTAVEECLRYES
PTQMTARVASEDIDICGVTIRQGEQVYLLLGAANRDPSIFTNPDVFDITRSPNPHLSFGHGHHVCLGSSL
ARLEAQIAINTLLQRMPSLNLADFEWRYRPLFGFRALEELPVTFE
```

Task: cofactor

Which cofactor is most strongly supported by this protein sequence?

- **A.** FAD
- **B.** FMN
- **C.** A four-iron four-sulfur cluster
- **D.** Heme

The sequence is line-wrapped for readability; the exact original prompt is retained in `questions.jsonl` and the request artifact.

## Astra’s worked solution

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

## Final answer

D

## Astra’s stated limitations

This is a sequence-based cofactor prediction, not direct evidence of bound heme. The sequence does not establish actual cofactor occupancy, substrate specificity, or catalytic reaction.

Confidence reported by Astra: high.

## Post-generation verification

The following information was **not supplied to Astra**.

Verified source identity: **Biotin biosynthesis cytochrome P450** — [UniProt P53554](https://www.uniprot.org/uniprotkb/P53554/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-004/uniprot_record.json), withheld from Astra.

Source-supported answer: **D**. Astra’s selected answer matches it.

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


---

# general-005 — Calcium binding through repeated structural motifs

[Original example and artifacts](../astra_sequence_only_nine_2026-10-23/examples/case-005.md)

# case-005 — cofactor

Astra received only the student question below and the shared system instructions. Protein identity, gold answer, annotations and papers were withheld.

## Student question

Protein sequence:

```text
MPFHPVTAALMYRGIYTVPNLLSEQRPVDIPEDELEEIREAFKVFDRDGNGFISKQELGTAMRSLGYMPN
EVELEVIIQRLDMDGDGQVDFEEFVTLLGPKLSTSGIPEKFHGTDFDTVFWKCDMQKLTVDELKRLLYDT
FCEHLSMKDIENIIMTEEESHLGTAEECPVDVETCSNQQIRQTCVRKSLICAFAIAFIISVMLIAANQVL
RSGMK
```

Task: cofactor

Which binding role is most consistent with the soluble region of this protein?

- **A.** Binding calcium ions through EF-hand domains.
- **B.** Binding a structural zinc ion through a C2H2 zinc-finger domain.
- **C.** Binding heme to catalyze peroxide-dependent oxidation.
- **D.** Binding FAD to transfer electrons during redox catalysis.

The sequence is line-wrapped for readability; the exact original prompt is retained in `questions.jsonl` and the request artifact.

## Astra’s worked solution

A. Binding calcium ions through EF-hand domains is the best-supported choice.

Sequence context: Residues 189–206, LICAFAIAFIISVMLIAA, form a strongly hydrophobic near-C-terminal segment consistent with a membrane anchor. The candidate binding motifs lie well upstream, in the likely soluble portion of the protein.

Positive evidence for EF hands: Two conspicuous 12-residue segments are residues 46–57, DRDGNGFISKQE, and residues 82–93, DMDGDGQVDFEE. A canonical EF hand contains a calcium-binding loop of approximately 12 residues between two helices. Characteristic features include oxygen-donating residues at particular loop positions, a frequently conserved glycine at position 6, and a terminal glutamate at position 12.

The first segment has D, D and N at loop positions 1, 3 and 5; the second has D, D and D at those positions. Both have G at position 6 and E at position 12. These features are chemically appropriate for calcium binding: Asp and Asn provide oxygen ligands, glycine accommodates the loop geometry, and the terminal glutamate commonly coordinates calcium through both carboxylate oxygens. Two repeated, position-specific patterns provide much stronger evidence than acidic composition alone.

Comparison with the alternatives:
• A directly explains both candidate calcium-binding loops.
• B requires the characteristically spaced Cys–Cys–His–His ligands of a classical C2H2 zinc finger. That arrangement is not present; scattered cysteine and histidine residues do not establish a zinc-finger domain.
• C requires a heme-binding pocket and a peroxide-reactive catalytic environment. Individual potential heme-ligating residues would not establish that activity, and there is no comparably specific positive evidence for it here.
• D requires a flavin-binding oxidoreductase architecture. Many FAD-binding proteins contain glycine-rich nucleotide-binding segments, but the glycine-containing segments identified here have the positional ligand pattern of calcium-binding loops instead. FAD proteins are diverse, so a missing generic motif would not categorically exclude them; the decisive point is the much stronger positive evidence for EF hands.

Thus, calcium binding through EF-hand domains is the most defensible role for the soluble region.

## Final answer

A

## Astra’s stated limitations

This is a strong sequence-based assignment, not a biochemical measurement. Calcium affinity, ion selectivity, site occupancy and the number of functional binding sites cannot be established from sequence alone. The EF-hand fold and membrane-anchor topology remain structural predictions.

Confidence reported by Astra: high.

## Post-generation verification

The following information was **not supplied to Astra**.

Verified source identity: **Calcium-binding protein 7** — [UniProt Q86V35](https://www.uniprot.org/uniprotkb/Q86V35/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-005/uniprot_record.json), withheld from Astra.

Source-supported answer: **A**. Astra’s selected answer matches it.

The primary NMR study reports two high-affinity calcium-binding EF-hand motifs in the N-terminal region of human CaBP7. Its N-terminal domain binds calcium rather than magnesium and changes conformation on binding. This directly supports calcium binding through EF-hand domains as the correct choice.

Scientific review: Strong sequence-based explanation.

- Two exact 12-residue loops show repeated, position-specific calcium-ligand patterns. The explanation distinguishes candidate EF hands from measured affinity, selectivity or occupancy.
- Source experiments support two high-affinity N-terminal sites. One reviewer had previously encountered this sequence's source association; this is not blinded expert validation.

Strong biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- Do not describe this as four functional calcium-binding sites: the supported answer concerns two high-affinity N-terminal sites.
- Acidic sequence loops are consistent with EF-hand calcium binding, but exact affinity, ion selectivity and the PI4KIIIbeta interaction come from experiments, not from acidity alone.
- The paper and annotation were retained for checking the answer after generation; they were not part of the solving prompt.

Papers and experimental references:

- [Solution NMR structure of the Ca2+-bound N-terminal domain of CaBP7: a regulator of golgi trafficking](https://pubmed.ncbi.nlm.nih.gov/22989873/). Primary abstract explicitly identifies two high-affinity EF-hand calcium sites and calcium-dependent structural changes in CaBP7. Review scope: Primary abstract and associated experimental structure deposition.
- [Solution structure of Ca2+-bound CaBP7 N-terminal domain, PDB 2LV7](https://www.rcsb.org/structure/2LV7). Experimental structure explicitly maps human CaBP7 to Q86V35 and contains two calcium ions. Review scope: Experimental deposition page, including protein identity and ligands.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.


---

# general-006 — Membrane anchoring

[Original example and artifacts](../astra_sequence_only_nine_2026-10-23/examples/case-006.md)

# case-006 — transmembrane

Astra received only the student question below and the shared system instructions. Protein identity, gold answer, annotations and papers were withheld.

## Student question

Protein sequence:

```text
MSSDFEGYEQDFAVLTAEITSKIARVPRLPPDEKKQMVANVEKQLEEARELLEQMDLEVREIPPQSRGMY
SNRMRSYKQEMGKLETDFKRSRIAYSDEVRNELLGDAGNSSENQRAHLLDNTERLERSSRRLEAGYQIAV
ETEQIGQEMLENLSHDREKIQRARDRLRDADANLGKSSRILTGMLRRIIQNRILLVILGIIVVIAILTAI
AFFVKGH
```

Task: transmembrane

Which overall membrane-association architecture best fits this protein sequence?

- **A.** A soluble peripheral membrane protein with no membrane-spanning segment.
- **B.** A protein with a large cytosolic region and a single membrane anchor near its C terminus.
- **C.** A seven-pass membrane receptor with short loops connecting its membrane-spanning helices.
- **D.** A secreted soluble protein whose only hydrophobic segment is a cleaved N-terminal signal peptide.

The sequence is line-wrapped for readability; the exact original prompt is retained in `questions.jsonl` and the request artifact.

## Astra’s worked solution

B is the best-supported architecture: a large cytosolic region with a single membrane anchor near the C terminus.

The strongest evidence is residues 193–214, ILLVILGIIVVIAILTAIAFFV. This 22-residue stretch is strongly hydrophobic and contains no charged residues. Its length and composition are appropriate for an alpha helix spanning a lipid bilayer; such helices commonly contain roughly 18–25 predominantly hydrophobic residues. Only KGH at positions 215–217 follows it, so the candidate anchor lies very close to the protein's C terminus.

In contrast, residues 1–192 contain frequent charged and polar residues and no other comparably long hydrophobic stretch. They therefore support a large region outside the membrane rather than additional transmembrane helices. The N-terminal 30 residues also lack the sustained hydrophobic core expected in a classical cleavable signal peptide. Together, these features support a C-terminally anchored architecture. The basic flank RRIIQNR at residues 186–192 is consistent with the positive-inside tendency, in which positively charged flanks preferentially lie on the cytosolic side. This strengthens, but does not prove, the inference that the large upstream region is cytosolic.

Comparison of the choices:
- A is disfavored because the sequence contains a conspicuous membrane-length hydrophobic segment, rather than lacking a membrane anchor.
- B matches the large nonmembrane region, single near-terminal hydrophobic segment, and very short following tail.
- C would require seven separate membrane-spanning hydrophobic segments; that repeated pattern is absent.
- D requires an N-terminal signal peptide and a soluble mature protein. Here, the strong hydrophobic segment is at the C terminus, not the N terminus.

Thus, B best accounts for both the number and location of the candidate membrane-spanning segments.

## Final answer

B

## Astra’s stated limitations

Sequence strongly supports one C-terminal membrane anchor, but exact membrane-spanning boundaries and membrane orientation cannot be established conclusively. The cytosolic location of the large upstream region is a well-supported topology inference, not a direct observation.

Confidence reported by Astra: high.

## Post-generation verification

The following information was **not supplied to Astra**.

Verified source identity: **Vesicle transport through interaction with t-SNAREs homolog 1A** — [UniProt O89116](https://www.uniprot.org/uniprotkb/O89116/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-006/uniprot_record.json), withheld from Astra.

Source-supported answer: **B**. Astra’s selected answer matches it.

The original Vti1-rp2 paper describes a 217-residue protein with a hydrophobic membrane anchor at its C terminus and an accessible cytoplasmic region. Antibody-based experiments identify it as an integral membrane protein enriched at the Golgi. This supports a large cytosolic region followed by a single C-terminal membrane anchor.

Scientific review: Strong sequence-based explanation.

- The long C-terminal hydrophobic stretch, short following tail and charged upstream region directly support the architecture. Cytosolic orientation is a weaker inference and is appropriately qualified.

Strong biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- The strongly hydrophobic C-terminal stretch supports an anchor, but sequence alone does not establish the precise Golgi or endosomal destination.
- Treat the annotated anchor at residues 193-213 as a sequence-analysis boundary, not a membrane boundary measured in that paper.
- Do not confuse the soluble N-terminal domain with the whole protein being soluble: a tail anchor still makes the full protein integral to a membrane.

Papers and experimental references:

- [A 29-kilodalton Golgi soluble N-ethylmaleimide-sensitive factor attachment protein receptor (Vti1-rp2) implicated in protein trafficking in the secretory pathway](https://pubmed.ncbi.nlm.nih.gov/9705316/). The primary abstract explicitly reports 217 residues, a C-terminal hydrophobic anchor, a cytoplasmic region, integral membrane behavior and Golgi enrichment. Review scope: Primary PubMed abstract retrieved in search results; direct page opening encountered a browser challenge.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.


---

# general-007 — Protein-interaction domains

[Original example and artifacts](../astra_sequence_only_nine_2026-10-23/examples/case-007.md)

# case-007 — domain feature

Astra received only the student question below and the shared system instructions. Protein identity, gold answer, annotations and papers were withheld.

## Student question

Protein sequence:

```text
MVHIPSDVTPPRLCVVEKLNGENEYGYNLHAEKGRGQFVGTVDPDSPAERGGLITGDRIFAVNGHSIIGE
NHKKVVERIKANPNRCEMLVISEEGAKWYNENNVQITLDLPNIERVSPMSKETPVFVPPPPPPTDAMPYL
PRLAELNKGTPDQEFGFNLHAERGRGHFIGTVDAGGIGEKAGLEAGQRIVGVNGQLIYPTTGHKEVVALI
KKDTMKTTLLVASEDVDKYHKDHNIAYSWDNVERVDTRPVINVETHHHHEEVSVPKSNGYDVPPLNPHSI
QVNEEREISKMTTTTRTETITNSNSAYQYKESSTAYDAYATPPVDSNDLMDEVFGRVNLPGVTMSSHTEV
LPPTDDISSVSSLSSHRESAVDVPVSHQYVPSYATESHQKHEQHSQTHHHHHQHQQPSPLSNGSSHGYAA
SSTSGYDDDDIYHLSAREARERLRMKNRKHHLHEMSLNEKYQLVSNM
```

Task: domain feature

Which protein-interaction domain architecture is most consistent with this sequence?

- **A.** A WD40-repeat beta-propeller that lacks PDZ domains.
- **B.** Two SH2 domains specialized for recognizing phosphotyrosine-containing peptides.
- **C.** Two PDZ domains capable of recognizing short peptide motifs on partner proteins.
- **D.** A single SH3 domain specialized for recognizing proline-rich peptides.

The sequence is line-wrapped for readability; the exact original prompt is retained in `questions.jsonl` and the request artifact.

## Astra’s worked solution

C. Two PDZ domains is the most consistent architecture.

Sequence evidence:
The N-terminal portion contains two related-looking regions. Residues 24–43, EYGYNLHAEKGRGQFVGTVD, closely resemble residues 154–173, EFGFNLHAERGRGHFIGTVD. Similarity also occurs farther downstream: residues 59–80, IFAVNGHSIIGENHKKVVERIK, resemble residues 189–211, IVGVNGQLIYPTTGHKEVVALIK. Thus, the repetition is not confined to one short motif or a low-complexity run.

These extended patterns are characteristic of PDZ-like domain sequences: aromatic/glycine-containing early segments are followed by similarly organized hydrophobic and polar regions, including the recurring VNG-containing segment. Together, they support two related PDZ-sized modules. This is a family-level inference from the broader sequence pattern, not a claimed exact GLGF-motif match; PDZ sequences are variable and need not contain that literal string.

Biological interpretation:
PDZ domains are compact, usually approximately 80–110-residue α/β interaction modules. They commonly recognize short peptides at a partner protein's C terminus, accommodating the terminal carboxylate and nearby side chains in a binding groove. Some PDZ domains also recognize internal peptide motifs. This general interaction mechanism matches choice C, although the precise preferences of these two candidate domains cannot be assigned here.

Comparison with the alternatives:
• A: A WD40 β-propeller normally contains several shorter WD-repeat units. The WD at residues 239–240 is insufficient evidence: a single dipeptide does not establish a repeated propeller architecture. The extended PDZ-like duplication is more informative.
• B: SH2 domains can also occur in tandem, so repeat number alone would not distinguish them. However, the sequence does not show a convincing common SH2 phosphotyrosine-binding signature, such as an FLVRES-like region. Absence of that exact motif is not conclusive by itself, but there is positive evidence for PDZ-like repeats instead.
• D: Residues 128–133 are PPPPPP. Proline-rich sequences can be ligands for SH3 domains, but they are not themselves SH3 domains. SH3 domains are folded interaction modules, typically about 60 residues long; a single SH3 model also fails to account for the two extended PDZ-like regions.

Therefore, the strongest supported choice is a tandem-PDZ interaction-domain architecture.

## Final answer

C

## Astra’s stated limitations

Confidence applies to choosing the best architecture among the supplied alternatives. Sequence inspection does not establish exact domain boundaries, confirm that both domains bind peptides, or identify their physiological partners, preferred peptide sequences, or affinities.

Confidence reported by Astra: high.

## Post-generation verification

The following information was **not supplied to Astra**.

Verified source identity: **Na(+)/H(+) exchange regulatory cofactor-like protein nrfl-1** — [UniProt G5EDM4](https://www.uniprot.org/uniprotkb/G5EDM4/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-007/uniprot_record.json), withheld from Astra.

Source-supported answer: **C**. Astra’s selected answer matches it.

The primary study identifies the selected C. elegans NRFL-1 isoform as a two-PDZ-domain scaffold. It combines domain comparisons with direct binding experiments involving the end of the AAT-6 transporter. The results support recognition of short partner-protein peptide motifs by PDZ domains.

Scientific review: Strong sequence-based explanation.

- Extended similarity across two regions supports tandem domains. The explanation avoids inventing a literal GLGF motif and distinguishes a proline-rich SH3 ligand from an SH3 domain.
- PDZ-family recognition depends on learned family knowledge; neither precise domain boundaries nor physiological partners are demonstrated from sequence alone.

Strong biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- The literal motif GLGF occurs zero times in this selected sequence. A solution must not claim it found one or two exact GLGF motifs. PDZ loop sequences can differ.
- Some NRFL-1 splice variants contain only one PDZ domain; the answer here is specific to the selected two-domain sequence.
- The particular AAT-6 interaction and preference for PDZ2 require the paper. They are not proven by spotting two interaction domains.
- The Results text says mutation of PDZ2 impairs binding; a duplicated phrase in the Figure 2 caption is inconsistent. Prefer the Results text and source annotation rather than repeating the caption typo.

Papers and experimental references:

- [NRFL-1, the C. elegans NHERF orthologue, interacts with amino acid transporter 6 (AAT-6) for age-dependent maintenance of AAT-6 on the membrane](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0043050). Figure 1 and Results describe double-PDZ NRFL-1 isoforms; the interaction section and Figure 2 test recognition of the AAT-6 C-terminal motif. Review scope: Full primary article, especially NRFL-1 identification, Figure 1 and the PDZ interaction Results section.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.


---

# general-008 — Chromophore binding

[Original example and artifacts](../astra_sequence_only_nine_2026-10-23/examples/case-008.md)

# case-008 — binding site

Astra received only the student question below and the shared system instructions. Protein identity, gold answer, annotations and papers were withheld.

## Student question

Protein sequence:

```text
MVGLTTLFWLGAIGMLVGTLAFAWAGRDAGSGERRYYVTLVGISGIAAVAYVVMALGVGWVPVAERTVFA
PRYIDWILTTPLIVYFLGLLAGLDSREFGIVITLNTVVMLAGFAGAMVPGIERYALFGMGAVAFLGLVYY
LVGPMTESASQRSSGIKSLYVRLRNLTVILWAIYPFIWLLGPPGVALLTPTVDVALIVYLDLVTKVGFGF
IALDAAATLRAEHGESLAGVDTDAPAVAD
```

Task: binding site

Which chromophore-association mechanism is most consistent with this protein sequence?

- **A.** Covalent bilin attachment to a cysteine in a large phytochrome photosensory domain.
- **B.** Noncovalent FMN binding in a soluble LOV-domain pocket.
- **C.** Formation of an internal GFP-like chromophore by cyclization of residues in a soluble beta-barrel.
- **D.** Retinal attachment through a Schiff-base linkage to a lysine in a membrane-embedded opsin.

The sequence is line-wrapped for readability; the exact original prompt is retained in `questions.jsonl` and the request artifact.

## Astra’s worked solution

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

## Final answer

D

## Astra’s stated limitations

Sequence inspection does not demonstrate retinal occupancy, Schiff-base formation specifically at Lys205, or exact transmembrane-helix boundaries. Confidence is high for choosing among the supplied mechanisms, not for experimentally establishing the modification.

Confidence reported by Astra: high.

## Post-generation verification

The following information was **not supplied to Astra**.

Verified source identity: **Sensory rhodopsin-2** — [UniProt P42196](https://www.uniprot.org/uniprotkb/P42196/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-008/uniprot_record.json), withheld from Astra.

Source-supported answer: **D**. Astra’s selected answer matches it.

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


---

# general-009 — Post-translational modification chemistry

[Original example and artifacts](../astra_sequence_only_nine_2026-10-23/examples/case-009.md)

# case-009 — catalytic activity

Astra received only the student question below and the shared system instructions. Protein identity, gold answer, annotations and papers were withheld.

## Student question

Protein sequence:

```text
MAGCAARAPPGSEARLSLATFLLGASVLALPLLTRAGLQGRTGLALYVAGLNALLLLLYRPPRYQIAIRA
CFLGFVFGCGTLLSFSQSSWSHFGWYMCSLSLFHYSEYLVTAVNNPKSLSLDSFLLNHSLEYTVAALSSW
LEFTLENIFWPELKQITWLSVTGLLMVVFGECLRKAAMFTAGSNFNHVVQNEKSDTHTLVTSGVYAWFRH
PSYVGWFYWSIGTQVMLCNPICGVSYALTVWRFFRDRTEEEEISLIHFFGEEYLEYKKRVPTGLPFIKGV
KVDL
```

Task: catalytic activity

Which biochemical transformation is most consistent with this protein sequence?

- **A.** SAM-dependent methylation of the terminal carboxyl group of a prenylated cysteine on a protein substrate.
- **B.** Proteolytic removal of the three residues following a prenylated cysteine in a C-terminal CaaX motif.
- **C.** ATP-dependent phosphorylation of serine hydroxyl groups on protein substrates.
- **D.** ATP-dependent attachment of biotin to a lysine side chain on a protein substrate.

The sequence is line-wrapped for readability; the exact original prompt is retained in `questions.jsonl` and the request artifact.

## Astra’s worked solution

The most defensible choice is A: SAM-dependent methylation of the terminal carboxyl group of a prenylated cysteine.

1. Sequence architecture. This 284-residue protein contains repeated hydrophobic regions, including residues 16–34 (LSLATFLLGASVLALPLLT), 43–59 (GLALYVAGLNALLLLLY), 156–173 (ITWLSVTGLLMVVFGECL), and 213–241 (YVGWFYWSIGTQVMLCNPICGVSYALTVW). Their distribution supports a compact multipass membrane protein rather than a predominantly soluble enzyme. These are illustrative hydrophobic intervals, not established transmembrane-helix boundaries.

2. Family-level evidence. The C-terminal portion contains RHPSY at residues 209–213, matching an RHPxY pattern, and paired glutamates within EEYLEY at residues 261–266. In combination with the multipass architecture, these fit the RHP-containing and acidic C-terminal regions associated with ICMT/Ste14-family isoprenylcysteine carboxyl methyltransferases. The combination is more informative than either a short motif or hydrophobicity alone; it does not independently prove SAM binding or catalysis.

3. Biochemical interpretation. ICMT acts after a CaaX protein has been prenylated and its final three residues have been removed. That processing exposes the prenylated cysteine as the protein's terminal residue. ICMT transfers a methyl group from S-adenosylmethionine (SAM) to the terminal carboxylate oxygen, converting –COO− into the methyl ester –COOCH3 and producing S-adenosylhomocysteine. The modification is on the carboxyl group, not on the prenylated sulfur. A membrane-embedded enzyme is well suited to recognizing a lipid-modified protein substrate.

4. Comparison with the alternatives.
• B describes RCE1-type CaaX proteolysis, the processing step preceding ICMT-mediated methylation. RCE1 is also a multipass membrane enzyme, so membrane architecture alone does not exclude B. The ICMT-like C-terminal sequence features are the main reason to favor A.
• C requires an ATP-dependent protein-kinase catalytic domain. Conventional serine kinases have a substantial globular kinase fold; the extensively hydrophobic architecture here does not support such a domain. A kinase can be membrane-associated, but membrane anchoring is different from having hydrophobic segments distributed throughout nearly the entire catalytic protein.
• D describes biotin-protein ligase activity, which proceeds through ATP-dependent formation of biotinyl-AMP followed by attachment to lysine. Such enzymes require a globular adenylating catalytic domain, not the membrane-rich ICMT-like architecture observed here.

Thus, A best integrates the observed architecture, the C-terminal family-associated features, and the chemistry of prenylated-protein processing.

## Final answer

A

## Astra’s stated limitations

This is a sequence-based family assignment, not direct evidence of catalytic activity. Hydrophobicity alone cannot distinguish ICMT from the membrane CaaX protease RCE1. The C-terminal sequence features favor ICMT, but do not establish individual catalytic residues, membrane topology, or cellular localization.

Confidence reported by Astra: moderate.

## Post-generation verification

The following information was **not supplied to Astra**.

Verified source identity: **Protein-S-isoprenylcysteine O-methyltransferase** — [UniProt O60725](https://www.uniprot.org/uniprotkb/O60725/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-009/uniprot_record.json), withheld from Astra.

Source-supported answer: **A**. Astra’s selected answer matches it.

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


---

# mutation-001 — APEX: enzyme behavior depends on substrate conditions

[Original example and artifacts](../astra_enzyme_mutation_pool_2026-10-23/examples/case-001.md)

# case-001 — APEX peroxidase: mutation effect assay interpretation

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

Reference protein sequence (canonical wild-type backbone; coordinate reference only):

```text
MGKSYPTVSADYQKAVEKAKKKLRGFIAEKRCAPLMLRLAWHSAGTFDKGTKTGGPFGTIKHPAELAHSA
NNGLDIAVRLLEPLKAEFPILSYADFYQLAGVVAVEVTGGPEVPFHPGREDKPEPPPEGRLPDATKGSDH
LRDVFGKAMGLTDQDIVALSGGHTIGAAHKERSGFEGPWTSNPLIFDNSYFTELLSGEKEGLLQLPSDKA
LLSDPVFRPLVDKYAADEDAFFADYAEAHQKLSELGFADA
```


Reference: Q43758. All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded. The sequence is not the complete tagged assay construct.

Published variant identities:
APEX: substitutions K14D, W41F, E112K; deletions none.
APEX2: substitutions K14D, W41F, E112K, A134P; deletions none.

Supplied assay observations:
- With 1.4 mM guaiacol, the reported rate maximum occurs around 0.1 mM peroxide for APEX and 2.5 mM for APEX2; rates decrease above these ranges.
- With 0.5 mM guaiacol, the corresponding values are around 0.05 mM and 0.5 mM.

**Question:** Which interpretation best explains the variant difference across both substrate conditions?

- **A.** Only the higher-guaiacol condition shows an APEX2 advantage; the lower-guaiacol condition gives the same inhibition threshold for both enzymes.
- **B.** Both substrate conditions show a higher peroxide-inhibition threshold for APEX2, with unchanged thresholds when guaiacol concentration changes.
- **C.** Both substrate conditions show a higher peroxide-inhibition threshold for APEX2, with the threshold also depending on guaiacol concentration.
- **D.** Both substrate conditions give the same peroxide-inhibition threshold for APEX and APEX2, despite different guaiacol concentrations.


## Astra’s worked solution

Choice C captures both the variant difference and the dependence on guaiacol concentration.

Use the peroxide concentration at the reported rate maximum as an approximate boundary above which activity declines:
- At 1.4 mM guaiacol, the maximum occurs around 0.1 mM peroxide for APEX versus 2.5 mM for APEX2: approximately a 25-fold higher peroxide concentration for APEX2.
- At 0.5 mM guaiacol, the corresponding values are 0.05 mM and 0.5 mM: approximately a 10-fold higher concentration for APEX2.

Thus, both substrate conditions show a higher apparent peroxide-inhibition threshold for APEX2. The threshold is also guaiacol-dependent: increasing guaiacol from 0.5 to 1.4 mM shifts the maximum from 0.05 to 0.1 mM peroxide for APEX and from 0.5 to 2.5 mM for APEX2, approximately twofold and fivefold increases, respectively.

Mechanistically, peroxide drives formation of oxidizing heme intermediates during peroxidase catalysis, while guaiacol supplies reducing equivalents for productive turnover. Excess peroxide can promote nonproductive states or oxidative inactivation. Changing the electron-donor concentration can alter the balance between productive turnover and these competing processes, so an apparent peroxide-inhibition threshold need not be substrate-independent. This is consistent with the observations without establishing their precise molecular cause.

The listed sequence difference is A134P added to the shared K14D/W41F/E112K background. The assay observations establish the kinetic distinction; alanine-to-proline substitution chemistry alone would not uniquely predict it.

A is excluded because APEX2 also has a higher threshold at lower guaiacol. B is excluded because the thresholds change with guaiacol concentration. D is excluded because the variants have different thresholds under both conditions.

## Final answer

C

## Astra’s stated limitations

The reported rate maxima are approximate, condition-dependent markers, not formal inhibition constants. These observations do not distinguish reversible inhibition from oxidative inactivation, establish a structural mechanism for A134P, or show that APEX2 has a higher maximum rate. The canonical sequence provides coordinates, not the complete tagged assay construct.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **APEX peroxidase** — [UniProt Q43758](https://www.uniprot.org/uniprotkb/Q43758/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly compares both guaiacol conditions and checks the approximate concentration ratios.
- Explains the peroxide/electron-donor balance without converting apparent rate maxima into formal inhibition constants or asserting an unmeasured structural mechanism.
- The assay evidence establishes the phenotype; the sequence supports the A134P background comparison.

Source support:

- Figure 2e; accompanying Results paragraph on purified-protein kinetics
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- Values are approximate maxima reported in Results, not newly fitted kinetic constants.
- Use corrected Figure 2a symbols and Figure 2e axis labels; correction dated December 10, 2014.

Primary references:

- [Directed evolution of APEX2 for electron microscopy and proximity labeling](https://www.nature.com/articles/nmeth.3179)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# mutation-004 — Adenylate kinase: a conservative substitution can impair catalysis

[Original example and artifacts](../astra_enzyme_mutation_pool_2026-10-23/examples/case-004.md)

# case-004 — adenylate_kinase: mutation kinetic reasoning

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

Wild-type protein: Adenylate kinase (Escherichia coli K-12).
Full canonical wild-type sequence, numbered from the initial methionine as residue 1:

```text
MRIILLGAPGAGKGTQAQFIMEKYGIPQISTGDMLRAAVKSGSELGKQAKDIMDAGKLVTDELVIALVKE
RIAQEDCRNGFLLDGFPRTIPQADAMKEAGINVDYVLEFDVPDELIVDRIVGRRVHAPSGRVYHVKFNPP
KVEGKDDVTGEELTTRKDDQEETVRKRLVEYHQMTAPLIGYYSKEAEAGNTKYAKVDGTKPVAEVRADLE
KILG
```


Published variant(s): R156K.

Experimental evidence:
Published ATP-dependent kinetic measurements (central values; kcat in s^-1, ATP Km in micromolar):
WT: kcat 330, Km 71.
R156K: kcat 0.74, Km 52.
Arginine and lysine both normally carry a positive side-chain charge near neutral pH.

**Question:** Which interpretation best explains why calling R156K a conservative substitution does not establish functional conservation?

- **A.** The lower ATP Km compensates for the turnover loss, so R156K should retain near-WT catalytic efficiency when ATP is limiting.
- **B.** The lower ATP Km establishes stronger equilibrium ATP binding, so the turnover defect must arise entirely from slower product release.
- **C.** The roughly 450-fold turnover loss with a modest Km shift shows that retaining positive charge need not preserve residue-specific catalytic performance.
- **D.** The roughly 450-fold turnover loss directly measures a 450-fold reduction in correctly folded protein, while catalysis by the folded molecules remains unchanged.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.


## Astra’s worked solution

The best interpretation is C: chemical similarity does not guarantee functional conservation.

1. Quantitative evidence
The turnover decrease is:
330 / 0.74 ≈ 446-fold.
Thus, R156K has roughly 450-fold lower reported kcat than WT. In contrast, its ATP Km decreases only modestly:
52 / 71 ≈ 0.73,
a decrease of about 27%.

At ATP concentrations well below both Km values, with other assay conditions fixed, the rate per enzyme is approximately (kcat/Km)[ATP]. The relevant catalytic efficiencies are:
• WT: 330/71 ≈ 4.65 s^-1 μM^-1.
• R156K: 0.74/52 ≈ 0.0142 s^-1 μM^-1.

The mutant therefore retains only about 0.31% of WT ATP-dependent catalytic efficiency, a roughly 327-fold loss. The modest Km decrease does not compensate for the turnover defect, ruling out A.

2. Why a charge-conserving substitution can strongly impair function
Arginine and lysine are both normally positively charged near neutral pH, making this substitution conservative in a broad chemical classification. However, arginine's guanidinium group and lysine's terminal ammonium group differ in geometry, charge distribution, and hydrogen-bonding arrangements. In an enzyme, these differences can affect substrate positioning, transition-state stabilization, or conformational steps during turnover. These are general mechanistic possibilities, not specific interactions established for residue 156 by the supplied sequence. The observed kinetic loss nevertheless demonstrates that preserving positive charge does not preserve this variant's catalytic performance.

3. Why the other interpretations are unsupported
B incorrectly equates Km with an equilibrium dissociation constant. Even in the simple mechanism E + S ⇌ ES → E + P, Km = (koff + kcat)/kon, whereas Kd = koff/kon. Consequently, a lower Km can accompany slower turnover without stronger equilibrium binding. Adenylate kinase has a more complex, multisubstrate catalytic cycle, so the ATP Km likewise cannot automatically be interpreted as ATP binding affinity. Nothing supplied identifies slower product release as the sole cause of the turnover loss.

D incorrectly treats kcat as a direct measurement of folding. A lower reported kcat can reflect changes in chemistry or other turnover-limiting steps; depending on enzyme normalization, an inactive fraction can also affect apparent turnover. These measurements do not establish a 450-fold reduction in correctly folded protein or unchanged catalysis by the folded molecules.

Thus, the strong turnover defect with only a modest Km shift supports C.

## Final answer

C

## Astra’s stated limitations

The conclusion applies to the supplied ATP-dependent kinetic measurements. Neither the sequence nor these kinetic parameters uniquely identify the affected microscopic step, establish equilibrium ATP affinity, or quantify the folded or active protein fraction.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **adenylate_kinase** — [UniProt P69441](https://www.uniprot.org/uniprotkb/P69441/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

Correct remapped answer C. Correctly calculates about 446-fold lower turnover, about 327-fold lower ATP-dependent catalytic efficiency, and a 27% Km decrease. Connects the shared positive charge to different guanidinium/ammonium geometry and hydrogen bonding without claiming specific Arg156 contacts were observed. Correctly distinguishes Km from Kd, and treats changes in chemistry, conformational steps, product release and active fraction as possibilities rather than measured causes.

Source support:

- 2021 Figure 2c / Table S2; 2023 Table 1, WT and R156K rows.
- Published ATP-dependent kinetic measurements (central values; kcat in s^-1, ATP Km in micromolar):
WT: kcat 330, Km 71.
R156K: kcat 0.74, Km 52.
Arginine and lysine both normally carry a positive side-chain charge near neutral pH.
- Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.
- Table 1, footnote a.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. Published R36, R88, R123, R156 and R167 all match the reference residues.
- The prompt supplies the verified canonical reference and published mutation labels. No unreported affinity tag, cloning scar or exact expressed-construct extension is inferred.

Primary references:

- [Dynamic Connection between Enzymatic Catalysis and Collective Protein Motions](https://pmc.ncbi.nlm.nih.gov/articles/PMC8297476/). Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.

- [Mechanistic basis for a connection between the catalytic step and slow opening dynamics of adenylate kinase](https://pmc.ncbi.nlm.nih.gov/articles/PMC11779523/). Table 1, footnote a.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# mutation-015 — PafA: inactive protein fraction versus inhibitor binding

[Original example and artifacts](../astra_enzyme_mutation_pool_2026-10-23/examples/case-015.md)

# case-015 — PafA alkaline phosphatase: published enzyme mutation reasoning

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

Protein: PafA alkaline phosphatase.

Full canonical reference sequence (546 amino acids):

```text
MLTPKKWLLGVLVVSGMLGAQKTNAVPRPKLVVGLVVDQMRWDYLYRYYSKYGEGGFKRMLNTGYSLNNV
HIDYVPTVTAIGHTSIFTGSVPSIHGIAGNDWYDKELGKSVYCTSDETVQPVGTTSNSVGQHSPRNLWST
TVTDQLGLATNFTSKVVGVSLKDRASILPAGHNPTGAFWFDDTTGKFITSTYYTKELPKWVNDFNNKNVP
AQLVANGWNTLLPINQYTESSEDNVEWEGLLGSKKTPTFPYTDLAKDYEAKKGLIRTTPFGNTLTLQMAD
AAIDGNQMGVDDITDFLTVNLASTDYVGHNFGPNSIEVEDTYLRLDRDLADFFNNLDKKVGKGNYLVFLS
ADHGAAHSVGFMQAHKMPTGFFVEDMKKEMNAKLKQKFGADNIIAAAMNYQVYFDRKVLADSKLELDDVR
DYVMTELKKEPSVLYVLSTDEIWESSIPEPIKSRVINGYNWKRSGDIQIISKDGYLSAYSKKGTTHSVWN
SYDSHIPLLFMGWGIKQGESNQPYHMTDIAPTVSSLLKIQFPSGAVGKPITEVIGR
```


Numbering: mutation labels use positions in this full reference. The published HT-MEK PafA construct contains an initiating methionine followed by reference residues21–546, with a C-terminal linker and eGFP for the on-chip experiments. Within the PafA-only expressed ORF, canonical position n maps to position n-19. The full reference is supplied for unambiguous mutation indexing; it is not a claim that the native N-terminal segment was present in the assay.

Published observations:
The published H83G variant has a lower Pi inhibition constant than wild type, meaning stronger phosphate binding. The inhibition readout is a fractional rate v(I)/v(0) for the same variant. In a simple model with a long-lived inactive fraction, only the active population reacts and binds inhibitor, and its concentration multiplies both v(I) and v(0) by the same factor. There is no interconversion of populations during the measurement.

**Question:** Can a smaller active population alone explain the changed normalized inhibition constant?

- **A.** The inactive population changes the fitted inhibition constant because normalization removes enzyme concentration only from the uninhibited rate, leaving inhibitor-dependent population effects.
- **B.** Cancellation of the active-enzyme factor shows that H83G stabilizes the catalytic transition state more strongly, so stronger inhibition establishes faster intrinsic chemistry.
- **C.** A smaller active population lowers the inhibitor concentration needed to halve its fractional rate, so inactive abundance alone can explain stronger apparent binding.
- **D.** The common active-enzyme factor cancels from the fractional rate; the changed inhibition constant therefore requires more than uniform dilution by inactive protein.


## Astra’s worked solution

The reference confirms histidine at canonical position 83, the site of H83G. This identifies the substitution but does not, by itself, establish its effect on phosphate binding or catalysis. The decisive evidence is the normalized inhibition measurement and the supplied population model.

Let E_total be total enzyme concentration, f the fixed fraction belonging to the active population, and r(I) the rate per active enzyme at phosphate concentration I under otherwise identical assay conditions. Inhibition of active enzyme is included in r(I). Then:

v(I) = f E_total r(I)
v(0) = f E_total r(0)
v(I)/v(0) = r(I)/r(0).

Both the active fraction and total enzyme concentration cancel. If H83G changed only the abundance of inactive protein, its per-active-enzyme response r(I) would remain unchanged. Absolute rates would decrease, but the normalized inhibition curve—and therefore its fitted inhibition constant—would not shift. In particular, the phosphate concentration giving half of the uninhibited fractional rate would remain unchanged.

Consequently, the reported lower Pi inhibition constant requires more than uniform dilution by inactive protein. Within the stated model, it reflects an altered inhibition/binding response of the active population.

A is incorrect because the active-enzyme factor appears in both rates and cancels from their ratio. C is incorrect because decreasing active abundance alone cannot shift fractional half-inhibition. B correctly invokes cancellation but adds an unsupported conclusion: stronger binding of phosphate, a product inhibitor, does not establish greater catalytic transition-state stabilization or faster intrinsic chemistry. D states the justified conclusion.

## Final answer

D

## Astra’s stated limitations

The conclusion applies to the supplied fixed-population model. A reduced active fraction could coexist with stronger phosphate binding, but cannot alone explain the normalized inhibition shift. The evidence does not identify the molecular cause of the binding change or establish effects on expression, stability, or intrinsic chemistry.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- The active-fraction and enzyme-concentration factors cancel correctly from v(I)/v(0); the solution distinguishes an absolute-rate change from a normalized inhibition-curve shift.
- The conclusion is explicitly conditional on fixed, noninterconverting populations. It allows reduced active abundance to coexist with altered binding and does not infer faster chemical catalysis.
- His83 and canonical83 to expressed-ORF64 indexing are correct. The explanation uses the provided binding result and population model rather than asserting a sequence-only affinity prediction.

Source support:

- Fig.6B, FC2/FC3 section; Fig.3D model
- H83G is the representative strengthened-Pi-binding(FC2) mutant; the study separates long-lived inactive fractions from catalytic/binding effects.

Source qualifications:

- The result is conditional on the stated noninterconverting inactive-state model and normalization.
- Do not assume every inactive conformation cannot bind phosphate in all possible biological systems.
- Expression and assay conditions are distinct. These standard on-chip conditions are not assigned to separate off-chip or tagless measurements without explicit source support.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Revealing enzyme functional architecture via high-throughput microfluidic enzyme kinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454890/). Fig.6B, FC2/FC3 section; Fig.3D model

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
