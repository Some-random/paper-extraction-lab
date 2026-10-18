import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


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


if __name__ == "__main__":
    unittest.main()
