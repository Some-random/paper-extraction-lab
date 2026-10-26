# Ten protein reasoning problems

Worked answers are in ALL_EXAMPLES.md.

# 1. APEX: what transfers across assay conditions?

A published comparison of APEX and APEX2 reports the following approximate peroxide concentrations at which the measured reaction rate reaches its maximum and then declines:

| Guaiacol concentration | APEX | APEX2 |
|---|---|---|
| 1.4 mM | 0.1 mM peroxide | 2.5 mM peroxide |
| 0.5 mM | 0.05 mM peroxide | 0.5 mM peroxide |

Guaiacol is the electron-donor substrate in this purified-enzyme assay. The table gives the location of each rate maximum, not the height of that maximum. These are approximate reported observations, not fitted inhibition constants.

A colleague wants to summarize this result as a single fold improvement in APEX2's peroxide tolerance and use that number to predict which enzyme will have the greater reaction rate at an untested guaiacol concentration.

**Question:** Which replacement conclusion best preserves what these comparisons establish and what can be predicted at an untested guaiacol concentration?

**Choices:**

- **A.** Average the two fold differences to summarize tolerance, then use that factor to predict relative reaction rates when guaiacol lies between the tested concentrations.
- **B.** Use the smaller observed fold difference as a conservative tolerance improvement, then use that bound to predict APEX2's rate advantage at untested guaiacol concentrations.
- **C.** Report APEX2's higher concentration at the maximum in both conditions, with a condition-dependent ratio; these locations do not establish the reaction-rate ranking at an untested condition.
- **D.** Report separate fold improvements for the two conditions, then use each factor to scale APEX reaction rates when comparing the enzymes at that guaiacol concentration.

---

# 2. APEX: can staining measure delivery of a reporter fusion?

A published APX reporter study compared wild-type APX, a form with reduced self-association called mAPX, and a further reporter form called APEX. It reported:

- Wild-type APX and mAPX had similar activity in a purified-enzyme comparison using guaiacol, an aromatic model substrate.
- When fused to connexin43, wild-type APX was largely retained inside cells, whereas mAPX fusions reached gap junctions much more effectively.
- In a separate cytosolic comparison, mAPX gave weaker DAB staining than wild-type APX; supplying heme increased mAPX staining. DAB staining reports accumulated peroxidase-catalyzed product.
- APEX gave stronger cellular DAB staining than mAPX while retaining similar predominantly monomeric behavior.

An analyst wants to use cellular DAB intensity to rank how much connexin43 fusion reaches gap junctions across these reporter forms. Their argument is that similar purified guaiacol activity already controls for catalytic differences, leaving staining intensity to report correctly localized protein amount.

**Question:** Which interpretation best evaluates the proposed use of cellular DAB intensity to rank junction-localized fusion protein across these reporter forms?

**Choices:**

- **A.** Apply the guaiacol comparison as a catalytic calibration for DAB, then interpret cellular staining differences as differences in the amount of correctly localized active fusion protein.
- **B.** Use the heme-supplementation response to calibrate the active-enzyme fraction, then interpret remaining DAB differences as fusion delivery; the separate localization comparison supports improved mAPX trafficking.
- **C.** Keep trafficking and staining comparisons separate: similar guaiacol activity does not calibrate cellular DAB, and stronger APEX staining can coexist with similar predominantly monomeric behavior.
- **D.** Use similar oligomeric behavior to normalize APEX and mAPX before ranking delivery by DAB; interpret wild-type APX separately because its greater self-association can affect fusion trafficking.

---

# 3. Choosing a labeling tool for the measurement objective

The TurboID study reported a candidate sequence change that appeared beneficial for labeling activity and was included, with other changes, in TurboID. It was also examined in the miniTurbo background but was not retained there because labeling increased when added biotin was omitted. In the broader comparison, miniTurbo generally produced less labeling before biotin addition, whereas TurboID generally produced greater labeling yield.

These enzymes produce covalent labels. Omitting added biotin does not remove biotin already present in cells. The reported candidate-change comparison is qualitative; it supplies neither an isolated binding constant nor a protein-by-protein history of when labels formed.

Consider a project whose purpose is to associate recovered proteins with a defined interval beginning at biotin addition. It also needs enough recovered material for analysis. There are no project-specific measurements of background labeling or recovery yet.

**Question:** For this project, treat a defined labeling start time as the primary objective, subject to recovering enough material for analysis. Which provisional decision best uses the published comparison while respecting both requirements?

**Choices:**

