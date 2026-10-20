#!/usr/bin/env python3
"""Controlled B200 training optimizations, with independent numerical and timing checks."""

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
from functools import partial
import importlib
import inspect
import types
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


class UnsupportedFeature(RuntimeError):
    """A requested implementation cannot execute; never fall back to another recipe."""


class NumericalMismatch(RuntimeError):
    """The short loss/gradient check failed its explicitly recorded tolerance."""


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sequence-length", type=int, default=4096)
    parser.add_argument("--global-batch-sequences", type=int, default=32)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--accumulation", type=int, default=16)
    parser.add_argument("--warmup", type=int, default=3)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--max-runtime-seconds", type=int, default=600)
    parser.add_argument("--target-tokens", type=int, default=200_000_000_000)
    parser.add_argument("--seed", type=int, default=20261018)
    parser.add_argument("--attention", choices=("sdpa_auto", "sdpa_flash", "sdpa_cudnn", "flash_attn4"),
                        default="sdpa_auto")
    parser.add_argument("--fused-kernels", "--kernels", dest="fused_kernels",
                        choices=("none", "liger_loss", "liger_full", "cce"), default="none")
    parser.add_argument("--activation-checkpointing", "--checkpointing", dest="activation_checkpointing",
                        choices=("off", "full", "selective"), default="full")
    parser.add_argument("--sharding", choices=("full_shard", "shard_grad_op", "fsdp2"),
                        default="full_shard")
    parser.add_argument("--compile", choices=("off", "on"), default="off")
    parser.add_argument("--precision", choices=("bf16", "float8_tensorwise", "float8_rowwise",
                                              "mxfp8", "nvfp4"), default="bf16")
    parser.add_argument("--float8-all-gather", choices=("off", "on"), default="off")
    parser.add_argument("--optimizer", choices=("adamw_fp32", "adamw_8bit"), default="adamw_fp32")
    parser.add_argument("--profile-steps", type=int, choices=(0, 1), default=0)
    args = parser.parse_args(argv)
    for name in ("sequence_length", "global_batch_sequences", "batch_size", "accumulation",
                 "warmup", "steps", "max_runtime_seconds", "target_tokens"):
        if getattr(args, name) <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    if args.sequence_length != 4096 or args.global_batch_sequences != 32:
        parser.error("The controlled sweep fixes context4096 and globalbatch32")
    if args.precision != "bf16" and args.sharding != "fsdp2":
        parser.error("Low-precision training requires an explicitly matched FSDP2 baseline")
    if args.float8_all_gather == "on" and args.precision != "float8_tensorwise":
        parser.error("FP8 all-gather is enabled only for the tensorwise Float8Linear recipe")
    return args


def validate_workload(args, world_size, config):
    if world_size * args.batch_size * args.accumulation != args.global_batch_sequences:
        raise ValueError("World size × microbatch × accumulation must equal 32 sequences")
    dimensions = {"model_type": "qwen3", "hidden_size": 2560, "intermediate_size": 9728,
                  "num_hidden_layers": 36, "num_attention_heads": 32,
                  "num_key_value_heads": 8, "head_dim": 128, "vocab_size": 151936,
                  "tie_word_embeddings": True}
    if any(config.get(key) != value for key, value in dimensions.items()):
        raise ValueError("The controlled sweep requires the pinned dense Qwen3-4B architecture")
    if config.get("attention_dropout", 0) or config.get("use_sliding_window", False):
        raise ValueError("This workload requires dropout-free, full causal attention")


def require_symbol(module, symbol):
    try:
        imported = importlib.import_module(module)
        value = getattr(imported, symbol)
    except (ImportError, AttributeError, OSError) as error:
        raise UnsupportedFeature(f"Required API {module}.{symbol} unavailable: {error}") from error
    if not callable(value):
        raise UnsupportedFeature(f"Required API {module}.{symbol} is not callable")
    return value


def comparison_metrics(torch, actual, expected, *, relative_tolerance, absolute_tolerance,
                       minimum_cosine=.98):
    """Use norm-relative gradient errors; elementwise ratios explode near zero."""
    actual, expected = actual.detach().float(), expected.detach().float()
    if actual.shape != expected.shape:
        raise NumericalMismatch(f"Shape mismatch: {tuple(actual.shape)} vs {tuple(expected.shape)}")
    if not bool(torch.isfinite(actual).all() and torch.isfinite(expected).all()):
        raise NumericalMismatch("Nonfinite output or gradient in numerical smoke test")
    difference = actual - expected
    reference_norm = float(torch.linalg.vector_norm(expected).item())
    error_norm = float(torch.linalg.vector_norm(difference).item())
    relative = error_norm / max(reference_norm, 1e-12)
    maximum_error = float(difference.abs().max().item())
    actual_norm = float(torch.linalg.vector_norm(actual).item())
    cosine = (float((actual.flatten() @ expected.flatten()).item()) /
              max(actual_norm * reference_norm, 1e-30)) if reference_norm else 1.
    passed = ((relative <= relative_tolerance or maximum_error <= absolute_tolerance)
              and (cosine >= minimum_cosine or maximum_error <= absolute_tolerance))
    report = dict(relative_l2_error=relative, maximum_absolute_error=maximum_error,
                  cosine_similarity=cosine, relative_tolerance=relative_tolerance,
                  absolute_tolerance=absolute_tolerance, minimum_cosine=minimum_cosine,
                  status="passed" if passed else "failed")
    if not passed:
        raise NumericalMismatch(json.dumps(report))
    return report


