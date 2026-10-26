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
