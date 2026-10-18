import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("throughput_watch", SCRIPTS / "watch_training_throughput.py")
watcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(watcher)


class Clock:
    def __init__(self):
        self.now = 0

    def time(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class ThroughputWatchTests(unittest.TestCase):
    def make_run(self, directory, setup="ready_jobs_released", status="queued"):
        root = Path(directory)
        run = root / "run"
        run.mkdir()
        (run / "setup_state.json").write_text(json.dumps({"stage": setup}))
        (run / "launch_241120.json").write_text(json.dumps({
            "job_id": "241120", "status": status, "requested_gpus": 1,
            "target_gpu": "A100", "runtime_validated": True,
        }))
        return root, run

    def test_scheduler_cancellation_beats_stale_queue_or_initializing_result(self):
        self.assertEqual(watcher.observed_status({"status": "queued"}, {"state": "CANCELLED"}, None), "cancelled")
        self.assertEqual(watcher.observed_status({"status": "running"}, {"state": "CANCELLED"},
                                                 {"status": "initializing"}), "cancelled")
        self.assertEqual(watcher.observed_status({"status": "queued"}, {"state": "TIMEOUT"},
                                                 {"status": "completed"}), "failed")

    def test_queue_and_accounting_only_include_allowlisted_allocations(self):
        calls = []
        def command(arguments):
            calls.append(arguments)
            if arguments[0] == "squeue":
                return "241120|RUNNING|None\n999999|RUNNING|None\n"
            return "241120|PENDING|0:0\n241122|CANCELLED by 123|0:15\n241122.batch|FAILED|1:0\n"
        states, errors = watcher.query_scheduler(["241120", "241122"], command)
        self.assertEqual(errors, [])
        self.assertEqual(set(states), {"241120", "241122"})
        self.assertEqual(states["241120"]["state"], "RUNNING")
        self.assertEqual(states["241122"]["state"], "CANCELLED")
        for arguments in calls:
            self.assertIn("241120,241122", arguments)
        with self.assertRaises(ValueError):
            watcher.query_scheduler(["241120;other"], command)

    def test_scheduler_outage_is_explicit_not_a_fresh_observation(self):
        def failed(arguments):
            raise RuntimeError("unavailable")
        states, errors = watcher.query_scheduler(["241120"], failed)
        self.assertEqual(states, {})
        self.assertEqual({item["source"] for item in errors}, {"sacct", "squeue"})
        with tempfile.TemporaryDirectory() as directory:
            root, run = self.make_run(directory)
            snapshot = watcher.collect_snapshot(run, root, 100, query=lambda ids: (states, errors))
            self.assertFalse(snapshot["jobs"][0]["scheduler_observed"])
            self.assertEqual(snapshot["scheduler_errors"], errors)

    def test_pending_running_and_cancellation_rewrite_only_named_launch(self):
        with tempfile.TemporaryDirectory() as directory:
            root, run = self.make_run(directory)
            unrelated = run / "unrelated.json"
            unrelated.write_text('{"job_id":"999999","status":"queued"}')
            for slurm, expected in (("PENDING", "queued"), ("RUNNING", "running"), ("CANCELLED", "cancelled")):
                snapshot = watcher.collect_snapshot(run, root, 100,
                    query=lambda ids: ({"241120": {"state": slurm, "source": "sacct"}}, []))
                self.assertEqual(snapshot["jobs"][0]["status"], expected)
                updated = json.loads((run / "launch_241120.json").read_text())
                self.assertEqual(updated["status"], expected)
                self.assertTrue(updated["runtime_validated"])
            self.assertEqual(json.loads(unrelated.read_text())["status"], "queued")

    def test_result_success_requires_completed_measurement_and_completed_allocation(self):
        self.assertEqual(watcher.observed_status({}, {"state": "COMPLETED"}, None), "failed")
        self.assertEqual(watcher.observed_status({}, {"state": "COMPLETED"}, {"status": "completed"}), "success")
        self.assertEqual(watcher.observed_status({}, {"state": "RUNNING"}, {"status": "completed"}), "running")

    def test_last_terminal_scheduler_failure_survives_an_accounting_outage(self):
        with tempfile.TemporaryDirectory() as directory:
            root, run = self.make_run(directory)
            output = run / "job_241120" / "results.json"
            output.parent.mkdir()
            output.write_text(json.dumps({"status": "initializing"}))
            watcher.collect_snapshot(run, root, 100,
                query=lambda ids: ({"241120": {"state": "TIMEOUT", "source": "sacct"}}, []))
            snapshot = watcher.collect_snapshot(run, root, 130,
                query=lambda ids: ({}, [{"source": "sacct", "error_type": "RuntimeError"}]))
            self.assertEqual(snapshot["jobs"][0]["status"], "failed")
            self.assertFalse(snapshot["jobs"][0]["scheduler_observed"])
            self.assertEqual(json.loads((run / "launch_241120.json").read_text())["slurm_state"], "TIMEOUT")

    def test_hourly_unchanged_waiting_and_immediate_terminal_publication(self):
        with tempfile.TemporaryDirectory() as directory:
            root, run = self.make_run(directory)
            clock, published = Clock(), []
            def query(ids):
                state = "CANCELLED" if clock.now >= 3630 else "PENDING"
                return {"241120": {"state": state, "source": "sacct", "reason": "Resources"}}, []
            def render(*args, **kwargs):
                published.append(clock.now)
                return {"status": "published"}
            state = watcher.watch(run, root / "report", root=root, publish=True,
                clock=clock.time, sleep=clock.sleep, query=query, renderer=render)
            self.assertEqual(published, [0, 3600, 3630])
            self.assertEqual(state["stop_reason"], "all_known_work_terminal")
            self.assertEqual(state["jobs"][0]["status"], "cancelled")
            history = [json.loads(line) for line in (run / "status_history.jsonl").read_text().splitlines()]
            self.assertEqual([entry["checked_epoch"] for entry in history], published)

    def test_running_transition_publishes_immediately_before_hourly_due(self):
        snapshot = {"setup": {"stage": "ready_jobs_released"}, "jobs": [{"job_id": "1", "status": "queued"}]}
        previous = {"last_report_epoch": 10, "last_report_fingerprint": watcher.meaningful_fingerprint(snapshot)}
        self.assertFalse(watcher.publication_due(previous, snapshot, 30))
        snapshot["jobs"][0]["status"] = "running"
        self.assertTrue(watcher.publication_due(previous, snapshot, 30))

    def test_terminal_setup_failure_without_any_submitted_job_publishes_then_stops(self):
        with tempfile.TemporaryDirectory() as directory:
            root, run = self.make_run(directory, setup="setup_failed")
            (run / "launch_241120.json").unlink()
            publications = []
            state = watcher.watch(run, root / "report", root=root,
                clock=lambda: 0, sleep=lambda _: self.fail("Terminal setup must not sleep"),
                query=lambda ids: ({}, []),
                renderer=lambda *args, **kwargs: publications.append(1) or {"status": "rendered"})
            self.assertEqual(publications, [1])
            self.assertEqual(state["watcher_status"], "stopped")

    def test_failed_publication_is_retried_at_bounded_cadence(self):
        snapshot = {"setup": {}, "jobs": []}
        previous = {"last_report_error": {"error_type": "RuntimeError"}, "last_report_attempt_epoch": 0,
                    "last_report_fingerprint": watcher.meaningful_fingerprint(snapshot)}
        self.assertFalse(watcher.publication_due(previous, snapshot, 30))
        self.assertTrue(watcher.publication_due(previous, snapshot, 300))

    def test_terminal_publication_failure_retries_before_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            root, run = self.make_run(directory, setup="setup_failed")
            (run / "launch_241120.json").unlink()
            clock, attempts = Clock(), []
            def render(*args, **kwargs):
                attempts.append(clock.now)
                if len(attempts) == 1:
                    raise RuntimeError("Temporary publication error")
                return {"status": "published"}
            state = watcher.watch(run, root / "report", root=root,
                clock=clock.time, sleep=clock.sleep, query=lambda ids: ({}, []), renderer=render)
            self.assertEqual(attempts, [0, 300])
            self.assertEqual(state["watcher_status"], "stopped")
            self.assertIsNone(state["last_report_error"])

    def test_watch_has_persistent_deadline_and_does_not_extend_on_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            root, run = self.make_run(directory)
            clock = Clock()
            watcher.report.write_json(run / "status.json", {"watcher_started_epoch": 0, "watcher_deadline_epoch": 60})
            state = watcher.watch(run, root / "report", root=root,
                clock=clock.time, sleep=clock.sleep,
                query=lambda ids: ({"241120": {"state": "PENDING", "source": "squeue"}}, []),
                renderer=lambda *args, **kwargs: {"status": "rendered"})
            self.assertEqual(clock.now, 60)
            self.assertEqual(state["watcher_deadline_epoch"], 60)
            self.assertEqual(state["stop_reason"], "watcher_runtime_limit")

    def test_duplicate_watchers_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            with watcher.watcher_lock(run):
                with self.assertRaises(RuntimeError):
                    with watcher.watcher_lock(run):
                        self.fail("Second watcher acquired lock")


if __name__ == "__main__":
    unittest.main()