def attention_context(torch, selection):
    if selection in ("sdpa_auto", "flash_attn4"):
        return nullcontext()
    from torch.nn.attention import SDPBackend, sdpa_kernel
    chosen = {"sdpa_flash": SDPBackend.FLASH_ATTENTION,
              "sdpa_cudnn": SDPBackend.CUDNN_ATTENTION}[selection]
    # A singleton prevents PyTorch silently falling back to a different backend.
    return sdpa_kernel(backends=[chosen])


def flash4_function():
    return require_symbol("flash_attn.cute", "flash_attn_func")


def install_flash4():
    from transformers.modeling_utils import ALL_ATTENTION_FUNCTIONS
    from transformers.masking_utils import AttentionMaskInterface, flash_attention_mask
    flash_function = flash4_function()

    def forward(module, query, key, value, attention_mask, dropout=0., scaling=None, **kwargs):
        if attention_mask is not None or dropout or kwargs.get("sliding_window"):
            raise UnsupportedFeature("FA4 adapter supports this fixed unpadded causal workload only")
        output = flash_function(query.transpose(1, 2), key.transpose(1, 2), value.transpose(1, 2),
                                causal=True, softmax_scale=scaling)
        if isinstance(output, tuple):
            output = output[0]
        return output, None

    ALL_ATTENTION_FUNCTIONS.register("b200_flash_attn4", forward)
    AttentionMaskInterface.register("b200_flash_attn4", flash_attention_mask)
    return "b200_flash_attn4"


def install_cudnn_attention(torch):
    """Expand GQA explicitly: PyTorch2.8's enable_gqa dispatch excludes cuDNN."""
    from transformers.modeling_utils import ALL_ATTENTION_FUNCTIONS
    from transformers.masking_utils import AttentionMaskInterface, flash_attention_mask

    def forward(module, query, key, value, attention_mask, dropout=0., scaling=None, **kwargs):
        if attention_mask is not None or dropout or kwargs.get("sliding_window"):
            raise UnsupportedFeature("cuDNN adapter supports the fixed unpadded causal workload only")
        groups = query.shape[1] // key.shape[1]
        key, value = key.repeat_interleave(groups, 1), value.repeat_interleave(groups, 1)
        with attention_context(torch, "sdpa_cudnn"):
            output = torch.nn.functional.scaled_dot_product_attention(
                query, key, value, dropout_p=0., scale=scaling, is_causal=True, enable_gqa=False)
        return output.transpose(1, 2).contiguous(), None

    ALL_ATTENTION_FUNCTIONS.register("b200_sdpa_cudnn", forward)
    AttentionMaskInterface.register("b200_sdpa_cudnn", flash_attention_mask)
    return "b200_sdpa_cudnn"


def numerical_attention_smoke(torch, selection, device):
    from torch.nn.attention import SDPBackend, sdpa_kernel
    # Qwen3 uses 4:1 GQA and head dimension128; preserve both in the smoke case.
    generator = torch.Generator(device=device).manual_seed(20261019)
    tensors = [torch.randn((1, heads, 64, 128), generator=generator, device=device,
                           dtype=torch.bfloat16) for heads in (8, 2, 2)]
    actual_inputs = [tensor.detach().clone().requires_grad_() for tensor in tensors]
    reference_inputs = [tensor.detach().float().requires_grad_() for tensor in tensors]

    def sdpa(inputs):
        query, key, value = inputs
        key, value = key.repeat_interleave(4, 1), value.repeat_interleave(4, 1)
        return torch.nn.functional.scaled_dot_product_attention(query, key, value, is_causal=True)

    with sdpa_kernel(backends=[SDPBackend.MATH]):
        expected = sdpa(reference_inputs)
    if selection == "flash_attn4":
        actual = flash4_function()(*(value.transpose(1, 2) for value in actual_inputs), causal=True)
        if isinstance(actual, tuple):
            actual = actual[0]
        actual = actual.transpose(1, 2)
    else:
        with attention_context(torch, selection):
            actual = sdpa(actual_inputs)
    upstream = torch.randn(actual.shape, generator=generator, device=device, dtype=torch.float32)
    actual_gradients = torch.autograd.grad(actual, actual_inputs, upstream.to(actual.dtype))
    expected_gradients = torch.autograd.grad(expected, reference_inputs, upstream)
    checks = dict(output=comparison_metrics(torch, actual, expected,
                                           relative_tolerance=.03, absolute_tolerance=.01))
    checks["gradients"] = [comparison_metrics(torch, actual_grad, expected_grad,
                                             relative_tolerance=.04, absolute_tolerance=.02)
                            for actual_grad, expected_grad in zip(actual_gradients, expected_gradients)]
    checks.update(status="passed", shape="B1 QH8 KVH2 S64 D128; causal; BF16 vs FP32 math")
    return checks


