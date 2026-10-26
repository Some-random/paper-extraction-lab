# Provenance and review scope

These are curated teaching examples prepared with AI assistance using published papers and protein records. All ten current worked answers are source-aware assistant revisions. Published observations are distinguished from hypothetical scenarios in each example's source notes. Human feedback informed earlier revisions; documented expert human validation of this final version is not claimed.

The final editorial pass corrected overstatements, removed personal deference and duplicate explanation, and consolidated preparation history here. It preserved all ten student questions, their A–D options, answer keys and the full sequences in questions 4–8. The answers retain the biological reasoning, alternative-choice analysis and relevant limits of inference.

Review checked consistency with the existing source evidence, sequence strings and residue coordinates, agreement between the questions and answers, and synchronization of readable and machine-readable versions. It did not repeat a full-text review of every paper. Earlier abstract-only and deposition-based checks are not represented as full-text validation. No new teacher API calls, experimental measurements or training runs were made for this revision.

The collection contains both foundational sequence interpretation and research judgment. Item difficulty, expert agreement and training benefit have not been measured. The earlier [criteria and feedback audit](alignment_audit_v1.json) records remaining question-design limitations, including answer-selection shortcuts; the final answer edit does not establish that those limitations have been eliminated.

## Review records

[Final answer revision and checks](final_answer_revision_v1.json) · [Current source and answer review](review_v6.json) · [Per-example provenance](selection_provenance.json) · [Question format](mcq_restoration_v1.json).

Earlier prompts, outputs and review records remain preserved in the existing artifacts and Git history. Historical independent-solver assertions for examples 9–10 lack recovered standalone execution artifacts. The [example 9 status record](artifacts/example-09/independent_check.json) and [example 10 status record](artifacts/example-10/independent_check.json) document that limitation; those assertions are not validation of the current questions or answers.

## Downloads

[Exact student prompts](questions.jsonl) · [Training messages](training_examples.jsonl) · [Answer review records](verification.jsonl) · [Selection spreadsheet](selection.csv) · [Plain-text questions and answers](ALL_EXAMPLES.txt).

The canonical pages in `examples/` generate the readable collection and exports through `build_exports.py`. Internal preparation criteria are separate from the review copy. This collection is separate from the completed 10,000-example training run.

## Attribution

UniProt-derived sequences retain [UniProt Consortium](https://www.uniprot.org/) attribution and [CC BY 4.0](https://www.uniprot.org/help/license) terms. Experimental observations are attributed to the linked primary papers. Full papers and PDFs are not redistributed.
