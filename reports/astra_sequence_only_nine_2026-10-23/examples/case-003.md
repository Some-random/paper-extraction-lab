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

[Frozen UniProt annotation](../artifacts/case-003/uniprot_record.json), withheld from Astra.

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
