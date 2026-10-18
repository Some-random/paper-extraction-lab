# 4B training-throughput diagnostic

Report updated **2026-10-18T14:45:19-08:00**. Cluster snapshot: **2026-10-18T11:56:06.264883-08:00**.

Runtime setup: **ready_jobs_held**.

The earlier setup failed with **TimeoutExpired**. Its cancelled requests are retained below. Replacement CPU validation passed.

Scheduler last checked **2026-10-18T14:45:07-08:00**. Monitor: **starting**. [Status snapshot](status.json).

While work is pending or running, this page is updated hourly even without a status change, and promptly on failure or completion. Updates are GitHub reports; automatic chat notifications are not configured.

This is a short compute diagnostic using the pinned **Qwen3-4B architecture**, random initialization, synthetic token IDs and a **4,096-token context**. It runs BF16 forward/backward computation with FP32 master parameters and conventional AdamW optimizer states. No pretrained weights or biological training corpus are downloaded for the benchmark.

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

**No completed throughput measurement yet.** Queued jobs have not produced a measured training-time estimate.

| Job | Status | GPUs | GPU type | Measured input tokens/s | 200B tokens at this allocation |
|:---|:---|---:|:---|---:|---:|
| 241120 | cancelled | 1 | A100 80GB | — | — |
| 241122 | cancelled | 8 | B200 180GB | — | — |
| 241333 | queued — runtime setup hold | 1 | B200 180GB | — | — |
| 241334 | queued — runtime setup hold | 8 | B200 180GB | — | — |

Measured token rates are aggregate input positions per second at the **actual measured GPU count**. The 200B-token duration is `200,000,000,000 / measured tokens per second`; no unmeasured GPU allocation or multi-node scaling is extrapolated.

## What the measurement covers

The timing includes synthetic-input transfers, forward/backward passes, optimizer updates and the communication used by this allocation. Multiple GPUs use FSDP FULL_SHARD. Activation checkpointing is enabled; PyTorch SDPA attention is used without torch.compile.

Production corpus loading, biological learning quality, validation, checkpoint saving, restart behavior and multi-node scaling are **not tested**. Queueing and interruptions are excluded from the compute-time estimate. No full 200B-token training run has been started.

Each requested allocation is bounded to 20 minutes and at most eight GPUs. No existing jobs are modified by this diagnostic.
