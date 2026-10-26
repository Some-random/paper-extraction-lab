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

Write a defensible replacement conclusion. Explain what comparison is reproduced across the two tested conditions, whether one fold-improvement number captures the result, and whether the proposed reaction-rate prediction follows.

## Answer

I would replace the single-number claim with: “APEX2 reaches its rate maximum at a higher peroxide concentration than APEX in both tested guaiacol conditions, but the magnitude of that difference depends on the assay condition. These observations do not establish which enzyme has the greater reaction rate at an untested guaiacol concentration.”

The repeated comparison is straightforward. At 1.4 mM guaiacol, the peroxide concentrations at the maxima are approximately 2.5 mM for APEX2 and 0.1 mM for APEX, a 25-fold difference. At 0.5 mM guaiacol, they are approximately 0.5 mM and 0.05 mM, a 10-fold difference. Thus, the direction is reproduced, while one fold-improvement factor would conceal a substantial change in magnitude. The location of the maximum also changes for each enzyme when guaiacol changes. It is a property of the measured response under those conditions, rather than an intrinsic, condition-independent inhibition constant.

There is a second distinction between where the maximum occurs and how high it is. The table describes the peroxide concentration at a turning point on a rate curve. It supplies no absolute rates or curve shapes. An enzyme can reach that turning point at a higher concentration without having the higher maximum rate or the higher rate at a particular peroxide concentration. The table therefore cannot rank rates even throughout the tested conditions, much less at an untested guaiacol concentration. It supports a repeated, condition-dependent shift in the response, rather than the colleague's proposed general prediction of catalytic performance.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