def make_loss(selection):
    if selection in ("liger_loss", "liger_full"):
        loss_class = require_symbol("liger_kernel.transformers", "LigerFusedLinearCrossEntropyLoss")
        criterion = loss_class()
        return lambda hidden, weight, labels: criterion(weight, hidden, labels)
    if selection == "cce":
        function = require_symbol("cut_cross_entropy", "linear_cross_entropy")
        # Disable approximate gradient filtering for the controlled comparison.
        return lambda hidden, weight, labels: function(hidden, weight, labels,
                                                       reduction="mean", filter_eps=None)
    return None


def numerical_loss_smoke(torch, function, device):
    generator = torch.Generator(device=device).manual_seed(20261020)
    hidden = torch.randn((64, 256), generator=generator, device=device, dtype=torch.bfloat16)
    weight = torch.randn((512, 256), generator=generator, device=device, dtype=torch.bfloat16) * .02
    labels = torch.randint(0, 512, (64,), generator=generator, device=device)
    actual_inputs = [value.detach().clone().requires_grad_() for value in (hidden, weight)]
    reference_inputs = [value.detach().float().requires_grad_() for value in (hidden, weight)]
    actual = function(*actual_inputs, labels)
    expected = torch.nn.functional.cross_entropy(reference_inputs[0] @ reference_inputs[1].T, labels)
    actual_gradients = torch.autograd.grad(actual, actual_inputs)
    expected_gradients = torch.autograd.grad(expected, reference_inputs)
    return dict(status="passed", loss=comparison_metrics(torch, actual, expected,
                                                        relative_tolerance=.01, absolute_tolerance=.015),
                gradients=[comparison_metrics(torch, actual_grad, expected_grad,
                                               relative_tolerance=.04, absolute_tolerance=.005)
                           for actual_grad, expected_grad in zip(actual_gradients, expected_gradients)],
                label_alignment="Full model explicitly shifts hidden[:-1] against labels[1:]")


def numerical_liger_blocks_smoke(torch, device):
    """Check the actual patched small Qwen3 model, including RoPE/RMSNorm/SwiGLU."""
    import copy
    from transformers import Qwen3Config, Qwen3ForCausalLM
    config = Qwen3Config(vocab_size=512, hidden_size=256, intermediate_size=512,
                         num_hidden_layers=1, num_attention_heads=4, num_key_value_heads=2,
                         head_dim=64, tie_word_embeddings=True, use_cache=False,
                         attention_dropout=0.)
    config._attn_implementation = "sdpa"
    reference = Qwen3ForCausalLM(config).to(device=device, dtype=torch.float32)
    patched = copy.deepcopy(reference)
    labels = torch.randint(0, 512, (2, 32), device=device)
    with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
        expected = reference(input_ids=labels, labels=labels).loss
    expected_grad = torch.autograd.grad(expected, reference.model.embed_tokens.weight)[0]
    # The official patch also changes module-level RoPE functions, so evaluate
    # the unpatched reference before applying it, rather than patching both.
    apply_liger_full(patched)
    with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
        actual = patched(input_ids=labels, labels=labels).loss
    actual_grad = torch.autograd.grad(actual, patched.model.embed_tokens.weight)[0]
    return dict(status="passed", loss=comparison_metrics(torch, actual, expected,
                                                         relative_tolerance=.015, absolute_tolerance=.015),
                embedding_gradient=comparison_metrics(torch, actual_grad, expected_grad,
                                                       relative_tolerance=.05, absolute_tolerance=.003),
                scope="One-layer Qwen3: patched RoPE/RMSNorm/SwiGLU vs original; BF16 compute")


