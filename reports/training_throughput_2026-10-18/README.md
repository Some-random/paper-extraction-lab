# 4B training-throughput diagnostic

Report updated **2026-10-19T21:54:48-08:00**. Cluster snapshot: **2026-10-18T11:56:06.264883-08:00**.

Runtime setup: **ready**.

The earlier setup failed with **TimeoutExpired**. Its cancelled requests are retained below. Replacement CPU validation passed.

Scheduler last checked **2026-10-19T21:54:46-08:00**. Monitor: **watching**. [Status snapshot](status.json).

While work is pending or running, this page is updated hourly even without a status change, and promptly on failure or completion. A separate session monitor queues the requested hourly chat updates.

This is a short compute diagnostic using the pinned **Qwen3-4B architecture**, random initialization, synthetic token IDs and a **4,096-token context**. The baseline runs BF16 computation with FP32 master parameters and conventional AdamW optimizer states; optimization profiles identify their precision and kernel changes. No pretrained weights or biological training corpus are downloaded for the benchmark.

## B200 optimization sweep

A controlled two-B200 sweep keeps the Qwen3-4B architecture, 4,096-token context and 131,072 input positions per optimizer update fixed. It compares attention backends, fused losses and pointwise kernels, checkpointing, sharding, compilation and native low precision. Individual changes precede selected combinations; unavailable features and failures stay visible.

This allocation is bounded to **two hours / four GPU-hours**, with a persistent 110-minute suite budget. Setup and warmup are outside steady training throughput. Warmup includes compilation where enabled. Numerical smoke checks establish executable compatibility, not biological quality or long-run convergence. [Evidence and test rationale](training_speedups_2026-10-19.md).

The planned comparisons include PyTorch Flash/cuDNN and FlashAttention-4; Liger and Cut Cross-Entropy; activation recomputation and batch sizes; FSDP2; compilation; native FP8/MXFP8 and FP8 communication; and an explicitly labeled 8-bit AdamW-state variant. The final combinations use successful earlier measurements. Any options left by the time limit are shown as skipped.

COAT's released integration requires incompatible library versions. Native NVFP4 requires a separate training-library build in this environment. Both remain unavailable here; neither is counted as an executed speed test.

### Optimization job 242576

Allocation: **2 × B200 180GB**. Scheduler status: **success**.

Fastest completed profile: **best_micro8**, **62,150 input tokens/s**; **4.28×** the new baseline.

| Profile | Parent | Attention / precision | Status | Input tokens/s | Peak allocated GiB |
|:---|:---|:---|:---|---:|---:|
| baseline | — | sdpa_auto / bf16 | completed | 14,534 | 61.91 |
| attention_flash | baseline | sdpa_flash / bf16 | failed — RuntimeError | — | — |
| attention_cudnn | baseline | sdpa_cudnn / bf16 | completed | 32,008 | 61.85 |
| attention_fa4 | baseline | flash_attn4 / bf16 | completed | 33,318 | 61.85 |
| loss_liger | baseline | sdpa_auto / bf16 | completed | 14,524 | 38.32 |
| loss_cce | baseline | sdpa_auto / bf16 | completed | 13,721 | 38.32 |
| liger_pointwise | loss_liger | sdpa_auto / bf16 | failed — LauncherNonzeroExit | — | — |
| best_bf16_kernels | baseline | flash_attn4 / bf16 | completed | 33,323 | 61.85 |
| checkpoint_off | best_bf16_kernels | flash_attn4 / bf16 | completed | 42,640 | 152.57 |
| memory_baseline_micro2 | best_bf16_kernels | flash_attn4 / bf16 | completed | 32,095 | 46.37 |
| checkpoint_off_micro2 | memory_baseline_micro2 | flash_attn4 / bf16 | completed | 41,006 | 91.74 |
| memory_baseline_micro1 | best_bf16_kernels | flash_attn4 / bf16 | completed | 30,240 | 38.64 |
| checkpoint_off_micro1 | memory_baseline_micro1 | flash_attn4 / bf16 | completed | 38,312 | 61.32 |
| checkpoint_selective | best_bf16_kernels | flash_attn4 / bf16 | failed — LauncherNonzeroExit | — | — |
| shard_grad | best_bf16_kernels | flash_attn4 / bf16 | completed | 33,835 | 68.43 |
| fsdp2 | best_bf16_kernels | flash_attn4 / bf16 | completed | 32,967 | 69.45 |
| optimizer_8bit | fsdp2 | flash_attn4 / bf16 | failed — LauncherNonzeroExit | — | — |
| optimizer_8bit_no_recompute | optimizer_8bit | flash_attn4 / bf16 | completed | 37,895 | 149.01 |
| fp8_tensorwise | fsdp2 | flash_attn4 / float8_tensorwise | completed | 17,579 | 69.45 |
| fp8_rowwise | fsdp2 | flash_attn4 / float8_rowwise | failed — LauncherNonzeroExit | — | — |
| mxfp8 | fsdp2 | flash_attn4 / mxfp8 | failed — NumericalMismatch | — | — |
| nvfp4 | fsdp2 | flash_attn4 / nvfp4 | unavailable — UnsupportedFeature | — | — |
| compiled_fsdp1 | best_bf16_kernels | flash_attn4 / bf16 | completed | 50,730 | 61.85 |
| compiled_fsdp2 | fsdp2 | flash_attn4 / bf16 | completed | 50,353 | 69.45 |
| compiled_fp8_tensorwise | fp8_tensorwise | flash_attn4 / float8_tensorwise | failed — LauncherNonzeroExit | — | — |
| fp8_all_gather | compiled_fp8_tensorwise | flash_attn4 / float8_tensorwise | completed | 57,239 | 69.35 |
| compiled_mxfp8 | mxfp8 | flash_attn4 / mxfp8 | failed — NumericalMismatch | — | — |
| best_micro1 | fp8_all_gather | flash_attn4 / float8_tensorwise | completed | 40,438 | 46.18 |
| best_micro2 | fp8_all_gather | flash_attn4 / float8_tensorwise | completed | 51,721 | 53.88 |
| best_micro8 | fp8_all_gather | flash_attn4 / float8_tensorwise | completed | 62,150 | 100.30 |
| best_micro16 | best_micro8 | flash_attn4 / float8_tensorwise | failed — LauncherNonzeroExit | — | 132.16 |

