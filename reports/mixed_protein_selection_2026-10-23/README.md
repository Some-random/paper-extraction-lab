# Mixed protein reasoning — 12 examples for selection

The goal is a broad protein-reasoning dataset with enzyme mutations as one component. This selection contains **nine broad protein questions and three enzyme-mutation questions** (75% / 25%). That is a starting mix for this small pilot, not a fixed training-data ratio.

The broad questions cover sequence motifs, membrane architecture, cofactors, binding, protein-interaction domains and modification chemistry. The three mutation examples add condition-dependent activity, side-chain chemistry and interpretation of active-protein fraction.

[Read all 12 complete examples](ALL_EXAMPLES.md) · [Plain text](ALL_EXAMPLES.txt) · [Questions only](QUESTIONS_ONLY.md) · [Questions as plain text](QUESTIONS_ONLY.txt) · [Selection spreadsheet](selection.csv)

## Broad protein reasoning — nine examples

| Example | Topic | Information supplied |
|---|---|---|
| general-001 | [Covalent modification of a particular lysine](../astra_sequence_only_nine_2026-10-23/examples/case-001.md) | Sequence-only |
| general-002 | [Locating repeated sequence motifs](../astra_sequence_only_nine_2026-10-23/examples/case-002.md) | Sequence-only |
| general-003 | [Recognizing multiple membrane-spanning segments](../astra_sequence_only_nine_2026-10-23/examples/case-003.md) | Sequence-only |
| general-004 | [Distinguishing heme from other cofactors](../astra_sequence_only_nine_2026-10-23/examples/case-004.md) | Sequence-only |
| general-005 | [Calcium binding through repeated structural motifs](../astra_sequence_only_nine_2026-10-23/examples/case-005.md) | Sequence-only |
| general-006 | [Membrane anchoring](../astra_sequence_only_nine_2026-10-23/examples/case-006.md) | Sequence-only |
| general-007 | [Protein-interaction domains](../astra_sequence_only_nine_2026-10-23/examples/case-007.md) | Sequence-only |
| general-008 | [Chromophore binding](../astra_sequence_only_nine_2026-10-23/examples/case-008.md) | Sequence-only |
| general-009 | [Post-translational modification chemistry](../astra_sequence_only_nine_2026-10-23/examples/case-009.md) | Sequence-only |

## Enzyme mutations — three examples

| Example | Topic | Information supplied |
|---|---|---|
| mutation-001 | [APEX: enzyme behavior depends on substrate conditions](../astra_enzyme_mutation_pool_2026-10-23/examples/case-001.md) | Sequence + published variants and assay evidence |
| mutation-004 | [Adenylate kinase: a conservative substitution can impair catalysis](../astra_enzyme_mutation_pool_2026-10-23/examples/case-004.md) | Sequence + published variants and assay evidence |
| mutation-015 | [PafA: inactive protein fraction versus inhibitor binding](../astra_enzyme_mutation_pool_2026-10-23/examples/case-015.md) | Sequence + published variants and assay evidence |

## What is already complete

All 12 worked answers were completed previously with GPT-6 Astra at maximum reasoning effort, pro mode. This page reorganizes existing material; it does not represent 12 new API generations. The full reference sequence, question, four choices, worked answer and paper links are available for every example. Original prompts and generated outputs remain unchanged in their source reports.

For the nine broad questions, papers and verification identities were withheld during solving. For the three mutation questions, the prompt explicitly supplies the published variants and essential assay evidence. Full papers and private gold labels were withheld in both groups. These two input formats should be evaluated separately before choosing a training mixture.

All 12 selected answers match their source-supported labels. Explanation reviews are assistant assessments, not expert human validation; source-specific qualifications remain with each example. No training gain or aggregate benchmark accuracy is claimed.

The larger [enzyme-mutation candidate bank](../astra_enzyme_mutation_pool_2026-10-23/README.md) remains available for selecting alternatives. It is one optional component of the broader dataset.

[Exact student prompts](questions.jsonl) · [Compilation provenance](selection_provenance.json)
