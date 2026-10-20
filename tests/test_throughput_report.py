import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("throughput_report", ROOT / "scripts/report_training_throughput.py")
report = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(report)


class TrainingThroughputReportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.run = self.root / "experiments/training_throughput_2026-10-18"
        self.public = self.root / report.DEFAULT_REPORT
        self.run.mkdir(parents=True)
        self.public.mkdir(parents=True)
        (self.public / "cluster_gpus.json").write_text(json.dumps({
            "checked_at_pst": "2026-10-18T12:00:00-08:00",
            "gpus": {"a100": {"configured": 71, "allocated": 71, "unallocated_online": 0,
                               "unavailable_node": 0}}, "total_configured": 71,
        }))

    def launch(self, job="123", state="queued", gpus=8):
        (self.run / f"launch_{job}.json").write_text(json.dumps({
            "job_id": job, "status": state, "requested_gpus": gpus, "target_gpu": "a100",
            "submitted_at_pst": "2026-10-18T12:00:00-08:00",
            "private_path": "/dfs/scratch0/another_user/secret",
        }))

    def result(self, job="123", status="completed", world_size=1):
        value = {
            "status": status, "world_size": world_size, "actual_parameter_count": 4_000_000_000,
            "arguments": {"model_config": "/dfs/private/config.json", "output": "/dfs/private/out.json",
                          "sequence_length": 4096, "batch_size": 1, "accumulation": 4},
            "hardware": [{"host": "private-owner-machine", "rank": 0, "gpu": "NVIDIA A100",
                          "total_memory_bytes": 80_000_000_000}],
            "throughput": {"input_tokens_per_second": 100_000, "measured_optimizer_steps": 15,
                           "measured_wall_seconds": 2.4576,
                           "extrapolation": {"gpu_count": 1000, "days": 0.0001}},
            "completed_warmup_steps": 5, "traceback": "/dfs/private/traceback.py:12",
            "failure_message": "problem in /dfs/other_user/cache/file.py",
        }
        destination = self.run / f"job_{job}" / "results.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(value))
        return destination

    def build(self):
        return report.build_report(self.run, self.public, self.root)

    def test_queued_has_no_measured_estimate(self):
        self.launch()
        summary = self.build()
        text = (self.public / "README.md").read_text()
        self.assertEqual(summary, {"status": "rendered", "jobs": 1})
        self.assertIn("| 123 | queued | 8 | a100 | — | — |", text)
        self.assertIn("No completed throughput measurement yet", text)
        self.assertFalse((self.public / "results_123.json").exists())

    def test_success_overrides_stale_queued_state_and_uses_actual_gpu_count(self):
        self.launch(gpus=8)
        self.result(world_size=1)
        self.build()
        text = (self.public / "README.md").read_text()
        self.assertIn("| 123 | success | 1 | NVIDIA A100 | 100,000 | 23.15 days |", text)
        self.assertNotIn("No completed throughput measurement yet", text)
        result = json.loads((self.public / "results_123.json").read_text())
        self.assertEqual(result["throughput"]["extrapolation"]["gpu_count"], 1)
        self.assertAlmostEqual(result["throughput"]["extrapolation"]["days"], 200_000_000_000 / 100_000 / 86400)

    def test_public_outputs_omit_paths_hostnames_and_private_failure_text(self):
        self.launch()
        self.result()
        self.build()
        text = "\n".join(path.read_text() for path in self.public.iterdir())
        for private in ("/dfs/", "private-owner-machine", "other_user", "traceback.py", "private_path"):
            self.assertNotIn(private, text)
        result = json.loads((self.public / "results_123.json").read_text())
        self.assertNotIn("model_config", result["arguments"])
        self.assertNotIn("host", result["hardware"][0])
        self.assertNotIn("traceback", result)
        self.assertNotIn("failure_message", result)

    def test_failed_output_does_not_project_stale_throughput(self):
        self.launch(state="running")
        path = self.result(status="failed")
        result = json.loads(path.read_text())
        result["failure_type"] = "OutOfMemoryError"
        path.write_text(json.dumps(result))
        self.build()
        text = (self.public / "README.md").read_text()
        self.assertIn("failed — OutOfMemoryError", text)
        self.assertNotIn("23.15 days", text)
        public = json.loads((self.public / "results_123.json").read_text())
        self.assertNotIn("extrapolation", public["throughput"])

    def test_partial_runtime_limit_remains_explicit_failure(self):
        self.launch()
        self.result(status="runtime_limit")
        self.build()
        text = (self.public / "README.md").read_text()
        self.assertIn("failed — time limit; partial measurement", text)
        self.assertIn("23.15 days (partial)", text)

    def test_launch_failed_without_results(self):
        self.launch(state="failed")
        self.build()
        self.assertIn("| 123 | failed | 8 | a100 | — | — |", (self.public / "README.md").read_text())

    def test_cancelled_is_not_resurrected_by_initializing_output(self):
        self.launch(state="cancelled")
        self.result(status="initializing")
        self.build()
        self.assertIn("| 123 | cancelled |", (self.public / "README.md").read_text())

    def test_scheduler_failure_overrides_completed_result(self):
        self.launch(state="failed")
        path = self.run / "launch_123.json"
        launch = json.loads(path.read_text())
        launch.update(slurm_state="TIMEOUT", scheduler_observed=True)
        path.write_text(json.dumps(launch))
        self.result()
        self.build()
        self.assertIn("| 123 | failed |", (self.public / "README.md").read_text())

    def test_monitor_and_setup_failure_are_visible_without_private_details(self):
        self.launch(state="cancelled")
        (self.run / "setup_state.json").write_text(json.dumps({
            "stage": "setup_failed", "error_type": "TimeoutExpired", "error": "/dfs/private/error"}))
        (self.run / "status.json").write_text(json.dumps({
            "checked_at_pst": "2026-10-18T12:45:00-08:00", "watcher_status": "stopped",
            "setup": {"stage": "setup_failed", "error_type": "TimeoutExpired"},
            "scheduler_errors": [{"source": "squeue", "error_type": "RuntimeError", "error": "/dfs/private"}],
            "jobs": [{"job_id": "123", "status": "cancelled", "reason": "private-hostname"}],
            "private_path": "/dfs/private",
        }))
        self.build()
        text = (self.public / "README.md").read_text()
        self.assertIn("setup_failed (TimeoutExpired)", text)
        self.assertIn("Scheduler query incomplete", text)
        self.assertIn("[Status snapshot](status.json)", text)
        public = (self.public / "status.json").read_text()
        self.assertNotIn("/dfs/", public)
        self.assertNotIn("private-hostname", public)

    def test_matched_suite_retains_profile_failures_and_admission_status(self):
        self.launch(state="queued", gpus=2)
        launch_path = self.run / "launch_123.json"
        launch = json.loads(launch_path.read_text())
        launch.update(comparison_group="2b200_vs_8a100", admission_required=True,
                      admission_status="waiting", hold_reason="Waiting for spare capacity")
        launch_path.write_text(json.dumps(launch))
        self.build()
        self.assertIn("waiting for spare capacity", (self.public / "README.md").read_text())
        launch.update(status="completed", admission_status="released")
        launch.pop("hold_reason")
        launch_path.write_text(json.dumps(launch))
        path = self.result(world_size=2)
        value = json.loads(path.read_text())
        value['suite'] = {'status':'completed', 'selected_profile':'micro_1', 'private_path':'/dfs/private',
                          'profiles':[{'microbatch_per_gpu':1,'accumulation':16,'status':'completed',
                                       'input_tokens_per_second':100000},
                                      {'microbatch_per_gpu':4,'accumulation':4,'status':'failed',
                                       'failure_type':'OutOfMemoryError','traceback':'/dfs/private'}]}
        path.write_text(json.dumps(value))
        self.build()
        text = (self.public / "README.md").read_text()
        self.assertIn("131,072 input tokens per optimizer", text)
        self.assertIn("failed — OutOfMemoryError", text)
        self.assertIn("| 1 | 16 | completed | 100,000 |", text)
        public = (self.public / "results_123.json").read_text()
        self.assertNotIn("/dfs/", public)
        self.assertNotIn("traceback", public)

    def test_launch_completed_without_results_is_not_a_measurement(self):
        self.launch(state="completed")
        self.build()
        self.assertIn("| 123 | failed | 8 | a100 | — | — |", (self.public / "README.md").read_text())

    def verification_result(self, state="completed", scheduler_state=None):
        self.launch(job="124", state=state, gpus=2)
        launch_path = self.run / "launch_124.json"
        launch = json.loads(launch_path.read_text())
        launch.update(target_gpu="b200", comparison_group=report.VERIFICATION_GROUP)
        if scheduler_state:
            launch.update(status="failed", slurm_state=scheduler_state, scheduler_observed=True)
        launch_path.write_text(json.dumps(launch))
        path = self.result(job="124", world_size=2)
        result = json.loads(path.read_text())
        baseline = {
            "name": "baseline", "role": "baseline", "status": "completed", "exit_code": 0,
            "activation_checkpointing": "on", "sharding": "full_shard",
            "microbatch_per_gpu": 4, "accumulation": 4, "input_tokens_per_second": 100_000,
            "setup_seconds": 20., "warmup_seconds": 10., "measurement_seconds": 2.4576,
            "phase_timings": [{"stage": "setup_complete", "rank": 0, "elapsed_seconds": 20.,
                               "host": "private-owner-machine", "path": "/dfs/private/phase"}],
            "profiler": {"status": "completed", "elapsed_seconds": 4.,
                         "trace_path": "/dfs/private/profile", "host": "private-owner-machine",
                         "operators": [{"name": "aten::_scaled_dot_product_flash_attention",
                                        "categories": ["attention"], "device_total_us": 10.,
                                        "host": "private-owner-machine", "path": "/dfs/private/operator"}],
                         "cuda_kernels": [{"name": "flash_fwd_kernel", "device_total_us": 8.,
                                           "host": "private-owner-machine"}]},
        }
        tuned = {"name": "tuned_micro8", "role": "tuning", "status": "completed", "exit_code": 0,
                 "activation_checkpointing": "off", "sharding": "shard_grad_op",
                 "microbatch_per_gpu": 8, "accumulation": 2, "input_tokens_per_second": 200_000}
        failed = {"name": "failed_tuned", "role": "tuning", "status": "failed", "exit_code": 1,
                  "input_tokens_per_second": 999_999, "failure_type": "ProfileTimeout",
                  "phase_timings": [{"stage": "first_forward_start", "elapsed_seconds": 30.}]}
        result.update(setup_seconds=20., warmup_seconds=10., measurement_seconds=2.4576,
                      arguments={**result["arguments"], "activation_checkpointing": "on",
                                 "sharding": "full_shard", "profile_steps": 1},
                      suite={"mode": "verification", "profiles": [baseline, tuned, failed],
                             "baseline_result": baseline, "fastest_completed_profile": tuned,
                             "tuning_speedup_over_baseline": 2.})
        path.write_text(json.dumps(result))
        return path

    def test_verification_keeps_baseline_tuning_and_old_comparison_distinct(self):
        self.launch(job="123", gpus=8)
        launch_path = self.run / "launch_123.json"
        launch = json.loads(launch_path.read_text())
        launch["comparison_group"] = "gpu_allocation_comparison"
        launch_path.write_text(json.dumps(launch))
        self.verification_result()
        self.build()
        text = (self.public / "README.md").read_text()
        self.assertLess(text.index("## Throughput verification"), text.index("## Matched GPU allocation comparison"))
        self.assertIn("| 124 / 2 × b200 | success | 100,000 | 200,000 |", text)
        self.assertIn("| 8 × a100 | queued |", text)
        self.assertIn("Only baseline-to-baseline measurements", text)
        self.assertIn("A timeout provides no training-speed ranking", text)
        self.assertIn("| baseline / baseline | on / full_shard | 4 × 4 | completed | 100,000 | 20.00 | 10.00 | 2.46 | 4.00 |", text)
        self.assertIn("first_forward_start", text)
        self.assertNotIn("| success | 100,000 | 999,999 |", text)
        public = json.loads((self.public / "results_124.json").read_text())
        self.assertEqual(public["throughput"]["input_tokens_per_second"], 100_000)
        self.assertEqual(public["suite"]["fastest_completed_profile"]["input_tokens_per_second"], 200_000)

    def test_verification_failure_cannot_win_and_nested_diagnostics_are_safe(self):
        self.verification_result(scheduler_state="TIMEOUT")
        self.build()
        text = (self.public / "README.md").read_text()
        self.assertIn("| 124 / 2 × b200 | failed | — | — |", text)
        self.assertIn("observed attention operators: `aten::_scaled_dot_product_flash_attention`", text)
        self.assertIn("observed CUDA kernels: `flash_fwd_kernel`", text)
        public_text = "\n".join(path.read_text() for path in self.public.iterdir())
        for private in ("/dfs/", "private-owner-machine", "trace_path", '"host"', '"path"'):
            self.assertNotIn(private, public_text)
        public = json.loads((self.public / "results_124.json").read_text())
        self.assertEqual(public["arguments"]["profile_steps"], 1)
        self.assertEqual(public["suite"]["baseline_result"]["setup_seconds"], 20.)

    def test_setup_no_job_is_explicit(self):
        (self.run / "setup_state.json").write_text(json.dumps({"stage": "installing_isolated_runtime"}))
        self.build()
        self.assertIn("Setup, no GPU job submitted", (self.public / "README.md").read_text())

    def test_optimization_features_budget_and_completed_winner_remain_explicit(self):
        baseline = {"name": "baseline", "role": "baseline", "status": "completed", "exit_code": 0,
                    "input_tokens_per_second": 14000, "features": {"attention": "sdpa_auto", "precision": "bf16"}}
        fast = {"name": "native_fp8", "role": "tuning", "parent": "baseline", "status": "completed",
                "exit_code": 0, "input_tokens_per_second": 21000,
                "peak_cuda_allocated_bytes": 64 * 1024 ** 3,
                "features": {"attention": "flash_attn4", "precision": "mxfp8", "private_path": "/dfs/private"}}
        failed = {"name": "oom", "status": "failed", "exit_code": 1,
                  "input_tokens_per_second": 999999, "failure_type": "OutOfMemoryError"}
        result = report.sanitize_result({"suite": {"profiles": [baseline, fast, failed]}}, "222")
        job = {"job_id": "222", "status": "success", "comparison_group": report.OPTIMIZATION_GROUP,
               "requested_gpus": 2, "target_gpu": "B200", "result": result}
        text = "\n".join(report.render_optimization([job]))
        self.assertIn("two hours / four GPU-hours", text)
        self.assertIn("**native_fp8**", text)
        self.assertIn("**1.50×**", text)
        self.assertIn("flash_attn4 / mxfp8", text)
        self.assertIn("64.00", text)
        self.assertNotIn("999,999", text)
        self.assertNotIn("private_path", json.dumps(result))
        job["status"] = "failed"
        self.assertNotIn("Fastest completed profile:", "\n".join(report.render_optimization([job])))

    def test_optimization_queue_has_no_invented_measurement(self):
        text = "\n".join(report.render_optimization([{"job_id": "222", "status": "queued",
            "comparison_group": report.OPTIMIZATION_GROUP, "requested_gpus": 2, "target_gpu": "B200"}]))
        self.assertIn("No profile measurements are available yet", text)
        self.assertNotIn("Fastest completed profile:", text)

    def test_invalid_job_id_cannot_write_arbitrary_public_file(self):
        self.launch(job="123")
        path = self.run / "launch_123.json"
        data = json.loads(path.read_text())
        data["job_id"] = "../../bad"
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "Invalid or missing job ID"):
            self.build()

    def test_default_does_not_publish(self):
        with patch.object(report, "publish") as publisher:
            self.build()
        publisher.assert_not_called()

    def test_public_value_redacts_absolute_and_experiment_paths(self):
        value = "failed at /dfs/scratch0/private/a.py and experiments/private/run.json"
        clean = report.public_value(value)
        self.assertEqual(clean, "failed at [local path] and [local path]")

    def test_publication_only_commits_generated_reports(self):
        remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(remote)],
                       check=True, capture_output=True)

        def git(*args):
            return subprocess.run(["git", *args], cwd=self.root, check=True,
                                  capture_output=True, text=True).stdout.strip()

        git("init", "--initial-branch=main")
        git("config", "user.name", "Test")
        git("config", "user.email", "test@example.invalid")
        other = self.root / "unrelated.txt"
        other.write_text("original\n")
        git("add", ".")
        git("commit", "-m", "Initial")
        git("remote", "add", "origin", str(remote))
        git("push", "-u", "origin", "main")
        other.write_text("staged\n")
        git("add", "unrelated.txt")
        other.write_text("unstaged\n")
        self.launch()
        self.result()
        summary = report.build_report(self.run, self.public, self.root, publish_requested=True)
        self.assertEqual(summary["status"], "published")
        self.assertEqual(git("show", "HEAD:unrelated.txt"), "original")
        self.assertEqual(git("show", ":unrelated.txt"), "staged")
        self.assertEqual(other.read_text(), "unstaged\n")
        changed = set(git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines())
        self.assertEqual(changed, {str(report.DEFAULT_REPORT / "README.md"),
                                   str(report.DEFAULT_REPORT / "results_123.json")})
        self.assertEqual(git("rev-parse", "HEAD"), git("rev-parse", "origin/main"))


if __name__ == "__main__":
    unittest.main()
