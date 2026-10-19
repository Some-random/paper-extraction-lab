import importlib.util
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


if __name__ == "__main__":
    unittest.main()
