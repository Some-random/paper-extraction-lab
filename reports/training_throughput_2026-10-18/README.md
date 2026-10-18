# 4B training-throughput diagnostic

Report updated **2026-10-18T15:11:59-08:00**. Cluster snapshot: **2026-10-18T11:56:06.264883-08:00**.

Runtime setup: **ready**.

The earlier setup failed with **TimeoutExpired**. Its cancelled requests are retained below. Replacement CPU validation passed.

Scheduler last checked **2026-10-18T15:11:58-08:00**. Monitor: **watching**. [Status snapshot](status.json).

While work is pending or running, this page is updated hourly even without a status change, and promptly on failure or completion. Updates are GitHub reports; automatic chat notifications are not configured.

This is a short compute diagnostic using the pinned **Qwen3-4B architecture**, random initialization, synthetic token IDs and a **4,096-token context**. It runs BF16 forward/backward computation with FP32 master parameters and conventional AdamW optimizer states. No pretrained weights or biological training corpus are downloaded for the benchmark.

## Two B200s versus eight A100s

Both allocations use **32 sequences × 4,096 positions = 131,072 input tokens per optimizer update**, BF16 computation, FP32 AdamW and FSDP FULL_SHARD. Each tests microbatches of 1, 2 and 4 per GPU with matching gradient accumulation. Each profile requests three warmup and eight measured updates. OOM, partial and skipped profiles remain visible; only fully completed profiles can supply the reported best rate.

Each allocation has a **20-minute wall limit**; both together use at most **3.33 GPU-hours**. Requests wait for observed spare capacity and a scheduler preview without proposed preemptions. Queue waiting is separate from execution time.

| Allocation | Status | Best completed input tokens/s | Seconds/update | Peak memory/GPU |
|:---|:---|---:|---:|---:|
| 2 × B200 180GB | waiting for spare capacity | — | — | — |
| 8 × A100 80GB | waiting for spare capacity | — | — | — |

The earlier one-B200 diagnostic uses a different global batch and provides context only. The comparison above reports the best of the tested profiles, not a claim of maximum possible performance. These short synthetic runs do not test biological learning or checkpoint recovery.

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
| 241355 | queued — waiting for spare capacity | 2 | B200 180GB | — | — |
| 241356 | queued — waiting for spare capacity | 8 | A100 80GB | — | — |

Measured token rates are aggregate input positions per second at the **actual measured GPU count**. The 200B-token duration is `200,000,000,000 / measured tokens per second`; no unmeasured GPU allocation or multi-node scaling is extrapolated.

### Job 241333

Status: **success**. Sanitized diagnostics: [results_241333.json](results_241333.json).

Measured 15 optimizer steps after 5 warmup steps. Context: 4096; microbatch per GPU: 1; gradient accumulation: 4.

## What the measurement covers

The timing includes synthetic-input transfers, forward/backward passes, optimizer updates and the communication used by this allocation. Multiple GPUs use FSDP FULL_SHARD. Activation checkpointing is enabled; PyTorch SDPA attention is used without torch.compile.

Production corpus loading, biological learning quality, validation, checkpoint saving, restart behavior and multi-node scaling are **not tested**. Queueing and interruptions are excluded from the compute-time estimate. No full 200B-token training run has been started.

Each requested allocation is bounded to 20 minutes and at most eight GPUs. No existing jobs are modified by this diagnostic.
