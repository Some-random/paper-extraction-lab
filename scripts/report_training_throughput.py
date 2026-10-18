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

ROOT = Path(__file__).resolve().parents[1]
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
)
PUBLIC_ARGUMENTS = (
    "sequence_length", "batch_size", "accumulation", "warmup", "steps",
    "max_runtime_seconds", "target_tokens", "seed",
)


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
                        if key in ("torch", "transformers")}
    if "throughput" in result:
        measurements = result["throughput"]
        safe["throughput"] = {key: public_value(measurements[key]) for key in
                              ("measured_optimizer_steps", "input_tokens_per_step", "measured_input_tokens",
                               "measured_wall_seconds", "input_tokens_per_second", "step_seconds")
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
                ("requested_gpus", "target_gpu", "submitted_at_pst", "hold_reason") if key in launch}
        safe.update(job_id=job_id, status=str(launch.get("status", "queued")).lower())
        output = result_path(launch, run_dir, root)
        if output.exists():
            safe["result"] = sanitize_result(read_json(output), job_id)
            state = safe["result"].get("status")
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


def render_markdown(cluster, jobs, generated_at, setup=None):
    lines = ["# 4B training-throughput diagnostic", "",
             f"Report updated **{generated_at}**. Cluster snapshot: **{cluster.get('checked_at_pst', 'unknown')}**.", "",
             "This is a short compute diagnostic using the pinned **Qwen3-4B architecture**, random initialization, "
             "synthetic token IDs and a **4,096-token context**. It runs BF16 forward/backward computation with "
             "FP32 master parameters and conventional AdamW optimizer states. No pretrained weights or biological "
             "training corpus are downloaded for the benchmark.", "", "## Cluster GPUs", "",
             "Each node is counted once across partitions. Unallocated GPUs are not necessarily schedulable "
             "immediately; account limits, reservations and planned allocations can apply.", "",
             "| GPU | Configured | Allocated | Unallocated on online nodes | On unavailable nodes |",
             "|:---|---:|---:|---:|---:|"]
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
            status += " — runtime setup hold"
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
        if job.get("report_note"):
            lines.extend([job["report_note"], ""])
    lines.extend(["## What the measurement covers", "",
                  "The timing includes synthetic-input transfers, forward/backward passes, optimizer updates and "
                  "the communication used by this allocation. Multiple GPUs use FSDP FULL_SHARD. "
                  "Activation checkpointing is enabled; PyTorch SDPA attention is used without torch.compile.", "",
                  "Production corpus loading, biological learning quality, validation, checkpoint saving, restart "
                  "behavior and multi-node scaling are **not tested**. Queueing and interruptions are excluded "
                  "from the compute-time estimate. No full 200B-token training run has been started.", "",
                  "Each requested allocation is bounded to 20 minutes and at most eight GPUs. "
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
        generated_at = datetime.now(PST).isoformat(timespec="seconds")
        readme = report_dir / "README.md"
        write_text(readme, render_markdown(cluster, jobs, generated_at, setup))
        generated = [readme]
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
