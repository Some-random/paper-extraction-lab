# case-003 — PafA alkaline phosphatase: published enzyme mutation reasoning

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
In wild-type PafA, Thr79 attacks the substrate phosphate and forms a covalent phospho-enzyme intermediate. The published T79G variant was used as a catalytically inactive control. Its eGFP signal showed that protein was expressed, and empty chambers were also retained to monitor local assay background.

**Question:** Which interpretation best connects the sequence change to the biochemical control?

- **A.** Comparable eGFP abundance makes remaining background activity an adequate estimate of intrinsic mutant turnover, provided the same normalization is applied to wild type.
- **B.** Removing Thr79's side-chain hydroxyl disrupts the usual covalent intermediate; an expression reporter does not demonstrate catalytic competence of the expressed PafA.
- **C.** T79G mainly reduces the amount of folded enzyme; matched eGFP abundance therefore isolates a selective folding defect rather than a catalytic defect.
- **D.** T79G primarily weakens phosphate-product binding; the reported loss of turnover therefore establishes product release as the rate-limiting step in the mutant.


## Astra’s worked solution

B best connects the sequence change to the biochemical control.

Sequence and experimental observations: The reference contains threonine at position 79. This position lies within the expressed reference segment 21–546 and maps to position 60 of the PafA-only expressed ORF; the omitted native N-terminal segment does not change which residue T79G denotes. The question explicitly identifies Thr79 as the nucleophile that attacks substrate phosphate and forms a covalent phospho-enzyme intermediate. That catalytic assignment comes from the supplied experimental information, not simply from finding a threonine in the sequence.

Mechanistic interpretation: Threonine has a side-chain hydroxyl whose oxygen can form the enzyme–phosphate bond. Glycine has a hydrogen side chain and lacks that hydroxyl. T79G therefore removes the functional group required for the usual Thr79-linked covalent intermediate. This provides a direct catalytic explanation for its reported use as an inactive control, without requiring an assumption that the protein was not expressed.

Control interpretation: The eGFP signal supports expression of the reporter-bearing construct. It does not establish that the PafA domain has a competent active site, is correctly folded, or contains the normal catalytic nucleophile. The stated observation also does not establish quantitatively matched abundance with wild type. Empty chambers monitor local assay background; a signal indistinguishable from that background is not evidence of intrinsic mutant turnover.

Why the other choices fail:
A: Even comparable eGFP abundance would not make background an adequate estimate of mutant catalysis. Applying the same expression normalization to wild type and mutant cannot convert background into enzyme-dependent turnover.
C: The evidence does not establish that reduced folding is the primary defect. Moreover, matched eGFP abundance would not isolate a PafA folding defect, because the reporter does not directly measure the folding of the PafA domain. Removal of the specified catalytic hydroxyl already supplies a mechanistic explanation.
D: No phosphate-product binding measurements or product-release kinetics are supplied. Loss of turnover after removing the catalytic nucleophile neither establishes weakened product binding nor identifies product release as rate-limiting.

Thus, the control demonstrates the distinction between detectable protein expression and catalytic competence, exactly as stated in B.

## Final answer

B

## Astra’s stated limitations

The supplied information does not quantify residual T79G turnover, the folded or active fraction of PafA, phosphate-product affinity, or individual catalytic rate constants. Additional structural effects of T79G cannot be excluded from sequence alone, but they are not needed to explain disruption of the specified catalytic mechanism.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- Correctly links removal of Thr79’s hydroxyl to loss of the normal covalent phospho-enzyme intermediate, without assuming loss of expression.
- Distinguishes the GFP reporter from active PafA, treats background as background, and does not invent a measured residual turnover or active fraction.
- Canonical Thr79 to expressed-ORF60 mapping is correct. Catalytic assignment is explicitly attributed to supplied observations rather than the sequence alone.

Source support:

- Fig.1A,H; Results: HT-MEK reproduces kinetic constants; BioC passages22 and24
- T79 is the covalent nucleophile; T79G lacks detectable activity and is used with empty chambers for local contamination/background controls.

Source qualifications:

- Do not assign exactly zero physical activity or a measured kcat to the inactive/upper-limit control.
- This addresses an already published substitution; it does not propose a new mutant or experiment.
- Expression and assay conditions are distinct. These standard on-chip conditions are not assigned to separate off-chip or tagless measurements without explicit source support.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Revealing enzyme functional architecture via high-throughput microfluidic enzyme kinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454890/). Fig.1A,H; Results: HT-MEK reproduces kinetic constants; BioC passages22 and24

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
