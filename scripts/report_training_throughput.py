#!/usr/bin/env python3
"""Render bounded training diagnostics; publish generated reports only on request."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import fcntl
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from report_publication_lock import publication_lock
DEFAULT_RUN = Path("experiments/training_throughput_2026-10-18")
DEFAULT_REPORT = Path("reports/training_throughput_2026-10-18")
PST = timezone(timedelta(hours=-8))
JOB_ID = re.compile(r"[0-9]+(?:[_+][0-9]+)?\Z")
PUBLIC_SCALARS = (
    "status", "started_utc", "world_size", "actual_parameter_count", "config_sha256", "runner_sha256",
    "cuda_runtime", "cudnn_version", "attention", "initialization", "optimizer",
    "sharding", "gradient_checkpointing", "torch_compile", "input_kind", "token_unit",
    "completed_warmup_steps", "warmup_losses", "measured_losses",
    "peak_cuda_allocated_bytes", "peak_cuda_reserved_bytes", "runtime_seconds",
    "stop_reason", "failure_type", "optimizer_state_dtypes",
    "setup_seconds", "warmup_seconds", "measurement_seconds",
)
PUBLIC_ARGUMENTS = (
    "sequence_length", "batch_size", "accumulation", "warmup", "steps",
    "max_runtime_seconds", "target_tokens", "seed", "activation_checkpointing", "sharding", "profile_steps",
    "attention", "fused_kernels", "compile", "precision", "float8_all_gather", "optimizer",
)
VERIFICATION_GROUP = "throughput_verification_2026-10-19"
OPTIMIZATION_GROUP = "b200_optimization_2026-10-19"
OPTIMIZATION_FEATURES = ("attention", "kernels", "checkpointing", "sharding", "compile", "precision",
                         "float8_all_gather", "optimizer")
MEASUREMENT_FIELDS = ("measured_optimizer_steps", "input_tokens_per_step", "measured_input_tokens",
                      "measured_wall_seconds", "input_tokens_per_second", "step_seconds")


def sanitize_timing_diagnostics(result):
    """Keep only known timing/profiler fields, never arbitrary trace metadata."""
    safe = {}
    if "phase_timings" in result:
        safe["phase_timings"] = [{key: public_value(value) for key, value in event.items() if key in
                                  ("stage", "rank", "elapsed_seconds", "utc", "setup_seconds", "measured_steps")}
                                 for event in result["phase_timings"][:100]]
    if "profiler" in result:
        profiler = result["profiler"]
        safe["profiler"] = {key: public_value(value) for key, value in profiler.items() if key in
                            ("status", "reason", "rank", "unit", "timing_scope", "elapsed_seconds",
                             "totals_are_overlapping", "observed_operator_count", "truncated")}
        for kind in ("operators", "cuda_kernels"):
            safe["profiler"][kind] = [{key: public_value(value) for key, value in row.items() if key in
                                       ("name", "calls", "self_cpu_us", "cpu_total_us", "self_device_us",
                                        "device_total_us", "categories")}
                                      for row in profiler.get(kind, [])[:100]]
    return safe


def sanitize_profile(profile):
    safe = {key: public_value(value) for key, value in profile.items() if key in
            ("name", "role", "microbatch_per_gpu", "accumulation", "activation_checkpointing", "sharding",
             "profile_steps", "status", "exit_code", "input_tokens_per_second", "measured_optimizer_steps",
             "input_tokens_per_step", "peak_cuda_allocated_bytes", "peak_cuda_reserved_bytes", "failure_type",
             "setup_seconds", "warmup_seconds", "measurement_seconds", "launcher_wall_seconds",
             "parent", "resolved_parent", "comparison_scope", "profiler_seconds")}
    for key in ("smoke_checks", "optimizer_update_check"):
        if isinstance(profile.get(key), dict):
            safe[key] = {name: public_value(value) for name, value in profile[key].items()
                         if name in ("status", "scope", "seconds", "dtype", "any_rank_changed",
                                     "sampled_elements", "maximum_local_absolute_change")}
    if isinstance(profile.get("features"), dict):
        safe["features"] = {key: public_value(value) for key, value in profile["features"].items()
                            if key in OPTIMIZATION_FEATURES and isinstance(value, (str, bool))}
    if "throughput" in profile:
        safe["throughput"] = {key: public_value(value) for key, value in profile["throughput"].items()
                              if key in MEASUREMENT_FIELDS}
    safe.update(sanitize_timing_diagnostics(profile))
    return safe


def write_json(path, payload):
    write_text(path, json.dumps(payload, indent=2, allow_nan=False) + "\n")


def write_text(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value)
    temporary.replace(path)


def read_json(path):
    # These are compact manifests/results, never model files or corpus contents.
    if path.stat().st_size > 2 * 1024 * 1024:
        raise ValueError(f"Manifest exceeds the 2 MiB limit: {path.name}")
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path.name}")
    return value


def public_value(value):
    """Defend against accidental paths in otherwise allowed diagnostic strings."""
    if isinstance(value, dict):
        return {str(key): public_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [public_value(item) for item in value]
    if isinstance(value, str):
        value = re.sub(r"(?<![\w:])/(?:[^\s\"'<>()[\]{}]+)", "[local path]", value)
        return re.sub(r"(?<!\w)(?:experiments|\.throughput-venv|\.review-venv)/[^\s\"'<>()[\]{}]+",
                      "[local path]", value)
    return value


def sanitize_result(result, job_id):
    # Hostnames, traceback text, arbitrary failure strings and argument paths are
    # deliberately excluded rather than trying to redact all possible formats.
    safe = {key: public_value(result[key]) for key in PUBLIC_SCALARS if key in result}
    safe["job_id"] = job_id
    safe["arguments"] = {key: public_value(value) for key, value in result.get("arguments", {}).items()
                         if key in PUBLIC_ARGUMENTS}
    safe["hardware"] = [{key: public_value(item[key]) for key in
                         ("rank", "gpu", "total_memory_bytes", "compute_capability") if key in item}
                        for item in result.get("hardware", [])]
    safe["packages"] = {key: public_value(value) for key, value in result.get("packages", {}).items()
                        if key in ("torch", "transformers", "triton", "torchao", "liger-kernel",
                                   "cut-cross-entropy", "flash-attn-4")}
    safe.update(sanitize_timing_diagnostics(result))
    if "suite" in result:
        suite = result["suite"]
        safe["suite"] = {key: public_value(value) for key, value in suite.items() if key in
                         ("status", "world_size", "sequence_length", "global_batch_sequences",
                          "input_tokens_per_update", "selection", "started_utc", "runtime_seconds",
                          "runner_sha256", "selected_profile", "mode", "tuning_speedup_over_baseline",
                          "stop_reason", "rate_scope")}
        safe["suite"]["profiles"] = [sanitize_profile(profile) for profile in suite.get("profiles", [])]
        for key in ("baseline_result", "fastest_completed_profile"):
            if isinstance(suite.get(key), dict):
                safe["suite"][key] = sanitize_profile(suite[key])
    if "throughput" in result:
        measurements = result["throughput"]
        safe["throughput"] = {key: public_value(measurements[key]) for key in
                              MEASUREMENT_FIELDS
                              if key in measurements}
        # Recalculate from the actual allocation and measured aggregate rate;
        # never project a single-GPU measurement to a hypothetical larger job.
        world = result.get("world_size")
        rate = measurements.get("input_tokens_per_second")
        if (isinstance(world, int) and world > 0 and valid_rate(rate)
                and result.get("status") in ("completed", "runtime_limit")):
            safe["throughput"]["extrapolation"] = {
                "target_input_tokens": 200_000_000_000,
                "gpu_count": world,
                "seconds": 200_000_000_000 / rate,
                "days": 200_000_000_000 / rate / 86400,
                "scope": "Measured allocation only; excludes queueing, production corpus loading, "
                         "checkpointing, validation and interruptions",
            }
    return safe


def valid_rate(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def result_path(launch, run_dir, root):
    explicit = launch.get("results_path") or launch.get("result_path")
    if explicit:
        path = Path(explicit)
        return path if path.is_absolute() else root / path
    job_id = str(launch["job_id"])
    candidates = [run_dir / f"job_{job_id}" / "results.json", run_dir / job_id / "results.json"]
    found = [path for path in candidates if path.exists()]
    if not found:
        found = [path for path in run_dir.glob("**/results.json") if
                 job_id in path.relative_to(run_dir).parts or
                 any(part in (f"job_{job_id}", f"job-{job_id}") for part in path.relative_to(run_dir).parts)]
    if len(found) > 1:
        raise ValueError(f"Ambiguous result paths for job {job_id}; set results_path")
    return found[0] if found else candidates[0]


def load_jobs(run_dir, root):
    jobs, seen = [], set()
    for path in sorted(run_dir.glob("launch*.json")):
        launch = read_json(path)
        job_id = str(launch.get("job_id", ""))
        if not JOB_ID.fullmatch(job_id):
            raise ValueError(f"Invalid or missing job ID in {path.name}")
        if job_id in seen:
            raise ValueError(f"Duplicate launch manifest for job {job_id}")
        seen.add(job_id)
        safe = {key: public_value(launch[key]) for key in
                ("requested_gpus", "target_gpu", "submitted_at_pst", "hold_reason", "admission_required",
                 "admission_status", "comparison_group", "global_batch_tokens", "superseded_reason",
                 "qos", "dependency", "scheduling_mode") if key in launch}
        safe.update(job_id=job_id, status=str(launch.get("status", "queued")).lower())
        output = result_path(launch, run_dir, root)
        if output.exists():
            safe["result"] = sanitize_result(read_json(output), job_id)
            state = safe["result"].get("status")
            # A result written before cancellation/failure must not resurrect a
            # job. The watcher records scheduler authority in the launch file.
            authoritative = (safe["status"] == "cancelled" or launch.get("scheduler_observed")
                             or launch.get("slurm_state") in {
                                 "CANCELLED", "FAILED", "TIMEOUT", "PREEMPTED", "OUT_OF_MEMORY",
                                 "NODE_FAIL", "BOOT_FAIL", "DEADLINE", "REVOKED"})
            if not authoritative:
                safe["status"] = {"completed": "success", "runtime_limit": "failed",
                                  "failed": "failed", "initializing": "running"}.get(state, safe["status"])
        if safe["status"] in ("submitted", "pending"):
            safe["status"] = "queued"
        if safe["status"] == "completed":
            safe["status"] = "success"
        if safe["status"] not in ("queued", "running", "failed", "success", "cancelled"):
            raise ValueError(f"Unsupported job status for {job_id}: {safe['status']}")
        if safe["status"] == "success" and "result" not in safe:
            safe["status"] = "failed"
            safe["report_note"] = "Job ended without a retained measurement result."
        jobs.append(safe)
    return jobs


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def sanitize_monitor(snapshot):
    safe = {key: public_value(snapshot[key]) for key in
            ("checked_at_pst", "watcher_status", "stop_reason", "delivery") if key in snapshot}
    safe["setup"] = {key: public_value(value) for key, value in snapshot.get("setup", {}).items()
                     if key in ("stage", "error_type", "updated_at_pst")}
    safe["admission"] = {key: public_value(value) for key, value in snapshot.get("admission", {}).items()
                         if key in ("checked_at_pst", "supervisor_status", "stop_reason")}
    safe["scheduler_errors"] = [{key: public_value(value) for key, value in error.items()
                                 if key in ("source", "error_type")}
                                for error in snapshot.get("scheduler_errors", [])]
    safe["jobs"] = [{key: public_value(value) for key, value in job.items() if key in
                     ("job_id", "status", "scheduler_state", "scheduler_observed", "requested_gpus",
                      "target_gpu", "result_status", "failure_type", "input_tokens_per_second",
                      "admission_status", "hold_reason", "comparison_group")}
                    for job in snapshot.get("jobs", [])]
    return safe


def completed_profile_rate(profile):
    if profile.get("status") != "completed" or profile.get("exit_code") != 0:
        return None
    rate = profile.get("input_tokens_per_second", profile.get("throughput", {}).get("input_tokens_per_second"))
    return rate if valid_rate(rate) else None


def seconds_cell(value):
    return f"{value:,.2f}" if (isinstance(value, (int, float)) and not isinstance(value, bool)
                               and math.isfinite(value) and value >= 0) else "—"


def render_verification(jobs):
    verification = [job for job in jobs if job.get("comparison_group") == VERIFICATION_GROUP]
    if not verification:
        return []
    lines = ["## Throughput verification", "",
             "These follow-up allocations separate **setup, warmup and timed training**. Each uses the same "
             "4B architecture, 4,096-token context and **131,072 input tokens per optimizer update**. "
             "The baseline retains activation checkpointing and FSDP FULL_SHARD, using microbatch 4 per GPU. "
             "The two-B200 allocation also tests checkpointing disabled with SHARD_GRAD_OP, at microbatches 4 and 8.", "",
             "The two requests add at most **3.33 GPU-hours** (two B200s and eight A100s, 20 minutes each), "
             "with one benchmark allocation running at a time. **Only baseline-to-baseline measurements compare "
             "the same training recipe across hardware.** Faster tuned profiles are separate optimization results. "
             "A timeout provides no training-speed ranking.", "",
             "| Job / allocation | Status | Baseline input tokens/s | Fastest completed tuning input tokens/s |",
             "|:---|:---|---:|---:|"]
    for job in verification:
        suite = job.get("result", {}).get("suite", {})
        profiles = suite.get("profiles", [])
        baseline = suite.get("baseline_result", next((item for item in profiles if item.get("role") == "baseline"), {}))
        tuned_rates = [completed_profile_rate(item) for item in profiles if item.get("role") == "tuning"]
        baseline_rate = completed_profile_rate(baseline) if job["status"] == "success" else None
        tuned_rate = max((rate for rate in tuned_rates if valid_rate(rate)), default=None)
        if job["status"] != "success":
            tuned_rate = None
        lines.append(f"| {job['job_id']} / {job.get('requested_gpus')} × {cell(job.get('target_gpu', 'unknown'))} | "
                     f"{cell(job['status'])} | {format(baseline_rate, ',.0f') if valid_rate(baseline_rate) else '—'} | "
                     f"{format(tuned_rate, ',.0f') if valid_rate(tuned_rate) else '—'} |")
    lines.extend(["", "**Timing scope:** input tokens/s divides timed training tokens by timed training wall time. "
                  "Setup and warmup are excluded. A separate post-measurement profiler update is also excluded; "
                  "profiler operator/device durations can overlap and must not be added as a wall-time breakdown.", ""])
    for job in verification:
        profiles = job.get("result", {}).get("suite", {}).get("profiles", [])
        if not profiles:
            continue
        lines.extend([f"Suite status: **{cell(suite.get('status', 'unknown'))}**. "
                      f"Stop reason: **{cell(suite.get('stop_reason') or 'none')}**.", ""])
        lines.extend([f"### Verification job {job['job_id']}", "",
                      "| Profile / role | Checkpointing / sharding | Microbatch × accumulation | Status | Input tokens/s | Setup s | Warmup s | Timed training s | Profiler s |",
                      "|:---|:---|:---|:---|---:|---:|---:|---:|---:|"])
        for profile in profiles:
            state = profile.get("status", "unknown")
            if profile.get("failure_type"):
                state += f" — {profile['failure_type']}"
            rate = completed_profile_rate(profile)
            measured = profile.get("measurement_seconds", profile.get("throughput", {}).get("measured_wall_seconds"))
            lines.append(f"| {cell(profile.get('name', 'unknown'))} / {cell(profile.get('role', 'unknown'))} | "
                         f"{cell(profile.get('activation_checkpointing', '—'))} / {cell(profile.get('sharding', '—'))} | "
                         f"{profile.get('microbatch_per_gpu', '—')} × {profile.get('accumulation', '—')} | {cell(state)} | "
                         f"{format(rate, ',.0f') if valid_rate(rate) else '—'} | "
                         f"{seconds_cell(profile.get('setup_seconds'))} | {seconds_cell(profile.get('warmup_seconds'))} | "
                         f"{seconds_cell(measured)} | {seconds_cell(profile.get('profiler', {}).get('elapsed_seconds'))} |")
        lines.append("")
        for profile in profiles:
            profiler = profile.get("profiler", {})
            operators = [row.get("name", "") for row in profiler.get("operators", [])
                         if "attention" in row.get("categories", [])]
            kernels = [row.get("name", "") for row in profiler.get("cuda_kernels", [])
                       if any(marker in row.get("name", "").lower() for marker in ("attention", "flash", "fmha"))]
            if operators or kernels:
                evidence = []
                if operators:
                    evidence.append("observed attention operators: " + ", ".join(f"`{cell(name)}`" for name in operators[:6]))
                if kernels:
                    evidence.append("observed CUDA kernels: " + ", ".join(f"`{cell(name)}`" for name in kernels[:4]))
                lines.extend([f"**{cell(profile.get('name', 'unknown'))}:** " + "; ".join(evidence) + ".", ""])
            elif profiler:
                lines.extend([f"**{cell(profile.get('name', 'unknown'))}:** no attention operator or CUDA-kernel "
                              "evidence retained in the compact profiler output.", ""])
            if profile.get("status") != "completed" and profile.get("phase_timings"):
                last = profile["phase_timings"][-1]
                lines.extend([f"Last retained milestone for **{cell(profile.get('name', 'unknown'))}**: "
                              f"**{cell(last.get('stage', 'unknown'))}**, {seconds_cell(last.get('elapsed_seconds'))} "
                              "seconds after process start. This identifies progress, not the cause of a stall.", ""])
    return lines


def render_optimization(jobs):
    selected = [job for job in jobs if job.get("comparison_group") == OPTIMIZATION_GROUP]
    if not selected:
        return []
    lines = ["## B200 optimization sweep", "",
             "A controlled two-B200 sweep keeps the Qwen3-4B architecture, 4,096-token context and "
             "131,072 input positions per optimizer update fixed. It compares attention backends, fused losses "
             "and pointwise kernels, checkpointing, sharding, compilation and native low precision. "
             "Individual changes precede selected combinations; unavailable features and failures stay visible.", "",
             "This allocation is bounded to **two hours / four GPU-hours**, with a persistent 110-minute suite "
             "budget. Setup and warmup are outside steady training throughput. Warmup includes compilation "
             "where enabled. Numerical smoke checks establish executable compatibility, not biological "
             "quality or long-run convergence. [Evidence and test rationale](training_speedups_2026-10-19.md).", ""]
    lines.extend(["The planned comparisons include PyTorch Flash/cuDNN and FlashAttention-4; Liger and "
                  "Cut Cross-Entropy; activation recomputation and batch sizes; FSDP2; compilation; "
                  "native FP8/MXFP8 and FP8 communication; and an explicitly labeled 8-bit AdamW-state "
                  "variant. The final combinations use successful earlier measurements. "
                  "Any options left by the time limit are shown as skipped.", "",
                  "COAT's released integration requires incompatible library versions. Native NVFP4 "
                  "requires a separate training-library build in this environment. Both remain "
                  "unavailable here; neither is counted as an executed speed test.", ""])
    for job in selected:
        suite = job.get("result", {}).get("suite", {})
        profiles = suite.get("profiles", [])
        lines.extend([f"### Optimization job {job['job_id']}", "",
                      f"Allocation: **{job.get('requested_gpus')} × {cell(job.get('target_gpu', 'unknown'))}**. "
                      f"Scheduler status: **{cell(job['status'])}**.", ""])
        completed = [(profile, completed_profile_rate(profile)) for profile in profiles]
        completed = [(profile, rate) for profile, rate in completed if valid_rate(rate)]
        if completed and job["status"] == "success":
            best, rate = max(completed, key=lambda item: item[1])
            baseline = next((value for profile, value in completed if profile.get("role") == "baseline"), None)
            improvement = f"; **{rate / baseline:.2f}×** the new baseline" if valid_rate(baseline) else ""
            lines.extend([f"Fastest completed profile: **{cell(best.get('name'))}**, **{rate:,.0f} input tokens/s**"
                          f"{improvement}.", ""])
        if not profiles:
            lines.extend(["No profile measurements are available yet.", ""])
            continue
        lines.extend(["| Profile | Parent | Attention / precision | Status | Input tokens/s | Peak allocated GiB |",
                      "|:---|:---|:---|:---|---:|---:|"])
        for profile in profiles:
            features = profile.get("features", {})
            status = profile.get("status", "unknown")
            if profile.get("failure_type"):
                status += " — " + profile["failure_type"]
            rate = completed_profile_rate(profile)
            memory = profile.get("peak_cuda_allocated_bytes")
            memory = f"{memory / 1024 ** 3:.2f}" if valid_rate(memory) else "—"
            lines.append(f"| {cell(profile.get('name', 'unknown'))} | "
                         f"{cell(profile.get('resolved_parent') or profile.get('parent') or '—')} | "
                         f"{cell(features.get('attention', '—'))} / {cell(features.get('precision', '—'))} | "
                         f"{cell(status)} | {format(rate, ',.0f') if valid_rate(rate) else '—'} | {memory} |")
        lines.extend(["", "Full feature settings, timings and retained failures are in the "
                      f"[sanitized results](results_{job['job_id']}.json).", ""])
    return lines


def render_markdown(cluster, jobs, generated_at, setup=None, monitor=None):
    lines = ["# 4B training-throughput diagnostic", "",
             f"Report updated **{generated_at}**. Cluster snapshot: **{cluster.get('checked_at_pst', 'unknown')}**.", ""]
    if setup:
        stage = cell(setup.get("stage", "unknown"))
        failure = f" ({cell(setup['error_type'])})" if setup.get("error_type") else ""
        lines.extend([f"Runtime setup: **{stage}{failure}**.", ""])
        if setup.get("prior_setup_failure_type"):
            lines.extend([f"The earlier setup failed with **{cell(setup['prior_setup_failure_type'])}**. "
                          "Its cancelled requests are retained below. Replacement CPU validation passed.", ""])
    if monitor:
        lines.extend([f"Scheduler last checked **{cell(monitor.get('checked_at_pst', 'unknown'))}**. "
                      f"Monitor: **{cell(monitor.get('watcher_status', 'unknown'))}**. "
                      "[Status snapshot](status.json).", "",
                      "While work is pending or running, this page is updated hourly even without a status change, "
                      "and promptly on failure or completion. A separate session monitor queues the requested "
                      "hourly chat updates.", ""])
        if monitor.get("scheduler_errors"):
            lines.extend(["**Scheduler query incomplete.** Some job states use the last observation; "
                          "see the status snapshot for query errors.", ""])
    lines.extend(["This is a short compute diagnostic using the pinned **Qwen3-4B architecture**, random initialization, "
             "synthetic token IDs and a **4,096-token context**. The baseline runs BF16 computation with "
             "FP32 master parameters and conventional AdamW optimizer states; optimization profiles identify "
             "their precision and kernel changes. No pretrained weights or biological "
             "training corpus are downloaded for the benchmark.", ""])
    lines.extend(render_optimization(jobs))
    lines.extend(render_verification(jobs))
    comparison = [job for job in jobs if job.get("comparison_group") in
                  {"2b200_vs_8a100", "gpu_allocation_comparison"}]
    if comparison:
        gpu_hours = sum(job.get("requested_gpus", 0) for job in comparison) / 3
        lines.extend(["## Matched GPU allocation comparison", "",
                      "All allocations use **32 sequences × 4,096 positions = 131,072 input tokens per optimizer "
                      "update**, BF16 computation, FP32 AdamW and FSDP FULL_SHARD. Each tests microbatches of "
                      "1, 2 and 4 per GPU with matching gradient accumulation. Each profile requests three warmup "
                      "and eight measured updates. OOM, partial and skipped profiles remain visible; only fully "
                      "completed profiles can supply the reported best rate.", "",
                      f"Each allocation has a **20-minute wall limit**; the listed requests together use at most **{gpu_hours:.2f} GPU-hours**. "
                      "Slurm schedules these requests normally; the earlier idle-only admission gate has been removed. "
                      "After-any dependencies limit execution to one benchmark allocation at a time. "
                      "Queue waiting is separate from execution time.", "",
                      "| Allocation | Status | Best completed input tokens/s | Seconds/update | Peak memory/GPU |",
                      "|:---|:---|---:|---:|---:|"])
        for job in comparison:
            result = job.get("result", {})
            rate = result.get("throughput", {}).get("input_tokens_per_second") if job["status"] == "success" else None
            state = job["status"]
            if state == "queued" and job.get("admission_required"):
                state = "waiting for spare capacity" if job.get("hold_reason") else "queued"
            if job.get("admission_status") == "expired":
                state = "waiting; automatic admission stopped at its deadline"
            if job.get("admission_status") == "invalid_request":
                state = "held; admission validation failed"
            memory = result.get("peak_cuda_allocated_bytes")
            lines.append(f"| {job.get('requested_gpus')} × {cell(job.get('target_gpu', 'unknown'))} | {cell(state)} | "
                         f"{format(rate, ',.0f') if valid_rate(rate) else '—'} | "
                         f"{format(131072 / rate, '.2f') if valid_rate(rate) else '—'} | "
                         f"{format(memory / 2**30, '.1f') + ' GiB' if valid_rate(memory) else '—'} |")
        lines.extend(["", "The earlier one-B200 diagnostic uses a different global batch and provides context only. "
                      "The comparison above reports the best of the tested profiles, not a claim of maximum possible "
                      "performance. These short synthetic runs do not test biological learning or checkpoint recovery.", ""])
        lines.extend(["Two B200s and eight A100s use regular **il**. Four and eight B200s use preemptible **il-lo**, "
                      "because regular B200 access is capped at two per user. GPU count alone does not remove "
                      "preemption eligibility.", ""])
        lines.extend(["The benchmark initializes the **Qwen3-4B-Base architecture with random weights**. "
                      "Proteo-R1's [official checkpoint configuration](https://huggingface.co/thinking-bio-lab/proteor1-understand/blob/main/config.json) "
                      "identifies **Qwen3-4B-Instruct-2507** as its language backbone. Their core layer dimensions match; "
                      "the context/RoPE settings and starting weights differ. These tests exclude Proteo-R1's "
                      "protein-specific encoders and diffusion generator. "
                      "[Configuration comparison](../../config/proteor1_backbone_reference.json).", ""])
    lines.extend(["## Cluster GPUs", "",
             "Each node is counted once across partitions. Unallocated GPUs are not necessarily schedulable "
             "immediately; account limits, reservations and planned allocations can apply.", "",
             "| GPU | Configured | Allocated | Unallocated on online nodes | On unavailable nodes |",
             "|:---|---:|---:|---:|---:|"])
    total = [0, 0, 0, 0]
    for name, counts in cluster.get("gpus", {}).items():
        numbers = [counts.get(key, 0) for key in
                   ("configured", "allocated", "unallocated_online", "unavailable_node")]
        if any(not isinstance(number, int) or number < 0 for number in numbers):
            raise ValueError("GPU inventory counts must be nonnegative integers")
        total = [left + right for left, right in zip(total, numbers)]
        lines.append("| " + cell(name.upper()) + " | " + " | ".join(map(str, numbers)) + " |")
    lines.extend(["| **Total** | " + " | ".join(f"**{number}**" for number in total) + " |", "",
                  "## Benchmark jobs", ""])
    completed = [job for job in jobs if job["status"] == "success"]
    if not completed:
        lines.extend(["**No completed throughput measurement yet.** Queued jobs have not produced a measured "
                      "training-time estimate.", ""])
    lines.extend(["| Job | Status | GPUs | GPU type | Measured input tokens/s | 200B tokens at this allocation |",
                  "|:---|:---|---:|:---|---:|---:|"])
    for job in jobs:
        result = job.get("result", {})
        throughput = result.get("throughput", {})
        extrapolation = throughput.get("extrapolation", {})
        measured = result.get("status") in ("completed", "runtime_limit")
        rate = throughput.get("input_tokens_per_second") if measured else None
        gpu_count = result.get("world_size", job.get("requested_gpus", "—"))
        hardware = result.get("hardware", [])
        gpu = hardware[0].get("gpu") if hardware else job.get("target_gpu", "—")
        status = job["status"]
        if status == "queued" and job.get("hold_reason"):
            status += " — waiting for spare capacity" if job.get("admission_required") else " — runtime setup hold"
        if job.get("superseded_reason"):
            status += " — replaced by the matched comparison"
        if result.get("status") == "runtime_limit":
            status += " — time limit; partial measurement" if valid_rate(rate) else " — time limit"
        elif status == "failed" and result.get("failure_type"):
            status += f" — {result['failure_type']}"
        days = extrapolation.get("days")
        duration = f"{days:,.2f} days" if valid_rate(days) else "—"
        if measured and result.get("status") == "runtime_limit" and duration != "—":
            duration += " (partial)"
        lines.append(f"| {job['job_id']} | {cell(status)} | {cell(gpu_count)} | {cell(gpu)} | "
                     f"{format(rate, ',.0f') if valid_rate(rate) else '—'} | {duration} |")
    if not jobs:
        stage = "Setup, no GPU job submitted" if setup else "No submitted job recorded"
        lines.append(f"| — | {stage} | — | — | — | — |")
    lines.extend(["", "Measured token rates are aggregate input positions per second at the **actual measured GPU count**. "
                  "The 200B-token duration is `200,000,000,000 / measured tokens per second`; no unmeasured GPU "
                  "allocation or multi-node scaling is extrapolated.", ""])
    for job in jobs:
        result = job.get("result", {})
        throughput = result.get("throughput", {})
        if not result:
            continue
        lines.extend([f"### Job {job['job_id']}", "",
                      f"Status: **{cell(job['status'])}**. Sanitized diagnostics: "
                      f"[results_{job['job_id']}.json](results_{job['job_id']}.json).", ""])
        if throughput:
            lines.append(f"Measured {throughput.get('measured_optimizer_steps', 0)} optimizer steps "
                         f"after {result.get('completed_warmup_steps', 0)} warmup steps. "
                         f"Context: {result.get('arguments', {}).get('sequence_length', 'unknown')}; "
                         f"microbatch per GPU: {result.get('arguments', {}).get('batch_size', 'unknown')}; "
                         f"gradient accumulation: {result.get('arguments', {}).get('accumulation', 'unknown')}.")
            lines.append("")
        if result.get("suite"):
            lines.extend(["| Microbatch/GPU | Accumulation | Status | Measured input tokens/s |",
                          "|---:|---:|:---|---:|"])
            for profile in result["suite"].get("profiles", []):
                state = profile.get("status", "unknown")
                if profile.get("failure_type"):
                    state += f" — {profile['failure_type']}"
                rate = profile.get("input_tokens_per_second") if profile.get("status") == "completed" else None
                lines.append(f"| {profile.get('microbatch_per_gpu', '—')} | {profile.get('accumulation', '—')} | "
                             f"{cell(state)} | {format(rate, ',.0f') if valid_rate(rate) else '—'} |")
            lines.append("")
        if job.get("report_note"):
            lines.extend([job["report_note"], ""])
    lines.extend(["## What the measurement covers", "",
                  "The timing includes synthetic-input transfers, forward/backward passes, optimizer updates and "
                  "the communication used by this allocation. The original matched comparison uses FSDP FULL_SHARD "
                  "and activation checkpointing. Verification tuning profiles list their different settings above. "
                  "The original comparisons request PyTorch SDPA without torch.compile; observed backend evidence, when "
                  "available, is reported separately. Setup, warmup and profiling are outside the measured denominator.", "",
                  "Production corpus loading, biological learning quality, validation, checkpoint saving, restart "
                  "behavior and multi-node scaling are **not tested**. Queueing and interruptions are excluded "
                  "from the compute-time estimate. No full 200B-token training run has been started.", "",
                  "The original comparison and verification allocations are bounded to 20 minutes and at most "
                  "eight GPUs. The optimization allocation above uses two B200s for at most two hours. "
                  "No existing jobs are modified by this diagnostic.", ""])
    return "\n".join(lines)


def git_command(root, *args):
    # Spool output rather than accumulating an unbounded subprocess pipe. Only a
    # bounded tail is returned; transport output never enters public reports.
    with tempfile.TemporaryFile() as output:
        process = subprocess.Popen(["git", *args], cwd=root, stdout=output, stderr=output)
        try:
            code = process.wait(timeout=60)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            raise RuntimeError(f"git {args[0]} exceeded 60 seconds") from None
        if code:
            raise RuntimeError(f"git {args[0]} failed with exit code {code}; inspect private command logs")
        length = output.tell()
        if length > 65536:
            raise RuntimeError(f"git {args[0]} output exceeded the 64 KiB limit")
        output.seek(0)
        return output.read().decode("utf-8", errors="replace").strip()


def publish(root, report_dir, generated_paths):
    with publication_lock(root):
        return _publish(root, report_dir, generated_paths)


def _publish(root, report_dir, generated_paths):
    relative = report_dir.resolve().relative_to(root.resolve())
    if relative != DEFAULT_REPORT:
        raise ValueError(f"Publication is restricted to {DEFAULT_REPORT}")
    paths = [str(path.resolve().relative_to(root.resolve())) for path in generated_paths]
    if git_command(root, "symbolic-ref", "--short", "HEAD") != "main":
        raise RuntimeError("Automatic publication requires main")
    if git_command(root, "rev-parse", "--abbrev-ref", "@{upstream}") != "origin/main":
        raise RuntimeError("Automatic publication requires upstream origin/main")
    for commit in git_command(root, "rev-list", "origin/main..HEAD").splitlines():
        subject = git_command(root, "show", "-s", "--format=%s", commit)
        changed = set(git_command(root, "diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines())
        if not subject.startswith("Report training throughput:") or not changed.issubset(paths):
            raise RuntimeError("Unpublished unrelated commits require review before automatic publication")
    git_command(root, "add", "--", *paths)
    if git_command(root, "diff", "--name-only", "HEAD", "--", *paths):
        git_command(root, "commit", "--only", "-m", "Report training throughput: bounded 4B diagnostic", "--", *paths)
    git_command(root, "push", "origin", "refs/heads/main:refs/heads/main")
    return git_command(root, "rev-parse", "HEAD")


@contextmanager
def report_lock(run_dir):
    run_dir.mkdir(parents=True, exist_ok=True)
    with (run_dir / "report.lock").open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def build_report(run_dir, report_dir, root=ROOT, publish_requested=False):
    with report_lock(run_dir):
        cluster = read_json(report_dir / "cluster_gpus.json")
        jobs = load_jobs(run_dir, root)
        setup_path = run_dir / "setup_state.json"
        setup = read_json(setup_path) if setup_path.exists() else None
        monitor_path = run_dir / "status.json"
        monitor = sanitize_monitor(read_json(monitor_path)) if monitor_path.exists() else None
        generated_at = datetime.now(PST).isoformat(timespec="seconds")
        readme = report_dir / "README.md"
        write_text(readme, render_markdown(cluster, jobs, generated_at, setup, monitor))
        generated = [readme]
        if monitor:
            destination = report_dir / "status.json"
            write_json(destination, monitor)
            generated.append(destination)
        for job in jobs:
            if "result" in job:
                destination = report_dir / f"results_{job['job_id']}.json"
                write_json(destination, job["result"])
                generated.append(destination)
        if publish_requested:
            commit = publish(root, report_dir, generated)
            return {"status": "published", "jobs": len(jobs), "commit": commit}
        return {"status": "rendered", "jobs": len(jobs)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, default=ROOT / DEFAULT_RUN)
    parser.add_argument("--report-dir", type=Path, default=ROOT / DEFAULT_REPORT)
    parser.add_argument("--publish", action="store_true", help="Commit and push only generated diagnostic reports")
    args = parser.parse_args()
    try:
        summary = build_report(args.run_dir, args.report_dir, publish_requested=args.publish)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        parser.exit(1, f"Training report failed: {type(error).__name__}: {error}\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
