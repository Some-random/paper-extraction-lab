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

    def test_launch_completed_without_results_is_not_a_measurement(self):
        self.launch(state="completed")
        self.build()
        self.assertIn("| 123 | failed | 8 | a100 | — | — |", (self.public / "README.md").read_text())

    def test_setup_no_job_is_explicit(self):
        (self.run / "setup_state.json").write_text(json.dumps({"stage": "installing_isolated_runtime"}))
        self.build()
        self.assertIn("Setup, no GPU job submitted", (self.public / "README.md").read_text())

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
