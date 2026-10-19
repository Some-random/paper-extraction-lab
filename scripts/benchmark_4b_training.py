#!/usr/bin/env python3
"""Bounded, offline dense-model training-throughput benchmark (no saved weights)."""

import argparse
from contextlib import nullcontext
from datetime import datetime, timedelta, timezone
import faulthandler
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


def phase_event(result, start, stage, *, clock=time.monotonic, emit=print, **details):
    """Record host-side milestones; GPU durations require explicit synchronization."""
    event = dict(stage=stage, rank=int(os.environ.get("RANK", "0")),
                 elapsed_seconds=clock() - start, utc=datetime.now(timezone.utc).isoformat(),
                 **details)
    result.setdefault("phase_timings", []).append(event)
    emit(json.dumps(event), flush=True)
    return event


def compact_profile(events, maximum_entries=100, maximum_bytes=500_000, *, kernel_events=()):
    """Keep bounded aggregated operator times, never tensors or a full trace."""
    if not 0 < maximum_entries <= 100 or maximum_bytes < 512:
        raise ValueError("Invalid compact profiler limits")
    records, kernel_times = [], {}
    for event in kernel_events:
        for kernel in getattr(event, "kernels", ()):
            name = str(kernel.name)[:400]
            row = kernel_times.setdefault(name, dict(name=name, calls=0, device_total_us=0.))
            row["calls"] += 1
            duration = float(kernel.duration)
            if math.isfinite(duration):
                row["device_total_us"] += max(0., duration)
    kernels = sorted(kernel_times.values(), key=lambda row: row["device_total_us"], reverse=True)
    special_kernels = [row for row in kernels if any(marker in row["name"].lower()
                       for marker in ("attention", "flash", "fmha", "cudnn", "nccl", "loss", "softmax"))]
    kernel_names = {row["name"] for row in special_kernels}
    kernel_limit = min(32, maximum_entries // 2)
    kernels = (special_kernels + [row for row in kernels if row["name"] not in kernel_names])[:kernel_limit]
    for event in events:
        def duration(*names):
            for name in names:
                value = getattr(event, name, None)
                if value is not None:
                    value = float(value)
                    if math.isfinite(value):
                        return max(0., value)
            return 0.
        name = str(event.key)[:400]
        lowered = name.lower()
        record = dict(name=name, calls=int(event.count),
                      self_cpu_us=duration("self_cpu_time_total"),
                      cpu_total_us=duration("cpu_time_total"),
                      self_device_us=duration("self_device_time_total", "self_cuda_time_total"),
                      device_total_us=duration("device_time_total", "cuda_time_total"))
        record["categories"] = [category for category, markers in (
            ("attention", ("attention", "flash", "fmha", "cudnn", "sdpa")),
            ("communication", ("nccl", "all_gather", "allgather", "reduce_scatter", "all_reduce")),
            ("loss", ("cross_entropy", "nll_loss", "log_softmax", "benchmark.loss")))
            if any(marker in lowered for marker in markers)]
        records.append(record)
    records.sort(key=lambda row: max(row["self_device_us"], row["self_cpu_us"]), reverse=True)
    # Reserve entries for the actual attention, loss and communication names even
    # when unrelated elementwise operators dominate the overall ranking.
    operator_limit = maximum_entries - len(kernels)
    special = [row for row in records if row["categories"]][:operator_limit // 2]
    names = {row["name"] for row in special}
    selected = (special + [row for row in records if row["name"] not in names])[:operator_limit]
    output = dict(unit="microseconds", timing_scope="Separate post-measurement optimizer update",
                  totals_are_overlapping=True, observed_operator_count=len(records),
                  operators=selected, cuda_kernels=kernels,
                  truncated=len(selected) < len(records) or len(kernels) < len(kernel_times))
    while len(json.dumps(output, allow_nan=False).encode()) > maximum_bytes:
        if output["operators"]:
            output["operators"].pop()
        elif output["cuda_kernels"]:
            output["cuda_kernels"].pop()
        else:
            raise ValueError("Profiler header exceeds byte limit")
        output["truncated"] = True
    return output


def arguments(argv=None):
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
    parser.add_argument("--activation-checkpointing", choices=("on", "off"), default="on")
    parser.add_argument("--sharding", choices=("full_shard", "shard_grad_op"), default="full_shard")
    parser.add_argument("--profile-steps", type=int, choices=(0, 1), default=0,
                        help="Profile one separate optimizer update after throughput timing")
    args = parser.parse_args(argv)
    for name in ("sequence_length", "batch_size", "accumulation", "warmup", "steps",
                 "max_runtime_seconds", "target_tokens"):
        if getattr(args, name) <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    return args


def benchmark(args, result, start):
    # Imports deliberately stay here: report arithmetic is testable without CUDA dependencies.
    phase = lambda stage, **details: phase_event(result, start, stage, **details)
    phase("torch_import_start")
    import torch
    phase("torch_import_complete", torch_version=torch.__version__)
    import torch.distributed as dist
    from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
    from torch.distributed.fsdp import MixedPrecision, ShardingStrategy
    from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
    from functools import partial
    from transformers import Qwen3Config, Qwen3ForCausalLM
    from transformers.models.qwen3.modeling_qwen3 import Qwen3DecoderLayer
    phase("framework_imports_complete")

    rank = int(os.environ.get("RANK", "0"))
    local_rank = int(os.environ.get("LOCAL_RANK", "0"))
    world_size = int(os.environ.get("WORLD_SIZE", "1"))
    phase("cuda_initialize_start", local_rank=local_rank, world_size=world_size)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required; CPU timing is not a training throughput estimate")
    torch.cuda.set_device(local_rank)
    device = torch.device("cuda", local_rank)
    if not torch.cuda.is_bf16_supported():
        raise RuntimeError("GPU must support BF16")
    phase("cuda_initialize_complete")
    if world_size > 1:
        phase("process_group_start")
        dist.init_process_group("nccl", timeout=timedelta(seconds=120))
        phase("process_group_complete")

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
    phase("hardware_gather_start")
    if world_size > 1:
        dist.all_gather_object(all_hardware, hardware)
    else:
        all_hardware = [hardware]
    phase("hardware_gather_complete")
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
    phase("cpu_model_initialize_start")
    model = Qwen3ForCausalLM(config).float()
    phase("cpu_model_initialize_complete")
    parameters = sum(parameter.numel() for parameter in model.parameters())
    if args.activation_checkpointing == "on":
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.train()
    if world_size > 1:
        phase("fsdp_wrap_start", sharding=args.sharding)
        strategy = {"full_shard": ShardingStrategy.FULL_SHARD,
                    "shard_grad_op": ShardingStrategy.SHARD_GRAD_OP}[args.sharding]
        model = FSDP(model, device_id=device, sharding_strategy=strategy,
                     auto_wrap_policy=partial(transformer_auto_wrap_policy,
                                              transformer_layer_cls={Qwen3DecoderLayer}),
                     mixed_precision=MixedPrecision(param_dtype=torch.bfloat16,
                                                    reduce_dtype=torch.float32,
                                                    buffer_dtype=torch.bfloat16),
                     limit_all_gathers=True, use_orig_params=False)
        phase("fsdp_wrap_complete")
    else:
        phase("model_to_device_start")
        model = model.to(device)
        phase("model_to_device_complete")
    phase("optimizer_initialize_start")
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5, betas=(.9, .95),
                                 weight_decay=.1, fused=True)
    phase("optimizer_initialize_complete")
    phase("input_initialize_start")
    generator = torch.Generator().manual_seed(args.seed + rank)
    inputs_cpu = torch.randint(0, config.vocab_size,
                              (args.batch_size, args.sequence_length),
                              generator=generator, dtype=torch.long).pin_memory()
    phase("input_initialize_complete")
    result.update(actual_parameter_count=parameters, config_sha256=hashlib.sha256(config_bytes).hexdigest(),
                  attention="sdpa", initialization="random FP32; no model weights downloaded",
                  optimizer="fused AdamW; FP32 parameters, gradients and moments; BF16 compute",
                  sharding=("FSDP " + args.sharding.upper()) if world_size > 1 else "single GPU, unsharded",
                  gradient_checkpointing="nonreentrant" if args.activation_checkpointing == "on" else "disabled",
                  torch_compile=False,
                  input_kind="fixed synthetic uniform token IDs, CPU to GPU transfer each microbatch",
                  token_unit="Input token positions; causal loss predicts sequence_length - 1 positions")

    def train_step(*, first_warmup=False, profiled=False):
        optimizer.zero_grad(set_to_none=True)
        total_loss = torch.zeros((), device=device)
        for micro in range(args.accumulation):
            # FSDP no_sync retains full accumulated gradients until the last microbatch.
            sync = model.no_sync() if world_size > 1 and micro + 1 < args.accumulation else nullcontext()
            with sync:
                if first_warmup and micro == 0:
                    phase("first_forward_start")
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    inputs = inputs_cpu.to(device, non_blocking=True)
                    context = torch.profiler.record_function("benchmark.forward_and_loss") if profiled else nullcontext()
                    with context:
                        loss = model(input_ids=inputs, labels=inputs, use_cache=False).loss
                    scaled_loss = loss / args.accumulation
                    total_loss += scaled_loss.detach().float()
                if first_warmup and micro == 0:
                    phase("first_forward_complete")
                    phase("first_backward_start")
                context = torch.profiler.record_function("benchmark.backward") if profiled else nullcontext()
                with context:
                    scaled_loss.backward()
                if first_warmup and micro == 0:
                    phase("first_backward_complete")
        norm = model.clip_grad_norm_(1.) if world_size > 1 else torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)
        nonfinite = not bool(torch.isfinite(total_loss).item() and torch.isfinite(norm).item())
        if maximum(int(nonfinite)):
            raise FloatingPointError("Nonfinite loss or gradient norm; optimizer update skipped")
        if first_warmup:
            phase("first_optimizer_update_start")
        context = torch.profiler.record_function("benchmark.optimizer") if profiled else nullcontext()
        with context:
            optimizer.step()
        if first_warmup:
            phase("first_optimizer_update_complete")
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
    barrier()
    result["setup_seconds"] = maximum(time.monotonic() - start)
    phase("setup_complete", setup_seconds=result["setup_seconds"])
    warmup_start = time.perf_counter()
    measurement_start = None
    total_steps = args.warmup + args.steps
    for index in range(total_steps):
        if maximum(time.monotonic() - start >= args.max_runtime_seconds):
            result["stop_reason"] = "runtime_limit_at_optimizer_step_boundary"
            break
        barrier()
        if index == args.warmup:
            result["warmup_seconds"] = maximum(time.perf_counter() - warmup_start)
            torch.cuda.reset_peak_memory_stats(device)
            measurement_start = time.perf_counter()
        step_start = time.perf_counter()
        loss = train_step(first_warmup=index == 0)
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
        result["measurement_seconds"] = elapsed
    if "warmup_seconds" not in result:
        result["warmup_seconds"] = maximum(time.perf_counter() - warmup_start)
    phase("throughput_measurement_complete", measured_steps=len(durations))
    if args.profile_steps and result["status"] == "completed":
        # Freeze throughput and memory results above. Profiling is additional
        # diagnostic work and cannot affect their denominator or token count.
        if maximum(time.monotonic() - start >= args.max_runtime_seconds):
            result["profiler"] = dict(status="skipped", reason="runtime_budget_exhausted")
        else:
            phase("profiler_start")
            result["profiler"] = dict(status="initializing", rank=rank,
                                      timing_scope="Separate post-measurement optimizer update")
            if rank == 0:
                # Preserve already measured throughput even if the optional
                # profiler is interrupted. Successful launcher exit is still
                # required before a suite may accept the completed profile.
                write_json(args.output, result)
            profile_start = time.perf_counter()
            with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU,
                                                    torch.profiler.ProfilerActivity.CUDA],
                                        record_shapes=False, profile_memory=False,
                                        with_stack=False) as profiler:
                train_step(profiled=True)
                torch.cuda.synchronize(device)
            result["profiler"] = compact_profile(profiler.key_averages(), kernel_events=profiler.events())
            result["profiler"].update(status="completed", rank=rank,
                                      elapsed_seconds=time.perf_counter() - profile_start)
            phase("profiler_complete")
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
    faulthandler.enable()
    faulthandler.dump_traceback_later(60, repeat=True)
    try:
        return benchmark(args, result, start)
    except Exception as error:
        result.update(status="failed", failure_type=type(error).__name__, failure_message=str(error),
                      traceback=traceback.format_exc(), runtime_seconds=time.monotonic() - start)
        destination = args.output if rank == 0 else args.output.with_name(args.output.stem + f".rank-{rank}.failure.json")
        write_json(destination, result)
        traceback.print_exc()
        return 1
    finally:
        faulthandler.cancel_dump_traceback_later()


if __name__ == "__main__":
    raise SystemExit(main())
