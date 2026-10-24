# Enzyme and mutation questions — no answers

All frozen candidate questions are included in their original order. Each displays the full reference sequence, all supplied variant/assay facts and the four choices. No generated solution, reference label or post-generation source evidence appears in this file. Sequences are line-wrapped; questions.jsonl preserves exact prompts.

---

# case-001 — APEX peroxidase

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

- **A.** Only the higher-guaiacol condition shows an APEX2 advantage; the lower-guaiacol condition gives the same inhibition threshold for both enzymes.
- **B.** Both substrate conditions show a higher peroxide-inhibition threshold for APEX2, with unchanged thresholds when guaiacol concentration changes.
- **C.** Both substrate conditions show a higher peroxide-inhibition threshold for APEX2, with the threshold also depending on guaiacol concentration.
- **D.** Both substrate conditions give the same peroxide-inhibition threshold for APEX and APEX2, despite different guaiacol concentrations.


---

# case-002 — PTEN phosphatase

Reference protein sequence (P60484, full canonical wild-type backbone; coordinate reference only):

```text
MTAIIKEIVSRNKRRYQEDGFDLDLTYIYPNIIAMGFPAERLEGVYRNNIDDVVRFLDSKHKNHYKIYNL
CAERHYDTAKFNCRVAQYPFEDHNPPQLELIKPFCEDLDQWLSEDDNHVAAIHCKAGKGRTGVMICAYLL
HRGKFLKAQEALDFYGEVRTRDKKGVTIPSQRRYVYYYSYLLKNHLDYRPVALLFHKMMFETIPMFSGGT
CNPQFVVCQLKVKIYSSNSGPTRREDKFMYFEFPQPLPVCGDIKVEFFHKQNKMLKKDKMFHFWVNTFFI
PGPEETSEKVENGSLCDQEIDSICSIERADNDKEYLVLTLTKNDLDKANKDKANRYFSPNFKVKLYFTKT
VEEPSNPEASSSTSVTPDVSDNEPDHYRYSDTTDSDPENEPFDEDQHTQITKV
```


All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.

Published variants: C124S.

Supplied experimental observations:
- In a published yeast growth-rescue assay that reports PTEN lipid-phosphatase-associated function, wild-type PTEN rescues growth whereas C124S does not.
- In a separate published VAMP-seq experiment in cultured human cells, C124S has a normalized abundance score of 1.14 and falls in the wild-type-like abundance class. This is an abundance score, not a catalytic rate or a fold-change.
- The two results come from different experimental systems; no same-system protein-normalized catalytic rate is supplied.

**Question:** Which interpretation best combines these two measurements?

- **A.** C124S has wild-type-like human-cell abundance but fails yeast rescue; normal accumulation and successful functional rescue are distinct outcomes across these assays.
- **B.** C124S retains functional rescue despite low abundance in human cells, indicating that improved catalytic performance compensates for reduced protein accumulation.
- **C.** C124S has a catalytic score of 1.14 in human cells, so the growth result measures a decrease in protein abundance rather than function.
- **D.** C124S has reduced human-cell abundance and reduced yeast rescue, making deficient protein accumulation the directly measured common outcome in both experimental systems.


---

# case-003 — PafA alkaline phosphatase

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
In wild-type PafA, Thr79 attacks the substrate phosphate and forms a covalent phospho-enzyme intermediate. The published T79G variant was used as a catalytically inactive control. Its eGFP signal showed that protein was expressed, and empty chambers were also retained to monitor local assay background.

**Question:** Which interpretation best connects the sequence change to the biochemical control?

- **A.** Comparable eGFP abundance makes remaining background activity an adequate estimate of intrinsic mutant turnover, provided the same normalization is applied to wild type.
- **B.** Removing Thr79's side-chain hydroxyl disrupts the usual covalent intermediate; an expression reporter does not demonstrate catalytic competence of the expressed PafA.
- **C.** T79G mainly reduces the amount of folded enzyme; matched eGFP abundance therefore isolates a selective folding defect rather than a catalytic defect.
- **D.** T79G primarily weakens phosphate-product binding; the reported loss of turnover therefore establishes product release as the rate-limiting step in the mutant.


---

# case-004 — adenylate_kinase

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

- **A.** The lower ATP Km compensates for the turnover loss, so R156K should retain near-WT catalytic efficiency when ATP is limiting.
- **B.** The lower ATP Km establishes stronger equilibrium ATP binding, so the turnover defect must arise entirely from slower product release.
- **C.** The roughly 450-fold turnover loss with a modest Km shift shows that retaining positive charge need not preserve residue-specific catalytic performance.
- **D.** The roughly 450-fold turnover loss directly measures a 450-fold reduction in correctly folded protein, while catalysis by the folded molecules remains unchanged.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.


---

# case-005 — Biotin ligase

Reference protein sequence (canonical wild-type backbone; coordinate reference only):

```text
MKDNTVPLKLIALLANGEFHSGEQLGETLGMSRAAINKHIQTLRDWGVDVFTVPGKGYSLPEPIQLLNAK
QILGQLDGGSVAVLPVIDSTNQYLLDRIGELKSGDACIAEYQQAGRGRRGRKWFSPFGANLYLSMFWRLE
QGPAAAIGLSLVIGIVMAEVLRKLGADKVRVKWPNDLYLQDRKLAGILVELTGKTGDAAQIVIGAGINMA
MRRVEESVVNQGWITLQEAGINLDRNTLAAMLIRELRAALELFEQEGLAPYLSRWEKLDNFINRPVKLII
GDKEIFGISRGIDKQGALLLEQDGIIKPWMGGEISLRSAEK
```


Reference: P06709. All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded. The sequence is not the complete tagged assay construct.

Published variant identities:
BioID, paper construct definition: substitutions R118G; deletions delete 146–146.
TurboID: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V, K194I, M241T, S263P; deletions delete 146–146.

