# Ten protein reasoning problems and worked answers

# 1. APEX: what transfers across assay conditions?

## Question

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

## Answer

**Answer: C.**

APEX2 reaches its rate maximum at a higher peroxide concentration than APEX in both tested guaiacol conditions, but the magnitude of that difference depends on the condition. The repeated direction supports a comparative response under those conditions, not a single improvement factor that predicts reaction rates elsewhere.

At 1.4 mM guaiacol, the peroxide concentrations at the maxima are approximately 2.5 mM for APEX2 and 0.1 mM for APEX, a 25-fold difference. At 0.5 mM guaiacol, they are approximately 0.5 mM and 0.05 mM, a 10-fold difference. One fold-improvement factor would conceal this change in magnitude. Each enzyme's maximum also shifts when guaiacol changes. These approximate peak locations describe the measured response; they are not fitted inhibition constants.

Peak location and peak height are different quantities. The table supplies no absolute rates or curve shapes. An enzyme can reach its maximum at a higher peroxide concentration without having the higher maximum rate or the higher rate at a particular peroxide concentration. The table therefore cannot establish a rate ranking at the tested conditions or predict one at an untested guaiacol concentration.

A averages a condition-dependent response and converts it into an unsupported rate prediction. B treats the smaller observed ratio as a bound beyond the observations and makes the same quantity error. D retains the two conditions but still uses peak-position ratios to scale unreported rates. C preserves both the observed comparison and the distinction between concentration and rate.

<details>
<summary>Sources and qualifications</summary>

