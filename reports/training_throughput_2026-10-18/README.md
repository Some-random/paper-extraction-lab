# 4B training-throughput diagnostic

Report updated **2026-10-19T13:38:59-08:00**. Cluster snapshot: **2026-10-18T11:56:06.264883-08:00**.

Runtime setup: **ready**.

The earlier setup failed with **TimeoutExpired**. Its cancelled requests are retained below. Replacement CPU validation passed.

Scheduler last checked **2026-10-19T13:38:57-08:00**. Monitor: **watching**. [Status snapshot](status.json).

While work is pending or running, this page is updated hourly even without a status change, and promptly on failure or completion. A separate session monitor queues the requested hourly chat updates.

This is a short compute diagnostic using the pinned **Qwen3-4B architecture**, random initialization, synthetic token IDs and a **4,096-token context**. It runs BF16 forward/backward computation with FP32 master parameters and conventional AdamW optimizer states. No pretrained weights or biological training corpus are downloaded for the benchmark.

## Throughput verification

These follow-up allocations separate **setup, warmup and timed training**. Each uses the same 4B architecture, 4,096-token context and **131,072 input tokens per optimizer update**. The baseline retains activation checkpointing and FSDP FULL_SHARD, using microbatch 4 per GPU. The two-B200 allocation also tests checkpointing disabled with SHARD_GRAD_OP, at microbatches 4 and 8.

The two requests add at most **3.33 GPU-hours** (two B200s and eight A100s, 20 minutes each), with one benchmark allocation running at a time. **Only baseline-to-baseline measurements compare the same training recipe across hardware.** Faster tuned profiles are separate optimization results. A timeout provides no training-speed ranking.

| Job / allocation | Status | Baseline input tokens/s | Fastest completed tuning input tokens/s |
|:---|:---|---:|---:|
| 242255 / 2 × B200 180GB | success | 14,522 | — |
| 242256 / 8 × A100 80GB | queued | — | — |

**Timing scope:** input tokens/s divides timed training tokens by timed training wall time. Setup and warmup are excluded. A separate post-measurement profiler update is also excluded; profiler operator/device durations can overlap and must not be added as a wall-time breakdown.

### Verification job 242255

| Profile / role | Checkpointing / sharding | Microbatch × accumulation | Status | Input tokens/s | Setup s | Warmup s | Timed training s | Profiler s |
|:---|:---|:---|:---|---:|---:|---:|---:|---:|
| baseline / baseline | on / full_shard | 4 × 4 | completed | 14,522 | 101.44 | 36.22 | 72.21 | 24.89 |
| tuned_micro4 / tuning | off / shard_grad_op | 4 × 4 | failed — OutOfMemoryError | — | 31.38 | — | — | — |
| tuned_micro8 / tuning | off / shard_grad_op | 8 × 2 | failed — OutOfMemoryError | — | 31.25 | — | — | — |

**baseline:** observed attention operators: `aten::_efficient_attention_backward`, `fmha_cutlassB_bf16_aligned_128x128_k128_seqaligned_sm80(PyTorchMemEffAttention::AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128, true>::Params)`, `aten::_efficient_attention_forward`, `fmha_cutlassF_bf16_aligned_64x128_rf_sm80(PyTorchMemEffAttention::AttentionKernel<cutlass::bfloat16_t, cutlass::arch::Sm80, true, 64, 128, 128, true, true>::Params)`, `aten::_scaled_dot_product_efficient_attention`, `aten::scaled_dot_product_attention`; observed CUDA kernels: `fmha_cutlassB_bf16_aligned_128x128_k128_seqaligned_sm80(PyTorchMemEffAttention::AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128, true>::Params)`, `fmha_cutlassF_bf16_aligned_64x128_rf_sm80(PyTorchMemEffAttention::AttentionKernel<cutlass::bfloat16_t, cutlass::arch::Sm80, true, 64, 128, 128, true, true>::Params)`.

Last retained milestone for **tuned_micro4**: **first_optimizer_update_complete**, 38.73 seconds after process start. This identifies progress, not the cause of a stall.

Last retained milestone for **tuned_micro8**: **first_forward_start**, 31.26 seconds after process start. This identifies progress, not the cause of a stall.

## Matched GPU allocation comparison

All allocations use **32 sequences × 4,096 positions = 131,072 input tokens per optimizer update**, BF16 computation, FP32 AdamW and FSDP FULL_SHARD. Each tests microbatches of 1, 2 and 4 per GPU with matching gradient accumulation. Each profile requests three warmup and eight measured updates. OOM, partial and skipped profiles remain visible; only fully completed profiles can supply the reported best rate.

Each allocation has a **20-minute wall limit**; the listed requests together use at most **7.33 GPU-hours**. Slurm schedules these requests normally; the earlier idle-only admission gate has been removed. After-any dependencies limit execution to one benchmark allocation at a time. Queue waiting is separate from execution time.

| Allocation | Status | Best completed input tokens/s | Seconds/update | Peak memory/GPU |
|:---|:---|---:|---:|---:|
| 2 × B200 180GB | success | 14,527 | 9.02 | 61.9 GiB |
| 8 × A100 80GB | failed | — | — | — |
| 4 × B200 180GB | queued | — | — | — |
| 8 × B200 180GB | queued | — | — | — |