Supplied assay observations:
- Expression-normalized cellular blot comparisons report nearly comparable biotinylated product for TurboID at 10 minutes and older ligases including BioID at 18 hours.
- Quantitation excludes the ligase self-biotinylation band. These are cellular product endpoints, not purified-enzyme turnover measurements.

**Question:** Which interpretation correctly combines the timing and readout information?

- **A.** Normalizing the cellular endpoints converts the 108-fold duration difference into a direct measurement of the purified turnover-number ratio.
- **B.** Expression normalization makes the comparison time-matched, so both variants reach the reported product endpoint after the same accumulation window.
- **C.** TurboID accumulates similar normalized product sooner; the cellular endpoint comparison does not directly measure the purified turnover-number ratio.
- **D.** TurboID appears faster because the normalized product signal includes only the ligase self-biotinylation band rather than nearby-protein labeling.


---

# case-006 — Glucokinase / hexokinase-4

Reference protein sequence (P35557, full canonical wild-type backbone; coordinate reference only):

```text
MLDDRARMEAAKKEKVEQILAEFQLQEEDLKKVMRRMQKEMDRGLRLETHEEASVKMLPTYVRSTPEGSE
VGDFLSLDLGGTNFRVMLVKVGEGEEGQWSVKTKHQMYSIPEDAMTGTAEMLFDYISECISDFLDKHQMK
HKKLPLGFTFSFPVRHEDIDKGILLNWTKGFKASGAEGNNVVGLLRDAIKRRGDFEMDVVAMVNDTVATM
ISCYYEDHQCEVGMIVGTGCNACYMEEMQNVELVEGDEGRMCVNTEWGAFGDSGELDEFLLEYDRLVDES
SANPGQQLYEKLIGGKYMGELVRLVLLRLVDENLLFHGEASEQLRTRGAFETRFVSQVESDTGDRKQIYN
ILSTLGLRPSTTDCDIVRRACESVSTRAAHMCSAGLAGVINRMRESRSEDVMRITVGVDGSVYKLHPSFK
ERFHASVRRLTPSCEITFIESEEGSGRGAALVSAVACKKACMLGQ
```


All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.

Published variants: W99R.

Supplied experimental observations:
- A published human glucokinase study used a yeast complementation assay in which growth depends on the supplied human enzyme supporting glucose metabolism.
- Under the same tested glucose condition, the W99R variant supports greater growth than wild-type glucokinase.
- These observations are a cellular functional readout. The supplied comparison does not separately measure enzyme concentration, turnover number and glucose-binding constants.

**Question:** What does this result show, and what remains unresolved by this readout alone?

- **A.** W99R reduces glucokinase-associated function in this assay; greater growth therefore indicates weaker glucose metabolism rather than improved complementation by the human enzyme.
- **B.** W99R improves functional performance through a measured increase in purified-enzyme turnover; the growth ratio supplies that kinetic ratio independently of protein abundance.
- **C.** W99R improves functional performance through a measured increase in enzyme abundance; the growth ratio supplies that abundance ratio independently of microscopic enzyme kinetics.
- **D.** W99R improves functional performance in this assay; the growth comparison does not separate changes in enzyme abundance from changes in microscopic kinetic steps.


---

# case-007 — PafA alkaline phosphatase

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
For the already tested surface substitutions D473V and D473G, use FC1=(mutant/WT efficiency on MecMUP)/(mutant/WT efficiency on MeP). The published FC1 effect exceeds60-fold for D473V but is less than twofold for D473G. Asp473 lies about20Å from the relevant active-site oxygen-interaction region. If a change in active fraction multiplied both measured efficiencies by the same factor, that factor would cancel in FC1.

**Question:** What follows most directly from these observations?

- **A.** The two substitutions share one distant position, so their different FC1 values primarily reflect total enzyme abundance rather than distinct local perturbations.
- **B.** The greater FC1 effect establishes a gain in absolute diester efficiency; unchanged active-fraction normalization makes that gain independent of monoester activity.
- **C.** The larger FC1 can reflect lower active-enzyme abundance without requiring a difference in the mutation's effects on the two substrates being compared.
- **D.** D473V perturbs the relative substrate responses more strongly; long-range coupling is consistent with this result, while absolute diester enhancement remains unestablished.


---

# case-008 — triosephosphate_isomerase

Wild-type protein: Triosephosphate isomerase (Saccharomyces cerevisiae).
Full canonical wild-type sequence, numbered from the initial methionine as residue 1:

```text
MARTFFVGGNFKLNGSKQSIKEIVERLNTASIPENVEVVICPPATYLDYSVSLVKKPQVTVGAQNAYLKA
SGAFTGENSVDQIKDVGAKWVILGHSERRSYFHEDDKFIADKTKFALGQGVGVILCIGETLEEKKAGKTL
DVVERQLNAVLEEVKDWTNVVVAYEPVWAIGTGLAATPEDAQDIHASIRKFLASKLGDKAASELRILYGG
SANGSNAVTFKDKADVDGFLVGGASLKPEFVDIINSRN
```


Published variant(s): Y208F/Y208A.

Experimental evidence:
Published GAP-isomerization values at pH 7.5 and 25 C (Km based on total GAP): WT kcat = 8900 s^-1, Km = 1.0 mM; Y208A kcat = 740 s^-1, Km = 2.9 mM; Y208F kcat = 13 s^-1, Km = 2.4 mM. Tyrosine-to-phenylalanine removes the phenolic hydroxyl while retaining an aromatic ring; tyrosine-to-alanine also removes that ring.

**Question:** What is the most defensible lesson from comparing the two published substitutions?

- **A.** Y208F turns over about 57 times more slowly than Y208A despite similar Km values; a structurally closer substitution need not have a smaller functional effect.
- **B.** Removing the same hydroxyl produces equivalent catalytic effects; the different turnover values directly establish different folded-protein fractions rather than different catalytic behavior.
- **C.** Retaining the aromatic ring preserves WT catalytic chemistry; the lower Y208F turnover therefore reflects only a loss of equilibrium substrate-binding affinity.
- **D.** Y208F is more catalytically efficient than Y208A because its smaller Km more than compensates for its lower turnover ceiling under substrate-limited conditions.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.


