# AI-created protein reasoning training data — ten examples

Ten AI-created question-and-answer examples intended for protein-model training. They connect protein sequences and published experimental observations to reusable ideas about catalysis, binding, membranes and protein interactions. The enzyme-mutation examples appear first.

Each example shows the question, the information needed to answer it, the choices and the worked answer. Sources, evidence checks and limitations expand below each answer.

**[Read all ten questions and answers](ALL_EXAMPLES.md)** · [Plain-text Q&A](ALL_EXAMPLES.txt) · [Questions only](QUESTIONS_ONLY.md) · [Selection spreadsheet](selection.csv)

| Example | Question topic |
|---|---|
| 1 | [APEX: enzyme behavior depends on substrate conditions](examples/example-01.md) |
| 2 | [Adenylate kinase: a conservative substitution can impair catalysis](examples/example-02.md) |
| 3 | [PafA: inactive protein fraction versus inhibitor binding](examples/example-03.md) |
| 4 | [Distinguishing heme from other cofactors](examples/example-04.md) |
| 5 | [Calcium binding through repeated structural motifs](examples/example-05.md) |
| 6 | [Membrane anchoring](examples/example-06.md) |
| 7 | [Protein-interaction domains](examples/example-07.md) |
| 8 | [Chromophore binding](examples/example-08.md) |
| 9 | [Testing whether a protein label changes its target](examples/example-09.md) |
| 10 | [What does a proximity-labeling ratio measure?](examples/example-10.md) |

<details>
<summary>Selection criteria and evidence checks</summary>

The examples were selected for a supported answer, fair input, a reusable biological lesson, clear substantive reasoning and variety. Examples 1–8 retain their original questions and answers. Examples 9–10 were revised after source review to require biological interpretation and comparison of plausible explanations; they address binding valency and the interpretation of localization controls. These two current explanations are source-aware AI edits, not unchanged teacher outputs or newly generated blinded responses.

All ten selected answers agree with their recorded source evidence. Explanatory steps can include qualified biological inferences and mathematical deductions; the cited papers do not prove every sentence. Reviews are assistant checks, not expert human ground truth. Training gains have not been measured.

Some questions use sequence and choices alone; others supply the published observations needed for experimental reasoning. For the original generations, full papers and private reference labels were withheld during solving and used for later checking. The revised questions and explanations for examples 9–10 were edited with source evidence available, and are identified accordingly. Their original earlier questions, exact requests and unchanged generated answers remain accessible beside the revisions. Source qualifications are retained with each example. These examples are not a reproduction of the LiveProteinBench evaluation set.

The original two generations cost **$0.70678**. Reusing the eight previous answers and editing examples 9–10 required no additional teacher API calls. The [revision record](revision_v2.json) distinguishes the current edited examples from the preserved original generations. [Training question-and-answer messages](training_examples.jsonl) · [Exact student prompts](questions.jsonl) · [Source provenance](selection_provenance.json) · [Verification labels](verification.jsonl) · [New-generation usage](new_generation_usage.json).

UniProt-derived sequence references retain the [UniProt Consortium](https://www.uniprot.org/) attribution and [CC BY 4.0](https://www.uniprot.org/help/license) terms. Experimental observations are attributed separately to their primary papers. Full paper texts and PDFs are not redistributed. The original AI outputs are preserved.

</details>
