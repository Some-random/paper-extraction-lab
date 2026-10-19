import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import report_paper_collection as report
import watch_paper_collection as monitor


class PaperCollectionReportingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.run = self.root / "experiments" / report.DEFAULT
        self.public = self.root / "reports" / report.DEFAULT
        self.run.mkdir(parents=True)
        self.config = {"run_id": report.DEFAULT, "target_new_papers": 10000,
                       "source_catalog": "/dfs/another_user/private/catalog.json",
                       "inventory": {"native_xml_papers": 28623, "known_pmcids": 144000},
                       "limits": {"runtime_seconds": 86400, "network_bytes": 8 * 2**30,
                                  "new_artifact_bytes": 32 * 2**30, "minimum_free_bytes": 64 * 2**30}}
        self.config_path = self.root / "config.json"
        report.write_json(self.config_path, self.config)
        report.write_json(self.run / "launch.json", {"job_id": "12345", "submitted_at_pst": report.timestamp(100),
                                                     "private_path": "/dfs/another_user/launch"})

    def worker(self, status="running", updated=1000, **extra):
        value = {"status": status, "updated_at_pst": report.timestamp(updated),
                 "stage": "process_reused_xml", "reused_processed_papers": 10, "new_selected_papers": 0,
                 "counts": {"raw_tokens": 10000, "exact_unique_tokens": 9000, "selected_tokens": 8000,
                            "selected_exact_unique_tokens": 7000},
                 "events": {"known_pmcid_skips": 12, "known_secondary_identifier_skips": 3},
                 "known_identifier_counts": {"pmcid": 144321},
                 "input_statuses": {"catalog": {"rejected": 2}, "candidates": {"rejected": 3}},
                 "new_artifact_bytes": 4096, "network_bytes": 2000, "network_charged_bytes": 4000,
                 "host": "private-owner-machine", "source_path": "/dfs/another_user/private.xml",
                 "traceback": "private raw traceback", "error_message": "problem at /dfs/private"}
        value.update(extra)
        report.write_json(self.run / "summary.json", value)

    def snapshot(self, state="RUNNING", now=1020, previous=None):
        return report.collect_snapshot(self.config, self.run, now,
                                       query=lambda job: ({"state": state, "source": "squeue"}, []), previous=previous)

    def test_queued_overrides_stale_worker_and_has_no_processing_claim(self):
        self.worker(status="complete", updated=1)
        snapshot = self.snapshot("PENDING")
        self.assertEqual(snapshot["status"], "queued")
        self.assertEqual(snapshot["scheduler_state"], "PENDING")

    def test_dead_worker_is_visible_while_allocation_survives(self):
        self.worker(updated=1000)
        snapshot = self.snapshot(now=1300)
        self.assertEqual(snapshot["status"], "stalled")
        self.assertEqual(snapshot["reason"], "worker_heartbeat_stale")

    def test_missing_first_heartbeat_gets_bounded_startup_grace(self):
        self.assertEqual(self.snapshot(now=1000)["status"], "running")
        self.assertEqual(self.snapshot(now=1200, previous={"first_running_epoch": 1000})["status"], "stalled")

    def test_scheduler_failure_overrides_completed_worker(self):
        self.worker(status="complete")
        self.assertEqual(self.snapshot("OUT_OF_MEMORY")["status"], "failed")
        self.assertEqual(self.snapshot("CANCELLED")["status"], "stopped")

    def test_success_requires_final_worker_status(self):
        self.worker()
        self.assertEqual(self.snapshot("COMPLETED")["reason"], "worker_final_status_missing")
        self.worker(status="complete")
        self.assertEqual(self.snapshot("COMPLETED")["status"], "completed")

    def test_public_schema_omits_private_paths_and_preserves_separate_counts(self):
        self.worker()
        snapshot = self.snapshot()
        snapshot["last_report_error"] = {"message": "/dfs/private/git-credentials"}
        report.build_report(self.config_path, self.run, self.public, snapshot=snapshot)
        rendered = "\n".join(path.read_text() for path in self.public.iterdir())
        for private in ("/dfs/", "private-owner-machine", "traceback", "git-credentials", "another_user"):
            self.assertNotIn(private, rendered)
        public = report.read_json(self.public / "summary.json")
        self.assertEqual(public["counts"]["raw_tokens"], 10000)
        self.assertEqual(public["counts"]["exact_unique_tokens"], 9000)
        self.assertEqual(public["counts"]["selected_exact_unique_tokens"], 7000)
        self.assertEqual(public["counts"]["known_id_skips"], 15)
        self.assertEqual(public["counts"]["rejected_papers"], 5)
        self.assertEqual(public["counts"]["known_pmcids"], 144321)
        self.assertEqual(public["counts"]["network_bytes"], 2000)
        self.assertEqual(public["counts"]["network_charged_bytes"], 4000)

    def test_unknown_scheduler_does_not_invent_a_queued_or_running_state(self):
        self.worker()
        snapshot = report.collect_snapshot(self.config, self.run, 1100, query=lambda job: ({}, []))
        self.assertEqual(snapshot["status"], "stalled")
        self.assertFalse(snapshot["scheduler_observed"])
        self.assertEqual(snapshot["reason"], "scheduler_unavailable")

    def test_terminal_scheduler_observation_survives_accounting_outage(self):
        self.worker(status="complete")
        snapshot = report.collect_snapshot(self.config, self.run, 1100, query=lambda job: ({}, []),
                                           previous={"scheduler_state": "FAILED", "status": "failed", "reason": "failed"})
        self.assertEqual(snapshot["status"], "failed")

    def test_report_is_due_hourly_even_without_change_and_promptly_on_failure(self):
        self.worker()
        snapshot = self.snapshot("PENDING")
        previous = {"last_report_epoch": 1000, "last_report_fingerprint": monitor.meaningful_fingerprint(snapshot)}
        self.assertFalse(monitor.publication_due(previous, snapshot, 4599))
        self.assertTrue(monitor.publication_due(previous, snapshot, 4600))
        snapshot["status"] = "failed"
        self.assertTrue(monitor.publication_due(previous, snapshot, 1001))

    def test_hourly_gains_compare_successful_reports_instead_of_last_poll(self):
        self.worker()
        current, rendered = [1000], []
        def sleep(seconds):
            current[0] += seconds
            self.worker(updated=current[0], reused_processed_papers=10 + int((current[0] - 1000) / 60))
        def renderer(*args, **kwargs):
            rendered.append(kwargs["snapshot"].copy())
            return report.build_report(*args, **kwargs)
        result = monitor.watch(self.config_path, self.run, self.public, clock=lambda: current[0],
                               sleep=sleep, max_hours=1, query=lambda job: ({"state": "RUNNING"}, []), renderer=renderer)
        self.assertEqual(len(rendered), 2)
        self.assertEqual(rendered[0]["status"], rendered[1]["status"])
        self.assertEqual(rendered[1]["since_previous_report"]["reused_papers"], 60)
        self.assertEqual(result["last_report_counts"]["reused_papers"], 70)
        self.assertIn("+60 existing papers", (self.public / "README.md").read_text())
        self.assertIn("+60 existing papers", (self.public / "progress.md").read_text())

    def test_artifact_delta_can_be_negative_after_temporary_files_are_removed(self):
        self.assertEqual(monitor.report_deltas({"artifact_bytes": 100}, {"artifact_bytes": 80}), {"artifact_bytes": -20})

    def test_watch_resume_preserves_original_deadline(self):
        self.worker()
        report.write_json(self.run / "watcher_status.json", {"watcher_started_epoch": 1, "watcher_deadline_epoch": 1000})
        rendered = []
        result = monitor.watch(self.config_path, self.run, self.public, clock=lambda: 2000,
                               query=lambda job: ({"state": "PENDING"}, []),
                               renderer=lambda *args, **kwargs: rendered.append(kwargs["snapshot"].copy()) or {"status": "rendered"})
        self.assertEqual(result["watcher_deadline_epoch"], 1000)
        self.assertEqual(result["monitor_stop_reason"], "monitor_runtime_limit")
        self.assertEqual(result["status"], "queued")
        self.assertEqual(len(rendered), 1)

    def test_final_publication_failure_retries_instead_of_losing_final_report(self):
        self.worker(status="complete")
        current, attempts = [1000], []
        def renderer(*args, **kwargs):
            attempts.append(current[0])
            return {"status": "failed" if len(attempts) == 1 else "published"}
        result = monitor.watch(self.config_path, self.run, self.public, clock=lambda: current[0],
                               sleep=lambda seconds: current.__setitem__(0, current[0] + seconds),
                               query=lambda job: ({"state": "COMPLETED"}, []), renderer=renderer)
        self.assertEqual(attempts, [1000, 1300])
        self.assertEqual(result["status"], "completed")
        self.assertIsNone(result["last_report_error"])

    def test_corrupt_initial_worker_file_still_yields_a_final_safe_report(self):
        (self.run / "summary.json").write_text("{broken json")
        report.write_json(self.run / "watcher_status.json", {"watcher_started_epoch": 1, "watcher_deadline_epoch": 1000})
        result = monitor.watch(self.config_path, self.run, self.public, clock=lambda: 2000,
                               query=lambda job: ({"state": "RUNNING"}, []))
        self.assertEqual(result["status"], "stalled")
        self.assertEqual(report.read_json(self.public / "summary.json")["error_type"], "JSONDecodeError")


if __name__ == "__main__":
    unittest.main()