---

# case-009 — APEX peroxidase

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
Dimeric APX-W41F comparator: substitutions W41F; deletions none.

Supplied assay observations:
- APEX2 is more active in cells than APEX and the dimeric APX-W41F comparator.
- Thermal stability and heme binding improve slightly over APEX, but remain below the dimeric comparator; purified assays show stronger peroxide-inhibition resistance for APEX2.

**Question:** Which mechanistic explanation best reconciles the cellular ranking with the independent biochemical comparisons?

- **A.** A heme-binding advantage over the dimeric comparator accounts for the stronger cellular signal observed with APEX2.
- **B.** Cellular activity follows the thermal-stability ranking across the variants, making the peroxide-tolerance comparison consistent with that same ranking.
- **C.** A thermal-stability advantage over the dimeric comparator accounts for the stronger cellular signal observed with APEX2.
- **D.** Peroxide-tolerance differences help explain the cellular advantage, whereas stability and heme-binding rankings alone do not match the cellular ranking.


---

# case-010 — PTEN phosphatase

Reference protein sequence (P60484, full canonical wild-type backbone; coordinate reference only):

```text
MTAIIKEIVSRNKRRYQEDGFDLDLTYIYPNIIAMGFPAERLEGVYRNNIDDVVRFLDSKHKNHYKIYNL
CAERHYDTAKFNCRVAQYPFEDHNPPQLELIKPFCEDLDQWLSEDDNHVAAIHCKAGKGRTGVMICAYLL
HRGKFLKAQEALDFYGEVRTRDKKGVTIPSQRRYVYYYSYLLKNHLDYRPVALLFHKMMFETIPMFSGGT
CNPQFVVCQLKVKIYSSNSGPTRREDKFMYFEFPQPLPVCGDIKVEFFHKQNKMLKKDKMFHFWVNTFFI
PGPEETSEKVENGSLCDQEIDSICSIERADNDKEYLVLTLTKNDLDKANKDKANRYFSPNFKVKLYFTKT
VEEPSNPEASSSTSVTPDVSDNEPDHYRYSDTTDSDPENEPFDEDQHTQITKV
```


All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.

Published variants: G129E.

Supplied experimental observations:
- A primary purified-protein study measured phosphate release from two PTEN substrates: the phosphoinositide lipid PIP3 and a phosphorylated poly(Glu,Tyr) protein-substrate preparation.
- Compared with wild type, G129E shows approximately 90% less activity against PIP3, but retains activity against the phosphorylated poly(Glu,Tyr) substrate.
- The report does not supply a universal claim about every possible protein substrate or a direct measurement of folding stability.

**Question:** Which conclusion is best supported by this substrate comparison?

- **A.** G129E preferentially impairs the protein-substrate reaction, while lipid dephosphorylation remains near the wild-type level under the measured conditions.
- **B.** G129E eliminates detectable activity on both tested substrates, supporting broad catalytic loss rather than separation of the measured substrate activities.
- **C.** G129E strongly impairs lipid dephosphorylation while retaining measured protein-substrate activity, showing that the two substrate activities can be affected differently.
- **D.** G129E preserves lipid dephosphorylation; its lower PIP3 signal measures reduced enzyme abundance, whereas the protein-substrate assay directly measures folding stability.


---

# case-011 — PafA alkaline phosphatase

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


---

# case-012 — adenylate_kinase

Wild-type protein: Adenylate kinase (Escherichia coli K-12).
Full canonical wild-type sequence, numbered from the initial methionine as residue 1:

```text
MRIILLGAPGAGKGTQAQFIMEKYGIPQISTGDMLRAAVKSGSELGKQAKDIMDAGKLVTDELVIALVKE
RIAQEDCRNGFLLDGFPRTIPQADAMKEAGINVDYVLEFDVPDELIVDRIVGRRVHAPSGRVYHVKFNPP
KVEGKDDVTGEELTTRKDDQEETVRKRLVEYHQMTAPLIGYYSKEAEAGNTKYAKVDGTKPVAEVRADLE
KILG
```


Published variant(s): R88A/R156K.

Experimental evidence:
Published central values: R88A kcat = 1.8 s^-1 and ATP Km = 120 micromolar; R156K kcat = 0.74 s^-1 and ATP Km = 52 micromolar. Compare equal active-enzyme concentrations with AMP held fixed and saturating. Use v/[E] = kcat[ATP]/(Km+[ATP]); no substrate inhibition is assumed in this comparison.

**Question:** How does the R88A-to-R156K rate ratio change from ATP far below both Km values to ATP far above both Km values?

- **A.** At low ATP, R88A is about 2.4 times faster; at saturating ATP, the variants are nearly equal in rate.
- **B.** At low ATP, R156K is about 2.3 times faster; at saturating ATP, R88A is about 2.4 times faster.
- **C.** At low ATP, R88A is about 2.4 times faster; at saturating ATP, R88A remains about 2.4 times faster.
- **D.** At low ATP, R88A is only about 1.05 times faster; at saturating ATP, R88A is about 2.4 times faster.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.


---

# case-013 — Biotin ligase

Reference protein sequence (canonical wild-type backbone; coordinate reference only):

```text
MKDNTVPLKLIALLANGEFHSGEQLGETLGMSRAAINKHIQTLRDWGVDVFTVPGKGYSLPEPIQLLNAK
QILGQLDGGSVAVLPVIDSTNQYLLDRIGELKSGDACIAEYQQAGRGRRGRKWFSPFGANLYLSMFWRLE
QGPAAAIGLSLVIGIVMAEVLRKLGADKVRVKWPNDLYLQDRKLAGILVELTGKTGDAAQIVIGAGINMA
MRRVEESVVNQGWITLQEAGINLDRNTLAAMLIRELRAALELFEQEGLAPYLSRWEKLDNFINRPVKLII
GDKEIFGISRGIDKQGALLLEQDGIIKPWMGGEISLRSAEK
```


