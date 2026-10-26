# Protein model training handoff

Prepared on 24 October 2026 for a new Codex session taking over model training. **Post-trained Qwen3.5-4B** finished SFT on 10,000 sequence multiple-choice examples, but the saved evaluations do not establish an improvement. Most explanations were subsequently graded as annotation restatement or assumed protein identity. Compare the saved predictions fairly and improve the data before another training run.

PMC, TheBioCollection and FineWeb-Edu preparation continues separately; live outputs are not a validated training release. Preserve background jobs and resource limits. This handoff starts no jobs or paid generation. Two-hour updates remain disabled.

Project-relative paths start at `/dfs/scratch0/dongweij/paper-extraction-lab`. Read `AGENTS.md` before changes. For the tables below, **data run** means `experiments/sequence_mcq_10000_2026-10-23/`; **SFT run** means `experiments/qwen35_4b_sequence_sft_2026-10-23/`.

## Model and training data

Use **`Qwen/Qwen3.5-4B`**, revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`. The approved starting model is the post-trained checkpoint, not Qwen3.5-4B-Base. Its existing cache is:

```text
/dfs/scratch0/dongweij/bio-evaluation/.local/qwen35_4b_comparison_20261022/models/posttrained
```

The exact 10,000-example dataset used by the finished training run is:

```text
experiments/sequence_mcq_10000_2026-10-23/answer_letter_only_v1/native.jsonl
```

It contains 1,910 distinct protein sequences across 25 tasks; proteins repeat under different tasks. It is train-only. Dataset checksum: `bc048eb086e27853d5138d244b6246e1a1412fd429aaef25a73d2a541ad964a1`.

| Material | Location |
|---|---|
| Dataset pointer | Data run: `current_training_dataset.json` |
| Readable questions, explanations and letters | Data run: `answer_letter_only_v1/qa.txt` |
| Counts and task distribution | Data run: `answer_letter_only_v1/manifest.json` |
| Native format and masking checks | SFT run: `preflight/native_dataset_v3.json` |
| Public dataset | [Protein sequence reasoning 10k](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k) |

The original public training revision is `5876c223c5d3c60425e36eb332c54918d904952f`; later provenance updates preserved its rows. Historical dataset `student_training_authorized: false` and `student_training_started: false` fields predate the explicit authorization and completed training.

## Native Qwen format and loss

Each row has an `id` and two messages:

```json
{"id":"example-id","messages":[
  {"role":"user","content":"Full protein sequence, task, question and A–D choices"},
  {"role":"assistant","reasoning_content":"Generated worked explanation","content":"B"}
]}
```

The letter illustrates the schema. Real assistant `content` is exactly A, B, C or D. Keep the explanation in `reasoning_content`; the older final-answer format with a second justification is superseded.

Render with the cached tokenizer's native `apply_chat_template(..., enable_thinking=True)`. The native inference prefix opens `<think>`. The supervised completion continues the explanation, closes `</think>`, then emits the final selected letter and native turn end. **Both the visible explanation and final letter are training targets.** Mask every prompt token with `-100`; verify the inference prefix is an exact token prefix of the complete training example. Do not concatenate a second thinking block or discard the explanation field.

SFT run `runtime/trainer_v2.py`, function `encode_row`, implements these checks. Preflight passed all 10,000 rows without truncation; the longest complete example was 994 tokens. Luna explanations are generated visible worked solutions, not exports of private teacher reasoning.

## Finished training experiment

Job **248546 completed** all 10,000 examples in one epoch, with 313 optimizer updates. Actual training took approximately 111 minutes on **one Quadro RTX 8000**. Training completion does not establish better biological accuracy.

| Setting | Actual value |
|---|---|
| Starting weights | Post-trained Qwen3.5-4B at the revision above |
| Precision | FP16, no weight quantization |
| Adapter | LoRA rank 16, alpha 32, dropout 0 |
| Targets | 152 attention projections across all 32 hybrid text blocks; 14,376,960 trainable parameters |
| Optimizer | AdamW; learning rate 0.0001; weight decay 0.01 |
| Schedule | 3% warmup; gradient norm clipped at 1.0; seed 42 |
| Actual batch | Microbatch 2, accumulation 16, effective batch 32; the proposed microbatch 4 failed memory admission |
| Context | 1,024; full examples, no truncation |
| Exposure | 0.003561706 billion input tokens, including 0.000779728 billion supervised completion tokens |
| Memory | Gradient checkpointing enabled |
| Development callback | None; development loss fields are null |

| Artifact | Location |
|---|---|
| Actual configuration | SFT run: `config.train_v3.json` |
| Actual executed trainer | SFT run: `runtime/trainer_v2.py` |
| Final summary and actual runtime | SFT run: `train_v2/summary.json` and `train_v2/started.json` |
| Final adapter | SFT run: `train_v2/adapter` |
| Intermediate adapters | SFT run: `train_v2/checkpoints/step_000100`, `step_000200`, `step_000300` |
| Metrics | SFT run: `train_v2/train_metrics.jsonl` |
| Actual batch admission | SFT run: `train_v2/gpu_batch_admission.json` |

Environment: PyTorch 2.8.0, Transformers 5.17.0, PEFT 0.21.2, Accelerate 1.12.0, CUDA 12.8. Preserve `runtime/plain_linear_backend_v1.py` and its preflight: it fixed failed attempt 248535's TorchAO incompatibility. `runtime/launch_v2.py` restores the required package overlay.

For a read-only status check:

```bash
cd /dfs/scratch0/dongweij/paper-extraction-lab
python3 -B experiments/qwen35_4b_sequence_sft_2026-10-23/monitoring/summarize_training_v2.py
```

`current_training_run.json` still records an early four-update observation. Use the final summary instead. Do not relaunch the completed configuration into its existing output directory.

## LiveProteinBench results and saved generations

The saved checkpoint diagnostic used a prespecified balanced **240-question pilot**, 20 questions in each of 12 tasks. Selection used a case-ID hash rather than labels or outcomes. Invalid final answers count as incorrect; explanations do not receive separate scoring credit.

| Checkpoint step | Training examples seen | Evaluation job | Accuracy |
|---|---:|---:|---:|
| 100 | 3,200 | 248638 | 22.92% |
| 200 | 6,400 | 248758 | 22.50% |
| 300 | 9,600 | 248759 | 23.75% |
| 313 | 10,000 | 248757 | 20.83% |

All four completed; none was selected as a winner. This partial, previously observed pilot does not establish a training effect against the unchanged model.

Protocol: native thinking, merged BF16, context 65,536, output cap 32,768; one sample, temperature 1, top-p 0.95, top-k 20, presence penalty 1.5, seed 42, concurrency 16. Score the final letter; truncations/malformed outputs fail. Preserve the frozen protocol.

| Material | Location |
|---|---|
| Pilot protocol | SFT run: `evaluation/checkpoint_0100_v3/plan.json` |
| Result table and per-task summary | SFT run: `evaluation/later_checkpoints_v3/comparison_watch_v3/REPORT.md` and adjacent `summary.json` |
| Step 100 saved generations | SFT run: `evaluation/checkpoint_0100_v3/runtime/cases/` |
| Later saved generations | SFT run: `evaluation/later_checkpoints_v3/checkpoint_0200/runtime/cases/`, with equivalent `checkpoint_0300` and `checkpoint_0313` directories |

Each runtime also contains scores and a prediction seal. Keep private reference/prepared files local and out of training inputs.

### The unchanged thinking baseline finished separately

The external original-model evaluation subsequently completed all **1,736 approved questions**, with 502 correct and 149 invalid answers: **28.92% overall accuracy and 28.59% task-average accuracy**. Generation continuation 248796 and CPU publication 249009 finished; do not launch a duplicate baseline.

Its current completion evidence is:

```text
/dfs/scratch0/dongweij/bio-evaluation/.local/qwen35_4b_thinking_enabled_20261022/continuation_20261023_v2/owner_progress.json
/dfs/scratch0/dongweij/bio-evaluation/.local/qwen35_4b_thinking_enabled_20261022/continuation_20261023_v2/runtime/combined/
```

The combined directory contains sealed predictions, provenance and `scores.json`. The [published original-model result](https://github.com/Some-random/bio-evaluation/blob/a232bacf9644456975bd8822cad3e65010f8a65b/reports/LIVEPROTEINBENCH_QWEN35_4B_POST_NATIVE_THINKING32K_V3_RESULT.md) records the completed baseline.

The checkpoint watcher still says `baseline_unavailable` because its paths predate that final continuation. **The CPU-only matched 240-case comparison remains pending.** Verify question IDs, prompts, parsing and generation settings, join sealed baseline predictions, and report paired overall/per-task changes. Full-baseline and balanced-pilot percentages have different case mixtures; do not directly compare them. Disclose hardware, merging and sampling differences.

All 240 pilot IDs occur in the completed baseline's `prediction_lock.json`; the recorded model and generation settings match. Join existing `runtime/combined/cases/<case_id>/` predictions using `combined_provenance.json`. Use the 149 invalid answers in `scores.json`, which differs from the generation-status count.

### Earlier direct-answer SFT results were negative

The earlier small-source experiment used a different protocol: NF4/FP16, thinking disabled, greedy decoding and a 16-token answer limit. Its matched baseline task-average accuracy was 31.27%. Protein-only SFT reached 26.81%, PMC-only 25.44%, a 25% PMC mixture 27.81%, a 50% PMC mixture 28.19%, and extended protein exposure 26.44%. All regressed overall against that matching baseline.

See `experiments/qwen35_4b_sft_2026-10-22/RESULTS.md` and that run's `evaluation/all_arms_followup_2026-10-22/REPORT.md`. Its sources were 128 PMC papers and 9,057 protein examples; FineWeb was absent. Lower development loss did not imply better benchmark accuracy. Keep these scores separate from BF16 thinking results.

## Data quality and paper provenance

GPT-6 Luna medium authored the 10k questions/explanations; fresh Luna calls judged them. Teachers received UniProt annotation packets absent from student sequence/question/choices. The papers attached afterward were **not supplied to the original 10k teacher**.

The audit graded 521 examples (**5.21%**) as supported sequence inference/direct demonstration and 8,699 (**86.99%**) as annotation restatement/assumed identity. There were 686 partial links, 30 inconsistent claims, 2 uncertain and 62 invalid/ungraded. These are AI diagnostics, not expert ground truth. No grade-based filtering preceded training.

Read `experiments/sequence_reasoning_strength_audit_2026-10-23/final_v1/REASONING_STRENGTH.txt`, adjacent `grades.tsv` and `reasoning_strength.jsonl`. The audit is not a validated replacement training set.

Public provenance is under `experiments/sequence_mcq_10000_2026-10-23/hf_release_v2_provenance/package/`: `SEQUENCE_PAPER_GUIDE.txt`, `SOURCE_GUIDE.md`, `provenance/examples.jsonl` and `provenance/sequence_paper_links.csv`. That release added 261 original papers with verified redistribution evidence. Follow example ID → sequence/accession/version → exact annotation → annotation-specific citation → paper. A general UniProt bibliography citation does not establish support for every annotation or every generated explanation sentence.

## Alice Ting lab review examples

The ten examples retain A–D choices and complete worked answers incorporating lab feedback. [Read the revised collection](../alice_training_examples_10_2026-10-24/ALL_EXAMPLES.md). The current revision is recorded in `revision_v6.json` and `review_v6.json` in that report directory. Questions 4–8 are explicitly foundational; the other items emphasize comparative evidence, assay interpretation and research judgments.

All ten current explanations are source-aware assistant revisions. Earlier unchanged teacher responses, source-aware edits and the failed TurboID generation attempt remain preserved in prior records. These are assistant source checks, not expert human validation or measured training gains. No new teacher calls were made for this revision.

These ten presentation examples do not change the 10,000 training rows. Their questions and worked explanations provide a reviewed starting point for discussing a future data recipe.

## Next work for the training session

1. Complete the CPU-only matched 240-case comparison. Preserve invalid answers and regressions; do not select a winner from already observed benchmark results.
2. Inspect saved generations and the reasoning audit. Build next examples whose student-visible evidence supports the intended inference, instead of relying on hidden decisive annotations.
3. Freeze a new dataset and genuinely separate development cohort before another run. Keep all **1,797 official LiveProteinBench questions and their 651 protein identities** excluded from training and synthetic generation, including the 61 held evaluation cases. Preserve existing development/quarantine/source exclusions. Exact matching and shared 8-mer screening do not certify remote-homology or publication separation.
4. Recheck full sequences, native thinking, masking, final-letter parsing, context and memory on the actual runtime. Version new code, data, configs and outputs; preserve earlier experiments. Different GPUs or longer explanations require new admission checks.
5. LiveProteinBench outcomes are already observed and the user wants it as a development reference. Further tuning on it is exploratory; independent confirmation needs a fresh locked external cohort. Preserve matched protocols and report per-task changes.

Source/split contracts: `experiments/protein_reasoning_recipe_2026-10-22/evaluation/protocol.json` and its `splits/README.md`. Their proposed conditions are historical; use the later actual checkpoint plan to reproduce finished thinking evaluations.

The [general corpus preparation report](../training_preparation_2026-10-21/README.md) covers acquisition, dedup, quality, provenance and export. Live partial outputs and provisionally retained FineWeb pages are not a validated biology release.

## Resource ownership for the next session

GPU ceilings and prior reservations are recorded in SFT run `authorization_v1.json`, `checkpoint_evaluation_authorization_v1.json` and `later_checkpoint_evaluation_authorization_v2.json`. Submission receipts are `train_submission_v2.json`, `evaluation/checkpoint_0100_v3/submission_v1.json` and `evaluation/later_checkpoints_v3/jobs.json`. Reconcile actual scheduler usage, including failed attempts, before new reservations; a historical remaining figure is not a new allowance.

Paid generation shares `experiments/protein_reasoning_scale_75000_2026-10-23/global_phase_registry_v1.json` and its adjacent `.coordinator.lock`. Preserve the cumulative $100 ceiling and unresolved billing reservations. The latest Alice attempt receipt is `experiments/alice_training_examples_10_2026-10-24/revision_v3/run_v3/receipt.json`; it records one completed response and one HTTP 502 with a $7 reservation and no returned answer. Do not retry that attempt or reset its accounting. Coordinate new GPU work with the ongoing corpus workers.

### Copy into the new Codex session

> Read `reports/training_handoff_2026-10-24/README.md` and `AGENTS.md`. Verify the finished 10k adapter, then complete the CPU-only matched 240-case comparison against the saved original-model baseline. Propose better grounded data and a matched experiment. Use post-trained Qwen3.5-4B with native thinking and explanation-plus-letter loss. Preserve exclusions, negative results, background corpus jobs and budgets. This handoff does not start new training or paid generation.
