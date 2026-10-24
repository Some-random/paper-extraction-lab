# case-031 — PafA alkaline phosphatase: published enzyme mutation reasoning

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
For the published K162A variant, catalytic efficiency(kcat/KM) for the methyl-phosphate reaction, whose chemical step is rate-limiting, is reduced by more than10^6-fold relative to wild type. Vanadate binding is weakened much less, by about10^2-fold. Vanadate is a transition-state analog, not the actual reacting transition state. Use these reported within-assay effects; they are not a cellular-fitness measurement or a direct measurement of kcat alone.

**Question:** What is the most justified conclusion from the mismatch?

- **A.** The residual vanadate affinity establishes substantial transition-state stabilization, so most catalytic loss should be assigned to reduced active-enzyme abundance rather than chemistry.
- **B.** The methyl-phosphate efficiency loss establishes the same change in first-order turnover; the analog comparison then distinguishes that turnover defect from altered substrate binding.
- **C.** Real catalysis is disrupted much more than analog binding; residual TSA affinity cannot establish preserved transition-state stabilization or retained catalytic power.
- **D.** Weaker vanadate binding quantitatively determines the catalytic defect, so its affinity change provides the appropriate correction for interpreting the larger methyl-phosphate effect.


## Astra’s worked solution

C is the most justified conclusion: real catalytic efficiency is disrupted far more than vanadate binding, so residual analog affinity cannot establish preserved transition-state stabilization or catalytic power.

Sequence and construct context: The reference confirms Lys162. Replacing lysine with alanine removes a long side chain capable of electrostatic and hydrogen-bonding interactions, but the sequence alone does not establish which interaction is important. The reported effects concern the specified assay construct, not an assumed full-length native protein.

Observed mismatch: K162A reduces methyl-phosphate kcat/KM by more than 10^6-fold, whereas vanadate affinity weakens by only about 10^2-fold. Thus, the fold effects differ by roughly four or more orders of magnitude. These are different observables: kcat/KM measures productive catalytic efficiency, while vanadate affinity measures binding of a stable ligand.

Mechanistic interpretation: Vanadate is a transition-state analog, not the actual reacting transition state. An analog can reproduce some transition-state features without reproducing its complete geometry, charge distribution, or interactions along the reaction coordinate. Consequently, a mutation can affect analog binding much less than it affects the activation barrier for real catalysis. Moreover, catalytic transition-state stabilization is evaluated relative to the relevant reactant states; residual binding to an analog does not directly measure that energetic advantage.

The supplied fact that chemistry is rate-limiting makes the methyl-phosphate result informative about a chemical-step-limited reaction. It does not, however, convert kcat/KM into kcat or uniquely separate substrate binding from chemical conversion.

Why the alternatives fail:
• A: Residual vanadate affinity does not establish substantial stabilization of the actual transition state. It also provides no basis for assigning most of the catalytic-efficiency loss to reduced active-enzyme abundance.
• B: kcat/KM is a second-order efficiency, whereas kcat is a first-order turnover constant. Even when chemistry limits turnover, an efficiency change does not establish the same fold change in kcat. Vanadate binding also does not directly measure methyl-phosphate binding, and KM is not generally an equilibrium binding constant.
• D: The vanadate affinity change cannot quantitatively determine or correct the catalytic defect without a justified relationship between analog binding and real catalysis. The reported mismatch shows that their mutational effects do not quantitatively track one another here.

Therefore, retained vanadate binding demonstrates retained ability to bind that analog—not retained catalytic power.

## Final answer

C

## Astra’s stated limitations

The observations do not separately determine kcat, KM, substrate affinity, active-enzyme abundance, stability, or the microscopic role of Lys162. The conclusion concerns the reported methyl-phosphate and vanadate assays; it does not imply that transition-state analog binding is always uninformative.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- Correctly contrasts the greater-than-millionfold catalytic-efficiency loss with the roughly hundredfold affinity loss; the disparity is about four or more orders of magnitude.
- Explains the imperfect physical correspondence of a stable transition-state analog to the actual transition state, while distinguishing catalytic efficiency, first-order turnover and substrate affinity.
- Does not use residual analog binding to infer preserved catalytic power or to assign the defect to active abundance. Canonical Lys162 to expressed-ORF143 mapping is correct.

Source support:

- Fig.3A; Results: Active-Site and Second-Shell mutations; PDFpage4 / BioC passage21
- K162A is an active-site exception:>10^6-fold catalytic loss versus~10^2-fold weaker vanadate binding. MeP chemistry is the relevant rate-limiting comparison.

Source qualifications:

- Binding affinity weakens rather than increases; retain that direction.
- The result does not specify a unique structural cause or imply every TSA is uninformative.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Decoupling of catalysis and transition state analog binding from mutations throughout a phosphatase revealed by high-throughput enzymology](https://pmc.ncbi.nlm.nih.gov/articles/PMC10629569/). Fig.3A; Results: Active-Site and Second-Shell mutations; PDFpage4 / BioC passage21

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
