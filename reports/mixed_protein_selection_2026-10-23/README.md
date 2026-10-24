Archived twelve-example presentation. [Current ten-example collection](../alice_training_examples_10_2026-10-24/README.md).

# AI-created protein reasoning training data

This collection contains **12 AI-created question-and-answer examples intended for protein-model training**. They combine protein function, binding, membrane architecture, sequence features and enzyme-mutation reasoning in one collection, with the enzyme examples first for convenient review.

Each example shows the full protein sequence, the question, answer choices and a worked answer. Sources, evidence checks and limitations are available in an expandable section below each answer.

**[Read all questions and answers](ALL_EXAMPLES.md)** · [Plain-text Q&A](ALL_EXAMPLES.txt) · [Questions only](QUESTIONS_ONLY.md) · [Selection spreadsheet](selection.csv)

| Example | Question topic |
|---|---|
| 1 | [APEX: enzyme behavior depends on substrate conditions](examples/example-01.md) |
| 2 | [Adenylate kinase: a conservative substitution can impair catalysis](examples/example-02.md) |
| 3 | [PafA: inactive protein fraction versus inhibitor binding](examples/example-03.md) |
| 4 | [Covalent modification of a particular lysine](examples/example-04.md) |
| 5 | [Locating repeated sequence motifs](examples/example-05.md) |
| 6 | [Recognizing multiple membrane-spanning segments](examples/example-06.md) |
| 7 | [Distinguishing heme from other cofactors](examples/example-07.md) |
| 8 | [Calcium binding through repeated structural motifs](examples/example-08.md) |
| 9 | [Membrane anchoring](examples/example-09.md) |
| 10 | [Protein-interaction domains](examples/example-10.md) |
| 11 | [Chromophore binding](examples/example-11.md) |
| 12 | [Post-translational modification chemistry](examples/example-12.md) |

<details>
<summary>How the examples were created and checked</summary>

AI generated the worked answers. Cited biological papers and experimental records were used to check the selected answers and key facts. All 12 selected answers agree with the recorded source evidence. Some explanations remain qualified sequence-based interpretations or calculations from supplied assumptions; the papers do not prove every explanatory sentence. Reviews were performed by assistants rather than expert human reviewers.

Where an experimentally measured mutation effect is needed, the question supplies the published variants and relevant observations. Other questions provide the sequence and choices. Full papers and private answer labels were withheld during solving; their role was to check the results afterward. The exact information supplied is preserved in the [student prompts](questions.jsonl).

Source checks include full-text Results, abstracts, indexed passages and experimental structure depositions, as specified for each example. We do not claim that every full paper was independently reread or every reasoning step experimentally established. These examples are intended for training; training benefit has not yet been measured.

This presentation reuses completed answers and incurs no additional model-generation cost. Original scientific inputs and generated outputs remain preserved in the source reports. [Source provenance and evidence-check notes](selection_provenance.json).

</details>
