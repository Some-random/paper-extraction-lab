# case-001 — APEX peroxidase: mutation effect assay interpretation

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

Choice C captures both the variant difference and the dependence on guaiacol concentration.

Use the peroxide concentration at the reported rate maximum as an approximate boundary above which activity declines:
- At 1.4 mM guaiacol, the maximum occurs around 0.1 mM peroxide for APEX versus 2.5 mM for APEX2: approximately a 25-fold higher peroxide concentration for APEX2.
- At 0.5 mM guaiacol, the corresponding values are 0.05 mM and 0.5 mM: approximately a 10-fold higher concentration for APEX2.

Thus, both substrate conditions show a higher apparent peroxide-inhibition threshold for APEX2. The threshold is also guaiacol-dependent: increasing guaiacol from 0.5 to 1.4 mM shifts the maximum from 0.05 to 0.1 mM peroxide for APEX and from 0.5 to 2.5 mM for APEX2, approximately twofold and fivefold increases, respectively.

Mechanistically, peroxide drives formation of oxidizing heme intermediates during peroxidase catalysis, while guaiacol supplies reducing equivalents for productive turnover. Excess peroxide can promote nonproductive states or oxidative inactivation. Changing the electron-donor concentration can alter the balance between productive turnover and these competing processes, so an apparent peroxide-inhibition threshold need not be substrate-independent. This is consistent with the observations without establishing their precise molecular cause.

The listed sequence difference is A134P added to the shared K14D/W41F/E112K background. The assay observations establish the kinetic distinction; alanine-to-proline substitution chemistry alone would not uniquely predict it.

A is excluded because APEX2 also has a higher threshold at lower guaiacol. B is excluded because the thresholds change with guaiacol concentration. D is excluded because the variants have different thresholds under both conditions.

## Final answer

C

## Astra’s stated limitations

The reported rate maxima are approximate, condition-dependent markers, not formal inhibition constants. These observations do not distinguish reversible inhibition from oxidative inactivation, establish a structural mechanism for A134P, or show that APEX2 has a higher maximum rate. The canonical sequence provides coordinates, not the complete tagged assay construct.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

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


---

# case-002 — PTEN phosphatase: mutation activity vs abundance

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

A best combines the measurements because abundance and functional rescue are distinct assay outcomes.

Observed evidence: In the yeast assay, wild-type PTEN rescues growth whereas C124S does not. This demonstrates failure of the mutant to support the lipid-phosphatase-associated rescue phenotype under those conditions; it is not a direct measurement of protein abundance or a protein-normalized catalytic rate. Separately, human-cell VAMP-seq assigns C124S a normalized abundance score of 1.14 and places it in the wild-type-like abundance class. The score therefore supports normal accumulation in that assay, not low abundance, enhanced catalysis, or a 1.14-fold catalytic rate.

Mechanistic interpretation: Reference residues 123–130 are HCKAGKGR, placing C124 in the phosphatase catalytic motif. PTEN uses this cysteine's thiolate as a nucleophile during phosphate removal. Replacing cysteine with serine changes that active-site chemistry, making an activity defect compatible with continued protein accumulation. This provides a mechanistic explanation consistent with the observations, but it does not convert either assay into a direct catalytic-rate measurement or establish normal abundance in yeast.

Discriminating the choices: A accurately states both observations while keeping their experimental contexts separate. B reverses both results: rescue fails, and human-cell abundance is not classified as low; improved catalytic performance is unsupported. C incorrectly treats an abundance score as a catalytic score and reinterprets a functional rescue readout as an abundance measurement. D contradicts the wild-type-like human-cell abundance classification and incorrectly claims that deficient accumulation was directly measured in yeast.

The reusable principle is that a protein can accumulate normally yet fail a functional assay, particularly when an essential catalytic residue is altered.

## Final answer

A

## Astra’s stated limitations

