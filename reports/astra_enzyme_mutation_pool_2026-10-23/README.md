# Enzyme and mutation reasoning — candidate selection catalog

This pool is for selecting useful training examples. Each candidate contains a complete reference protein sequence, a question and four choices. Many questions also provide **published variants and essential assay observations**. Astra was asked to reason from that exact input and its existing biological knowledge. Full papers and private answer labels were not supplied to the solver.

These are evidence-supported enzyme and mutation questions; supplied measurements must not be presented as predictions from sequence alone. Reference backbones must not be confused with complete tagged experimental constructs. Source scope and coordinate qualifications remain visible with each candidate.

## Read and select

[All examples, grouped by assistant tier](ALL_EXAMPLES.md) · [Plain-text version](ALL_EXAMPLES.txt) · [Questions without answers](QUESTIONS_ONLY.md) · [Questions as plain text](QUESTIONS_ONLY.txt) · [Selection spreadsheet](selection.csv)

### Suggested shortlist

- [case-001: APEX peroxidase — Peroxide tolerance changes with substrate conditions](examples/case-001.md)
- [case-002: PTEN phosphatase — Normal protein abundance does not ensure catalytic function](examples/case-002.md)
- [case-004: Adenylate kinase — A conservative charge substitution can disrupt catalysis](examples/case-004.md)
- [case-009: APEX peroxidase — Activity, stability and heme binding give different rankings](examples/case-009.md)
- [case-010: PTEN phosphatase — One mutation separates lipid and protein substrate activity](examples/case-010.md)
- [case-012: Adenylate kinase — Variant rankings depend on substrate concentration](examples/case-012.md)
- [case-015: PafA alkaline phosphatase — Inactive enzyme fraction versus inhibitor affinity](examples/case-015.md)
- [case-019: PafA alkaline phosphatase — Stronger product binding does not imply faster catalysis](examples/case-019.md)
- [case-021: Biotin ligase — A matched mutation improves activity without raising background](examples/case-021.md)
- [case-026: PTEN phosphatase — A downstream phenotype can mask partial functional loss](examples/case-026.md)
- [case-030: Glucokinase / hexokinase-4 — Different substitutions affect binding and conformational change](examples/case-030.md)
- [case-031: PafA alkaline phosphatase — Transition-state-analog binding is not catalytic power](examples/case-031.md)

These are assistant suggestions for inspection, not validated training examples. Starred entries in the catalog are on this shortlist.

### Complete catalog

