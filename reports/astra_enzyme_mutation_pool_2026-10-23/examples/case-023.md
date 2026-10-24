# case-023 — PafA alkaline phosphatase: published enzyme mutation reasoning

**Assistant selection tier: moderate.** Generation status: `completed`.

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
The reference places His83 in the nucleophile helix(residues77–89), which contains Thr79. Ala165 lies immediately after Arg164 in the monoesterase helix(residues161–171), which also contains Lys162. The published H83G mutant strengthens Pi binding, while A165V weakens it. Neither substitution directly replaces Thr79,Lys162,or Arg164.

**Question:** Which mechanistic conclusion is supported without claiming an unobserved structure?

- **A.** Distinct local networks can shift phosphate interactions in opposite directions without replacing catalytic residues; proximity alone does not determine effect direction.
- **B.** Opposite phosphate-binding effects establish opposite changes in overall folding stability, making local interaction changes unnecessary to explain either mutant's behavior.
- **C.** Membership in active-site helices predicts the same phosphate-binding response; the opposite measurements therefore primarily indicate inconsistent normalization between the two mutants.
- **D.** A165V's weaker phosphate binding establishes displacement of Arg164 from its productive geometry, whereas H83G's stronger binding establishes improved positioning of Thr79.


## Astra’s worked solution

A is the supported conclusion.

Sequence and experimental observations: Using the supplied full-reference numbering and helix assignments, His83 shares the nucleophile helix with Thr79, while Ala165 immediately follows Arg164 in the monoesterase helix containing Lys162. Neither mutation replaces those specified catalytic residues. The reported binding measurements nevertheless have opposite directions: H83G strengthens Pi binding, whereas A165V weakens it. These directions are experimental observations, not predictions from the sequence.

Mechanistic interpretation: Phosphate affinity depends on the combined contributions of electrostatics, hydrogen bonding, hydration, packing, and the populations of binding-compatible conformations. Neighboring residues can influence these contributions without changing the identities of catalytic residues. H83G removes a histidine side chain, whereas A165V introduces a larger hydrophobic side chain at a different site. Such distinct perturbations can affect local interaction networks differently. Their proximity to active-site residues therefore does not require the same binding response. This supports A without specifying an unobserved rearrangement or claiming that any particular microscopic mechanism has been demonstrated.

Why the alternatives fail:
• B confuses ligand-binding energetics with overall folding stability. Stronger or weaker Pi binding does not establish corresponding changes in the folded-versus-unfolded equilibrium, and no folding-stability evidence is supplied.
• C assumes that membership in active-site helices determines the sign of an affinity change. Neither sequence proximity nor helix membership provides that rule, and there is no supplied evidence of inconsistent normalization.
• D converts plausible structural hypotheses into established facts. Weaker binding by A165V does not prove displacement of Arg164, and stronger binding by H83G does not prove improved positioning of Thr79. Multiple changes in interactions, hydration, or conformational populations could produce either result.

Finally, Pi binding is not a direct measure of catalytic performance. Pi is a phosphatase reaction product, so tighter binding alone does not establish faster catalysis or improved substrate specificity.

## Final answer

A

## Astra’s stated limitations

The observations establish opposite changes in Pi binding, but do not identify the altered atomic contacts or conformations. They also do not establish effects on overall folding stability, expression, catalytic rate, or substrate specificity.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **A**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- Correctly places His83 and Ala165 in the supplied helix intervals, confirms that the named catalytic residues are retained, and explains why proximity does not force the same binding response.
- Does not claim an observed Arg164 displacement, a uniquely improved Thr79 position, or a global folding change. The suggested interaction, hydration and conformational routes remain possibilities.
- Scientifically sound but less discriminating than the quantitative PafA examples: much of the solution restates the supplied opposite binding effects and lists compatible mechanisms rather than deriving a particular one.

Source support:

- Fig.1A helix definitions; Fig.6B and6G; BioC passages166 and176
- The nucleophile helix is77–89; monoesterase helix161–171. H83G and A165V exemplify strengthened and weakened Pi binding, respectively.

Source qualifications:

- Structural proximity and mutation identity do not reveal a unique atomistic mechanism.
- Do not treat weaker product binding as automatic evidence for faster chemistry or improved fitness.
- Expression and assay conditions are distinct. These standard on-chip conditions are not assigned to separate off-chip or tagless measurements without explicit source support.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Revealing enzyme functional architecture via high-throughput microfluidic enzyme kinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454890/). Fig.1A helix definitions; Fig.6B and6G; BioC passages166 and176

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
