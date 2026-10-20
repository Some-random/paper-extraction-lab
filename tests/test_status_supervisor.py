import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
SPEC = importlib.util.spec_from_file_location("status_supervisor", SCRIPTS / "supervise_status_updates.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class SupervisorCommandsTests(unittest.TestCase):
    def test_continuation_paths_and_two_hour_cadence_reach_children(self):
        config = {"interval_seconds": 7200, "paper_config_path": "config/continuation.json",
                  "paper_run_directory": "experiments/continuation", "paper_report_directory": "reports/continuation"}
        commands = module.reporter_commands(config, Path("private/config.json"))
        for name in ("papers", "throughput"):
            self.assertEqual(commands[name][commands[name].index("--report-seconds") + 1], "7200")
        for option, expected in (("--config", "config/continuation.json"),
                                 ("--run-dir", "experiments/continuation"),
                                 ("--report-dir", "reports/continuation")):
            self.assertEqual(commands["papers"][commands["papers"].index(option) + 1], expected)
        self.assertEqual(commands["chat"][-2:], ["--config", "private/config.json"])
        self.assertNotIn("--force", commands["chat"])

    def test_invalid_cadence_rejected_before_spawn(self):
        with self.assertRaises(ValueError):
            module.reporter_commands({"interval_seconds": 7201}, Path("config.json"))

    def test_explicit_reporter_reload_keeps_cadence_history_and_deadline(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            state = {"monitor_status": "stopped", "stop_reason": "requested_stop", "checked_epoch": 102,
                     "last_accepted_epoch": 70, "next_due_epoch": 7270, "deadline_epoch": 1000}
            (directory / "queue_state.json").write_text(json.dumps(state))
            (directory / "reporter_reload.json").write_text(json.dumps({"requested_epoch": 100, "deadline_epoch": 1000}))
            module.apply_requested_reload(directory, {"deadline_epoch": 1000})
            observed = json.loads((directory / "queue_state.json").read_text())
            self.assertEqual(observed, {key: value for key, value in {**state, "monitor_status": "watching"}.items()
                                        if key != "stop_reason"})
            self.assertFalse((directory / "reporter_reload.json").exists())
            module.apply_requested_reload(directory, {"deadline_epoch": 1000})
            self.assertEqual(observed, json.loads((directory / "queue_state.json").read_text()))
