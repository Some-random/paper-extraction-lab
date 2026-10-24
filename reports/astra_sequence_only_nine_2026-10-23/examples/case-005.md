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

[Frozen UniProt annotation](../artifacts/case-005/uniprot_record.json), withheld from Astra.

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
