# AI-created protein reasoning training data — ten examples

Ten AI-created question-and-answer examples intended for protein-model training. The first three use enzyme engineering from Alice Ting's laboratory: APEX/APEX2 and TurboID. The remaining questions preserve variety in cofactors, calcium binding, membranes, interaction domains and labeling controls.

Each example shows the complete question, supplied sequence or experimental observations, choices and worked answer. Sources and limitations expand below each answer.

**[Read all ten questions and answers](ALL_EXAMPLES.md)** · [Plain-text Q&A](ALL_EXAMPLES.txt) · [Questions only](QUESTIONS_ONLY.md) · [Selection spreadsheet](selection.csv)

| Example | Question topic |
|---|---|
| 1 | [APEX: enzyme behavior depends on substrate conditions](examples/example-01.md) |
| 2 | [APEX: why an active enzyme can still be a poor cellular reporter](examples/example-02.md) |
| 3 | [TurboID and miniTurbo: when more labeling weakens the time window](examples/example-03.md) |
| 4 | [Distinguishing heme from other cofactors](examples/example-04.md) |
| 5 | [Calcium binding through repeated structural motifs](examples/example-05.md) |
| 6 | [Membrane anchoring](examples/example-06.md) |
| 7 | [Protein-interaction domains](examples/example-07.md) |
| 8 | [Chromophore binding](examples/example-08.md) |
| 9 | [Testing whether a protein label changes its target](examples/example-09.md) |
| 10 | [What does a proximity-labeling ratio measure?](examples/example-10.md) |

<details>
<summary>Selection criteria and evidence checks</summary>

The examples were selected for a supported answer, fair input, a reusable biological lesson, clear reasoning and variety. All ten are AI-created. The collection includes generated explanations and explanations revised with source evidence. Creation and revision records are preserved in the [source provenance](selection_provenance.json) and [revision record](revision_v4.json).

All ten selected answers agree with their recorded source evidence. Explanations include qualified biological inferences and calculations; cited papers do not prove every sentence. Reviews are assistant checks, not expert human ground truth. Training gains have not been measured, and this package does not release model training. Some questions use sequence and choices alone; others supply the observations needed for experimental reasoning. These examples are not a reproduction of the LiveProteinBench evaluation set.

[Training messages](training_examples.jsonl) · [Exact student prompts](questions.jsonl) · [Source provenance](selection_provenance.json) · [Verification labels](verification.jsonl) · [Generation records](revision_v4_usage.json).

UniProt-derived sequence references retain [UniProt Consortium](https://www.uniprot.org/) attribution and [CC BY 4.0](https://www.uniprot.org/help/license) terms. Experimental observations are attributed to their primary papers. Full paper texts and PDFs are not redistributed.

</details>
