# AI-created protein reasoning training data

# 1. APEX: enzyme behavior depends on substrate conditions

## Question

Reference protein sequence (canonical wild-type backbone; coordinate reference only):

```text
MGKSYPTVSADYQKAVEKAKKKLRGFIAEKRCAPLMLRLAWHSAGTFDKGTKTGGPFGTIKHPAELAHSA
NNGLDIAVRLLEPLKAEFPILSYADFYQLAGVVAVEVTGGPEVPFHPGREDKPEPPPEGRLPDATKGSDH
LRDVFGKAMGLTDQDIVALSGGHTIGAAHKERSGFEGPWTSNPLIFDNSYFTELLSGEKEGLLQLPSDKA
LLSDPVFRPLVDKYAADEDAFFADYAEAHQKLSELGFADA
```


Reference: Q43758. All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded. The sequence is not the complete tagged assay construct.

Published variant identities:
APEX: substitutions K14D, W41F, E112K; deletions none.
APEX2: substitutions K14D, W41F, E112K, A134P; deletions none.

Supplied assay observations:
- With 1.4 mM guaiacol, the reported rate maximum occurs around 0.1 mM peroxide for APEX and 2.5 mM for APEX2; rates decrease above these ranges.
- With 0.5 mM guaiacol, the corresponding values are around 0.05 mM and 0.5 mM.

**Question:** Which interpretation best explains the variant difference across both substrate conditions?

**Choices:**

- **A.** Only the higher-guaiacol condition shows an APEX2 advantage; the lower-guaiacol condition gives the same inhibition threshold for both enzymes.
- **B.** Both substrate conditions show a higher peroxide-inhibition threshold for APEX2, with unchanged thresholds when guaiacol concentration changes.
- **C.** Both substrate conditions show a higher peroxide-inhibition threshold for APEX2, with the threshold also depending on guaiacol concentration.
- **D.** Both substrate conditions give the same peroxide-inhibition threshold for APEX and APEX2, despite different guaiacol concentrations.

## Answer

Choice C captures both the variant difference and the dependence on guaiacol concentration.

Use the peroxide concentration at the reported rate maximum as an approximate boundary above which activity declines:
- At 1.4 mM guaiacol, the maximum occurs around 0.1 mM peroxide for APEX versus 2.5 mM for APEX2: approximately a 25-fold higher peroxide concentration for APEX2.
- At 0.5 mM guaiacol, the corresponding values are 0.05 mM and 0.5 mM: approximately a 10-fold higher concentration for APEX2.

Thus, both substrate conditions show a higher apparent peroxide-inhibition threshold for APEX2. The threshold is also guaiacol-dependent: increasing guaiacol from 0.5 to 1.4 mM shifts the maximum from 0.05 to 0.1 mM peroxide for APEX and from 0.5 to 2.5 mM for APEX2, approximately twofold and fivefold increases, respectively.

Mechanistically, peroxide drives formation of oxidizing heme intermediates during peroxidase catalysis, while guaiacol supplies reducing equivalents for productive turnover. Excess peroxide can promote nonproductive states or oxidative inactivation. Changing the electron-donor concentration can alter the balance between productive turnover and these competing processes, so an apparent peroxide-inhibition threshold need not be substrate-independent. This is consistent with the observations without establishing their precise molecular cause.

The listed sequence difference is A134P added to the shared K14D/W41F/E112K background. The assay observations establish the kinetic distinction; alanine-to-proline substitution chemistry alone would not uniquely predict it.

A is excluded because APEX2 also has a higher threshold at lower guaiacol. B is excluded because the thresholds change with guaiacol concentration. D is excluded because the variants have different thresholds under both conditions.

**Final answer: C**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

Primary full-text Results and Figure 2E text support the condition-dependent peroxide comparisons. The precise molecular cause of the A134P effect remains an interpretation, rather than an experimentally established mechanism.

### Answer limitations

The reported rate maxima are approximate, condition-dependent markers, not formal inhibition constants. These observations do not distinguish reversible inhibition from oxidative inactivation, establish a structural mechanism for A134P, or show that APEX2 has a higher maximum rate. The canonical sequence provides coordinates, not the complete tagged assay construct.

### References and source review

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to AI remain visible above.

