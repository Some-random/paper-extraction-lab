# case-019 — PafA alkaline phosphatase: published enzyme mutation reasoning

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
PafA uses Thr79 as its nucleophile. The published T79S substitution retains a hydroxyl-bearing side chain but increases affinity for inorganic phosphate(Pi), the reaction product and a ground-state analog, by about100-fold. The authors discuss electrostatic repulsion between the anionic nucleophile and phosphate oxygens as a source of ground-state destabilization; greater nucleophile mobility after T79S is a proposed interpretation.

**Question:** Which statement is consistent with both the substitution chemistry and the reported phosphate-binding result?

- **A.** Serine preserves the catalytic hydroxyl, so the phosphate-affinity difference must arise entirely from a changed active fraction rather than local interaction geometry.
- **B.** Retained hydroxyl chemistry can accompany altered positioning and reduced phosphate repulsion; stronger ground-state binding does not by itself establish improved catalysis.
- **C.** Stronger phosphate affinity raises the inhibition constant; product inhibition consequently weakens, explaining why a conservative nucleophile substitution should accelerate turnover.
- **D.** The smaller serine side chain strengthens binding to phosphate and the transition state equally; the affinity change therefore establishes improved catalytic efficiency.


## Astra’s worked solution

B is consistent with both the substitution chemistry and the reported binding result.

1. Chemistry of the substitution. Threonine has a –CH(OH)CH3 side chain, whereas serine has –CH2OH. T79S therefore preserves a hydroxyl that can participate in nucleophilic chemistry, but changes the side chain’s size and steric constraints. Preserving the functional group does not guarantee preservation of its positioning, mobility, ionization, or interactions.

2. Observation versus interpretation. The supplied observation is approximately 100-fold stronger binding of inorganic phosphate by T79S. In equilibrium dissociation-constant terms, stronger affinity corresponds to a lower Kd. The proposed mechanism is that altered nucleophile positioning or increased mobility reduces repulsion between the anionic nucleophile and phosphate oxygens. Less unfavorable electrostatic interaction would favor phosphate binding and reduce ground-state destabilization. This explains how hydroxyl retention and stronger phosphate binding can coexist, without claiming that the proposed geometry has been demonstrated.

3. Binding is not equivalent to catalysis. Pi is the reaction product and a ground-state analog, not a direct measurement of transition-state stabilization. Catalytic rates depend on activation free-energy barriers, while catalytic efficiency depends on the kinetic pathway from free enzyme and substrate toward product. Stronger Pi binding alone therefore establishes neither faster turnover nor improved catalytic efficiency.

The alternatives fail for distinct reasons:
• A incorrectly makes an exclusive attribution to active fraction. Retaining a hydroxyl does not prevent changes in local interactions, and no supplied evidence assigns the affinity shift entirely to a change in the fraction of active protein.
• C reverses the affinity–constant relationship. Stronger binding means a smaller dissociation constant; if the same binding interaction governs inhibition, it would correspond to a smaller, not larger, Ki. The observation consequently does not establish weaker product inhibition or accelerated turnover.
• D assumes, without evidence, that phosphate and the transition state gain equal binding stabilization. A smaller side chain does not require such equal effects, and the reported phosphate affinity cannot establish improved catalytic efficiency.

Thus, B correctly separates retained hydroxyl chemistry, a plausible change in local electrostatics, and the unresolved consequences for catalysis.

## Final answer

B

## Astra’s stated limitations

The supplied data do not establish the mutant’s precise geometry, mobility, ionization state, active fraction, inhibition constant, or catalytic efficiency. Reduced phosphate repulsion is a compatible mechanistic interpretation, not a uniquely demonstrated consequence of the sequence change.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- Accurately contrasts the threonine and serine side chains: the hydroxyl remains while the methyl substituent is removed. It does not equate functional-group retention with identical positioning or energetics.
- Interprets stronger phosphate affinity as a smaller dissociation/inhibition constant under the relevant binding model, and avoids equating ground-state binding with improved turnover or efficiency.
- The reduced-repulsion/mobility explanation is kept as a compatible mechanistic model. No specific conformation, active fraction or measured intrinsic rate is invented; canonical79 to ORF60 mapping is correct.

Source support:

- FC2/FC3 section; Fig.6A; BioC passage56
- T79S increases Pi affinity about100-fold; reduced electrostatic repulsion through increased mobility is presented as a mechanistic interpretation.

Source qualifications:

- Treat the mobility/repulsion explanation as a supported model, not a measured trajectory.
- Do not replace the published approximate100-fold comparison with an exact value inferred from censored summary entries.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Revealing enzyme functional architecture via high-throughput microfluidic enzyme kinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454890/). FC2/FC3 section; Fig.6A; BioC passage56

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