def install_loss(model, function):
    from transformers.modeling_outputs import CausalLMOutputWithPast

    def forward(self, input_ids=None, labels=None, use_cache=False, **kwargs):
        if labels is None or use_cache:
            raise ValueError("The fused-loss benchmark requires causal labels and no KV cache")
        output = self.model(input_ids=input_ids, use_cache=False, **kwargs)
        hidden = output.last_hidden_state[..., :-1, :].contiguous().view(-1, self.config.hidden_size)
        targets = labels[..., 1:].contiguous().view(-1)
        loss = function(hidden, self.lm_head.weight, targets)
        return CausalLMOutputWithPast(loss=loss)

    model.forward = types.MethodType(forward, model)


def apply_liger_full(model):
    patch = require_symbol("liger_kernel.transformers", "apply_liger_kernel_to_qwen3")
    signature = inspect.signature(patch)
    if "model" not in signature.parameters:
        raise UnsupportedFeature("Pinned Liger Qwen3 patch does not support patching a model instance")
    patch(model=model, rope=True, rms_norm=True, swiglu=True, cross_entropy=False,
          fused_linear_cross_entropy=False)


def configure_checkpointing(model, selection, torch):
    if selection == "off":
        return dict(kind="disabled")
    kwargs = dict(use_reentrant=False)
    detail = dict(kind="full nonreentrant decoder-layer recomputation")
    if selection == "selective":
        from torch.utils.checkpoint import CheckpointPolicy, create_selective_checkpoint_contexts
        names = ("aten.mm.default", "aten.addmm.default", "aten.bmm.default",
                 "aten._scaled_dot_product_efficient_attention.default",
                 "aten._scaled_dot_product_flash_attention.default",
                 "aten._scaled_dot_product_cudnn_attention.default")
        save_operations = set()
        for name in names:
            try:
                namespace, operator, overload = name.split(".")
                save_operations.add(getattr(getattr(getattr(torch.ops, namespace), operator), overload))
            except AttributeError:
                continue

        def policy(ctx, operation, *args, **kwargs):
            return (CheckpointPolicy.MUST_SAVE if operation in save_operations
                    else CheckpointPolicy.PREFER_RECOMPUTE)

        kwargs["context_fn"] = partial(create_selective_checkpoint_contexts, policy)
        detail = dict(kind="selective nonreentrant decoder-layer recomputation",
                      saved_expensive_operations=list(names),
                      other_operations="prefer recomputation")
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs=kwargs)
    return detail


def low_precision_converter(torch, args, result):
    if args.precision == "bf16":
        return None, None
    if args.precision == "nvfp4":
        raise UnsupportedFeature("Native NVFP4 forward/backward training is not integrated in this "
                                 "pinned Qwen3/PyTorch stack; no emulated or BF16 fallback")
    if args.precision.startswith("float8_"):
        config_class = require_symbol("torchao.float8", "Float8LinearConfig")
        convert = require_symbol("torchao.float8", "convert_to_float8_training")
        recipe = args.precision.removeprefix("float8_")
        config = config_class.from_recipe_name(recipe)
        if getattr(config, "emulate", False):
            raise UnsupportedFeature("Native FP8 training is required; Float8Linear emulation is forbidden")
        if args.float8_all_gather == "on":
            import dataclasses
            if not dataclasses.is_dataclass(config) or not hasattr(config, "enable_fsdp_float8_all_gather"):
                raise UnsupportedFeature("This Float8LinearConfig cannot enable FSDP FP8 all-gather")
            config = dataclasses.replace(config, enable_fsdp_float8_all_gather=True)

        def eligible(module, name):
            return (isinstance(module, torch.nn.Linear) and name != "lm_head"
                    and all(dimension % 16 == 0 for dimension in module.weight.shape))

        def converter(module):
            return convert(module, config=config, module_filter_fn=eligible)

        precompute = None
        if args.float8_all_gather == "on":
            precompute = require_symbol("torchao.float8", "precompute_float8_dynamic_scale_for_fsdp")
        result["precision_recipe"] = dict(implementation="torchao Float8Linear",
                                          recipe=recipe, output_head="BF16", master_parameters="FP32",
                                          float8_all_gather=args.float8_all_gather)
        return converter, precompute
    if args.precision == "mxfp8":
        config_class = require_symbol("torchao.prototype.mx_formats", "MXLinearConfig")
        quantize = require_symbol("torchao.quantization", "quantize_")
        try:
            from torchao.prototype.mx_formats import MXGemmKernelChoice
            from torchao.prototype.mx_formats.config import MXFP8Dim1CastKernelChoice, ScaleCalculationMode
            config = config_class(gemm_kernel_choice=MXGemmKernelChoice.CUBLAS,
                                  mxfp8_cast_kernel_choice=MXFP8Dim1CastKernelChoice.TRITON,
                                  scale_calculation_mode=ScaleCalculationMode.FLOOR)
        except (ImportError, AttributeError, TypeError) as error:
            raise UnsupportedFeature(f"Pinned TorchAO native MXFP8 CUBLAS API unavailable: {error}") from error

        def eligible(module, name):
            return (isinstance(module, torch.nn.Linear) and name != "lm_head"
                    and all(dimension % 32 == 0 for dimension in module.weight.shape))

        def converter(module):
            quantize(module, config, filter_fn=eligible)
            return module

        result["precision_recipe"] = dict(implementation="torchao MXLinear", format="mxfp8",
                                          gemm_kernel="native CUBLAS block-scaled _scaled_mm",
                                          casts="Triton", scale_calculation="FLOOR",
                                          output_head="BF16", master_parameters="FP32",
                                          emulation=False)
        return converter, None
    raise UnsupportedFeature(f"Unknown precision recipe {args.precision}")


