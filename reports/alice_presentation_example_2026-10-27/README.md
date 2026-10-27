# Validating LOV-Turbo for pulse-chase proteomics

A hypothetical linker-engineered LOV-Turbo variant is being evaluated for ER-to-nucleus pulse-chase proteomics. A brief blue-light/biotin pulse should label proteins near the cytosolic face of the ER; a dark chase should then follow that labeled cohort. Biotin tags remain covalently attached after enzyme activity stops.

The following are **hypothetical follow-up observations**, not published measurements:

- Purified protein rapidly recovers its dark-state LOV absorbance spectrum after illumination.
- In cells, labeling is strong with light plus biotin and negligible in never-illuminated controls. Expression and ER localization remain stable during the chase.
- Total cellular streptavidin signal plateaus after the pulse. Nevertheless, nuclear proteomics detects additional biotinylated proteins after the chase; fractionation controls show no increase in ER contamination.

A colleague takes these results as sufficient evidence that the additional nuclear proteins were labeled during the intended pulse. In this cellular assay, biotin-omitted labeling is negligible, and supplied biotin becomes available rapidly enough to resolve the intended pulse boundary.

**Which added comparison most directly tests the colleague’s interpretation?**

A. Match pulse-end biotinylation between the variant and parental LOV-Turbo, then compare their nuclear proteomes after the same dark chase.

B. Illuminate before adding biotin, then supply biotin at successive times in darkness; compare labeling with never-illuminated and freshly illuminated controls.

C. Measure dark-state spectral recovery across intracellular-like solution conditions, alongside purified-protein stability and light-dependent labeling of an added protein substrate.

D. Repeat chase proteomics with a cytosolic labeling reference, comparing nuclear enrichment over that reference before and after the chase.

## Worked answer

B is the most direct test because it separates the activating light from the opportunity to add detectable biotin labels.

With biotin supplied only after illumination ends, labeling above the never-illuminated baseline would reveal activity that survives the light pulse. Successive delays test how long that activity persists. Freshly illuminated controls at matched delays establish that biotin is available and the enzyme remains competent. The stated low biotin-omitted background makes this comparison informative.

The existing readouts do not answer that timing question. LOV absorbance reports the photosensor’s state, not the catalytic activity of the cellular fusion. A whole-cell streptavidin plateau can conceal new labeling of a small protein subset subsequently detected by nuclear enrichment. Nuclear proteomics establishes where labeled proteins are recovered, but does not timestamp label addition. Stable enzyme localization and clean fractionation strengthen the spatial interpretation without resolving this temporal uncertainty.

A controls total labeling yield; equally labeled samples can still have different labeling histories. C tests purified-protein photochemistry, stability and illuminated activity, but does not directly measure cellular activity after light removal. D tests spatial enrichment against a useful reference, but likewise leaves the labeling window unresolved.

Post-illumination labeling would show that optical recovery is insufficient to guarantee catalytic shutoff. Little or no labeling would support shutoff in this delayed-biotin comparison, within assay sensitivity. Because the biotin history differs, that result alone would not validate the actual biotin-containing pulse or establish every protein’s trafficking route.

<details>
<summary>Sources and scope</summary>

[Branon et al., 2018](https://doi.org/10.1038/nbt.4201), Figure 1a; [Lee et al., 2023](https://doi.org/10.1038/s41592-023-01880-5), Figure 3a, the Results description of Supplementary Figure 3b (the light-before-biotin test), and Figures 4–5 for pulse-chase applications. The candidate variant and all follow-up observations are hypothetical.

</details>
