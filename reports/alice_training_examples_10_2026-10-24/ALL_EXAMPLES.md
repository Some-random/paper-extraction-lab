# AI-created protein reasoning training data — ten revised examples

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

APEX2 reaches its rate maximum at a higher peroxide concentration than APEX in both tested guaiacol conditions. That repeated direction is supported; a condition-independent improvement factor is not. The approximate ratios are 25-fold and 10-fold, and each enzyme's maximum shifts when guaiacol changes. These observations therefore describe a condition-dependent response rather than one intrinsic tolerance number. They also locate a maximum without measuring its height: a later decline does not establish a greater maximum rate, or greater activity at every peroxide concentration. I would report the reproduced conditional comparison and its changing magnitude. The table alone cannot rank reaction rates at the untested guaiacol concentration.

## Assessment rubric

- Identifies the reproduced within-condition comparison and explains why its magnitude is condition dependent.
- Separates the peroxide concentration at a maximum from the reaction rate itself; does not convert the observations into an intrinsic inhibition constant.
- Gives a usable replacement conclusion with a justified limit on transfer. Accept alternative wording or summaries that preserve these distinctions; exact fold calculations are optional.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency and rubric review. No independently documented blinded solver test or expert human validation is claimed for the current question.


Primary source: [Lam et al., Directed evolution of APEX2 for electron microscopy and proximity labeling](https://doi.org/10.1038/nmeth.3179), Figure 2e and the accompanying purified-protein kinetics Results. The existing source review records the corrected Figure 2e axis labels and the December 10, 2014 correction.

Source qualification: [UniProt Q43758](https://www.uniprot.org/uniprotkb/Q43758/entry) is wild-type soybean (Glycine max) ascorbate peroxidase. It was the coordinate reference in the earlier APEX2 example, not the complete engineered assay construct. Pea APX has a different accession, P48534. The unused reference sequence is not part of the current student question.

Supplied evidence: the two guaiacol conditions and approximate concentrations at the reported rate maxima. No absolute reaction rates, new fitted parameters, or measurements at an additional condition are supplied. The colleague's proposed summary and transfer claim are hypothetical assessment framing, not statements attributed to the paper.

Inference being assessed: whether a repeated comparative pattern supports a universal factor or a prediction of a different measured quantity. The example does not ask for a molecular explanation of the APEX2 change, a new variant, or an assay procedure. Sequence and variant-coordinate material from the earlier question was removed because it was unnecessary to this inference.

This is an assistant source-aware revision of the existing example, not a fresh teacher-generated solution. Source agreement and the rubric have not been validated by an expert human or a student-learning study.

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

I would not use DAB intensity as a calibrated ranking of fusion delivery. Similar purified guaiacol activity does not establish equal DAB activity in cells, equal heme loading, or equal amounts of active enzyme. The connexin43 result supports improved trafficking with mAPX; its weaker staining in a separate cytosolic comparison does not contradict that result. Heme supplementation shows that cellular staining can change without establishing a change in fusion delivery or measuring equilibrium heme affinity. Stronger APEX staining despite similar monomeric behavior further separates catalytic signal from self-association. The supported conclusion is that trafficking and staining performance are distinct properties. Their individual comparisons are useful, but they do not provide a common conversion from staining intensity to junction-localized protein amount.

## Assessment rubric

- Rejects or qualifies the proposed calibration for a specific reason involving assay substrate, active-enzyme population, or cellular context.
- Uses the localization and staining comparisons together without treating the separate cytosolic result as a measurement of connexin43 delivery.
- Explains what APEX versus mAPX contributes and preserves the supported trafficking result. Accept alternative compatible causal accounts; do not require a unique explanation for heme response or staining differences.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency and rubric review. No independently documented blinded solver test or expert human validation is claimed for the current question.


Primary source: [Martell et al., Engineered ascorbate peroxidase as a genetically encoded reporter for electron microscopy](https://doi.org/10.1038/nbt.2375), Figure 1b–e and accompanying Results on self-association and connexin43 trafficking, and Figure 2b–d and accompanying Results on purified activity, cellular DAB staining, and heme supplementation.

Supplied evidence: the four published comparisons above. The proposed DAB-based ranking of junction delivery is hypothetical assessment framing. The source study did not establish that cross-assay calibration. The cytosolic and connexin43-fusion observations concern different comparisons and must not be merged into one measurement.

Inference being assessed: whether one assay can calibrate a different cellular endpoint, and how apparently conflicting results can reflect different biological properties. Heme-dependent active-enzyme availability is a compatible explanation, not a uniquely identified microscopic cause. Predominantly monomeric behavior is qualified rather than asserted at every concentration.

This is an assistant source-aware revision of the existing example, not a fresh teacher-generated solution. No new measurements, mutations, or procedures are proposed. Source agreement and the rubric have not been validated by an expert human or a student-learning study.

</details>

---

# 3. Choosing a labeling tool for the measurement objective

## Question

The TurboID study reported a candidate sequence change that appeared beneficial for labeling activity and was included, with other changes, in TurboID. It was also examined in the miniTurbo background but was not retained there because labeling increased when added biotin was omitted. In the broader comparison, miniTurbo generally produced less labeling before biotin addition, whereas TurboID generally produced greater labeling yield.

These enzymes produce covalent labels. Omitting added biotin does not remove biotin already present in cells. The reported candidate-change comparison is qualitative; it supplies neither an isolated binding constant nor a protein-by-protein history of when labels formed.

Consider a project whose purpose is to associate recovered proteins with a defined interval beginning at biotin addition. It also needs enough recovered material for analysis. There are no project-specific measurements of background labeling or recovery yet.

Compare TurboID and miniTurbo as initial candidates for this project. Make a provisional choice and explain the tradeoff. What missing information would most affect that choice? Explain whether the reported candidate change counts as an improvement for this objective, and how your recommendation could change for a project that prioritizes cumulative yield instead.

## Answer

miniTurbo is a reasonable initial candidate when the defined start time is the priority, because its lower reported pre-addition labeling better serves that objective. This is provisional: its recovery and background in the project's actual context could change the choice. If recovery were inadequate, TurboID's higher yield could become more valuable, with the timing compromise made explicit. In the tested miniTurbo background, the candidate change's increased omit-added-biotin signal is a disadvantage for temporal control despite possible yield benefits; the supplied evidence does not establish its molecular mechanism. A project prioritizing cumulative yield could instead favor TurboID. Neither recommendation is universal.

## Assessment rubric

- Makes a provisional tool choice using both the temporal objective and the need for sufficient recovery. Accept either candidate when the tradeoff and assumptions are defensible.
- Identifies project-specific background and recovery as decision-relevant missing evidence; does not convert the paper's broader comparison into a guaranteed outcome in the new context.
- Explains how the candidate change and an objective emphasizing cumulative yield could be valued differently. Do not require a unique molecular mechanism, a universal tool preference, or extra discussion of subtraction.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency and rubric review. No independently documented blinded solver test or expert human validation is claimed for the current question.


Primary source: [Branon et al., Efficient proximity labeling in living cells and organisms with TurboID](https://doi.org/10.1038/nbt.4201), Methods under “Yeast display directed evolution” for the reported candidate-change decision, Figure 2a–b and Discussion for the yield/background comparison, and Supplementary Note 2 for labeling chemistry and qualified mechanistic interpretations.

Supplied evidence: the published qualitative activity and omit-added-biotin observations, the broader reported tool comparison, and the covalent nature of labeling. The proposed project and its alternative objectives are hypothetical assessment framing. No new quantitative effect size or project-specific performance is supplied or inferred.

Inference being assessed: how a measurement objective and a recovery constraint change the value of an observed property, and which missing evidence could reverse a provisional recommendation. The example does not identify an affinity change, predict a new variant, or prescribe a labeling procedure. The candidate's identity and the unused reference sequence from the earlier question were removed because they are unnecessary to the decision.

This is an assistant source-aware revision of the existing example, not a fresh teacher-generated solution. Source agreement and the rubric have not been validated by an expert human or a student-learning study.

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

A heme-containing cytochrome P450 is the strongest assignment. The segment FGHGHHVCLG at residues 338–347 matches the P450 FxxGxxxCxG signature; Cys345 is a candidate axial ligand to heme iron. ECLR at 274–277 and AGHETT at 235–240 provide supporting P450-context evidence in the expected order. A cysteine could also participate in iron–sulfur binding, but that possibility alone does not explain this combined pattern. The argument depends on family context, rather than cysteine presence. Sequence supports a cofactor hypothesis; it does not demonstrate bound heme, the substrate, reaction specificity or catalytic activity.

## Assessment rubric

- Identifies heme/P450 as the leading assignment and cites the actual FGHGHHVCLG segment, with at least one supporting P450-associated segment.
- Explains the proposed cysteine–heme-iron coordination without calling it a covalent attachment of heme to the polypeptide.
- Compares one plausible alternative using positive sequence context; does not treat a missing generic motif as definitive exclusion.
- Separates predicted family/cofactor from measured occupancy or activity. Credit a defensible alternative assessment if it addresses the same sequence evidence and explains its uncertainty.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency and rubric review. No independently documented blinded solver test or expert human validation is claimed for the current question.


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

Two candidate EF-hand calcium-binding loops are DRDGNGFISKQE at residues 46–57 and DMDGDGQVDFEE at 82–93. Both place oxygen-donating residues at positions 1, 3 and 5, glycine at 6, and glutamate at 12, supporting a repeated calcium-binding architecture. A generally acidic region could also attract ions, but would not explain these repeated positional patterns as well. The motifs lie upstream of a strongly hydrophobic near-terminal region, consistent with a soluble binding domain and membrane anchor. Sequence does not measure calcium affinity, ion selectivity, occupancy or how many sites are functional, and it does not directly demonstrate the EF-hand fold.

## Assessment rubric

- Proposes EF-hand calcium binding and identifies both actual 12-residue segments, explaining at least two relevant positional features.
- Explains why repeated ligand-compatible patterns support more than a generic acidic-composition claim.
- Uses the near-terminal hydrophobic region only as architectural context, without assigning an experimentally established topology.
- Does not infer affinity, selectivity, occupancy or four functional sites from sequence. Credit a reasoned tentative assignment or alternative if it addresses both loops and distinguishes evidence from speculation.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency and rubric review. No independently documented blinded solver test or expert human validation is claimed for the current question.


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

A single near-C-terminal membrane anchor is strongly supported by the continuous hydrophobic stretch ILLVILGIIVVIAILTAIAFFV at residues 193–214, followed by KGH. This composition-based 22-residue call favors a bilayer-spanning helix over purely peripheral association; it is not an exact membrane-boundary measurement. The much longer upstream region is rich in charged and polar residues, without comparable hydrophobic stretches. The basic RRIIQNR flank at 186–192 supports a cytosolic upstream region through the positive-inside tendency, although assigning a membrane side is less secure than identifying the anchor. The sequence does not establish exact helix boundaries, insertion route or organelle destination.

## Assessment rubric

- Identifies the actual near-terminal hydrophobic stretch and short following tail as support for a single integral anchor.
- Accepts a justified approximate span ending at 213 or 214; distinguishing a hydrophobic-composition call from a precise helix boundary matters more than one-residue agreement.
- Contrasts an integral anchor with peripheral association using that sequence evidence, rather than assuming all membrane-associated proteins span the bilayer.
- Distinguishes strong anchor evidence from the weaker orientation inference; a cautious refusal to assign orientation is acceptable if explained.
- Does not infer Golgi/endosomal destination, exact measured boundaries or an insertion mechanism. Credit defensible alternatives that account for the hydrophobic segment and explain what evidence is missing.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency and rubric review. No independently documented blinded solver test or expert human validation is claimed for the current question.


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

Two PDZ-like interaction modules are a reasonable family-level hypothesis. EYGYNLHAEKGRGQFVGTVD resembles EFGFNLHAERGRGHFIGTVD, with additional downstream similarity between IFAVNGHSIIGENHKKVVERIK and IVGVNGQLIYPTTGHKEVVALIK. Extended repetition supports two related modules more than a single short motif does, although repetition alone does not uniquely identify PDZ domains. The PPPPPP stretch could be an SH3-binding ligand motif; it is not evidence that this protein contains an SH3 fold. No literal GLGF motif occurs, so that cannot be cited. Sequence inspection does not establish precise domain boundaries, whether both modules bind peptides, their affinities or their physiological partners.

## Assessment rubric

- Identifies extended similarity in two regions using actual sequence segments; does not rely only on a low-complexity run.
- Treats tandem PDZ-like modules as a hypothesis requiring family knowledge, not a deduction from repeat count alone. A cautious tandem-module answer can receive full credit if it explains why exact family identification remains uncertain.
- Distinguishes a potential proline-rich ligand motif from a folded SH3 domain; does not invent a literal GLGF motif.
- Separates architecture from precise boundaries, partner identity, functional binding and affinity. Credit another family hypothesis if it explains the extended sequence evidence and acknowledges its limitations.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency and rubric review. No independently documented blinded solver test or expert human validation is claimed for the current question.


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

A retinal-binding microbial opsin is a plausible leading hypothesis. Repeated hydrophobic regions across this compact sequence support a multipass membrane bundle. Lys205 lies in the late hydrophobic segment VALIVYLDLVTKVGFGFIALDAAATL, a position compatible with the lysine that forms a retinal Schiff base in microbial opsins. This combined architecture and residue context is more persuasive than lysine presence alone. A soluble chromophore-binding fold fits the extensive membrane-length hydrophobicity less well. Nevertheless, other membrane proteins can have multiple helices and lysines. Sequence inspection does not prove retinal occupancy, attachment at Lys205, exact helix boundaries, spectral properties or sensory function.

## Assessment rubric

- Connects repeated hydrophobic regions with a multipass membrane architecture, without presenting sequence windows as experimentally measured helices.
- Identifies Lys205 in the actual late hydrophobic segment and explains its compatibility with retinal Schiff-base chemistry.
- Compares a soluble chromophore-binding interpretation using architecture; does not claim that seven helices or a lysine uniquely establishes an opsin.
- Separates the proposed mechanism from demonstrated attachment, occupancy, spectra or function. Credit a more cautious membrane-protein conclusion or defensible alternative if it addresses the residue evidence and explains what prevents a unique assignment.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency and rubric review. No independently documented blinded solver test or expert human validation is claimed for the current question.


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

The observations show probe-dependent labeling patterns consistent with redistribution; neither similar soluble affinity nor a diffuse image establishes the native state. One useful comparison is organization across functional valencies with measured initial target engagement and detection differences accounted for. A systematic valency-dependent change would support crosslinking as a contributor; persistence without that pattern would motivate other preparation or cellular effects. A second comparison is agreement with an independently validated organization readout that minimizes probe perturbation. Agreement would strengthen, but not prove, a native-state interpretation; disagreement would challenge it. Concentration dependence is another defensible comparison, although changing concentration can also change engagement. Matching engagement alone does not establish a molecular mechanism or the unlabelled baseline.

## Assessment rubric

- Separate binding affinity, functional valency, cellular target engagement, optical detection, and native organization.
- Develop two useful comparisons: identify the uncertainty each addresses and a possible result that would alter the conclusion. A well-justified concentration-based comparison may replace either reference comparison.
- Explain relevant confounding. Initial engagement matching does not control every later interaction, and concentration effects alone do not isolate a mechanism.
- Require independent evidence before calling either observed pattern native. Do not claim that the suggested comparisons or their outcomes were reported in the paper.
- Accept other defensible priorities and compatible interpretations. Naming a particular comparison without explaining its evidential value is insufficient.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency and rubric review. No independently documented blinded solver test or expert human validation is claimed for the current question.


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

The result establishes failure of this relative-enrichment filter, not absence from contacts or lack of biological importance. P might have a substantial cytosolic pool alongside genuine contact association, or it might have little contact association under the sampled conditions. The current data do not distinguish these possibilities. Independent localization evidence would address where P is found; functional evidence would address its contribution to the process of interest. Neither claim follows directly from the other. Deferring P can be reasonable when stronger candidates or limited resources dominate, provided it is a prioritization decision rather than a biological exclusion. Relevant independent evidence and the project's objective could change that priority.

## Assessment rubric

- State exactly what P passed and failed; distinguish a filtered enrichment list from an inventory of all biologically important proteins.
- Give at least two compatible explanations without asserting either as P's measured biology. Dual localization and weak or absent contact association are examples; other justified explanations involving biological accessibility or labeling history also receive credit.
- Distinguish evidence about localization from evidence about function. Do not equate proximity with direct binding or functional necessity.
- Make a reasoned prioritization decision. Accept follow-up or deferral when assumptions, competing priorities, and evidence that would change the decision are explained.
- No numerical calculation is required. Do not infer protein-specific rates, occupancy, or an individual error probability from the supplied comparison.

<details>
<summary>Sources and review notes</summary>

**Creation method:** Source-aware assistant revision (revision 6, final polish 1).

**Review type:** Assistant source-consistency and rubric review. No independently documented blinded solver test or expert human validation is claimed for the current question.


[Cho et al., Split-TurboID enables contact-dependent proximity labeling in cells](https://doi.org/10.1073/pnas.1919528117) (2020): Figure 3F and Results before Figure 4 for unequal-duration bulk matching; Figure 4 and Methods, Generation of ER–Mitochondria Proteome Lists, for sequential filtering; Results before Validation of ER–Mitochondria Contact Orphans for loss of dual-localized proteins.

Source qualification: [UniProt P06709](https://www.uniprot.org/uniprotkb/P06709/entry) is native Escherichia coli BirA, the ancestral reference backbone. It is not the complete evolved split-TurboID fragments or their tags, localization elements and dimerization domains.

[Historical independent-check status](artifacts/example-10/independent_check.json). The earlier revision records a check assertion, but its standalone solver response and model metadata were not recovered. No independently verifiable blinded check of the current open-response question is claimed.

The assay description is source-derived. P, the collaborator's proposal, and the prioritization discussion are hypothetical. The paper does not supply P's identity, localization, function, or labeling kinetics. Exact durations and the reference-set false-discovery criterion were removed because this item requires no valid protein-specific quantitative calculation. Relative enrichment remains useful for its intended filtering role.

This is a source-aware assistant revision responding to review feedback, not a fresh teacher-model response or expert human validation. No new experiments or outcomes are claimed, and training benefit has not been measured. Earlier questions, answers, and generation records remain in Git history and existing artifacts.

</details>