Reference: P06709. All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded. The sequence is not the complete tagged assay construct.

Published variant identities:
TurboID: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V, K194I, M241T, S263P; deletions delete 146–146.
miniTurbo: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V, K194I; deletions delete 1–63, delete 146–146.

Supplied assay observations:
- The published cellular comparison finds miniTurbo less active overall than TurboID.
- miniTurbo also produces less labeling before exogenous biotin addition. The variants differ at multiple positions and in N-terminal-domain retention.

**Question:** A dataset annotation must distinguish induced labeling strength from control over when labeling begins. Which annotation is best supported?

- **A.** miniTurbo reduces pre-addition labeling but also lowers overall activity, separating temporal-background control from the strongest labeling signal.
- **B.** miniTurbo provides stronger overall labeling than TurboID, at the cost of more labeling before exogenous biotin addition.
- **C.** miniTurbo reduces pre-addition labeling while maintaining the same overall labeling activity as TurboID after biotin addition.
- **D.** Both variants have the same pre-addition labeling, while miniTurbo has lower overall activity following exogenous biotin addition.


---

# case-014 — Glucokinase / hexokinase-4

Reference protein sequence (P35557, full canonical wild-type backbone; coordinate reference only):

```text
MLDDRARMEAAKKEKVEQILAEFQLQEEDLKKVMRRMQKEMDRGLRLETHEEASVKMLPTYVRSTPEGSE
VGDFLSLDLGGTNFRVMLVKVGEGEEGQWSVKTKHQMYSIPEDAMTGTAEMLFDYISECISDFLDKHQMK
HKKLPLGFTFSFPVRHEDIDKGILLNWTKGFKASGAEGNNVVGLLRDAIKRRGDFEMDVVAMVNDTVATM
ISCYYEDHQCEVGMIVGTGCNACYMEEMQNVELVEGDEGRMCVNTEWGAFGDSGELDEFLLEYDRLVDES
SANPGQQLYEKLIGGKYMGELVRLVLLRLVDENLLFHGEASEQLRTRGAFETRFVSQVESDTGDRKQIYN
ILSTLGLRPSTTDCDIVRRACESVSTRAAHMCSAGLAGVINRMRESRSEDVMRITVGVDGSVYKLHPSFK
ERFHASVRRLTPSCEITFIESEEGSGRGAALVSAVACKKACMLGQ
```


All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.

Published variants: F150S, D217N, E279Q.

Supplied experimental observations:
- In a primary study of pancreatic human glucokinase, the same yeast complementation assay compares wild type with several published variants.
- F150S gives lower growth-based functional performance than wild type.
- D217N and E279Q give approximately wild-type-like performance in that assay.
- No matched abundance measurement or purified-enzyme kinetic measurement for these three variants is supplied in this question.

**Question:** Which comparative conclusion follows from the data?

- **A.** D217N and E279Q perform below wild type like F150S, so the experiment groups all three substitutions together as reduced-function variants in this cellular assay.
- **B.** F150S performs worse than the two wild-type-like comparators; this cellular comparison does not distinguish altered abundance, folding or kinetics as its molecular cause.
- **C.** F150S performs worse because its protein abundance is directly measured as lower; the growth comparison independently excludes altered folding or kinetics as contributing causes.
- **D.** F150S performs better than D217N and E279Q in the cellular assay, placing it above the two comparators despite its non-conservative amino-acid substitution.


---

# case-015 — PafA alkaline phosphatase

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

- **A.** The inactive population changes the fitted inhibition constant because normalization removes enzyme concentration only from the uninhibited rate, leaving inhibitor-dependent population effects.
- **B.** Cancellation of the active-enzyme factor shows that H83G stabilizes the catalytic transition state more strongly, so stronger inhibition establishes faster intrinsic chemistry.
- **C.** A smaller active population lowers the inhibitor concentration needed to halve its fractional rate, so inactive abundance alone can explain stronger apparent binding.
- **D.** The common active-enzyme factor cancels from the fractional rate; the changed inhibition constant therefore requires more than uniform dilution by inactive protein.


---

# case-016 — triosephosphate_isomerase

Wild-type protein: Triosephosphate isomerase (Saccharomyces cerevisiae).
Full canonical wild-type sequence, numbered from the initial methionine as residue 1:

```text
MARTFFVGGNFKLNGSKQSIKEIVERLNTASIPENVEVVICPPATYLDYSVSLVKKPQVTVGAQNAYLKA
SGAFTGENSVDQIKDVGAKWVILGHSERRSYFHEDDKFIADKTKFALGQGVGVILCIGETLEEKKAGKTL
DVVERQLNAVLEEVKDWTNVVVAYEPVWAIGTGLAATPEDAQDIHASIRKFLASKLGDKAASELRILYGG
SANGSNAVTFKDKADVDGFLVGGASLKPEFVDIINSRN
```


Published variant(s): S211A/S211G.

Experimental evidence:
Published GAP-isomerization central values at pH 7.5 and 25 C, using total GAP: S211A kcat = 2800 s^-1, Km = 12 mM; S211G kcat = 7500 s^-1, Km = 1.8 mM. Both substitutions remove the serine side-chain hydroxyl; alanine retains a methyl side chain and glycine does not.

**Question:** At GAP concentrations well below both Km values, which comparison is supported?

- **A.** S211A has about 2.5-fold higher catalytic efficiency; the product of kcat and Km determines the rate ratio when GAP is well below Km.
- **B.** S211G has about 2.7-fold higher catalytic efficiency; the turnover ratio alone determines the rate ratio when GAP is well below Km.
- **C.** S211G has about 18-fold higher catalytic efficiency; removing the same hydroxyl group need not produce the same low-substrate functional effect.
- **D.** S211G has about 6.7-fold higher catalytic efficiency; the inverse Km ratio alone determines the rate ratio when GAP is well below Km.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.


---

