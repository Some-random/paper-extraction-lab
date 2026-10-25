# AI-created protein reasoning questions — ten revised examples

Ten open-response questions with concise reference answers and assessment rubrics. The first three concern APEX/APEX2 and TurboID work from Alice Ting's laboratory. Questions 4–8 retain foundational sequence interpretation; questions 9–10 address probe perturbation and interpretation of filtered evidence.

**[Read all ten questions and answers](ALL_EXAMPLES.md)** · [Questions only](QUESTIONS_ONLY.md) · [Plain-text Q&A](ALL_EXAMPLES.txt) · [Selection and assessment rubric](RUBRIC.md)

| Example | Topic |
|---|---|
| 1 | [APEX: what transfers across assay conditions?](examples/example-01.md) |
| 2 | [APEX: can staining measure delivery of a reporter fusion?](examples/example-02.md) |
| 3 | [Choosing a labeling tool for the measurement objective](examples/example-03.md) |
| 4 | [Inferring a cofactor from a motif combination](examples/example-04.md) |
| 5 | [Recognizing repeated calcium-binding loops](examples/example-05.md) |
| 6 | [Separating membrane anchoring from topology](examples/example-06.md) |
| 7 | [Distinguishing interaction domains from ligand motifs](examples/example-07.md) |
| 8 | [Judging a chromophore-binding hypothesis](examples/example-08.md) |
| 9 | [Does a label reveal or change protein organization?](examples/example-09.md) |
| 10 | [What does exclusion from a proximity-labeling list mean?](examples/example-10.md) |

The original five criteria remain: source-supported answers, fair input, reusable biological lessons, substantive clear reasoning, and variety. Revision 6 incorporates lab feedback by removing answer-choice shortcuts, unused sequence material and irrelevant numerical detail. Reference answers are illustrative; justified alternatives receive credit under each item's rubric. More explanation does not earn credit by itself.

All ten are source-aware AI revisions. The supplied observations and retained sequences come from the earlier source-reviewed collection; hypothetical decisions and comparisons are identified in the notes. Assistant review is not expert human validation. Question difficulty and training benefit have not been measured. This collection remains separate from the completed 10,000-example training run.

<details>
<summary>Sources, versions and machine-readable files</summary>

[Current revision](revision_v6.json) · [Review scope and checks](review_v6.json) · [Per-example provenance](selection_provenance.json) · [Earlier substantive revision](revision_v4.json).

[Exact student prompts](questions.jsonl) · [Training messages](training_examples.jsonl) · [Reference answers and rubrics](verification.jsonl) · [Selection spreadsheet](selection.csv).

Revision 6 changes the machine-readable format to open responses. Letter-choice fields are removed; reference answers and assessment rubrics replace single-letter answer matches. `training_examples.jsonl` contains only the student question and the reference answer in its user/assistant messages. Source notes and grading rubrics remain outside those messages. These examples are not an automatically validated large training dataset.

The ten per-example Markdown files are canonical. Run `python3 build_exports.py` to regenerate exports, and `python3 build_exports.py --check` to validate them. Earlier prompts, outputs and source-aware revisions remain in the existing artifacts and Git history; their creation and billing records are unchanged. No new teacher API calls were made for revision 6.

UniProt-derived sequences retain [UniProt Consortium](https://www.uniprot.org/) attribution and [CC BY 4.0](https://www.uniprot.org/help/license) terms. Experimental observations are attributed to the linked primary papers. Full papers and PDFs are not redistributed.

</details>
