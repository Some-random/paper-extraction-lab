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

[Exact generation request](../artifacts/example-02/request.json) · [Unchanged generated output](../artifacts/example-02/generated_output.json) · [Question, answer and source verification](../artifacts/example-02/source_verification.json) · [Revision record](../revision_v4.json)

Assistant reviews are not expert human validation, and training gains have not been measured.

</details>