# case-017 — APEX peroxidase

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
VPGAPEX: substitutions K14D, W41F, E112K, A19V, A134P, D222G; deletions none.

Supplied assay observations:
- APEX2 has one additional substitution relative to APEX; VPGAPEX has three additional substitutions relative to APEX.
- The reported follow-up assays did not distinguish APEX2 from VPGAPEX, while the evolved variants improved on APEX.

**Question:** Which genotype-to-phenotype summary is justified by this comparison?

- **A.** APEX2 and VPGAPEX have matching assay performance because they carry the same set of additional substitutions relative to APEX.
- **B.** APEX2 improves on APEX with one added substitution; the extra VPGAPEX substitutions produce no further improvement detected in these assays.
- **C.** APEX2 and VPGAPEX both retain parent-level performance, despite carrying different numbers of additional substitutions relative to APEX.
- **D.** VPGAPEX improves on APEX2, associating an additional activity gain with its two extra substitutions beyond the APEX2 sequence.


---

# case-018 — PTEN phosphatase

Reference protein sequence (P60484, full canonical wild-type backbone; coordinate reference only):

```text
MTAIIKEIVSRNKRRYQEDGFDLDLTYIYPNIIAMGFPAERLEGVYRNNIDDVVRFLDSKHKNHYKIYNL
CAERHYDTAKFNCRVAQYPFEDHNPPQLELIKPFCEDLDQWLSEDDNHVAAIHCKAGKGRTGVMICAYLL
HRGKFLKAQEALDFYGEVRTRDKKGVTIPSQRRYVYYYSYLLKNHLDYRPVALLFHKMMFETIPMFSGGT
CNPQFVVCQLKVKIYSSNSGPTRREDKFMYFEFPQPLPVCGDIKVEFFHKQNKMLKKDKMFHFWVNTFFI
PGPEETSEKVENGSLCDQEIDSICSIERADNDKEYLVLTLTKNDLDKANKDKANRYFSPNFKVKLYFTKT
VEEPSNPEASSSTSVTPDVSDNEPDHYRYSDTTDSDPENEPFDEDQHTQITKV
```


All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.

Published variants: Y138L.

Supplied experimental observations:
- A primary biochemical study compared wild-type PTEN and Y138L using PIP3 as a lipid substrate and phosphorylated poly(Glu,Tyr) as a protein-substrate preparation.
- Further kinetic analysis found Y138L lipid phosphatase activity essentially indistinguishable from wild type under the tested conditions.
- Against the phosphorylated protein substrate, Y138L activity was approximately 3% of wild type and was frequently undetectable.

**Question:** Which description of Y138L best fits both readouts?

- **A.** Y138L increases the protein-substrate reaction while preserving lipid activity, indicating preferential enhancement of protein dephosphorylation rather than selective loss of that activity.
- **B.** Y138L lowers both tested activities to approximately 3% of wild type, supporting a similar impairment across the lipid and protein-substrate reactions.
- **C.** Y138L preserves the tested protein-substrate activity while strongly reducing lipid activity, so its principal defect is selective loss of PIP3 processing.
- **D.** Y138L preserves the tested lipid activity while strongly reducing protein-substrate activity, so a single total-activity category would obscure the substrate-dependent effect.


---

# case-019 — PafA alkaline phosphatase

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


---

# case-020 — adenylate_kinase

Wild-type protein: Adenylate kinase (Escherichia coli K-12).
Full canonical wild-type sequence, numbered from the initial methionine as residue 1:

```text
MRIILLGAPGAGKGTQAQFIMEKYGIPQISTGDMLRAAVKSGSELGKQAKDIMDAGKLVTDELVIALVKE
RIAQEDCRNGFLLDGFPRTIPQADAMKEAGINVDYVLEFDVPDELIVDRIVGRRVHAPSGRVYHVKFNPP
KVEGKDDVTGEELTTRKDDQEETVRKRLVEYHQMTAPLIGYYSKEAEAGNTKYAKVDGTKPVAEVRADLE
KILG
```


Published variant(s): R36A/R123A.

Experimental evidence:
Published ATP-dependent measurements: WT kcat = 330 s^-1, ATP Km = 71 micromolar; R36A kcat = 55 s^-1, Km = 89 micromolar; R123A kcat = 0.28 s^-1, Km = 110 micromolar. Both substitutions replace one arginine with alanine in the same enzyme.

**Question:** Which explanation is most consistent with the very different effects of these two nominally similar charge-removing substitutions?

- **A.** Both substitutions primarily change protein stability; their residual turnover values directly quantify the fraction of properly folded enzyme in each sample.
- **B.** Their different positions can make distinct catalytic contributions; removing the same side-chain charge need not produce similar effects on turnover.
- **C.** R123A primarily weakens equilibrium ATP binding rather than catalytic performance; its modest ATP Km increase accounts for the large turnover decrease.
- **D.** Their catalytic contributions become equivalent after correcting turnover for ATP Km; the different half-saturation concentrations fully explain their different turnover ceilings.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.


---

# case-021 — Biotin ligase

Reference protein sequence (canonical wild-type backbone; coordinate reference only):

```text
MKDNTVPLKLIALLANGEFHSGEQLGETLGMSRAAINKHIQTLRDWGVDVFTVPGKGYSLPEPIQLLNAK
QILGQLDGGSVAVLPVIDSTNQYLLDRIGELKSGDACIAEYQQAGRGRRGRKWFSPFGANLYLSMFWRLE
QGPAAAIGLSLVIGIVMAEVLRKLGADKVRVKWPNDLYLQDRKLAGILVELTGKTGDAAQIVIGAGINMA
MRRVEESVVNQGWITLQEAGINLDRNTLAAMLIRELRAALELFEQEGLAPYLSRWEKLDNFINRPVKLII
GDKEIFGISRGIDKQGALLLEQDGIIKPWMGGEISLRSAEK
```


Reference: P06709. All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded. The sequence is not the complete tagged assay construct.

Published variant identities:
G3Δ, published intermediate: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V; deletions delete 1–63, delete 146–146.
miniTurbo: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V, K194I; deletions delete 1–63, delete 146–146.

