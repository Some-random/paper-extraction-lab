# case-007 — PafA alkaline phosphatase: published enzyme mutation reasoning

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
For the already tested surface substitutions D473V and D473G, use FC1=(mutant/WT efficiency on MecMUP)/(mutant/WT efficiency on MeP). The published FC1 effect exceeds60-fold for D473V but is less than twofold for D473G. Asp473 lies about20Å from the relevant active-site oxygen-interaction region. If a change in active fraction multiplied both measured efficiencies by the same factor, that factor would cancel in FC1.

**Question:** What follows most directly from these observations?

- **A.** The two substitutions share one distant position, so their different FC1 values primarily reflect total enzyme abundance rather than distinct local perturbations.
- **B.** The greater FC1 effect establishes a gain in absolute diester efficiency; unchanged active-fraction normalization makes that gain independent of monoester activity.
- **C.** The larger FC1 can reflect lower active-enzyme abundance without requiring a difference in the mutation's effects on the two substrates being compared.
- **D.** D473V perturbs the relative substrate responses more strongly; long-range coupling is consistent with this result, while absolute diester enhancement remains unestablished.


## Astra’s worked solution

D is the most direct conclusion.

1. Observations and indexing. The reference contains Asp at canonical position 473, corresponding to position 454 in the stated PafA-only expressed ORF. The observations concern the supplied HT-MEK PafA–eGFP construct, not an assumed full-length native protein. The reported FC1 effect exceeds 60-fold for D473V but is less than twofold for D473G. The approximately 20 Å separation from the relevant active-site oxygen-interaction region is also supplied experimental context, not something inferred from sequence alone.

2. FC1 measures relative substrate response. Let R_di = efficiency(mutant, MecMUP)/efficiency(WT, MecMUP), and R_mono = efficiency(mutant, MeP)/efficiency(WT, MeP). Then FC1 = R_di/R_mono. Consequently, the larger effect for D473V establishes a stronger perturbation of the relative diester-versus-monoester response. It does not establish that R_di exceeds 1. A large FC1 could arise from enhanced diester efficiency, depressed monoester efficiency, or decreases on both substrates with a larger decrease on the monoester.

3. A common active-fraction effect cancels. If a factor q representing a mutant/WT change in active fraction multiplies both substrate efficiencies equally, then R_di = q × r_di and R_mono = q × r_mono. Therefore FC1 = (q × r_di)/(q × r_mono) = r_di/r_mono. Such a shared abundance or active-fraction effect cannot by itself explain the FC1 difference. The active fraction need not remain unchanged for this cancellation to occur.

4. Mechanistic interpretation. Sharing a position does not make two substitutions equivalent. Both replacements remove the Asp carboxylate, but valine introduces a branched hydrophobic side chain, whereas glycine lacks a side chain beyond hydrogen and permits different backbone conformations. These differences could produce distinct local perturbations. Given the supplied distance, their differing substrate responses are consistent with long-range coupling to functional regions, without establishing a particular structural or dynamical mechanism.

A and C incorrectly explain the ratio through abundance alone without a substrate-dependent effect. B mistakes a ratio of effects for an absolute diester gain and overlooks the monoester denominator. D correctly states the relative-response conclusion while retaining the appropriate uncertainty about mechanism and absolute enhancement.

## Final answer

D

## Astra’s stated limitations

The individual substrate efficiencies are not supplied, so absolute diester enhancement cannot be established. The observations also do not identify a specific coupling pathway or distinguish altered binding, catalytic steps, or substrate-dependent conformational effects. Cancellation applies to a shared multiplicative active-fraction effect.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- Correctly defines the specificity ratio and explains why a large FC1 need not mean improved absolute diester activity.
- The shared active-fraction factor cancels algebraically even when the active fraction changes; the solution makes this condition explicit.
- Contrasts valine and glycine chemistry without claiming an observed atomic rearrangement or a proven long-range pathway. Canonical473 to ORF454 mapping is correct.

Source support:

- Fig.5B,F; text describing D473/L434/I451; BioC passage54
- D473V has anFC1 effect>60-fold versus<2-fold for D473G at a solvent-exposed residue about20Å away; a specific local-folding/allosteric interpretation is proposed.

Source qualifications:

- Distance is a structural observation, not proof of a particular communication route.
- The conformational explanation remains a model; FC1 is not kcat and not an absolute improvement measure.
- Expression and assay conditions are distinct. These standard on-chip conditions are not assigned to separate off-chip or tagless measurements without explicit source support.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Revealing enzyme functional architecture via high-throughput microfluidic enzyme kinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454890/). Fig.5B,F; text describing D473/L434/I451; BioC passage54

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
