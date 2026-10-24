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

Source identity: **APEX peroxidase** — [UniProt Q43758](https://www.uniprot.org/uniprotkb/Q43758/entry).

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

</details>


---

# 2. Adenylate kinase: a conservative substitution can impair catalysis

## Question

Wild-type protein: Adenylate kinase (Escherichia coli K-12).
Full canonical wild-type sequence, numbered from the initial methionine as residue 1:

```text
MRIILLGAPGAGKGTQAQFIMEKYGIPQISTGDMLRAAVKSGSELGKQAKDIMDAGKLVTDELVIALVKE
RIAQEDCRNGFLLDGFPRTIPQADAMKEAGINVDYVLEFDVPDELIVDRIVGRRVHAPSGRVYHVKFNPP
KVEGKDDVTGEELTTRKDDQEETVRKRLVEYHQMTAPLIGYYSKEAEAGNTKYAKVDGTKPVAEVRADLE
KILG
```


Published variant(s): R156K.

Experimental evidence:
Published ATP-dependent kinetic measurements (central values; kcat in s^-1, ATP Km in micromolar):
WT: kcat 330, Km 71.
R156K: kcat 0.74, Km 52.
Arginine and lysine both normally carry a positive side-chain charge near neutral pH.

**Question:** Which interpretation best explains why calling R156K a conservative substitution does not establish functional conservation?

**Choices:**

- **A.** The lower ATP Km compensates for the turnover loss, so R156K should retain near-WT catalytic efficiency when ATP is limiting.
- **B.** The lower ATP Km establishes stronger equilibrium ATP binding, so the turnover defect must arise entirely from slower product release.
- **C.** The roughly 450-fold turnover loss with a modest Km shift shows that retaining positive charge need not preserve residue-specific catalytic performance.
- **D.** The roughly 450-fold turnover loss directly measures a 450-fold reduction in correctly folded protein, while catalysis by the folded molecules remains unchanged.

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.

## Answer

The best interpretation is C: chemical similarity does not guarantee functional conservation.

1. Quantitative evidence
The turnover decrease is:
330 / 0.74 ≈ 446-fold.
Thus, R156K has roughly 450-fold lower reported kcat than WT. In contrast, its ATP Km decreases only modestly:
52 / 71 ≈ 0.73,
a decrease of about 27%.

At ATP concentrations well below both Km values, with other assay conditions fixed, the rate per enzyme is approximately (kcat/Km)[ATP]. The relevant catalytic efficiencies are:
• WT: 330/71 ≈ 4.65 s^-1 μM^-1.
• R156K: 0.74/52 ≈ 0.0142 s^-1 μM^-1.

The mutant therefore retains only about 0.31% of WT ATP-dependent catalytic efficiency, a roughly 327-fold loss. The modest Km decrease does not compensate for the turnover defect, ruling out A.

2. Why a charge-conserving substitution can strongly impair function
Arginine and lysine are both normally positively charged near neutral pH, making this substitution conservative in a broad chemical classification. However, arginine's guanidinium group and lysine's terminal ammonium group differ in geometry, charge distribution, and hydrogen-bonding arrangements. In an enzyme, these differences can affect substrate positioning, transition-state stabilization, or conformational steps during turnover. These are general mechanistic possibilities, not specific interactions established for residue 156 by the supplied sequence. The observed kinetic loss nevertheless demonstrates that preserving positive charge does not preserve this variant's catalytic performance.

3. Why the other interpretations are unsupported
B incorrectly equates Km with an equilibrium dissociation constant. Even in the simple mechanism E + S ⇌ ES → E + P, Km = (koff + kcat)/kon, whereas Kd = koff/kon. Consequently, a lower Km can accompany slower turnover without stronger equilibrium binding. Adenylate kinase has a more complex, multisubstrate catalytic cycle, so the ATP Km likewise cannot automatically be interpreted as ATP binding affinity. Nothing supplied identifies slower product release as the sole cause of the turnover loss.

D incorrectly treats kcat as a direct measurement of folding. A lower reported kcat can reflect changes in chemistry or other turnover-limiting steps; depending on enzyme normalization, an inactive fraction can also affect apparent turnover. These measurements do not establish a 450-fold reduction in correctly folded protein or unchanged catalysis by the folded molecules.

Thus, the strong turnover defect with only a modest Km shift supports C.

**Final answer: C**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

Primary full-text Results and a kinetic table support the reported measurements and fold-change calculations. General side-chain chemistry helps interpret them; a specific structural cause is not established by the table.

### Answer limitations

The conclusion applies to the supplied ATP-dependent kinetic measurements. Neither the sequence nor these kinetic parameters uniquely identify the affected microscopic step, establish equilibrium ATP affinity, or quantify the folded or active protein fraction.

### References and source review

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to AI remain visible above.

Source identity: **adenylate_kinase** — [UniProt P69441](https://www.uniprot.org/uniprotkb/P69441/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

Correct remapped answer C. Correctly calculates about 446-fold lower turnover, about 327-fold lower ATP-dependent catalytic efficiency, and a 27% Km decrease. Connects the shared positive charge to different guanidinium/ammonium geometry and hydrogen bonding without claiming specific Arg156 contacts were observed. Correctly distinguishes Km from Kd, and treats changes in chemistry, conformational steps, product release and active fraction as possibilities rather than measured causes.

Source support:

- 2021 Figure 2c / Table S2; 2023 Table 1, WT and R156K rows.
- Published ATP-dependent kinetic measurements (central values; kcat in s^-1, ATP Km in micromolar):
WT: kcat 330, Km 71.
R156K: kcat 0.74, Km 52.
Arginine and lysine both normally carry a positive side-chain charge near neutral pH.
- Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.
- Table 1, footnote a.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. Published R36, R88, R123, R156 and R167 all match the reference residues.
- The prompt supplies the verified canonical reference and published mutation labels. No unreported affinity tag, cloning scar or exact expressed-construct extension is inferred.

Primary references:

- [Dynamic Connection between Enzymatic Catalysis and Collective Protein Motions](https://pmc.ncbi.nlm.nih.gov/articles/PMC8297476/). Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.

- [Mechanistic basis for a connection between the catalytic step and slow opening dynamics of adenylate kinase](https://pmc.ncbi.nlm.nih.gov/articles/PMC11779523/). Table 1, footnote a.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.

[Original source records and unchanged AI output](../astra_enzyme_mutation_pool_2026-10-23/examples/case-004.md)

</details>


---

# 3. PafA: inactive protein fraction versus inhibitor binding

## Question

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
The published H83G variant has a lower Pi inhibition constant than wild type, meaning stronger phosphate binding. The inhibition readout is a fractional rate v(I)/v(0) for the same variant. In a simple model with a long-lived inactive fraction, only the active population reacts and binds inhibitor, and its concentration multiplies both v(I) and v(0) by the same factor. There is no interconversion of populations during the measurement.

**Question:** Can a smaller active population alone explain the changed normalized inhibition constant?

**Choices:**

- **A.** The inactive population changes the fitted inhibition constant because normalization removes enzyme concentration only from the uninhibited rate, leaving inhibitor-dependent population effects.
- **B.** Cancellation of the active-enzyme factor shows that H83G stabilizes the catalytic transition state more strongly, so stronger inhibition establishes faster intrinsic chemistry.
- **C.** A smaller active population lowers the inhibitor concentration needed to halve its fractional rate, so inactive abundance alone can explain stronger apparent binding.
- **D.** The common active-enzyme factor cancels from the fractional rate; the changed inhibition constant therefore requires more than uniform dilution by inactive protein.

## Answer

The reference confirms histidine at canonical position 83, the site of H83G. This identifies the substitution but does not, by itself, establish its effect on phosphate binding or catalysis. The decisive evidence is the normalized inhibition measurement and the supplied population model.

Let E_total be total enzyme concentration, f the fixed fraction belonging to the active population, and r(I) the rate per active enzyme at phosphate concentration I under otherwise identical assay conditions. Inhibition of active enzyme is included in r(I). Then:

v(I) = f E_total r(I)
v(0) = f E_total r(0)
v(I)/v(0) = r(I)/r(0).

Both the active fraction and total enzyme concentration cancel. If H83G changed only the abundance of inactive protein, its per-active-enzyme response r(I) would remain unchanged. Absolute rates would decrease, but the normalized inhibition curve—and therefore its fitted inhibition constant—would not shift. In particular, the phosphate concentration giving half of the uninhibited fractional rate would remain unchanged.

Consequently, the reported lower Pi inhibition constant requires more than uniform dilution by inactive protein. Within the stated model, it reflects an altered inhibition/binding response of the active population.

A is incorrect because the active-enzyme factor appears in both rates and cancels from their ratio. C is incorrect because decreasing active abundance alone cannot shift fractional half-inhibition. B correctly invokes cancellation but adds an unsupported conclusion: stronger binding of phosphate, a product inhibitor, does not establish greater catalytic transition-state stabilization or faster intrinsic chemistry. D states the justified conclusion.

**Final answer: D**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

Cached primary full-text Results and Figure 6B support stronger phosphate binding for H83G. Cancellation of the active-enzyme fraction is a mathematical derivation from the fixed-population assumptions supplied in the question, not a separate measured result.

### Answer limitations

The conclusion applies to the supplied fixed-population model. A reduced active fraction could coexist with stronger phosphate binding, but cannot alone explain the normalized inhibition shift. The evidence does not identify the molecular cause of the binding change or establish effects on expression, stability, or intrinsic chemistry.

### References and source review

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to AI remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- The active-fraction and enzyme-concentration factors cancel correctly from v(I)/v(0); the solution distinguishes an absolute-rate change from a normalized inhibition-curve shift.
- The conclusion is explicitly conditional on fixed, noninterconverting populations. It allows reduced active abundance to coexist with altered binding and does not infer faster chemical catalysis.
- His83 and canonical83 to expressed-ORF64 indexing are correct. The explanation uses the provided binding result and population model rather than asserting a sequence-only affinity prediction.

Source support:

- Fig.6B, FC2/FC3 section; Fig.3D model
- H83G is the representative strengthened-Pi-binding(FC2) mutant; the study separates long-lived inactive fractions from catalytic/binding effects.

Source qualifications:

- The result is conditional on the stated noninterconverting inactive-state model and normalization.
- Do not assume every inactive conformation cannot bind phosphate in all possible biological systems.
- Expression and assay conditions are distinct. These standard on-chip conditions are not assigned to separate off-chip or tagless measurements without explicit source support.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Revealing enzyme functional architecture via high-throughput microfluidic enzyme kinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454890/). Fig.6B, FC2/FC3 section; Fig.3D model

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.

[Original source records and unchanged AI output](../astra_enzyme_mutation_pool_2026-10-23/examples/case-015.md)

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

The strongest evidence is residues 193–214, ILLVILGIIVVIAILTAIAFFV. This 22-residue stretch is strongly hydrophobic and contains no charged residues. Its length and composition are appropriate for an alpha helix spanning a lipid bilayer; such helices commonly contain roughly 18–25 predominantly hydrophobic residues. Only KGH at positions 215–217 follows it, so the candidate anchor lies very close to the protein's C terminus.

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

# 9. Binding affinity versus valency and probe-induced clustering

## Question

Streptavidin is used to attach labels to biotinylated proteins. Compare these published observations. A4 is a tetramer of four active, His-tagged subunits; A1D3 is a tetramer containing one active and three binding-inactive subunits. The affinity measurements below use these tagged preparations, whereas the cellular comparison uses wild-type streptavidin versus A1D3.

| Preparation | Biotins bound per tetramer | Biotin Kd, mean ± SEM |
|---|---|---|
| A4 | 4 | (4.4 ± 1.1) × 10^-14 M |
| A1D3 | 1 | (4.8 ± 0.5) × 10^-14 M |

In cultured neurons expressing acceptor-peptide-tagged neuroligin-1, both fluorescent labels initially gave diffuse surface labeling. Two hours later, wild-type streptavidin produced strong clustering, whereas A1D3 labeling remained predominantly diffuse.

**Question:** Which explanation best reconciles the binding measurements with the cellular labeling pattern?

- **A.** A1D3 retains strong binding at its remaining site but has fewer sites for bridging labeled proteins; affinity and crosslinking capacity can therefore separate.
- **B.** A1D3 retains four-site bridging but has substantially weaker binding at every site; reduced occupancy therefore explains the predominantly diffuse labeling.
- **C.** A1D3 loses tetramer assembly and its neighboring-subunit support for binding; monomer formation therefore explains the reduced cellular clustering.
- **D.** A1D3 retains four functional binding sites because its Kd is similar to A4; the Kd measurement therefore establishes equivalent crosslinking capacity.

## Answer

A best reconciles the observations because binding affinity and binding valency are different properties.

Measured binding: A4 binds four biotins per tetramer, whereas A1D3 binds only one. Nevertheless, their biotin Kd values—(4.4 ± 1.1) × 10^-14 M and (4.8 ± 0.5) × 10^-14 M, respectively—are very similar. These measurements support retention of strong binding at A1D3’s remaining functional site, rather than substantial weakening of that site. Similar Kd values do not imply equal numbers of functional binding sites.

Biological mechanism: Kd describes equilibrium binding affinity. Crosslinking instead requires a reagent to engage at least two distinct target molecules simultaneously. Wild-type streptavidin has multiple functional biotin-binding sites and can therefore bridge biotinylated surface proteins. A1D3 remains tetrameric, but its single functional site cannot directly bridge two biotinylated proteins through biotin binding.

Connection to the cellular observations: Both labels can bind biotinylated neuroligin-1, explaining why both initially label the surface. The strong clustering observed after two hours with wild-type streptavidin is consistent with its multivalent crosslinking capacity. Predominantly diffuse A1D3 labeling is consistent with high-affinity attachment without direct bridging of separate labeled proteins.

Why the alternatives fail:
• B contradicts both the one-biotin-per-tetramer measurement and the similar measured affinities.
• C contradicts the stated tetrameric assembly of A1D3; reduced functional valency does not require monomer formation.
• D confuses affinity with valency. A similar Kd cannot establish four functional sites or equivalent crosslinking capacity, and the measured binding stoichiometry explicitly shows only one functional site in A1D3.

**Final answer: A**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Primary evidence

[A monovalent streptavidin with a single femtomolar biotin binding site](https://doi.org/10.1038/nmeth861) (2006).

- Table 1: bound-biotin stoichiometry; printed page 268
- Figure 3b and Results: biotin affinity; printed page 269
- Figure 4a and Results: initial versus two-hour AP-neuroligin-1 labeling; printed page 270

Table 1 establishes one bound biotin per A1D3 tetramer versus four for A4; Figure 3b gives comparable femtomolar site affinity. Figure 4a shows that the multivalent cellular label clusters tagged neuroligin whereas A1D3 does not to the same extent. Reduced capacity to bridge targets, rather than a large affinity loss or monomerization, reconciles these observations.

### Answer limitations

The affinity measurements compare tagged A4 and A1D3, whereas the neuronal experiment compares wild-type streptavidin with A1D3. The reported Kd values therefore do not directly establish wild-type affinity under cellular conditions or cellular binding kinetics. The labeling pattern is consistent with differential crosslinking capacity but does not directly reveal every molecular step of clustering.

### Source qualifications

- Canonical P22629 is the native 183-residue precursor, not the exact mature, tagged assayed subunit.
- A1D3 is monovalent but remains tetrameric. A4 affinity measurements involve His-tagged active subunits; the cellular multivalent comparison is wild-type streptavidin.
- No canonical-to-assay residue-number mapping or new mutation recipe is supplied.
- The neuronal target is a transfected acceptor-peptide-tagged neuroligin-1 construct; the observations do not establish universal effects on every native receptor.

### Evidence review

- Correctly separates equilibrium affinity, functional valency, oligomeric assembly and cellular clustering.
- Reproduces both Kd estimates and their errors correctly; treats them as comparable, without an unsupported claim of formal statistical equivalence.
- Correctly states that a single functional biotin-binding site cannot directly bridge two biotinylated targets through biotin binding, while the complex remains tetrameric.
- Connects the stated initially diffuse and two-hour divergent labeling patterns to multivalent bridging using appropriately qualified language.
- Explicitly distinguishes tagged A4 affinity measurements from wild-type cellular comparison and avoids inferring cellular binding kinetics from those Kd measurements.
- All three rejected alternatives are refuted by supplied measurements or the stated tetrameric construction.

Both the primary-source facts and this answer were reviewed by assistants. No material errors were found. This is not expert human validation or evidence of a training gain. Full author-copy PDFs were inspected; they are not redistributed here. No protein sequence, private gold label or full paper was supplied to the AI for this question.

[Exact generation request](artifacts/example-09/request.json) · [Unchanged generated output](artifacts/example-09/generated_output.json)

</details>


---

# 10. Background controls, compartment references and dual localization

## Question

Split-TurboID was used to label proteins near contacts between the endoplasmic reticulum (ER) and mitochondria in human cells. Its fragments were attached separately to the ER membrane and the outer mitochondrial membrane. Nearby proteins were recovered for mass spectrometry. The authors used these sequential comparisons:

| Stage | Reference sample | Proteins retained in two independent +rapamycin replicates |
|---|---|---|
| Filter 1 | Split-TurboID with added biotin omitted | 607 and 619 |
| Filter 2 | Full-length TurboID in the cytosol, after filter 1 | 97 and 97 |
| Intersection of the filtered replicates | Both replicates | 67 |

Split-TurboID samples were labeled for four hours; full-length TurboID samples for one minute. These are enrichment comparisons under the published conditions, not equal-duration catalytic-rate measurements.

**Question:** What does the cytosolic-reference filter add, and what kind of genuine contact-associated protein could it exclude?

- **A.** It removes biotin-independent capture rather than cytosolic labeling; therefore a protein present in both contact sites and cytosol should always be retained.
- **B.** It favors contact-site labeling over cytosolic labeling; therefore a genuine contact-associated protein may be lost if it also labels strongly in the cytosol.
- **C.** It favors general cytosolic labeling over contact-site labeling; therefore abundant cytosolic proteins should become more prominent in the final contact-site list.
- **D.** It identifies direct binding between the two organelle membranes; therefore a retained protein is established as a physical tether that holds those membranes together.

## Answer

B is correct: the cytosolic-reference filter favors contact-site labeling over general cytosolic labeling, but can exclude genuine contact-associated proteins that also label strongly in the cytosol.

Reported observations: The no-added-biotin comparison retained 607 and 619 proteins. The subsequent cytosolic-reference comparison reduced these lists to 97 proteins each, with 67 shared between replicates. These numbers document progressively more selective enrichment and reproducibility criteria; they do not establish that every excluded protein was a false positive.

What each filter adds: TurboID biotinylates nearby accessible proteins, so recovery reflects proximity-dependent labeling as well as factors such as protein abundance and exposure to the enzyme. Filter 1 addresses background recovery present without added biotin, including nonspecific capture and pre-existing biotinylation. It does not by itself establish contact-site specificity. Filter 2 adds a spatial-enrichment criterion: candidates must be preferentially labeled by contact-targeted split-TurboID relative to cytosolic full-length TurboID. It therefore reduces inclusion of proteins that are readily labeled in the general cytosolic environment.

Potential genuine exclusion: A peripheral contact-associated protein could have both a contact-localized pool and a substantial soluble cytosolic pool. Alternatively, it could visit contacts only transiently. If its cytosolic-reference labeling is strong, its genuine contact-site signal may not be sufficiently enriched to pass filter 2. Such a protein is not necessarily absent from contacts; it fails the relative-enrichment criterion.

Assay interpretation: Split-TurboID labeling lasted four hours, whereas full-length TurboID labeling lasted one minute. The filter compares enrichment under those specific conditions, not equal-duration catalytic rates. Proximity labeling also does not demonstrate direct molecular binding or a functional membrane-tethering role.

Why the other choices fail: A confuses the cytosolic-reference filter with the no-added-biotin control and incorrectly guarantees retention of dual-localized proteins. C reverses the direction of enrichment. D mistakes proximity evidence for proof of direct binding and physical tethering.

**Final answer: B**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Primary evidence

[Split-TurboID enables contact-dependent proximity labeling in cells](https://doi.org/10.1073/pnas.1919528117) (2020).

- Figure 3A and Results: complementary fragments targeted to opposing organelle membranes
- Figure 4A: four-hour split-TurboID versus one-minute full-length TurboID labeling
- Figure 4B: 607/619 after filter 1, 97/97 after filter 2, and 67 intersected +rapamycin hits
- Figure 4B–C and Results, printed page 12147: omit-biotin versus cytosolic references
- Results, printed page 12147, paragraph before Validation of ER–Mitochondria Contact Orphans: reduced recovery of dual-localized contact/cytosol proteins

Figure 4B contrasts added-biotin labeling with the omit-biotin baseline, then contrasts contact-site labeling with a cytosolic TurboID reference. The second comparison selects relative contact enrichment rather than generic labeling strength. The Results explicitly explain that ratiometric filtering can remove genuine proteins dual-localized to contacts and cytosol. Proximity labeling alone does not identify direct tethers.

### Answer limitations

Individual protein enrichments and filtering thresholds are not provided, so the identities and number of genuine contact-associated proteins excluded cannot be determined. The unequal labeling durations also prevent interpreting these comparisons as measurements of intrinsic catalytic rates.

### Source qualifications

- P06709 is the canonical native BirA backbone used for private source-exclusion screening, not the complete evolved split-TurboID fragments with tags, localization elements and dimerization domains.
- The question interprets an already published assay and filtering comparison; it supplies neither novel variants nor engineering instructions.
- Enrichment and specificity depend on the reported conditions; the unequal labeling times do not support a direct catalytic-rate comparison.
- Surviving proteins are proximity-enriched candidates. Neither membership nor absence establishes direct binding, membrane tethering or exclusive localization.
- The displayed counts are the +rapamycin replicate filtering path only; they are not the full union of +rapamycin and omit-rapamycin datasets.

### Evidence review

- Correctly reproduces the +rapamycin path 607/619 to 97/97 and intersection 67, without conflating excluded proteins with false positives.
- Correctly separates omit-added-biotin background comparison from cytosolic-reference spatial enrichment.
- Correctly explains the documented loss of genuine contact/cytosol dual-localized proteins through a relative enrichment threshold.
- Labels a transient-contact scenario as a possible exclusion mechanism, not a paper-measured example.
- Correctly preserves the four-hour split versus one-minute full-length caveat and does not infer intrinsic catalytic rates.
- Correctly distinguishes proximity enrichment from direct physical binding or functional tether proof.
- Correctly rejects A, C and D without requiring hidden source facts.

Both the primary-source facts and this answer were reviewed by assistants. No material errors were found. This is not expert human validation or evidence of a training gain. Full author-copy PDFs were inspected; they are not redistributed here. No protein sequence, private gold label or full paper was supplied to the AI for this question.

[Exact generation request](artifacts/example-10/request.json) · [Unchanged generated output](artifacts/example-10/generated_output.json)

</details>
