import importlib.util
from pathlib import Path
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
