import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from corpus_progress import ProgressReporter


def snapshot(tokens=100, status="running"):
    counts = {"raw_records": 10, "unique_records": 9, "raw_tokens": tokens, "unique_tokens": tokens - 5}
    return {"run_id": "pilot", "status": status, "totals": counts,
        "current_file": "db_1", "files": {"db_1": {"status": "counting"}},
        "sources": {"biocollection": {"name": "TheBioCollection", "content_category": "database_records", **counts}},
        "content_categories": {"database_records": counts},
        "paper_expansion": {"status": "phase_time_limit"},
        "updated_at_pst": "2026-10-18T08:21:43-08:00", "stop_at_pst": "2026-10-18T08:21:42-08:00",
        "network_body_bytes": 2**30, "new_artifact_bytes": 2 * 2**30, "filesystem_free_bytes": 3 * 2**30}


class CorpusProgressTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.run = Path(self.temporary.name) / "run"
        self.report = Path(self.temporary.name) / "report"
        self.reporter = ProgressReporter(self.run, self.report)

    def events(self):
        return [json.loads(line) for line in (self.run / "progress_events.jsonl").read_text().splitlines()]

    def test_hourly_boundary_uses_last_emission_and_preserves_resume_deltas(self):
        first = self.reporter.emit(snapshot(), now_epoch=10000)
        self.assertEqual(first["kind"], "start")
        self.assertIsNone(first["delta"])
        self.assertIsNone(self.reporter.emit(snapshot(200), now_epoch=13599))
        resumed = ProgressReporter(self.run, self.report)
        hourly = resumed.emit(snapshot(300), now_epoch=13600)
        self.assertEqual(hourly["kind"], "hourly")
        self.assertEqual(hourly["delta"]["unique_tokens"], 200)
        self.assertEqual(hourly["sources"]["biocollection"]["delta_unique_tokens"], 200)
        self.assertEqual(hourly["phase"], "counting")
        self.assertEqual(len(self.events()), 2)
        self.assertIsNone(resumed.emit(snapshot(400), now_epoch=17199))
        text = (self.report / "progress.md").read_text()
        self.assertIn("+200 exact-unique tokens", text)
        self.assertIn("fixed PST", text)
        self.assertIn("1.00 GiB", text)
        self.assertIn("final usable biology tokens remain unmeasured", text)

    def test_terminal_is_immediate_deduplicated_and_can_restart(self):
        self.reporter.emit(snapshot(), now_epoch=10000)
        stopped = snapshot(120, "stopped")
        stopped["stop_reason"] = "runtime_limit"
        event = self.reporter.emit(stopped, now_epoch=10001)
        self.assertEqual(event["kind"], "terminal")
        self.assertEqual(event["delta"]["raw_tokens"], 20)
        self.assertIsNone(ProgressReporter(self.run, self.report).emit(stopped, now_epoch=20000))
        self.assertEqual(len(self.events()), 2)
        self.assertIn("runtime_limit", (self.report / "progress.md").read_text())
        self.assertEqual(self.reporter.emit(snapshot(130), now_epoch=20001)["kind"], "start")

    def test_final_backfill_does_not_require_running_worker_and_keeps_paper_scope(self):
        final = snapshot(120, "failed")
        final["error"] = "ValueError: checksum mismatch"
        final["sources"]["pmc"] = {"name": "PMC", "content_category": "papers", "raw_records": 2333}
        final["paper_expansion"] = {"accepted_new_papers": 1873, "scope_excluded_acquired_papers": 6}
        original = copy.deepcopy(final)
        event = self.reporter.emit(final, now_epoch=10000)
        self.assertEqual(event["kind"], "terminal")
        self.assertEqual(event["papers"]["selected_papers"], 2327)
        self.assertEqual(final, original)
        self.assertIn("checksum mismatch", (self.report / "progress.md").read_text())

    def test_failed_report_write_recovers_without_duplicate_journal_or_lost_baseline(self):
        self.reporter.emit(snapshot(), now_epoch=10000)
        import corpus_progress
        real_write = corpus_progress._atomic_text

        def fail_report(path, text):
            if path.name == "progress.md":
                raise OSError("temporary report failure")
            return real_write(path, text)

        with patch("corpus_progress._atomic_text", side_effect=fail_report):
            with self.assertRaisesRegex(OSError, "temporary report failure"):
                self.reporter.emit(snapshot(200), now_epoch=13600)
        self.assertEqual(len(self.events()), 2)
        resumed = ProgressReporter(self.run, self.report)
        recovered = resumed.emit(snapshot(210), now_epoch=13601)
        self.assertEqual(recovered["totals"]["raw_tokens"], 200)
        self.assertEqual(len(self.events()), 2)
        self.assertNotIn("pending_event", json.loads((self.run / "progress_state.json").read_text()))
        next_event = resumed.emit(snapshot(400), now_epoch=17200)
        self.assertEqual(next_event["delta"]["raw_tokens"], 200)

    def test_run_identity_and_interval_are_validated(self):
        self.reporter.emit(snapshot(), now_epoch=10000)
        other = snapshot()
        other["run_id"] = "another-pilot"
        with self.assertRaisesRegex(ValueError, "another run"):
            self.reporter.emit(other, now_epoch=13600)
        with self.assertRaisesRegex(ValueError, "positive"):
            ProgressReporter(self.run, self.report, interval_seconds=0)


if __name__ == "__main__":
    unittest.main()