The earlier one-B200 diagnostic uses a different global batch and provides context only. The comparison above reports the best of the tested profiles, not a claim of maximum possible performance. These short synthetic runs do not test biological learning or checkpoint recovery.

Two B200s and eight A100s use regular **il**. Four and eight B200s use preemptible **il-lo**, because regular B200 access is capped at two per user. GPU count alone does not remove preemption eligibility.

The benchmark initializes the **Qwen3-4B-Base architecture with random weights**. Proteo-R1's [official checkpoint configuration](https://huggingface.co/thinking-bio-lab/proteor1-understand/blob/main/config.json) identifies **Qwen3-4B-Instruct-2507** as its language backbone. Their core layer dimensions match; the context/RoPE settings and starting weights differ. These tests exclude Proteo-R1's protein-specific encoders and diffusion generator. [Configuration comparison](../../config/proteor1_backbone_reference.json).

## Cluster GPUs

Each node is counted once across partitions. Unallocated GPUs are not necessarily schedulable immediately; account limits, reservations and planned allocations can apply.

| GPU | Configured | Allocated | Unallocated on online nodes | On unavailable nodes |
|:---|---:|---:|---:|---:|
| A100 | 71 | 71 | 0 | 0 |
| B200 | 8 | 8 | 0 | 0 |
| TITANXP | 7 | 0 | 4 | 3 |
| RTX8000 | 20 | 4 | 16 | 0 |
| 2080TI | 30 | 0 | 30 | 0 |
| **Total** | **136** | **83** | **50** | **3** |

## Benchmark jobs

| Job | Status | GPUs | GPU type | Measured input tokens/s | 200B tokens at this allocation |
|:---|:---|---:|:---|---:|---:|
| 241120 | cancelled | 1 | A100 80GB | — | — |
| 241122 | cancelled | 8 | B200 180GB | — | — |
| 241333 | success | 1 | NVIDIA B200 | 6,546 | 353.61 days |
| 241334 | cancelled — replaced by the matched comparison | 8 | B200 180GB | — | — |
| 241355 | success | 2 | NVIDIA B200 | 14,527 | 159.35 days |
| 241356 | failed — NoCompletedMatchedProfile | 8 | A100 80GB | — | — |
| 241366 | queued | 4 | B200 180GB | — | — |
| 241367 | queued | 8 | B200 180GB | — | — |
| 242255 | success | 2 | NVIDIA B200 | 14,522 | 159.40 days |
| 242256 | queued | 8 | A100 80GB | — | — |

Measured token rates are aggregate input positions per second at the **actual measured GPU count**. The 200B-token duration is `200,000,000,000 / measured tokens per second`; no unmeasured GPU allocation or multi-node scaling is extrapolated.

### Job 241333

Status: **success**. Sanitized diagnostics: [results_241333.json](results_241333.json).

Measured 15 optimizer steps after 5 warmup steps. Context: 4096; microbatch per GPU: 1; gradient accumulation: 4.

### Job 241355

Status: **success**. Sanitized diagnostics: [results_241355.json](results_241355.json).

Measured 8 optimizer steps after 3 warmup steps. Context: 4096; microbatch per GPU: 4; gradient accumulation: 4.

| Microbatch/GPU | Accumulation | Status | Measured input tokens/s |
|---:|---:|:---|---:|
| 1 | 16 | completed | 13,826 |
| 2 | 8 | completed | 14,223 |
| 4 | 4 | completed | 14,527 |

### Job 241356

Status: **failed**. Sanitized diagnostics: [results_241356.json](results_241356.json).

| Microbatch/GPU | Accumulation | Status | Measured input tokens/s |
|---:|---:|:---|---:|
| 1 | 4 | failed — TimeoutExpired | — |
| 2 | 2 | failed — TimeoutExpired | — |
| 4 | 1 | skipped — InsufficientRemainingBudget | — |

### Job 242255

Status: **success**. Sanitized diagnostics: [results_242255.json](results_242255.json).

Measured 8 optimizer steps after 3 warmup steps. Context: 4096; microbatch per GPU: 4; gradient accumulation: 4.

| Microbatch/GPU | Accumulation | Status | Measured input tokens/s |
|---:|---:|:---|---:|
| 4 | 4 | completed | 14,522 |
| 4 | 4 | failed — OutOfMemoryError | — |
| 8 | 2 | failed — OutOfMemoryError | — |

## What the measurement covers

The timing includes synthetic-input transfers, forward/backward passes, optimizer updates and the communication used by this allocation. The original matched comparison uses FSDP FULL_SHARD and activation checkpointing. Verification tuning profiles list their different settings above. PyTorch SDPA attention is requested without torch.compile; observed backend evidence, when available, is reported separately. Setup, warmup and profiling are outside the measured denominator.

Production corpus loading, biological learning quality, validation, checkpoint saving, restart behavior and multi-node scaling are **not tested**. Queueing and interruptions are excluded from the compute-time estimate. No full 200B-token training run has been started.

Each requested allocation is bounded to 20 minutes and at most eight GPUs. No existing jobs are modified by this diagnostic.