- **A.** Prefer TurboID initially, taking its greater reported yield as evidence of faster labeling within the intended interval; reconsider if the project's recovered material is insufficient.
- **B.** Prefer miniTurbo initially, using its lower reported pre-addition labeling to serve the temporal objective; reconsider if project-specific background or inadequate recovery undermines that advantage.
- **C.** Withhold an initial preference because the published comparison is not project specific; project-specific background and recovery must be known before either candidate can receive provisional priority.
- **D.** Prefer TurboID initially, using subtraction of the omit-added-biotin signal to identify labels acquired within the interval; reconsider if project-specific recovery falls below the analytical requirement.

---

# 4. Inferring a cofactor from a motif combination

Protein sequence:

```text
MTIASSTASSEFLKNPYSFYDTLRAVHPIYKGSFLKYPGWYVTGYEETAAILKDARFKVRTPLPESSTKY
QDLSHVQNQMMLFQNQPDHRRLRTLASGAFTPRTTESYQPYIIETVHHLLDQVQGKKKMEVISDFAFPLA
SFVIANIIGVPEEDREQLKEWAASLIQTIDFTRSRKALTEGNIMAVQAMAYFKELIQKRKRHPQQDMISM
LLKGREKDKLTEEEAASTCILLAIAGHETTVNLISNSVLCLLQHPEQLLKLRENPDLIGTAVEECLRYES
PTQMTARVASEDIDICGVTIRQGEQVYLLLGAANRDPSIFTNPDVFDITRSPNPHLSFGHGHHVCLGSSL
ARLEAQIAINTLLQRMPSLNLADFEWRYRPLFGFRALEELPVTFE
```

**Question:** Which cofactor is most strongly supported by this protein sequence?

**Choices:**

- **A.** FAD
- **B.** FMN
- **C.** A four-iron four-sulfur cluster
- **D.** Heme

---

# 5. Recognizing repeated calcium-binding loops

Protein sequence:

```text
MPFHPVTAALMYRGIYTVPNLLSEQRPVDIPEDELEEIREAFKVFDRDGNGFISKQELGTAMRSLGYMPN
EVELEVIIQRLDMDGDGQVDFEEFVTLLGPKLSTSGIPEKFHGTDFDTVFWKCDMQKLTVDELKRLLYDT
FCEHLSMKDIENIIMTEEESHLGTAEECPVDVETCSNQQIRQTCVRKSLICAFAIAFIISVMLIAANQVL
RSGMK
```

**Question:** Which binding role is most consistent with the soluble region of this protein?

**Choices:**

- **A.** Binding calcium through EF-hand domains.
- **B.** Binding zinc through C2H2 zinc-finger domains.
- **C.** Binding heme within a peroxidase domain.
- **D.** Binding FAD within an oxidoreductase domain.

---

# 6. Separating membrane anchoring from topology

Protein sequence:

```text
MSSDFEGYEQDFAVLTAEITSKIARVPRLPPDEKKQMVANVEKQLEEARELLEQMDLEVREIPPQSRGMY
SNRMRSYKQEMGKLETDFKRSRIAYSDEVRNELLGDAGNSSENQRAHLLDNTERLERSSRRLEAGYQIAV
ETEQIGQEMLENLSHDREKIQRARDRLRDADANLGKSSRILTGMLRRIIQNRILLVILGIIVVIAILTAI
AFFVKGH
```

**Question:** Which overall membrane-association architecture best fits this protein sequence?

**Choices:**

- **A.** Peripheral membrane association without a membrane-spanning segment.
- **B.** A single C-terminal membrane anchor with a large upstream domain.
- **C.** Multiple membrane-spanning segments distributed throughout the protein.
- **D.** An N-terminal cleaved signal peptide followed by a soluble domain.

---

# 7. Distinguishing interaction domains from ligand motifs

Protein sequence:

```text
MVHIPSDVTPPRLCVVEKLNGENEYGYNLHAEKGRGQFVGTVDPDSPAERGGLITGDRIFAVNGHSIIGE
NHKKVVERIKANPNRCEMLVISEEGAKWYNENNVQITLDLPNIERVSPMSKETPVFVPPPPPPTDAMPYL
PRLAELNKGTPDQEFGFNLHAERGRGHFIGTVDAGGIGEKAGLEAGQRIVGVNGQLIYPTTGHKEVVALI
KKDTMKTTLLVASEDVDKYHKDHNIAYSWDNVERVDTRPVINVETHHHHEEVSVPKSNGYDVPPLNPHSI
QVNEEREISKMTTTTRTETITNSNSAYQYKESSTAYDAYATPPVDSNDLMDEVFGRVNLPGVTMSSHTEV
LPPTDDISSVSSLSSHRESAVDVPVSHQYVPSYATESHQKHEQHSQTHHHHHQHQQPSPLSNGSSHGYAA
SSTSGYDDDDIYHLSAREARERLRMKNRKHHLHEMSLNEKYQLVSNM
```

