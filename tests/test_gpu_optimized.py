import importlib.util
import array
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("gpu_optimized", ROOT / "scripts/benchmark_gpu_optimized.py")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class OptimizedRecipeTests(unittest.TestCase):
    def test_real_measurement_requires_completed_updates_and_full600_seconds(self):
        args = SimpleNamespace(steps=8, minimum_measured_seconds=600.)
        self.assertFalse(runner.complete_measurement(8, 599.99, args))
        self.assertFalse(runner.complete_measurement(7, 900., args))
        self.assertTrue(runner.complete_measurement(8, 600., args))
        self.assertTrue(runner.complete_measurement(150, 603., args))

    def test_global_rank_partition_covers32_sequences_once_for_all_microbatches(self):
        for microbatch in (1, 2, 4):
            accumulation = 32 // (8 * microbatch)
            ranges = []
            for rank in range(8):
                for micro in range(accumulation):
                    first, last = runner.global_token_slice(0, micro, rank=rank, world_size=8,
                                    batch_size=microbatch, accumulation=accumulation,
                                    sequence_length=4, available_tokens=256)
                    ranges.extend(range(first, last))
            self.assertEqual(sorted(ranges), list(range(128)))
            first, last = runner.global_token_slice(1, 0, rank=0, world_size=8,
                            batch_size=microbatch, accumulation=accumulation,
                            sequence_length=4, available_tokens=256)
            self.assertEqual(first, 128)

    def test_every_rank_rejects_incomplete_global_batch_without_replay(self):
        for rank in range(8):
            with self.subTest(rank=rank), self.assertRaises(runner.TokenPackExhausted):
                runner.global_token_slice(1, 0, rank=rank, world_size=8, batch_size=4,
                                          accumulation=1, sequence_length=4, available_tokens=255)

    def test_pack_checksum_and_vocabulary_are_validated_before_mmap(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            token_path = directory / "tokens.uint32"
            token_path.write_bytes(array.array("I", [1, 2, 3, 4]).tobytes())
            digest = hashlib.sha256(token_path.read_bytes()).hexdigest()
            manifest_path = directory / "manifest.json"
            manifest = dict(status="completed", dtype="uint32_le", pack_sha256=digest,
                            token_count=4, maximum_token_id=4)
            manifest_path.write_text(json.dumps(manifest))
            args = SimpleNamespace(input_token_pack=token_path, input_token_pack_sha256=digest,
                                   data_manifest=manifest_path)
            checked = runner.verify_token_pack(args, 7)
            self.assertFalse(checked["replay"])
            token_path.write_bytes(array.array("I", [1, 2, 3, 5]).tobytes())
            with self.assertRaisesRegex(ValueError, "hash"):
                runner.verify_token_pack(args, 7)

    def test_chunk_rates_use_observed_wall_endpoints_and_preserve_partial_tail(self):
        chunks = runner.chunk_rates([20., 40., 65., 85., 110., 130., 140.], 100)
        self.assertEqual([row["input_tokens"] for row in chunks], [300, 300, 100])
        self.assertEqual([row["seconds"] for row in chunks], [65., 65., 10.])
        self.assertTrue(chunks[-1]["partial_window"])
        self.assertAlmostEqual(chunks[0]["input_tokens_per_second"], 300 / 65)

    def test_a100_rejects_blackwell_only_recipes_and_nonzero_cursor(self):
        common = ["--hardware", "a100", "--model-config", "model.json", "--output", "results.json"]
        for flags in (["--attention", "flash_attn4"],
                      ["--precision", "float8_tensorwise", "--sharding", "fsdp2"],
                      ["--input-start-token", "1"]):
            with self.subTest(flags=flags), self.assertRaises(SystemExit):
                runner.arguments(common + flags)

    def test_workload_rejects_smaller_token_batches_and_model_architecture_changes(self):
        args = runner.arguments(["--hardware", "b200", "--model-config", "config.json", "--output", "result.json",
                                 "--batch-size", "4", "--accumulation", "4"])
        config = json.loads((ROOT / "config/qwen3_4b_throughput_model.json").read_text())
        runner.validate_workload(args, 2, config)
        with self.assertRaisesRegex(ValueError, "32 sequences"):
            runner.validate_workload(args, 1, config)
        for altered in ({"vocab_size": 32000}, {"head_dim": 64}, {"tie_word_embeddings": False},
                        {"attention_dropout": .1}, {"use_sliding_window": True}):
            with self.subTest(altered=altered), self.assertRaises(ValueError):
                runner.validate_workload(args, 2, {**config, **altered})

    def test_recipe_flags_keep_precisions_and_sharding_explicit(self):
        common = ["--hardware", "b200", "--model-config", "config.json", "--output", "result.json"]
        args = runner.arguments(common + ["--checkpointing", "selective", "--kernels", "cce",
                                          "--sharding", "fsdp2", "--compile", "on",
                                          "--precision", "mxfp8"])
        self.assertEqual(args.activation_checkpointing, "selective")
        self.assertEqual(args.fused_kernels, "cce")
        self.assertEqual(args.compile, "on")
        self.assertEqual(args.precision, "mxfp8")
        self.assertEqual(args.optimizer, "adamw_fp32")
        changed = runner.arguments(common + ["--optimizer", "adamw_8bit"])
        self.assertEqual(changed.optimizer, "adamw_8bit")
        for flags in (["--precision", "float8_tensorwise"],
                      ["--float8-all-gather", "on"], ["--sequence-length", "1024"]):
            with self.subTest(flags=flags), self.assertRaises(SystemExit):
                runner.arguments(common + flags)

    def test_missing_feature_never_returns_a_fallback(self):
        with self.assertRaises(runner.UnsupportedFeature):
            runner.require_symbol("this_package_must_not_exist", "training")
        with self.assertRaises(runner.UnsupportedFeature):
            runner.require_symbol("json", "imaginary_fp8_training")
        args = SimpleNamespace(precision="nvfp4")
        with self.assertRaisesRegex(runner.UnsupportedFeature, "no emulated or BF16 fallback"):
            runner.low_precision_converter(None, args, {})

    def test_forced_attention_cannot_claim_success_from_a_fallback_kernel(self):
        efficient = {"operators": [{"name": "aten::_efficient_attention_forward"}], "cuda_kernels": []}
        with self.assertRaises(runner.UnsupportedFeature):
            runner.assert_attention_evidence(efficient, "sdpa_flash")
        with self.assertRaises(runner.UnsupportedFeature):
            runner.assert_attention_evidence(efficient, "sdpa_cudnn")
        flash = {"operators": [{"name": "aten::_scaled_dot_product_flash_attention"}], "cuda_kernels": []}
        proof = runner.assert_attention_evidence(flash, "sdpa_flash")
        self.assertEqual(proof["status"], "observed")
        self.assertIn("flash_attention", proof["actual_attention_names"][0])

    def test_elapsed_training_rate_includes_all_microbatches_and_excludes_setup(self):
        rate = runner.summarize([1., 1.], 2.2, world_size=2, batch_size=4,
                                accumulation=4, sequence_length=4096, target_tokens=200_000_000_000)
        self.assertEqual(rate["measured_input_tokens"], 262144)
        self.assertAlmostEqual(rate["input_tokens_per_second"], 262144 / 2.2)


try:
    import torch
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "CPU numerical checks require the pinned torch environment")
class NumericalGuardTests(unittest.TestCase):
    def test_optimizer_rejects_low_precision_master_weights(self):
        weight = torch.nn.Parameter(torch.ones(4, dtype=torch.bfloat16))
        with self.assertRaisesRegex(RuntimeError, "FP32 master"):
            runner.make_optimizer(torch, [weight], "adamw_fp32")

    def test_quantized_state_reports_physical_codes_separately_from_logical_dtype(self):
        state = SimpleNamespace(dtype=torch.float32,
                                codes=torch.zeros(4096, dtype=torch.uint8),
                                scale=torch.ones(16, dtype=torch.float32))
        fake = SimpleNamespace(state={"parameter": {"exp_avg": state, "exp_avg_sq": state}})
        rows = runner.optimizer_encoding(fake)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["logical_dtype"], "torch.float32")
        self.assertEqual(rows[0]["codes_dtype"], "torch.uint8")
        self.assertEqual(rows[0]["scale_dtype"], "torch.float32")

    def test_finite_guard_accepts_roundoff_and_rejects_wrong_gradients(self):
        expected = torch.tensor([1., 0., -2., .1])
        report = runner.comparison_metrics(torch, expected + 1e-5, expected,
                                           relative_tolerance=.001, absolute_tolerance=1e-4)
        self.assertEqual(report["status"], "passed")
        for actual in (-expected, torch.zeros_like(expected),
                       torch.tensor([float("nan"), 0., 0., 0.])):
            with self.subTest(actual=actual), self.assertRaises(runner.NumericalMismatch):
                runner.comparison_metrics(torch, actual, expected,
                                           relative_tolerance=.01, absolute_tolerance=.001)

    def test_loss_smoke_checks_both_hidden_and_classifier_gradients(self):
        def correct(hidden, weight, labels):
            return torch.nn.functional.cross_entropy(hidden.float() @ weight.float().T, labels)
        report = runner.numerical_loss_smoke(torch, correct, torch.device("cpu"))
        self.assertEqual(report["status"], "passed")
        self.assertEqual(len(report["gradients"]), 2)
        with self.assertRaises(runner.NumericalMismatch):
            runner.numerical_loss_smoke(torch, lambda h, w, y: correct(h, w, y) * 2,
                                        torch.device("cpu"))

    def test_causal_loss_adapter_shifts_once_and_preserves_tied_weight_gradient(self):
        try:
            from transformers.modeling_outputs import CausalLMOutputWithPast
        except ImportError:
            self.skipTest("Requires pinned Transformers")

        class Body(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.embed_tokens = torch.nn.Embedding(7, 4)

            def forward(self, input_ids, use_cache=False):
                return SimpleNamespace(last_hidden_state=self.embed_tokens(input_ids))

        class Model(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.model = Body()
                self.lm_head = torch.nn.Linear(4, 7, bias=False)
                self.lm_head.weight = self.model.embed_tokens.weight
                self.config = SimpleNamespace(hidden_size=4)

        model = Model()
        ids = torch.tensor([[1, 2, 3, 4], [4, 2, 1, 6]])
        original_hidden = model.model(ids).last_hidden_state
        expected = torch.nn.functional.cross_entropy(
            (original_hidden[:, :-1] @ model.lm_head.weight.T).reshape(-1, 7), ids[:, 1:].reshape(-1))
        expected_gradient = torch.autograd.grad(expected, model.lm_head.weight)[0]

        def fused(hidden, weight, targets):
            return torch.nn.functional.cross_entropy(hidden @ weight.T, targets)
        runner.install_loss(model, fused)
        output = model(input_ids=ids, labels=ids)
        self.assertIsInstance(output, CausalLMOutputWithPast)
        self.assertTrue(torch.allclose(output.loss, expected))
        gradient = torch.autograd.grad(output.loss, model.model.embed_tokens.weight)[0]
        self.assertTrue(torch.allclose(gradient, expected_gradient))
        with self.assertRaisesRegex(ValueError, "causal labels"):
            model(input_ids=ids, labels=None)

    def test_selective_checkpointing_saves_matmul_and_recomputes_pointwise(self):
        class Model:
            def gradient_checkpointing_enable(self, gradient_checkpointing_kwargs):
                self.kwargs = gradient_checkpointing_kwargs
        model = Model()
        recipe = runner.configure_checkpointing(model, "selective", torch)
        self.assertIn("selective", recipe["kind"])
        self.assertIn("context_fn", model.kwargs)
        # Real selective checkpoint contexts must be distinct save/recompute modes.
        save, recompute = model.kwargs["context_fn"]()
        self.assertNotEqual(type(save), type(recompute))


if __name__ == "__main__":
    unittest.main()
