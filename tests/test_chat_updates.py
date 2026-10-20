import importlib.util
import errno
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("chat_updates", SCRIPTS / "queue_chat_updates.py")
monitor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(monitor)


class ChatUpdatesTests(unittest.TestCase):
    def setUp(self):
        self.config = {"thread_id": "5cb945eb-3eb8-46ba-b62e-d0842086c4cc", "codex_path": "/bin/codex",
                       "paper_run_directory": "/private/paper", "throughput_run_directory": "/private/gpu",
                       "interval_seconds": 3600, "deadline_epoch": 100000}
        self.observed = {"paper": {"status": "running", "stage": "process_reused_xml", "counts": {"raw_tokens": 100}},
                         "gpu_jobs": [{"job_id": "123", "status": "queued", "scheduler_state": "PENDING"}]}
        self.sent = []

    def send(self, config, prompt):
        self.sent.append(prompt)
        return {"status": "accepted", "exit_code": 0}

    def tick(self, state, now, **kwargs):
        return monitor.tick(self.config, state, self.observed, now, send=self.send, **kwargs)

    def test_hourly_cadence_survives_restart_without_minute_backlog(self):
        state = self.tick({}, 0)
        for now in (60, 600, 3599):
            state = self.tick(json.loads(json.dumps(state)), now)
        self.assertEqual(self.sent, [])
        state = self.tick(state, 3600)
        self.assertEqual(state["last_accepted_epoch"], 3600)
        for now in (3601, 3660, 7199):
            state = self.tick(state, now)
        self.assertEqual(len(self.sent), 1)
        state = self.tick(state, 7200)
        self.assertEqual(len(self.sent), 2)

    def test_counter_changes_do_not_flood_but_status_change_is_immediate(self):
        state = self.tick({}, 0)
        self.observed["paper"]["counts"]["raw_tokens"] = 500
        state = self.tick(state, 60)
        self.assertFalse(self.sent)
        self.observed["paper"].update(status="stopped", stop_reason="free_space_floor")
        state = self.tick(state, 120)
        self.assertEqual(state["last_accepted_epoch"], 120)
        self.assertIn("free_space_floor", self.sent[0])

    def test_failure_retries_five_minutes_without_claiming_acceptance(self):
        def fail(*args):
            raise RuntimeError("offline")
        state = monitor.tick(self.config, {}, self.observed, 0, force=True, send=fail)
        self.assertNotIn("last_accepted_epoch", state)
        self.assertIsNotNone(state["pending_fingerprint"])
        state = self.tick(state, 299)
        self.assertFalse(self.sent)
        state = self.tick(state, 300)
        self.assertEqual(len(self.sent), 1)
        self.assertIsNone(state["queue_error"])

    def test_terminal_final_update_must_be_accepted_before_stopping(self):
        self.observed["paper"]["status"] = "stopped"
        self.observed["gpu_jobs"][0]["status"] = "success"
        state = monitor.tick(self.config, {}, self.observed, 0,
                             send=lambda *args: {"status": "unconfirmed", "exit_code": 0})
        self.assertEqual(state["monitor_status"], "watching")
        state = self.tick(state, 300)
        self.assertEqual(state["monitor_status"], "stopped")
        self.assertEqual(state["stop_reason"], "all_work_terminal_final_update_accepted")

    def test_persistent_deadline_cannot_extend_on_restart(self):
        state = self.tick({"started_epoch": 0, "deadline_epoch": 100}, 60)
        self.config["deadline_epoch"] = 999999
        state = self.tick(state, 100)
        self.assertEqual(state["deadline_epoch"], 100)
        self.assertEqual(state["stop_reason"], "monitor_deadline")

    def test_cli_targets_only_exact_existing_thread_and_requires_exit_zero(self):
        process = mock.MagicMock()
        process.__enter__.return_value = process
        process.wait.return_value = 0
        with mock.patch.object(monitor.subprocess, "Popen", return_value=process) as command:
            self.assertEqual(monitor.enqueue(self.config, "status"), {"status": "accepted", "exit_code": 0})
        self.assertEqual(command.call_args.args[0], ["/bin/codex", "queue", "--thread", self.config["thread_id"],
                                                    "--message", "status"])
        process.wait.return_value = 1
        with mock.patch.object(monitor.subprocess, "Popen", return_value=process):
            with self.assertRaises(RuntimeError):
                monitor.enqueue(self.config, "status")

    def test_duplicate_monitor_lock_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with monitor.lock(Path(directory)):
                with self.assertRaises(RuntimeError):
                    with monitor.lock(Path(directory)):
                        self.fail("Duplicate monitor acquired lock")

    def test_snapshot_queries_exact_ids_once_and_does_not_rewrite_manifests(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paper_run, gpu_run = root / "paper", root / "gpu"
            paper_run.mkdir()
            gpu_run.mkdir()
            files = {paper_run / "launch.json": {"job_id": "123", "config_path": "config.json"},
                     paper_run / "summary.json": {"status": "stopped", "stop_reason": "free_space_floor"},
                     gpu_run / "launch_456.json": {"job_id": "456", "status": "queued"},
                     root / "config.json": {"run_id": "test"}}
            for path, value in files.items():
                path.write_text(json.dumps(value))
            before = {str(path): path.read_bytes() for path in files}
            calls = []
            def query(identifiers):
                calls.append(identifiers)
                return {"123": {"state": "COMPLETED"}, "456": {"state": "PENDING"}}, []
            config = {**self.config, "paper_run_directory": str(paper_run), "throughput_run_directory": str(gpu_run)}
            with mock.patch.object(monitor, "ROOT", root):
                observed = monitor.snapshot(config, 10, query=query)
            self.assertEqual(calls, [["123", "456"]])
            self.assertEqual(observed["paper"]["stop_reason"], "free_space_floor")
            self.assertEqual(observed["gpu_jobs"][0]["status"], "queued")
            self.assertEqual(before, {str(path): path.read_bytes() for path in files})

    def test_terminal_restart_does_not_enqueue_again(self):
        self.observed["paper"]["status"] = "stopped"
        self.observed["gpu_jobs"][0]["status"] = "success"
        state = self.tick({}, 0)
        state = self.tick(json.loads(json.dumps(state)), 10)
        self.assertEqual(len(self.sent), 1)
        with self.assertRaises(ValueError):
            self.tick({**state, "thread_id": "another-thread"}, 20)

    def test_large_current_and_previous_profiler_dumps_compact_on_restart(self):
        profiler = {"elapsed_seconds": 24.9,
                    "operators": [{"name": "kernel" * 500, "device_total_us": 123}] * 100,
                    "cuda_kernels": [{"name": "kernel" * 500}] * 100}
        profile = {"name": "baseline", "status": "completed", "input_tokens_per_second": 14521.8,
                   "setup_seconds": 101.4, "warmup_seconds": 36.2, "measurement_seconds": 72.2,
                   "microbatch_per_gpu": 4, "accumulation": 4, "activation_checkpointing": "on",
                   "sharding": "full_shard", "profiler": profiler,
                   "phase_timings": [{"stage": "model_initialize", "host": "private.host"}] * 100,
                   "hardware": [{"host": "private.host"}]}
        self.observed["paper"].update(job_id="242193", deadline_at_pst="2026-10-19T22:28:05-08:00",
                                      counts={"raw_tokens": 342022180, "reused_papers": 17959,
                                              "new_papers": 0, "artifact_bytes": 1947822283,
                                              "network_bytes": 0, "selected_exact_unique_tokens": 203163980})
        self.observed["gpu_jobs"] = [
            {"job_id": str(242250 + number), "gpus": 2, "gpu_type": "B200 180GB", "status": "success",
             "scheduler_state": "COMPLETED", "measurement": {"input_tokens_per_second": 14521.8,
                 "measured_input_tokens": 1048576, "measured_wall_seconds": 72.2,
                 "step_seconds": {"mean": 9.02, "values": [9.0] * 10000}},
             "suite": {"baseline_result": profile, "fastest_completed_profile": profile,
                       "profiles": [profile, {"name": "tuned_micro4", "status": "failed",
                           "failure_type": "OutOfMemoryError", "failure_message": "private.host"}]}}
            for number in range(10)]
        old_state = {"last_accepted_snapshot": self.observed, "last_accepted_epoch": 10,
                     "started_epoch": 0, "deadline_epoch": 100000, "next_due_epoch": 3610,
                     "accepted_count": 1}
        self.assertGreater(len(json.dumps(old_state)), 128 * 1024)
        state = self.tick(old_state, 3610)
        prompt = self.sent[0]
        self.assertLess(len(prompt.encode("utf-8")), 20 * 1024)
        self.assertNotIn("private.host", prompt)
        self.assertNotIn('"profiler"', prompt)
        self.assertNotIn('"phase_timings"', prompt)
        self.assertNotIn('"values"', prompt)
        for label in ("Latest observed status: ", "Previous accepted update observation: "):
            parsed = json.loads(prompt.split(label, 1)[1].split("\n", 1)[0])
            self.assertEqual(parsed["paper"]["counts"], self.observed["paper"]["counts"])
            self.assertEqual(parsed["paper"]["job_id"], "242193")
            self.assertEqual(len(parsed["gpu_jobs"]), 10)
            self.assertEqual(parsed["gpu_jobs"][0]["measurement"]["measured_input_tokens"], 1048576)
            self.assertEqual(parsed["gpu_jobs"][0]["suite"]["baseline_profile"], "baseline")
            self.assertEqual(parsed["gpu_jobs"][0]["suite"]["profiles"][0]["setup_seconds"], 101.4)
            self.assertEqual(parsed["gpu_jobs"][0]["suite"]["profiles"][0]["profiler_seconds"], 24.9)
            self.assertEqual(parsed["gpu_jobs"][0]["suite"]["profiles"][1]["failure_type"], "OutOfMemoryError")
        self.assertEqual(state["accepted_count"], 2)
        self.assertEqual(state["deadline_epoch"], 100000)
        self.assertEqual(state["next_due_epoch"], 7210)
        self.assertLess(len(json.dumps(state)), 40 * 1024)

    def test_prompt_bound_counts_utf8_bytes_and_does_not_send_or_truncate(self):
        self.observed["paper"]["reason"] = "生" * 23000
        state = self.tick({}, 0, force=True)
        self.assertEqual(self.sent, [])
        self.assertNotIn("last_accepted_epoch", state)
        self.assertEqual(state["queue_error"]["error_type"], "PromptTooLargeError")
        self.assertGreater(state["queue_error"]["prompt_bytes"], monitor.MAX_PROMPT_BYTES)
        self.assertEqual(state["queue_error"]["maximum_prompt_bytes"], 65536)
        self.assertEqual(state["observation"]["paper"]["counts"]["raw_tokens"], 100)
        with mock.patch.object(monitor.subprocess, "Popen") as command:
            with self.assertRaises(monitor.PromptTooLargeError):
                monitor.enqueue(self.config, "生" * 23000)
            command.assert_not_called()

    def test_full_optimization_sweep_and_previous_update_fit_chat_payload(self):
        profiles = []
        for index in range(32):
            profiles.append({"name": f"optimized_profile_{index}", "role": "tuning",
                             "status": "completed", "exit_code": 0,
                             "input_tokens_per_second": 14521.807479872334,
                             "microbatch_per_gpu": 4, "accumulation": 4,
                             "setup_seconds": 101.43789654783905,
                             "warmup_seconds": 36.22404126636684,
                             "measurement_seconds": 72.20698948483914,
                             "runtime_seconds": 234.8385501075536,
                             "launcher_wall_seconds": 316.6443138467148,
                             "peak_cuda_allocated_bytes": 66474954240,
                             "peak_cuda_reserved_bytes": 89336578048,
                             "features": {"attention": "flash_attn4", "kernels": "liger_full",
                                          "checkpointing": "selective", "sharding": "fsdp2",
                                          "compile": "on", "precision": "float8_tensorwise",
                                          "float8_all_gather": "on", "optimizer": "adamw_8bit"},
                             "throughput": {"input_tokens_per_second": 14521.807479872334,
                                            "input_tokens_per_step": 131072,
                                            "measured_input_tokens": 1048576,
                                            "measured_optimizer_steps": 8,
                                            "measured_wall_seconds": 72.20698948483914},
                             "profiler": {"operators": [{"name": "private_kernel"}] * 1000}})
        self.observed["gpu_jobs"].append({"job_id": "999", "gpus": 2, "gpu_type": "B200 180GB",
                                          "status": "running", "scheduler_state": "RUNNING",
                                          "suite": {"status": "running", "profiles": profiles}})
        prompt = monitor.message(self.config, self.observed, self.observed)
        self.assertLess(len(prompt.encode()), monitor.MAX_PROMPT_BYTES)
        self.assertNotIn("private_kernel", prompt)
        self.assertIn('"optimizer":"adamw_8bit"', prompt)
        self.assertIn('"name":"optimized_profile_31"', prompt)

    def test_oserror_retains_actionable_errno_without_private_argument(self):
        def fail(*args):
            raise OSError(errno.E2BIG, "Argument list too long", "/private/thread-id")
        state = monitor.tick(self.config, {}, self.observed, 0, force=True, send=fail)
        self.assertEqual(state["queue_error"], {"error_type": "OSError", "errno": errno.E2BIG,
                                               "strerror": "Argument list too long"})
        self.assertNotIn("last_accepted_epoch", state)
        self.assertEqual(state["retry_after_epoch"], 300)


if __name__ == "__main__":
    unittest.main()
