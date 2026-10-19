import importlib.util
import hashlib
import json
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


PATH = Path(__file__).resolve().parents[1] / "scripts/benchmark_training_check.py"
SPEC = importlib.util.spec_from_file_location("training_check", PATH)
check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check)


CONFIG = {"sequence_length": 4096, "global_batch_sequences": 32,
          "warmup_optimizer_steps": 3, "measured_optimizer_steps": 8}


def completed_result(profile, world=2, gpu="B200", rate=14000):
    return {"status": "completed", "world_size": world,
            "hardware": [{"gpu": f"NVIDIA {gpu}"} for _ in range(world)],
            "arguments": {"sequence_length": 4096, "batch_size": profile["microbatch_per_gpu"],
                          "accumulation": profile["accumulation"],
                          "activation_checkpointing": profile["activation_checkpointing"],
                          "sharding": profile["sharding"], "profile_steps": profile["profile_steps"]},
            "completed_warmup_steps": 3, "setup_seconds": 20., "warmup_seconds": 30.,
            "measurement_seconds": 74., "profiler": {"status": "completed", "elapsed_seconds": 11.},
            "throughput": {"input_tokens_per_second": rate,
                           "input_tokens_per_step": 131072, "measured_optimizer_steps": 8}}


class TrainingCheckTests(unittest.TestCase):
    def test_all_profiles_keep_matched_batch_and_baseline_is_identified(self):
        for mode, world, gpu in (("b200_tuning", 2, "b200"), ("a100_diagnostic", 8, "a100")):
            profiles = check.profiles(mode, world, gpu)
            self.assertEqual(profiles[0]["role"], "baseline")
            self.assertEqual(profiles[0]["activation_checkpointing"], "on")
            self.assertEqual(profiles[0]["sharding"], "full_shard")
            for profile in profiles:
                self.assertEqual(world * profile["microbatch_per_gpu"] * profile["accumulation"], 32)
                self.assertEqual(profile["profile_steps"], 1 if profile["role"] == "baseline" else 0)
        with self.assertRaises(ValueError):
            check.profiles("a100_diagnostic", 2, "b200")

    def test_saved_deadline_never_resets_and_changed_binding_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "suite_state.json"
            first = check.load_state(path, {"hash": "a"}, 1080, 1000)
            check.write_json(path, first)
            resumed = check.load_state(path, {"hash": "a"}, 1080, 9000)
            self.assertEqual(resumed["deadline_epoch"], 2080)
            with self.assertRaises(ValueError):
                check.load_state(path, {"hash": "b"}, 1080, 9000)

    def read_result(self, profile, result, code=0, reason=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.json"
            check.write_json(path, result)
            return check.profile_result(profile, path, code, reason,
                                        world_size=2, gpu_type="b200", config=CONFIG)

    def test_timeout_and_launcher_failure_never_supply_a_rate(self):
        profile = check.profiles("b200_tuning", 2, "b200")[0]
        result = completed_result(profile)
        for code, reason in ((-15, "profile_wall_timeout"), (1, None), (0, "shared_free_space_floor")):
            with self.subTest(code=code, reason=reason):
                record = self.read_result(profile, result, code, reason)
                self.assertEqual(record["status"], "failed")
                self.assertNotIn("throughput", record)
                self.assertNotIn("input_tokens_per_second", record)

    def test_incorrect_batch_hardware_or_incomplete_measurement_is_rejected(self):
        profile = check.profiles("b200_tuning", 2, "b200")[0]
        for change in ("tokens", "warmup", "hardware", "checkpoint", "rate"):
            result = completed_result(profile)
            if change == "tokens":
                result["throughput"]["input_tokens_per_step"] = 16384
            elif change == "warmup":
                result["completed_warmup_steps"] = 2
            elif change == "hardware":
                result["hardware"][0]["gpu"] = "NVIDIA A100"
            elif change == "checkpoint":
                result["arguments"]["activation_checkpointing"] = "off"
            else:
                result["throughput"]["input_tokens_per_second"] = 0
            with self.subTest(change=change):
                self.assertEqual(self.read_result(profile, result)["status"], "failed")

    def test_tuned_winner_is_separate_from_baseline_and_profiler_time(self):
        profiles = check.profiles("b200_tuning", 2, "b200")
        records = {p["name"]: self.read_result(p, completed_result(p, rate=rate))
                   for p, rate in zip(profiles, (14000, 22000, 21000))}
        state = {"configuration": {"mode": "b200_tuning", "world_size": 2},
                 "started_utc": "2026-10-19T00:00:00+00:00", "started_epoch": 1,
                 "deadline_epoch": 1081, "attempted_profiles": records}
        result = check.summarize(state, profiles, 500)
        self.assertEqual(result["baseline_result"]["input_tokens_per_second"], 14000)
        self.assertEqual(result["fastest_completed_profile"]["input_tokens_per_second"], 22000)
        self.assertEqual(result["baseline_result"]["measurement_seconds"], 74.)
        self.assertEqual(result["baseline_result"]["profiler"]["elapsed_seconds"], 11.)
        self.assertAlmostEqual(result["tuning_speedup_over_baseline"], 22 / 14)

    def test_child_command_is_offline_torchrun_with_matching_flags(self):
        profile = check.profiles("b200_tuning", 2, "b200")[1]
        command = check.child_command(profile, SimpleNamespace(world_size=2), CONFIG,
                                      Path("model.json"), Path("result.json"), 310)
        self.assertIn("torch.distributed.run", command)
        self.assertIn("--nproc_per_node=2", command)
        self.assertEqual(command[command.index("--activation-checkpointing") + 1], "off")
        self.assertEqual(command[command.index("--sharding") + 1], "shard_grad_op")
        self.assertEqual(command[command.index("--max-runtime-seconds") + 1], "310")

    def test_storage_guards_use_preflight_and_small_job_tree(self):
        config = {"baseline_environment_and_artifact_bytes": 7 * 1024 ** 3,
                  "bounds": {"new_run_artifact_bytes": 64 * check.MIB,
                             "new_environment_and_artifact_bytes": 16 * 1024 ** 3,
                             "minimum_free_bytes": 64 * 1024 ** 3}}
        with patch.object(check, "tree_bytes", return_value=63 * check.MIB), \
             patch.object(check.shutil, "disk_usage", return_value=SimpleNamespace(free=100 * 1024 ** 3)):
            self.assertEqual(check.storage_reason(config), "new_artifact_limit")
        with patch.object(check, "tree_bytes", return_value=0), \
             patch.object(check.shutil, "disk_usage", return_value=SimpleNamespace(free=60 * 1024 ** 3)):
            self.assertEqual(check.storage_reason(config), "shared_free_space_floor")

    def test_owned_group_cleanup_sends_term_and_kill_even_if_launcher_exited(self):
        process = SimpleNamespace(pid=1234567, wait=lambda timeout: 0, poll=lambda: 0)
        with patch.object(check.os, "killpg") as killpg:
            self.assertEqual(check.terminate_owned(process), 0)
        self.assertEqual(killpg.call_args_list,
                         [unittest.mock.call(1234567, signal.SIGTERM),
                          unittest.mock.call(1234567, signal.SIGKILL)])

    def test_real_cpu_child_is_bounded_and_environment_is_offline(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "worker.log"
            command = [sys.executable, "-u", "-c",
                       "import os,time; print(os.environ['HF_HUB_OFFLINE'],flush=True); time.sleep(30)"]
            code, reason, elapsed = check.run_process(command, path, .15, lambda: None)
            self.assertEqual(reason, "profile_wall_timeout")
            self.assertNotEqual(code, 0)
            self.assertLess(elapsed, 6)
            self.assertEqual(path.read_text().strip(), "1")

    def test_cpu_simulated_suite_preserves_baseline_and_never_repeats_profiles(self):
        model = check.ROOT / "config/qwen3_4b_throughput_model.json"
        config = dict(CONFIG, model_config=str(model.relative_to(check.ROOT)),
                      model_config_sha256=hashlib.sha256(model.read_bytes()).hexdigest(),
                      baseline_environment_and_artifact_bytes=7 * 1024 ** 3,
                      baseline_checked_epoch=1000,
                      bounds={"suite_seconds": 1080, "b200_profile_seconds": 320,
                              "a100_profile_seconds": 900, "new_run_artifact_bytes": 64 * check.MIB,
                              "new_environment_and_artifact_bytes": 16 * 1024 ** 3,
                              "minimum_free_bytes": 64 * 1024 ** 3})
        with tempfile.TemporaryDirectory(dir=check.ROOT / "experiments") as directory:
            directory = Path(directory)
            config_path = directory / "config.json"
            check.write_json(config_path, config)
            args = SimpleNamespace(config=config_path, world_size=2, gpu_type="b200",
                                   output_dir=directory / "job_cpu_test", mode="b200_tuning")
            by_name = {p["name"]: p for p in check.profiles(args.mode, 2, "b200")}
            rates = {"baseline": 14000, "tuned_micro4": 22000, "tuned_micro8": 21000}
            def simulated(command, log_path, timeout, guard):
                output = Path(command[command.index("--output") + 1])
                name = output.parent.name
                result = completed_result(by_name[name], rate=rates[name])
                result["config_sha256"] = config["model_config_sha256"]
                check.write_json(output, result)
                return 0, None, .1
            with patch.object(check, "ORIGINAL_RUN", directory), \
                 patch.object(check, "storage_reason", return_value=None), \
                 patch.object(check, "run_process", side_effect=simulated) as run:
                self.assertEqual(check.run_suite(args), 0)
                result = json.loads((args.output_dir / "results.json").read_text())
                deadline = result["suite"]["deadline_epoch"]
                self.assertEqual(result["throughput"]["input_tokens_per_second"], 14000)
                self.assertEqual(result["suite"]["fastest_completed_profile"]["input_tokens_per_second"], 22000)
                self.assertEqual(run.call_count, 3)
                self.assertEqual(check.run_suite(args), 0)
                self.assertEqual(run.call_count, 3)
                self.assertEqual(json.loads((args.output_dir / "results.json").read_text())
                                 ["suite"]["deadline_epoch"], deadline)


if __name__ == "__main__":
    unittest.main()