def numerical_precision_smoke(torch, converter, device):
    model = torch.nn.Sequential(torch.nn.Linear(256, 256, bias=False)).to(device=device, dtype=torch.float32)
    reference = torch.nn.Linear(256, 256, bias=False).to(device=device, dtype=torch.float32)
    reference.load_state_dict(model[0].state_dict())
    converter(model)
    # Compile is required for some TorchAO recipes and stays outside model timing.
    model.compile(fullgraph=False)
    actual_input = torch.randn(128, 256, device=device, dtype=torch.bfloat16, requires_grad=True)
    reference_input = actual_input.detach().clone().requires_grad_()
    with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
        actual, expected = model(actual_input), reference(reference_input)
    upstream = torch.randn_like(actual)
    actual_gradients = torch.autograd.grad(actual, (actual_input, next(model.parameters())), upstream)
    expected_gradients = torch.autograd.grad(expected, (reference_input, reference.weight), upstream)
    return dict(status="passed", convergence_claim=False,
                output=comparison_metrics(torch, actual, expected,
                                          relative_tolerance=.15, absolute_tolerance=.02, minimum_cosine=.98),
                gradients=[comparison_metrics(torch, actual_grad, expected_grad,
                                               relative_tolerance=.20, absolute_tolerance=.05,
                                               minimum_cosine=.97)
                           for actual_grad, expected_grad in zip(actual_gradients, expected_gradients)],
                scope="Single 256×256 linear forward/backward vs BF16; not long-run stability")


def local_tensor(tensor):
    return tensor.to_local() if hasattr(tensor, "to_local") else tensor


def make_optimizer(torch, parameters, selection):
    parameters = list(parameters)
    if any(parameter.dtype != torch.float32 for parameter in parameters):
        raise RuntimeError("All controlled recipes must preserve FP32 master parameters")
    kwargs = dict(lr=1e-5, betas=(.9, .95), eps=1e-8, weight_decay=.1)
    if selection == "adamw_fp32":
        return torch.optim.AdamW(parameters, **kwargs, fused=True)
    optimizer_class = require_symbol("torchao.optim", "AdamW8bit")
    return optimizer_class(parameters, **kwargs, block_size=256, bf16_stochastic_round=False)


def optimizer_encoding(optimizer):
    encoding = {}
    for state in optimizer.state.values():
        for name in ("exp_avg", "exp_avg_sq"):
            if name not in state:
                continue
            value = local_tensor(state[name])
            row = dict(implementation=type(value).__module__ + "." + type(value).__name__,
                       logical_dtype=str(value.dtype))
            if hasattr(value, "codes"):
                row.update(codes_dtype=str(value.codes.dtype), scale_dtype=str(value.scale.dtype))
            encoding[json.dumps(row, sort_keys=True)] = row
    return list(encoding.values())


def numerical_optimizer_smoke(torch, device):
    # >4096 values and divisible by256 force real 8-bit state, rather than the
    # optimizer's small-tensor FP32 bypass. Do not compare only final weights:
    # initial weights dwarf these small AdamW updates, masking wrong updates.
    initial = torch.randn(256, 256, device=device, dtype=torch.float32) * .02
    actual = torch.nn.Parameter(initial.clone())
    expected = torch.nn.Parameter(initial.clone())
    actual_optimizer = make_optimizer(torch, [actual], "adamw_8bit")
    expected_optimizer = make_optimizer(torch, [expected], "adamw_fp32")
    losses = []
    for _ in range(5):
        inputs = torch.randn(32, 256, device=device)
        targets = torch.randn(32, 256, device=device)
        for parameter, optimizer in ((expected, expected_optimizer), (actual, actual_optimizer)):
            optimizer.zero_grad(set_to_none=True)
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                loss = (inputs @ parameter.T - targets).square().mean()
            loss.backward()
            optimizer.step()
            if not bool(torch.isfinite(loss) and torch.isfinite(parameter).all()):
                raise NumericalMismatch("8-bit optimizer smoke produced nonfinite loss or weights")
            losses.append(float(loss.item()))
    encoding = optimizer_encoding(actual_optimizer)
    if not any(row.get("codes_dtype") == "torch.uint8" for row in encoding):
        raise UnsupportedFeature("AdamW8bit requested but smoke did not allocate real uint8 optimizer states")
    return dict(status="passed", optimizer_steps=5, losses=losses, state_encoding=encoding,
                update_vector=comparison_metrics(torch, actual - initial, expected - initial,
                                                  relative_tolerance=.20, absolute_tolerance=5e-6,
                                                  minimum_cosine=.95),
                scope="Short AdamW update-vector agreement vs FP32; no long-run quality claim")


