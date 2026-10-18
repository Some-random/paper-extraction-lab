import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from biology_share import LABELS, estimate_biology_share


def record(shard, population, tokens, label, *, target=None, corpus="web", index=None):
    row = dict(corpus=corpus, shard_id=shard, shard_rows=population,
               source_tokens=tokens, target_tokens=tokens if target is None else target, label=label)
    if index is not None:
        row["row_index"] = index
    return row


class BiologyShareTests(unittest.TestCase):
    def test_unequal_shard_weights_and_document_lengths_change_token_share(self):
        rows = [record("large", 1000, 100, "biology"),
                record("large", 1000, 900, "other"),
                record("small", 10, 100, "biology"),
                record("small", 10, 100, "biology")]
        result = estimate_biology_share(rows)["corpora"]["web"]
        biology = result["categories"]["biology"]
        self.assertEqual(result["population_records"], 1010)
        self.assertEqual(result["token_totals"]["source_tokens"]["estimate"], 501000)
        self.assertEqual(biology["source_tokens"]["estimate"], 51000)
        self.assertAlmostEqual(biology["source_tokens"]["share"], 51000 / 501000)
        self.assertAlmostEqual(biology["documents"]["share"], 510 / 1010)
        self.assertNotAlmostEqual(biology["documents"]["share"], 3 / 4)
        self.assertGreater(biology["source_tokens"]["share_standard_error"], 0)

    def test_finite_census_has_zero_sampling_uncertainty(self):
        rows = [record("a", 2, 10, "biology"), record("a", 2, 30, "clinical"),
                record("b", 1, 20, "mixed")]
        result = estimate_biology_share(rows)["corpora"]["web"]
        for category in result["categories"].values():
            for unit in ("documents", "source_tokens", "target_tokens"):
                self.assertEqual(category[unit]["standard_error"], 0)
                self.assertEqual(category[unit]["share_standard_error"], 0)
                self.assertEqual(category[unit]["share_ci95"], [category[unit]["share"]] * 2)
        self.assertEqual(result["token_totals"]["source_tokens"]["ci95"], [60, 60])

    def test_fpc_and_ratio_residual_variance_are_calculated(self):
        rows = [record("a", 4, 10, "biology"), record("a", 4, 30, "other")]
        biology = estimate_biology_share(rows)["corpora"]["web"]["categories"]["biology"]
        # z=[7.5,-7.5], s_z^2=112.5, FPC=1/2, N=4, n=2, T_hat=80.
        expected_se = math.sqrt(4 ** 2 * 0.5 * 112.5 / 2) / 80
        self.assertAlmostEqual(biology["source_tokens"]["share_standard_error"], expected_se)
        self.assertEqual(biology["source_tokens"]["share_ci95"][0], 0)

    def test_categories_partition_totals_and_mixed_is_definition_sensitivity(self):
        rows = [record("a", 8, 10, "biology", target=20),
                record("a", 8, 20, "clinical", target=10),
                record("b", 12, 30, "other", target=60),
                record("b", 12, 40, "mixed", target=20)]
        result = estimate_biology_share(rows)["corpora"]["web"]
        for unit in ("source_tokens", "target_tokens"):
            categories = result["categories"]
            self.assertAlmostEqual(sum(categories[label][unit]["share"] for label in LABELS), 1)
            self.assertEqual(sum(categories[label][unit]["estimate"] for label in LABELS),
                             result["token_totals"][unit]["estimate"])
            self.assertAlmostEqual(categories["biology_plus_mixed"][unit]["share"],
                                   categories["biology"][unit]["share"] + categories["mixed"][unit]["share"])
        self.assertNotEqual(result["categories"]["biology"]["source_tokens"]["share"],
                            result["categories"]["biology"]["target_tokens"]["share"])

    def test_complete_labels_population_sizes_and_manifest_are_required(self):
        valid = [record("a", 10, 10, "biology"), record("a", 10, 20, "other")]
        mutations = [([], "empty"), (valid[:1], "at least two"),
                     ([dict(valid[0], label=None), valid[1]], "final"),
                     ([dict(valid[0], shard_rows=0), valid[1]], "positive integer"),
                     ([dict(valid[0], shard_rows=11), valid[1]], "inconsistent"),
                     ([dict(valid[0], shard_rows=1), dict(valid[1], shard_rows=1)], "exceeds"),
                     ([dict(valid[0], source_tokens=float("nan")), valid[1]], "finite")]
        for rows, message in mutations:
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                estimate_biology_share(rows)
        with self.assertRaisesRegex(ValueError, "frozen sampling manifest"):
            estimate_biology_share(valid, expected_sample_counts={"web": {"a": 2, "omitted": 2}})
        estimate_biology_share(valid, expected_sample_counts={"web": {"a": 2}})

    def test_external_projection_is_explicit_and_keeps_corpora_separate(self):
        rows = [record("a", 2, 10, "biology"), record("a", 2, 30, "other")]
        category = estimate_biology_share(rows)["corpora"]["web"]["categories"]["biology"]
        self.assertNotIn("source_total_projection", category)
        projected = estimate_biology_share(rows, source_total_tokens=220e9)["corpora"]["web"]
        self.assertEqual(projected["categories"]["biology"]["source_total_projection"]["estimate"], 55e9)
        other = [dict(row, corpus="overlapping_other_corpus") for row in rows]
        result = estimate_biology_share(rows + other)
        self.assertEqual(set(result["corpora"]), {"web", "overlapping_other_corpus"})
        self.assertNotIn("combined_tokens", result)
        with self.assertRaisesRegex(ValueError, "require.*mapping"):
            estimate_biology_share(rows + other, source_total_tokens=220e9)

    def test_duplicate_sampled_rows_are_rejected(self):
        rows = [record("a", 10, 10, "biology", index=3),
                record("a", 10, 20, "other", index=3)]
        with self.assertRaisesRegex(ValueError, "duplicate sampled"):
            estimate_biology_share(rows)

    def test_unreadable_rows_keep_original_weights_and_do_not_become_other(self):
        rows = [record("large", 100, 10, "biology"),
                dict(record("large", 100, 0, None), readable=False),
                record("small", 10, 10, "other"),
                dict(record("small", 10, 0, None), readable=False)]
        result = estimate_biology_share(
            rows, expected_sample_counts={"web": {"large": 2, "small": 2}})["corpora"]["web"]
        self.assertEqual(result["sample_records"], 4)
        self.assertEqual(result["readable_sample_records"], 2)
        self.assertEqual(result["unreadable_sample_records"], 2)
        self.assertEqual(result["sampled_strata"], 2)
        self.assertEqual(result["readability"]["estimate"], 55)
        self.assertEqual(result["readability"]["share"], 0.5)
        self.assertEqual(result["token_totals"]["source_tokens"]["estimate"], 550)
        self.assertEqual(result["categories"]["biology"]["source_tokens"]["estimate"], 500)
        self.assertEqual(result["categories"]["other"]["source_tokens"]["estimate"], 50)
        self.assertAlmostEqual(result["categories"]["biology"]["documents"]["share"], 10 / 11)
        self.assertEqual(result["categories"]["other"]["documents"]["estimate"], 5)
        self.assertGreater(result["categories"]["biology"]["source_tokens"]["share_standard_error"], 0)
        # The failed sample remains a zero in each two-row stratum's variance.
        expected_total_variance = 100 ** 2 * (1 - 2 / 100) * 50 / 2 + 10 ** 2 * (1 - 2 / 10) * 50 / 2
        self.assertAlmostEqual(result["token_totals"]["source_tokens"]["standard_error"],
                               math.sqrt(expected_total_variance))
        self.assertIn("readable", result["estimate_scope"])
        with self.assertRaisesRegex(ValueError, "invalid with unreadable"):
            estimate_biology_share(rows, source_total_tokens=220e9)

    def test_unreadable_state_must_be_explicit_and_cannot_have_imputed_tokens(self):
        valid = record("a", 10, 10, "biology")
        for bad, message in [
                (record("a", 10, 0, None), "final"),
                (dict(record("a", 10, 0, "other"), readable=False), "label=None"),
                (dict(record("a", 10, 5, None), readable=False), "zero domain"),
                (dict(record("a", 10, 0, None), readable=0), "boolean")]:
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                estimate_biology_share([valid, bad])


if __name__ == "__main__":
    unittest.main()
