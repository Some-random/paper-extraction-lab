#!/usr/bin/env python3
"""Release only allowlisted held benchmarks after spare-capacity checks.

This CPU-only supervisor never submits GPU work, cancels jobs, changes resource
requests or touches another user's jobs. Capacity checks and scheduler previews
are observations, not an atomic reservation; Slurm remains the allocator.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import time

import report_training_throughput as report
from watch_training_throughput import scheduler_command, timestamp

DONE = {"terminal", "invalid_request"}
ACTIVE = {"released", "already_started", "not_held"}
TERMINAL_SLURM = {"COMPLETED", "CANCELLED", "FAILED", "TIMEOUT", "OUT_OF_MEMORY", "NODE_FAIL",
                  "BOOT_FAIL", "PREEMPTED", "REVOKED", "DEADLINE"}
SHAPES = {("b200", 2): (24, 192 * 1024), ("a100", 8): (48, 384 * 1024),
          ("b200", 4): (32, 256 * 1024), ("b200", 8): (48, 384 * 1024)}


def fields(line):
    return dict(re.findall(r"(?:^|\s)([A-Za-z][A-Za-z0-9_/:]*)=([^\s]*)", line))


def tres(value):
    return dict(item.split("=", 1) for item in value.split(",") if "=" in item)


def mib(value):
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)([KMGT]?)", str(value))
    if not match:
        raise ValueError("Unrecognized scheduler memory unit")
    return float(match[1]) * {"": 1, "K": 1 / 1024, "M": 1, "G": 1024, "T": 1024 ** 2}[match[2]]


def spare(node, gpu_type, count, cpus, memory):
    state = set(node.get("State", "").split("+"))
    if not state & {"IDLE", "MIXED"} or state & {
        "DOWN", "DRAIN", "DRAINING", "MAINT", "FAIL", "FAILING", "NOT_RESPONDING",
        "POWER_DOWN", "POWERED_DOWN", "POWERING_DOWN", "REBOOT_REQUESTED", "REBOOT_ISSUED",
    } or "il" not in node.get("Partitions", "").split(","):
        return False
    configured, allocated = tres(node.get("CfgTRES", "")), tres(node.get("AllocTRES", ""))
    key = f"gres/gpu:{gpu_type}"
    # Never infer that untyped GPU allocations belong to another GPU type.
    if int(allocated.get("gres/gpu", 0)) and key not in allocated:
        return False
    return (int(configured.get(key, 0)) - int(allocated.get(key, 0)) >= count
            and int(node.get("CPUEfctv", node.get("CPUTot", 0))) - int(node.get("CPUAlloc", 0)) >= cpus
            and int(node.get("RealMemory", 0)) - int(node.get("AllocMem", 0)) >= memory)


def request_shape(launch):
    gpu = str(launch.get("gpu_type", launch.get("target_gpu", ""))).lower()
    shape = (gpu, launch.get("requested_gpus"))
    cpus, memory = SHAPES.get(shape, (None, None))
    if (not launch.get("admission_required") or cpus is None
            or launch.get("cpus_per_task") != cpus or launch.get("memory_mib") != memory):
        raise ValueError("Manifest does not match an authorized benchmark shape")
    return gpu, shape[1], cpus, memory


def valid_job(job, job_id, shape, uid):
    gpu, count, cpus, memory = shape
    requested = tres(job.get("ReqTRES", ""))
    owner = re.search(r"\(([0-9]+)\)$", job.get("UserId", ""))
    return (job.get("JobId") == job_id and owner is not None and int(owner[1]) == uid
            and job.get("JobName") == "bio4b-match" and job.get("QOS") == "il-lo"
            and job.get("Account") == "infolab" and job.get("Partition") == "il"
            and job.get("Nice") == "10000" and job.get("Requeue") == "0"
            and job.get("NumNodes") in {"1", "1-1"} and job.get("NumTasks") == "1"
            and job.get("NumCPUs") == str(cpus) and job.get("TimeLimit") == "00:20:00"
            and int(requested.get(f"gres/gpu:{gpu}", 0)) == count
            and int(requested.get("gres/gpu", 0)) == count
            and mib(requested.get("mem", "0")) == memory)


def preview_arguments(node, shape):
    gpu, count, cpus, memory = shape
    return ["sbatch", "--test-only", "--account=infolab", "--partition=il", "--qos=il-lo",
            "--nice=10000", "--job-name=bio4b-match", "--nodes=1", "--ntasks=1",
            f"--cpus-per-task={cpus}", f"--mem={memory}M", f"--gres=gpu:{gpu}:{count}",
            "--time=00:20:00", "--no-requeue", f"--nodelist={node}", "--wrap=true"]


def preview_safe(output, node):
    return (not re.search(r"Preempts\s*:", output, re.IGNORECASE)
            and "to start at" in output and re.search(rf"\bnodes\s+{re.escape(node)}\b", output) is not None)


def attempt(job_id, launch, command=scheduler_command, uid=None):
    shape = request_shape(launch)
    job = fields(command(["scontrol", "show", "job", "-o", job_id]))
    if not valid_job(job, job_id, shape, os.getuid() if uid is None else uid):
        return {"status": "invalid_request"}
    if job.get("JobState") != "PENDING":
        return {"status": "terminal" if job.get("JobState") in TERMINAL_SLURM else "already_started",
                "scheduler_state": job.get("JobState")}
    if job.get("Reason") != "JobHeldUser" or job.get("Priority") != "0":
        return {"status": "not_held"}
    nodes = [fields(line) for line in command(["scontrol", "show", "nodes", "-o"]).splitlines()]
    for node in sorted(nodes, key=lambda item: item.get("NodeName", "")):
        name = node.get("NodeName", "")
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name) or not spare(node, *shape):
            continue
        if not preview_safe(command(preview_arguments(name, shape)), name):
            continue
        command(["scontrol", "update", f"JobId={job_id}", f"ReqNodeList={name}"])
        rebound = fields(command(["scontrol", "show", "job", "-o", job_id]))
        current = fields(command(["scontrol", "show", "node", "-o", name]))
        # Recheck the exact binding, held request and capacity immediately before
        # releasing. Do not replace an existing allocation or change its shape.
        if (not valid_job(rebound, job_id, shape, os.getuid() if uid is None else uid)
                or rebound.get("JobState") != "PENDING" or rebound.get("Reason") != "JobHeldUser"
                or rebound.get("Priority") != "0" or rebound.get("ReqNodeList") != name
                or not spare(current, *shape)
                or not preview_safe(command(preview_arguments(name, shape)), name)):
            return {"status": "waiting_spare_capacity"}
        command(["scontrol", "release", job_id])
        return {"status": "released", "node": name}
    return {"status": "waiting_spare_capacity"}


def refresh_active(job_id, previous, command):
    """Keep remaining requests held until the released allocation is terminal."""
    try:
        record = fields(command(["scontrol", "show", "job", "-o", job_id]))
        if record.get("JobId") != job_id:
            raise ValueError("Scheduler returned an unexpected job")
        slurm_state = record.get("JobState")
    except (OSError, ValueError, RuntimeError):
        # scontrol eventually forgets completed jobs; consult only this ID's
        # allocation accounting. Missing or ambiguous state remains blocking.
        rows = command(["sacct", "--noheader", "--parsable2", "--allocations", "--jobs", job_id,
                        "--format=JobIDRaw,State"])
        matching = [line.strip().split("|") for line in rows.splitlines()
                    if line.strip().split("|", 1)[0] == job_id]
        if len(matching) != 1 or len(matching[0]) < 2:
            raise ValueError("Released benchmark has no authoritative allocation state")
        slurm_state = matching[0][1].split(" ", 1)[0].rstrip("+")
    return {**previous, "status": "terminal" if slurm_state in TERMINAL_SLURM else previous["status"],
            "scheduler_state": slurm_state}


def supervise(run_dir, job_ids, *, once=False, max_days=7, poll_seconds=60,
              command=scheduler_command, clock=time.time, sleep=time.sleep):
    if not 0 < max_days <= 7 or not 30 <= poll_seconds <= 60:
        raise ValueError("Require a 30–60 second poll and a budget of at most seven days")
    if not job_ids or len(job_ids) > 4 or len(set(job_ids)) != len(job_ids) or any(
            not re.fullmatch(r"[0-9]+", item) for item in job_ids):
        raise ValueError("Require one to four explicit numeric benchmark job IDs")
    run_dir.mkdir(parents=True, exist_ok=True)
    with (run_dir / "admission.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        path = run_dir / "admission_state.json"
        previous = report.read_json(path) if path.exists() else {}
        if previous and previous.get("job_ids") != sorted(job_ids):
            raise ValueError("Persisted admission allowlist differs; do not reuse or reset its budget")
        started = previous.get("started_epoch", clock())
        deadline = min(previous.get("deadline_epoch", started + max_days * 86400), started + max_days * 86400)
        state = {**previous, "job_ids": sorted(job_ids), "started_epoch": started, "deadline_epoch": deadline,
                 "jobs": previous.get("jobs", {job_id: {"status": "waiting_spare_capacity"} for job_id in job_ids})}
        while True:
            now = clock()
            expired = now >= deadline
            blocked = False
            if not expired:
                # Admit one allocation at a time: released-but-pending work also
                # blocks all remaining requests, preserving the eight-GPU cap.
                for job_id in job_ids:
                    current = state["jobs"].get(job_id, {})
                    if current.get("status") in ACTIVE:
                        try:
                            state["jobs"][job_id] = refresh_active(job_id, current, command)
                        except (OSError, ValueError, RuntimeError) as error:
                            state["jobs"][job_id] = {**current, "error_type": type(error).__name__}
                        blocked |= state["jobs"][job_id]["status"] in ACTIVE
                for job_id in job_ids:
                    if blocked:
                        break
                    if state["jobs"].get(job_id, {}).get("status") in DONE:
                        continue
                    try:
                        launch = report.read_json(run_dir / f"launch_{job_id}.json")
                        if str(launch.get("job_id")) != job_id:
                            raise ValueError("Manifest ID mismatch")
                        state["jobs"][job_id] = attempt(job_id, launch, command)
                        if state["jobs"][job_id]["status"] in ACTIVE | {"invalid_request"}:
                            break
                    except (OSError, ValueError, RuntimeError) as error:
                        state["jobs"][job_id] = {"status": "check_failed", "error_type": type(error).__name__}
            done = all(state["jobs"].get(job_id, {}).get("status") in DONE for job_id in job_ids)
            invalid = any(item.get("status") == "invalid_request" for item in state["jobs"].values())
            state.update(checked_at_pst=timestamp(now), checked_epoch=now,
                         supervisor_status="stopped" if expired or done or invalid else "watching",
                         stop_reason="admission_runtime_limit" if expired else "invalid_request" if invalid
                         else "all_requests_handled" if done else None)
            report.write_json(path, state)
            with (run_dir / "admission_history.jsonl").open("a") as history:
                history.write(json.dumps(state, sort_keys=True) + "\n")
            if once or expired or done or invalid:
                return state
            sleep(min(poll_seconds, max(0, deadline - clock())))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, default=report.ROOT / report.DEFAULT_RUN)
    parser.add_argument("--job-ids", nargs="+", required=True)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--max-days", type=float, default=7)
    parser.add_argument("--poll-seconds", type=float, default=60)
    args = parser.parse_args()
    if not 0 < args.max_days <= 7 or not 30 <= args.poll_seconds <= 60:
        parser.error("Require a 30–60 second poll and a budget of at most seven days")
    try:
        state = supervise(args.run_dir, args.job_ids, once=args.once,
                          max_days=args.max_days, poll_seconds=args.poll_seconds)
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f"Admission supervisor failed: {type(error).__name__}: {error}\n")
    print(json.dumps(state), flush=True)


if __name__ == "__main__":
    main()
