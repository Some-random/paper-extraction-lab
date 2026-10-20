#!/usr/bin/env python3
"""CPU-only audit of the isolated B200 optimization overlay.

The original throughput environment is read through a .pth file and is never
modified. Installation is a separate explicit pip operation; this command only
records the resolved packages, their source paths, and import/API compatibility.
No CUDA availability probe or GPU allocation is performed.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import inspect
import json
import os
from pathlib import Path
import shutil
import time


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "experiments/b200_optimization_2026-10-19"
NEW_ENV = ROOT / ".b200-opt-venv"
BASE_ENV = ROOT / ".throughput-venv"
ENVIRONMENT_CAP = 16 * 2**30
FREE_FLOOR = 64 * 2**30


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_api(module_name: str, symbols: tuple[str, ...]) -> dict:
    try:
        module = importlib.import_module(module_name)
        result = {
            "status": "imported",
            "module_file": getattr(module, "__file__", None),
            "symbols": {},
        }
        for name in symbols:
            value = getattr(module, name)
            try:
                signature = str(inspect.signature(value))
            except (TypeError, ValueError):
                signature = None
            result["symbols"][name] = {"signature": signature}
        return result
    except Exception as error:
        return {
            "status": "failed",
            "error_type": type(error).__name__,
            "message": str(error)[:2000],
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=RUN / "environment_preflight.json")
    args = parser.parse_args()
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    packages = {}
    for name in (
        "torch", "triton", "transformers", "flash-attn-4", "liger-kernel",
        "cut-cross-entropy", "torchao", "nvidia-cutlass-dsl", "apache-tvm-ffi",
        "torch-c-dlpack-ext", "quack-kernels", "cuda-bindings",
    ):
        try:
            dist = importlib.metadata.distribution(name)
            metadata_file = Path(dist._path) / "METADATA"
            packages[name] = {
                "version": dist.version,
                "metadata_path": str(metadata_file),
                "metadata_sha256": digest(metadata_file),
                "requires": dist.requires,
            }
        except importlib.metadata.PackageNotFoundError:
            packages[name] = {"status": "not_installed"}
    apis = {
        "torch": check_api("torch", ("compile",)),
        "fsdp2": check_api("torch.distributed.fsdp", ("fully_shard", "MixedPrecisionPolicy")),
        "sdpa_backends": check_api("torch.nn.attention", ("sdpa_kernel", "SDPBackend")),
        "qwen3": check_api("transformers.models.qwen3.modeling_qwen3", ("Qwen3ForCausalLM",)),
        "liger_qwen3": check_api("liger_kernel.transformers", ("apply_liger_kernel_to_qwen3",)),
        "liger_loss": check_api("liger_kernel.transformers", ("LigerFusedLinearCrossEntropyLoss",)),
        "cce": check_api("cut_cross_entropy", ("linear_cross_entropy",)),
        "float8": check_api("torchao.float8", ("convert_to_float8_training", "Float8LinearConfig")),
        "mxfp8": check_api("torchao.prototype.mx_formats", ("MXLinearConfig", "MXGemmKernelChoice")),
        "quantize": check_api("torchao.quantization", ("quantize_",)),
        "fa4": check_api("flash_attn.cute", ("flash_attn_func",)),
    }
    # Import and constructor checks establish API compatibility, not GPU support.
    recipe_checks = {}
    if apis["float8"]["status"] == "imported":
        import torch
        from torchao.float8 import Float8LinearConfig, convert_to_float8_training
        for recipe in ("tensorwise", "rowwise"):
            try:
                config = Float8LinearConfig.from_recipe_name(recipe)
                converted = convert_to_float8_training(torch.nn.Sequential(torch.nn.Linear(32, 32, dtype=torch.float32)), config=config)[0]
                recipe_checks[recipe] = {
                    "status": "constructed",
                    "config": str(config),
                    "cpu_module_conversion": type(converted).__name__,
                    "master_weight_dtype": str(converted.weight.dtype),
                    "kernel_executed": False,
                }
            except Exception as error:
                recipe_checks[recipe] = {"status": "failed", "message": str(error)}
    if apis["mxfp8"]["status"] == "imported":
        try:
            from torchao.prototype.mx_formats import MXGemmKernelChoice, MXLinearConfig
            from torchao.prototype.mx_formats.config import MXFP8Dim1CastKernelChoice
            from torchao.quantization import quantize_
            config = MXLinearConfig(gemm_kernel_choice=MXGemmKernelChoice.CUBLAS, mxfp8_cast_kernel_choice=MXFP8Dim1CastKernelChoice.TRITON)
            converted_model = torch.nn.Sequential(torch.nn.Linear(32, 32, dtype=torch.float32))
            quantize_(converted_model, config)
            converted = converted_model[0]
            recipe_checks["mxfp8_cublas_triton_cast"] = {
                "status": "constructed", "config": str(config), "emulated": False,
                "cpu_module_conversion": type(converted).__name__,
                "master_weight_dtype": str(converted.weight.dtype),
                "kernel_executed": False,
            }
        except Exception as error:
            recipe_checks["mxfp8_cublas_triton_cast"] = {"status": "failed", "message": str(error)}
    import torch
    fingerprint_path = RUN / "baseline_runtime_fingerprint.json"
    fingerprint = json.loads(fingerprint_path.read_text())
    baseline_checks = {
        path: digest(Path(path)) == value["sha256"]
        and Path(path).stat().st_mtime_ns == value["mtime_ns"]
        for path, value in fingerprint["files"].items()
    }
    owned_bytes = sum(p.stat().st_size for p in NEW_ENV.rglob("*") if p.is_file() and not p.is_symlink())
    storage = {"environment_bytes": owned_bytes, "environment_cap_bytes": ENVIRONMENT_CAP, "shared_free_bytes": shutil.disk_usage(ROOT).free, "shared_free_floor_bytes": FREE_FLOOR}
    result = {
        "checked_epoch": time.time(),
        "scope": "CPU imports and API construction only; no CUDA calls or kernel execution",
        "python_executable": os.sys.executable,
        "torch_file": torch.__file__,
        "torch_version": torch.__version__,
        "cuda_build_version": torch.version.cuda,
        "overlay_environment": str(NEW_ENV),
        "baseline_environment": str(BASE_ENV),
        "baseline_critical_files_unchanged": all(baseline_checks.values()),
        "baseline_fingerprint_checks": baseline_checks,
        "packages": packages,
        "apis": apis,
        "recipe_checks": recipe_checks,
        "storage": storage,
        "unavailable_features": {
            "coat": {
                "status": "incompatible_drop_in_recipe",
                "evidence": "fp8-coat 1.0.11 requires triton==3.1.0 and transformers==4.45.2, while this Qwen3 stack uses 3.4.0/4.57.1; official activation classes target Llama and FSDP2 integration remains a TODO.",
                "sources": ["https://pypi.org/pypi/fp8-coat/1.0.11/json", "https://github.com/NVlabs/COAT"],
            },
            "nvfp4": {
                "status": "no_compatible_binary_training_binding",
                "evidence": "Transformer Engine provides real NVFP4BlockScaling training, but transformer-engine-torch 2.20.2 on PyPI ships only a source tarball. Its current torch binding metadata also requires transformer_engine_cu13; source compilation or a different CUDA/PyTorch stack is outside this bounded binary overlay.",
                "sources": ["https://pypi.org/pypi/transformer-engine-torch/2.20.2/json", "https://docs.nvidia.com/deeplearning/transformer-engine/features/low_precision_training/nvfp4/nvfp4.html"],
            },
        },
    }
    ready = (
        all(v["status"] == "imported" for v in apis.values())
        and all(baseline_checks.values())
        and str(Path(torch.__file__).resolve()).startswith(str(BASE_ENV) + "/")
        and owned_bytes <= ENVIRONMENT_CAP
        and storage["shared_free_bytes"] >= FREE_FLOOR
    )
    result["status"] = "ready_for_gpu_checks" if ready else "partial"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "apis": {k: v["status"] for k, v in apis.items()}, "storage": storage, "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