def optimizer_sample(model):
    for name, parameter in model.named_parameters():
        value = local_tensor(parameter)
        if value.requires_grad and value.numel() >= 1024:
            return name, parameter, value.detach().flatten()[:1024].clone()
    raise RuntimeError("No trainable local parameter shard available for update check")


def assert_attention_evidence(profile, selection):
    names = [row["name"].lower() for row in profile.get("operators", [])]
    names += [row["name"].lower() for row in profile.get("cuda_kernels", [])]
    required = {"sdpa_flash": ("flash_attention", "flash_fwd", "flash_bwd"),
                "sdpa_cudnn": ("cudnn_attention", "cudnn", "cudnn_generated"),
                "flash_attn4": ("flash_attn", "flash_fwd", "flash_bwd", "flashattention")}
    if selection in required and not any(marker in name for name in names for marker in required[selection]):
        raise UnsupportedFeature(f"Requested {selection}, but profiler has no matching executed kernel/operator")
    return dict(status="observed" if names else "not_profiled", requested=selection,
                actual_attention_names=[name for name in names if any(marker in name
                                        for marker in ("attention", "flash", "fmha", "cudnn"))][:20])




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
    for package in ("torchao", "liger-kernel", "cut-cross-entropy", "flash-attn-4", "triton"):
        try:
            result["packages"][package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            result["packages"][package] = "not installed"
    config_bytes = args.model_config.read_bytes()
    config_data = json.loads(config_bytes)
    if config_data.get("model_type") != "qwen3":
        raise ValueError("Expected a pinned Qwen3 dense-model configuration")
    validate_workload(args, world_size, config_data)
    if any("B200" not in item["gpu"] or item["compute_capability"][0] != 10 for item in all_hardware):
        raise UnsupportedFeature("This sweep requires real NVIDIA B200 GPUs (sm100)")
    config = Qwen3Config.from_dict(config_data)
    config.use_cache = False
    config._attn_implementation = "sdpa"
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.set_float32_matmul_precision("high")
    phase("numerical_smoke_start")
    smoke_start = time.perf_counter()
    result["smoke_checks"] = dict(status="initializing")
    result["smoke_checks"]["attention"] = numerical_attention_smoke(torch, args.attention, device)
    loss_function = make_loss(args.fused_kernels)
    if loss_function is not None:
        result["smoke_checks"]["loss"] = numerical_loss_smoke(torch, loss_function, device)
    if args.fused_kernels == "liger_full":
        result["smoke_checks"]["liger_blocks"] = numerical_liger_blocks_smoke(torch, device)
    converter, float8_precompute = low_precision_converter(torch, args, result)
    if converter is not None:
        result["smoke_checks"]["precision"] = numerical_precision_smoke(torch, converter, device)
    if args.optimizer == "adamw_8bit":
        result["smoke_checks"]["optimizer"] = numerical_optimizer_smoke(torch, device)
    torch.cuda.synchronize(device)
    result["smoke_checks"].update(status="passed", seconds=time.perf_counter() - smoke_start,
                                  scope="Small functional output/gradient checks; no quality claim")
    phase("numerical_smoke_complete")
    # FP32 originals ensure FP32 master weights and Adam moments throughout.
    # Some independent smoke modules consume the global RNG. Restore it so
    # every controlled recipe starts with the same full-model initialization.
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    phase("cpu_model_initialize_start")
    model = Qwen3ForCausalLM(config).float()
    phase("cpu_model_initialize_complete")
    parameters = sum(parameter.numel() for parameter in model.parameters())
    if args.attention == "flash_attn4":
        model.config._attn_implementation = install_flash4()
    elif args.attention == "sdpa_cudnn":
        model.config._attn_implementation = install_cudnn_attention(torch)
    if args.fused_kernels == "liger_full":
        apply_liger_full(model)
    if loss_function is not None:
        install_loss(model, loss_function)
    result["checkpointing_recipe"] = configure_checkpointing(model, args.activation_checkpointing, torch)
    if converter is not None:
        converter(model)
        low_modules = [dict(name=name, implementation=type(module).__module__ + "." + type(module).__name__)
                       for name, module in model.named_modules()
                       if "torchao" in type(module).__module__ and "Linear" in type(module).__name__]
        if not low_modules:
            raise UnsupportedFeature("Requested low precision but no TorchAO linear modules were converted")
        result["converted_linears"] = dict(count=len(low_modules), examples=low_modules[:6])
    decoder_layers = list(model.model.layers)
    model.train()
    phase("fsdp_wrap_start", sharding=args.sharding)
    if args.sharding == "fsdp2":
        from torch.distributed.device_mesh import init_device_mesh
        from torch.distributed.fsdp import fully_shard, MixedPrecisionPolicy
        if world_size < 2:
            raise UnsupportedFeature("This controlled FSDP2 sweep requires distributed B200s")
        mesh = init_device_mesh("cuda", (world_size,))
        policy = MixedPrecisionPolicy(param_dtype=torch.bfloat16, reduce_dtype=torch.float32)
        model = model.to(device)
        for layer in decoder_layers:
            fully_shard(layer, mesh=mesh, mp_policy=policy, reshard_after_forward=True)
        fully_shard(model, mesh=mesh, mp_policy=policy, reshard_after_forward=False)
    elif world_size > 1:
        strategy = {"full_shard": ShardingStrategy.FULL_SHARD,
                    "shard_grad_op": ShardingStrategy.SHARD_GRAD_OP}[args.sharding]
        model = FSDP(model, device_id=device, sharding_strategy=strategy,
                     auto_wrap_policy=partial(transformer_auto_wrap_policy,
                                              transformer_layer_cls={Qwen3DecoderLayer}),
                     mixed_precision=MixedPrecision(param_dtype=torch.bfloat16,
                                                    reduce_dtype=torch.float32,
                                                    buffer_dtype=torch.bfloat16),
                     limit_all_gathers=True, use_orig_params=args.compile == "on")
    else:
        model = model.to(device)
    phase("fsdp_wrap_complete")
    result["compile_seconds"] = 0.
    if args.compile == "on":
        phase("compile_registration_start")
        registration_start = time.perf_counter()
        import torch._dynamo
        torch._dynamo.config.cache_size_limit = 64
        compiler_graphs_before = int(torch._dynamo.utils.counters["stats"]["unique_graphs"])
        for layer in decoder_layers:
            layer.compile(fullgraph=False, dynamic=False)
        result["compile_registration_seconds"] = time.perf_counter() - registration_start
        result["compile_timing_scope"] = ("Lazy compilation occurs during the first warmup update; "
                                           "compile_seconds records the entire first warmup update, "
                                           "not compiler-only time")
        phase("compile_registration_complete")
    phase("optimizer_initialize_start")
    optimizer = make_optimizer(torch, model.parameters(), args.optimizer)
    phase("optimizer_initialize_complete")
    phase("input_initialize_start")
    generator = torch.Generator().manual_seed(args.seed + rank)
    inputs_cpu = torch.randint(0, config.vocab_size,
                              (args.batch_size, args.sequence_length),
                              generator=generator, dtype=torch.long).pin_memory()
    phase("input_initialize_complete")
    result.update(actual_parameter_count=parameters, config_sha256=hashlib.sha256(config_bytes).hexdigest(),
                  attention=args.attention, initialization="random FP32; no model weights downloaded",
                  optimizer=("fused AdamW; FP32 master parameters/gradients/moments" if args.optimizer == "adamw_fp32"
                             else "TorchAO AdamW8bit; FP32 masters/gradients; blockwise uint8 moment codes"),
                  sharding=("FSDP " + args.sharding.upper()) if world_size > 1 else "single GPU, unsharded",
                  gradient_checkpointing=args.activation_checkpointing,
                  torch_compile=args.compile == "on", precision=args.precision, fused_kernels=args.fused_kernels,
                  input_kind="fixed synthetic uniform token IDs, CPU to GPU transfer each microbatch",
                  token_unit="Input token positions; causal loss predicts sequence_length - 1 positions")

    def train_step(*, first_warmup=False, profiled=False):
        optimizer.zero_grad(set_to_none=True)
        total_loss = torch.zeros((), device=device)
        for micro in range(args.accumulation):
            # FSDP no_sync retains full accumulated gradients until the last microbatch.
            if args.sharding == "fsdp2":
                model.set_requires_gradient_sync(micro + 1 == args.accumulation)
                model.set_is_last_backward(micro + 1 == args.accumulation)
                sync = nullcontext()
            else:
                sync = model.no_sync() if world_size > 1 and micro + 1 < args.accumulation else nullcontext()
            with sync, attention_context(torch, args.attention):
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
        if first_warmup:
            result["gradient_dtypes"] = sorted({str(parameter.grad.dtype) for parameter in model.parameters()
                                                 if parameter.grad is not None})
            if result["gradient_dtypes"] != ["torch.float32"]:
                raise RuntimeError(f"Expected FP32 accumulated gradients, got {result['gradient_dtypes']}")
        if world_size > 1 and args.sharding != "fsdp2":
            norm = model.clip_grad_norm_(1.)
        else:
            norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)
            if hasattr(norm, "full_tensor"):
                norm = norm.full_tensor()
        nonfinite = not bool(torch.isfinite(total_loss).item() and torch.isfinite(norm).item())
        if maximum(int(nonfinite)):
            raise FloatingPointError("Nonfinite loss or gradient norm; optimizer update skipped")
        if first_warmup:
            phase("first_optimizer_update_start")
        sample = optimizer_sample(model) if first_warmup else None
        context = torch.profiler.record_function("benchmark.optimizer") if profiled else nullcontext()
        with context:
            optimizer.step()
        if float8_precompute is not None:
            float8_precompute(model)
        if sample is not None:
            sample_name, parameter, before = sample
            after = local_tensor(parameter).detach().flatten()[:before.numel()]
            finite = bool(torch.isfinite(after).all())
            maximum_delta = float((after - before).abs().max().item())
            changed_any_rank = maximum(int(maximum_delta > 0))
            if maximum(int(not finite)) or not changed_any_rank:
                raise FloatingPointError("First optimizer update did not change finite FP32 master weights")
            result["optimizer_update_check"] = dict(status="passed", sampled_parameter=sample_name,
                                                     sampled_elements=before.numel(),
                                                     maximum_local_absolute_change=maximum_delta,
                                                     any_rank_changed=bool(changed_any_rank),
                                                     dtype=str(after.dtype))
        if first_warmup:
            phase("first_optimizer_update_complete")
        if not result.get("optimizer_state_dtypes"):
            moment_dtypes = sorted({str(state[key].dtype) for state in optimizer.state.values()
                                    for key in ("exp_avg", "exp_avg_sq") if key in state})
            encoding = optimizer_encoding(optimizer)
            if args.optimizer == "adamw_fp32" and moment_dtypes != ["torch.float32"]:
                raise RuntimeError(f"Expected FP32 Adam moments, got {moment_dtypes}")
            if args.optimizer == "adamw_8bit" and not any(row.get("codes_dtype") == "torch.uint8"
                                                         for row in encoding):
                raise UnsupportedFeature("AdamW8bit did not create any uint8 encoded moment state")
            result["optimizer_state_dtypes"] = moment_dtypes
            result["optimizer_state_encoding"] = encoding
            result["master_parameter_dtypes"] = sorted({str(parameter.dtype) for parameter in model.parameters()})
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
            if index == 0:
                result["first_warmup_seconds"] = elapsed
                if args.compile == "on" or args.optimizer == "adamw_8bit":
                    result["compile_seconds"] = elapsed
                if args.optimizer == "adamw_8bit":
                    result["optimizer_compile_timing_scope"] = ("Native TorchAO AdamW8bit compiles its update; "
                                                               "first warmup includes optimizer compilation")
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
    if losses:
        result["loss_summary"] = dict(first=losses[0], last=losses[-1], mean=statistics.mean(losses),
                                      finite=all(math.isfinite(value) for value in losses),
                                      meaning="Synthetic uniform-token loss; no biological-quality claim")
    if args.compile == "on":
        captured_graphs = int(torch._dynamo.utils.counters["stats"]["unique_graphs"]) - compiler_graphs_before
        result["compilation_evidence"] = dict(unique_graphs=captured_graphs,
                                               decoder_blocks_requested=len(decoder_layers),
                                               cache_size_limit=64,
                                               status="compiled" if captured_graphs else "not_observed")
        if result["status"] == "completed" and not captured_graphs:
            raise UnsupportedFeature("Compilation requested but no full-model decoder graph was captured")
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
            result["attention_evidence"] = assert_attention_evidence(result["profiler"], args.attention)
            phase("profiler_complete")
    if "attention_evidence" not in result:
        result["attention_evidence"] = dict(status="not_profiled", requested=args.attention,
                                             dispatch="singleton forced backend" if args.attention in
                                             ("sdpa_flash", "sdpa_cudnn") else "explicit FA4 function" if
                                             args.attention == "flash_attn4" else "PyTorch automatic selection")
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
        if args.precision == "nvfp4":
            raise UnsupportedFeature("Native NVFP4 training requires a compatible Transformer Engine "
                                     "training extension; the pinned binary-only overlay cannot provide it. "
                                     "No GPU initialization, emulation or BF16 fallback was attempted")
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
