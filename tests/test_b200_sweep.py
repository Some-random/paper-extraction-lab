import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import signal
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[1] / "scripts/benchmark_b200_sweep.py"
SPEC = importlib.util.spec_from_file_location("b200_sweep", PATH)
sweep = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sweep)

BASE_FEATURES = dict(attention="sdpa_auto", kernels="none", checkpointing="full",
                     sharding="full_shard", compile="off", precision="bf16", float8_all_gather="off", optimizer="adamw_fp32")


def config():
    return dict(world_size=2, sequence_length=4096, global_batch_sequences=32,
                warmup_optimizer_steps=3, measured_optimizer_steps=8,
                model_config_sha256="model-hash", runner_sha256="runner-hash",
                baseline_environment_and_artifact_bytes=7 * sweep.GIB, baseline_checked_epoch=1,
                bounds=dict(suite_seconds=6600, profile_seconds=420, compile_profile_seconds=900,
                            new_log_bytes=64 * sweep.MIB, new_run_artifact_bytes=256 * sweep.MIB,
                            new_compile_cache_bytes=4 * sweep.GIB,
                            new_environment_and_artifact_bytes=16 * sweep.GIB,
                            minimum_free_bytes=64 * sweep.GIB),
                profiles=[dict(name="baseline", parent=None, role="baseline", features=BASE_FEATURES.copy(),
                               microbatch_per_gpu=4, accumulation=4),
                          dict(name="flash", parent="baseline", role="tuning", features={"attention": "sdpa_flash"},
                               microbatch_per_gpu=4, accumulation=4),
                          dict(name="compile", parent="@best", role="combination", features={"compile": "on"},
                               microbatch_per_gpu=4, accumulation=4)])


def completed_result(profile, rate=15000):
    args = dict(sequence_length=4096, batch_size=profile["microbatch_per_gpu"], accumulation=profile["accumulation"])
    args.update({sweep.ARGUMENTS.get(key, key): value for key, value in profile["features"].items()})
    return dict(status="completed", world_size=2, arguments=args,
                config_sha256="model-hash", runner_sha256="runner-hash",
                hardware=[{"gpu": "NVIDIA B200"}, {"gpu": "NVIDIA B200"}],
                completed_warmup_steps=3, setup_seconds=20., warmup_seconds=30., compile_seconds=10.,
                measurement_seconds=70., smoke_checks={"status": "passed"},
                optimizer_update_check={"status": "passed"},
                throughput=dict(input_tokens_per_second=rate, input_tokens_per_step=131072,
                                measured_optimizer_steps=8, measured_input_tokens=1048576,
                                measured_wall_seconds=70.))


