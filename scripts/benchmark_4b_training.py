#!/usr/bin/env python3
"""Bounded, offline dense-model training-throughput benchmark (no saved weights)."""

import argparse
from contextlib import nullcontext
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import socket
import statistics
import time
import traceback


def percentile(values, fraction):
    ordered = sorted(values)
    if not ordered or not 0 <= fraction <= 1:
        raise ValueError("Need observations and a percentile between zero and one")
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    return ordered[lower] + (ordered[math.ceil(position)] - ordered[lower]) * (position - lower)


def summarize(step_seconds, elapsed_seconds, *, world_size, batch_size, sequence_length,
              accumulation, target_tokens):
    if not step_seconds or any(not math.isfinite(t) or t <= 0 for t in step_seconds):
        raise ValueError("Measured step times must be finite and positive")
    if not math.isfinite(elapsed_seconds) or elapsed_seconds <= 0:
        raise ValueError("Measured elapsed time must be finite and positive")
    if any(value <= 0 for value in (world_size, batch_size, sequence_length,
                                    accumulation, target_tokens)):
        raise ValueError("Token and batch dimensions must be positive")
    step_tokens = world_size * batch_size * sequence_length * accumulation
    total_tokens = step_tokens * len(step_seconds)
    throughput = total_tokens / elapsed_seconds
    return dict(measured_optimizer_steps=len(step_seconds), input_tokens_per_step=step_tokens,
                measured_input_tokens=total_tokens, measured_wall_seconds=elapsed_seconds,
                input_tokens_per_second=throughput,
                step_seconds=dict(mean=statistics.mean(step_seconds),
                                  p50=percentile(step_seconds, .5),
                                  p95=percentile(step_seconds, .95), values=step_seconds),
                extrapolation=dict(target_input_tokens=target_tokens,
                                   gpu_count=world_size,
                                   seconds=target_tokens / throughput,
                                   days=target_tokens / throughput / 86400,
                                   scope="Measured GPU count only; excludes queueing, checkpoints, "
                                         "validation, interruptions and production data loading"))


def write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".{os.getpid()}.tmp")
    temporary.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sequence-length", type=int, default=4096)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--accumulation", type=int, default=4)
    parser.add_argument("--warmup", type=int, default=5)
    parser.add_argument("--steps", type=int, default=15)
    parser.add_argument("--max-runtime-seconds", type=int, default=600)
    parser.add_argument("--target-tokens", type=int, default=200_000_000_000)
    parser.add_argument("--seed", type=int, default=20261018)
    args = parser.parse_args()
    for name in ("sequence_length", "batch_size", "accumulation", "warmup", "steps",
                 "max_runtime_seconds", "target_tokens"):
        if getattr(args, name) <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    return args