| Candidate | Enzyme / variants | Topic | Assistant tier | Generation | Source-answer match |
|---|---|---|---|---|---|
| case-001 ★ | APEX peroxidase / APEX; APEX2 | [Peroxide tolerance changes with substrate conditions](examples/case-001.md) | strong | completed | Yes |
| case-002 ★ | PTEN phosphatase / C124S | [Normal protein abundance does not ensure catalytic function](examples/case-002.md) | strong | completed | Yes |
| case-004 ★ | Adenylate kinase / R156K | [A conservative charge substitution can disrupt catalysis](examples/case-004.md) | strong | completed | Yes |
| case-009 ★ | APEX peroxidase / APEX; APEX2; Dimeric APX-W41F comparator | [Activity, stability and heme binding give different rankings](examples/case-009.md) | strong | completed | Yes |
| case-010 ★ | PTEN phosphatase / G129E | [One mutation separates lipid and protein substrate activity](examples/case-010.md) | strong | completed | Yes |
| case-012 ★ | Adenylate kinase / R88A; R156K | [Variant rankings depend on substrate concentration](examples/case-012.md) | strong | completed | Yes |
| case-015 ★ | PafA alkaline phosphatase / H83G | [Inactive enzyme fraction versus inhibitor affinity](examples/case-015.md) | strong | completed | Yes |
| case-019 ★ | PafA alkaline phosphatase / T79S | [Stronger product binding does not imply faster catalysis](examples/case-019.md) | strong | completed | Yes |
| case-021 ★ | Biotin ligase / G3Δ, published intermediate; miniTurbo | [A matched mutation improves activity without raising background](examples/case-021.md) | strong | completed | Yes |
| case-026 ★ | PTEN phosphatase / D92N | [A downstream phenotype can mask partial functional loss](examples/case-026.md) | strong | completed | Yes |
| case-030 ★ | Glucokinase / hexokinase-4 / A456V; W99R | [Different substitutions affect binding and conformational change](examples/case-030.md) | strong | completed | Yes |
| case-031 ★ | PafA alkaline phosphatase / K162A | [Transition-state-analog binding is not catalytic power](examples/case-031.md) | strong | completed | Yes |
| case-003 | PafA alkaline phosphatase / T79G | [Removing a catalytic hydroxyl: activity versus expression](examples/case-003.md) | strong | completed | Yes |
| case-006 | Glucokinase / hexokinase-4 / W99R | [Cellular growth improvement does not identify a kinetic mechanism](examples/case-006.md) | strong | completed | Yes |
| case-007 | PafA alkaline phosphatase / D473V; D473G | [A distant substitution changes relative substrate activity](examples/case-007.md) | strong | completed | Yes |
| case-011 | PafA alkaline phosphatase / Y103G | [Expression history changes the active protein population](examples/case-011.md) | strong | completed | Yes |
| case-017 | APEX peroxidase / APEX; APEX2; VPGAPEX | [Single versus combined substitutions: what is established?](examples/case-017.md) | strong | completed | Yes |
| case-018 | PTEN phosphatase / Y138L | [Reverse substrate selectivity in the same enzyme](examples/case-018.md) | strong | completed | Yes |
| case-020 | Adenylate kinase / R36A; R123A | [The location of an arginine substitution matters](examples/case-020.md) | strong | completed | Yes |
| case-025 | APEX peroxidase / APEX; APEX2 | [Improved labeling can retain spatial discrimination](examples/case-025.md) | strong | completed | Yes |
| case-027 | PafA alkaline phosphatase / D38G; D352G; H353V | [Metal ligands can have different substrate-specific roles](examples/case-027.md) | strong | completed | Yes |
| case-028 | Adenylate kinase / R167A | [Cofactor presence does not replace a catalytic residue](examples/case-028.md) | strong | completed | Yes |
| case-029 | Biotin ligase / G3, published intermediate; G3Δ, published intermediate | [Deletion effects and endogenous substrate controls](examples/case-029.md) | strong | completed | Yes |
| case-005 | Biotin ligase / BioID, paper construct definition; TurboID | [A shorter labeling window is not a kcat measurement](examples/case-005.md) | moderate | completed | Yes |
| case-013 | Biotin ligase / TurboID; miniTurbo | [Labeling strength versus temporal background](examples/case-013.md) | moderate | completed | Yes |
| case-014 | Glucokinase / hexokinase-4 / F150S; D217N; E279Q | [Compare cellular activity without assuming a mechanism](examples/case-014.md) | moderate | completed | Yes |
| case-022 | Glucokinase / hexokinase-4 / D217N; E279Q | [Acid-to-amide substitutions can preserve measured function](examples/case-022.md) | moderate | completed | Yes |
| case-023 | PafA alkaline phosphatase / A165V; H83G | [Nearby residues can alter binding in opposite directions](examples/case-023.md) | moderate | completed | Yes |
| case-008 | Triosephosphate isomerase / Y208F; Y208A | [Aromatic replacements can differ in catalytic effect](examples/case-008.md) | held | not_dispatched_source_hold | Not available |
| case-016 | Triosephosphate isomerase / S211A; S211G | [Similar group loss can produce different kinetics](examples/case-016.md) | held | not_dispatched_source_hold | Not available |
| case-024 | Triosephosphate isomerase / Y208T; S211G; Y208T/S211G | [Testing a specified model of kinetic epistasis](examples/case-024.md) | held | not_dispatched_source_hold | Not available |
| case-032 | Triosephosphate isomerase / Y208F | [A substitution changes protonation in a bound state](examples/case-032.md) | held | not_dispatched_source_hold | Not available |

Strong, moderate and held are **assistant review categories**, not expert ratings. Held, failed and undispatched candidates remain visible rather than being silently discarded. The original generated solutions are unchanged.

## Recorded result

- Frozen candidates: 32; attempted requests: 28; valid structured outputs: 28.
- Source-held candidates: 4. These were not submitted to Astra and are never counted as incorrect model answers.
- Source-label matches: 28. This is a selected development pool, not an estimate of benchmark accuracy.
- Assistant tiers: 23 strong, 5 moderate, 4 held.
- Teacher: GPT-6 Astra, maximum reasoning effort, pro mode. No automatic paid retries.
- Usage-based known cost: **$15.2453**. Billing-unknown cases: 0. Elapsed batch time: approximately 7.2 minutes. This includes dispatch and completion accounting; individual request times are recorded separately. Cost is calculated from usage, not an independently retrieved invoice.

Reference-answer support, exact sequence-coordinate checks, explanation quality and training usefulness are separate questions. A correct answer may accompany weak reasoning. Assay interpretation may be strong even when sequence alone cannot predict the result. No expert human validation or student training improvement is claimed.

## Inputs, outputs and sources

- [Exact student questions](questions.jsonl) and [shared solver instructions](system_prompt.txt).
- Per-candidate exact requests, unchanged generated text/JSON and available literal sequence checks under `artifacts/`. A prepared request file for an undispatched candidate does not mean an API call occurred.
- [Separate verification labels and identities](verification.jsonl), [source notes](source_notes.json), and [assistant reviews](review.json).
- [Raw usage and cost components](usage_and_cost.json), with transport and account identifiers removed. Full paper texts are not redistributed.

Reference protein sequences are attributed to the [UniProt Consortium](https://www.uniprot.org/), release 2026_03, under [CC BY 4.0](https://www.uniprot.org/help/license). Experimental observations and variant effects are attributed separately to the cited primary papers. Questions are project adaptations of published protein evidence; generated solutions are attributed to Astra. This does not apply a new license to cited papers.
