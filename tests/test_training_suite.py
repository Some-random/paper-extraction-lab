import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("training_suite", ROOT / "scripts/benchmark_training_suite.py")
suite = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(suite)


class TrainingSuiteTests(unittest.TestCase):
    def test_all_profiles_match_global_tokens_for_all_allocations(self):
        for world in (2, 4, 8):
            for profile in suite.profiles(world):
                self.assertEqual(world * profile["microbatch_per_gpu"] * profile["accumulation"] * 4096,
                                 131072)
        self.assertEqual([profile["accumulation"] for profile in suite.profiles(2)], [16, 8, 4])
        self.assertEqual([profile["accumulation"] for profile in suite.profiles(4)], [8, 4, 2])
        self.assertEqual([profile["accumulation"] for profile in suite.profiles(8)], [4, 2, 1])
        with self.assertRaises(ValueError):
            suite.profiles(8, 31)

    def test_winner_excludes_partial_failed_and_nonzero_launcher_exit(self):
        records = [dict(name="good", status="completed", exit_code=0, input_tokens_per_second=100),
                   dict(name="partial", status="runtime_limit", exit_code=2, input_tokens_per_second=900),
                   dict(name="failed", status="failed", exit_code=1, input_tokens_per_second=1000),
                   dict(name="bad_exit", status="completed", exit_code=1, input_tokens_per_second=1100)]
        self.assertEqual(suite.fastest_completed(records)["name"], "good")
        self.assertIsNone(suite.fastest_completed(records[1:]))

    def test_persisted_deadline_and_attempts_prevent_reset_or_repeat(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "suite_state.json"
            state = suite.load_state(path, {"world": 2}, 100, 1000)
            profile = suite.profiles(2)[0]
            self.assertTrue(suite.eligible(profile, state, 1000, 80))
            state["attempted_profiles"][profile["name"]] = {"status": "failed"}
            suite.write_json(path, state)
            resumed = suite.load_state(path, {"world": 2}, 100, 1090)
            self.assertEqual(resumed["deadline_epoch"], 1100)
            self.assertFalse(suite.eligible(profile, resumed, 1000, 80))
            self.assertFalse(suite.eligible(suite.profiles(2)[1], resumed, 1090, 80))
            with self.assertRaises(ValueError):
                suite.load_state(path, {"world": 8}, 100, 1090)

    def test_command_is_argument_vector_without_shell_interpolation(self):
        profile = suite.profiles(2)[1]
        command = suite.child_command(profile, python="/python path/python", world_size=2,
                                      model_config=Path("config with spaces.json"),
                                      output=Path("out; $(false)/results.json"), sequence_length=4096,
                                      warmup=3, steps=8, runtime_seconds=280)
        self.assertEqual(command[0], "/python path/python")
        self.assertIn("--nproc_per_node=2", command)
        self.assertEqual(command[command.index("--batch-size") + 1], "2")
        self.assertEqual(command[command.index("--accumulation") + 1], "8")
        self.assertIn("out; $(false)/results.json", command)

    def test_timeout_overrides_completed_result_and_partial_stays_partial(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.json"
            profile = suite.profiles(8)[0]
            suite.write_json(path, {"status": "completed", "throughput": {"input_tokens_per_second": 100}})
            record = suite.read_profile_result(profile, path, -15, True)
            self.assertEqual(record["failure_type"], "ProfileTimeout")
            self.assertIsNone(suite.fastest_completed([record]))
            suite.write_json(path, {"status": "runtime_limit", "throughput": {"input_tokens_per_second": 100}})
            record = suite.read_profile_result(profile, path, 2, False)
            self.assertEqual(record["status"], "runtime_limit")
            self.assertEqual(record["input_tokens_per_second"], 100)

    def test_orchestrator_retains_profiles_selects_complete_result_and_does_not_rerun(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "model.json"
            config.write_text("{}")
            args = SimpleNamespace(world_size=2, global_batch_sequences=32, sequence_length=4096,
                                   model_config=config, warmup=3, steps=8, profile_runtime_seconds=1,
                                   total_runtime_seconds=100, output_dir=root / "job")

            def fake_process(command, log_path, timeout):
                micro = int(command[command.index("--batch-size") + 1])
                destination = Path(command[command.index("--output") + 1])
                value = {"status": "runtime_limit" if micro == 4 else "completed",
                         "world_size": 2,
                         "arguments": {"sequence_length": 4096, "batch_size": micro,
                                       "accumulation": 32 // (2 * micro)},
                         "throughput": {"input_tokens_per_second": micro * 100,
                                                            "input_tokens_per_step": 131072}}
                suite.write_json(destination, value)
                return (2 if micro == 4 else 0), False

            with patch.object(suite, "run_process", side_effect=fake_process) as process:
                self.assertEqual(suite.run_suite(args), 0)
                self.assertEqual(process.call_count, 3)
                process.reset_mock()
                self.assertEqual(suite.run_suite(args), 0)
                process.assert_not_called()
            result = json.loads((args.output_dir / "results.json").read_text())
            self.assertEqual(result["throughput"]["input_tokens_per_second"], 200)
            self.assertEqual(result["suite"]["selected_profile"], "micro_2")
            self.assertEqual(len(result["suite"]["profiles"]), 3)
            self.assertEqual(result["suite"]["profiles"][2]["status"], "runtime_limit")

    def test_completed_result_must_match_actual_allocation_and_batch_dimensions(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.json"
            profile = suite.profiles(2)[0]
            original = {"status": "completed", "world_size": 2,
                        "arguments": {"sequence_length": 4096, "batch_size": 1, "accumulation": 16},
                        "throughput": {"input_tokens_per_second": 100, "input_tokens_per_step": 131072}}
            for field, wrong in (("world_size", 8), ("sequence_length", 2048),
                                 ("batch_size", 2), ("accumulation", 4),
                                 ("input_tokens_per_step", 16384)):
                value = json.loads(json.dumps(original))
                if field == "world_size":
                    value[field] = wrong
                elif field == "input_tokens_per_step":
                    value["throughput"][field] = wrong
                else:
                    value["arguments"][field] = wrong
                suite.write_json(path, value)
                record = suite.read_profile_result(profile, path, 0, False, world_size=2,
                                                   sequence_length=4096, global_batch_sequences=32)
                with self.subTest(field=field):
                    self.assertEqual(record["failure_type"], "MatchedConfigurationMismatch")
                    self.assertIsNone(suite.fastest_completed([record]))
            suite.write_json(path, original)
            record = suite.read_profile_result(profile, path, 0, False, world_size=2,
                                               sequence_length=4096, global_batch_sequences=32)
            self.assertEqual(record["status"], "completed")


if __name__ == "__main__":
    unittest.main()
