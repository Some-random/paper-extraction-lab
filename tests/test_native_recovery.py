"""Outages preserve pending work, byte accounting and explicit deadlines."""
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from run_native_scale import NativeScale, NetworkUnavailable, continuation_deadline
from run_pmc_batch import Batch, LimitReached, Rejected, PST


def worker():
    run = NativeScale.__new__(NativeScale)
    run.config = {"network_retry_initial_seconds": 30, "network_retry_maximum_seconds": 300,
                  "network_outage_budget_seconds": 120}
    run.state = {"papers": [], "stage": "download_and_native_parse", "downloaded_response_bytes": 123}
    run.guard = Mock()
    run.event = Mock()
    run.wait_for_network = Mock()
    run.persist = Mock()
    return run


class NativeRecoveryChecks(unittest.TestCase):
    def test_fresh_run_does_not_open_or_seed_any_prior_batch(self):
        run = worker()
        run.config.update(reuse_existing_sources=False,
                          reuse_state="missing-prior-run/state.json")
        run.seed_cached()
        self.assertEqual(run.state['papers'], [])
        self.assertTrue(run.state['cache_seed_complete'])
        self.assertIn('Fresh acquisition', run.state['cache_policy'])
        run.persist.assert_called_once()

    def test_outage_retries_same_request_and_keeps_cumulative_accounting(self):
        run = worker()
        with patch.object(Batch, "request", side_effect=[URLError("refused"), b"source"]) as fetch:
            result = run.request("https://example.test/source.xml", 500)
        self.assertEqual(result, b"source")
        self.assertEqual(fetch.call_count, 2)
        self.assertEqual(fetch.call_args_list[0], fetch.call_args_list[1])
        run.wait_for_network.assert_called_once_with(30)
        self.assertEqual(run.state["downloaded_response_bytes"], 123)
        self.assertEqual(run.state["stage"], "download_and_native_parse")
        self.assertNotIn("network_outage", run.state)

    def test_persistent_outage_stops_batch_instead_of_skipping_candidates(self):
        run = worker()
        run.seed_cached = Mock()
        run.acquire = lambda: run.request("https://example.test/source.xml", 500)
        clock = [0]
        run.wait_for_network.side_effect = lambda seconds: clock.__setitem__(0, clock[0] + seconds)
        with patch.object(Batch, "request", side_effect=URLError("refused")) as fetch, \
                patch("run_native_scale.time.monotonic", side_effect=lambda: clock[0]):
            run.run()
        self.assertEqual(run.state["status"], "network_unavailable")
        self.assertNotEqual(run.state["status"], "candidate_pool_exhausted")
        self.assertEqual(fetch.call_count, 4)
        self.assertEqual(run.state["papers"], [])
        self.assertEqual(run.state["downloaded_response_bytes"], 123)

    def test_permanent_rejection_does_not_start_outage_wait(self):
        run = worker()
        with patch.object(Batch, "request", side_effect=Rejected("HTTP 404")):
            with self.assertRaises(Rejected):
                run.request("https://example.test/missing", 500)
        run.wait_for_network.assert_not_called()

    def test_stop_or_deadline_during_outage_is_honored(self):
        run = worker()
        run.wait_for_network.side_effect = LimitReached("User stop file requested")
        with patch.object(Batch, "request", side_effect=URLError("refused")):
            with self.assertRaises(LimitReached):
                run.request("https://example.test/source.xml", 500)

    def test_continuation_uses_recorded_cutoff_without_resetting_it(self):
        start = datetime(2026, 10, 15, 12, tzinfo=PST)
        old = start - timedelta(hours=3)
        self.assertEqual(continuation_deadline({}, old, start), old)
        config = {"authorized_continuation": {
            "user_instruction": "you can actually keep going, right?",
            "authorized_at_pst": start.isoformat(), "maximum_session_hours": 6,
            "stop_before_pst": (start + timedelta(hours=6)).isoformat()}}
        self.assertEqual(continuation_deadline(config, old, start), start + timedelta(hours=6))
        self.assertEqual(continuation_deadline(config, old, start + timedelta(hours=2)), start + timedelta(hours=6))
        config["authorized_continuation"].pop("user_instruction")
        with self.assertRaises(ValueError):
            continuation_deadline(config, old, start)


if __name__ == "__main__":
    unittest.main()
