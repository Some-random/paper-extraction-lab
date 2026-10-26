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