**Question:** Which protein-interaction domain architecture is most consistent with this sequence?

**Choices:**

- **A.** A WD40-repeat beta-propeller interaction scaffold.
- **B.** Two SH2 interaction domains for phosphotyrosine-containing peptides.
- **C.** Two PDZ interaction domains for short partner-protein peptides.
- **D.** One SH3 interaction domain for proline-rich partner peptides.

---

# 8. Judging a chromophore-binding hypothesis

Protein sequence:

```text
MVGLTTLFWLGAIGMLVGTLAFAWAGRDAGSGERRYYVTLVGISGIAAVAYVVMALGVGWVPVAERTVFA
PRYIDWILTTPLIVYFLGLLAGLDSREFGIVITLNTVVMLAGFAGAMVPGIERYALFGMGAVAFLGLVYY
LVGPMTESASQRSSGIKSLYVRLRNLTVILWAIYPFIWLLGPPGVALLTPTVDVALIVYLDLVTKVGFGF
IALDAAATLRAEHGESLAGVDTDAPAVAD
```

**Question:** Which chromophore-association mechanism is most consistent with this protein sequence?

**Choices:**

- **A.** Covalent bilin attachment to a cysteine in a large phytochrome photosensory domain.
- **B.** Noncovalent FMN binding in a soluble LOV-domain pocket.
- **C.** Formation of an internal GFP-like chromophore by cyclization of residues in a soluble beta-barrel.
- **D.** Retinal attachment through a Schiff-base linkage to a lysine in a membrane-embedded opsin.

---

# 9. Does a label reveal or change protein organization?

Published observations from a study of biotinylated neuroligin-1 on cultured neurons:

- Wild-type streptavidin has four functional biotin-binding sites. A1D3 is still a tetramer, but only one of its sites binds biotin.
- Tagged four-site and one-site preparations had similar soluble-biotin affinities. The cellular comparison used wild-type streptavidin and A1D3, so the affinity and cell experiments were not comparisons of exactly the same preparations.
- Both cellular labels initially appeared diffuse. Later, wild-type streptavidin labeling showed pronounced clustering while A1D3 labeling remained predominantly diffuse.

A collaborator concludes that the diffuse A1D3 image reveals native neuroligin organization and that similar soluble-biotin affinity makes further comparison unnecessary.

**Question:** Which initial comparison most directly tests a contribution from functional valency while accounting for differences in cellular target engagement and detection?

**Choices:**

- **A.** Compare one-, intermediate- and four-site probes at comparable measured initial target engagement, using an independently calibrated organization readout.
- **B.** Compare probe concentrations selected from soluble-biotin affinity estimates, using the original labeling images to quantify organization and initial target engagement.
- **C.** Compare preparations supplying equal total functional binding-site concentrations, using their matched initial surface fluorescence as the measure of target engagement.
- **D.** Compare the probes at equal tetramer concentrations, using identical imaging settings and the initially diffuse patterns as the baseline for organization.

---

# 10. What does exclusion from a proximity-labeling list mean?

Cho and colleagues compared proteins recovered by contact-targeted split-TurboID at endoplasmic reticulum–mitochondria contacts with proteins recovered using a cytosolic TurboID reference. The preparations used different labeling durations because their activities differed; overall labeling signals were comparable. The comparison measures accumulated labeling under those conditions.

Proteins were first compared with a no-added-biotin control and then filtered for enrichment in contact-targeted labeling relative to the cytosolic reference.

Consider a hypothetical protein P that reproducibly passes the no-added-biotin comparison but fails the contact-versus-cytosol enrichment filter. There are no independent localization measurements, protein-specific labeling kinetics, or functional measurements for P.

A collaborator proposes prioritizing proteins that passed both filters and deferring P because follow-up resources are limited. There is no independent evidence that P is especially important to this project's biological question.

**Question:** Given the stated resource limit and lack of independent evidence prioritizing P, which recommendation best follows the available evidence?

**Choices:**

- **A.** Follow up P first because passing the no-added-biotin comparison establishes contact association; treat the second filter as a measure of detection sensitivity.
- **B.** Prioritize the passing proteins and provisionally defer P; reconsider its priority if independent localization or functional evidence makes it relevant to the project.
- **C.** Defer P until its enrichment ratio is converted into contact occupancy; use that quantity to decide whether its contact-associated pool merits functional study.
- **D.** Follow up P first because failure of the cytosolic-reference filter identifies a dual-localized protein; treat that inferred pool as evidence of a missed contact function.
