# case-027 — PafA alkaline phosphatase: published enzyme mutation reasoning

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
Define D_mono and D_di as mutant/wild-type catalytic-efficiency ratios for the phosphate monoester MeP and phosphate diester MecMUP, respectively; FC1=D_di/D_mono. The three tested variants D38G,D352G,and H353V alter zinc-ligand residues. D38G has an FC1 effect; D352G and H353V do not show a significant FC1 effect. In the structure, Asp38 accepts a hydrogen bond from Lys162, whereas Asp352 and His353 do not contact Lys162 or Arg164. Lys162/Arg164 interact with the phosphoryl oxygen that is anionic in the monoester and esterified in the diester.

**Question:** Which interpretation best explains the different specificity responses?

- **A.** All three substitutions affect the same metal center, so differences in FC1 primarily report unequal active fractions rather than substrate-selective catalytic interactions.
- **B.** D38G's FC1 effect establishes enhanced absolute diester turnover; its structural connection to Lys162 identifies increased diester catalysis as the cause of selectivity.
- **C.** Asp38 additionally connects to the oxygen-interaction network through Lys162; this coupling can distinguish monoester from diester effects despite shared metal-ligand status.
- **D.** An unchanged FC1 establishes preserved catalytic efficiency on both substrates; D352G and H353V therefore demonstrate that their zinc-ligand interactions are dispensable.


## Astra’s worked solution

C is the best interpretation: Asp38 connects zinc coordination to an interaction network that can discriminate between the two substrates.

Sequence and experimental context
The reference confirms the relevant wild-type residues. All lie within reference residues 21–546 retained in the assay construct; canonical numbering is used here. Their zinc-ligand assignments and three-dimensional contacts come from the supplied observations, not from sequence inspection alone.

All three substitutions alter zinc ligands, but their interaction contexts differ. Among these ligands, Asp38 accepts a hydrogen bond from Lys162, whereas Asp352 and His353 do not contact Lys162 or Arg164. D38G has an FC1 effect; the other two variants have no significant detected FC1 effect.

Mechanistic interpretation
Lys162 and Arg164 interact with an oxygen whose chemical environment differs between MeP and MecMUP: it is anionic in the monoester but esterified in the diester. Consequently, the positioning and electrostatic environment of these residues can contribute differently to the two catalytic efficiencies.

Replacing Asp38 with Gly removes the Asp side-chain carboxylate involved in both zinc coordination and the stated hydrogen bond to Lys162. This provides a plausible route for changing the substrate-discriminating network in addition to changing metal coordination. Such coupling can produce unequal monoester and diester effects. The absence of direct Lys162/Arg164 contacts for Asp352 and His353 is consistent with their different specificity responses, without implying that their metal interactions are catalytically unimportant.

What FC1 establishes
Writing catalytic efficiency as η = kcat/KM:

FC1 = [η_di(mut)/η_mono(mut)] / [η_di(WT)/η_mono(WT)].

Thus, FC1 measures a change in relative substrate preference, not an absolute turnover rate or an isolated binding affinity.

Why the alternatives fail
• A: Shared zinc-ligand status does not make the residues’ interaction networks equivalent. If a mutant/WT active-fraction factor is common to both substrate measurements, it multiplies both D values and cancels in FC1. Unequal active fractions across variants therefore do not, by themselves, explain different FC1 responses.
• B: An FC1 effect does not establish enhanced absolute diester turnover—or even enhanced diester catalytic efficiency. Its direction is not supplied. Even an increased FC1 could result from monoester efficiency decreasing more strongly while both efficiencies decline.
• D: No significant FC1 effect means no detected change in relative specificity, not preservation of both efficiencies. Both could decrease proportionally, leaving FC1 unchanged. These observations cannot establish that the zinc-ligand interactions are dispensable.

The discriminating evidence is therefore Asp38’s additional structural connection to Lys162 and the substrate-sensitive oxygen-interaction network, as stated in C.

## Final answer

C

## Astra’s stated limitations

The direction and magnitude of D38G’s FC1 effect and the individual catalytic-efficiency ratios are not supplied. The structural observations support differential coupling, but do not establish a unique mutant conformation or an increase in absolute diester activity. Lack of statistical significance does not prove exact equality.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- Builds a defensible mechanism from the supplied Asp38–Lys162 contact and the different chemical environments of the relevant monoester/diester oxygen. It does not infer those three-dimensional contacts from the sequence alone.
- Correctly interprets FC1 as a ratio of relative efficiencies, cancels a shared active-fraction factor and refuses to invent the direction or size of an effect not supplied to the solver.
- Separates a lack of significant specificity change from unchanged absolute activity and preserves uncertainty about a unique structural rearrangement. All residue identities match the canonical reference.

Source support:

- Fig.5A,E; TableS9A/B; BioC passages50–52
- D38G shows a specificity-component effect whereas D352G/H353V do not; D38 contacts K162 through a hydrogen bond. MeP/MecMUP probe the oxygen-interaction distinction.

Source qualifications:

- No significant FC1 effect does not mean no catalytic effect.
- Do not identify a specific atomistic rearrangement from the ratio alone or infer that all zinc dissociates.
- Expression and assay conditions are distinct. These standard on-chip conditions are not assigned to separate off-chip or tagless measurements without explicit source support.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Revealing enzyme functional architecture via high-throughput microfluidic enzyme kinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454890/). Fig.5A,E; TableS9A/B; BioC passages50–52

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
