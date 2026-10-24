# Nine sequence-only protein reasoning examples

This pilot tests whether a strong teacher can produce useful worked solutions when it receives the same kind of information as the student: the **complete protein sequence, task, question and four answer choices**. Astra received no papers, curated annotations, protein names, accession identifiers, gold answers or previous teacher solutions. No external tools were supplied.

The nine proteins cover 7 task types, including sequence motifs, membrane architecture, cofactors, protein interactions and modification chemistry. Their topics connect broadly to [Ting laboratory research interests](https://www.tinglab.org/research); the cited protein studies are **not presented as Ting-authored work**.

Unlike the [earlier paper-assisted CorA example](../astra_protein_pilot_2026-10-23/README.md), these are new sequence-only solving attempts. Protein identities and supporting sources appear only **after** each unchanged solution, as post-generation checks.

[Next focus: enzyme mutations and experimental evidence](ENZYME_MUTATION_FOCUS.md). Source selection is complete; mutation-focused teacher generation has not started.

## Read the examples

[All nine examples](ALL_EXAMPLES.md) · [Plain-text version](ALL_EXAMPLES.txt)

| Example | Topic | Task | Source-answer match | Scientific review |
|---|---|---|---|---|
| case-001 | [Covalent modification of a particular lysine](examples/case-001.md) | modified residue | Yes | Qualified modification-site inference |
| case-002 | [Locating repeated LYR sequence motifs](examples/case-002.md) | motif position | Yes | Supported sequence-indexing control |
| case-003 | [Recognizing a protein with multiple membrane-spanning segments](examples/case-003.md) | transmembrane | Yes | Qualified membrane-architecture inference |
| case-004 | [Distinguishing heme from flavin and iron-sulfur cofactors](examples/case-004.md) | cofactor | Yes | Strong sequence-based explanation |
| case-005 | [Calcium binding](examples/case-005.md) | cofactor | Yes | Strong sequence-based explanation |
| case-006 | [Membrane anchoring](examples/case-006.md) | transmembrane | Yes | Strong sequence-based explanation |
| case-007 | [Protein-interaction domains](examples/case-007.md) | domain feature | Yes | Strong sequence-based explanation |
| case-008 | [Chromophore binding](examples/case-008.md) | binding site | Yes | Qualified chromophore-mechanism inference |
| case-009 | [Post-translational modification chemistry](examples/case-009.md) | catalytic activity | Yes | Qualified enzyme-family inference |

## What was measured

- Teacher: GPT-6 Astra, maximum reasoning effort, pro mode. Nine concurrent requests, with no automatic paid retries.
- Structured outputs available: 9/9. Selected answers matching the frozen source-supported labels: 9/9. This is a deliberately selected pilot, not a benchmark accuracy estimate.
- Parallel batch elapsed time: approximately 8.9 minutes, including local dispatch and completion accounting. Individual request times are recorded separately.
- Recorded usage-based cost: **$10.7952** at standard rates. Billing-unknown cases: 0. This is a usage calculation, not an independently retrieved invoice.

Exact requests, all available generated text, structured solutions, sequence checks and [usage/cost components](usage_and_cost.json) are included. Internal private reasoning traces are not exposed by the API; the visible worked solutions are externally justified explanations requested from the teacher.

## How to interpret quality

Matching a source-supported answer, verifying literal sequence coordinates, and judging a biological explanation are separate checks. A correct letter can accompany an incomplete or unsupported explanation. The scientific review and source qualifications remain visible for every case, including mistakes and failed outputs. Papers establish or qualify the reference answer; they do not prove that Astra derived its answer from the sequence.

Assistant review rated **four biological explanations strong and four moderate**. The remaining example is a deliberately simple **exact motif-indexing control**, rather than a deep biological inference. The strongest examples connect several sequence features to a mechanism or architecture; the moderate examples retain explicit limits on family recognition and topology inference.

These are assistant-reviewed research drafts. No expert human validation, student training improvement, or production-quality dataset release is claimed.

## Reproducibility and sources

- [Student questions](questions.jsonl): the exact solver prompts plus sequence, task, question and choices.
- [Shared system instructions](system_prompt.txt) and per-example exact `request.json` files under `artifacts/`.
- [Verification identities and labels](verification.jsonl), held out of generation.
- Frozen UniProt record objects are included as `artifacts/case-XXX/uniprot_record.json`; acquisition wrappers and private paths are excluded. These records were withheld from Astra.
- [Source notes and paper links](source_notes.json), including the scope actually inspected. Full paper texts are not redistributed here.
- [Scientific review](review.json) and per-example `generated_output.json` and `generated_output.txt`.

Protein sequences and curated source facts derive from **UniProtKB, release 2026_03**, attributed to the [UniProt Consortium](https://www.uniprot.org/). UniProt data are provided under [CC BY 4.0](https://www.uniprot.org/help/license). Questions are adaptations of the project’s source-bound protein task pool; Astra-generated answers are identified as such. This attribution does not apply a new license to the cited papers.