Supplied assay observations:
- Supplementary Table 1 defines miniTurbo as G3Δ with one additional substitution, K194I in the reference numbering.
- The published cellular screening reports higher labeling activity for this change without increased signal when exogenous biotin is omitted.

**Question:** Which characterization combines the controlled sequence difference and the two readouts correctly?

- **A.** The added K194I substitution raises both activity and the no-added-biotin signal in G3Δ, producing a measured background tradeoff.
- **B.** The added K194I substitution raises activity in the G3Δ background without increasing the measured no-added-biotin signal.
- **C.** The compared enzyme cores differ at multiple internal sites, associating the higher activity with combined substitutions rather than the stated single difference.
- **D.** The added K194I substitution lowers the no-added-biotin signal but leaves the measured activity at the G3Δ level.


---

# case-022 — Glucokinase / hexokinase-4

Reference protein sequence (P35557, full canonical wild-type backbone; coordinate reference only):

```text
MLDDRARMEAAKKEKVEQILAEFQLQEEDLKKVMRRMQKEMDRGLRLETHEEASVKMLPTYVRSTPEGSE
VGDFLSLDLGGTNFRVMLVKVGEGEEGQWSVKTKHQMYSIPEDAMTGTAEMLFDYISECISDFLDKHQMK
HKKLPLGFTFSFPVRHEDIDKGILLNWTKGFKASGAEGNNVVGLLRDAIKRRGDFEMDVVAMVNDTVATM
ISCYYEDHQCEVGMIVGTGCNACYMEEMQNVELVEGDEGRMCVNTEWGAFGDSGELDEFLLEYDRLVDES
SANPGQQLYEKLIGGKYMGELVRLVLLRLVDENLLFHGEASEQLRTRGAFETRFVSQVESDTGDRKQIYN
ILSTLGLRPSTTDCDIVRRACESVSTRAAHMCSAGLAGVINRMRESRSEDVMRITVGVDGSVYKLHPSFK
ERFHASVRRLTPSCEITFIESEEGSGRGAALVSAVACKKACMLGQ
```


All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.

Published variants: D217N, E279Q.

Supplied experimental observations:
- D217N replaces an aspartate side chain with asparagine, and E279Q replaces glutamate with glutamine. Each removes a negatively charged carboxylate while preserving a similarly sized polar amide side chain.
- In a published pancreatic human glucokinase complementation assay, both D217N and E279Q show wild-type-like functional performance.
- The experiment does not report the behavior of every other acidic residue in the protein or establish identical kinetics in every glucose condition.

**Question:** Which generalization about sequence changes is justified by these two tested substitutions?

- **A.** Loss of an acidic side-chain charge is tolerated at these two tested positions; substitution effects therefore depend on position and the measured assay context.
- **B.** The wild-type-like outcome demonstrates preservation of side-chain charge, because the asparagine and glutamine replacements retain the negative carboxylate groups of the original residues.
- **C.** Both substitutions introduce positively charged side chains, so their wild-type-like performance demonstrates tolerance of a negative-to-positive charge reversal at the two tested positions.
- **D.** The two wild-type-like outcomes establish a position-independent rule: acidic-to-amide substitutions preserve glucokinase function equally wherever they occur within this protein under the tested conditions.


---

# case-023 — PafA alkaline phosphatase

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


---

# case-024 — triosephosphate_isomerase

Wild-type protein: Triosephosphate isomerase (Saccharomyces cerevisiae).
Full canonical wild-type sequence, numbered from the initial methionine as residue 1:

```text
MARTFFVGGNFKLNGSKQSIKEIVERLNTASIPENVEVVICPPATYLDYSVSLVKKPQVTVGAQNAYLKA
SGAFTGENSVDQIKDVGAKWVILGHSERRSYFHEDDKFIADKTKFALGQGVGVILCIGETLEEKKAGKTL
DVVERQLNAVLEEVKDWTNVVVAYEPVWAIGTGLAATPEDAQDIHASIRKFLASKLGDKAASELRILYGG
SANGSNAVTFKDKADVDGFLVGGASLKPEFVDIINSRN
```


Published variant(s): Y208T/S211G.

Experimental evidence:
Published GAP-isomerization kcat values at pH 7.5 and 25 C: WT 8900 s^-1; Y208T 3700 s^-1; S211G 7500 s^-1; the experimentally measured double variant Y208T/S211G 520 s^-1. For this question, an independent fractional-effects model predicts kcat(double) = kcat(Y208T) * kcat(S211G) / kcat(WT).

**Question:** How does the observed double-variant turnover compare with that specified independence model?

- **A.** The model predicts about 2300 s^-1 by adding the two changes from WT; the observed value is about fourfold lower, indicating negative kinetic epistasis.
- **B.** The model predicts about 3100 s^-1; the observed value is about sixfold lower, indicating negative kinetic epistasis for turnover under these conditions.
- **C.** The model predicts about 3100 s^-1; the sixfold deficit establishes direct physical contact between the substituted residues as the mechanism of their interaction.
- **D.** The model predicts about 3100 s^-1; the observed value is about sixfold above that prediction, indicating positive kinetic epistasis for turnover.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.


---

# case-025 — APEX peroxidase

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
- With matched outer-mitochondrial-membrane targeting, APEX2 strongly enriches Tom70 and Tom20; APEX barely enriches them.
- APEX2 does not enrich the matrix marker ATP5B and gives only slight enrichment of ER-membrane marker BCAP31. Construct pairs have similar expression.

**Question:** What does the pattern support about the evolved variant in this assay?

- **A.** The APEX2 variant increases proximal-marker enrichment while the other compartment markers remain excluded or much more weakly enriched.
- **B.** The APEX2 variant enriches the supplied mitochondrial and ER-membrane markers equally, indicating reduced discrimination between those membranes.
- **C.** The APEX2 variant increases proximal-marker enrichment together with similarly strong enrichment of the supplied mitochondrial-matrix marker.
- **D.** The APEX2 reporter is expressed at much higher abundance, accounting for increased enrichment under otherwise matched targeting.