def benchmark(args, result, start):
    # Imports deliberately stay here: report arithmetic is testable without CUDA dependencies.
    import torch
    import torch.distributed as dist
    from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
    from torch.distributed.fsdp import MixedPrecision, ShardingStrategy
    from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
    from functools import partial
    from transformers import Qwen3Config, Qwen3ForCausalLM
    from transformers.models.qwen3.modeling_qwen3 import Qwen3DecoderLayer

    rank = int(os.environ.get("RANK", "0"))
    local_rank = int(os.environ.get("LOCAL_RANK", "0"))
    world_size = int(os.environ.get("WORLD_SIZE", "1"))
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required; CPU timing is not a training throughput estimate")
    torch.cuda.set_device(local_rank)
    device = torch.device("cuda", local_rank)
    if not torch.cuda.is_bf16_supported():
        raise RuntimeError("GPU must support BF16")
    if world_size > 1:
        dist.init_process_group("nccl", timeout=timedelta(seconds=120))

    def barrier():
        if world_size > 1:
            dist.barrier()
        torch.cuda.synchronize(device)

    def maximum(value):
        tensor = torch.tensor(float(value), device=device, dtype=torch.float64)
        if world_size > 1:
            dist.all_reduce(tensor, op=dist.ReduceOp.MAX)
        return tensor.item()

    properties = torch.cuda.get_device_properties(device)
    hardware = dict(rank=rank, host=socket.gethostname(), gpu=properties.name,
                    total_memory_bytes=properties.total_memory,
                    compute_capability=list(torch.cuda.get_device_capability(device)))
    all_hardware = [None] * world_size
    if world_size > 1:
        dist.all_gather_object(all_hardware, hardware)
    else:
        all_hardware = [hardware]
    result.update(world_size=world_size, hardware=all_hardware,
                  packages={name: importlib.metadata.version(name)
                            for name in ("torch", "transformers")},
                  cuda_runtime=torch.version.cuda, cudnn_version=torch.backends.cudnn.version())
    config_bytes = args.model_config.read_bytes()
    config_data = json.loads(config_bytes)
    if config_data.get("model_type") != "qwen3":
        raise ValueError("Expected a pinned Qwen3 dense-model configuration")
    config = Qwen3Config.from_dict(config_data)
    config.use_cache = False
    config._attn_implementation = "sdpa"
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.set_float32_matmul_precision("high")
    # FP32 originals ensure FP32 Adam moments; BF16 compute comes from autocast/FSDP.
    model = Qwen3ForCausalLM(config).float()
    parameters = sum(parameter.numel() for parameter in model.parameters())
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.train()
    if world_size > 1:
        model = FSDP(model, device_id=device, sharding_strategy=ShardingStrategy.FULL_SHARD,
                     auto_wrap_policy=partial(transformer_auto_wrap_policy,
                                              transformer_layer_cls={Qwen3DecoderLayer}),
                     mixed_precision=MixedPrecision(param_dtype=torch.bfloat16,
                                                    reduce_dtype=torch.float32,
                                                    buffer_dtype=torch.bfloat16),
                     limit_all_gathers=True, use_orig_params=False)
    else:
        model = model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5, betas=(.9, .95),
                                 weight_decay=.1, fused=True)
    generator = torch.Generator().manual_seed(args.seed + rank)
    inputs_cpu = torch.randint(0, config.vocab_size,
                              (args.batch_size, args.sequence_length),
                              generator=generator, dtype=torch.long).pin_memory()
    result.update(actual_parameter_count=parameters, config_sha256=hashlib.sha256(config_bytes).hexdigest(),
                  attention="sdpa", initialization="random FP32; no model weights downloaded",
                  optimizer="fused AdamW; FP32 parameters, gradients and moments; BF16 compute",
                  sharding="FSDP FULL_SHARD" if world_size > 1 else "single GPU, unsharded",
                  gradient_checkpointing="nonreentrant", torch_compile=False,
                  input_kind="fixed synthetic uniform token IDs, CPU to GPU transfer each microbatch",
                  token_unit="Input token positions; causal loss predicts sequence_length - 1 positions")

    def train_step():
        optimizer.zero_grad(set_to_none=True)
        total_loss = torch.zeros((), device=device)
        for micro in range(args.accumulation):
            # FSDP no_sync retains full accumulated gradients until the last microbatch.
            sync = model.no_sync() if world_size > 1 and micro + 1 < args.accumulation else nullcontext()
            with sync:
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    inputs = inputs_cpu.to(device, non_blocking=True)
                    loss = model(input_ids=inputs, labels=inputs, use_cache=False).loss
                    scaled_loss = loss / args.accumulation
                    total_loss += scaled_loss.detach().float()
                scaled_loss.backward()
        norm = model.clip_grad_norm_(1.) if world_size > 1 else torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)
        nonfinite = not bool(torch.isfinite(total_loss).item() and torch.isfinite(norm).item())
        if maximum(int(nonfinite)):
            raise FloatingPointError("Nonfinite loss or gradient norm; optimizer update skipped")
        optimizer.step()
        if not result.get("optimizer_state_dtypes"):
            moment_dtypes = sorted({str(state[key].dtype) for state in optimizer.state.values()
                                    for key in ("exp_avg", "exp_avg_sq") if key in state})
            if moment_dtypes != ["torch.float32"]:
                raise RuntimeError(f"Expected FP32 Adam moments, got {moment_dtypes}")
            result["optimizer_state_dtypes"] = moment_dtypes
        if world_size > 1:
            dist.all_reduce(total_loss, op=dist.ReduceOp.SUM)
            total_loss /= world_size
        return total_loss.item()

    warmup_losses, losses, durations = [], [], []
    measurement_start = None
    total_steps = args.warmup + args.steps
    for index in range(total_steps):
        if maximum(time.monotonic() - start >= args.max_runtime_seconds):
            result["stop_reason"] = "runtime_limit_at_optimizer_step_boundary"
            break
        barrier()
        if index == args.warmup:
            torch.cuda.reset_peak_memory_stats(device)
            measurement_start = time.perf_counter()
        step_start = time.perf_counter()
        loss = train_step()
        torch.cuda.synchronize(device)
        elapsed = maximum(time.perf_counter() - step_start)
        if index < args.warmup:
            warmup_losses.append(loss)
        else:
            durations.append(elapsed)
            losses.append(loss)
        if rank == 0:
            print(json.dumps(dict(stage="warmup" if index < args.warmup else "measurement",
                                  step=index + 1, loss=loss, seconds=elapsed)), flush=True)
    barrier()
    result.update(status="completed" if len(durations) == args.steps else "runtime_limit",
                  completed_warmup_steps=len(warmup_losses), warmup_losses=warmup_losses,
                  measured_losses=losses, peak_cuda_allocated_bytes=maximum(torch.cuda.max_memory_allocated(device)),
                  peak_cuda_reserved_bytes=maximum(torch.cuda.max_memory_reserved(device)))
    if durations:
        elapsed = maximum(time.perf_counter() - measurement_start)
        result["throughput"] = summarize(durations, elapsed, world_size=world_size,
                                         batch_size=args.batch_size, sequence_length=args.sequence_length,
                                         accumulation=args.accumulation, target_tokens=args.target_tokens)
    result["runtime_seconds"] = time.monotonic() - start
    if rank == 0:
        write_json(args.output, result)
    barrier()
    if world_size > 1:
        dist.destroy_process_group()
    return 0 if result["status"] == "completed" else 2


def main():
    args = arguments()
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    start = time.monotonic()
    result = dict(status="initializing", started_utc=datetime.now(timezone.utc).isoformat(),
                  runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  arguments={key: str(value) if isinstance(value, Path) else value
                             for key, value in vars(args).items()},
                  purpose="Training compute throughput only; no data-quality or convergence claim")
    rank = int(os.environ.get("RANK", "0"))
    try:
        return benchmark(args, result, start)
    except Exception as error:
        result.update(status="failed", failure_type=type(error).__name__, failure_message=str(error),
                      traceback=traceback.format_exc(), runtime_seconds=time.monotonic() - start)
        destination = args.output if rank == 0 else args.output.with_name(args.output.stem + f".rank-{rank}.failure.json")
        write_json(destination, result)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