class B200SweepTests(unittest.TestCase):
    def result_record(self, profile, result, code=0, reason=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.json"
            sweep.write_json(path, result)
            return sweep.profile_result(profile, path, code, reason, world_size=2, config=config())

    def baseline(self):
        cfg = config()
        return sweep.resolve_profile(cfg["profiles"][0], cfg["profiles"], {"attempted_profiles": {}})

    def test_profiles_require_matched_batch_ordered_parents_and_single_baseline(self):
        cfg = config()
        self.assertEqual(sweep.validate_profiles(cfg, 2), cfg["profiles"])
        for case in ("batch", "parent", "baseline", "name", "feature", "adaptive_baseline"):
            candidate = copy.deepcopy(cfg)
            if case == "batch":
                candidate["profiles"][1]["accumulation"] = 8
            elif case == "parent":
                candidate["profiles"][1]["parent"] = "future"
            elif case == "baseline":
                candidate["profiles"][1]["role"] = "baseline"
            elif case == "name":
                candidate["profiles"][1]["name"] = "../escape"
            elif case == "feature":
                candidate["profiles"][1]["features"] = {"precision": "unknown"}
            else:
                candidate["profiles"][0]["features"]["attention"] = "@best:attention"
            with self.subTest(case=case), self.assertRaises(ValueError):
                sweep.validate_profiles(candidate, 2)

    def test_resume_preserves_deadline_and_rejects_changed_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            first = sweep.load_state(path, {"hash": "a"}, 6600, 1000)
            sweep.write_json(path, first)
            self.assertEqual(sweep.load_state(path, {"hash": "a"}, 6600, 100000)["deadline_epoch"], 7600)
            with self.assertRaises(ValueError):
                sweep.load_state(path, {"hash": "b"}, 6600, 100000)

    def test_adaptive_parent_uses_only_completed_winner_and_records_feature_origin(self):
        cfg, baseline = config(), self.baseline()
        state = {"attempted_profiles": {"baseline": dict(baseline, status="completed", input_tokens_per_second=15000)}}
        flash = sweep.resolve_profile(cfg["profiles"][1], cfg["profiles"], state)
        state["attempted_profiles"]["flash"] = dict(flash, status="completed", input_tokens_per_second=24000)
        state["attempted_profiles"]["failed_fast"] = dict(flash, name="failed_fast", status="failed", input_tokens_per_second=99000)
        compiled = sweep.resolve_profile(cfg["profiles"][2], cfg["profiles"], state)
        self.assertEqual(compiled["resolved_parent"], "flash")
        self.assertEqual(compiled["features"]["attention"], "sdpa_flash")
        self.assertEqual(compiled["feature_sources"]["attention"], "flash")
        self.assertEqual(compiled["changed_features"], ["compile"])
        plan = dict(name="combo", parent="baseline", role="combination", features={"attention": "@best:attention"},
                    microbatch_per_gpu=4, accumulation=4)
        self.assertEqual(sweep.resolve_profile(plan, cfg["profiles"] + [plan], state)["features"]["attention"], "sdpa_flash")
        state["attempted_profiles"]["flash"]["input_tokens_per_second"] = 10000
        self.assertEqual(sweep.resolve_profile(plan, cfg["profiles"] + [plan], state)["features"]["attention"], "sdpa_auto")

    def test_adaptive_combination_can_merge_distinct_attention_and_loss_winners(self):
        cfg, baseline = config(), self.baseline()
        plans = [cfg["profiles"][0], cfg["profiles"][1],
                 dict(name="liger", parent="baseline", role="tuning", features={"kernels": "liger_loss"},
                      microbatch_per_gpu=4, accumulation=4)]
        combo = dict(name="combined", parent="baseline", role="combination",
                     features={"attention": "@best:attention", "kernels": "@best:kernels"},
                     feature_candidates={"attention": ["baseline", "flash"], "kernels": ["baseline", "liger"]},
                     microbatch_per_gpu=4, accumulation=4)
        cfg["profiles"] = plans + [combo]
        sweep.validate_profiles(cfg, 2)
        state = {"attempted_profiles": {}}
        for plan, rate in zip(plans, (15000, 24000, 22000)):
            profile = sweep.resolve_profile(plan, cfg["profiles"], state)
            state["attempted_profiles"][profile["name"]] = dict(profile, status="completed", input_tokens_per_second=rate)
        result = sweep.resolve_profile(combo, cfg["profiles"], state)
        self.assertEqual(result["features"]["attention"], "sdpa_flash")
        self.assertEqual(result["features"]["kernels"], "liger_loss")
        self.assertEqual(result["feature_sources"]["attention"], "flash")
        self.assertEqual(result["feature_sources"]["kernels"], "liger")
        state["attempted_profiles"]["liger"]["status"] = "failed"
        self.assertEqual(sweep.resolve_profile(combo, cfg["profiles"], state)["features"]["kernels"], "none")
        combo["feature_candidates"]["attention"].append("future")
        with self.assertRaises(ValueError):
            sweep.validate_profiles(cfg, 2)

    def test_timeout_unavailable_and_nonzero_exit_cannot_supply_rate(self):
        profile = self.baseline()
        for code, reason, failure, status in ((-15, "profile_wall_timeout", None, "failed"),
                                             (1, None, "UnsupportedFeature", "unavailable"),
                                             (1, None, "OutOfMemoryError", "failed"),
                                             (0, "compile_cache_limit", None, "failed")):
            result = completed_result(profile)
            if failure:
                result.update(status="failed", failure_type=failure)
            record = self.result_record(profile, result, code, reason)
            self.assertEqual(record["status"], status)
            self.assertNotIn("throughput", record)
            self.assertNotIn("input_tokens_per_second", record)

    def test_smoke_optimizer_hardware_hash_and_fixed_shape_are_enforced(self):
        profile = self.baseline()
        for case in ("smoke", "update", "hardware", "model", "runner", "warmup", "steps", "tokens", "feature", "rate"):
            result = completed_result(profile)
            if case == "smoke":
                result["smoke_checks"]["status"] = "failed"
            elif case == "update":
                result["optimizer_update_check"]["status"] = "failed"
            elif case == "hardware":
                result["hardware"][0]["gpu"] = "NVIDIA A100"
            elif case in ("model", "runner"):
                result["config_sha256" if case == "model" else "runner_sha256"] = "changed"
            elif case == "warmup":
                result["completed_warmup_steps"] = 2
            elif case == "steps":
                result["throughput"]["measured_optimizer_steps"] = 1
            elif case == "tokens":
                result["throughput"]["measured_input_tokens"] = 5000
            elif case == "feature":
                result["arguments"]["precision"] = "mxfp8"
            else:
                result["throughput"]["input_tokens_per_second"] = 0
            with self.subTest(case=case):
                self.assertEqual(self.result_record(profile, result)["status"], "failed")
        record = self.result_record(profile, completed_result(profile))
        self.assertEqual(record["status"], "completed")
        self.assertEqual(record["warmup_seconds"], 30.)
        self.assertEqual(record["measurement_seconds"], 70.)

    def test_baseline_and_tuned_winner_remain_separate(self):
        cfg = config()
        state = dict(configuration={"world_size": 2}, started_epoch=1, deadline_epoch=6601,
                     started_utc="2026-10-19T00:00:00+00:00", attempted_profiles={})
        for plan, rate in zip(cfg["profiles"], (15000, 24000, 22000)):
            profile = sweep.resolve_profile(plan, cfg["profiles"], state)
            state["attempted_profiles"][plan["name"]] = self.result_record(profile, completed_result(profile, rate))
        summary = sweep.summarize(state, cfg["profiles"], 500)
        self.assertEqual(summary["baseline_result"]["input_tokens_per_second"], 15000)
        self.assertEqual(summary["fastest_completed_profile_name"], "flash")
        self.assertAlmostEqual(summary["tuning_speedup_over_baseline"], 1.6)
        self.assertIn("compile-inclusive warmup", summary["rate_scope"])

    def test_live_snapshot_keeps_active_and_unattempted_profiles_distinct(self):
        cfg = config()
        profile = self.baseline()
        state = dict(configuration={"world_size": 2}, started_epoch=1, deadline_epoch=6601,
                     started_utc="2026-10-19T00:00:00+00:00",
                     attempted_profiles={"baseline": dict(profile, status="initializing")})
        live = sweep.summarize(state, cfg["profiles"], 10, terminal=False)
        self.assertEqual(live["status"], "running")
        self.assertEqual(live["profiles"][0]["status"], "initializing")
        self.assertEqual(live["profiles"][1]["status"], "pending")
        self.assertNotIn("failure_type", live["profiles"][1])
        final = sweep.summarize(state, cfg["profiles"], 7000)
        self.assertEqual(final["profiles"][0]["failure_type"], "InterruptedPreviousAttempt")
        self.assertEqual(final["profiles"][1]["status"], "skipped")

    def test_compile_cache_is_separate_but_counts_towards_total_and_free_floor(self):
        cfg = config()
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            (directory / "compile_cache").mkdir()
            (directory / "compile_cache" / "kernel").write_bytes(b"a" * 100)
            (directory / "worker.log").write_bytes(b"b" * 10)
            self.assertEqual(sweep.tree_sizes(directory), (10, 10, 100))
            for sizes, free, reason in (((1, 1, 4 * sweep.GIB), 100 * sweep.GIB, "compile_cache_limit"),
                                        ((255 * sweep.MIB, 1, 0), 100 * sweep.GIB, "new_artifact_limit"),
                                        ((1, 1, 0), 60 * sweep.GIB, "shared_free_space_floor")):
                with patch.object(sweep, "tree_sizes", return_value=sizes), \
                     patch.object(sweep.shutil, "disk_usage", return_value=SimpleNamespace(free=free)):
                    self.assertEqual(sweep.storage_reason(cfg, directory), reason)

    def test_child_command_keeps_global_shape_and_explicit_feature_flags(self):
        profile = self.baseline()
        command = sweep.child_command(profile, SimpleNamespace(world_size=2), config(),
                                      Path("model.json"), Path("result.json"), 420)
        self.assertIn("--nproc_per_node=2", command)
        for flag, value in (("--global-batch-sequences", "32"), ("--fused-kernels", "none"),
                            ("--activation-checkpointing", "full"), ("--precision", "bf16"),
                            ("--max-runtime-seconds", "410")):
            self.assertEqual(command[command.index(flag) + 1], value)

    def test_cpu_child_is_timed_out_cleaned_up_and_offline(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            log = directory / "worker.log"
            command = [sys.executable, "-u", "-c",
                       "import os,time; print(os.environ['HF_HUB_OFFLINE'],flush=True);time.sleep(30)"]
            code, reason, seconds = sweep.run_process(command, log, .15, lambda: None, directory / "cache")
            self.assertEqual(reason, "profile_wall_timeout")
            self.assertNotEqual(code, 0)
            self.assertLess(seconds, 6)
            self.assertEqual(log.read_text().strip(), "1")

    def test_cleanup_only_targets_owned_process_group(self):
        process = SimpleNamespace(pid=1234567, wait=lambda timeout: 0, poll=lambda: 0)
        with patch.object(sweep.os, "killpg") as kill:
            sweep.terminate_owned(process)
        self.assertEqual(kill.call_args_list,
                         [unittest.mock.call(1234567, signal.SIGTERM), unittest.mock.call(1234567, signal.SIGKILL)])

    def simulated_suite(self, interrupt_first=False, expired=False):
        with tempfile.TemporaryDirectory(dir=sweep.ROOT / "experiments") as directory:
            directory = Path(directory)
            model, runner = directory / "model.json", directory / "runner.py"
            model.write_text("{}")
            runner.write_text("# simulated runner\n")
            cfg = config()
            cfg.update(model_config=str(model.relative_to(sweep.ROOT)), model_config_sha256=sweep.sha256(model),
                       runner_sha256=sweep.sha256(runner))
            config_path = directory / "config.json"
            sweep.write_json(config_path, cfg)
            args = SimpleNamespace(config=config_path, world_size=2, output_dir=directory / "job_cpu_test")
            def simulated(command, log_path, timeout, guard, cache):
                output = Path(command[command.index("--output") + 1])
                state = json.loads((args.output_dir / "suite_state.json").read_text())
                profile = state["attempted_profiles"][output.parent.name]
                if output.parent.name == "flash":
                    result = dict(status="failed", failure_type="UnsupportedFeature")
                    code = 1
                else:
                    result = completed_result(profile, 15000 if output.parent.name == "baseline" else 23000)
                    result.update(config_sha256=cfg["model_config_sha256"], runner_sha256=cfg["runner_sha256"])
                    code = 0
                sweep.write_json(output, result)
                return code, None, .1
            with patch.object(sweep, "REGISTRY", directory), patch.object(sweep, "RUNNER", runner), \
                 patch.object(sweep, "storage_reason", return_value=None), \
                 patch.object(sweep, "run_process", side_effect=simulated) as run:
                if interrupt_first or expired:
                    _, _, binding = sweep.configuration(args)
                    args.output_dir.mkdir()
                    state = sweep.load_state(args.output_dir / "suite_state.json", binding, 6600, 1 if expired else __import__("time").time())
                    if interrupt_first:
                        profile = sweep.resolve_profile(cfg["profiles"][0], cfg["profiles"], state)
                        state["attempted_profiles"]["baseline"] = dict(profile, status="initializing")
                    sweep.write_json(args.output_dir / "suite_state.json", state)
                sweep.run_suite(args)
                state = json.loads((args.output_dir / "suite_state.json").read_text())
                result = json.loads((args.output_dir / "results.json").read_text())
                deadline = state["deadline_epoch"]
                calls = run.call_count
                sweep.run_suite(args)
                self.assertEqual(run.call_count, calls)
                self.assertEqual(json.loads((args.output_dir / "suite_state.json").read_text())["deadline_epoch"], deadline)
                if expired:
                    self.assertEqual(calls, 0)
                    self.assertEqual(result["suite"]["stop_reason"], "suite_deadline")
                elif interrupt_first:
                    self.assertEqual(calls, 2)
                    self.assertEqual(state["attempted_profiles"]["baseline"]["failure_type"], "InterruptedPreviousAttempt")
                    self.assertEqual(result["status"], "failed")
                    self.assertEqual(result["suite"]["fastest_completed_profile_name"], "compile")
                else:
                    self.assertEqual(calls, 3)
                    self.assertEqual(result["throughput"]["input_tokens_per_second"], 15000)
                    self.assertEqual(result["suite"]["fastest_completed_profile_name"], "compile")
                    self.assertEqual(state["attempted_profiles"]["flash"]["status"], "unavailable")

    def test_optional_backend_failure_does_not_block_independent_profiles_or_replace_baseline(self):
        self.simulated_suite()

    def test_interrupted_profile_is_not_retried_and_cannot_win(self):
        self.simulated_suite(interrupt_first=True)

    def test_expired_resume_submits_no_children_and_never_resets_deadline(self):
        self.simulated_suite(expired=True)


if __name__ == "__main__":
    unittest.main()
