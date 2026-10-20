# Faster training: evidence and a controlled comparison

Reviewed October 19, 2026, fixed PST (UTC−8).

**The measured 2-B200 baseline is reproducible; its implementation is not an optimized hardware limit.** The original run achieved **14,527 tokens/s** and verification achieved **14,522 tokens/s**. Both use the Qwen3-4B architecture, **4,022,468,096 parameters**, 4,096-token sequences and 32 sequences / **131,072 token positions per optimizer update**. The stack is PyTorch 2.8, Transformers 4.57.1, BF16 computation, FP32 master parameters/gradients/AdamW moments, FSDP1 FULL_SHARD, activation checkpointing enabled and compilation disabled. Setup, warmup and the separate profiler step are excluded from measured throughput. [Original result](results_241355.json); [verification](results_242255.json).

The profiler observed `aten::_efficient_attention` operators and CUTLASS attention kernels named `sm80` on B200. This identifies the executed path, not a measured speedup from replacing it. The two attempts that jointly disabled checkpointing and changed sharding ran out of memory; they did not isolate either change or establish a faster configuration.

## Improve the BF16 implementation first

| Technique and primary reference | Published evidence | Application to this workload |
|---|---|---|
| **[FlashAttention-4](https://arxiv.org/abs/2603.05451)**, March 2026 | On B200 with BF16, up to **1.3× versus cuDNN 9.13** and **2.7× versus Triton** for attention. | Test a Blackwell attention implementation with the same causal/grouped-query semantics. These are **attention-kernel** speedups, not whole-training gains and not comparisons against our exact executed kernel. |
| **[Liger Kernel](https://arxiv.org/abs/2410.10989)**, 2024/2025 | Reports average **20% higher training throughput and 60% less GPU memory** across its evaluated Hugging Face workloads using fusion and chunking. | Its [maintained implementation](https://github.com/linkedin/Liger-Kernel) supports Qwen3, including fused linear cross-entropy, RMSNorm and SwiGLU. These aggregate numbers are not Qwen3-4B/B200 guarantees. |
| **[Cut Your Losses](https://arxiv.org/abs/2411.09009)**, ICLR 2025 | Avoids materializing the full token-by-vocabulary logits matrix. Gemma2-2B loss memory fell **24 GB → 1 MB**; classifier-head training memory **28 GB → 1 GB**, with comparable convergence. | Our vocabulary has **151,936 entries**, making fused/chunked loss a concrete memory target. The quoted savings concern the loss/head, not total model memory. Compare correctness and memory before changing batch size. |
| **[TorchTitan](https://arxiv.org/abs/2410.06511)**, 2024/2025 | Integrates compilation, FSDP2, selective recomputation and low precision in controlled training recipes. Its reported gains combine optimizations at much larger H100 scales. | Use its composable recipe design; isolate compilation and FSDP2 changes. Do not transplant a large-cluster headline as a two-GPU prediction. |

These priorities are an inference from the observed kernels and allocation failures. Neither the attention replacement nor a fused loss has been measured in this project.

## FP8: relevant B200 evidence

The closest readily reproducible dense-model reference is TorchAO's [B200 training benchmark](https://docs.pytorch.org/ao/stable/workflows/training.html#training-e2e-benchmarks-on-nvidia-b200): Llama3-8B on **eight power-limited B200s**, batch size 1, context 8,192, 100 steps, compilation, FSDP2 and selective activation checkpointing.

| Precision recipe | Reported median tokens/s | Gain over its BF16 baseline | Peak memory |
|---|---:|---:|---:|
| BF16 | 8,307.5 | — | 33.71 GB |
| FP8 tensorwise + FP8 all-gather | 10,417.0 | **25.4%** | 33.38 GB |
| MXFP8 cuBLAS | 9,969.0 | **20.0%** | 33.88 GB |
| FP8 rowwise | 8,640.5 | **4.0%** | 33.72 GB |

Values retain the source's reporting convention; compare **within this table**, not directly with our aggregate two-GPU rate. FP8 computation does not automatically halve total training memory. Scaling/quantization overhead and tensor shapes affect the gain.

That benchmark pins a PyTorch **2.9 development build**, TorchAO **0.13** and a TorchTitan commit. Our installed benchmark uses PyTorch **2.8**. A reproduction needs a separately pinned compatible environment and numerical checks before GPU timing; these are not switches already validated in the installed stack.

[Transformer Engine's support matrix](https://nvidia.github.io/TransformerEngine/support_matrix.html) lists native FP8/MXFP8 support on B200 and none on A100. Its [MXFP8 recipe](https://docs.nvidia.com/deeplearning/transformer-engine-releases/release-2.15/user-guide/features/low_precision_training/mxfp8/mxfp8.html) uses one scale per 32 elements. Keep two comparisons distinct: **matched BF16 hardware performance**, and **the best validated recipe for each hardware type**.

The [Meta/Crusoe MXFP8 report](https://pytorch.org/blog/accelerating-2k-scale-pre-training-up-to-1-28x-with-torchao-mxfp8-and-torchtitan-on-crusoe-b200-cluster/) provides larger-scale corroboration: **1.22–1.28× training throughput**, equivalent loss curves, Llama3-70B up to 1,856 B200s. It does not predict our two-GPU gain.

## What the training papers establish

**[DeepSeek-V3](https://arxiv.org/html/2412.19437v1)** uses FP8 inputs for linear forward/backward matrix multiplications, fine-grained scaling and higher-precision accumulation. Attention, embeddings, output head and normalization retain higher precision; master weights/accumulated gradients remain FP32, Adam moments BF16. Controlled comparisons at 16B/1.33T and 230B/~0.9T tokens kept relative loss differences below 0.25%. It supports a careful mixed-precision recipe, not an isolated end-to-end FP8 speedup claim.

**[COAT](https://arxiv.org/html/2410.19313v3)**, ICLR 2025, compresses saved activations and Adam moments in addition to FP8 computation. Its headline results are approximately **1.54× less memory and 1.43× faster training**, with H100 Llama benchmarks and OLMo-1B/300B-token and OLMo-7B/250B-token quality studies. This addresses memory pressure directly. Results vary; some gains include larger feasible batches, and evaluations show small differences rather than exact equality.

**[NVFP4 pretraining](https://arxiv.org/html/2509.25149v2)**, revised March 2026, demonstrates a 12B hybrid model trained for **10T tokens**, with MMLU-Pro **62.58 versus 62.62** for FP8. It requires selective higher precision, stochastic rounding, Hadamard transforms and careful scaling. The report focuses on numerical methodology, not measured runtime: its tensor-core arithmetic rates do not establish whole-training speedups. FP32 training states remain.

**[Delta-Matching](https://arxiv.org/abs/2609.37852)**, September 2026, studies stable native FP8 attention, including degradation short runs can conceal. It belongs on the watchlist; we have not measured its speed, integration or convergence here.

## Proposed tests and acceptance criteria

1. **BF16 kernel checks:** compare the executed attention path with a supported faster implementation; separately compare standard loss with fused/chunked loss. Check causal masking, gradient/loss agreement and memory.
2. **BF16 systems checks:** test compilation, FSDP2 and selective checkpointing as separate changes. Preserve optimizer mathematics; record actual communication and attention kernels.
3. **B200 precision checks:** compare FP8 tensorwise and MXFP8 against the improved BF16 baseline. Change activation/optimizer compression separately if memory remains limiting.
4. **Real-text confirmation:** use the same starting checkpoint, ordered biological text, token budget and optimizer settings for loss/convergence checks before long CPT. A 20-minute synthetic benchmark cannot validate biological capability or long-run numerical stability.

Hold context **4,096**, global batch **32 sequences**, and equivalent AdamW settings fixed for speed comparisons; adjust accumulation to preserve tokens/update when microbatch changes. Record setup/compile time separately, measured step time/tokens per second, peak allocated/reserved memory, failures and real-text validation loss. Changes that alter numerics require quality evidence. Do not multiply unrelated papers' speedups together. This research note does not launch jobs, install packages, alter queued experiments or allocate another GPU budget.
