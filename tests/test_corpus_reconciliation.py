import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("reconciliation", ROOT / "scripts/reconcile_corpus_inventory.py")
reconciliation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reconciliation)


class CorpusReconciliationTests(unittest.TestCase):
    def test_same_size_never_claims_hash_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "shard.jsonl"
            path.write_bytes(b"wrong")
            result = reconciliation.inspect_local_file(path, 5)
            self.assertEqual(result["local_file_status"], "same_size_unverified")
            self.assertEqual(result["checksum_status"], "not_recomputed")

    def test_missing_truncated_oversized_and_partial_are_distinct(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "shard.zst"
            self.assertEqual(reconciliation.inspect_local_file(path, 10)["local_file_status"], "missing")
            path.write_bytes(b"abc")
            self.assertEqual(reconciliation.inspect_local_file(path, 10)["local_file_status"], "truncated")
            self.assertEqual(reconciliation.inspect_local_file(path, 2)["local_file_status"], "oversized")
            path.rename(path.with_suffix(".zst.part"))
            partial = reconciliation.inspect_local_file(path, 10)
            self.assertEqual(partial["local_file_status"], "partial_download")
            self.assertEqual(partial["partial_bytes"], 3)
            self.assertEqual(partial["local_bytes"], 0)

    def test_pmcid_normalization_preserves_identifier_level_join(self):
        self.assertEqual(reconciliation.normalize_pmcid(" pmc00123.2 "), "PMC123")
        self.assertEqual(reconciliation.normalize_pmcid(123), "PMC123")
        with self.assertRaises(ValueError):
            reconciliation.normalize_pmcid("10.123/doi")

    def test_selection_uses_completed_expansions_and_reconciles_unique_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "PMC2").mkdir()
            (root / "PMC2/selected_metadata.json").write_text(json.dumps({"pmcid": "pmc2", "version": 3}))
            selected = reconciliation.selected_papers({"papers": [{"pmcid": "PMC1"}]}, {
                "pmc_new_PMC2": {"status": "complete"},
                "pmc_new_PMC3": {"status": "excluded_scope"},
                "pmc_new_PMC4": {"status": "pending"}}, root)
            summary, private = reconciliation.reconcile_papers(selected, [
                {"pmcid": "pmc2.3", "bytes": "100", "source_path": "/private/two"},
                {"pmcid": "PMC5", "bytes": "200", "source_path": "/private/five"}])
            self.assertEqual(summary["selected_pilot_pmcs"], 2)
            self.assertEqual(summary["overlap_by_pmcid"], 1)
            self.assertEqual(summary["additional_cached_pmcids"], 1)
            self.assertEqual(summary["union_pmcids"], 3)
            self.assertNotIn("/private/", json.dumps(summary))
            self.assertIn("/private/", json.dumps(private))

    def test_online_output_preserves_pins_status_and_omits_local_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "private").mkdir()
            (root / "private/shard").write_text("abc")
            items = [{"id": "one", "source": "finefineweb", "path": "private/shard",
                      "dataset_path": "biology/one.jsonl", "revision": "pinned", "bytes": 3, "sha256": "expected"},
                     {"id": "two", "source": "biocollection", "path": "private/missing",
                      "dataset_path": "data/two.zst", "revision": "otherpin", "bytes": 10, "sha256": "hash"}]
            rows = reconciliation.reconcile_online(items, {"one": {"status": "counting", "rows_committed": 4}}, root)
            summary = reconciliation.summarize_online(rows)
            self.assertEqual(summary["finefineweb"]["partly_counted_files"], 1)
            self.assertEqual(summary["biocollection"]["missing_file_bytes"], 10)
            self.assertEqual(summary["finefineweb"]["payload_checksums_recomputed"], 0)
            paths = reconciliation.write_outputs(root / "public", summary, {}, rows)
            contents = "".join(path.read_text() for path in paths)
            self.assertNotIn("private/shard", contents)
            self.assertIn("pinned", contents)
            self.assertIn("expected", contents)
            with paths[1].open() as handle:
                self.assertEqual(len(list(csv.DictReader(handle))), 2)


if __name__ == "__main__":
    unittest.main()