---

# case-026 — PTEN phosphatase

Reference protein sequence (P60484, full canonical wild-type backbone; coordinate reference only):

```text
MTAIIKEIVSRNKRRYQEDGFDLDLTYIYPNIIAMGFPAERLEGVYRNNIDDVVRFLDSKHKNHYKIYNL
CAERHYDTAKFNCRVAQYPFEDHNPPQLELIKPFCEDLDQWLSEDDNHVAAIHCKAGKGRTGVMICAYLL
HRGKFLKAQEALDFYGEVRTRDKKGVTIPSQRRYVYYYSYLLKNHLDYRPVALLFHKMMFETIPMFSGGT
CNPQFVVCQLKVKIYSSNSGPTRREDKFMYFEFPQPLPVCGDIKVEFFHKQNKMLKKDKMFHFWVNTFFI
PGPEETSEKVENGSLCDQEIDSICSIERADNDKEYLVLTLTKNDLDKANKDKANRYFSPNFKVKLYFTKT
VEEPSNPEASSSTSVTPDVSDNEPDHYRYSDTTDSDPENEPFDEDQHTQITKV
```


All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.

Published variants: D92N.

Supplied experimental observations:
- A published PTEN study reports that D92N resembles wild type in its yeast growth-rescue readout.
- The same paper notes that a PIP3 fluorescence reporter and an in-vitro phosphatase assay detect only partial activity for D92N.
- Growth rescue is a downstream cellular phenotype; reporter and biochemical assays read out other aspects of PTEN function. No quantitative calibration converting one assay into the others is provided.

**Question:** What is the most defensible interpretation of this apparent disagreement?

- **A.** The growth-rescue result establishes fully wild-type phosphatase activity in the direct assays, because downstream growth provides a calibrated measure of enzymatic rate.
- **B.** Partial phosphatase function can support wild-type-like growth; the downstream rescue result therefore does not establish fully wild-type activity in the other assays.
- **C.** The assays give a common quantitative activity estimate: wild-type-like growth and partial biochemical activity are interchangeable once expressed relative to their wild-type controls.
- **D.** The reporter and biochemical assays establish complete loss of phosphatase activity, so wild-type-like growth must occur without any residual activity from D92N.


---

# case-027 — PafA alkaline phosphatase

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


---

# case-028 — adenylate_kinase

Wild-type protein: Adenylate kinase (Escherichia coli K-12).
Full canonical wild-type sequence, numbered from the initial methionine as residue 1:

```text
MRIILLGAPGAGKGTQAQFIMEKYGIPQISTGDMLRAAVKSGSELGKQAKDIMDAGKLVTDELVIALVKE
RIAQEDCRNGFLLDGFPRTIPQADAMKEAGINVDYVLEFDVPDELIVDRIVGRRVHAPSGRVYHVKFNPP
KVEGKDDVTGEELTTRKDDQEETVRKRLVEYHQMTAPLIGYYSKEAEAGNTKYAKVDGTKPVAEVRADLE
KILG
```


Published variant(s): R167A.

Experimental evidence:
The primary study reports WT kcat = 330 s^-1 with Mg2+ and 0.0075 s^-1 without Mg2+. The published R167A variant has kcat = 2.4 s^-1 in the Mg2+-containing kinetic comparison. These are reported turnover measurements; they are not Mg2+ binding-affinity measurements.

**Question:** Which quantitative and biological comparison is supported by these observations?

- **A.** Mg2+ removal causes about a 44,000-fold loss and R167A about a 140-fold loss; cofactor presence does not replace the missing residue contribution.
- **B.** Mg2+ removal causes about a 44,000-fold loss and R167A about a 140-fold loss; these turnover ratios also give the corresponding binding-affinity losses.
- **C.** Mg2+ removal causes about a 44,000-fold loss and R167A about a 140-fold loss; sufficiently high ATP must therefore restore R167A to WT turnover.
- **D.** Mg2+ removal causes about a 140-fold loss, while R167A with Mg2+ causes about a 44,000-fold loss; the residue substitution is the larger defect.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.


---

# case-029 — Biotin ligase

Reference protein sequence (canonical wild-type backbone; coordinate reference only):

```text
MKDNTVPLKLIALLANGEFHSGEQLGETLGMSRAAINKHIQTLRDWGVDVFTVPGKGYSLPEPIQLLNAK
QILGQLDGGSVAVLPVIDSTNQYLLDRIGELKSGDACIAEYQQAGRGRRGRKWFSPFGANLYLSMFWRLE
QGPAAAIGLSLVIGIVMAEVLRKLGADKVRVKWPNDLYLQDRKLAGILVELTGKTGDAAQIVIGAGINMA
MRRVEESVVNQGWITLQEAGINLDRNTLAAMLIRELRAALELFEQEGLAPYLSRWEKLDNFINRPVKLII
GDKEIFGISRGIDKQGALLLEQDGIIKPWMGGEISLRSAEK
```


Reference: P06709. All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded. The sequence is not the complete tagged assay construct.

Published variant identities:
G3, published intermediate: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V; deletions delete 146–146.
G3Δ, published intermediate: substitutions Q65P, I87V, R118S, E140K, Q141R, S150G, L151P, V160A, T192A, M209V, I305V; deletions delete 1–63, delete 146–146.

Supplied assay observations:
- G3Δ removes reference residues 1–63 from the G3 enzyme core and retains the listed internal substitutions.
- G3 gives labeling without exogenous biotin in regular medium; the signal disappears in biotin-depleted medium. The G3Δ comparison shows reduced pre-addition labeling.

**Question:** Which interpretation integrates the deletion comparison with the substrate-depletion control?

