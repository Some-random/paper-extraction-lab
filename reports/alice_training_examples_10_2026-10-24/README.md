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

The examples were selected for a supported answer, fair input, a reusable biological lesson, clear substantive reasoning and variety. Examples 2–3 replace the previous adenylate-kinase and PafA questions with enzyme-mutation questions from Ting-laboratory papers. Example 2 is an unchanged new AI-generated response: the solver saw only the printed question, while full papers and private labels were withheld. Example 3 is a source-aware AI-authored explanation written after its sole fresh generation attempt returned HTTP 502 without an answer; it is not a successful teacher response or blinded solve. No retry was made. Assistant source review checked both current answers.

The source caption for example 1 now identifies its wild-type reference backbone correctly; its question and generated answer are unchanged. Example 6's answer has a labeled coordinate correction checked against its frozen sequence annotation; its question and answer letter are unchanged. Examples 4–5 and 7–10 retain their previous question-and-answer pages. Examples 9–10 remain the explicitly source-aware edited revisions from revision 2. Original responses, earlier presentations and the [revision record](revision_v4.json) are retained.

All ten selected answers agree with their recorded source evidence. Explanations include qualified biological inferences and calculations; cited papers do not prove every sentence. Reviews are assistant checks, not expert human ground truth. Training gains have not been measured, and this package does not release model training. Some questions use sequence and choices alone; others supply the observations needed for experimental reasoning. These examples are not a reproduction of the LiveProteinBench evaluation set.

Two generation requests were attempted; one completed. The known new cost is **$0.86597**, with **$7.00 still reserved because the failed request's billing is uncertain**. The [usage record](revision_v4_usage.json) is separate from the unchanged earlier two-generation record ($0.70678). [Training messages](training_examples.jsonl) · [Exact student prompts](questions.jsonl) · [Source provenance](selection_provenance.json) · [Verification labels](verification.jsonl).

UniProt-derived sequence references retain [UniProt Consortium](https://www.uniprot.org/) attribution and [CC BY 4.0](https://www.uniprot.org/help/license) terms. Experimental observations are attributed to their primary papers. Full paper texts and PDFs are not redistributed.

</details>
