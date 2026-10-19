import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


PATH = Path(__file__).resolve().parents[1] / "scripts" / "benchmark_4b_training.py"
SPEC = importlib.util.spec_from_file_location("training_throughput", PATH)
benchmark = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(benchmark)


class TrainingThroughputTests(unittest.TestCase):
    def test_total_throughput_uses_wall_time_and_all_accumulation_microbatches(self):
        result = benchmark.summarize([2., 3.], 6., world_size=8, batch_size=1,
                                     sequence_length=4096, accumulation=4,
                                     target_tokens=200_000_000_000)
        self.assertEqual(result["input_tokens_per_step"], 131072)
        self.assertEqual(result["measured_input_tokens"], 262144)
        self.assertAlmostEqual(result["input_tokens_per_second"], 262144 / 6)
        self.assertEqual(result["extrapolation"]["gpu_count"], 8)
        self.assertAlmostEqual(result["extrapolation"]["days"], 200_000_000_000 / (262144 / 6) / 86400)

    def test_percentiles_interpolate_and_one_observation_is_valid(self):
        self.assertEqual(benchmark.percentile([3, 1, 2], .5), 2)
        self.assertAlmostEqual(benchmark.percentile([1, 2, 3], .95), 2.9)
        self.assertEqual(benchmark.percentile([7], .95), 7)

    def test_invalid_or_empty_measurements_cannot_produce_successful_estimate(self):
        dimensions = dict(world_size=1, batch_size=1, sequence_length=4096,
                          accumulation=1, target_tokens=200_000_000_000)
        for times, elapsed in (([], 1), ([0], 1), ([float("nan")], 1),
                               ([1], 0), ([1], float("inf"))):
            with self.subTest(times=times, elapsed=elapsed), self.assertRaises(ValueError):
                benchmark.summarize(times, elapsed, **dimensions)
        with self.assertRaises(ValueError):
            benchmark.summarize([1], 1, **{**dimensions, "world_size": 0})

    def test_atomic_json_rejects_nonfinite_data(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "nested" / "result.json"
            benchmark.write_json(output, {"status": "failed", "failure_type": "OutOfMemoryError"})
            self.assertEqual(json.loads(output.read_text())["status"], "failed")
            with self.assertRaises(ValueError):
                benchmark.write_json(output, {"seconds": float("nan")})
            self.assertEqual(json.loads(output.read_text())["status"], "failed")

    def test_diagnostic_flags_preserve_original_defaults_and_accept_explicit_alternatives(self):
        required = ["--model-config", "model.json", "--output", "result.json"]
        defaults = benchmark.arguments(required)
        self.assertEqual(defaults.activation_checkpointing, "on")
        self.assertEqual(defaults.sharding, "full_shard")
        self.assertEqual(defaults.profile_steps, 0)
        changed = benchmark.arguments(required + ["--activation-checkpointing", "off",
                                                  "--sharding", "shard_grad_op", "--profile-steps", "1"])
        self.assertEqual(changed.activation_checkpointing, "off")
        self.assertEqual(changed.sharding, "shard_grad_op")
        self.assertEqual(changed.profile_steps, 1)

    def test_phase_milestones_use_monotonic_time_and_include_rank(self):
        emitted = []
        result = {}
        with patch.dict("os.environ", {"RANK": "7"}):
            event = benchmark.phase_event(result, 100., "cpu_model_initialize_start", clock=lambda: 102.5,
                                           emit=lambda value, **kwargs: emitted.append(json.loads(value)))
        self.assertEqual(event["elapsed_seconds"], 2.5)
        self.assertEqual(event["rank"], 7)
        self.assertEqual(result["phase_timings"], [event])
        self.assertEqual(emitted, [event])

    def test_compact_profiler_keeps_important_ops_and_actual_kernel_names_with_bounds(self):
        events = [SimpleNamespace(key=f"aten::ordinary_{index}", count=1,
                                  self_cpu_time_total=1000. - index, cpu_time_total=1200.,
                                  self_device_time_total=1000. - index, device_time_total=2000.)
                  for index in range(150)]
        for name in ("aten::_scaled_dot_product_flash_attention", "nccl:all_gather", "aten::cross_entropy_loss"):
            events.append(SimpleNamespace(key=name, count=1, self_cpu_time_total=1., cpu_time_total=2.,
                                          self_device_time_total=1., device_time_total=2.))
        kernels = [SimpleNamespace(kernels=[SimpleNamespace(name="flash_fwd_kernel", duration=12.5),
                                             SimpleNamespace(name="ncclDevKernel_AllGather", duration=7.5)])]
        result = benchmark.compact_profile(events, maximum_entries=20, kernel_events=kernels)
        self.assertLessEqual(len(result["operators"]) + len(result["cuda_kernels"]), 20)
        self.assertTrue(result["truncated"])
        by_name = {row["name"]: row for row in result["operators"]}
        self.assertEqual(by_name["aten::_scaled_dot_product_flash_attention"]["categories"], ["attention"])
        self.assertEqual(by_name["nccl:all_gather"]["categories"], ["communication"])
        self.assertEqual(by_name["aten::cross_entropy_loss"]["categories"], ["loss"])
        self.assertEqual(result["cuda_kernels"][0]["name"], "flash_fwd_kernel")
        self.assertEqual(result["cuda_kernels"][0]["device_total_us"], 12.5)
        self.assertLess(len(json.dumps(result).encode()), 500_000)
        tiny = benchmark.compact_profile(events, maximum_bytes=512, kernel_events=kernels)
        self.assertLessEqual(len(json.dumps(tiny).encode()), 512)

    def test_compact_profiler_handles_legacy_cuda_fields_and_nonfinite_times(self):
        event = SimpleNamespace(key="old_backend", count=2, self_cpu_time_total=float("nan"),
                                cpu_time_total=3., self_cuda_time_total=5., cuda_time_total=8.)
        result = benchmark.compact_profile([event])
        self.assertEqual(result["operators"][0]["self_cpu_us"], 0.)
        self.assertEqual(result["operators"][0]["self_device_us"], 5.)
        self.assertEqual(result["operators"][0]["device_total_us"], 8.)
        with self.assertRaises(ValueError):
            benchmark.compact_profile([event], maximum_entries=101)


if __name__ == "__main__":
    unittest.main()
