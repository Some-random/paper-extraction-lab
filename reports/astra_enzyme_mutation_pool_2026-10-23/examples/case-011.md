# case-011 — PafA alkaline phosphatase: published enzyme mutation reasoning

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
For the published Y103G variant, protein made at23°C had wild-type-like activity, whereas the tagless protein made at37°C had about260-fold less activity. The study separately held reaction conditions constant when testing expression-temperature effects. Y103G made at the lower temperature had a wild-type-like circular-dichroism spectrum; protein made at the higher temperature had an altered spectrum. The tagless result was included to test whether eGFP caused the effect.

**Question:** Which explanation is best supported, without equating the activity difference to a260-fold change in the rate constant of every folded molecule?

- **A.** Expression history changes the long-lived active and inactive populations; the tagless result argues against an explanation confined to the eGFP reporter.
- **B.** Different expression temperatures shift the reversible folded-unfolded equilibrium during the subsequent assay; the activity difference therefore reports equilibrium stability under assay conditions.
- **C.** Higher-temperature expression uniformly slows catalysis in correctly folded molecules; the entire activity loss can therefore be assigned to their intrinsic chemical-step rate constant.
- **D.** Temperature-dependent GFP maturation biases the enzyme-concentration estimate; the tagless result therefore attributes the activity difference primarily to reporter calibration rather than PafA.


## Astra’s worked solution

A is best supported: expression history changes the persistent functional populations of PafA, and the tagless result argues against a reporter-only explanation.

Sequence and construct: The reference contains Tyr103, so Y103G is a Tyr-to-Gly substitution within the retained PafA portion of the assay construct, not within the omitted N-terminal segment or eGFP. Removing an aromatic side chain and introducing glycine can affect folding and conformational preferences, but sequence alone does not establish the affected interaction or the mutation’s functional consequence.

Experimental evidence: Protein produced at 23°C had wild-type-like activity and a wild-type-like circular-dichroism spectrum. Higher-temperature production yielded an altered spectrum, and tagless protein produced at 37°C showed the approximately 260-fold activity loss. Crucially, reaction conditions were held constant when expression-temperature effects were tested. The comparison therefore concerns the consequences of protein production history, not simply the direct temperature dependence of an enzyme reaction.

Mechanistic interpretation: The coupled changes in activity and circular dichroism support different conformational ensembles being generated during production. An active-like population and a poorly active or inactive population could persist into the subsequent assay because their interconversion is slow on the measurement timescale. The altered spectrum supports structural differences in the ensemble, although it does not identify a particular misfolded state or prove that every high-temperature-produced molecule is inactive.

Why the activity ratio is not a chemical-step rate ratio: For activity normalized to total PafA, a simple population model is a_observed ≈ f_active × a_active when the inactive population contributes negligibly. Here a_active is the per-active-molecule activity under the assay conditions. A large reduction in f_active can therefore produce a large activity loss without a corresponding reduction in every active molecule’s catalytic rate. The observations do not separately determine these factors. Moreover, an overall activity measurement does not necessarily isolate the intrinsic chemical step.

Discriminating the alternatives:
• B incorrectly interprets production-temperature dependence as equilibrium stability during the assay. A reversible folding equilibrium established under identical assay conditions should not retain expression-history dependence. These observations instead support persistent states and do not measure equilibrium stability.
• C assigns the entire loss uniformly to correctly folded molecules’ chemical-step rate constants. Neither the bulk activity nor the altered circular-dichroism spectrum justifies that assignment.
• D reverses the significance of the tagless control. A large effect without eGFP cannot be explained solely by GFP maturation or GFP-based concentration calibration. The result argues against an explanation confined to the reporter, as stated in A.

## Final answer

A

## Astra’s stated limitations

The observations do not identify the inactive conformation, quantify active-state fractions or interconversion rates, or establish that all remaining active molecules have unchanged intrinsic kinetics. Sequence alone cannot determine Tyr103’s structural role or predict this temperature-dependent phenotype.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **A**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- Separates expression temperature from reaction temperature and correctly interprets persistence under matched assays as support for long-lived functional populations.
- The population equation separates active fraction from per-active-molecule activity; the260-fold bulk loss is not misreported as a260-fold chemical-step kcat change.
- Uses the tagless and circular-dichroism controls appropriately, without claiming a unique inactive structure or unchanged kinetics of every remaining active molecule. Canonical103 to ORF84 mapping is correct.

Source support:

- Fig.3D–K; TableS6; Figs.S39–S40 and TableS7; BioC passages38,41,43
- The tagless Y103G test gave wild-type-like activity after23°C expression and260-fold less after37°C expression; CD spectra differed. Standard expression-history tests used matched23°C/100μMZn assays.

Source qualifications:

- Do not claim that a CD change proves a unique atomic structure or equilibrium-unfolding mechanism.
- The exact reporter-free terminal tag sequence was not independently reconstructed; canonical PafA mutation numbering is verified, and the tagless condition is kept separate from the deposited eGFP construct.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Revealing enzyme functional architecture via high-throughput microfluidic enzyme kinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454890/). Fig.3D–K; TableS6; Figs.S39–S40 and TableS7; BioC passages38,41,43

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