Primary source: [Lam et al., Directed evolution of APEX2 for electron microscopy and proximity labeling](https://doi.org/10.1038/nmeth.3179), Figure 2e and the accompanying purified-protein kinetics Results. The reported comparison uses the corrected Figure 2e axis labels; the correction is dated December 10, 2014.

The supplied evidence consists of two guaiacol conditions and approximate peroxide concentrations at the reported rate maxima. No absolute reaction rates, fitted inhibition constants, or measurements at an additional condition are supplied. The colleague's proposed summary and transfer claim are hypothetical teaching scenarios, not statements attributed to the paper.

Source identity: [UniProt Q43758](https://www.uniprot.org/uniprotkb/Q43758/entry) is wild-type soybean (*Glycine max*) ascorbate peroxidase. Pea APX has a different accession, [P48534](https://www.uniprot.org/uniprotkb/P48534/entry). A canonical wild-type sequence is a reference backbone, not the complete engineered, tagged assay construct.

</details>

---

# 2. APEX: can staining measure delivery of a reporter fusion?

## Question

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

## Answer

**Answer: C.**

The supplied comparisons do not calibrate cellular DAB intensity as a ranking of how much connexin43 fusion reaches gap junctions. They measure purified activity, fusion localization, and cellular staining in different settings.

The similar purified guaiacol activities apply to that assay's conditions. They do not establish equal catalytic output with DAB in cells. Guaiacol and DAB are different substrates, and cellular staining depends on more than the catalytic competence demonstrated by a purified preparation. Even an equal-molecule comparison with guaiacol would not establish equal DAB activity per molecule in cells. The purified result therefore supplies no conversion factor from staining intensity to protein amount.

The connexin43 comparison supports improved fusion trafficking: mAPX fusions reached gap junctions more effectively than wild-type APX fusions. Reduced self-association is a plausible explanation for less interference with the fusion partner, although the supplied observations do not identify every contribution to trafficking. The weaker mAPX staining was observed in a separate cytosolic comparison, so it does not show that less mAPX–connexin43 reached gap junctions. Improved delivery and weaker catalytic staining can coexist because they describe different properties in different comparisons.

The heme-supplementation result also argues against treating staining as a simple molecule count. APX requires heme for catalytic activity. Increased staining after heme supply is consistent with more available active, heme-containing enzyme, but it does not directly measure total protein abundance, fusion delivery, or equilibrium heme affinity. Cellular heme availability and incorporation, folding, stability, and substrate-dependent performance can all influence the readout. The response supports an active-enzyme contribution without identifying weaker heme affinity as the unique cause of mAPX's lower signal.

APEX produced stronger cellular DAB staining than mAPX while retaining similar predominantly monomeric behavior. Staining performance can therefore differ without a further reported difference in that oligomeric property. These supplied comparisons alone do not quantify the contributions of catalytic performance, active-enzyme fraction, and protein amount to the signal difference. Similar monomeric behavior does not normalize those quantities.

Fusion trafficking and staining output must therefore be interpreted separately. Better connexin43 delivery with mAPX and stronger cellular staining with APEX are supported in their respective comparisons; together they do not establish a three-way ranking of junction-localized fusion abundance. DAB remains an informative catalytic endpoint, but the supplied evidence does not calibrate it for that ranking.

A assumes transfer between substrates and cellular contexts. B treats a qualitative downstream heme response as a quantitative calibration that was not supplied. D treats similar oligomeric behavior as control for catalytic performance and active-enzyme abundance. C avoids these assumptions while preserving the supported trafficking and staining results.

<details>
<summary>Sources and qualifications</summary>

Primary source: [Martell et al., Engineered ascorbate peroxidase as a genetically encoded reporter for electron microscopy](https://doi.org/10.1038/nbt.2375), Figure 1b–e and accompanying Results on self-association and connexin43 trafficking, and Figure 2b–d and accompanying Results on purified activity, cellular DAB staining, and heme supplementation.

The four supplied observations paraphrase the published comparisons. The proposed DAB-based ranking of junction delivery is hypothetical teaching material. The cytosolic and connexin43-fusion observations concern different comparisons and do not provide a common calibration of staining to localized fusion amount.

Heme-dependent active-enzyme availability is a compatible explanation, not a uniquely identified microscopic cause. Predominantly monomeric behavior is condition dependent; it is not asserted at every concentration. These qualifications concern what follows from the supplied observations rather than an exhaustive account of the paper's evidence.

</details>

---

# 3. Choosing a labeling tool for the measurement objective

## Question

The TurboID study reported a candidate sequence change that appeared beneficial for labeling activity and was included, with other changes, in TurboID. It was also examined in the miniTurbo background but was not retained there because labeling increased when added biotin was omitted. In the broader comparison, miniTurbo generally produced less labeling before biotin addition, whereas TurboID generally produced greater labeling yield.

These enzymes produce covalent labels. Omitting added biotin does not remove biotin already present in cells. The reported candidate-change comparison is qualitative; it supplies neither an isolated binding constant nor a protein-by-protein history of when labels formed.

Consider a project whose purpose is to associate recovered proteins with a defined interval beginning at biotin addition. It also needs enough recovered material for analysis. There are no project-specific measurements of background labeling or recovery yet.

**Question:** For this project, treat a defined labeling start time as the primary objective, subject to recovering enough material for analysis. Which provisional decision best uses the published comparison while respecting both requirements?

**Choices:**

- **A.** Prefer TurboID initially, taking its greater reported yield as evidence of faster labeling within the intended interval; reconsider if the project's recovered material is insufficient.
- **B.** Prefer miniTurbo initially, using its lower reported pre-addition labeling to serve the temporal objective; reconsider if project-specific background or inadequate recovery undermines that advantage.
- **C.** Withhold an initial preference because the published comparison is not project specific; project-specific background and recovery must be known before either candidate can receive provisional priority.
- **D.** Prefer TurboID initially, using subtraction of the omit-added-biotin signal to identify labels acquired within the interval; reconsider if project-specific recovery falls below the analytical requirement.

## Answer

**Answer: B.**

miniTurbo is the better-supported provisional starting candidate for the stated temporal priority because of its lower reported pre-addition labeling. Adequate recovery remains a feasibility constraint: a cleaner start is insufficient if too little usable material is recovered. This preference does not establish that miniTurbo will perform better in the project's actual context.

The covalent labels record a history of enzyme activity. Omitting added biotin does not remove biotin already in cells, so labeling before the intended start can contribute to material recovered later. A stronger accumulated signal need not contain more information about the interval of interest. Temporal interpretation depends on the pre-start contribution as well as on the amount of useful recovery.

The most decision-relevant missing evidence is project-specific background and recovery: how much pre-addition labeling contributes, and whether the amount and reproducibility of useful recovery meet the analytical need. Adequate miniTurbo recovery with substantially less pre-start contribution would support the initial preference. Inadequate recovery could instead make TurboID more useful, with a timing compromise that greater yield alone would not resolve. The published comparison does not establish these project-specific outcomes.

The candidate change illustrates why greater activity need not serve this objective. Its increased omit-added-biotin signal in the tested miniTurbo background counts against temporal control. Inclusion with other changes in TurboID does not establish the same isolated effect in both backgrounds, and the qualitative observations identify neither an affinity change nor a particular catalytic mechanism.

For an objective prioritizing cumulative yield, TurboID's greater reported yield could instead justify initial priority. Pre-addition activity would carry less penalty only if accumulated labeling remained appropriate to that biological question.

A converts accumulated yield into evidence about within-interval labeling rate. C requires project-specific background and recovery to be known before even a provisional preference is allowed. Those data are needed to assess actual project performance, but the reported comparison and stated priority already support a provisional starting choice. D assumes that subtracting an aggregate background identifies when individual labels formed; subtraction can describe a signal difference without assigning recovered labels exclusively to the intended interval. B retains both the temporal priority and the recovery constraint.

<details>
<summary>Sources and qualifications</summary>

Primary source: [Branon et al., Efficient proximity labeling in living cells and organisms with TurboID](https://doi.org/10.1038/nbt.4201), Methods under “Yeast display directed evolution” for the reported candidate-change decision, Figure 2a–b and Discussion for the yield/background comparison, and Supplementary Note 2 for labeling chemistry and qualified mechanistic interpretations.

The qualitative activity and omit-added-biotin observations, broader tool comparison, and labeling chemistry are source-derived. The proposed project and its alternative objectives are hypothetical teaching scenarios. No quantitative effect size or project-specific background, recovery, or temporal performance is supplied.

The candidate-change observation applies to the reported miniTurbo background. The comparison does not isolate an affinity change, a catalytic constant, or the cause of any difference between backgrounds. Covalent labeling can persist after the time of formation, subject to turnover and other biological processes; it is not a timestamp or a claim of permanent labeling.

</details>

---

# 4. Inferring a cofactor from a motif combination

## Question

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

## Answer

**Answer: D.**

The strongest assignment is a heme-containing cytochrome P450. The evidence is a combination of sequence features in the appropriate order, rather than the presence of a metal-binding amino acid by itself.

The most direct clue is FGHGHHVCLG at residues 338–347. It matches the P450-associated pattern FxxGxxxCxG, where x can be any residue. The cysteine in this pattern is Cys345. In P450 enzymes, the corresponding cysteine supplies a thiolate sulfur that coordinates the heme iron. This makes Cys345 a plausible axial ligand and connects the sequence pattern to a specific cofactor-binding chemistry. The sequence predicts cysteine–iron coordination, not direct attachment of the porphyrin ring to the polypeptide.

Two other regions strengthen the family assignment. ECLR at residues 274–277 matches the characteristic P450 E-x-x-R pattern. This supports the P450 core architecture; it is not itself a direct heme-binding site. AGHETT at residues 235–240 contains an acidic residue and adjacent threonines consistent with the I-helix region involved in oxygen activation in many P450s. Calling it an I helix is a family-based structural inference, not an observed secondary structure. These regions precede the cysteine-containing signature in the expected sequence order, so they provide mutually consistent support.

An iron–sulfur cluster (C) is a reasonable alternative to consider when a sequence contains cysteines. However, cysteine presence alone does not distinguish an iron–sulfur ligand from a heme ligand or an unrelated cysteine. Here, the specific cysteine-containing signature together with the supporting P450 patterns explains the evidence better than a generic iron–sulfur assignment. FAD (A) and FMN (B) occur in diverse flavin-binding families, but neither assignment explains this combined P450 pattern as well. Their rejection rests on stronger positive evidence for heme, not on the absence of a supposed universal flavin-binding motif.

The supported conclusion is a strong P450/heme hypothesis. The sequence does not demonstrate that the protein actually contains heme, identify its substrate or establish its reaction specificity and catalytic activity. Those are separate claims from recognizing a cofactor-binding family.

<details>
<summary>Sources and qualifications</summary>

Source identity: biotin biosynthesis cytochrome P450, [UniProt P53554](https://www.uniprot.org/uniprotkb/P53554/entry). The primary structure supports heme and coordination by Cys345. Its substrate complex supplies experimental context for specificity; the anonymous sequence does not independently establish that substrate or the biotin-biosynthesis role.

Primary reference: [Structural insights from a P450 carrier protein complex reveal how specificity is achieved in the P450BioI ACP complex](https://pmc.ncbi.nlm.nih.gov/articles/PMC2572933/), especially Active Site Architecture.

The source supports the family/cofactor assignment. Actual heme occupancy and catalytic specificity are distinct from the sequence-based inference in the answer.

</details>

---

# 5. Recognizing repeated calcium-binding loops

## Question

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

## Answer

**Answer: A.**

The likely soluble region supports an EF-hand calcium-binding architecture, with two particularly convincing candidate loops. They are DRDGNGFISKQE at residues 46–57 and DMDGDGQVDFEE at residues 82–93.

An EF hand contains a calcium-binding loop of about 12 residues between two helices. The informative feature here is the arrangement of potential ligands within each loop. In DRDGNGFISKQE, positions 1, 3 and 5 are Asp, Asp and Asn. In DMDGDGQVDFEE, those positions are all Asp. Both loops have glycine at position 6 and glutamate at position 12. Asp, Asn and Glu provide oxygen-containing groups compatible with calcium coordination. Glycine can accommodate the tight loop geometry, while the terminal glutamate commonly contributes its carboxylate to calcium binding. The repeated positional pattern is therefore chemically and structurally coherent.

This is stronger evidence than high acidic content alone. A nonspecific acidic region could interact with positively charged ions, but acidity does not specify a calcium-binding fold. Two separate segments with the same ligand-compatible positions, loop length and conserved glycine are more suggestive of repeated binding modules than an arbitrary Asp/Glu-rich stretch would be. The interpretation depends on their organization, not simply on counting negative charges.

The candidate loops lie well upstream of the hydrophobic near-terminal sequence LICAFAIAFIISVMLIAA. That distribution is consistent with a soluble binding region attached to a membrane through a C-terminal anchor. It helps place the proposed ion-binding loops outside the hydrophobic segment, but does not establish membrane orientation or the protein’s cellular destination.

B would require the characteristic Cys/His arrangement of a C2H2 zinc finger; scattered cysteines and histidines do not supply that architecture. The heme- and FAD-binding roles in C and D likewise do not explain the two repeated ligand-compatible loop patterns as directly as the EF-hand assignment.

The sequence supports candidate EF hands; it does not directly demonstrate their three-dimensional fold or prove that both bind ions under physiological conditions. Nor does it measure calcium affinity, calcium-versus-magnesium selectivity, occupancy or a calcium-dependent conformational change. The architecture prediction and the biochemical properties of its sites require different evidence.

<details>
<summary>Sources and qualifications</summary>

Source identity: human calcium-binding protein 7 (CaBP7), [UniProt Q86V35](https://www.uniprot.org/uniprotkb/Q86V35/entry). The primary abstract and experimental deposition support two high-affinity N-terminal calcium sites. The NMR construct omits the full canonical C-terminal region.

Primary references: [Solution NMR structure of the Ca2+-bound N-terminal domain of CaBP7: a regulator of Golgi trafficking](https://pubmed.ncbi.nlm.nih.gov/22989873/) and [experimental structure PDB 2LV7](https://www.rcsb.org/structure/2LV7).

Those experimental findings support the EF-hand assignment, but affinity, ion selectivity and calcium-dependent structural changes cannot be read directly from the anonymous sequence. The complete sequence’s proposed membrane anchor is outside the NMR construct.

</details>

---

# 6. Separating membrane anchoring from topology

## Question

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

## Answer

**Answer: B.**

The sequence strongly supports a protein with one membrane anchor near its C terminus and a much larger region outside the bilayer. Its most conspicuous feature is ILLVILGIIVVIAILTAIAFFV at residues 193–214: a continuous 22-residue hydrophobic stretch followed by only KGH.

That combination of length, composition and position is appropriate for a membrane-spanning alpha helix. There are no charged residues within this stretch, whereas the surrounding protein contains many charged and polar residues. Placing such a long hydrophobic segment in the lipid bilayer provides a more coherent interpretation than the purely peripheral membrane association in A. Peripheral association can occur through interactions with lipids or other proteins, but does not by itself explain this pronounced hydrophobic tail.

The upstream region does not contain several comparable hydrophobic stretches. The sequence therefore supports one anchor rather than the multipass membrane bundle in C. Its C-terminal position also differs from the N-terminal cleaved signal peptide proposed in D. The anchor’s near-terminal position and very short following tail are also consistent with a tail-anchored architecture. This is an architectural assignment, not identification of the cellular machinery or route that inserts it.

Orientation is a separate, less certain inference. The RRIIQNR segment at residues 186–192 places several basic residues immediately before the candidate anchor. This agrees with the positive-inside tendency, in which positively charged flanks often occur on the cytosolic side of membrane-spanning helices. It therefore supports a cytosolic location for the large upstream region. However, a tendency is not a direct observation, and saying that a region lies outside the bilayer does not by itself identify which membrane side it occupies.

Residues 193–214 describe a hydrophobic-composition window, not a measured helix boundary. A structural boundary could differ slightly without changing the overall conclusion. The sequence alone does not establish the exact membrane-spanning endpoints, prove orientation, identify the insertion pathway or distinguish a Golgi, endosomal or other membrane destination. Confidence is strongest for the single C-terminal anchor and weaker for those more specific cellular assignments.

<details>
<summary>Sources and qualifications</summary>

Source identity: Vti1-rp2/Vti1a, [UniProt O89116](https://www.uniprot.org/uniprotkb/O89116/entry). The primary abstract supports a C-terminal anchor, cytoplasmic region and integral membrane behavior.

| Evidence | Residues | Interpretation |
|---|---|---|
| Hydrophobic composition of the supplied sequence | 193–214 | A continuous 22-residue hydrophobic stretch, followed by KGH. |
| UniProt annotated helical anchor | 193–213 | Annotated helix; V214 belongs to the following vesicular region. |
| UniProt topological domains | 1–192 cytoplasmic; 214–217 vesicular | Annotation-based orientation and residue partition. |

The [frozen UniProt record](artifacts/example-06/frozen_uniprot_record.json) assigns all three topology features evidence code ECO:0000255 (sequence analysis). The RRIIQNR flank at residues 186–192 and the proposed cytosolic upstream region agree with that annotation. This agreement does not independently demonstrate residue-exact boundaries or orientation: the annotation itself is based on sequence analysis. An extramembrane assignment alone does not specify the cytoplasmic side. The answer’s confidence is therefore based on the anonymous sequence, with stronger evidence for the anchor than for orientation.

Primary reference: [A 29-kilodalton Golgi soluble N-ethylmaleimide-sensitive factor attachment protein receptor (Vti1-rp2) implicated in protein trafficking in the secretory pathway](https://pubmed.ncbi.nlm.nih.gov/9705316/). The abstract’s experimental cellular context supports the broad topology; it does not turn either sequence-based window into a measured membrane boundary.

</details>

---

# 7. Distinguishing interaction domains from ligand motifs

## Question

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

## Answer

**Answer: C.**

A reasonable hypothesis is a tandem arrangement of two PDZ-like interaction modules. The clearest sequence evidence is extended similarity between two regions of the N-terminal portion, rather than one short conserved word or a low-complexity repeat.

For example, EYGYNLHAEKGRGQFVGTVD at residues 24–43 resembles EFGFNLHAERGRGHFIGTVD at residues 154–173. Both contain related aromatic/glycine-rich portions followed by a similar GTVD-containing segment. The similarity continues farther along the candidate modules: IFAVNGHSIIGENHKKVVERIK at residues 59–80 resembles IVGVNGQLIYPTTGHKEVVALIK at residues 189–211. Agreement across separated parts of each region is more informative than matching a single short motif. It supports two related modules with internal sequence complexity.

The broader pattern is compatible with PDZ domains, compact interaction modules whose folded binding grooves often recognize short peptides at the C termini of partner proteins. Recognition can involve the partner’s terminal carboxylate and nearby side chains; some PDZ domains also recognize internal motifs. This explains how a tandem-domain protein could participate in partner recognition without identifying any particular partner. The PDZ assignment requires family knowledge: duplication alone would establish related regions, not uniquely name their fold. There is no literal GLGF motif in this sequence, so that familiar PDZ motif cannot be claimed as observed evidence here.

The PPPPPP stretch at residues 128–133 illustrates a different kind of sequence feature. A proline-rich segment could serve as a ligand for an SH3-containing partner. It is not itself evidence for the SH3 domain proposed in D. A ligand motif is a short recognition sequence; a domain is a larger folded module that performs recognition. Confusing the two would substitute a potential partner-binding site for a domain-architecture assignment.

A would require a repeated WD40 architecture, not merely an isolated WD pair. SH2 domains can also occur in tandem, so repeat count alone does not distinguish B from C. The broader PDZ-like patterns across separated parts of both modules provide the more specific support for C.

The sequence therefore supports tandem related interaction modules, with PDZ-like domains as a reasonable leading interpretation. It does not determine exact domain boundaries, prove that both modules bind peptides, establish their affinities or identify their physiological partners.

<details>
<summary>Sources and qualifications</summary>

Source identity: the tandem-PDZ NRFL-1 isoform, [UniProt G5EDM4](https://www.uniprot.org/uniprotkb/G5EDM4/entry). Some NRFL-1 splice variants contain only one PDZ domain; this example concerns the supplied two-domain sequence.

Primary reference: [NRFL-1, the C. elegans NHERF orthologue, interacts with amino acid transporter 6 (AAT-6) for age-dependent maintenance of AAT-6 on the membrane](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0043050), especially Figure 1 and the PDZ-interaction Results.

The study supports the selected architecture and examines AAT-6 binding. The specific partner and PDZ2 preference come from the interaction Results, not from recognizing two sequence repeats. Domain boundaries, binding preferences and affinities remain separate from the anonymous sequence-based assignment.

</details>

---

# 8. Judging a chromophore-binding hypothesis

## Question

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

## Answer

**Answer: D.**

A retinal-binding microbial opsin is a plausible leading hypothesis. The reasoning combines the protein’s overall membrane-rich architecture with the position and chemistry of a candidate attachment lysine; neither feature is sufficient alone.

Long hydrophobic regions occur throughout this compact 239-residue sequence, rather than being confined to one terminal anchor. Illustrative windows occur at residues 1–26, 36–64, 73–94, 98–121, 124–145, 166–190 and 194–219. Their distribution is consistent with a compact bundle of membrane-spanning helices, including the seven-helix architecture characteristic of microbial opsins. These are approximate sequence windows, not experimentally established helix boundaries or a demonstrated count of seven helices.

The late hydrophobic region, VALIVYLDLVTKVGFGFIALDAAATL at residues 194–219, contains Lys205. In a retinal-binding opsin, retinal’s aldehyde can form an imine, or Schiff base, with the lysine side chain’s amino group. The corresponding attachment lysine in microbial opsins lies in the final membrane helix. Lys205 therefore has compatible chemistry and a qualitatively appropriate position within the proposed membrane architecture. Its relevance comes from that context, not simply from finding a lysine somewhere in the protein.

The soluble LOV-domain protein proposed in B would bind FMN within a folded pocket in a largely soluble domain. The many long hydrophobic regions here fit a membrane bundle substantially better than that overall architecture. Likewise, protein length alone would not justify the GFP-like soluble beta-barrel interpretation in C. The distribution of hydrophobicity is more discriminating than size.

A specifically requires a cysteine for the stated bilin linkage, but this sequence has no cysteine. Its compact membrane-rich architecture also differs from the proposed large photosensory domain.

The strongest conclusion from direct inspection is that this is likely a multipass membrane protein. The retinal/opsin interpretation is a more specific hypothesis that draws on family knowledge. Other membrane proteins can also contain several helices and lysines, so these observations do not uniquely prove opsin identity. They also do not demonstrate retinal occupancy, a Schiff-base linkage specifically at Lys205, an absorption wavelength or sensory rather than transport function. Those claims go beyond the anonymous sequence evidence.

<details>
<summary>Sources and qualifications</summary>

Source identity: microbial sensory rhodopsin II, [UniProt P42196](https://www.uniprot.org/uniprotkb/P42196/entry). Experimental structures establish retinal binding and the Lys205 linkage. These are structural findings, rather than direct observations available from the anonymous sequence.

Primary references: [Crystal structure of sensory rhodopsin II at 2.4 angstroms: insights into color tuning and transducer interaction](https://pubmed.ncbi.nlm.nih.gov/11452084/), [experimental structure PDB 1JGJ](https://www.rcsb.org/structure/1JGJ), and [Molecular basis of transmembrane signalling by sensory rhodopsin II-transducer complex](https://pubmed.ncbi.nlm.nih.gov/12368857/).

The deposition maps the protein to P42196 and lists retinal; the structure study supports attachment at Lys205. The protein is a microbial sensory rhodopsin, rather than an animal G-protein-coupled receptor. Neither the sensory function nor the chromophore’s spectral properties follow directly from the hydrophobic architecture and candidate lysine alone.

</details>

---

# 9. Does a label reveal or change protein organization?

## Question

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

## Answer

**Answer: A.**

Option A tests whether the organization pattern depends on functional valency at comparable measured initial target engagement, using a calibrated organization readout. This addresses both the probe's capacity to connect targets and differences in how many targets are engaged or detected. A tetramer with four active sites can connect separate biotinylated targets; an A1D3 tetramer has only one functional site and cannot make that same connection through multiple biotin-binding sites. Similar soluble-biotin affinity does not remove this difference in functional valency. Nor does it establish equal cellular target engagement or equal fluorophores per detected complex. The affinity measurements also did not use exactly the same preparations as the cellular comparison.

An intermediate-valency preparation could strengthen the comparison: an intermediate tendency to form clusters would support a valency-dependent contribution. A difference between multivalent and monovalent labels at comparable engagement would be consistent with probe-mediated crosslinking. If the apparent difference instead largely disappeared after accounting for engagement or detection, the original images would give weaker support for redistribution. Neither result would isolate every difference between the preparations, and matching initial engagement would not guarantee identical engagement later.

Establishing native organization requires more than calibrating detection. The observed labeling patterns justify concern about probe-induced perturbation, but neither pattern is established as the native state. An independent organization readout evaluated for perturbation would provide additional evidence. If it also showed diffuse organization, the A1D3 image would gain support as a less perturbing representation. If it instead revealed clusters or a different organization, the diffuse A1D3 image could be missing a feature of the target distribution. Agreement is useful only to the extent that the independent method has different, understood biases; agreement between two perturbing methods is not sufficient validation.

A concentration-dependence comparison is also informative, especially when asking whether clustering occurs only in a particular labeling regime. Its interpretation must distinguish altered opportunities for crosslinking from altered target coverage and detection. Lowering probe concentration is therefore a meaningful alternative to examine, but concentration alone does not establish comparable engagement or a native-state baseline.

B chooses concentrations from soluble-biotin affinity estimates and relies on the original labeling images; this does not establish comparable cellular engagement or calibrated detection. C matches supplied binding capacity and fluorescence, which can agree despite different target coverage. D supplies unequal nominal numbers of functional binding sites at equal tetramer concentrations and does not establish comparable target engagement. These comparisons can inform other questions, but A controls the stated alternatives most directly.

<details>
<summary>Sources and qualifications</summary>

[Howarth et al., A monovalent streptavidin with a single femtomolar biotin binding site](https://doi.org/10.1038/nmeth861) (2006): Table 1 and Figure 3 for stoichiometry and soluble binding; Figure 4 and accompanying Results for neuronal labeling and clustering.

Source qualification: [UniProt P22629](https://www.uniprot.org/uniprotkb/P22629/entry) is the native 183-residue streptavidin precursor from Streptomyces avidinii. It identifies the source protein, not the exact mature, engineered or tagged assayed subunit, and does not specify the A1D3 preparation.

The three observations are paraphrases of the published comparisons. The collaborator's claim and proposed comparisons are hypothetical teaching material. The possible outcomes discussed in the answer are conditional interpretations, not additional results reported by the paper. Neither a native-state measurement nor the outcome of an engagement-matched comparison is supplied.

</details>

---

# 10. What does exclusion from a proximity-labeling list mean?

## Question

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

## Answer

**Answer: B.**

P passes the no-added-biotin comparison but fails the contact-versus-cytosol enrichment filter. Under the stated resource constraint, and without independent evidence giving P higher priority, these results support prioritizing proteins that passed both filters and provisionally deferring P. This is a practical ranking based on the assay's selection criterion, not a conclusion that P is absent from contacts or biologically unimportant. The filtered list is not a complete inventory of proteins relevant to the biological process.

The two comparisons answer different questions. P's recovery exceeds the no-added-biotin background, so it passes that first selection step. It nevertheless fails the required enrichment relative to the cytosolic reference. The second result establishes insufficient relative enrichment under the sampled conditions. It does not identify the reason: the ratio depends on recovery in both the contact-targeted condition and the reference condition.

One compatible explanation is that P has a substantial cytosolic pool as well as a genuine contact-associated pool. Recovery from the cytosolic population can reduce relative enrichment even if some P is present at contacts. Another is that P has little or no contact association in this setting. Differences in accessibility to labeling or in the labeling history could also contribute. These remain possible explanations; no protein-specific evidence supplied here selects among them. Comparable overall labeling does not provide a separate calibration of P's recovery, kinetics or occupancy.

Independent localization evidence would address whether P is found at contacts, in the cytosol, or in more than one compartment under relevant conditions. Evidence about function would address a separate question: whether P contributes to the process the project aims to understand. A small contact-associated pool could be functionally important, while a readily detected contact-associated protein need not be a key functional factor. Neither localization nor proximity labeling alone establishes direct molecular binding or functional necessity.

P would merit reconsideration if independent evidence linked it to the relevant contact-associated process, supported a meaningful contact-localized pool, or suggested that this filtering scheme systematically misses the kind of protein the project seeks. A different project objective could also justify following up P despite its failed filter. In the absence of such evidence, provisional deferral reflects weaker support from this assay's enrichment criterion, not a demonstrated lack of biological relevance.

A promotes background-control passage into localization evidence. C assumes an unavailable occupancy calibration. D treats one possible explanation as an established result and then infers function. B avoids those unsupported biological conclusions while retaining a practical basis for prioritization.

<details>
<summary>Sources and qualifications</summary>

[Cho et al., Split-TurboID enables contact-dependent proximity labeling in cells](https://doi.org/10.1073/pnas.1919528117) (2020): Figure 3F and Results before Figure 4 for unequal-duration bulk matching; Figure 4 and Methods, Generation of ER–Mitochondria Proteome Lists, for sequential filtering; Results before Validation of ER–Mitochondria Contact Orphans for loss of dual-localized proteins.

Source qualification: [UniProt P06709](https://www.uniprot.org/uniprotkb/P06709/entry) is native Escherichia coli BirA, the ancestral reference backbone. It is not the complete evolved split-TurboID fragments or their tags, localization elements and dimerization domains.

The assay description is source-derived. P and the prioritization scenario are hypothetical. The paper does not supply P's identity, localization, function, labeling kinetics or a quantitative occupancy calibration. Relative enrichment remains useful for its filtering role; the possible explanations discussed here are not measured outcomes for P.

</details>

---

[Provenance and review scope](PROVENANCE.md).