The measurements come from different experimental systems. No yeast abundance measurement or same-system, protein-normalized catalytic rate is supplied, so these data cannot quantify intrinsic catalytic activity or establish that failed rescue is caused exclusively by a catalytic defect. Wild-type-like human-cell abundance does not establish unchanged folding or stability.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PTEN phosphatase** — [UniProt P60484](https://www.uniprot.org/uniprotkb/P60484/entry).

Source-supported reference answer: **A**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly separates wild-type-like human-cell abundance from failed yeast rescue and does not turn score 1.14 into a fold-change or catalytic rate.
- Adds a correct catalytic-cysteine explanation and explicitly limits what cross-system comparisons establish.

Source support:

- Figure 1A; Results describing growth rescue
- Wild-type PTEN rescues the growth defect; C124S does not. Methods use a 403-aa NP_000305 reference.
- Results on wild-type-like abundance of inactive variants, near Figure 4
- C124S is among inactive variants with wild-type-like abundance; its reported abundance score is 1.14.

Source qualifications:

- Do not treat score 1.14 as a 1.14-fold protein concentration.
- Do not infer that human-cell abundance measured the amount in the yeast assay.
- Catalytic impairment has stronger primary support than a specific folding or degradation mechanism.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Mighell2018 Methods: NM_000314.6, corresponding 403-aa NP_000305; current canonical record cross-references NP_000305.3. Full paper-assay construct sequence still requires final replay before release.
- VAMP-seq is an abundance assay in a different cellular system, not a direct PTEN catalytic-rate measurement.

Primary references:

- [A Saturation Mutagenesis Approach to Understanding PTEN Lipid Phosphatase Activity and Genotype-Phenotype Relationships](https://pmc.ncbi.nlm.nih.gov/articles/PMC5986715/)

- [Multiplex assessment of protein variant abundance by massively parallel sequencing](https://pmc.ncbi.nlm.nih.gov/articles/PMC5980760/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-004 — adenylate_kinase: mutation kinetic reasoning

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

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

## Final answer

C

## Astra’s stated limitations

The conclusion applies to the supplied ATP-dependent kinetic measurements. Neither the sequence nor these kinetic parameters uniquely identify the affected microscopic step, establish equilibrium ATP affinity, or quantify the folded or active protein fraction.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

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


---

# case-009 — APEX peroxidase: mutation effect mechanism evidence

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

D best reconciles the observations.

Sequence comparison: APEX2 adds A134P to the K14D/W41F/E112K background of APEX. This identifies the listed sequence difference, but the presence of a proline substitution alone does not establish its effects on stability, heme binding or peroxide inhibition. Those effects must be interpreted from the supplied measurements.

Observed rankings: Cellular activity places APEX2 above both APEX and the dimeric APX-W41F comparator. In contrast, thermal stability and heme binding each rank the dimeric comparator above APEX2, with APEX2 only slightly improved over APEX. Therefore, neither thermal stability nor heme binding alone reproduces the cellular ranking.

Mechanistic interpretation: Peroxide is a catalytic cosubstrate for a heme peroxidase, but excessive peroxide exposure can also inhibit catalysis or cause oxidative inactivation. Resistance to peroxide inhibition is therefore distinct from resistance to thermal unfolding and from heme binding. If peroxide inhibition limits activity under the cellular assay conditions, APEX2's observed greater resistance can preserve catalytic activity despite its lower thermal stability and heme binding relative to the dimeric comparator. The purified-assay result supplies independent biochemical support for this explanation without requiring a particular structural mechanism.

Discriminating the alternatives: A incorrectly asserts a heme-binding advantage over the dimeric comparator, directly contradicting the observations. C makes the corresponding incorrect assertion about thermal stability. B incorrectly states that cellular activity follows the thermal-stability ranking and treats peroxide tolerance as though it necessarily follows that ranking. D correctly identifies peroxide tolerance as a plausible contributor while recognizing that stability and heme-binding rankings alone cannot explain the cellular advantage.

## Final answer

D

## Astra’s stated limitations

The observations support peroxide tolerance as a contributor, not necessarily the sole cause of higher cellular activity. Peroxide concentrations, cellular enzyme abundance and complete assay constructs are not supplied. Neither the sequence nor these comparisons establish the precise structural mechanism of A134P.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **APEX peroxidase** — [UniProt Q43758](https://www.uniprot.org/uniprotkb/Q43758/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly contrasts the cellular ranking with the different stability and heme-binding rankings.
- Uses independent peroxide-tolerance evidence as a conditional contributing explanation, without claiming exclusive causality.
- Correctly identifies the shared substitutions and sole additional A134P difference.

Source support:

- Figure 2e; Supplementary Figures 8c and 9; accompanying Results
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- The assays support a contributing explanation; they do not prove a uniquely sufficient mechanism.
- Use corrected Figure 2a symbols and Figure 2e axis labels; correction dated December 10, 2014.

Primary references:

- [Directed evolution of APEX2 for electron microscopy and proximity labeling](https://www.nature.com/articles/nmeth.3179)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-010 — PTEN phosphatase: mutation substrate specificity

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

C is directly supported by the substrate comparison. Approximately 90% less PIP3 activity means that G129E retains roughly 10% of the wild-type activity in that lipid-substrate assay: a strong impairment, not preservation and not necessarily complete abolition. In contrast, activity remains detectable against the phosphorylated poly(Glu,Tyr) preparation. Thus, the mutation affects the two measured substrate reactions differently. The supplied description does not quantify how closely the retained protein-substrate activity matches wild type.

The sequence provides a mechanistically relevant context: Gly129 lies in the phosphatase active-site loop containing catalytic Cys124 and Arg130. Replacing glycine with a larger acidic glutamate side chain could alter substrate accommodation or local active-site chemistry, allowing different effects on lipid and protein-substrate processing. This is a plausible interpretation, not a demonstrated structural mechanism; the assay observations, rather than sequence alone, establish the differential activities.

A reverses the observed substrate effects. B contradicts the retained protein-substrate activity and the reported residual PIP3 activity. D incorrectly describes lipid dephosphorylation as preserved and misidentifies the assay readouts: phosphate release measures substrate dephosphorylation, not enzyme abundance or folding stability. Therefore, C is the supported conclusion.

## Final answer

C

## Astra’s stated limitations

The conclusion applies to the two tested substrates under the reported assay conditions. Retained activity on phosphorylated poly(Glu,Tyr) does not establish unchanged activity on every protein substrate. The observations do not directly measure folding stability, enzyme abundance, substrate binding, or the precise catalytic step affected.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PTEN phosphatase** — [UniProt P60484](https://www.uniprot.org/uniprotkb/P60484/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly converts approximately 90% less lipid activity into approximately 10% residual activity, while not inventing a quantitative protein-substrate value.
- Correctly identifies substrate-dependent functional separation and restricts the claim to the tested substrates.
- The bulky acidic substitution in the active-site loop is offered as a plausible interpretation, not a demonstrated structure or precise kinetic mechanism.

Source support:

- Figure 1A; Results paragraph comparing purified WT, C124S and G129E on PIP3 and polyGluTyr
- G129E reduces lipid phosphatase activity by approximately 90% while retaining activity against polyGluTyr.

Source qualifications:

- Retained polyGluTyr activity does not prove every physiological protein substrate is processed normally.
- No causal structural mechanism or folding-stability value is measured in this question.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Mighell2018 Methods: NM_000314.6, corresponding 403-aa NP_000305; current canonical record cross-references NP_000305.3. Full paper-assay construct sequence still requires final replay before release.
- The qualitative retention of polyGluTyr activity is supported; do not invent an exact percentage for that substrate.

Primary references:

- [The lipid phosphatase activity of PTEN is critical for its tumor supressor function](https://pmc.ncbi.nlm.nih.gov/articles/PMC24850/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-012 — adenylate_kinase: mutation kinetic reasoning

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

The supplied reference has arginine at both reported mutation positions. The rate comparison follows from the supplied kinetic measurements, rather than from predicting effects of these substitutions from sequence.

Adenylate kinase catalyzes ATP + AMP ⇌ 2 ADP. With AMP fixed and saturating, use the stated ATP-dependent rate law. Equal active-enzyme concentrations cancel in the rate ratio. Writing S = [ATP] in micromolar:

R(S) = v_R88A/v_R156K = (1.8/0.74) × (52 + S)/(120 + S).

At ATP far below both Km values, v/[E] ≈ (kcat/Km)S. Thus the relevant quantities are ATP catalytic efficiencies:
• R88A: 1.8/120 = 0.0150 s^-1 µM^-1.
• R156K: 0.74/52 ≈ 0.01423 s^-1 µM^-1.

The low-ATP rate ratio is therefore 0.0150/0.01423 ≈ 1.054. R88A is only about 1.05 times faster. Its approximately 2.43-fold higher kcat is almost offset by its approximately 2.31-fold higher ATP Km. A lower Km alone does not establish a faster low-substrate rate, and Km should not automatically be interpreted as a binding dissociation constant.

At ATP far above both Km values, v/[E] approaches kcat. The rate ratio becomes 1.8/0.74 ≈ 2.43, so R88A is about 2.4 times faster.

The ratio therefore increases from approximately 1.05 at low ATP to approximately 2.4 at saturating ATP. A and C incorrectly assign a 2.4-fold advantage at low ATP; B incorrectly favors R156K at low ATP. The supplied measurements support D.

## Final answer

D

## Astra’s stated limitations

The conclusion uses the supplied central values and assumes saturating AMP, equal active-enzyme concentrations, and the stated Michaelis–Menten model without substrate inhibition. No measurement uncertainties are provided, so the approximately 5% low-ATP difference is not evidence of statistical significance. Sequence alone would not establish these kinetic effects.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **adenylate_kinase** — [UniProt P69441](https://www.uniprot.org/uniprotkb/P69441/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

Correct remapped answer D. Derives the full ratio R(S) = (1.8/0.74)*(52+S)/(120+S), then correctly obtains about 1.054 at low ATP and 2.432 at saturation. Keeps the equal-active-enzyme and saturating-AMP assumptions explicit. Correctly notes that the roughly 5% low-ATP difference is a central-value comparison rather than demonstrated statistical significance. Distractors are rejected using the appropriate kinetic regimes.

Source support:

- 2021 Figure 2c / Table S2; 2023 Table 1, R88A and R156K rows.
- Published central values: R88A kcat = 1.8 s^-1 and ATP Km = 120 micromolar; R156K kcat = 0.74 s^-1 and ATP Km = 52 micromolar. Compare equal active-enzyme concentrations with AMP held fixed and saturating. Use v/[E] = kcat[ATP]/(Km+[ATP]); no substrate inhibition is assumed in this comparison.
- Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.
- Table 1, footnote a.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. Published R36, R88, R123, R156 and R167 all match the reference residues.
- The prompt supplies the verified canonical reference and published mutation labels. No unreported affinity tag, cloning scar or exact expressed-construct extension is inferred.

Primary references:

- [Dynamic Connection between Enzymatic Catalysis and Collective Protein Motions](https://pmc.ncbi.nlm.nih.gov/articles/PMC8297476/). Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.

- [Mechanistic basis for a connection between the catalytic step and slow opening dynamics of adenylate kinase](https://pmc.ncbi.nlm.nih.gov/articles/PMC11779523/). Table 1, footnote a.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-015 — PafA alkaline phosphatase: published enzyme mutation reasoning

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
The published H83G variant has a lower Pi inhibition constant than wild type, meaning stronger phosphate binding. The inhibition readout is a fractional rate v(I)/v(0) for the same variant. In a simple model with a long-lived inactive fraction, only the active population reacts and binds inhibitor, and its concentration multiplies both v(I) and v(0) by the same factor. There is no interconversion of populations during the measurement.

**Question:** Can a smaller active population alone explain the changed normalized inhibition constant?

- **A.** The inactive population changes the fitted inhibition constant because normalization removes enzyme concentration only from the uninhibited rate, leaving inhibitor-dependent population effects.
- **B.** Cancellation of the active-enzyme factor shows that H83G stabilizes the catalytic transition state more strongly, so stronger inhibition establishes faster intrinsic chemistry.
- **C.** A smaller active population lowers the inhibitor concentration needed to halve its fractional rate, so inactive abundance alone can explain stronger apparent binding.
- **D.** The common active-enzyme factor cancels from the fractional rate; the changed inhibition constant therefore requires more than uniform dilution by inactive protein.


## Astra’s worked solution

The reference confirms histidine at canonical position 83, the site of H83G. This identifies the substitution but does not, by itself, establish its effect on phosphate binding or catalysis. The decisive evidence is the normalized inhibition measurement and the supplied population model.

Let E_total be total enzyme concentration, f the fixed fraction belonging to the active population, and r(I) the rate per active enzyme at phosphate concentration I under otherwise identical assay conditions. Inhibition of active enzyme is included in r(I). Then:

v(I) = f E_total r(I)
v(0) = f E_total r(0)
v(I)/v(0) = r(I)/r(0).

Both the active fraction and total enzyme concentration cancel. If H83G changed only the abundance of inactive protein, its per-active-enzyme response r(I) would remain unchanged. Absolute rates would decrease, but the normalized inhibition curve—and therefore its fitted inhibition constant—would not shift. In particular, the phosphate concentration giving half of the uninhibited fractional rate would remain unchanged.

Consequently, the reported lower Pi inhibition constant requires more than uniform dilution by inactive protein. Within the stated model, it reflects an altered inhibition/binding response of the active population.

A is incorrect because the active-enzyme factor appears in both rates and cancels from their ratio. C is incorrect because decreasing active abundance alone cannot shift fractional half-inhibition. B correctly invokes cancellation but adds an unsupported conclusion: stronger binding of phosphate, a product inhibitor, does not establish greater catalytic transition-state stabilization or faster intrinsic chemistry. D states the justified conclusion.

## Final answer

D

## Astra’s stated limitations

The conclusion applies to the supplied fixed-population model. A reduced active fraction could coexist with stronger phosphate binding, but cannot alone explain the normalized inhibition shift. The evidence does not identify the molecular cause of the binding change or establish effects on expression, stability, or intrinsic chemistry.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

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


---

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


---

# case-021 — Biotin ligase: single substitution characterization

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

The controlled comparison is miniTurbo versus G3Δ, not either variant versus canonical wild type. Both variants share all 11 substitutions listed for G3Δ and both deletions, covering reference positions 1–63 and position 146. miniTurbo has exactly one additional enzyme-core substitution: K194I. Thus, although both variants differ substantially from wild type, they differ from each other at only this one retained position.

The supplied cellular screening reports two distinct outcomes: adding K194I increases labeling activity, while the measured signal does not increase when exogenous biotin is omitted. The no-added-biotin condition is an operational background readout; it does not imply that cells contain no endogenous biotin. Likewise, an absence of increased signal does not establish zero background or a background reduction.

These observations directly support B: K194I raises activity in the G3Δ background without increasing the measured no-added-biotin signal.

A incorrectly asserts an increased background signal. C mistakes shared differences from wild type for differences between the compared cores. D contradicts the observed activity increase and additionally asserts a background reduction that is not supplied. The justified conclusion is therefore improved cellular labeling performance without an observed background increase, rather than a demonstrated change in any particular catalytic or binding mechanism.

## Final answer

B

## Astra’s stated limitations

These qualitative cellular readouts do not establish a molecular mechanism or distinguish effects on intrinsic catalysis from expression, stability, or other determinants of labeling. The conclusion applies to K194I in the G3Δ background under the supplied screening conditions, not necessarily to other backgrounds or assay constructs.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Biotin ligase** — [UniProt P06709](https://www.uniprot.org/uniprotkb/P06709/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly distinguishes the single difference between G3Δ and miniTurbo from their many shared differences relative to canonical wild type.
- Jointly interprets increased activity and unchanged no-added-biotin signal, without equating unchanged background with zero or reduced background.
- Keeps the conclusion specific to the tested background and cellular assay.

Source support:

- Supplementary Table 1; Methods subsection on miniTurbo evolution; final/intermediate variant comparison in Figure 1e–g
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- Published screening describes this comparison qualitatively; no unreported numerical effect size is supplied.
- Correction concerns Supplementary Tables 2–7; variant definitions here use Supplementary Table 1 and the stated main/supplementary figures.

Primary references:

- [Efficient proximity labeling in living cells and organisms with TurboID](https://pmc.ncbi.nlm.nih.gov/articles/PMC6126969/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-026 — PTEN phosphatase: mutation assay context and sensitivity

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

B is the most defensible interpretation: partial phosphatase function can support wild-type-like growth, so growth rescue does not establish fully wild-type activity in other assays.

Sequence context: The reference confirms Asp at position 92. Asp92 lies in PTEN’s catalytic-loop region, and replacing its carboxylate with an asparagine amide can alter catalytic chemistry. However, this sequence-based mechanistic consideration does not determine the magnitude of the activity change or establish complete inactivation.

Experimental observations: D92N resembles wild type in yeast growth rescue, whereas the PIP3 fluorescence reporter and in-vitro phosphatase assay report partial activity. These are distinct endpoints. The reporter reflects a cellular PIP3-related state, the biochemical assay assesses phosphatase function under its assay conditions, and growth is a downstream cellular phenotype rather than a direct measurement of enzymatic rate.

Mechanistic interpretation: The relationship between phosphatase function and growth need not be linear. For example, residual activity could exceed the threshold needed for near-maximal growth rescue, even while reporter and biochemical measurements remain detectably below wild type. Such a threshold or saturation effect is a compatible explanation, not a quantitatively established mechanism here. Consequently, the supplied results need not be contradictory.

Discriminating the choices: A incorrectly treats growth as a calibrated measure of enzymatic activity. C incorrectly assumes that normalization to each assay’s own wild-type control makes different readouts quantitatively interchangeable; normalization does not eliminate their different response relationships. D contradicts the supplied description of partial activity, which is not complete loss. B preserves the distinction between residual phosphatase function and its downstream growth consequence without claiming more than the evidence supports.

## Final answer

B

## Astra’s stated limitations

No quantitative relationship between growth, reporter output and biochemical activity is supplied. The observations do not establish an exact residual catalytic rate or uniquely explain why growth appears wild-type-like. The canonical sequence establishes residue numbering, not the complete assay constructs.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PTEN phosphatase** — [UniProt P60484](https://www.uniprot.org/uniprotkb/P60484/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly separates the downstream growth phenotype from PIP3 reporter and biochemical endpoints.
- Uses a residual-activity threshold or saturation relationship as an explicitly hypothetical explanation, rather than asserting a measured mechanism.
- Does not assert the paper's proposed deamidation explanation as established and does not infer an exact residual catalytic rate.

Source support:

- Discussion paragraph on the Asp92 discrepancy and D92N
- D92N appears WT-like in growth rescue but partially functional in PIP3 fluorescence or in-vitro phosphatase assays.

Source qualifications:

- The question does not determine an exact kinetic rate or which assay is universally superior.
- Deamidation is not established by these observations and must not be asserted as the demonstrated cause.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Mighell2018 Methods: NM_000314.6, corresponding 403-aa NP_000305; current canonical record cross-references NP_000305.3. Full paper-assay construct sequence still requires final replay before release.
- The paper proposes deamidation as a possible explanation, rather than establishing it. No mechanism of deamidation is required or taught as a fact here.

Primary references:

- [A Saturation Mutagenesis Approach to Understanding PTEN Lipid Phosphatase Activity and Genotype-Phenotype Relationships](https://pmc.ncbi.nlm.nih.gov/articles/PMC5986715/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-030 — Glucokinase / hexokinase-4: mutation kinetic mechanism comparison

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

The supplied transient-kinetic evidence separates glucose recognition into two microscopic steps:

E + glucose ⇌ E·glucose ⇌ E*·glucose

Here, E denotes glucose-free glucokinase, the first transition is initial glucose association, and the second is the subsequent conformational isomerization toward the active form, E*.

The reported effects map differently onto this pathway:
- A456V accelerates initial glucose binding to the glucose-free enzyme—the first step.
- W99R facilitates the subsequent isomerization toward the active form—the second step.

Thus, initial substrate association and conversion of the bound enzyme into an active conformation are distinct opportunities to enhance function. Similar functional gains need not reflect the same microscopic mechanism: one variant can accelerate glucose association, while another facilitates the conformational transition that follows. These observations concern the same glucokinase reaction and do not imply a new substrate, a new product, or faster chemical catalysis itself.

Choice C states this lesson correctly. A reverses the experimental assignments. B incorrectly assigns both reported effects to initial association, whereas W99R is associated with the later isomerization. D incorrectly assigns both effects to isomerization, whereas A456V is reported to accelerate initial association. The sequence establishes the variant identities; the supplied kinetic observations establish the mechanistic distinction.

## Final answer

C

## Astra’s stated limitations

The kinetic assignments come from the supplied experimental observations, not from sequence alone. They do not establish that either variant affects only one step, quantify overall turnover or equilibrium glucose affinity, or identify a unique structural cause. The canonical sequence supplies reference coordinates, not complete assay-construct sequences.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Glucokinase / hexokinase-4** — [UniProt P35557](https://www.uniprot.org/uniprotkb/P35557/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly assigns A456V to initial glucose association and W99R to the later active-form isomerization.
- The two-step reversible pathway accurately organizes the supplied kinetic observations.
- Distinguishes binding and conformational changes from chemical catalysis, avoids exclusive one-step claims, and does not invent kinetic constants or structural causes.

Source support:

- Primary abstract, Results describing transient kinetic analysis
- The abstract groups A456V with variants accelerating initial glucose binding and W99R with variants facilitating isomerization to the active form.

Source qualifications:

- Do not infer identical catalytic-efficiency ratios, abundance changes or glucose responses from these qualitative findings.
- The full paper-specific purified construct has not been replayed; numbering matches the canonical human reference.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Gersing2023 Methods: pancreatic isoform ENST00000403799.8; same transcript is cross-referenced by current P35557-1. Paper also identifies P35557 isoform1 in its sequence analysis.
- This case is based on verified qualitative findings in the primary abstract. No uninspected figure/table number or unreported kinetic constant is assigned.

Primary references:

- [Biochemical basis of glucokinase activation and the regulation by glucokinase regulatory protein in naturally occurring mutations](https://pubmed.ncbi.nlm.nih.gov/17082186/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-031 — PafA alkaline phosphatase: published enzyme mutation reasoning

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
For the published K162A variant, catalytic efficiency(kcat/KM) for the methyl-phosphate reaction, whose chemical step is rate-limiting, is reduced by more than10^6-fold relative to wild type. Vanadate binding is weakened much less, by about10^2-fold. Vanadate is a transition-state analog, not the actual reacting transition state. Use these reported within-assay effects; they are not a cellular-fitness measurement or a direct measurement of kcat alone.

**Question:** What is the most justified conclusion from the mismatch?

- **A.** The residual vanadate affinity establishes substantial transition-state stabilization, so most catalytic loss should be assigned to reduced active-enzyme abundance rather than chemistry.
- **B.** The methyl-phosphate efficiency loss establishes the same change in first-order turnover; the analog comparison then distinguishes that turnover defect from altered substrate binding.
- **C.** Real catalysis is disrupted much more than analog binding; residual TSA affinity cannot establish preserved transition-state stabilization or retained catalytic power.
- **D.** Weaker vanadate binding quantitatively determines the catalytic defect, so its affinity change provides the appropriate correction for interpreting the larger methyl-phosphate effect.


## Astra’s worked solution

C is the most justified conclusion: real catalytic efficiency is disrupted far more than vanadate binding, so residual analog affinity cannot establish preserved transition-state stabilization or catalytic power.

Sequence and construct context: The reference confirms Lys162. Replacing lysine with alanine removes a long side chain capable of electrostatic and hydrogen-bonding interactions, but the sequence alone does not establish which interaction is important. The reported effects concern the specified assay construct, not an assumed full-length native protein.

Observed mismatch: K162A reduces methyl-phosphate kcat/KM by more than 10^6-fold, whereas vanadate affinity weakens by only about 10^2-fold. Thus, the fold effects differ by roughly four or more orders of magnitude. These are different observables: kcat/KM measures productive catalytic efficiency, while vanadate affinity measures binding of a stable ligand.

Mechanistic interpretation: Vanadate is a transition-state analog, not the actual reacting transition state. An analog can reproduce some transition-state features without reproducing its complete geometry, charge distribution, or interactions along the reaction coordinate. Consequently, a mutation can affect analog binding much less than it affects the activation barrier for real catalysis. Moreover, catalytic transition-state stabilization is evaluated relative to the relevant reactant states; residual binding to an analog does not directly measure that energetic advantage.

The supplied fact that chemistry is rate-limiting makes the methyl-phosphate result informative about a chemical-step-limited reaction. It does not, however, convert kcat/KM into kcat or uniquely separate substrate binding from chemical conversion.

Why the alternatives fail:
• A: Residual vanadate affinity does not establish substantial stabilization of the actual transition state. It also provides no basis for assigning most of the catalytic-efficiency loss to reduced active-enzyme abundance.
• B: kcat/KM is a second-order efficiency, whereas kcat is a first-order turnover constant. Even when chemistry limits turnover, an efficiency change does not establish the same fold change in kcat. Vanadate binding also does not directly measure methyl-phosphate binding, and KM is not generally an equilibrium binding constant.
• D: The vanadate affinity change cannot quantitatively determine or correct the catalytic defect without a justified relationship between analog binding and real catalysis. The reported mismatch shows that their mutational effects do not quantitatively track one another here.

Therefore, retained vanadate binding demonstrates retained ability to bind that analog—not retained catalytic power.

## Final answer

C

## Astra’s stated limitations

The observations do not separately determine kcat, KM, substrate affinity, active-enzyme abundance, stability, or the microscopic role of Lys162. The conclusion concerns the reported methyl-phosphate and vanadate assays; it does not imply that transition-state analog binding is always uninformative.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- Correctly contrasts the greater-than-millionfold catalytic-efficiency loss with the roughly hundredfold affinity loss; the disparity is about four or more orders of magnitude.
- Explains the imperfect physical correspondence of a stable transition-state analog to the actual transition state, while distinguishing catalytic efficiency, first-order turnover and substrate affinity.
- Does not use residual analog binding to infer preserved catalytic power or to assign the defect to active abundance. Canonical Lys162 to expressed-ORF143 mapping is correct.

Source support:

- Fig.3A; Results: Active-Site and Second-Shell mutations; PDFpage4 / BioC passage21
- K162A is an active-site exception:>10^6-fold catalytic loss versus~10^2-fold weaker vanadate binding. MeP chemistry is the relevant rate-limiting comparison.

Source qualifications:

- Binding affinity weakens rather than increases; retain that direction.
- The result does not specify a unique structural cause or imply every TSA is uninformative.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Decoupling of catalysis and transition state analog binding from mutations throughout a phosphatase revealed by high-throughput enzymology](https://pmc.ncbi.nlm.nih.gov/articles/PMC10629569/). Fig.3A; Results: Active-Site and Second-Shell mutations; PDFpage4 / BioC passage21

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-003 — PafA alkaline phosphatase: published enzyme mutation reasoning

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
In wild-type PafA, Thr79 attacks the substrate phosphate and forms a covalent phospho-enzyme intermediate. The published T79G variant was used as a catalytically inactive control. Its eGFP signal showed that protein was expressed, and empty chambers were also retained to monitor local assay background.

**Question:** Which interpretation best connects the sequence change to the biochemical control?

- **A.** Comparable eGFP abundance makes remaining background activity an adequate estimate of intrinsic mutant turnover, provided the same normalization is applied to wild type.
- **B.** Removing Thr79's side-chain hydroxyl disrupts the usual covalent intermediate; an expression reporter does not demonstrate catalytic competence of the expressed PafA.
- **C.** T79G mainly reduces the amount of folded enzyme; matched eGFP abundance therefore isolates a selective folding defect rather than a catalytic defect.
- **D.** T79G primarily weakens phosphate-product binding; the reported loss of turnover therefore establishes product release as the rate-limiting step in the mutant.


## Astra’s worked solution

B best connects the sequence change to the biochemical control.

Sequence and experimental observations: The reference contains threonine at position 79. This position lies within the expressed reference segment 21–546 and maps to position 60 of the PafA-only expressed ORF; the omitted native N-terminal segment does not change which residue T79G denotes. The question explicitly identifies Thr79 as the nucleophile that attacks substrate phosphate and forms a covalent phospho-enzyme intermediate. That catalytic assignment comes from the supplied experimental information, not simply from finding a threonine in the sequence.

Mechanistic interpretation: Threonine has a side-chain hydroxyl whose oxygen can form the enzyme–phosphate bond. Glycine has a hydrogen side chain and lacks that hydroxyl. T79G therefore removes the functional group required for the usual Thr79-linked covalent intermediate. This provides a direct catalytic explanation for its reported use as an inactive control, without requiring an assumption that the protein was not expressed.

Control interpretation: The eGFP signal supports expression of the reporter-bearing construct. It does not establish that the PafA domain has a competent active site, is correctly folded, or contains the normal catalytic nucleophile. The stated observation also does not establish quantitatively matched abundance with wild type. Empty chambers monitor local assay background; a signal indistinguishable from that background is not evidence of intrinsic mutant turnover.

Why the other choices fail:
A: Even comparable eGFP abundance would not make background an adequate estimate of mutant catalysis. Applying the same expression normalization to wild type and mutant cannot convert background into enzyme-dependent turnover.
C: The evidence does not establish that reduced folding is the primary defect. Moreover, matched eGFP abundance would not isolate a PafA folding defect, because the reporter does not directly measure the folding of the PafA domain. Removal of the specified catalytic hydroxyl already supplies a mechanistic explanation.
D: No phosphate-product binding measurements or product-release kinetics are supplied. Loss of turnover after removing the catalytic nucleophile neither establishes weakened product binding nor identifies product release as rate-limiting.

Thus, the control demonstrates the distinction between detectable protein expression and catalytic competence, exactly as stated in B.

## Final answer

B

## Astra’s stated limitations

The supplied information does not quantify residual T79G turnover, the folded or active fraction of PafA, phosphate-product affinity, or individual catalytic rate constants. Additional structural effects of T79G cannot be excluded from sequence alone, but they are not needed to explain disruption of the specified catalytic mechanism.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- Correctly links removal of Thr79’s hydroxyl to loss of the normal covalent phospho-enzyme intermediate, without assuming loss of expression.
- Distinguishes the GFP reporter from active PafA, treats background as background, and does not invent a measured residual turnover or active fraction.
- Canonical Thr79 to expressed-ORF60 mapping is correct. Catalytic assignment is explicitly attributed to supplied observations rather than the sequence alone.

Source support:

- Fig.1A,H; Results: HT-MEK reproduces kinetic constants; BioC passages22 and24
- T79 is the covalent nucleophile; T79G lacks detectable activity and is used with empty chambers for local contamination/background controls.

Source qualifications:

- Do not assign exactly zero physical activity or a measured kcat to the inactive/upper-limit control.
- This addresses an already published substitution; it does not propose a new mutant or experiment.
- Expression and assay conditions are distinct. These standard on-chip conditions are not assigned to separate off-chip or tagless measurements without explicit source support.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Revealing enzyme functional architecture via high-throughput microfluidic enzyme kinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454890/). Fig.1A,H; Results: HT-MEK reproduces kinetic constants; BioC passages22 and24

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-006 — Glucokinase / hexokinase-4: mutation effect and measurement scope

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

The supported conclusion is improved functional performance in this assay, with the mechanism unresolved.

Glucokinase phosphorylates glucose to glucose-6-phosphate using ATP. In the supplied yeast complementation assay, growth depends on the human enzyme supporting glucose metabolism. W99R produces greater growth than wild type under the same tested glucose condition, so it provides stronger functional complementation.

However, growth is an integrated cellular outcome, not a direct measurement of purified-enzyme kinetics or protein abundance. Improved complementation could result from more functional enzyme being present, altered activity per enzyme molecule at the tested glucose concentration, or both. Expression, folding and stability can affect functional enzyme abundance; substrate interactions, conformational transitions and catalytic steps can affect per-molecule performance. None of these possible mechanisms is individually established by the reported growth comparison or by the W99R substitution itself.

Furthermore, growth need not be proportional to enzymatic flux. Therefore, a growth ratio cannot be interpreted as either a turnover-number ratio or an enzyme-abundance ratio. Testing one glucose condition also does not determine glucose-binding constants.

A reverses the functional interpretation of the supplied complementation result. B incorrectly claims that purified-enzyme turnover was measured independently of abundance. C incorrectly claims that abundance was measured independently of kinetics. D correctly states both the improved assay performance and the unresolved distinction between abundance and microscopic kinetic effects.

## Final answer

D

## Astra’s stated limitations

The supplied readout does not separately measure enzyme abundance, expression, stability, turnover number or glucose-binding constants. It establishes improved complementation under the tested glucose condition, not a unique molecular mechanism or an effect that necessarily generalizes to other conditions.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Glucokinase / hexokinase-4** — [UniProt P35557](https://www.uniprot.org/uniprotkb/P35557/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly reads greater W99R complementation under the tested condition.
- Explains why cellular growth need not scale linearly with enzymatic flux and cannot determine abundance or turnover ratios.
- Possible abundance, folding and kinetic contributions are presented as alternatives rather than claimed measurements.

Source support:

- Figure 1B and Results validating the yeast complementation assay
- W99R has higher activity than WT in the initial growth assay; F150S/R191W/G223S/G261R reduce function, while D217N/E279Q are WT-like.

Source qualifications:

- A higher growth readout is not itself a measured purified-enzyme turnover number.
- No clinical outcome or variant design recommendation follows from this question.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Gersing2023 Methods: pancreatic isoform ENST00000403799.8; same transcript is cross-referenced by current P35557-1. Paper also identifies P35557 isoform1 in its sequence analysis.
- The assay uses pancreatic glucokinase, ENST00000403799.8, and the paper identifies P35557 isoform 1. No exact kcat is supplied by Figure 1B.

Primary references:

- [A comprehensive map of human glucokinase variant activity](https://pmc.ncbi.nlm.nih.gov/articles/PMC10131484/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-007 — PafA alkaline phosphatase: published enzyme mutation reasoning

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
For the already tested surface substitutions D473V and D473G, use FC1=(mutant/WT efficiency on MecMUP)/(mutant/WT efficiency on MeP). The published FC1 effect exceeds60-fold for D473V but is less than twofold for D473G. Asp473 lies about20Å from the relevant active-site oxygen-interaction region. If a change in active fraction multiplied both measured efficiencies by the same factor, that factor would cancel in FC1.

**Question:** What follows most directly from these observations?

- **A.** The two substitutions share one distant position, so their different FC1 values primarily reflect total enzyme abundance rather than distinct local perturbations.
- **B.** The greater FC1 effect establishes a gain in absolute diester efficiency; unchanged active-fraction normalization makes that gain independent of monoester activity.
- **C.** The larger FC1 can reflect lower active-enzyme abundance without requiring a difference in the mutation's effects on the two substrates being compared.
- **D.** D473V perturbs the relative substrate responses more strongly; long-range coupling is consistent with this result, while absolute diester enhancement remains unestablished.


## Astra’s worked solution

D is the most direct conclusion.

1. Observations and indexing. The reference contains Asp at canonical position 473, corresponding to position 454 in the stated PafA-only expressed ORF. The observations concern the supplied HT-MEK PafA–eGFP construct, not an assumed full-length native protein. The reported FC1 effect exceeds 60-fold for D473V but is less than twofold for D473G. The approximately 20 Å separation from the relevant active-site oxygen-interaction region is also supplied experimental context, not something inferred from sequence alone.

2. FC1 measures relative substrate response. Let R_di = efficiency(mutant, MecMUP)/efficiency(WT, MecMUP), and R_mono = efficiency(mutant, MeP)/efficiency(WT, MeP). Then FC1 = R_di/R_mono. Consequently, the larger effect for D473V establishes a stronger perturbation of the relative diester-versus-monoester response. It does not establish that R_di exceeds 1. A large FC1 could arise from enhanced diester efficiency, depressed monoester efficiency, or decreases on both substrates with a larger decrease on the monoester.

3. A common active-fraction effect cancels. If a factor q representing a mutant/WT change in active fraction multiplies both substrate efficiencies equally, then R_di = q × r_di and R_mono = q × r_mono. Therefore FC1 = (q × r_di)/(q × r_mono) = r_di/r_mono. Such a shared abundance or active-fraction effect cannot by itself explain the FC1 difference. The active fraction need not remain unchanged for this cancellation to occur.

4. Mechanistic interpretation. Sharing a position does not make two substitutions equivalent. Both replacements remove the Asp carboxylate, but valine introduces a branched hydrophobic side chain, whereas glycine lacks a side chain beyond hydrogen and permits different backbone conformations. These differences could produce distinct local perturbations. Given the supplied distance, their differing substrate responses are consistent with long-range coupling to functional regions, without establishing a particular structural or dynamical mechanism.

A and C incorrectly explain the ratio through abundance alone without a substrate-dependent effect. B mistakes a ratio of effects for an absolute diester gain and overlooks the monoester denominator. D correctly states the relative-response conclusion while retaining the appropriate uncertainty about mechanism and absolute enhancement.

## Final answer

D

## Astra’s stated limitations

The individual substrate efficiencies are not supplied, so absolute diester enhancement cannot be established. The observations also do not identify a specific coupling pathway or distinguish altered binding, catalytic steps, or substrate-dependent conformational effects. Cancellation applies to a shared multiplicative active-fraction effect.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- Correctly defines the specificity ratio and explains why a large FC1 need not mean improved absolute diester activity.
- The shared active-fraction factor cancels algebraically even when the active fraction changes; the solution makes this condition explicit.
- Contrasts valine and glycine chemistry without claiming an observed atomic rearrangement or a proven long-range pathway. Canonical473 to ORF454 mapping is correct.

Source support:

- Fig.5B,F; text describing D473/L434/I451; BioC passage54
- D473V has anFC1 effect>60-fold versus<2-fold for D473G at a solvent-exposed residue about20Å away; a specific local-folding/allosteric interpretation is proposed.

Source qualifications:

- Distance is a structural observation, not proof of a particular communication route.
- The conformational explanation remains a model; FC1 is not kcat and not an absolute improvement measure.
- Expression and assay conditions are distinct. These standard on-chip conditions are not assigned to separate off-chip or tagless measurements without explicit source support.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Revealing enzyme functional architecture via high-throughput microfluidic enzyme kinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454890/). Fig.5B,F; text describing D473/L434/I451; BioC passage54

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-011 — PafA alkaline phosphatase: published enzyme mutation reasoning

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
For the published Y103G variant, protein made at23°C had wild-type-like activity, whereas the tagless protein made at37°C had about260-fold less activity. The study separately held reaction conditions constant when testing expression-temperature effects. Y103G made at the lower temperature had a wild-type-like circular-dichroism spectrum; protein made at the higher temperature had an altered spectrum. The tagless result was included to test whether eGFP caused the effect.

**Question:** Which explanation is best supported, without equating the activity difference to a260-fold change in the rate constant of every folded molecule?

- **A.** Expression history changes the long-lived active and inactive populations; the tagless result argues against an explanation confined to the eGFP reporter.
- **B.** Different expression temperatures shift the reversible folded-unfolded equilibrium during the subsequent assay; the activity difference therefore reports equilibrium stability under assay conditions.
- **C.** Higher-temperature expression uniformly slows catalysis in correctly folded molecules; the entire activity loss can therefore be assigned to their intrinsic chemical-step rate constant.
- **D.** Temperature-dependent GFP maturation biases the enzyme-concentration estimate; the tagless result therefore attributes the activity difference primarily to reporter calibration rather than PafA.


## Astra’s worked solution

A is best supported: expression history changes the persistent functional populations of PafA, and the tagless result argues against a reporter-only explanation.

Sequence and construct: The reference contains Tyr103, so Y103G is a Tyr-to-Gly substitution within the retained PafA portion of the assay construct, not within the omitted N-terminal segment or eGFP. Removing an aromatic side chain and introducing glycine can affect folding and conformational preferences, but sequence alone does not establish the affected interaction or the mutation’s functional consequence.

Experimental evidence: Protein produced at 23°C had wild-type-like activity and a wild-type-like circular-dichroism spectrum. Higher-temperature production yielded an altered spectrum, and tagless protein produced at 37°C showed the approximately 260-fold activity loss. Crucially, reaction conditions were held constant when expression-temperature effects were tested. The comparison therefore concerns the consequences of protein production history, not simply the direct temperature dependence of an enzyme reaction.

Mechanistic interpretation: The coupled changes in activity and circular dichroism support different conformational ensembles being generated during production. An active-like population and a poorly active or inactive population could persist into the subsequent assay because their interconversion is slow on the measurement timescale. The altered spectrum supports structural differences in the ensemble, although it does not identify a particular misfolded state or prove that every high-temperature-produced molecule is inactive.

Why the activity ratio is not a chemical-step rate ratio: For activity normalized to total PafA, a simple population model is a_observed ≈ f_active × a_active when the inactive population contributes negligibly. Here a_active is the per-active-molecule activity under the assay conditions. A large reduction in f_active can therefore produce a large activity loss without a corresponding reduction in every active molecule’s catalytic rate. The observations do not separately determine these factors. Moreover, an overall activity measurement does not necessarily isolate the intrinsic chemical step.

Discriminating the alternatives:
• B incorrectly interprets production-temperature dependence as equilibrium stability during the assay. A reversible folding equilibrium established under identical assay conditions should not retain expression-history dependence. These observations instead support persistent states and do not measure equilibrium stability.
• C assigns the entire loss uniformly to correctly folded molecules’ chemical-step rate constants. Neither the bulk activity nor the altered circular-dichroism spectrum justifies that assignment.
• D reverses the significance of the tagless control. A large effect without eGFP cannot be explained solely by GFP maturation or GFP-based concentration calibration. The result argues against an explanation confined to the reporter, as stated in A.

## Final answer

A

## Astra’s stated limitations

The observations do not identify the inactive conformation, quantify active-state fractions or interconversion rates, or establish that all remaining active molecules have unchanged intrinsic kinetics. Sequence alone cannot determine Tyr103’s structural role or predict this temperature-dependent phenotype.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PafA alkaline phosphatase** — [UniProt Q9KJX5](https://www.uniprot.org/uniprotkb/Q9KJX5/entry).

Source-supported reference answer: **A**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- Separates expression temperature from reaction temperature and correctly interprets persistence under matched assays as support for long-lived functional populations.
- The population equation separates active fraction from per-active-molecule activity; the260-fold bulk loss is not misreported as a260-fold chemical-step kcat change.
- Uses the tagless and circular-dichroism controls appropriately, without claiming a unique inactive structure or unchanged kinetics of every remaining active molecule. Canonical103 to ORF84 mapping is correct.

Source support:

- Fig.3D–K; TableS6; Figs.S39–S40 and TableS7; BioC passages38,41,43
- The tagless Y103G test gave wild-type-like activity after23°C expression and260-fold less after37°C expression; CD spectra differed. Standard expression-history tests used matched23°C/100μMZn assays.

Source qualifications:

- Do not claim that a CD change proves a unique atomic structure or equilibrium-unfolding mechanism.
- The exact reporter-free terminal tag sequence was not independently reconstructed; canonical PafA mutation numbering is verified, and the tagless condition is kept separate from the deposited eGFP construct.
- Initiating M followed by canonical Q9KJX5 residues21–546; linker/eGFP omitted from PafA-only ORF translation. This is an experimental truncation, not a claim about the natural signal-peptide cleavage position.
- Canonical residue n (21<=n<=546) maps to one-based PafA_ORF residue n-19. GenBank T79 feature265..267 mapsORF60; N100328..330 mapsORF81; K162514..516 mapsORF143; R164520..522 mapsORF145.
- On-chip PafA was fused to a Ser-Gly linker and eGFP. Canonical numbering of the PafA segment is retained; neither reporter sequence nor linker is treated as PafA.
- The source separately reports a reporter-free Y103G control. Do not conflate its260-fold expression-temperature effect with a specific on-chip numeric ratio.

Primary references:

- [Revealing enzyme functional architecture via high-throughput microfluidic enzyme kinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC8454890/). Fig.3D–K; TableS6; Figs.S39–S40 and TableS7; BioC passages38,41,43

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-017 — APEX peroxidase: published variant comparison

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

The relevant comparison is against the APEX parent, not against canonical wild type. All three variants share K14D, W41F, and E112K. Subtracting these shared substitutions gives:

- APEX2 relative to APEX: A134P only.
- VPGAPEX relative to APEX: A19V, A134P, and D222G.
- VPGAPEX relative to APEX2: A19V and D222G.

There are no listed deletions. Thus, APEX2 and VPGAPEX share A134P but do not carry identical sets of additional substitutions.

The supplied assay observations state that the evolved variants improved on APEX, while follow-up assays did not distinguish APEX2 from VPGAPEX. Therefore, APEX2 shows improved performance with one added substitution in the APEX background. The two further substitutions present in VPGAPEX are not associated with any additional improvement detected in those assays. This is exactly choice B.

Choice A is incorrect because the additional mutation sets differ. Choice C contradicts the observed improvement over APEX. Choice D claims a further gain over APEX2 that the assays did not detect.

The reusable principle is that mutation count does not determine phenotype: additional substitutions need not produce additive gains. Here, the evidence supports a shared improved assay outcome despite different genotypes, without establishing the individual effects or molecular mechanisms of the extra VPGAPEX substitutions.

## Final answer

B

## Astra’s stated limitations

The observations establish a comparative assay outcome, not its molecular mechanism. They do not distinguish effects on intrinsic catalysis, expression, stability, or other assay-dependent factors. Failure to distinguish APEX2 from VPGAPEX does not prove biochemical equivalence or show that A19V and D222G are individually neutral. The supplied sequence defines canonical coordinates, not the complete tagged assay construct.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **APEX peroxidase** — [UniProt Q43758](https://www.uniprot.org/uniprotkb/Q43758/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly subtracts shared substitutions against the APEX parent and distinguishes the two extra VPGAPEX changes.
- Connects that genotype comparison to the assay result without equating nondetection of a difference with biochemical equivalence or individual mutation neutrality.
- The explanation teaches why additional substitutions need not yield additive gains.

Source support:

- Figure 1a; first Results section identifying evolved clones; Figure 2a–b
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- Indistinguishable in reported assays does not mean identical under every conceivable condition.
- Use corrected Figure 2a symbols and Figure 2e axis labels; correction dated December 10, 2014.

Primary references:

- [Directed evolution of APEX2 for electron microscopy and proximity labeling](https://www.nature.com/articles/nmeth.3179)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-018 — PTEN phosphatase: mutation substrate specificity

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

Y138L replaces the reference Tyr138 with leucine, removing an aromatic, hydroxyl-bearing side chain. That chemical change alone cannot determine which phosphatase reaction will be affected; the supplied assays provide the decisive evidence.

The two readouts must be considered separately:
- Lipid substrate: kinetic analysis found Y138L activity against PIP3 essentially indistinguishable from wild type under the tested conditions. This supports preservation of the tested lipid phosphatase activity.
- Protein-substrate preparation: activity against phosphorylated poly(Glu,Tyr) was approximately 3% of wild type, corresponding to roughly a 97% reduction, and was frequently undetectable. This supports a severe loss of the tested protein-substrate activity. Undetectability does not establish that activity is absolutely zero.

Different substrates impose different recognition and productive-positioning requirements on an enzyme. Consequently, retaining lipid dephosphorylation does not require retaining the protein-substrate reaction. Preserved PIP3 activity argues against uniform catalytic inactivation under these conditions, while the protein-substrate result demonstrates a strongly substrate-dependent impairment. A single total-activity label would conceal this distinction.

A is inconsistent with the reduced, rather than increased, protein-substrate activity. B incorrectly assigns the approximately 3% result to both substrates. C reverses the observed pattern. D correctly describes preserved tested lipid activity together with strongly reduced protein-substrate activity.

## Final answer

D

## Astra’s stated limitations

The conclusion applies to PIP3 and phosphorylated poly(Glu,Tyr) under the tested conditions, not necessarily to every physiological substrate. These readouts do not establish whether the protein-substrate defect arises from altered binding, productive substrate positioning, or catalytic chemistry, and they do not separately measure expression or stability.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PTEN phosphatase** — [UniProt P60484](https://www.uniprot.org/uniprotkb/P60484/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly separates preserved PIP3 activity from approximately 3% protein-substrate activity and computes the corresponding approximately 97% reduction.
- Correctly distinguishes frequently undetectable activity from a demonstrated absolute zero.
- Explains different substrate-recognition and positioning requirements without claiming that the precise microscopic cause was measured.

Source support:

- Figure 1e/f; Figure 2 and Supplementary Figure S2; Results following the initial mutant screen
- Y138L lipid activity is essentially indistinguishable from WT, whereas polyGluTyr-P activity is approximately 3% of WT and often undetectable.

Source qualifications:

- The answer applies to the tested substrates and conditions.
- Do not infer unchanged thermal stability or cellular expression from these activity readouts.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Mighell2018 Methods: NM_000314.6, corresponding 403-aa NP_000305; current canonical record cross-references NP_000305.3. Full paper-assay construct sequence still requires final replay before release.
- Figure 1d describes GST fusion production and tag removal. The exact full assay construct sequence has not been independently reconstructed.

Primary references:

- [Suppression of cellular proliferation and invasion by the concerted lipid and protein phosphatase activities of PTEN](https://pmc.ncbi.nlm.nih.gov/articles/PMC2816976/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-020 — adenylate_kinase: mutation kinetic reasoning

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

The supplied sequence confirms that both substitutions replace arginine, but at different positions. Arg-to-Ala removes the guanidinium group, including its electrostatic and hydrogen-bonding capabilities, and substantially reduces side-chain size. Identical substitution chemistry therefore does not imply identical functional consequences.

Quantitative comparison:

| Enzyme | kcat (s^-1) | ATP Km (µM) | kcat/Km (M^-1 s^-1) |
|---|---:|---:|---:|
| WT | 330 | 71 | 4.65 × 10^6 |
| R36A | 55 | 89 | 6.18 × 10^5 |
| R123A | 0.28 | 110 | 2.55 × 10^3 |

R36A decreases turnover by 330/55 = 6-fold. R123A decreases turnover by 330/0.28 ≈ 1,180-fold and turns over approximately 196-fold more slowly than R36A. In contrast, their ATP Km values are only about 1.25-fold and 1.55-fold the WT value. Thus, the striking difference is in turnover capacity, not ATP half-saturation.

For the fitted Michaelis–Menten ATP dependence at fixed other assay conditions, v/[E] = kcat[ATP]/(Km + [ATP]). Increasing ATP approaches the turnover ceiling kcat; changing Km changes how that ceiling is approached, not its height. Moreover, Km is a kinetic parameter and is not generally equal to the equilibrium dissociation constant Kd. Consequently, the modest Km increase cannot explain R123A's approximately thousand-fold decrease in kcat as simply weaker equilibrium ATP binding.

Adenylate kinase catalyzes phosphoryl transfer in ATP + AMP ⇌ 2 ADP. Depending on their three-dimensional positions, arginine residues can contribute differently to nucleotide positioning, transition-state electrostatics, or formation of catalytically competent conformations. The results are consistent with Arg123 making a substantially more consequential contribution to the turnover cycle under these conditions. They do not establish which microscopic step is affected: steady-state kcat can reflect chemistry, conformational changes, and product release.

The alternatives fail for distinct reasons:
• A: Turnover ratios are not direct measurements of folded fractions. That interpretation would require unsupported assumptions that the only defect is loss of active molecules and that the remaining active molecules retain WT turnover.
• C: Km is not an equilibrium-binding measurement, and its modest increase cannot account for the greatly reduced ATP-saturated turnover ceiling.
• D: kcat/Km is a low-ATP catalytic-efficiency measure, not a correction that makes turnover ceilings equivalent. These efficiencies still differ by approximately 243-fold between R36A and R123A.

Therefore, the most consistent explanation is that the same charge-removing substitution has different consequences because the two positions make different functional contributions. Answer: B.

## Final answer

B

## Astra’s stated limitations

The measurements support different effects on catalytic turnover but do not identify the precise atomic roles of Arg36 and Arg123, isolate the rate-limiting step, or establish protein-folding fractions. ATP Km alone does not determine equilibrium ATP affinity.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **adenylate_kinase** — [UniProt P69441](https://www.uniprot.org/uniprotkb/P69441/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

Correct remapped answer B. Correctly converts the efficiencies to M^-1 s^-1 and calculates 6-fold versus about 1180-fold WT turnover losses, about 196-fold difference in mutant turnover and about 243-fold difference in mutant catalytic efficiencies. Explains why half-saturation changes do not determine the turnover ceiling. Gives plausible position-specific catalytic roles while explicitly declining to identify exact contacts, folded fractions or a microscopic rate-limiting step.

Source support:

- 2021 Figure 2c / Table S2; 2023 Table 1, WT, R36A and R123A rows.
- Published ATP-dependent measurements: WT kcat = 330 s^-1, ATP Km = 71 micromolar; R36A kcat = 55 s^-1, Km = 89 micromolar; R123A kcat = 0.28 s^-1, Km = 110 micromolar. Both substitutions replace one arginine with alanine in the same enzyme.
- Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.
- Table 1, footnote a.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. Published R36, R88, R123, R156 and R167 all match the reference residues.
- The prompt supplies the verified canonical reference and published mutation labels. No unreported affinity tag, cloning scar or exact expressed-construct extension is inferred.

Primary references:

- [Dynamic Connection between Enzymatic Catalysis and Collective Protein Motions](https://pmc.ncbi.nlm.nih.gov/articles/PMC8297476/). Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.

- [Mechanistic basis for a connection between the catalytic step and slow opening dynamics of adenylate kinase](https://pmc.ncbi.nlm.nih.gov/articles/PMC11779523/). Table 1, footnote a.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-025 — APEX peroxidase: mutation effect localization controls

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

A is supported by the assay observations.

The supplied variant definitions show that APEX2 is APEX plus A134P, with no deletions. This identifies the sequence difference, but the substitution alone does not predict its functional effect; the experimental comparison supplies that evidence.

Under matched outer-mitochondrial-membrane targeting, APEX2 strongly enriches the proximal markers Tom70 and Tom20, whereas APEX barely enriches them. Crucially, this stronger proximal signal is not accompanied by similarly strong enrichment of the other tested compartments: the mitochondrial-matrix marker ATP5B is not enriched, and the ER-membrane marker BCAP31 is only slightly enriched. Similar construct expression also argues against a large increase in reporter abundance as the explanation.

APEX proximity labeling uses peroxidase chemistry to generate locally acting labeling intermediates that modify nearby accessible proteins. Thus, the pattern supports more effective proximal-marker labeling and recovery while retaining substantial spatial discrimination among the tested markers. Enrichment is not a direct measurement of reporter–marker binding affinity or an isolated catalytic parameter.

The alternatives conflict with specific observations:
- B predicts equal mitochondrial- and ER-membrane-marker enrichment, contrary to the weak BCAP31 signal.
- C predicts strong matrix-marker enrichment, contrary to the ATP5B result.
- D predicts much higher APEX2 expression, contrary to the similar expression of the construct pairs.

Therefore, A best captures both the enhanced proximal signal and the absent or much weaker enrichment of the supplied other-compartment markers.

## Final answer

A

## Astra’s stated limitations

The conclusion is restricted to the supplied markers and assay conditions. The data do not establish complete absence of off-target labeling or determine whether A134P changes intrinsic catalysis, stability, active-enzyme fraction, or substrate specificity.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **APEX peroxidase** — [UniProt Q43758](https://www.uniprot.org/uniprotkb/Q43758/entry).

Source-supported reference answer: **A**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Combines comparable expression, stronger proximal-marker enrichment and weak or absent other-compartment markers.
- Correctly separates increased reporter performance from indiscriminate labeling or higher protein abundance.
- Explains proximity-labeling chemistry while avoiding claims of direct reporter–marker binding or an isolated kinetic effect.

Source support:

- Figure 2c and accompanying Results
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- Proximity enrichment does not demonstrate direct physical binding to the reporter.
- Use corrected Figure 2a symbols and Figure 2e axis labels; correction dated December 10, 2014.

Primary references:

- [Directed evolution of APEX2 for electron microscopy and proximity labeling](https://www.nature.com/articles/nmeth.3179)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

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


---

# case-028 — adenylate_kinase: mutation kinetic reasoning

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

Both fold-loss calculations use WT turnover with Mg2+, 330 s^-1, as the reference.

1. Mg2+ removal from WT: 330 / 0.0075 = 44,000-fold lower turnover.
2. R167A in the Mg2+-containing comparison: 330 / 2.4 = 137.5-fold lower turnover, approximately 140-fold.

Thus, R167A retains only about 0.73% of WT turnover despite Mg2+ being present. Under these assay conditions, the cofactor does not replace the contribution lost upon substituting Arg167.

Biologically, adenylate kinase catalyzes ATP + AMP ⇌ 2 ADP. Mg2+ commonly assists phosphoryl-transfer reactions by coordinating nucleotide phosphates, organizing reacting groups, and stabilizing charge. An arginine side chain can contribute electrostatic stabilization or active-site organization; alanine lacks its positively charged group. These are plausible mechanisms for the residue's contribution, not proof of a particular contact or catalytic role at position 167. The direct experimental observation is the substantial turnover deficit in the Mg2+-containing mutant assay.

The alternatives differ as follows:
- A gives both correct ratios and the supported conclusion that Mg2+ presence does not restore WT turnover to R167A.
- B incorrectly equates turnover losses with binding-affinity losses. kcat measures catalytic turnover, whereas binding affinity requires separate binding information; their ratios are not interchangeable.
- C incorrectly asserts obligatory rescue by ATP. Increasing substrate occupancy does not, by itself, remove a lower catalytic turnover limit, and no ATP-dependent rescue is reported.
- D reverses the two quantitative effects: Mg2+ removal produces the approximately 44,000-fold loss, while R167A with Mg2+ produces the approximately 140-fold loss.

Answer: A.

## Final answer

A

## Astra’s stated limitations

The turnover measurements do not establish binding affinities, protein stability, or the precise catalytic step affected by R167A. The conclusion about incomplete compensation by Mg2+ applies to the supplied Mg2+-containing comparison.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **adenylate_kinase** — [UniProt P69441](https://www.uniprot.org/uniprotkb/P69441/entry).

Source-supported reference answer: **A**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

Correct remapped answer A. Calculates 44000-fold loss without Mg2+ and 137.5-fold loss for R167A with Mg2+, plus about 0.73% retained mutant turnover. Correctly confines the lack of compensation to the supplied Mg2+-containing comparison. General phosphate-coordination and electrostatic explanations are labeled plausible rather than experimentally established Arg167 contacts. Does not confuse turnover ratios with affinities or assert an unmeasured ATP-rescue result.

Source support:

- 2021 main-text Mg2+ paragraph and Figure S9; arginine data in Figure 2c / Table S2, reproduced in 2023 Table 1.
- The primary study reports WT kcat = 330 s^-1 with Mg2+ and 0.0075 s^-1 without Mg2+. The published R167A variant has kcat = 2.4 s^-1 in the Mg2+-containing kinetic comparison. These are reported turnover measurements; they are not Mg2+ binding-affinity measurements.
- Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.
- Table 1, footnote a.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. Published R36, R88, R123, R156 and R167 all match the reference residues.
- The prompt supplies the verified canonical reference and published mutation labels. No unreported affinity tag, cloning scar or exact expressed-construct extension is inferred.

Primary references:

- [Dynamic Connection between Enzymatic Catalysis and Collective Protein Motions](https://pmc.ncbi.nlm.nih.gov/articles/PMC8297476/). Figure 2c and supporting Table S2 for arginine variants; main-text Mg2+ comparison and Figure S9.

- [Mechanistic basis for a connection between the catalytic step and slow opening dynamics of adenylate kinase](https://pmc.ncbi.nlm.nih.gov/articles/PMC11779523/). Table 1, footnote a.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-029 — Biotin ligase: deletion effect substrate controls

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

D integrates both supplied observations.

The substrate-depletion control shows that G3 labeling depends on available biotin: labeling occurs in regular medium without exogenous biotin, but disappears in biotin-depleted medium. “Without exogenous biotin” therefore does not mean “without biotin.” Ambient biotin in the regular-medium condition can supply the substrate needed for pre-addition labeling.

The variant comparison addresses a different issue: the magnitude of that pre-addition signal. G3 and G3Δ share all listed internal substitutions and the deletion at reference position 146. G3Δ additionally lacks reference residues 1–63 and shows reduced pre-addition labeling. Thus, the supplied comparison supports an association between the N-terminal deletion and reduced background labeling under the tested conditions; it does not identify a particular binding or catalytic mechanism.

The alternatives conflict with the supplied facts:
- A incorrectly says G3 labeling persists after biotin depletion; the signal disappears.
- B incorrectly says the N-terminal deletion leaves labeling unchanged; the comparison shows a reduction.
- C incorrectly identifies the isolated change as the internal A146 deletion and says both variants retain the same N-terminal region. The internal deletion is shared, whereas residues 1–63 are removed only in G3Δ.

Therefore, ambient biotin supports G3 pre-addition labeling, and the published N-terminal deletion reduces that signal in the tested comparison.

## Final answer

D

## Astra’s stated limitations

The observations establish substrate dependence and reduced labeling in the deletion comparison, but not the molecular mechanism of that reduction. They do not distinguish altered biotin binding or catalytic activity from differences in enzyme abundance or stability, nor show that G3Δ eliminates background labeling entirely. The reference sequence excludes assay tags and fusions.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Biotin ligase** — [UniProt P06709](https://www.uniprot.org/uniprotkb/P06709/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly uses biotin depletion to distinguish no added biotin from absence of available substrate.
- Compares the distinguishing N-terminal deletion against the shared internal deletion and substitutions.
- Explains the reduced background phenotype without inventing a binding constant, altered catalytic mechanism or complete elimination of background.

Source support:

- Supplementary Figure 3e; Supplementary Table 1
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- This cellular phenotype does not supply a measured binding constant or uniquely establish the molecular cause of the deletion effect.
- Correction concerns Supplementary Tables 2–7; variant definitions here use Supplementary Table 1 and the stated main/supplementary figures.

Primary references:

- [Efficient proximity labeling in living cells and organisms with TurboID](https://pmc.ncbi.nlm.nih.gov/articles/PMC6126969/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-005 — Biotin ligase: mutation effect timecourse interpretation

**Assistant selection tier: moderate.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

C correctly distinguishes faster cellular product accumulation from a purified-enzyme kinetic measurement.

The supplied observation is that TurboID at 10 minutes produces nearly comparable expression-normalized biotinylated product to older ligases, including BioID, at 18 hours. Since 18 hours equals 1,080 minutes, the accumulation windows differ by 1,080/10 = 108-fold. Thus, TurboID reaches a similar reported product endpoint in a much shorter interval under the cellular assay conditions.

Expression normalization adjusts the comparison for measured ligase abundance; it does not change the elapsed labeling times or turn endpoint signals into turnover numbers. Covalent biotinylation products accumulate over time, and their cellular abundance can depend on substrate accessibility, effective enzyme activity, and product persistence. A purified turnover number, kcat, instead describes catalytic turnovers per active enzyme per unit time under defined kinetic conditions. The supplied endpoint comparison does not directly measure that parameter or its ratio between variants. Even dividing endpoint signal by elapsed time would not by itself establish a purified kcat ratio.

The alternatives fail for distinct reasons:
- A incorrectly treats the 108-fold duration difference as a directly measured purified turnover-number ratio.
- B incorrectly equates expression normalization with time matching; the windows remain 10 minutes and 18 hours.
- D contradicts the stated quantitation: the ligase self-biotinylation band was excluded, so the quantified signal is not exclusively self-labeling.

Therefore, the supported interpretation is faster accumulation of comparable normalized non-self cellular biotinylation product, without a direct purified-turnover inference.

## Final answer

C

## Astra’s stated limitations

These cellular endpoints do not establish a purified turnover-number ratio or identify which sequence changes cause faster labeling. The supplied canonical sequence is a coordinate reference, not the complete tagged assay construct.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Biotin ligase** — [UniProt P06709](https://www.uniprot.org/uniprotkb/P06709/entry).

Source-supported reference answer: **C**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly distinguishes a 108-fold endpoint-duration difference from an intrinsic turnover-number ratio.
- Expression normalization and exclusion of self-biotinylation are handled correctly.
- The decisive distinction is already stated in the supplied observations, so the question is relatively easy evidence reading despite a useful explanation.

Source support:

- Figure 2a–b; normalization in Figure 1g; accompanying Results
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- Do not translate elapsed-time ratios into an unmeasured catalytic constant.
- Correction concerns Supplementary Tables 2–7; variant definitions here use Supplementary Table 1 and the stated main/supplementary figures.

Primary references:

- [Efficient proximity labeling in living cells and organisms with TurboID](https://pmc.ncbi.nlm.nih.gov/articles/PMC6126969/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-013 — Biotin ligase: published variant tradeoff

**Assistant selection tier: moderate.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

A is supported by both supplied observations: miniTurbo has lower overall cellular labeling activity than TurboID, and it produces less labeling before exogenous biotin addition. The annotation must preserve both findings rather than treating reduced background as evidence of equally strong or stronger induced labeling.

Mechanistically, biotin-dependent proximity-labeling enzymes can use biotin already available in cells. Therefore, before exogenous biotin addition does not necessarily mean before any labeling can occur. Reduced pre-addition labeling supports lower temporal background, whereas overall labeling strength is a separate performance dimension. This does not demonstrate an absolute off state or a particular activation speed.

The sequence definitions also prevent a single-change causal interpretation. miniTurbo lacks canonical residues 1–63, which TurboID retains, and their substitution sets differ. The cellular observations therefore compare complete variants with multiple differences; they do not isolate the effect of the N-terminal deletion or any individual substitution.

The alternatives fail as follows:
- B reverses both observations, claiming stronger overall labeling and more pre-addition labeling for miniTurbo.
- C correctly states reduced pre-addition labeling but replaces the reported activity reduction with an unsupported claim of equal activity after addition.
- D retains the lower-activity distinction but contradicts the observed reduction in pre-addition labeling.

Thus A correctly separates miniTurbo's lower pre-addition background from TurboID's stronger overall labeling activity.

## Final answer

A

## Astra’s stated limitations

The observations are qualitative cellular comparisons. They do not establish zero pre-addition labeling, a better induced-to-background ratio, or precise switching kinetics. They also cannot separate contributions from catalysis, biotin binding, expression, stability, or assay-construct context, nor assign the differences to a particular mutation or deletion. The reference sequence is not the complete tagged assay construct.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Biotin ligase** — [UniProt P06709](https://www.uniprot.org/uniprotkb/P06709/entry).

Source-supported reference answer: **A**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly preserves both the lower overall activity and lower pre-addition labeling findings.
- Explains endogenous biotin and avoids claiming zero background, a superior induced/background ratio, or isolated causality from a multimutant comparison.
- The answer is mainly a careful synthesis of two explicitly supplied qualitative observations.

Source support:

- Figure 2a–b; Supplementary Figure 6; accompanying Results
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- This compares published multimutant variants; it does not isolate a single causal substitution.
- Correction concerns Supplementary Tables 2–7; variant definitions here use Supplementary Table 1 and the stated main/supplementary figures.

Primary references:

- [Efficient proximity labeling in living cells and organisms with TurboID](https://pmc.ncbi.nlm.nih.gov/articles/PMC6126969/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-014 — Glucokinase / hexokinase-4: mutation comparator interpretation

**Assistant selection tier: moderate.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

The reported comparison directly supports B: F150S produces lower growth-based functional performance than wild type, whereas D217N and E279Q are approximately wild-type-like in the same yeast complementation assay. Thus, F150S performs worse than the two comparators in this cellular readout. No finer ranking between D217N and E279Q is established.

Glucokinase catalyzes ATP-dependent phosphorylation of glucose. Yeast complementation reports whether the expressed enzyme supports cellular function, rather than measuring an isolated molecular property. Reduced growth can reflect less protein, a smaller correctly folded or stable protein population, altered catalytic kinetics under cellular conditions, or combinations of these effects. The supplied observations do not distinguish those possibilities.

The reference sequence confirms that F150S is a chemically nonconservative substitution. Such a change could affect protein interactions or conformational behavior, but neither the residue identity nor the growth result proves a particular folding, abundance, or catalytic defect. Likewise, the acidic-to-amide substitutions in the two comparators cannot be assumed biochemically neutral merely because their growth performance is approximately wild-type-like.

A contradicts the reported performance of D217N and E279Q. C asserts an abundance measurement that was not supplied and unjustifiably excludes folding and kinetic contributions, which can coexist with abundance changes. D reverses the observed comparison. B alone preserves both the measured functional ranking and the uncertainty about its molecular cause.

## Final answer

B

## Astra’s stated limitations

The molecular cause of the F150S growth defect is unresolved because no matched abundance measurements or purified-enzyme kinetics are supplied. Approximately wild-type-like growth also does not establish identical biochemical behavior under other conditions.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Glucokinase / hexokinase-4** — [UniProt P35557](https://www.uniprot.org/uniprotkb/P35557/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly ranks F150S below the two near-wild-type comparators without inventing a finer D217N-versus-E279Q ranking.
- Residue identities and side-chain chemistry are correct; abundance, folding and kinetic explanations remain possibilities rather than measured causes.
- The main inference is reading the supplied assay comparison; the response does not establish a specific molecular mechanism.

Source support:

- Figure 1B; Results describing initial assay validation
- F150S is among the function-reducing test variants; D217N and E279Q are WT-like.

Source qualifications:

- No exact magnitude or confidence interval is invented from the qualitative comparison.
- The assay does not isolate protein abundance, folding stability, substrate affinity or turnover in this question.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Gersing2023 Methods: pancreatic isoform ENST00000403799.8; same transcript is cross-referenced by current P35557-1. Paper also identifies P35557 isoform1 in its sequence analysis.
- These are observed test-variant results, not imputed values from unmeasured variants.

Primary references:

- [A comprehensive map of human glucokinase variant activity](https://pmc.ncbi.nlm.nih.gov/articles/PMC10131484/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-022 — Glucokinase / hexokinase-4: mutation chemistry and position dependence

**Assistant selection tier: moderate.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

A is the justified generalization.

Sequence and chemical observations: The reference contains Asp at position 217 and Glu at position 279. Asp and Glu have acidic carboxylate side chains; their respective replacements, Asn and Gln, have neutral polar amide side chains. These substitutions therefore neutralize a negative charge. They neither preserve that charge nor introduce a positive charge.

Experimental interpretation: Both variants show wild-type-like functional performance in the supplied pancreatic human glucokinase complementation assay. Thus, loss of the acidic side-chain charge is tolerated for these particular substitutions at these two positions in that measured context. This conclusion comes from the supplied functional observations, not from sequence inspection alone.

Mechanistic scope: Retaining similar side-chain size and polarity may help preserve some interactions, but the observations do not identify why these variants perform well. Acidic residues elsewhere can have different roles in local electrostatics, substrate interactions, catalysis, or structural stability. Consequently, the same type of chemical substitution need not have the same functional effect at another position. Likewise, wild-type-like complementation does not establish that every underlying molecular property or kinetic parameter is unchanged.

Discriminating the alternatives:
- B is chemically incorrect: Asn and Gln do not retain the original negatively charged carboxylate groups.
- C is chemically incorrect: these replacements are neutral amides, not positively charged side chains, so neither substitution is a negative-to-positive charge reversal.
- D overgeneralizes two position-specific observations into a rule for every acidic residue. The supplied evidence does not support that extrapolation.

A correctly limits the conclusion to the tested positions and assay context.

## Final answer

A

## Astra’s stated limitations

The supplied evidence concerns these two substitutions in a pancreatic human glucokinase complementation assay. It does not establish identical kinetics across glucose conditions, independently unchanged binding, expression or stability, or the effects of substitutions at other acidic residues.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **Glucokinase / hexokinase-4** — [UniProt P35557](https://www.uniprot.org/uniprotkb/P35557/entry).

Source-supported reference answer: **A**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly describes acidic-to-neutral-amide side-chain changes and does not call either replacement positively charged.
- Correctly restricts the functional conclusion to the two tested positions and the assay context.
- Most of the chemistry and functional facts are already given in the question; the added interpretation is useful but not a newly inferred enzyme mechanism.

Source support:

- Figure 1B; Results validating the assay with common variants
- D217N and E279Q are described as WT-like in the yeast functional assay.

Source qualifications:

- WT-like complementation does not mean all microscopic constants are identical.
- No claim is made that these positions are universally nonessential across all cellular settings.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Gersing2023 Methods: pancreatic isoform ENST00000403799.8; same transcript is cross-referenced by current P35557-1. Paper also identifies P35557 isoform1 in its sequence analysis.
- Side-chain chemistry is standard biochemical interpretation of the exact mapped substitutions, not a claim that the paper measured side-chain charge.

Primary references:

- [A comprehensive map of human glucokinase variant activity](https://pmc.ncbi.nlm.nih.gov/articles/PMC10131484/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

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


---

# case-008 — triosephosphate_isomerase: mutation kinetic reasoning

**Assistant selection tier: held.** Generation status: `not_dispatched_source_hold`.

Hold/status note: Overlap with reserved evaluation/development sources; not submitted to Astra.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

No valid structured solution is recorded. This candidate remains in the catalog.

Returned model text, if any, is preserved below without editing.

```text

```

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **triosephosphate_isomerase** — [UniProt P00942](https://www.uniprot.org/uniprotkb/P00942/entry).

Source-supported reference answer: **A**. No valid selected answer was available.

Scientific review: Source exclusion; not submitted to Astra.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- This reference overlaps a reserved source group. The candidate is retained for visibility and excluded from generation and the shortlist.

Source support:

- Table 1, GAP columns, WT/Y208A/Y208F rows and footnotes a-d.
- Published GAP-isomerization values at pH 7.5 and 25 C (Km based on total GAP): WT kcat = 8900 s^-1, Km = 1.0 mM; Y208A kcat = 740 s^-1, Km = 2.9 mM; Y208F kcat = 13 s^-1, Km = 2.4 mM. Tyrosine-to-phenylalanine removes the phenolic hydroxyl while retaining an aromatic ring; tyrosine-to-alanine also removes that ring.
- Table 1 and footnotes a-d.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. E165, Y208 and S211 match the paper labels.
- The canonical reference includes initiator methionine. The verified mature structural polymer omits it but retains canonical author numbering. No additional tags or scars are inferred.

Primary references:

- [Role of Loop-Clamping Side Chains in Catalysis by Triosephosphate Isomerase](https://pmc.ncbi.nlm.nih.gov/articles/PMC4694050/). Table 1 and footnotes a-d.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-016 — triosephosphate_isomerase: mutation kinetic reasoning

**Assistant selection tier: held.** Generation status: `not_dispatched_source_hold`.

Hold/status note: Overlap with reserved evaluation/development sources; not submitted to Astra.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

No valid structured solution is recorded. This candidate remains in the catalog.

Returned model text, if any, is preserved below without editing.

```text

```

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **triosephosphate_isomerase** — [UniProt P00942](https://www.uniprot.org/uniprotkb/P00942/entry).

Source-supported reference answer: **C**. No valid selected answer was available.

Scientific review: Source exclusion; not submitted to Astra.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- This reference overlaps a reserved source group. The candidate is retained for visibility and excluded from generation and the shortlist.

Source support:

- Table 1, GAP kcat and Km columns, S211A/S211G rows.
- Published GAP-isomerization central values at pH 7.5 and 25 C, using total GAP: S211A kcat = 2800 s^-1, Km = 12 mM; S211G kcat = 7500 s^-1, Km = 1.8 mM. Both substitutions remove the serine side-chain hydroxyl; alanine retains a methyl side chain and glycine does not.
- Table 1 and footnotes a-d.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. E165, Y208 and S211 match the paper labels.
- The canonical reference includes initiator methionine. The verified mature structural polymer omits it but retains canonical author numbering. No additional tags or scars are inferred.

Primary references:

- [Role of Loop-Clamping Side Chains in Catalysis by Triosephosphate Isomerase](https://pmc.ncbi.nlm.nih.gov/articles/PMC4694050/). Table 1 and footnotes a-d.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-024 — triosephosphate_isomerase: mutation kinetic reasoning

**Assistant selection tier: held.** Generation status: `not_dispatched_source_hold`.

Hold/status note: Overlap with reserved evaluation/development sources; not submitted to Astra.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

No valid structured solution is recorded. This candidate remains in the catalog.

Returned model text, if any, is preserved below without editing.

```text

```

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **triosephosphate_isomerase** — [UniProt P00942](https://www.uniprot.org/uniprotkb/P00942/entry).

Source-supported reference answer: **B**. No valid selected answer was available.

Scientific review: Source exclusion; not submitted to Astra.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- This reference overlaps a reserved source group. The candidate is retained for visibility and excluded from generation and the shortlist.

Source support:

- Table 1, GAP kcat column, WT/Y208T/S211G/Y208T-S211G rows.
- Published GAP-isomerization kcat values at pH 7.5 and 25 C: WT 8900 s^-1; Y208T 3700 s^-1; S211G 7500 s^-1; the experimentally measured double variant Y208T/S211G 520 s^-1. For this question, an independent fractional-effects model predicts kcat(double) = kcat(Y208T) * kcat(S211G) / kcat(WT).
- Table 1 and footnotes a-d.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. E165, Y208 and S211 match the paper labels.
- The canonical reference includes initiator methionine. The verified mature structural polymer omits it but retains canonical author numbering. No additional tags or scars are inferred.

Primary references:

- [Role of Loop-Clamping Side Chains in Catalysis by Triosephosphate Isomerase](https://pmc.ncbi.nlm.nih.gov/articles/PMC4694050/). Table 1 and footnotes a-d.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.


---

# case-032 — triosephosphate_isomerase: mutation kinetic reasoning

**Assistant selection tier: held.** Generation status: `not_dispatched_source_hold`.

Hold/status note: Overlap with reserved evaluation/development sources; not submitted to Astra.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

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


## Astra’s worked solution

No valid structured solution is recorded. This candidate remains in the catalog.

Returned model text, if any, is preserved below without editing.

```text

```

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **triosephosphate_isomerase** — [UniProt P00942](https://www.uniprot.org/uniprotkb/P00942/entry).

Source-supported reference answer: **D**. No valid selected answer was available.

Scientific review: Source exclusion; not submitted to Astra.

Reference-sequence scope: Canonical wild-type coordinate reference; this does not reconstruct the complete tagged, fused or truncated assay construct. See the prompt and source qualifications for any explicit canonical-to-assay mapping.

- This reference overlaps a reserved source group. The candidate is retained for visibility and excluded from generation and the shortlist.

Source support:

- Table 1, WT yeast and Y208F rows; Figure 2 and associated inhibitor-complex interpretation.
- Published pH-dependent inhibitor-binding analysis estimates pKa = 10.4 for E165 in the WT TIM complex with the intermediate analogue phosphoglycolate trianion (PGA), and pKa = 6.3 for the corresponding Y208F complex. These pKa values refer specifically to the inhibitor-bound enzyme. For the simple protonation equilibrium in this question, protonated fraction = 1/(1+10^(pH-pKa)).
- Table 1 (yeast WT and Y208F rows), Figure 2, and discussion of inhibitor-bound E165 protonation.

Source qualifications:

- Canonical full-length sequence; initial methionine is residue 1. E165, Y208 and S211 match the paper labels.
- The canonical reference includes initiator methionine. The verified mature structural polymer omits it but retains canonical author numbering. No additional tags or scars are inferred.

Primary references:

- [Enzyme Architecture: Amino Acid Side-Chains That Function To Optimize the Basicity of the Active Site Glutamate of Triosephosphate Isomerase](https://pmc.ncbi.nlm.nih.gov/articles/PMC6037162/). Table 1 (yeast WT and Y208F rows), Figure 2, and discussion of inhibitor-bound E165 protonation.

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.