- **A.** G3 retains its ordinary-medium labeling after biotin depletion, placing the deletion-associated signal change outside the substrate-dependent background.
- **B.** The N-terminal deletion leaves pre-addition labeling unchanged, so substrate depletion is the only supplied condition that reduces the signal.
- **C.** The G3 versus G3Δ comparison isolates internal A146 deletion while both variants retain the same N-terminal domain.
- **D.** Ambient biotin supports pre-addition labeling by G3, and the published N-terminal deletion reduces that signal in the tested comparison.


---

# case-030 — Glucokinase / hexokinase-4

Reference protein sequence (P35557, full canonical wild-type backbone; coordinate reference only):

```text
MLDDRARMEAAKKEKVEQILAEFQLQEEDLKKVMRRMQKEMDRGLRLETHEEASVKMLPTYVRSTPEGSE
VGDFLSLDLGGTNFRVMLVKVGEGEEGQWSVKTKHQMYSIPEDAMTGTAEMLFDYISECISDFLDKHQMK
HKKLPLGFTFSFPVRHEDIDKGILLNWTKGFKASGAEGNNVVGLLRDAIKRRGDFEMDVVAMVNDTVATM
ISCYYEDHQCEVGMIVGTGCNACYMEEMQNVELVEGDEGRMCVNTEWGAFGDSGELDEFLLEYDRLVDES
SANPGQQLYEKLIGGKYMGELVRLVLLRLVDENLLFHGEASEQLRTRGAFETRFVSQVESDTGDRKQIYN
ILSTLGLRPSTTDCDIVRRACESVSTRAAHMCSAGLAGVINRMRESRSEDVMRITVGVDGSVYKLHPSFK
ERFHASVRRLTPSCEITFIESEEGSGRGAALVSAVACKKACMLGQ
```


All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.

Published variants: A456V, W99R.

Supplied experimental observations:
- A primary transient-kinetic study of published human glucokinase variants describes glucose recognition as an initial enzyme-glucose association followed by a conformational isomerization that favors the active form.
- For A456V, the study reports acceleration of the initial glucose-binding step to the glucose-free enzyme.
- For W99R, the study reports facilitation of the subsequent isomerization toward the active form.
- Both variants concern the same glucokinase reaction; these observations do not introduce a new substrate or reaction product.

**Question:** What mechanistic lesson follows from comparing A456V and W99R?

- **A.** A456V facilitates active-form isomerization whereas W99R accelerates initial glucose association, separating the variants by assigning their measured effects to different steps of this pathway.
- **B.** Both variants accelerate initial glucose association with the glucose-free enzyme, so their functional gains arise from a common effect before the conformational isomerization step.
- **C.** The variants affect different steps in the same binding and conformational pathway, so similar functional gains need not arise from the same microscopic mechanism.
- **D.** Both variants facilitate the subsequent active-form isomerization, so their functional gains arise from a common conformational effect after the initial glucose-association step has occurred.


---

# case-031 — PafA alkaline phosphatase

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
For the published K162A variant, catalytic efficiency(kcat/KM) for the methyl-phosphate reaction, whose chemical step is rate-limiting, is reduced by more than10^6-fold relative to wild type. Vanadate binding is weakened much less, by about10^2-fold. Vanadate is a transition-state analog, not the actual reacting transition state. Use these reported within-assay effects; they are not a cellular-fitness measurement or a direct measurement of kcat alone.

**Question:** What is the most justified conclusion from the mismatch?

- **A.** The residual vanadate affinity establishes substantial transition-state stabilization, so most catalytic loss should be assigned to reduced active-enzyme abundance rather than chemistry.
- **B.** The methyl-phosphate efficiency loss establishes the same change in first-order turnover; the analog comparison then distinguishes that turnover defect from altered substrate binding.
- **C.** Real catalysis is disrupted much more than analog binding; residual TSA affinity cannot establish preserved transition-state stabilization or retained catalytic power.
- **D.** Weaker vanadate binding quantitatively determines the catalytic defect, so its affinity change provides the appropriate correction for interpreting the larger methyl-phosphate effect.


---

# case-032 — triosephosphate_isomerase

Wild-type protein: Triosephosphate isomerase (Saccharomyces cerevisiae).
Full canonical wild-type sequence, numbered from the initial methionine as residue 1:

```text
MARTFFVGGNFKLNGSKQSIKEIVERLNTASIPENVEVVICPPATYLDYSVSLVKKPQVTVGAQNAYLKA
SGAFTGENSVDQIKDVGAKWVILGHSERRSYFHEDDKFIADKTKFALGQGVGVILCIGETLEEKKAGKTL
DVVERQLNAVLEEVKDWTNVVVAYEPVWAIGTGLAATPEDAQDIHASIRKFLASKLGDKAASELRILYGG
SANGSNAVTFKDKADVDGFLVGGASLKPEFVDIINSRN
```


Published variant(s): Y208F.

Experimental evidence:
Published pH-dependent inhibitor-binding analysis estimates pKa = 10.4 for E165 in the WT TIM complex with the intermediate analogue phosphoglycolate trianion (PGA), and pKa = 6.3 for the corresponding Y208F complex. These pKa values refer specifically to the inhibitor-bound enzyme. For the simple protonation equilibrium in this question, protonated fraction = 1/(1+10^(pH-pKa)).

**Question:** At pH 8.0, which interpretation of these experimentally fitted pKa values is correct?

- **A.** WT is about 0.4% protonated and Y208F about 98%; the protonated fractions are obtained by subtracting the higher-pKa and lower-pKa populations from unity.
- **B.** WT is about 99.6% protonated and Y208F about 2%; these same fractions also establish E165 protonation in the free enzyme and true catalytic intermediate.
- **C.** WT is about 2% protonated and Y208F about 99.6%; the mutation therefore increases proton retention by E165 in the specified inhibitor-bound state.
- **D.** WT is about 99.6% protonated and Y208F about 2%; changing the protein environment can strongly alter E165 protonation in the specified inhibitor-bound state.

Additional solver instructions:

Interpret the supplied published measurements. Explain the relevant biological and quantitative reasoning, then give one answer letter. Do not propose new variants or experimental procedures.