Full feature settings, timings and retained failures are in the [sanitized results](results_242576.json).

## Throughput verification

These follow-up allocations separate **setup, warmup and timed training**. Each uses the same 4B architecture, 4,096-token context and **131,072 input tokens per optimizer update**. The baseline retains activation checkpointing and FSDP FULL_SHARD, using microbatch 4 per GPU. The two-B200 allocation also tests checkpointing disabled with SHARD_GRAD_OP, at microbatches 4 and 8.

The two requests add at most **3.33 GPU-hours** (two B200s and eight A100s, 20 minutes each), with one benchmark allocation running at a time. **Only baseline-to-baseline measurements compare the same training recipe across hardware.** Faster tuned profiles are separate optimization results. A timeout provides no training-speed ranking.

| Job / allocation | Status | Baseline input tokens/s | Fastest completed tuning input tokens/s |
|:---|:---|---:|---:|
| 242255 / 2 × B200 180GB | success | 14,522 | — |
| 242256 / 8 × A100 80GB | success | 21,897 | — |

**Timing scope:** input tokens/s divides timed training tokens by timed training wall time. Setup and warmup are excluded. A separate post-measurement profiler update is also excluded; profiler operator/device durations can overlap and must not be added as a wall-time breakdown.

Suite status: **completed**. Stop reason: **none**.

### Verification job 242255

| Profile / role | Checkpointing / sharding | Microbatch × accumulation | Status | Input tokens/s | Setup s | Warmup s | Timed training s | Profiler s |
|:---|:---|:---|:---|---:|---:|---:|---:|---:|
| baseline / baseline | on / full_shard | 4 × 4 | completed | 14,522 | 101.44 | 36.22 | 72.21 | 24.89 |
| tuned_micro4 / tuning | off / shard_grad_op | 4 × 4 | failed — OutOfMemoryError | — | 31.38 | — | — | — |
| tuned_micro8 / tuning | off / shard_grad_op | 8 × 2 | failed — OutOfMemoryError | — | 31.25 | — | — | — |

**baseline:** observed attention operators: `aten::_efficient_attention_backward`, `fmha_cutlassB_bf16_aligned_128x128_k128_seqaligned_sm80(PyTorchMemEffAttention::AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128, true>::Params)`, `aten::_efficient_attention_forward`, `fmha_cutlassF_bf16_aligned_64x128_rf_sm80(PyTorchMemEffAttention::AttentionKernel<cutlass::bfloat16_t, cutlass::arch::Sm80, true, 64, 128, 128, true, true>::Params)`, `aten::_scaled_dot_product_efficient_attention`, `aten::scaled_dot_product_attention`; observed CUDA kernels: `fmha_cutlassB_bf16_aligned_128x128_k128_seqaligned_sm80(PyTorchMemEffAttention::AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128, true>::Params)`, `fmha_cutlassF_bf16_aligned_64x128_rf_sm80(PyTorchMemEffAttention::AttentionKernel<cutlass::bfloat16_t, cutlass::arch::Sm80, true, 64, 128, 128, true, true>::Params)`.

Last retained milestone for **tuned_micro4**: **first_optimizer_update_complete**, 38.73 seconds after process start. This identifies progress, not the cause of a stall.

Last retained milestone for **tuned_micro8**: **first_forward_start**, 31.26 seconds after process start. This identifies progress, not the cause of a stall.

