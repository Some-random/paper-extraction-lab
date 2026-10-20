import copy
import importlib.util
import json
from pathlib import Path
import signal
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[1] / "scripts/benchmark_gpu_sweep.py"
SPEC = importlib.util.spec_from_file_location("gpu_sweep", PATH)
sweep = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sweep)
BASE_FEATURES = dict(attention="sdpa_auto", kernels="none", checkpointing="full", sharding="full_shard",
                     compile="off", precision="bf16", float8_all_gather="off", optimizer="adamw_fp32")


def configuration(gpu="a100"):
    world = 8 if gpu == "a100" else 2
    return dict(gpu_type=gpu, world_size=world, sequence_length=4096, global_batch_sequences=32,
                warmup_optimizer_steps=3, measured_optimizer_steps=8,
                model_config_sha256="model-hash", runner_sha256="runner-hash", data_pack_sha256="data-hash",
                data_manifest_sha256="manifest-hash", baseline_environment_and_artifact_bytes=8 * sweep.GIB,
                baseline_checked_epoch=1,
                confirmations=dict(minimum_measurement_seconds=600, minimum_optimizer_steps=8,
                                   baseline_name="confirm_baseline", winner_name="confirm_winner"),
                bounds=dict(suite_seconds=6600, profile_seconds=420, compile_profile_seconds=900,
                            confirmation_profile_seconds=900, confirmation_reserve_seconds=1900,
                            new_log_bytes=64 * sweep.MIB, new_run_artifact_bytes=256 * sweep.MIB,
                            new_compile_cache_bytes=4 * sweep.GIB,
                            new_environment_and_artifact_bytes=16 * sweep.GIB, minimum_free_bytes=64 * sweep.GIB),
                profiles=[dict(name="baseline", parent=None, role="baseline", features=BASE_FEATURES.copy(),
                               microbatch_per_gpu=4, accumulation=32 // (world * 4)),
                          dict(name="flash", parent="baseline", role="tuning", features={"attention": "sdpa_flash"},
                               microbatch_per_gpu=4, accumulation=32 // (world * 4))])


def state_for(cfg, now=1000):
    return dict(configuration=dict(world_size=cfg["world_size"], gpu_type=cfg["gpu_type"]),
                started_epoch=now, deadline_epoch=now + cfg["bounds"]["suite_seconds"],
                started_utc="2026-10-20T00:00:00+00:00", attempted_profiles={}, confirmations={}, stage="short_sweep")


def result_for(profile, cfg, *, real_data=False, seconds=None, steps=None):
    seconds = (600. if real_data else 70.) if seconds is None else seconds
    steps = (80 if real_data else 8) if steps is None else steps
    args = dict(sequence_length=4096, batch_size=profile["microbatch_per_gpu"], accumulation=profile["accumulation"],
                hardware=cfg["gpu_type"])
    args.update({sweep.ARGUMENTS.get(key, key): value for key, value in profile["features"].items()})
    if real_data:
        args.update(minimum_measured_seconds=600, input_start_token=0,
                    input_token_pack_sha256=cfg["data_pack_sha256"])
    return dict(status="completed", world_size=cfg["world_size"], arguments=args,
                config_sha256=cfg["model_config_sha256"], runner_sha256=cfg["runner_sha256"],
                hardware=[{"gpu": "NVIDIA " + cfg["gpu_type"].upper()} for _ in range(cfg["world_size"])],
                packages={"torch": "2.8", "transformers": "4.57.1"},
                completed_warmup_steps=3, setup_seconds=20., warmup_seconds=18., measurement_seconds=seconds,
                smoke_checks={"status": "passed"}, optimizer_update_check={"status": "passed"},
                data_validation={"status": "passed"}, data_pack_sha256=cfg["data_pack_sha256"],
                data_manifest_sha256=cfg["data_manifest_sha256"], data={"replay": False},
                measurement_requirements={"satisfied": True, "last_completed_update_end_seconds": seconds},
                throughput=dict(input_tokens_per_second=steps * 131072 / seconds, input_tokens_per_step=131072,
                                measured_optimizer_steps=steps, measured_input_tokens=steps * 131072,
                                measured_wall_seconds=seconds, valid_sustained_measurement=True))


class GPUSweepTests(unittest.TestCase):
    def baseline(self, cfg=None):
        cfg = cfg or configuration()
        return sweep.resolve_profile(cfg["profiles"][0], cfg["profiles"], state_for(cfg))

    def record(self, profile, cfg, result, *, real_data=False, code=0, reason=None, launcher_seconds=700):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.json"
            sweep.write_json(path, result)
            return sweep.profile_result(profile, path, code, reason, world_size=cfg["world_size"],
                                        gpu_type=cfg["gpu_type"], config=cfg, real_data=real_data,
                                        launcher_seconds=launcher_seconds)

    def test_fixed_global_batch_works_for_both_gpu_counts(self):
        for gpu in ("a100", "b200"):
            cfg = configuration(gpu)
            sweep.validate_profiles(cfg, cfg["world_size"])
            for profile in cfg["profiles"]:
                self.assertEqual(cfg["world_size"] * profile["microbatch_per_gpu"] * profile["accumulation"], 32)
            cfg["profiles"][1]["accumulation"] += 1
            with self.assertRaises(ValueError):
                sweep.validate_profiles(cfg, cfg["world_size"])

    def test_saved_deadline_never_resets(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            state = sweep.load_state(path, {"hash": "a"}, 6600, 1000)
            sweep.write_json(path, state)
            self.assertEqual(sweep.load_state(path, {"hash": "a"}, 6600, 100000)["deadline_epoch"], 7600)
            with self.assertRaises(ValueError):
                sweep.load_state(path, {"hash": "changed"}, 6600, 100000)

    def test_independent_attention_loss_candidates_can_combine(self):
        cfg = configuration()
        loss = dict(name="loss", parent="baseline", role="tuning", features={"kernels": "liger_loss"},
                    microbatch_per_gpu=4, accumulation=1)
        combo = dict(name="combo", parent="baseline", role="combination", microbatch_per_gpu=4, accumulation=1,
                     features={"attention": "@best:attention", "kernels": "@best:kernels"},
                     feature_candidates={"attention": ["baseline", "flash"], "kernels": ["baseline", "loss"]})
        cfg["profiles"] += [loss, combo]
        state = state_for(cfg)
        for plan, rate in zip(cfg["profiles"][:3], (15000, 24000, 22000)):
            profile = sweep.resolve_profile(plan, cfg["profiles"], state)
            state["attempted_profiles"][profile["name"]] = dict(profile, status="completed", input_tokens_per_second=rate)
        effective = sweep.resolve_profile(combo, cfg["profiles"], state)
        self.assertEqual(effective["features"]["attention"], "sdpa_flash")
        self.assertEqual(effective["features"]["kernels"], "liger_loss")
        state["attempted_profiles"]["loss"]["status"] = "failed"
        self.assertEqual(sweep.resolve_profile(combo, cfg["profiles"], state)["features"]["kernels"], "none")

    def test_confirmation_requires600_real_seconds_and_parent_wall_not_just_eight_steps(self):
        cfg, profile = configuration(), self.baseline()
        valid = result_for(profile, cfg, real_data=True)
        self.assertEqual(self.record(profile, cfg, valid, real_data=True)["status"], "completed")
        for case in ("short", "parent_short", "wrong_data", "wrong_start", "missing_request", "few_steps", "barrier_only", "not_sustained", "manifest_hash", "replay"):
            result = copy.deepcopy(valid)
            parent = 700
            if case == "short":
                result = result_for(profile, cfg, real_data=True, seconds=599.9)
            elif case == "parent_short":
                parent = 72.
            elif case == "wrong_data":
                result["arguments"]["input_token_pack_sha256"] = "wrong"
            elif case == "wrong_start":
                result["arguments"]["input_start_token"] = 131072
            elif case == "missing_request":
                result["arguments"].pop("minimum_measured_seconds")
            elif case == "few_steps":
                result = result_for(profile, cfg, real_data=True, steps=7)
            elif case == "barrier_only":
                result["measurement_requirements"]["last_completed_update_end_seconds"] = 70.
            elif case == "not_sustained":
                result["throughput"]["valid_sustained_measurement"] = False
            elif case == "manifest_hash":
                result["data_manifest_sha256"] = "wrong"
            else:
                result["data"]["replay"] = True
            with self.subTest(case=case):
                self.assertEqual(self.record(profile, cfg, result, real_data=True, launcher_seconds=parent)["status"], "failed")

    def test_mismatched_hardware_hashes_numerical_checks_and_arithmetic_fail(self):
        cfg, profile = configuration(), self.baseline()
        for case in ("hardware", "model", "runner", "smoke", "update", "tokens", "rate", "feature"):
            result = result_for(profile, cfg)
            if case == "hardware":
                result["hardware"][0]["gpu"] = "NVIDIA B200"
            elif case == "model":
                result["config_sha256"] = "changed"
            elif case == "runner":
                result["runner_sha256"] = "changed"
            elif case == "smoke":
                result["smoke_checks"]["status"] = "failed"
            elif case == "update":
                result["optimizer_update_check"]["status"] = "failed"
            elif case == "tokens":
                result["throughput"]["measured_input_tokens"] -= 1
            elif case == "rate":
                result["throughput"]["input_tokens_per_second"] *= 1.1
            else:
                result["arguments"]["activation_checkpointing"] = "off"
            with self.subTest(case=case):
                self.assertEqual(self.record(profile, cfg, result)["status"], "failed")

    def test_actual_runtime_packages_must_match_cpu_preflight_versions(self):
        cfg, profile = configuration(), self.baseline()
        cfg["_expected_runtime_packages"] = {"torch": "2.8", "transformers": "4.57.1"}
        result = result_for(profile, cfg)
        self.assertEqual(self.record(profile, cfg, result)["status"], "completed")
        result["packages"]["torch"] = "2.9"
        record = self.record(profile, cfg, result)
        self.assertEqual(record["failure_type"], "RuntimePackageVersionMismatch")
        self.assertNotIn("throughput", record)

    def test_unavailable_timeout_and_failure_never_supply_usable_rate(self):
        cfg, profile = configuration(), self.baseline()
        for code, reason, failure, status in ((1, None, "UnsupportedFeature", "unavailable"),
                                             (1, None, "OutOfMemoryError", "failed"),
                                             (-15, "profile_wall_timeout", None, "failed")):
            result = result_for(profile, cfg)
            if failure:
                result.update(status="failed", failure_type=failure)
            record = self.record(profile, cfg, result, code=code, reason=reason)
            self.assertEqual(record["status"], status)
            self.assertNotIn("throughput", record)

    def test_launcher_signal_is_visible_without_claiming_cache_error_caused_it(self):
        cfg, profile = configuration(), self.baseline()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.json"
            path.with_name("worker.log").write_text("[Errno 27] File too large\nSignal11(SIGSEGV)\n")
            record = sweep.profile_result(profile, path, 1, None, world_size=8, gpu_type="a100", config=cfg)
            self.assertEqual(record["failure_type"], "WorkerSegmentationFault")
            self.assertTrue(record["log_signatures"]["file_size_error"])

    def test_short_probe_winner_cannot_be_reported_as_confirmed(self):
        cfg, state = configuration(), state_for(configuration())
        baseline = self.baseline(cfg)
        state["attempted_profiles"]["baseline"] = dict(baseline, status="completed", input_tokens_per_second=20000)
        winner = dict(baseline, name="flash", features={**baseline["features"], "attention": "sdpa_flash"},
                      status="completed", input_tokens_per_second=50000)
        state["attempted_profiles"]["flash"] = winner
        summary = sweep.summarize(state, cfg, 1200)
        self.assertEqual(summary["short_sweep_winner"]["input_tokens_per_second"], 50000)
        self.assertIsNone(summary["fastest_completed_profile"])
        self.assertEqual(summary["baseline_result"]["status"], "pending")
        for is_winner, seconds in ((False, 600), (True, 620)):
            profile = sweep.confirmation_profile(cfg, state, winner=is_winner)
            result = result_for(profile, cfg, real_data=True, seconds=seconds)
            state["confirmations"][profile["name"]] = self.record(profile, cfg, result, real_data=True)
        summary = sweep.summarize(state, cfg, 2500, terminal=True)
        self.assertEqual(summary["status"], "completed")
        self.assertEqual(summary["fastest_completed_profile_name"], "confirm_baseline")
        self.assertLess(summary["candidate_speedup_over_baseline"], 1)
        self.assertEqual(summary["tuning_speedup_over_baseline"], 1.)

    def test_real_data_command_fixes_pack_hash_order_and_minimum_duration(self):
        cfg, profile = configuration(), self.baseline()
        paths = {key: Path(key) for key in ("model_config", "data_pack", "data_manifest")}
        command = sweep.child_command(profile, SimpleNamespace(world_size=8, gpu_type="a100"), cfg,
                                      paths, Path("results.json"), 899.9, real_data=True)
        for flag, value in (("--hardware", "a100"), ("--input-token-pack-sha256", "data-hash"),
                            ("--minimum-measured-seconds", "600"), ("--input-start-token", "0"),
                            ("--max-runtime-seconds", "889"), ("--global-batch-sequences", "32")):
            self.assertEqual(command[command.index(flag) + 1], value)

    def test_large_compiler_file_allowed_while_noisy_log_is_capped(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            cache, log = directory / "cache", directory / "worker.log"
            output = cache / "compiled_blob"
            code = ("import os,pathlib; p=pathlib.Path(os.environ['TORCHINDUCTOR_CACHE_DIR']);"
                    "p.mkdir(parents=True,exist_ok=True);(p/'compiled_blob').write_bytes(b'x'*(9*1024*1024));"
                    "os.write(1,b'z'*(10*1024*1024));print('done',flush=True)")
            exit_code, reason, elapsed, capture = sweep.run_process([sys.executable, "-u", "-c", code], log,
                                                                    10, lambda: None, cache, log_limit=8 * sweep.MIB)
            self.assertEqual(exit_code, 0)
            self.assertIsNone(reason)
            self.assertEqual((cache / "inductor" / "compiled_blob").stat().st_size, 9 * sweep.MIB)
            self.assertEqual(log.stat().st_size, 8 * sweep.MIB)
            self.assertTrue(capture["truncated"])
            self.assertGreater(capture["discarded_bytes"], sweep.MIB)

    def test_real_child_timeout_cleanup_and_project_local_caches(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            log = directory / "worker.log"
            command = [sys.executable, "-u", "-c",
                       "import os,time;print(os.environ['HF_HUB_OFFLINE'],os.environ['CUDA_CACHE_PATH'],flush=True);time.sleep(30)"]
            code, reason, elapsed, capture = sweep.run_process(command, log, .2, lambda: None, directory / "cache")
            self.assertNotEqual(code, 0)
            self.assertEqual(reason, "profile_wall_timeout")
            self.assertLess(elapsed, 8)
            self.assertIn(str(directory / "cache" / "cuda"), log.read_text())
            self.assertFalse(capture["truncated"])

    def test_cache_has_separate_cap_but_is_in_total_footprint(self):
        cfg = configuration()
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            (directory / "compile_cache").mkdir()
            (directory / "compile_cache" / "kernel").write_bytes(b"x" * 100)
            (directory / "worker.log").write_bytes(b"z" * 10)
            self.assertEqual(sweep.tree_sizes(directory), (10, 10, 100))
            with patch.object(sweep, "tree_sizes", return_value=(1, 1, 4 * sweep.GIB)), \
                 patch.object(sweep.shutil, "disk_usage", return_value=SimpleNamespace(free=100 * sweep.GIB)):
                self.assertEqual(sweep.storage_reason(cfg, directory), "compile_cache_limit")

    def suite_fixture(self, directory):
        cfg = configuration()
        files = {"model_config": "{}", "data_manifest": '{"source":"local"}',
                 "environment_preflight": '{"packages":{"torch":"2.8","transformers":"4.57.1"}}'}
        for key, contents in files.items():
            path = directory / (key + ".json")
            path.write_text(contents)
            cfg[key] = str(path.relative_to(sweep.ROOT))
            cfg[key + "_sha256"] = sweep.sha256(path)
        pack, runner = directory / "tokens.bin", directory / "runner.py"
        with pack.open("wb") as handle:
            handle.truncate(64_000_000 * 4)
        runner.write_text("# CPU simulation\n")
        cfg.update(data_pack=str(pack.relative_to(sweep.ROOT)), data_pack_sha256="a" * 64,
                   runner_sha256=sweep.sha256(runner))
        config_path = directory / "config.json"
        sweep.write_json(config_path, cfg)
        args = SimpleNamespace(config=config_path, world_size=8, gpu_type="a100", output_dir=directory / "job_cpu_test")
        actual_sha = sweep.sha256
        def bound_sha(path):
            return cfg["data_pack_sha256"] if Path(path) == pack else actual_sha(path)
        return cfg, args, runner, bound_sha

    def test_cpu_suite_confirms_real_data_and_resume_never_repeats_attempts(self):
        with tempfile.TemporaryDirectory(dir=sweep.ROOT / "experiments") as temporary:
            directory = Path(temporary)
            cfg, args, runner, bound_sha = self.suite_fixture(directory)
            def simulated(command, log, timeout, guard, cache):
                output = Path(command[command.index("--output") + 1])
                state = json.loads((args.output_dir / "suite_state.json").read_text())
                real_data = "--input-token-pack" in command
                container = state["confirmations"] if real_data else state["attempted_profiles"]
                profile = container[output.parent.name]
                result = result_for(profile, cfg, real_data=real_data,
                                    seconds=600 if real_data else (60 if profile["name"] == "flash" else 70))
                sweep.write_json(output, result)
                return 0, None, 700 if real_data else 90, {"truncated": False}
            with patch.object(sweep, "REGISTRY", directory), patch.object(sweep, "RUNNER", runner), \
                 patch.object(sweep, "sha256", side_effect=bound_sha), \
                 patch.object(sweep, "storage_reason", return_value=None), \
                 patch.object(sweep, "run_process", side_effect=simulated) as run:
                self.assertEqual(sweep.run_suite(args), 0)
                result = json.loads((args.output_dir / "results.json").read_text())
                self.assertEqual(result["status"], "completed")
                self.assertEqual(result["throughput"]["measured_wall_seconds"], 600)
                self.assertEqual(result["suite"]["short_sweep_winner"]["name"], "flash")
                self.assertEqual(len(result["suite"]["real_data_confirmations"]), 2)
                deadline = result["suite"]["deadline_epoch"]
                self.assertEqual(run.call_count, 4)
                self.assertEqual(sweep.run_suite(args), 0)
                self.assertEqual(run.call_count, 4)
                self.assertEqual(json.loads((args.output_dir / "results.json").read_text())["suite"]["deadline_epoch"], deadline)

    def test_short_probes_stop_with_confirmation_reserve_preserved(self):
        with tempfile.TemporaryDirectory(dir=sweep.ROOT / "experiments") as temporary:
            directory = Path(temporary)
            cfg, args, runner, bound_sha = self.suite_fixture(directory)
            cfg["profiles"] += [dict(name=f"probe_{n}", parent="baseline", role="tuning", features={},
                                     microbatch_per_gpu=4, accumulation=1) for n in range(16)]
            sweep.write_json(args.config, cfg)
            clock = [1_000_000.]
            def simulated(command, log, timeout, guard, cache):
                output = Path(command[command.index("--output") + 1])
                state = json.loads((args.output_dir / "suite_state.json").read_text())
                real_data = "--input-token-pack" in command
                container = state["confirmations"] if real_data else state["attempted_profiles"]
                profile = container[output.parent.name]
                sweep.write_json(output, result_for(profile, cfg, real_data=real_data))
                elapsed = 700 if real_data else min(400, timeout)
                clock[0] += elapsed
                return 0, None, elapsed, {"truncated": False}
            with patch.object(sweep, "REGISTRY", directory), patch.object(sweep, "RUNNER", runner), \
                 patch.object(sweep, "sha256", side_effect=bound_sha), \
                 patch.object(sweep, "storage_reason", return_value=None), \
                 patch.object(sweep.time, "time", side_effect=lambda: clock[0]), \
                 patch.object(sweep, "run_process", side_effect=simulated):
                self.assertEqual(sweep.run_suite(args), 0)
                result = json.loads((args.output_dir / "results.json").read_text())
                self.assertEqual(result["suite"]["short_stop_reason"], "reserved_for_real_data_confirmations")
                self.assertTrue(any(p["status"] == "skipped" for p in result["suite"]["short_probe_profiles"]))
                self.assertTrue(all(p["status"] == "completed" for p in result["suite"]["real_data_confirmations"]))
                self.assertLessEqual(clock[0], 1_006600.)

    def test_expired_resume_launches_nothing(self):
        with tempfile.TemporaryDirectory(dir=sweep.ROOT / "experiments") as temporary:
            directory = Path(temporary)
            cfg, args, runner, bound_sha = self.suite_fixture(directory)
            with patch.object(sweep, "REGISTRY", directory), patch.object(sweep, "RUNNER", runner), \
                 patch.object(sweep, "sha256", side_effect=bound_sha), \
                 patch.object(sweep, "storage_reason", return_value=None), \
                 patch.object(sweep, "run_process") as run:
                _, _, binding = sweep.configuration(args)
                args.output_dir.mkdir()
                state = sweep.load_state(args.output_dir / "suite_state.json", binding, 6600, 1)
                sweep.write_json(args.output_dir / "suite_state.json", state)
                self.assertEqual(sweep.run_suite(args), 1)
                self.assertEqual(run.call_count, 0)
                self.assertEqual(json.loads((args.output_dir / "suite_state.json").read_text())["deadline_epoch"], 6601)

    def test_config_rejects_blackwell_recipes_on_a100_and_insufficient_confirmation_reserve(self):
        with tempfile.TemporaryDirectory(dir=sweep.ROOT / "experiments") as temporary:
            directory = Path(temporary)
            cfg, args, runner, bound_sha = self.suite_fixture(directory)
            with patch.object(sweep, "RUNNER", runner), patch.object(sweep, "sha256", side_effect=bound_sha):
                sweep.configuration(args)
                for case in ("precision", "reserve", "data_hash"):
                    candidate = copy.deepcopy(cfg)
                    if case == "precision":
                        candidate["profiles"][1]["features"]["precision"] = "mxfp8"
                    elif case == "reserve":
                        candidate["bounds"]["confirmation_reserve_seconds"] = 1000
                    else:
                        candidate["data_pack_sha256"] = "wrong"
                    sweep.write_json(args.config, candidate)
                    with self.subTest(case=case), self.assertRaises(ValueError):
                        sweep.configuration(args)


if __name__ == "__main__":
    unittest.main()