Source identity: **wild-type soybean ascorbate-peroxidase reference backbone** — [UniProt Q43758](https://www.uniprot.org/uniprotkb/Q43758/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly compares both guaiacol conditions and checks the approximate concentration ratios.
- Explains the peroxide/electron-donor balance without converting apparent rate maxima into formal inhibition constants or asserting an unmeasured structural mechanism.
- The assay evidence establishes the phenotype; the sequence supports the A134P background comparison.

Source support:

- Figure 2e; accompanying Results paragraph on purified-protein kinetics
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- Values are approximate maxima reported in Results, not newly fitted kinetic constants.
- Use corrected Figure 2a symbols and Figure 2e axis labels; correction dated December 10, 2014.

Primary references:

- [Directed evolution of APEX2 for electron microscopy and proximity labeling](https://www.nature.com/articles/nmeth.3179)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.

[Original source records and unchanged AI output](../astra_enzyme_mutation_pool_2026-10-23/examples/case-001.md)


### Revision 4 source-caption clarification

The UniProt sequence above is the wild-type soybean ascorbate-peroxidase reference backbone. It is a coordinate reference for the separately listed APEX/APEX2 variants, not the assayed engineered construct. Only this source caption was corrected; the question and generated answer are unchanged. [Prior presentation](artifacts/example-01/previous_presentation_v2.txt) · [Revision record](revision_v4.json).

</details>

---

# 2. APEX: why an active enzyme can still be a poor cellular reporter

## Question

Protein: pea cytosolic ascorbate peroxidase (APX). The full canonical wild-type sequence below is a coordinate reference; residue 1 is the initial methionine. It is not the complete expressed fusion.

Protein sequence:

```text
MGKSYPTVSPDYQKAIEKAKRKLRGFIAEKKCAPLILRLAWHSAGTFDSKTKTGGPFGTIKHQAELAHGA
NNGLDIAVRLLEPIKEQFPIVSYADFYQLAGVVAVEITGGPEVPFHPGREDKPEPPPEGRLPDATKGSDH
LRDVFGKAMGLSDQDIVALSGGHTIGAAHKERSGFEGPWTSNPLIFDNSYFTELLTGEKDGLLQLPSDKA
LLTDSVFRPLVEKYAADEDVFFADYAEAHLKLSELGFAEA
```

Published variants use those wild-type coordinates: mAPX carries K14D/E112K; APEX carries K14D/E112K/W41F. The enzyme cores have no deletion. Experimental tags, targeting sequences and fusion partners are not shown.

Published observations:
- Wild-type APX and mAPX had similar activity in the purified-enzyme comparison, which used guaiacol, an aromatic model substrate.
- Wild-type APX fused to connexin43 was largely retained inside cells, whereas mAPX fusions reached gap junctions much more effectively.
- In the cytosol, mAPX gave weaker DAB staining than wild-type APX; supplying heme increased its staining. DAB staining reports peroxidase-catalyzed product formation.
- APEX gave stronger cellular DAB staining than mAPX while retaining similar predominantly monomeric behavior.

**Question:** Which interpretation best preserves what the biochemical and cellular comparisons actually measure?

- **A.** Purified guaiacol activity provides the per-molecule calibration for cellular DAB staining; after that calibration, the remaining signal differences can be assigned to amounts of correctly localized fusion protein.
- **B.** The heme-supplementation response provides a direct ranking of equilibrium heme-binding affinity; it therefore identifies weaker heme affinity as the complete cause of the mAPX cellular defect.
- **C.** The mutations balance different properties: reduced self-association can improve fusion trafficking, while cell staining also depends on active heme-containing enzyme and substrate chemistry. Similar purified guaiacol activity does not calibrate cellular DAB signal.
- **D.** Because APEX and mAPX have similar oligomeric behavior, their cellular DAB difference primarily reports different amounts of correctly localized fusion protein, rather than a difference in activity per enzyme molecule.

Interpret the published observations using the relevant biology. Explain the alternatives, then give one answer letter. Do not propose new variants or experimental procedures.

## Answer

*AI-generated answer; unchanged response.*

APX is a heme-dependent peroxidase that uses hydrogen peroxide to oxidize electron-donor substrates. Cellular DAB staining measures accumulated catalytic product, not protein abundance directly. Its intensity can depend on the amount of accessible enzyme, the fraction that is folded and heme-loaded, substrate-dependent catalytic performance, and local staining conditions.

What the observations establish

1. Purified guaiacol activity: Wild-type APX and mAPX performed similarly with guaiacol under the supplied purified-enzyme conditions. Guaiacol and DAB are both aromatic substrates, but that does not make their binding and oxidation kinetics interchangeable. Even a rigorously equal-molecule guaiacol comparison would not establish equal DAB activity per molecule in cells or equal cellular fractions of active holoenzyme.

2. Connexin43 trafficking: The greater delivery of mAPX fusions to gap junctions is a localization/trafficking result. Reduced self-association can lessen interference with a fusion partner’s assembly and transport, providing a biologically plausible explanation for improved trafficking. This is distinct from catalytic activity. In particular, the connexin43 localization comparison cannot normalize the separate cytosolic DAB-staining comparison.

3. Heme supplementation: Increased mAPX staining after heme supply is consistent with more functional heme-containing enzyme becoming available. It does not directly measure equilibrium heme-binding affinity. Cellular heme availability, delivery and incorporation, folding, and stability can all influence the active-enzyme population. Thus, the response neither ranks equilibrium affinities nor establishes weaker affinity as the complete cause of the staining deficit.

4. APEX versus mAPX: APEX adds W41F and produces stronger cellular DAB staining while retaining similar predominantly monomeric behavior. This shows that improved staining does not require a further reported change in oligomerization. Similar oligomeric behavior does not establish equal DAB turnover, equal heme loading, equal stability, or equal cellular abundance. The precise contribution of each remains unresolved.

Evaluation of the alternatives

A is incorrect because purified guaiacol activity is not a per-molecule calibration for cellular DAB staining. Differences in substrate chemistry, active-enzyme fraction, and cellular conditions remain unaccounted for.

B is incorrect because a downstream activity response to heme supplementation is not an equilibrium binding measurement. Its claim of a complete causal explanation is also unsupported.

C correctly separates reduced self-association and fusion trafficking from heme-dependent, substrate-specific catalytic output. It preserves both the measured observations and their mechanistic limits.

D is incorrect because similar oligomerization does not control for catalytic performance or the fraction of active holoenzyme. Protein amount or localization could contribute, but the supplied evidence does not justify assigning them the primary role.

Answer: C.

Final answer: C

<details>
<summary>Sources, evidence checks and limitations</summary>

**Source-supported answer: C.** The answer selects C and matches that reference.

### Primary evidence

[Engineered ascorbate peroxidase as a genetically encoded reporter for electron microscopy](https://doi.org/10.1038/nbt.2375) (2012).

- Figure 1b-e and Results, printed pp.1143-1144: K14D/E112K monomerization, concentration-dependent residual association and connexin43 trafficking.
- Figure 2b-d and Results, printed pp.1144-1145: purified guaiacol kinetics, cellular DAB comparisons, and heme supplementation.
- Online Methods, Cloning and mutagenesis: pea cytosolic APX reference, with some humanized-codon versions.

The original pea-APX study distinguishes fusion trafficking, purified model-substrate activity, cellular staining and heme response. It supports the observations supplied to the solver; the multiple-choice interpretation is AI-created and is not an author-assigned experimental label.

### Answer limitations

- No unique microscopic mechanism or full causal decomposition is established.
- The question does not predict a mutation effect from unannotated sequence alone.
- A matched reference label does not validate every future generated explanation or demonstrate training benefit.

### Source qualifications

- Pea P48534 is distinct from the soybean Q43758 backbone in the retained APEX2 example.
- The full canonical reference is shown, not a reconstruction of the His-tagged purification proteins, NES fusions or connexin43 fusions.
- Predominantly monomeric is concentration-dependent; residual self-association at high concentration was reported.
- Heme incorporation/stability is a supported working explanation; the experiment does not isolate equilibrium heme affinity or exclude other contributors.
- Guaiacol and DAB are different substrates and the cellular endpoint is not a direct molecule count.

### Evidence review and provenance

- The canonical sequence and published observations are supplied; this is experimental interpretation, not sequence-only prediction.
- Source-backed AI interpretation, not an expert-human label; no measured training benefit or item discrimination is claimed.

This is an unchanged new AI-generated response to the question shown above. The solver received only the sequence and observations printed in the question; full papers and the private reference label were withheld. Assistant source review followed generation.

[Exact generation request](artifacts/example-02/request.json) · [Unchanged generated output](artifacts/example-02/generated_output.json) · [Question, answer and source verification](artifacts/example-02/source_verification.json) · [Revision record](revision_v4.json)

Assistant reviews are not expert human validation, and training gains have not been measured.

</details>

---

# 3. TurboID and miniTurbo: when more labeling weakens the time window

## Question

Reference protein: Escherichia coli BirA, the ancestral biotin ligase of TurboID and miniTurbo. The full canonical wild-type sequence is supplied only for coordinates; it is not the complete evolved or tagged assay construct.

Protein sequence:

```text
MKDNTVPLKLIALLANGEFHSGEQLGETLGMSRAAINKHIQTLRDWGVDVFTVPGKGYSLPEPIQLLNAK
QILGQLDGGSVAVLPVIDSTNQYLLDRIGELKSGDACIAEYQQAGRGRRGRKWFSPFGANLYLSMFWRLE
QGPAAAIGLSLVIGIVMAEVLRKLGADKVRVKWPNDLYLQDRKLAGILVELTGKTGDAAQIVIGAGINMA
MRRVEESVVNQGWITLQEAGINLDRNTLAAMLIRELRAALELFEQEGLAPYLSRWEKLDNFINRPVKLII
GDKEIFGISRGIDKQGALLLEQDGIIKPWMGGEISLRSAEK
```

Numbering uses the initial methionine as wild-type residue 1. Both evolved enzyme cores delete Ala146. miniTurbo additionally lacks wild-type residues 1-63. Thus wild-type Met241 corresponds to enzyme-core position 240 in TurboID and 177 in miniTurbo, before any added tags or linkers. The evolved backgrounds contain other substitutions; the sequence above does not represent either final variant.

Published observations:
- Screening found M241T potentially beneficial for labeling activity, and the substitution was included with other changes in TurboID.
- M241T was also tested in the miniTurbo background but was not retained because signal increased when added biotin was omitted.
- In the broader comparison, miniTurbo generally showed less labeling before biotin addition than TurboID, while TurboID generally gave greater labeling yield.

The purpose is to label neighboring proteins within a defined time window after biotin addition. The omit-added-biotin condition does not experimentally remove the biotin already present in cells.

**Question:** What is the most defensible interpretation of the M241T tradeoff for that time-window objective?

- **A.** The higher omit-biotin signal identifies stronger equilibrium biotin binding as the M241T mechanism; correcting added biotin concentration for that affinity difference should recover the original labeling window.
- **B.** Labeling before the intended start can use biotin already present and leave covalent marks on proteins. Greater total yield can therefore weaken temporal control; these observations do not identify which molecular step M241T changes or establish the same effect in every background.
- **C.** Protein-by-protein subtraction of the omit-biotin sample converts the later accumulated signal into labels acquired exclusively after biotin addition, because the same labeling chemistry operates in both samples.
- **D.** The difference between TurboID and miniTurbo identifies interaction with the deleted N-terminal domain as the source of the M241T tradeoff; the other evolved substitutions and expression differences need not contribute to that interpretation.

Interpret the published observations using the relevant biology. Explain the alternatives, then give one answer letter. Do not propose new variants or experimental procedures.

## Answer

*Source-aware AI explanation.*

B. Greater labeling yield can weaken control over when the labels were acquired.

A promiscuous biotin ligase uses biotin and ATP to produce an activated intermediate that can covalently label nearby proteins. Omitting added biotin does not establish that the cell contains no biotin. Signal generated before the intended start can therefore contribute to a later accumulated readout. A protein carrying a label need not have acquired it during the intended window; movement and turnover can further change the observed population.

This explains why the miniTurbo observation matters. M241T increased signal when added biotin was omitted, so excluding that substitution could favor temporal control even if including it increased total labeling. The choice of an enzyme variant depends on the measurement objective: maximal accumulated signal and a well-defined observation window are different objectives.

The observations do not identify the molecular step altered by M241T. More signal could reflect differences in the active enzyme population, substrate handling, intermediate production or release, or other context-dependent properties. It is not a measurement of an isolated affinity or catalytic constant, and the full-length and truncated evolved enzymes differ in more than their N-terminal domain.

A confuses an accumulated labeling endpoint with an equilibrium binding measurement. No measured affinity change is supplied, so the proposed affinity correction is unsupported.

B connects the covalent labeling chemistry to the timing problem while leaving the particular molecular mechanism and its generality unresolved.

C overstates what background subtraction establishes. Subtraction can help quantify differences between matched samples. It does not generally identify when each individual covalent mark was formed or guarantee an exclusively post-addition protein set. Estimating an incremental signal under a validated model is a narrower claim.

D assigns a unique causal interaction to the N-terminal deletion without isolating that change from the other substitutions and expression differences.

The supplied wild-type BirA sequence is a coordinate reference. It does not, by itself, predict this mutation's labeling tradeoff. The experimental observations and labeling chemistry support the inference.

Answer: B.

Final answer: B

<details>
<summary>Sources, evidence checks and limitations</summary>

**Source-supported answer: B.** The answer selects B and matches that reference.

### Primary evidence

[Efficient proximity labeling in living cells and organisms with TurboID](https://doi.org/10.1038/nbt.4201) (2018).

- Methods, Yeast display directed evolution, last two paragraphs: M241T activity observation, introduction with K194I/S263P into G3, and exclusion of M241T from miniTurbo because omit-biotin signal increased.
- Methods, Cloning: all ligase variants have wild-type A146 deleted.
- Supplementary Table 1: TurboID and miniTurbo genotype rows; miniTurbo retains wild-type span64-321 plus A146 deletion.
- Figure 2a-b and Discussion: yield versus pre-biotin-labeling tradeoff; miniTurbo temporal-control consideration.
- Supplementary Note2: biotin-AMP formation, release and covalent labeling; proposed mechanisms remain hypotheses.

The paper reports the M241T decision and the broader yield/background tradeoff. Covalent label accumulation explains why pre-window activity matters. The multiple-choice inference is AI-created; no new M241T measurements, fixed affinity change or causal epistasis map is claimed.

### Answer limitations

- A baseline control improves interpretation but cannot generally timestamp individual covalent marks after the fact.
- Protein movement and turnover can influence accumulated labeling; marks are not asserted permanent.
- The result applies to the reported backgrounds and conditions, not every cell, compartment or variant.

### Source qualifications

- The displayed sequence is native321-residue BirA, not TurboID, miniTurbo or a complete V5/NES fusion.
- All substitution labels retain native BirA coordinates even after deletions.
- A146 deletion gives n-1 for retained n>146 in TurboID; deletion1-63 plus146 gives n-64 for retained n>146 in miniTurbo. M241T is therefore core240 or177, respectively. Added fusion offsets are unknown here.
- The enzyme-core genotypes are supported by Supplementary Table1; canonical references are checked independently against official UniProt.
- The main-text methods describe the M241T miniTurbo result qualitatively without a numeric fold-change or isolated binding/turnover constants.
- The comparison does not isolate the N-terminal domain as the cause of context dependence; other substitutions, enzyme stability and expression can matter.

### Evidence review and provenance

- The canonical sequence and published observations are supplied; this is experimental interpretation, not sequence-only prediction.
- Source-backed AI interpretation, not an expert-human label; no measured training benefit or item discrimination is claimed.

The sole fresh generation attempt returned HTTP 502 without an answer. This explanation was subsequently authored by an AI assistant with the frozen question and reviewed source evidence available; it is a source-aware authored explanation, not a successful teacher response or a blinded solve. The failed request and response are preserved; $7 remains reserved because billing is uncertain. No retry was made.

[Failed generation request](artifacts/example-03/request.json) · [Recorded failed attempt](artifacts/example-03/failed_attempt_public.json) · [Failed response](artifacts/example-03/failed_response.txt) · [Authored explanation](artifacts/example-03/source_aware_answer.json) · [Question, answer and source verification](artifacts/example-03/source_verification.json) · [Revision record](revision_v4.json)

Assistant reviews are not expert human validation, and training gains have not been measured.

</details>

---

# 4. Distinguishing heme from other cofactors

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

D. Heme is the most strongly supported cofactor.

The decisive evidence is a coherent combination of cytochrome P450 sequence signatures, rather than simply the presence of cysteine or histidine residues.

1. Heme-binding signature: residues 338–347 are FGHGHHVCLG. This matches FxxGxxxCxG, where x denotes any residue. In P450 proteins, the cysteine at this motif position supplies the axial sulfur ligand to the heme iron. Thus, Cys345 is a strong candidate for a heme-ligating cysteine. This is the most direct cofactor-related clue.

2. Supporting P450 core signature: residues 274–277 are ECLR, matching the characteristic E-x-x-R motif associated with the P450 K helix. This motif supports the fold assignment; it is not itself a direct metal-binding motif.

3. Supporting catalytic-region signature: residues 235–240 are AGHETT. Its acidic residue and adjacent threonines are consistent with the conserved I-helix region used in oxygen activation by many P450 enzymes. Assigning this segment to an I helix is an inference from the motif context, not an observed secondary structure.

These features occur in the expected sequence order: the I-helix-like segment, the E-x-x-R motif, and then the cysteine-containing heme-binding loop toward the C terminus. Together they strongly support a P450-family protein, whose defining prosthetic group is heme.

Comparison with the alternatives:
- A. FAD and B. FMN: flavin-binding proteins are diverse, so neither cofactor can be excluded merely by the absence of one universal motif. Nevertheless, the observed combination specifically supports a P450 heme-binding domain, not a flavin-binding assignment.
- C. A four-iron four-sulfur cluster: cysteines can ligate iron–sulfur clusters, but cysteine presence alone is insufficient evidence. Here the key cysteine occurs in a characteristic heme-thiolate signature reinforced by two other P450-associated motifs.
- D. Heme: directly explains the predicted cysteine–iron coordination and the overall motif combination, making it the most defensible choice.

**Final answer: D**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

Primary structural Results directly support heme, its coordinating cysteine and the catalytic-region facts. Assigning a family from sequence remains an inference; exact catalytic properties require experiments.

### Answer limitations

This is a sequence-based cofactor prediction, not direct evidence of bound heme. The sequence does not establish actual cofactor occupancy, substrate specificity, or catalytic reaction.

### References and source review

The following information was **not supplied to AI**.

Verified source identity: **Biotin biosynthesis cytochrome P450** — [UniProt P53554](https://www.uniprot.org/uniprotkb/P53554/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-004/uniprot_record.json), withheld from AI.

Source-supported answer: **D**. AI’s selected answer matches it.

The primary structural study visualizes the enzyme with its carrier-protein-bound substrate above an active-site heme. It identifies Cys345 as the proximal sulfur ligand to the heme iron. These observations directly support heme as the cofactor.

Scientific review: Strong sequence-based explanation.

- The cysteine heme-ligand signature, ExxR motif and I-helix-like region form a coherent P450-family argument. Actual heme occupancy and substrate specificity remain unmeasured.

Strong biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- A cysteine by itself does not prove heme binding; the relevant sequence context and protein-family evidence matter.
- Do not claim that the paper demonstrates a covalent bond attaching the heme group to the polypeptide. The inspected text describes a cysteine thiolate ligand coordinating heme iron.
- Identifying the cofactor does not establish the exact substrate, reaction specificity or biotin-biosynthesis role from the anonymous sequence alone.

Papers and experimental references:

- [Structural insights from a P450 Carrier Protein complex reveal how specificity is achieved in the P450BioI ACP complex.](https://pmc.ncbi.nlm.nih.gov/articles/PMC2572933/). The structure and Active Site Architecture section directly establish heme and the coordinating Cys345 residue. Review scope: Primary full-text paper, abstract, structural Results and Active Site Architecture section inspected.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.

[Original source records and unchanged AI output](../astra_sequence_only_nine_2026-10-23/examples/case-004.md)

</details>

---

# 5. Calcium binding through repeated structural motifs

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

- **A.** Binding calcium ions through EF-hand domains.
- **B.** Binding a structural zinc ion through a C2H2 zinc-finger domain.
- **C.** Binding heme to catalyze peroxide-dependent oxidation.
- **D.** Binding FAD to transfer electrons during redox catalysis.

## Answer

A. Binding calcium ions through EF-hand domains is the best-supported choice.

Sequence context: Residues 189–206, LICAFAIAFIISVMLIAA, form a strongly hydrophobic near-C-terminal segment consistent with a membrane anchor. The candidate binding motifs lie well upstream, in the likely soluble portion of the protein.

Positive evidence for EF hands: Two conspicuous 12-residue segments are residues 46–57, DRDGNGFISKQE, and residues 82–93, DMDGDGQVDFEE. A canonical EF hand contains a calcium-binding loop of approximately 12 residues between two helices. Characteristic features include oxygen-donating residues at particular loop positions, a frequently conserved glycine at position 6, and a terminal glutamate at position 12.

The first segment has D, D and N at loop positions 1, 3 and 5; the second has D, D and D at those positions. Both have G at position 6 and E at position 12. These features are chemically appropriate for calcium binding: Asp and Asn provide oxygen ligands, glycine accommodates the loop geometry, and the terminal glutamate commonly coordinates calcium through both carboxylate oxygens. Two repeated, position-specific patterns provide much stronger evidence than acidic composition alone.

Comparison with the alternatives:
• A directly explains both candidate calcium-binding loops.
• B requires the characteristically spaced Cys–Cys–His–His ligands of a classical C2H2 zinc finger. That arrangement is not present; scattered cysteine and histidine residues do not establish a zinc-finger domain.
• C requires a heme-binding pocket and a peroxide-reactive catalytic environment. Individual potential heme-ligating residues would not establish that activity, and there is no comparably specific positive evidence for it here.
• D requires a flavin-binding oxidoreductase architecture. Many FAD-binding proteins contain glycine-rich nucleotide-binding segments, but the glycine-containing segments identified here have the positional ligand pattern of calcium-binding loops instead. FAD proteins are diverse, so a missing generic motif would not categorically exclude them; the decisive point is the much stronger positive evidence for EF hands.

Thus, calcium binding through EF-hand domains is the most defensible role for the soluble region.

**Final answer: A**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

A primary abstract and experimental structure deposition support two N-terminal calcium-binding sites. The full canonical sequence includes a C-terminal region absent from the NMR construct. Binding affinity and occupancy cannot be established from sequence alone.

### Answer limitations

This is a strong sequence-based assignment, not a biochemical measurement. Calcium affinity, ion selectivity, site occupancy and the number of functional binding sites cannot be established from sequence alone. The EF-hand fold and membrane-anchor topology remain structural predictions.

### References and source review

The following information was **not supplied to AI**.

Verified source identity: **Calcium-binding protein 7** — [UniProt Q86V35](https://www.uniprot.org/uniprotkb/Q86V35/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-005/uniprot_record.json), withheld from AI.

Source-supported answer: **A**. AI’s selected answer matches it.

The primary NMR study reports two high-affinity calcium-binding EF-hand motifs in the N-terminal region of human CaBP7. Its N-terminal domain binds calcium rather than magnesium and changes conformation on binding. This directly supports calcium binding through EF-hand domains as the correct choice.

Scientific review: Strong sequence-based explanation.

- Two exact 12-residue loops show repeated, position-specific calcium-ligand patterns. The explanation distinguishes candidate EF hands from measured affinity, selectivity or occupancy.
- Source experiments support two high-affinity N-terminal sites. One reviewer had previously encountered this sequence's source association; this is not blinded expert validation.

Strong biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- Do not describe this as four functional calcium-binding sites: the supported answer concerns two high-affinity N-terminal sites.
- Acidic sequence loops are consistent with EF-hand calcium binding, but exact affinity, ion selectivity and the PI4KIIIbeta interaction come from experiments, not from acidity alone.
- The paper and annotation were retained for checking the answer after generation; they were not part of the solving prompt.

Papers and experimental references:

- [Solution NMR structure of the Ca2+-bound N-terminal domain of CaBP7: a regulator of golgi trafficking](https://pubmed.ncbi.nlm.nih.gov/22989873/). Primary abstract explicitly identifies two high-affinity EF-hand calcium sites and calcium-dependent structural changes in CaBP7. Review scope: Primary abstract and associated experimental structure deposition.
- [Solution structure of Ca2+-bound CaBP7 N-terminal domain, PDB 2LV7](https://www.rcsb.org/structure/2LV7). Experimental structure explicitly maps human CaBP7 to Q86V35 and contains two calcium ions. Review scope: Experimental deposition page, including protein identity and ligands.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.

[Original source records and unchanged AI output](../astra_sequence_only_nine_2026-10-23/examples/case-005.md)

</details>

---

# 6. Membrane anchoring

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

- **A.** A soluble peripheral membrane protein with no membrane-spanning segment.
- **B.** A protein with a large cytosolic region and a single membrane anchor near its C terminus.
- **C.** A seven-pass membrane receptor with short loops connecting its membrane-spanning helices.
- **D.** A secreted soluble protein whose only hydrophobic segment is a cleaved N-terminal signal peptide.

## Answer

B is the best-supported architecture: a large cytosolic region with a single membrane anchor near the C terminus.

The strongest evidence is residues 193–213, ILLVILGIIVVIAILTAIAFF. This 21-residue stretch is strongly hydrophobic and contains no charged residues. Its length and composition are appropriate for an alpha helix spanning a lipid bilayer; such helices commonly contain roughly 18–25 predominantly hydrophobic residues. Only VKGH at positions 214–217 follows it, so the candidate anchor lies very close to the protein's C terminus.

In contrast, residues 1–192 contain frequent charged and polar residues and no other comparably long hydrophobic stretch. They therefore support a large region outside the membrane rather than additional transmembrane helices. The N-terminal 30 residues also lack the sustained hydrophobic core expected in a classical cleavable signal peptide. Together, these features support a C-terminally anchored architecture. The basic flank RRIIQNR at residues 186–192 is consistent with the positive-inside tendency, in which positively charged flanks preferentially lie on the cytosolic side. This strengthens, but does not prove, the inference that the large upstream region is cytosolic.

Comparison of the choices:
- A is disfavored because the sequence contains a conspicuous membrane-length hydrophobic segment, rather than lacking a membrane anchor.
- B matches the large nonmembrane region, single near-terminal hydrophobic segment, and very short following tail.
- C would require seven separate membrane-spanning hydrophobic segments; that repeated pattern is absent.
- D requires an N-terminal signal peptide and a soluble mature protein. Here, the strong hydrophobic segment is at the C terminus, not the N terminus.

Thus, B best accounts for both the number and location of the candidate membrane-spanning segments.

**Final answer: B**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

A primary abstract supports the C-terminal membrane anchor and cytoplasmic region. Exact boundaries and orientation inferred from the sequence remain predictions.

### Answer limitations

Sequence strongly supports one C-terminal membrane anchor, but exact membrane-spanning boundaries and membrane orientation cannot be established conclusively. The cytosolic location of the large upstream region is a well-supported topology inference, not a direct observation.

### References and source review

The following information was **not supplied to AI**.

Verified source identity: **Vesicle transport through interaction with t-SNAREs homolog 1A** — [UniProt O89116](https://www.uniprot.org/uniprotkb/O89116/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-006/uniprot_record.json), withheld from AI.

Source-supported answer: **B**. AI’s selected answer matches it.

The original Vti1-rp2 paper describes a 217-residue protein with a hydrophobic membrane anchor at its C terminus and an accessible cytoplasmic region. Antibody-based experiments identify it as an integral membrane protein enriched at the Golgi. This supports a large cytosolic region followed by a single C-terminal membrane anchor.

Scientific review: Strong sequence-based explanation.

- The long C-terminal hydrophobic stretch, short following tail and charged upstream region directly support the architecture. Cytosolic orientation is a weaker inference and is appropriately qualified.

Strong biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- The strongly hydrophobic C-terminal stretch supports an anchor, but sequence alone does not establish the precise Golgi or endosomal destination.
- Treat the annotated anchor at residues 193-213 as a sequence-analysis boundary, not a membrane boundary measured in that paper.
- Do not confuse the soluble N-terminal domain with the whole protein being soluble: a tail anchor still makes the full protein integral to a membrane.

Papers and experimental references:

- [A 29-kilodalton Golgi soluble N-ethylmaleimide-sensitive factor attachment protein receptor (Vti1-rp2) implicated in protein trafficking in the secretory pathway](https://pubmed.ncbi.nlm.nih.gov/9705316/). The primary abstract explicitly reports 217 residues, a C-terminal hydrophobic anchor, a cytoplasmic region, integral membrane behavior and Golgi enrichment. Review scope: Primary PubMed abstract retrieved in search results; direct page opening encountered a browser challenge.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.

[Original source records and unchanged AI output](../astra_sequence_only_nine_2026-10-23/examples/case-006.md)


### Revision 4 coordinate clarification

The frozen sequence and UniProt annotation identify residues 193–213 as a 21-residue predicted anchor, followed by VKGH at residues 214–217. The worked answer was AI-edited to use those coordinates consistently; the question and answer letter B are unchanged. These are sequence-analysis boundaries, not membrane boundaries measured in the paper. [Unchanged original AI output](artifacts/example-06/original_generated_output.json) · [Frozen sequence annotation](artifacts/example-06/frozen_uniprot_record.json) · [Exact coordinate correction](artifacts/example-06/coordinate_correction.json) · [Prior presentation](artifacts/example-06/previous_presentation_v2.txt).

</details>

---

# 7. Protein-interaction domains

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

- **A.** A WD40-repeat beta-propeller that lacks PDZ domains.
- **B.** Two SH2 domains specialized for recognizing phosphotyrosine-containing peptides.
- **C.** Two PDZ domains capable of recognizing short peptide motifs on partner proteins.
- **D.** A single SH3 domain specialized for recognizing proline-rich peptides.

## Answer

C. Two PDZ domains is the most consistent architecture.

Sequence evidence:
The N-terminal portion contains two related-looking regions. Residues 24–43, EYGYNLHAEKGRGQFVGTVD, closely resemble residues 154–173, EFGFNLHAERGRGHFIGTVD. Similarity also occurs farther downstream: residues 59–80, IFAVNGHSIIGENHKKVVERIK, resemble residues 189–211, IVGVNGQLIYPTTGHKEVVALIK. Thus, the repetition is not confined to one short motif or a low-complexity run.

These extended patterns are characteristic of PDZ-like domain sequences: aromatic/glycine-containing early segments are followed by similarly organized hydrophobic and polar regions, including the recurring VNG-containing segment. Together, they support two related PDZ-sized modules. This is a family-level inference from the broader sequence pattern, not a claimed exact GLGF-motif match; PDZ sequences are variable and need not contain that literal string.

Biological interpretation:
PDZ domains are compact, usually approximately 80–110-residue α/β interaction modules. They commonly recognize short peptides at a partner protein's C terminus, accommodating the terminal carboxylate and nearby side chains in a binding groove. Some PDZ domains also recognize internal peptide motifs. This general interaction mechanism matches choice C, although the precise preferences of these two candidate domains cannot be assigned here.

Comparison with the alternatives:
• A: A WD40 β-propeller normally contains several shorter WD-repeat units. The WD at residues 239–240 is insufficient evidence: a single dipeptide does not establish a repeated propeller architecture. The extended PDZ-like duplication is more informative.
• B: SH2 domains can also occur in tandem, so repeat number alone would not distinguish them. However, the sequence does not show a convincing common SH2 phosphotyrosine-binding signature, such as an FLVRES-like region. Absence of that exact motif is not conclusive by itself, but there is positive evidence for PDZ-like repeats instead.
• D: Residues 128–133 are PPPPPP. Proline-rich sequences can be ligands for SH3 domains, but they are not themselves SH3 domains. SH3 domains are folded interaction modules, typically about 60 residues long; a single SH3 model also fails to account for the two extended PDZ-like regions.

Therefore, the strongest supported choice is a tandem-PDZ interaction-domain architecture.

**Final answer: C**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

Full primary Results and Figures 1–2 support the selected tandem-PDZ isoform and interaction with a partner terminus. Exact partner specificity is an experimental question.

### Answer limitations

Confidence applies to choosing the best architecture among the supplied alternatives. Sequence inspection does not establish exact domain boundaries, confirm that both domains bind peptides, or identify their physiological partners, preferred peptide sequences, or affinities.

### References and source review

The following information was **not supplied to AI**.

Verified source identity: **Na(+)/H(+) exchange regulatory cofactor-like protein nrfl-1** — [UniProt G5EDM4](https://www.uniprot.org/uniprotkb/G5EDM4/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-007/uniprot_record.json), withheld from AI.

Source-supported answer: **C**. AI’s selected answer matches it.

The primary study identifies the selected C. elegans NRFL-1 isoform as a two-PDZ-domain scaffold. It combines domain comparisons with direct binding experiments involving the end of the AAT-6 transporter. The results support recognition of short partner-protein peptide motifs by PDZ domains.

Scientific review: Strong sequence-based explanation.

- Extended similarity across two regions supports tandem domains. The explanation avoids inventing a literal GLGF motif and distinguishes a proline-rich SH3 ligand from an SH3 domain.
- PDZ-family recognition depends on learned family knowledge; neither precise domain boundaries nor physiological partners are demonstrated from sequence alone.

Strong biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- The literal motif GLGF occurs zero times in this selected sequence. A solution must not claim it found one or two exact GLGF motifs. PDZ loop sequences can differ.
- Some NRFL-1 splice variants contain only one PDZ domain; the answer here is specific to the selected two-domain sequence.
- The particular AAT-6 interaction and preference for PDZ2 require the paper. They are not proven by spotting two interaction domains.
- The Results text says mutation of PDZ2 impairs binding; a duplicated phrase in the Figure 2 caption is inconsistent. Prefer the Results text and source annotation rather than repeating the caption typo.

Papers and experimental references:

- [NRFL-1, the C. elegans NHERF orthologue, interacts with amino acid transporter 6 (AAT-6) for age-dependent maintenance of AAT-6 on the membrane](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0043050). Figure 1 and Results describe double-PDZ NRFL-1 isoforms; the interaction section and Figure 2 test recognition of the AAT-6 C-terminal motif. Review scope: Full primary article, especially NRFL-1 identification, Figure 1 and the PDZ interaction Results section.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.

[Original source records and unchanged AI output](../astra_sequence_only_nine_2026-10-23/examples/case-007.md)

</details>

---

# 8. Chromophore binding

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

D is the most consistent choice: retinal attachment through a Schiff-base linkage to a lysine in a membrane-embedded opsin.

1. Overall sequence architecture
The 239-residue protein contains repeated long, hydrophobic-rich windows at residues 1–26, 36–64, 73–94, 98–121, 124–145, 166–190, and 194–219. Their distribution throughout the chain strongly favors a compact multipass membrane protein rather than a soluble chromophore-binding domain. These are illustrative sequence windows, not experimentally established helix boundaries. Nevertheless, this pattern is consistent with the seven-transmembrane-helical architecture typical of microbial opsins.

2. A plausible attachment residue
The late hydrophobic-rich segment at residues 194–219, VALIVYLDLVTKVGFGFIALDAAATL, contains Lys205. In opsins, retinal's aldehyde forms a covalent imine, or Schiff base, with a lysine side chain's ε-amino group. In microbial opsins, the attachment lysine lies in the final transmembrane helix. Thus, Lys205 has both suitable chemistry and an appropriate qualitative sequence location. The combination of membrane architecture and lysine position is more informative than lysine presence alone.

3. Comparison with the alternatives
A: The sequence contains no cysteine, so no cysteine is available for the specified bilin linkage. Its compact, membrane-rich architecture also does not support the large phytochrome photosensory module described in this choice.
B: Noncovalent FMN binding in a LOV domain requires a folded, predominantly soluble pocket. The extensive hydrophobic segments throughout this sequence instead favor a membrane-helical bundle.
C: GFP-like chromophore formation requires the soluble GFP β-barrel scaffold. Although GFP proteins can have a similar overall length, length alone is not diagnostic, and the repeated membrane-length hydrophobic regions argue strongly against that architecture.

Therefore, D best explains both the overall sequence organization and the candidate lysine attachment site, while the actual chromophore and covalent linkage remain inferred.

**Final answer: D**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

A primary abstract and experimental structure deposition support retinal attachment through Schiff-base chemistry. Seven membrane helices plus a lysine are compatible with this family but do not independently prove retinal attachment.

### Answer limitations

Sequence inspection does not demonstrate retinal occupancy, Schiff-base formation specifically at Lys205, or exact transmembrane-helix boundaries. Confidence is high for choosing among the supplied mechanisms, not for experimentally establishing the modification.

### References and source review

The following information was **not supplied to AI**.

Verified source identity: **Sensory rhodopsin-2** — [UniProt P42196](https://www.uniprot.org/uniprotkb/P42196/entry).

[Frozen UniProt annotation](../astra_sequence_only_nine_2026-10-23/artifacts/case-008/uniprot_record.json), withheld from AI.

Source-supported answer: **D**. AI’s selected answer matches it.

Structural studies of this natural archaeal sensory rhodopsin establish a seven-helix membrane architecture surrounding retinal. The experimentally linked structure and paper identify attachment of retinal to Lys205, consistent with the Schiff-base mechanism in the correct answer.

Scientific review: Qualified chromophore-mechanism inference.

- Repeated hydrophobic regions, a late lysine and the absence of cysteine discriminate among these choices. They do not uniquely prove an opsin identity or retinal attachment.

Moderate biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- A seven-transmembrane pattern alone does not prove retinal binding: many unrelated receptors also cross membranes seven times. The microbial-opsin sequence pattern and conserved lysine provide the more specific connection.
- The selected sequence contains lysine at canonical position 205, but the covalent chromophore attachment is experimentally established, not demonstrated just by the presence of a lysine.
- Do not describe this microbial sensory rhodopsin as an animal G-protein-coupled receptor or infer a precise absorption wavelength from sequence inspection.

Papers and experimental references:

- [Crystal structure of sensory rhodopsin II at 2.4 angstroms: insights into color tuning and transducer interaction](https://pubmed.ncbi.nlm.nih.gov/11452084/). Primary structure paper identifies retinal/retinylidene Schiff-base chemistry in this sensory rhodopsin; its figure descriptions locate retinal attachment at Lys205. Review scope: Primary abstract and indexed figure description, checked against the experimental deposition; PMC full-text page opening encountered a browser challenge.
- [Sensory rhodopsin II experimental structure, PDB 1JGJ](https://www.rcsb.org/structure/1JGJ). Experimental deposition maps the protein to P42196 and explicitly lists retinal as a ligand. Review scope: Experimental deposition page, protein mapping and ligand list.
- [Molecular basis of transmembrane signalling by sensory rhodopsin II-transducer complex](https://pubmed.ncbi.nlm.nih.gov/12368857/). Independent primary structure study describes seven-helix retinal-containing microbial rhodopsins and the exact N. pharaonis SRII-HtrII complex. Review scope: Primary abstract.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.

[Original source records and unchanged AI output](../astra_sequence_only_nine_2026-10-23/examples/case-008.md)

</details>

---

# 9. Testing whether a protein label changes its target

## Question

Streptavidin is used to label biotinylated proteins. A4 is a tetramer of four active, His-tagged subunits; A1D3 is a tetramer containing one active and three binding-inactive subunits. The affinity measurements below use these tagged preparations, whereas the cellular comparison uses wild-type streptavidin versus A1D3.

| Preparation | Biotins bound per tetramer | Biotin Kd, mean ± SEM |
|---|---|---|
| A4 | 4 | (4.4 ± 1.1) × 10^-14 M |
| A1D3 | 1 | (4.8 ± 0.5) × 10^-14 M |

In cultured neurons expressing acceptor-peptide-tagged neuroligin-1, both fluorescent labels initially gave diffuse surface labeling. Two hours later, wild-type streptavidin produced strong clustering, whereas A1D3 labeling remained predominantly diffuse.

A colleague argues: "Because the soluble-biotin affinities are similar, the two labels should be interchangeable for observing neuroligin's native organization once the amount of initial labeling is matched."

In each proposed follow-up, the chosen matching strategy would be followed by tracking neuroligin organization with the same independent readout that does not link target molecules together. These are thought-experiment comparisons, not additional experiments reported in the paper.

**Question:** Which matching strategy most directly tests whether the labels differently perturb neuroligin organization?

- **A.** Match the measured fraction of neuroligin molecules initially occupied by each preparation.
- **B.** Measure soluble-biotin binding in the neuronal assay medium, then choose probe concentrations giving the same predicted occupancy in that soluble-binding measurement.
- **C.** Match the total concentration of functional biotin-binding sites supplied by the two preparations.
- **D.** Match the initial surface fluorescence intensity using the same imaging settings, without separately calibrating fluorophores per bound complex.

## Answer

A is the most direct comparison because it matches initial target engagement, rather than a proxy for it.

The biological question is whether the label changes the organization of the protein being observed. Before comparing later organization, the two treatments should engage comparable fractions of neuroligin molecules. Measuring that fraction directly addresses this variable. The shared independent readout then helps distinguish redistribution of neuroligin from differences in how the streptavidin probes themselves appear.

Why occupancy matters: soluble-biotin affinity, the number of available binding sites and the number of occupied target molecules are different quantities. Several active sites grouped on one tetramer can connect biotins on different targets. The same number of active sites distributed among separate monovalent tetramers does not create that connection through biotin binding. Thus, equal initial target coverage can coexist with different capacities to reorganize targets.

If the two labels produce different later organization at matched initial target occupancy, that would support differential probe-induced perturbation. It would not by itself prove that every observed cluster arose through direct bridging, or identify which treatment best reproduces an unlabeled native state.

Why the other matching strategies are less direct:

B addresses a real evidence gap: the printed affinity measurements use tagged A4, while the cell experiment uses wild-type streptavidin. Measuring soluble-biotin binding in the relevant medium would improve that comparison. However, predicted occupancy in a soluble-binding measurement is not measured occupancy of membrane-bound neuroligin. Surface geometry, accessibility, multivalent attachment and the labeling history can change how the probes engage cellular targets. A comparable equilibrium affinity also does not establish identical binding kinetics.

C matches the supply of functional sites. It does not establish how many neuroligin molecules are occupied. It also leaves the sites grouped differently: four on a multivalent complex versus one on each monovalent complex. Equal binding capacity supplied to cells therefore does not remove the biological distinction of interest.

D matches an optical signal. Fluorescence counts fluorophores, rather than target molecules directly. Differences in fluorophores per bound complex, or in the number of targets engaged by each complex, can produce the same intensity with different target coverage. Using identical imaging settings does not supply those missing calibrations.

The distinction is between matching the actual biological variable and matching a convenient measurement related to it. All four strategies can be useful; A most directly controls initial target engagement for the stated comparison.

**Final answer: A**

<details>
<summary>Sources, evidence checks and limitations</summary>

**Source-supported answer: A.** The edited answer selects A and matches that reference.

### Primary evidence

[A monovalent streptavidin with a single femtomolar biotin binding site](https://doi.org/10.1038/nmeth861) (2006).

- Table 1, printed page 268: bound-biotin stoichiometry for A4 and A1D3
- Figure 3b and Results, printed page 269: soluble-biotin affinity measurements
- Figure 4a and Results, printed page 270: initially diffuse and later divergent neuroligin labeling
- Introduction and Discussion: distinction between strong biotin binding and multivalent target crosslinking

The paper supports the affinity, binding-site counts and neuronal labeling observations. Its distinction between affinity and multivalent crosslinking motivates the revised question. The occupancy-matched comparison and independent readout are AI-created follow-up reasoning, not an additional experiment or result reported by the authors.

### Answer limitations

- This is a proposed comparison. No occupancy-matched follow-up or independent-readout outcome is asserted to have been measured.
- An independent readout must itself avoid linking or substantially perturbing the targets. No particular implementation is assumed.
- Matched occupancy can test differential perturbation, but does not establish which condition reproduces native organization; a suitable independent baseline would be needed.
- The comparison does not isolate every difference between preparations or prove the molecular origin of every cluster.

### Source qualifications

- The affinity data compare tagged A4 with A1D3. The published neuronal experiment compares wild-type streptavidin with A1D3; that distinction is explicit in the question.
- A1D3 is monovalent and tetrameric. Functional valency, oligomeric assembly, equilibrium affinity and target occupancy are separate properties.
- The question concerns transfected acceptor-peptide-tagged neuroligin-1. It does not claim the same outcome for every native receptor.

### Evidence review and revision provenance

- All four strategies share the same downstream organization readout; no option is singled out merely by measuring that endpoint.
- Rejected choices are compatible with the printed observations. They rely on soluble binding, supplied site concentration or fluorescence as an insufficiently calibrated proxy for occupied targets.
- An independent solver given only the final question selected A and found no material ambiguity.
- Question difficulty and benefit for model training have not been measured.

This question and explanation were AI-edited after source review. They are source-aware revisions, not unchanged teacher responses or a new blinded generation. Assistant review passed for the frozen revision; this is not expert human validation or evidence of a training gain. No new teacher API request was made for the revision.

[Revised question](artifacts/example-09/revised_question.json) · [Revised answer and source label](artifacts/example-09/revised_answer.json) · [Original earlier question and answer](artifacts/example-09/original_presentation.md) · [Original generation request for the earlier question](artifacts/example-09/request.json) · [Unchanged original output for the earlier question](artifacts/example-09/generated_output.json) · [Revision record](revision_v2.json)

</details>

---

# 10. What does a proximity-labeling ratio measure?

## Question

Cho and colleagues used split-TurboID targeted to contacts between the endoplasmic reticulum and mitochondria. They compared the recovered proteins with a reference made using full-length TurboID in the cytosol.

The contact-targeted samples were labeled for four hours; the cytosolic-reference samples for one minute. The authors chose these different durations because the enzymes had different activities. Under those conditions, the preparations gave comparable overall signals for biotinylated proteins.

Proteins were first compared with an omit-added-biotin control, then filtered using their contact-targeted/cytosolic-reference enrichment ratios. The latter threshold was calibrated using a reference list of cytosolic proteins and the paper's 10% false-discovery criterion.

Consider a hypothetical protein P that reproducibly exceeds the omit-biotin background but fails the cytosolic-reference filter. No protein-specific labeling kinetics or independent localization measurements are available for P.

**Question:** Which interpretation best explains what this comparison establishes?

- **A.** Dividing P's contact-targeted signal by 240 would compensate for the unequal labeling durations. The adjusted ratio could estimate its relative contact-encounter rate, although direct molecular binding would remain unproven.
- **B.** P failed a comparison of accumulated labeling under these conditions. A cytosolic pool could depress its ratio even if P visits contacts, and covalent labels can persist after movement; matching bulk signal does not calibrate P's labeling kinetics or contact occupancy.
- **C.** Matching overall labeling compensates for the enzymes' different activities. P's ratio can therefore estimate its relative contact occupancy; failure favors predominantly cytosolic localization, although brief visits to contacts would remain possible.
- **D.** Calibrating the threshold with cytosolic reference proteins supplies an error probability for each candidate. A passing protein would have at most a 10% probability of being a false contact hit; P's failure chiefly reflects insufficient statistical confidence rather than compartment-dependent labeling.

## Answer

B gives the interpretation supported by this comparison: P did not pass a condition-specific enrichment filter on accumulated labeling.

What is measured: proximity labeling produces covalent modifications on accessible proteins near an active enzyme. Recovery therefore reflects a history of labeling, rather than a direct count of how many molecules occupy a contact at the moment of collection. A protein can acquire a label during a visit and move elsewhere while retaining it. Label persistence is subject to protein turnover and other biological processes; it is not permanent by definition.

What the cytosolic reference adds: the comparison favors proteins recovered more strongly from contact-targeted labeling than from the cytosolic reference. A protein with both a contact-associated pool and a substantial cytosolic pool can be labeled in both conditions. Strong cytosolic-reference labeling can reduce its ratio even when genuine contact association occurs. The paper explicitly discusses loss of such dual-localized proteins through this filtering approach.

Why the unequal durations matter: four hours and one minute sample different histories of protein movement and enzyme exposure. The two preparations also use different enzyme forms and locations. Comparable overall biotinylation establishes a bulk comparison, not a separate calibration for each protein. Local accessibility, enzyme exposure, abundance, movement and potential saturation can all affect a particular protein's recovered signal.

A introduces an unsupported kinetic correction. Four hours is 240 minutes, but dividing the contact-targeted signal by 240 only estimates a rate under additional assumptions about linear signal accumulation and relevant enzyme activity. Those assumptions are not established for P. A simple time correction therefore cannot recover its encounter rate from these endpoints.

C extends bulk matching into an individual localization measurement. Equal total signal can arise from different distributions of labeling across proteins and time. It does not convert P's ratio into a fraction of molecules, or a fraction of time, at contacts.

D turns reference-set calibration into an individual error probability. The paper's cutoff uses recovery of specified reference false-positive proteins. That procedure does not assign a probability of incorrect localization to each candidate, and failing the filter is not itself an estimate of statistical confidence about P's compartment.

P's result is compatible with several biological histories. It does not establish absence from contacts, contact residence time, the size of a contact-associated pool, or direct molecular binding. The supported conclusion remains its failure to meet this particular relative-labeling criterion.

**Final answer: B**

<details>
<summary>Sources, evidence checks and limitations</summary>

**Source-supported answer: B.** The edited answer selects B and matches that reference.

### Primary evidence

[Split-TurboID enables contact-dependent proximity labeling in cells](https://doi.org/10.1073/pnas.1919528117) (2020).

- Results before Figure 4 and Figure 3F: different enzyme activities, four-hour versus one-minute labeling, and comparable overall biotinylation
- Figure 4A-C: labeling conditions and sequential omit-biotin/cytosolic-reference comparisons
- Methods, Generation of ER-Mitochondria Proteome Lists: reference-protein sets and false-discovery cutoffs
- Results before Validation of ER-Mitochondria Contact Orphans: reduced recovery of contact/cytosol dual-localized proteins

The published assay used different labeling durations to obtain comparable overall biotinylation and applied reference-based enrichment filters. The authors explicitly identify dual-localized contact/cytosol proteins as a source of lost recovery. P is an AI-created hypothetical case; its behavior is used to reason about the assay, not presented as a new observation from the paper.

### Answer limitations

- P is hypothetical. No identity, individual kinetics, localization measurement or numerical enrichment value is supplied.
- The question does not establish how much temporal integration, saturation or any other mechanism affected an actual protein. Those are relevant possibilities, not measured explanations for P.
- The ratio is an assay-condition-dependent enrichment measure; it is not a calibrated contact-occupancy fraction or encounter rate.
- The reference-set false-discovery criterion does not establish a per-protein posterior error probability.

### Source qualifications

- The enzymes differ in activity and spatial distribution. Matching bulk labeling does not establish matched protein-specific kinetics or equal-duration sampling.
- The original reported counts remain in the archived first version. They were removed from this question because selecting the answer should not depend on copying retained-list counts.
- The original paper used reference-protein false-discovery cutoffs, not a rule retaining exactly 97 proteins per replicate.
- Proximity enrichment does not establish direct binding, physical membrane tethering or exclusive localization.

### Evidence review and revision provenance

- The stem no longer tells the solver to name an excluded genuine protein or states the correct interpretation of unequal durations.
- All distractors preserve the reported observations. Their errors involve time normalization, bulk-to-protein calibration or reference-set-to-individual probability inference.
- An independent solver given only the final question selected B and found no material ambiguity.
- This is an experimental-interpretation exercise; its difficulty and training benefit have not been measured.

This question and explanation were AI-edited after source review. They are source-aware revisions, not unchanged teacher responses or a new blinded generation. Assistant review passed for the frozen revision; this is not expert human validation or evidence of a training gain. No new teacher API request was made for the revision.

[Revised question](artifacts/example-10/revised_question.json) · [Revised answer and source label](artifacts/example-10/revised_answer.json) · [Original earlier question and answer](artifacts/example-10/original_presentation.md) · [Original generation request for the earlier question](artifacts/example-10/request.json) · [Unchanged original output for the earlier question](artifacts/example-10/generated_output.json) · [Revision record](revision_v2.json)

</details>
