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
