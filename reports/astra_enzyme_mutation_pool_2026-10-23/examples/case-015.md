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