Primary source: [Lam et al., Directed evolution of APEX2 for electron microscopy and proximity labeling](https://doi.org/10.1038/nmeth.3179), Figure 2e and the accompanying purified-protein kinetics Results. The existing source review records the corrected Figure 2e axis labels and the December 10, 2014 correction.

Source qualification: [UniProt Q43758](https://www.uniprot.org/uniprotkb/Q43758/entry) is wild-type soybean (Glycine max) ascorbate peroxidase. It was the coordinate reference in the earlier APEX2 example, not the complete engineered assay construct. Pea APX has a different accession, P48534. The unused reference sequence is not part of the current student question.

Supplied evidence: the two guaiacol conditions and approximate concentrations at the reported rate maxima. No absolute reaction rates, new fitted parameters, or measurements at an additional condition are supplied. The colleague's proposed summary and transfer claim are hypothetical assessment framing, not statements attributed to the paper.

Inference being assessed: whether a repeated comparative pattern supports a universal factor or a prediction of a different measured quantity. The example does not ask for a molecular explanation of the APEX2 change, a new variant, or an assay procedure. Sequence and variant-coordinate material from the earlier question was removed because it was unnecessary to this inference.

This is an assistant source-aware revision of the existing example, not a fresh teacher-generated solution. Expert human validation and student-learning benefit have not been established.

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

Should the analysis use that interpretation? Explain how the observations fit together, what the APEX–mAPX comparison adds, and which conclusions about reporter performance remain supported.

## Answer

I would not interpret cellular DAB intensity as a calibrated ranking of how much connexin43 fusion reaches gap junctions. The argument combines measurements of different properties and assumes that the purified assay has removed sources of variation that it did not measure.

First, the similar purified guaiacol activities support a comparison under that assay's conditions. They do not establish equal catalytic output with DAB in cells. Guaiacol and DAB are different substrates, and cellular staining depends on more than the catalytic competence demonstrated by a purified preparation. Even an equal-molecule comparison with guaiacol would not establish equal DAB activity per molecule in the cellular setting. The analyst therefore cannot use the purified result as a conversion factor from staining intensity to protein amount.

Second, the connexin43 comparison directly concerns fusion trafficking: mAPX fusions reached gap junctions more effectively than wild-type APX fusions. Reduced self-association is a plausible explanation for less interference with the fusion partner, although these observations do not identify every contribution to trafficking. This remains a supported improvement in the localization comparison. The weaker mAPX staining was observed in a separate cytosolic comparison, so it does not show that less mAPX–connexin43 reached gap junctions. The two findings can coexist because delivery of a fusion and catalytic staining output are different properties.

Third, the heme-supplementation result helps explain why staining cannot simply count protein molecules. APX requires heme for catalytic activity. More staining after heme supply is consistent with an increase in the available active, heme-containing enzyme population. It does not directly measure total protein abundance, fusion delivery, or equilibrium heme affinity. Cellular availability and incorporation of heme, folding, stability, and substrate-dependent performance can all influence the readout. The observation supports an active-enzyme contribution without establishing weaker heme affinity as the unique cause of mAPX's lower signal.

Finally, APEX produced stronger cellular DAB staining than mAPX while retaining similar predominantly monomeric behavior. This shows that staining performance can differ without a further reported difference in that oligomeric property. It does not tell us whether the signal difference arose from catalytic performance, the active-enzyme fraction, protein amount, or a combination. In particular, similar monomeric behavior is not a normalization for cellular DAB activity.

The useful conclusion is that reporter fidelity and signal production must be interpreted separately. The supplied evidence supports better connexin43 trafficking with mAPX than with wild-type APX, and stronger cellular DAB staining with APEX than with mAPX in their respective comparisons. Those results matter for reporter performance, but they do not form a single three-way ranking of junction-localized fusion abundance. DAB remains an informative catalytic endpoint; it has not been shown here to be an interchangeable measure of the quantity the analyst wants to rank.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


Primary source: [Martell et al., Engineered ascorbate peroxidase as a genetically encoded reporter for electron microscopy](https://doi.org/10.1038/nbt.2375), Figure 1b–e and accompanying Results on self-association and connexin43 trafficking, and Figure 2b–d and accompanying Results on purified activity, cellular DAB staining, and heme supplementation.

Supplied evidence: the four published comparisons above. The proposed DAB-based ranking of junction delivery is hypothetical assessment framing. The source study did not establish that cross-assay calibration. The cytosolic and connexin43-fusion observations concern different comparisons and must not be merged into one measurement.

Inference being assessed: whether one assay can calibrate a different cellular endpoint, and how apparently conflicting results can reflect different biological properties. Heme-dependent active-enzyme availability is a compatible explanation, not a uniquely identified microscopic cause. Predominantly monomeric behavior is qualified rather than asserted at every concentration.

This is an assistant source-aware revision of the existing example, not a fresh teacher-generated solution. No new measurements, mutations, or procedures are proposed. Expert human validation and student-learning benefit have not been established.

</details>

---

# 3. Choosing a labeling tool for the measurement objective

## Question

The TurboID study reported a candidate sequence change that appeared beneficial for labeling activity and was included, with other changes, in TurboID. It was also examined in the miniTurbo background but was not retained there because labeling increased when added biotin was omitted. In the broader comparison, miniTurbo generally produced less labeling before biotin addition, whereas TurboID generally produced greater labeling yield.

These enzymes produce covalent labels. Omitting added biotin does not remove biotin already present in cells. The reported candidate-change comparison is qualitative; it supplies neither an isolated binding constant nor a protein-by-protein history of when labels formed.

Consider a project whose purpose is to associate recovered proteins with a defined interval beginning at biotin addition. It also needs enough recovered material for analysis. There are no project-specific measurements of background labeling or recovery yet.

Compare TurboID and miniTurbo as initial candidates for this project. Make a provisional choice and explain the tradeoff. What missing information would most affect that choice? Explain whether the reported candidate change counts as an improvement for this objective, and how your recommendation could change for a project that prioritizes cumulative yield instead.

## Answer

I would provisionally favor miniTurbo for a project that makes the defined start time its main interpretive requirement, provided it can recover enough material. The reason is the reported lower pre-addition labeling, rather than a claim that miniTurbo is generally the better enzyme. TurboID's greater yield addresses an equally real constraint, so the decision cannot be settled from timing considerations alone.

The timing problem concerns the history represented by the recovered labels. Omitting added biotin does not remove biotin already in cells, and these enzymes produce covalent marks. Labeling before the intended start can therefore contribute to the material recovered later. A stronger accumulated signal need not mean that more of the signal represents the interval of interest. Conversely, a preparation with lower pre-start labeling is not useful to this project if its recovery is too low to support the analysis. The appropriate comparison is between temporal interpretability and sufficient recovery, rather than between low and high signal in isolation.

The missing information most likely to reverse my choice is how those two constraints balance in the project's actual context: the extent of pre-addition labeling, the recovered material associated with the intended interval, and whether the amount and reproducibility of that recovery meet the analytical need. If miniTurbo gives adequate recovery with substantially less pre-start contribution, its reported advantage fits the objective. If recovery is inadequate, TurboID could be the more useful candidate, but its greater yield would not by itself restore a sharply defined labeling interval. The timing compromise would remain part of interpreting the result. The paper's broad comparison does not establish any of these project-specific outcomes.

The candidate change illustrates the same distinction at the variant level. In the tested miniTurbo background, its increased omit-added-biotin signal counts against temporal control, even if some aspect of labeling activity improved. Its inclusion with other changes in TurboID does not establish that its isolated effect is identical in the two backgrounds. The qualitative observations also do not identify a change in affinity, a catalytic constant, or the particular molecular step responsible.

For a project that prioritizes cumulative yield over a sharply defined start time, I could instead provisionally favor TurboID. The greater yield reported in the broader comparison would then serve the stated objective more directly, and activity before biotin addition might carry less penalty. It would still matter if that activity made the recovered material unsuitable for the biological interpretation. Thus, changing the objective can change the recommendation without changing any of the published observations; the decision depends on what the measurement must mean and whether it produces enough usable material.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


Primary source: [Branon et al., Efficient proximity labeling in living cells and organisms with TurboID](https://doi.org/10.1038/nbt.4201), Methods under “Yeast display directed evolution” for the reported candidate-change decision, Figure 2a–b and Discussion for the yield/background comparison, and Supplementary Note 2 for labeling chemistry and qualified mechanistic interpretations.

Supplied evidence: the published qualitative activity and omit-added-biotin observations, the broader reported tool comparison, and the covalent nature of labeling. The proposed project and its alternative objectives are hypothetical assessment framing. No new quantitative effect size or project-specific performance is supplied or inferred.

Inference being assessed: how a measurement objective and a recovery constraint change the value of an observed property, and which missing evidence could reverse a provisional recommendation. The example does not identify an affinity change, predict a new variant, or prescribe a labeling procedure. The candidate's identity and the unused reference sequence from the earlier question were removed because they are unnecessary to the decision.

This is an assistant source-aware revision of the existing example, not a fresh teacher-generated solution. Expert human validation and student-learning benefit have not been established.

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

What cofactor and protein-family assignment does this sequence most strongly support? Identify the sequence evidence that matters, explain why it is stronger than one plausible alternative cofactor interpretation, and state what the sequence cannot establish about the protein’s activity.

## Answer

The strongest assignment is a heme-containing cytochrome P450. The evidence is a combination of sequence features in the appropriate order, rather than the presence of a metal-binding amino acid by itself.

The most direct clue is FGHGHHVCLG at residues 338–347. It matches the P450-associated pattern FxxGxxxCxG, where x can be any residue. The cysteine in this pattern is Cys345. In P450 enzymes, the corresponding cysteine supplies a thiolate sulfur that coordinates the heme iron. This makes Cys345 a plausible axial ligand and connects the sequence pattern to a specific cofactor-binding chemistry. Coordination of heme iron should not be confused with a covalent bond attaching the heme group to the polypeptide.

Two other regions strengthen the family assignment. ECLR at residues 274–277 matches the characteristic P450 E-x-x-R pattern. This supports the P450 core architecture; it is not itself a direct heme-binding site. AGHETT at residues 235–240 contains an acidic residue and adjacent threonines consistent with the I-helix region involved in oxygen activation in many P450s. Calling it an I helix is a family-based structural inference, not an observed secondary structure. These regions precede the cysteine-containing signature in the expected sequence order, so they provide mutually consistent support.

An iron–sulfur protein is a reasonable alternative to consider when a sequence contains cysteines. However, cysteine presence alone does not distinguish an iron–sulfur ligand from a heme ligand or an unrelated cysteine. Here, the specific cysteine-containing signature together with the supporting P450 patterns explains the evidence better than a generic iron–sulfur assignment. Flavin-binding families are also diverse, so the argument should not be that one missing universal FAD or FMN motif rules them out.

The supported conclusion is a strong P450/heme hypothesis. The sequence does not demonstrate that the protein actually contains heme, identify its substrate or establish its reaction specificity and catalytic activity. Those are separate claims from recognizing a cofactor-binding family.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


The existing source review identifies the sequence as UniProt P53554. The primary structure supports heme and Cys345 coordination; the anonymous sequence does not independently reveal the biotin-biosynthesis substrate.

Primary reference: [Structural insights from a P450 carrier protein complex reveal how specificity is achieved in the P450BioI ACP complex](https://pmc.ncbi.nlm.nih.gov/articles/PMC2572933/), especially Active Site Architecture.

This is a source-aware assistant revision of the existing source-checked example into an open-response task. The original full sequence is unchanged. No new experiment, measurement or variant is proposed. The question uses only the anonymous sequence and standard family knowledge; the source identity and experimental findings remain in these review notes. No expert human validation or measured training benefit is claimed.

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

What ion-binding architecture is supported by the likely soluble region of this sequence? Cite the relevant segments and explain why their arrangement is more informative than acidic composition alone. Contrast your interpretation with a nonspecific acidic region, and distinguish the prediction from properties that require experimental evidence.

## Answer

The likely soluble region supports an EF-hand calcium-binding architecture, with two particularly convincing candidate loops. They are DRDGNGFISKQE at residues 46–57 and DMDGDGQVDFEE at residues 82–93.

An EF hand contains a calcium-binding loop of about 12 residues between two helices. The informative feature here is the arrangement of potential ligands within each loop. In DRDGNGFISKQE, positions 1, 3 and 5 are Asp, Asp and Asn. In DMDGDGQVDFEE, those positions are all Asp. Both loops have glycine at position 6 and glutamate at position 12. Asp, Asn and Glu provide oxygen-containing groups compatible with calcium coordination. Glycine can accommodate the tight loop geometry, while the terminal glutamate commonly contributes its carboxylate to calcium binding. The repeated positional pattern is therefore chemically and structurally coherent.

This is stronger evidence than high acidic content alone. A nonspecific acidic region could interact with positively charged ions, but acidity does not specify a calcium-binding fold. Two separate segments with the same ligand-compatible positions, loop length and conserved glycine are more suggestive of repeated binding modules than an arbitrary Asp/Glu-rich stretch would be. The interpretation depends on their organization, not simply on counting negative charges.

The candidate loops lie well upstream of the hydrophobic near-terminal sequence LICAFAIAFIISVMLIAA. That distribution is consistent with a soluble binding region attached to a membrane through a C-terminal anchor. It helps place the proposed ion-binding loops outside the hydrophobic segment, but does not establish membrane orientation or the protein’s cellular destination.

The sequence supports candidate EF hands; it does not directly demonstrate their three-dimensional fold or prove that both bind ions under physiological conditions. Nor does it measure calcium affinity, calcium-versus-magnesium selectivity, occupancy or a calcium-dependent conformational change. In particular, recognizing these two loops does not justify claiming four functional calcium-binding sites. The architecture prediction and the biochemical properties of its sites require different evidence.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


The existing review identifies the sequence as human CaBP7, UniProt Q86V35. The primary abstract and experimental deposition support two high-affinity N-terminal calcium sites. The NMR construct omits the full canonical C-terminal region. Those experimental facts are withheld from the student input; they do not make affinity or selectivity readable from the anonymous sequence.

Primary references: [Solution NMR structure of the Ca2+-bound N-terminal domain of CaBP7: a regulator of Golgi trafficking](https://pubmed.ncbi.nlm.nih.gov/22989873/) and [experimental structure PDB 2LV7](https://www.rcsb.org/structure/2LV7). The prior review used the primary abstract and deposition; it was not a new full-text review.

This is a source-aware assistant revision of the existing source-checked example into an open-response task. The original full sequence is unchanged. No new experiment, measurement or variant is proposed. The question uses only the anonymous sequence and standard family knowledge; the source identity and experimental findings remain in these review notes. No expert human validation or measured training benefit is claimed.

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

Infer this protein’s membrane-association architecture from the sequence. Identify the strongest evidence for an integral anchor rather than peripheral association, and explain how confidently you can assign the orientation of the large upstream region. What cellular information remains unresolved?

## Answer

The sequence strongly supports a protein with one membrane anchor near its C terminus and a much larger region outside the bilayer. Its most conspicuous feature is ILLVILGIIVVIAILTAIAFFV at residues 193–214: a continuous 22-residue hydrophobic stretch followed by only KGH.

That combination of length, composition and position is appropriate for a membrane-spanning alpha helix. There are no charged residues within this stretch, whereas the surrounding protein contains many charged and polar residues. Placing such a long hydrophobic segment in the lipid bilayer provides a more coherent interpretation than treating the entire protein as a soluble domain that associates only peripherally with a membrane. Peripheral association can occur through interactions with lipids or other proteins, but does not by itself explain this pronounced hydrophobic tail.

The upstream region does not contain several comparable hydrophobic stretches. The sequence therefore supports one anchor rather than a multipass membrane bundle. The anchor’s near-terminal position and very short following tail are also consistent with a tail-anchored architecture. This is an architectural assignment, not identification of the cellular machinery or route that inserts it.

Orientation is a separate, less certain inference. The RRIIQNR segment at residues 186–192 places several basic residues immediately before the candidate anchor. This agrees with the positive-inside tendency, in which positively charged flanks often occur on the cytosolic side of membrane-spanning helices. It therefore supports a cytosolic location for the large upstream region. However, a tendency is not a direct observation, and saying that a region lies outside the bilayer does not by itself identify which membrane side it occupies.

Residues 193–214 describe a hydrophobic-composition window, not a measured helix boundary. A structural boundary could differ slightly without changing the overall conclusion. The sequence alone does not establish the exact membrane-spanning endpoints, prove orientation, identify the insertion pathway or distinguish a Golgi, endosomal or other membrane destination. Confidence is strongest for the single C-terminal anchor and weaker for those more specific cellular assignments.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


Source identity: Vti1-rp2/Vti1a, [UniProt O89116](https://www.uniprot.org/uniprotkb/O89116/entry). The primary abstract supports a C-terminal anchor, cytoplasmic region and integral membrane behavior.

Two boundary descriptions are legitimate and should not be conflated:

| Quantity | Residues | Interpretation |
|---|---|---|
| Composition-based hydrophobic call in the reference answer | 193–214 | A continuous 22-residue hydrophobic stretch, with KGH following it. |
| UniProt annotated helical anchor | 193–213 | Annotated helix; V214 is assigned to the following vesicular region. |
| UniProt topological domains | 1–192 cytoplasmic; 214–217 vesicular | Annotation-based orientation and residue partition. |

The frozen UniProt record assigns all three topology features evidence code ECO:0000255 (sequence analysis). The RRIIQNR flank at 186–192 and the proposed cytosolic upstream region agree with that annotation. This is a source-consistency check, not independent experimental confirmation of a residue-exact boundary or proof that the current answer was produced blind. An extramembrane assignment alone does not specify the cytoplasmic side. The current reference answer remains a source-aware revision; its confidence must reflect the anonymous student input.

[Frozen UniProt record](artifacts/example-06/frozen_uniprot_record.json) · [Final-review disposition](final_review_v1.json). The historical coordinate-edit record is preserved; this clarification supersedes treating the one-residue composition/annotation difference as a sequence error.

Primary reference: [A 29-kilodalton Golgi soluble N-ethylmaleimide-sensitive factor attachment protein receptor (Vti1-rp2) implicated in protein trafficking in the secretory pathway](https://pubmed.ncbi.nlm.nih.gov/9705316/). The prior review used the primary abstract retrieved in search results; direct page opening encountered a browser challenge.

This is a source-aware assistant revision of the existing source-checked example into an open-response task. The original full sequence is unchanged. No new experiment, measurement or variant is proposed. The question uses only the anonymous sequence and standard family knowledge; the source identity and experimental findings remain in these review notes. No expert human validation or measured training benefit is claimed.

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

What interaction-domain architecture is a reasonable hypothesis for this sequence? Use repeated sequence regions to support your assessment. Explain whether the proline-rich stretch identifies a folded interaction domain or could instead be a partner-binding motif, and state which conclusions about binding partners remain unsupported.

## Answer

A reasonable hypothesis is a tandem arrangement of two PDZ-like interaction modules. The clearest sequence evidence is extended similarity between two regions of the N-terminal portion, rather than one short conserved word or a low-complexity repeat.

For example, EYGYNLHAEKGRGQFVGTVD at residues 24–43 resembles EFGFNLHAERGRGHFIGTVD at residues 154–173. Both contain related aromatic/glycine-rich portions followed by a similar GTVD-containing segment. The similarity continues farther along the candidate modules: IFAVNGHSIIGENHKKVVERIK at residues 59–80 resembles IVGVNGQLIYPTTGHKEVVALIK at residues 189–211. Agreement across separated parts of each region is more informative than matching a single short motif. It supports two related modules with internal sequence complexity.

The broader pattern is compatible with PDZ domains, compact interaction modules whose folded binding grooves often recognize short peptides at the C termini of partner proteins. Recognition can involve the partner’s terminal carboxylate and nearby side chains; some PDZ domains also recognize internal motifs. This explains how a tandem-domain protein could participate in partner recognition without identifying any particular partner. The PDZ assignment requires family knowledge: duplication alone would establish related regions, not uniquely name their fold. There is no literal GLGF motif in this sequence, so that familiar PDZ motif cannot be claimed as observed evidence here.

The PPPPPP stretch at residues 128–133 illustrates a different kind of sequence feature. A proline-rich segment could serve as a ligand for an SH3-containing partner. It is not itself evidence for an SH3 domain in this protein. A ligand motif is a short recognition sequence; a domain is a larger folded module that performs recognition. Confusing the two would substitute a potential partner-binding site for a domain-architecture assignment.

The sequence therefore supports tandem related interaction modules, with PDZ-like domains as a reasonable leading interpretation. It does not determine exact domain boundaries, prove that both modules bind peptides, establish their affinities or identify their physiological partners. A more cautious tandem-module conclusion is appropriate if family recognition remains uncertain.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


The existing review identifies the selected sequence as the tandem-PDZ NRFL-1 isoform, UniProt G5EDM4. Some splice variants have one PDZ domain. The primary study supports the selected two-domain architecture and examines AAT-6 binding; the specific partner and PDZ2 preference are not supplied in the student input. The prior review preferred the Results text over an inconsistent duplicated phrase in the Figure 2 caption.

Primary reference: [NRFL-1, the C. elegans NHERF orthologue, interacts with amino acid transporter 6 (AAT-6) for age-dependent maintenance of AAT-6 on the membrane](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0043050), especially Figure 1 and the PDZ-interaction Results.

This is a source-aware assistant revision of the existing source-checked example into an open-response task. The original full sequence is unchanged. No new experiment, measurement or variant is proposed. The question uses only the anonymous sequence and standard family knowledge; the source identity and experimental findings remain in these review notes. No expert human validation or measured training benefit is claimed.

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

What chromophore-binding mechanism would you prioritize as a hypothesis for this sequence, and why? Identify evidence from the overall architecture and a candidate attachment residue. Compare that hypothesis with a soluble chromophore-binding protein, and distinguish compatibility from proof of chromophore attachment.

## Answer

A retinal-binding microbial opsin is a plausible leading hypothesis. The reasoning combines the protein’s overall membrane-rich architecture with the position and chemistry of a candidate attachment lysine; neither feature is sufficient alone.

Long hydrophobic regions occur throughout this compact 239-residue sequence, rather than being confined to one terminal anchor. Illustrative windows occur at residues 1–26, 36–64, 73–94, 98–121, 124–145, 166–190 and 194–219. Their distribution is consistent with a compact bundle of membrane-spanning helices, including the seven-helix architecture characteristic of microbial opsins. These are approximate sequence windows, not experimentally established helix boundaries or a demonstrated count of seven helices.

The late hydrophobic region, VALIVYLDLVTKVGFGFIALDAAATL at residues 194–219, contains Lys205. In a retinal-binding opsin, retinal’s aldehyde can form an imine, or Schiff base, with the lysine side chain’s amino group. The corresponding attachment lysine in microbial opsins lies in the final membrane helix. Lys205 therefore has compatible chemistry and a qualitatively appropriate position within the proposed membrane architecture. Its relevance comes from that context, not simply from finding a lysine somewhere in the protein.

A soluble chromophore-binding protein is a meaningful alternative. A soluble LOV-domain protein can bind FMN, for example, but its folded pocket would need to accommodate the chromophore within a largely soluble domain. The many long hydrophobic regions here fit a membrane bundle substantially better than that overall architecture. Likewise, protein length alone would not justify a GFP-like soluble beta-barrel interpretation. The distribution of hydrophobicity is more discriminating than size.

The strongest conclusion from direct inspection is that this is likely a multipass membrane protein. The retinal/opsin interpretation is a more specific hypothesis that draws on family knowledge. Other membrane proteins can also contain several helices and lysines, so these observations do not uniquely prove opsin identity. They also do not demonstrate retinal occupancy, a Schiff-base linkage specifically at Lys205, an absorption wavelength or sensory rather than transport function. Those claims go beyond the anonymous sequence evidence.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


The existing review identifies the sequence as sensory rhodopsin II, UniProt P42196. Experimental structures establish retinal binding and the Lys205 linkage; the student must not treat those withheld findings as observations available from sequence alone. This microbial protein should not be labeled an animal G-protein-coupled receptor.

Primary references: [Crystal structure of sensory rhodopsin II at 2.4 angstroms: insights into color tuning and transducer interaction](https://pubmed.ncbi.nlm.nih.gov/11452084/), [experimental structure PDB 1JGJ](https://www.rcsb.org/structure/1JGJ), and [Molecular basis of transmembrane signalling by sensory rhodopsin II-transducer complex](https://pubmed.ncbi.nlm.nih.gov/12368857/). The prior review used primary abstracts, an indexed figure description and the experimental deposition; full-text opening encountered a browser challenge.

This is a source-aware assistant revision of the existing source-checked example into an open-response task. The original full sequence is unchanged. No new experiment, measurement or variant is proposed. The question uses only the anonymous sequence and standard family knowledge; the source identity and experimental findings remain in these review notes. No expert human validation or measured training benefit is claimed.

</details>

---

# 9. Does a label reveal or change protein organization?

## Question

Published observations from a study of biotinylated neuroligin-1 on cultured neurons:

- Wild-type streptavidin has four functional biotin-binding sites. A1D3 is still a tetramer, but only one of its sites binds biotin.
- Tagged four-site and one-site preparations had similar soluble-biotin affinities. The cellular comparison used wild-type streptavidin and A1D3, so the affinity and cell experiments were not comparisons of exactly the same preparations.
- Both cellular labels initially appeared diffuse. Later, wild-type streptavidin labeling showed pronounced clustering while A1D3 labeling remained predominantly diffuse.

A collaborator concludes that the diffuse A1D3 image reveals native neuroligin organization and that similar soluble-biotin affinity makes further comparison unnecessary.

**Question:** Assess that conclusion. Choose two high-level comparisons that would most help separate probe-induced redistribution from differences in target engagement or detection. For each, explain which competing explanations it addresses and what possible result would change your interpretation. You may consider functional valency, concentration dependence, direct target engagement, or an independent organization readout; justify your choices rather than listing every possibility. Explain what would still be needed to call either pattern native. No experimental protocol is requested.

## Answer

The observations justify concern that the probe affects the observed pattern, but they do not establish which pattern represents native neuroligin organization. Similar affinity for soluble biotin controls only part of the problem. A tetramer with four active sites can connect separate biotinylated targets; an A1D3 tetramer has only one functional site and cannot make that same connection through multiple biotin-binding sites. This difference in functional valency remains even though both preparations are tetramers. Cellular target engagement and fluorophores per detected complex can also affect the image, and the affinity measurements did not use exactly the same preparations as the cellular comparison.

My first comparison would ask whether the organization pattern depends on functional valency after accounting for initial target engagement and detection. An intermediate-valency preparation could be informative here: a corresponding intermediate tendency to form clusters would support a valency-dependent contribution. A difference between multivalent and monovalent labels at comparable engagement would be consistent with probe-mediated crosslinking. If the apparent difference instead largely disappeared after accounting for engagement or detection, the original images would give weaker support for redistribution. Neither pattern alone would isolate every difference between the preparations, and matching initial engagement would not guarantee identical engagement later.

My second comparison would ask whether the organization agrees with an independent readout that has been evaluated for perturbation. If that readout also showed diffuse organization, the A1D3 image would gain support as a less perturbing representation. If it instead revealed clusters or a different organization, the diffuse A1D3 image could be missing a feature of the target distribution. Agreement is useful only to the extent that the independent method has different, understood biases; agreement between two perturbing methods is not sufficient validation.

A concentration-dependence comparison is another defensible priority, especially if the concern is whether clustering occurs only in a particular labeling regime. Its interpretation would still need to distinguish altered opportunities for crosslinking from altered target coverage and detection. Thus, the next evidence should resolve a specific competing explanation. The current results motivate testing probe-induced perturbation, while a native-state claim additionally needs a suitable independent baseline and attention to the perturbations introduced by that baseline.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


[Howarth et al., A monovalent streptavidin with a single femtomolar biotin binding site](https://doi.org/10.1038/nmeth861) (2006): Table 1 and Figure 3 for stoichiometry and soluble binding; Figure 4 and accompanying Results for neuronal labeling and clustering.

Source qualification: [UniProt P22629](https://www.uniprot.org/uniprotkb/P22629/entry) is the native 183-residue streptavidin precursor from Streptomyces avidinii. It identifies the source protein, not the exact mature, engineered or tagged assayed subunit, and does not specify the A1D3 preparation.

[Historical independent-check status](artifacts/example-09/independent_check.json). The earlier revision records a check assertion, but its standalone solver response and model metadata were not recovered. No independently verifiable blinded check of the current open-response question is claimed.

The three observations are paraphrases of the published comparisons. The collaborator's claim and follow-up choices are hypothetical teaching material. No new comparison, result, native-state measurement, or experimental procedure is asserted. The answer offers conditional reasoning, not a unique experimental prescription.

This is a source-aware assistant revision responding to review feedback. It replaces the earlier fixed-choice matching question. It is not a fresh teacher-model response or expert human validation, and training benefit has not been measured. Earlier versions remain in Git history and the existing revision artifacts.

</details>

---

# 10. What does exclusion from a proximity-labeling list mean?

## Question

Cho and colleagues compared proteins recovered by contact-targeted split-TurboID at endoplasmic reticulum–mitochondria contacts with proteins recovered using a cytosolic TurboID reference. The preparations used different labeling durations because their activities differed; overall labeling signals were comparable. The comparison measures accumulated labeling under those conditions.

Proteins were first compared with a no-added-biotin control and then filtered for enrichment in contact-targeted labeling relative to the cytosolic reference.

Consider a hypothetical protein P that reproducibly passes the no-added-biotin comparison but fails the contact-versus-cytosol enrichment filter. There are no independent localization measurements, protein-specific labeling kinetics, or functional measurements for P.

A collaborator proposes prioritizing proteins that passed both filters and deferring P because follow-up resources are limited. There is no independent evidence that P is especially important to this project's biological question.

**Question:** Would you follow that priority or make a case for following up P? Distinguish the measured result from at least two possible biological explanations. Explain how independent evidence about localization and about function would answer different questions, and what information would most affect your decision. A justified decision either to defer or to follow up P is acceptable; state its basis and what would change it.

## Answer

With limited resources and no independent reason to prioritize P, I would provisionally follow the collaborator's priority and defer it. That is a practical ranking of candidates, not a conclusion that P is absent from contacts or biologically unimportant. Passing both filters provides the passing candidates with stronger support under this particular selection scheme. It does not make the filtered list a complete inventory of proteins relevant to the biological process.

The two comparisons answer different questions. P's recovery exceeds the no-added-biotin background, so it passes that first selection step. It nevertheless fails the required enrichment relative to the cytosolic reference. The second result establishes insufficient relative enrichment under the sampled conditions. It does not identify the reason: the ratio depends on recovery in both the contact-targeted condition and the reference condition.

One compatible explanation is that P has a substantial cytosolic pool as well as a genuine contact-associated pool. Recovery from the cytosolic population can reduce relative enrichment even if some P is present at contacts. Another is that P has little or no contact association in this setting, making deferral biologically appropriate as well as practical. Differences in accessibility to labeling or in the labeling history could also contribute. These remain possible explanations; no protein-specific evidence supplied here selects among them. Comparable overall labeling does not provide a separate calibration of P's recovery, kinetics or occupancy.

Independent localization evidence would address whether P is found at contacts, in the cytosol, or in more than one compartment under relevant conditions. Evidence about function would address a separate question: whether P contributes to the process the project aims to understand. A small contact-associated pool could be functionally important, while a readily detected contact-associated protein need not be a key functional factor. Neither localization nor proximity labeling alone establishes direct molecular binding or functional necessity.

My priority would change if independent evidence linked P to the relevant contact-associated process, supported a meaningful contact-localized pool, or suggested that this filtering scheme systematically misses the kind of protein the project seeks. A different project objective could also justify following up P despite its failed filter. Without such a reason, deferral is reasonable, provided the record states the actual basis: P currently has weaker support from this assay's enrichment criterion, not a demonstrated lack of biological relevance.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency review. No independently documented blinded solver test or expert human validation is claimed for the current question.


[Cho et al., Split-TurboID enables contact-dependent proximity labeling in cells](https://doi.org/10.1073/pnas.1919528117) (2020): Figure 3F and Results before Figure 4 for unequal-duration bulk matching; Figure 4 and Methods, Generation of ER–Mitochondria Proteome Lists, for sequential filtering; Results before Validation of ER–Mitochondria Contact Orphans for loss of dual-localized proteins.

Source qualification: [UniProt P06709](https://www.uniprot.org/uniprotkb/P06709/entry) is native Escherichia coli BirA, the ancestral reference backbone. It is not the complete evolved split-TurboID fragments or their tags, localization elements and dimerization domains.

[Historical independent-check status](artifacts/example-10/independent_check.json). The earlier revision records a check assertion, but its standalone solver response and model metadata were not recovered. No independently verifiable blinded check of the current open-response question is claimed.

The assay description is source-derived. P, the collaborator's proposal, and the prioritization discussion are hypothetical. The paper does not supply P's identity, localization, function, or labeling kinetics. Exact durations and the reference-set false-discovery criterion were removed because this item requires no valid protein-specific quantitative calculation. Relative enrichment remains useful for its intended filtering role.

This is a source-aware assistant revision responding to review feedback, not a fresh teacher-model response or expert human validation. No new experiments or outcomes are claimed, and training benefit has not been measured. Earlier questions, answers, and generation records remain in Git history and existing artifacts.

</details>
