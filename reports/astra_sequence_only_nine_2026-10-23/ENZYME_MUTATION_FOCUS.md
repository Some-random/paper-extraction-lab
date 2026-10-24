# Enzyme mutations: the next question pool

The next pool will focus on how experimentally tested mutations change enzyme function, and what the evidence says about the mechanism. The aim is to teach a model to connect a sequence change with enzyme chemistry, interpret measurements, and distinguish competing explanations.

**Current status:** primary papers and question formats have been selected. New mutation-focused Astra answers have not been generated. The [nine completed sequence-only examples](README.md) remain available as a separate pilot.

## Priority sources

| Paper | What makes it useful | Questions to develop |
|---|---|---|
| [Lam et al., APEX2, Nature Methods (2015)](https://doi.org/10.1038/nmeth.3179) | A Ting-authored study comparing an evolved peroxidase with its parent in cellular and purified-enzyme assays. | How does the variant's measured activity depend on assay conditions? What can expression-controlled labeling establish about function? |
| [Branon et al., TurboID and miniTurbo, Nature Biotechnology (2018)](https://doi.org/10.1038/nbt.4201) | A Ting-authored study comparing evolved biotin ligase variants, cellular labeling and background. | What activity/background trade-off do the measurements support? Which conclusions require expression normalization or additional kinetic data? |
| [Han et al., split APEX2, ACS Chemical Biology (2019)](https://doi.org/10.1021/acschembio.8b00919) | A Ting-authored study comparing enzyme-fragment variants and interaction-dependent activity. | Does a stronger signal reflect useful interaction dependence or increased background? What do the controls discriminate? |
| [Markin et al., PafA/HT-MEK, Science (2021)](https://doi.org/10.1126/science.abf8761) | A complementary study of 1,036 enzyme mutants with multiple kinetic and physical measurements. It separates effects on catalysis from formation of an inactive misfolded state. | How can mutations outside an active site affect function? Which measurements distinguish catalytic changes from changes in the active enzyme fraction? |

The first three papers directly involve Ting. PafA is a complementary source from other researchers. Multiple substitutions or fragment changes will be recorded as such; a comparison between two multi-change constructs cannot isolate the effect of every individual substitution.

Evidence panels selected for extraction are APEX2 Figure 2a–b and 2e; TurboID Figure 2a–b and Figure 1f–g; and split APEX2 Figure 3b–d. Exact panel context, controls and corrected versions will accompany each extracted result. PafA's per-variant measurements must be bound to their assay definitions before use.

## Three useful question formats

1. **Mutation and function.** Give the reference sequence, the published variant and relevant biological context. Ask which broad functional interpretation is most defensible. Preserve uncertainty when sequence and background knowledge do not resolve the effect.
2. **Activity and mechanism.** Give a small, sourced evidence table alongside the variant. Ask whether the observations support an effect on catalysis, binding, abundance or the fraction of active enzyme. Abundance is not a direct measurement of thermodynamic stability.
3. **Controls and combinations.** Give the parent/variant comparisons and assay conditions needed to assess background, condition dependence or combined effects. Ask what the measurements establish and what remains unresolved. Claims about epistasis require the relevant single and combined variants and an explicit comparison scale.

The intended answer is a worked biological explanation followed by one selected letter. More detail is useful when it connects evidence to the alternatives; answer length is not the quality target.

## How papers enter the data

For each example, the paper establishes the tested construct, experimental observations and reference answer. The reference sequence, mutation numbering and assay construct must agree. A naturally occurring UniProt sequence will not automatically be treated as the experimental construct.

The solver receives exactly what the student will receive. For evidence-based questions, that includes the small assay table or structural context needed to reason about the mutation. Full papers and discussion conclusions remain separate verification sources. A sequence-only question cannot silently depend on an omitted experimental result.

These formats add enzyme-mutation skills to the data. They differ from the sequence-only format of the current pilot, so improvement on mutation questions and improvement on LiveProteinBench must be assessed separately.

## Source qualifications

- Use the current [TurboID correction](https://doi.org/10.1038/s41587-019-0355-0) when extracting Supplementary Tables 2–7.
- The APEX2 article records corrections to Figure 2a symbols and Figure 2e axis-label display. Extract the corrected panels.
- The [split APEX2 correction](https://doi.org/10.1021/acschembio.9b00798) replaces images in Figures 1e and 2b. Figure 3 is the preferred starting point for the comparison questions above.
- Source selection and question design are assistant work. They are not expert validation, completed training-data generation or measured evidence of a training gain.