Suite status: **completed**. Stop reason: **none**.

### Verification job 242256

| Profile / role | Checkpointing / sharding | Microbatch × accumulation | Status | Input tokens/s | Setup s | Warmup s | Timed training s | Profiler s |
|:---|:---|:---|:---|---:|---:|---:|---:|---:|
| baseline / baseline | on / full_shard | 4 × 1 | completed | 21,897 | 63.74 | 20.35 | 47.89 | 12.42 |

**baseline:** observed attention operators: `aten::_efficient_attention_backward`, `fmha_cutlassB_bf16_aligned_128x128_k128_seqaligned_sm80(PyTorchMemEffAttention::AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128, true>::Params)`, `aten::_efficient_attention_forward`, `fmha_cutlassF_bf16_aligned_64x128_rf_sm80(PyTorchMemEffAttention::AttentionKernel<cutlass::bfloat16_t, cutlass::arch::Sm80, true, 64, 128, 128, true, true>::Params)`, `aten::_scaled_dot_product_efficient_attention`, `ScaledDotProductEfficientAttentionBackward0`; observed CUDA kernels: `fmha_cutlassB_bf16_aligned_128x128_k128_seqaligned_sm80(PyTorchMemEffAttention::AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128, true>::Params)`, `fmha_cutlassF_bf16_aligned_64x128_rf_sm80(PyTorchMemEffAttention::AttentionKernel<cutlass::bfloat16_t, cutlass::arch::Sm80, true, 64, 128, 128, true, true>::Params)`.

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
| 242256 | success | 8 | NVIDIA A100-SXM4-80GB | 21,897 | 105.71 days |
| 242576 | success | 2 | NVIDIA B200 | 14,534 | 159.27 days |

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

### Job 242256

Status: **success**. Sanitized diagnostics: [results_242256.json](results_242256.json).

Measured 8 optimizer steps after 3 warmup steps. Context: 4096; microbatch per GPU: 4; gradient accumulation: 1.

| Microbatch/GPU | Accumulation | Status | Measured input tokens/s |
|---:|---:|:---|---:|
| 4 | 1 | completed | 21,897 |

### Job 242576

Status: **success**. Sanitized diagnostics: [results_242576.json](results_242576.json).

Measured 8 optimizer steps after 3 warmup steps. Context: 4096; microbatch per GPU: 4; gradient accumulation: 4.

| Microbatch/GPU | Accumulation | Status | Measured input tokens/s |
|---:|---:|:---|---:|
| 4 | 4 | completed | 14,534 |
| 4 | 4 | failed — RuntimeError | — |
| 4 | 4 | completed | 32,008 |
| 4 | 4 | completed | 33,318 |
| 4 | 4 | completed | 14,524 |
| 4 | 4 | completed | 13,721 |
| 4 | 4 | failed — LauncherNonzeroExit | — |
| 4 | 4 | completed | 33,323 |
| 4 | 4 | completed | 42,640 |
| 2 | 8 | completed | 32,095 |
| 2 | 8 | completed | 41,006 |
| 1 | 16 | completed | 30,240 |
| 1 | 16 | completed | 38,312 |
| 4 | 4 | failed — LauncherNonzeroExit | — |
| 4 | 4 | completed | 33,835 |
| 4 | 4 | completed | 32,967 |
| 4 | 4 | failed — LauncherNonzeroExit | — |
| 4 | 4 | completed | 37,895 |
| 4 | 4 | completed | 17,579 |
| 4 | 4 | failed — LauncherNonzeroExit | — |
| 4 | 4 | failed — NumericalMismatch | — |
| 4 | 4 | unavailable — UnsupportedFeature | — |
| 4 | 4 | completed | 50,730 |
| 4 | 4 | completed | 50,353 |
| 4 | 4 | failed — LauncherNonzeroExit | — |
| 4 | 4 | completed | 57,239 |
| 4 | 4 | failed — NumericalMismatch | — |
| 1 | 16 | completed | 40,438 |
| 2 | 8 | completed | 51,721 |
| 8 | 2 | completed | 62,150 |
| 16 | 1 | failed — LauncherNonzeroExit | — |

## What the measurement covers

The timing includes synthetic-input transfers, forward/backward passes, optimizer updates and the communication used by this allocation. The original matched comparison uses FSDP FULL_SHARD and activation checkpointing. Verification tuning profiles list their different settings above. The original comparisons request PyTorch SDPA without torch.compile; observed backend evidence, when available, is reported separately. Setup, warmup and profiling are outside the measured denominator.

Production corpus loading, biological learning quality, validation, checkpoint saving, restart behavior and multi-node scaling are **not tested**. Queueing and interruptions are excluded from the compute-time estimate. No full 200B-token training run has been started.

The original comparison and verification allocations are bounded to 20 minutes and at most eight GPUs. The optimization allocation above uses two B200s for at most two hours. No existing jobs are modified by this diagnostic.
