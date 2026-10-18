import json
import sys
import tempfile
import unittest
import subprocess
from pathlib import Path

from tokenizers import Tokenizer, models, pre_tokenizers
import zstandard

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from corpus_count import Ledger, inspect_text


class CorpusCountingTests(unittest.TestCase):
    def setUp(self):
        # No merges: one token per byte, with real Unicode offset handling.
        vocabulary = {char: i for i, char in enumerate(sorted(pre_tokenizers.ByteLevel.alphabet()))}
        self.tokenizer = Tokenizer(models.BPE(vocab=vocabulary, merges=[]))
        self.tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False, use_regex=False)

    def test_modalities_partition_full_record_tokens_with_unicode_and_tag_boundaries(self):
        text = "α text <dna>ACGT</dna> <protein>MKT</protein> <smiles>C(C)</smiles> β"
        measured = inspect_text(text, self.tokenizer)
        self.assertEqual(measured["tokens"], len(text.encode("utf-8")))
        self.assertEqual(measured["modalities"]["dna"], 4)
        self.assertEqual(measured["modalities"]["protein"], 3)
        self.assertEqual(measured["modalities"]["smiles"], 4)
        self.assertEqual(sum(measured["modalities"].values()), measured["tokens"])
        self.assertEqual(measured["modalities"]["text_or_unclassified"], measured["tokens"] - 11)
        # Untagged strings are not silently certified as biological sequences.
        self.assertEqual(inspect_text("ACGT MKT", self.tokenizer)["modalities"]["dna"], 0)

    def test_cross_source_dedup_preserves_case_and_distinct_annotations_and_resumes(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "counts.sqlite3"
            first = {"id": "paper", "source": "pmc"}
            second = {"id": "dataset", "source": "import"}
            ledger = Ledger(path, "manifest", "tokenizer")
            ledger.register([first, second])
            texts = ["Gene ABC\nfunction", "Gene ABC   function", "gene ABC function", "Gene ABC function extra"]
            measurements = [inspect_text(t, self.tokenizer) for t in texts]
            ledger.append(first, [(1, measurements[0], {"doi": "10.example/1"})])
            ledger.append(second, [(i, m, {}) for i, m in enumerate(measurements[1:], 1)])
            ledger.close()
            ledger = Ledger(path, "manifest", "tokenizer")
            # Replay a committed batch, as on restart. It must have no effect.
            ledger.append(second, [(i, m, {}) for i, m in enumerate(measurements[1:], 1)])
            totals = ledger.totals()
            self.assertEqual(sum(s["raw_records"] for s in totals.values()), 4)
            self.assertEqual(sum(s["unique_records"] for s in totals.values()), 3)
            self.assertEqual(totals["import"]["unique_tokens"], sum(m["tokens"] for m in measurements[2:]))
            self.assertEqual(ledger.file_state("dataset")[1], 3)
            self.assertEqual(sum(s["raw_tokens"] for s in totals.values()), sum(m["tokens"] for m in measurements))
            for counts in totals.values():
                self.assertEqual(sum(v for k, v in counts.items() if k.startswith("unique_") and k.endswith("_tokens") and k != "unique_tokens"), counts["unique_tokens"])
            self.assertEqual(json.loads(ledger.db.execute("SELECT provenance FROM records WHERE file_id='paper'").fetchone()[0])["doi"], "10.example/1")
            ledger.close()
            with self.assertRaisesRegex(ValueError, "identity changed"):
                Ledger(path, "different manifest", "tokenizer")

    def test_bad_batch_rolls_back_records_counters_and_resume_cursor_together(self):
        with tempfile.TemporaryDirectory() as temporary:
            ledger = Ledger(Path(temporary) / "counts.sqlite3", "manifest", "tokenizer")
            item = {"id": "input", "source": "source"}
            ledger.register([item])
            good = inspect_text("Valid text", self.tokenizer)
            with self.assertRaises(KeyError):
                ledger.append(item, [(1, good, {}), (2, {}, {})])
            self.assertEqual(ledger.file_state("input")[1], 0)
            self.assertEqual(ledger.db.execute("SELECT COUNT(*) FROM records").fetchone()[0], 0)
            self.assertEqual(ledger.totals(), {})
            ledger.close()

    def test_full_compressed_shard_and_restart_reconcile_report_axes(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            tokenizer_path = base / "tokenizer.json"
            self.tokenizer.save(str(tokenizer_path))
            texts = ["A study of <dna>ACGT</dna>", "A distinct annotation"]
            raw = b"".join((json.dumps({"text": text}) + "\n").encode() for text in texts)
            first, second = base / "papers.jsonl", base / "records.jsonl.zst"
            first.write_bytes(raw)
            second.write_bytes(zstandard.ZstdCompressor().compress(raw))
            from corpus_count import sha256
            files = [{"id": path.name, "source": source, "path": str(path), "format": format,
                      "bytes": path.stat().st_size, "sha256": sha256(path), "expected_records": 2}
                     for path, source, format in [(first, "paper", "jsonl"), (second, "dataset", "jsonl.zst")]]
            sources = {source: {"name": source, "acquisition_route": route, "content_category": category,
                                "expected_files": 1, "whole_source_inventory": True}
                       for source, route, category in [("paper", "online_papers", "papers"),
                                                       ("dataset", "existing_datasets", "database_records")]}
            config = {"run_id": "test", "destination": str(base / "run"),
                      "report_directory": str(base / "report"), "tokenizer_path": str(tokenizer_path),
                      "tokenizer_sha256": sha256(tokenizer_path), "tokenizer_identity": "test fixture",
                      "limits": {"runtime_seconds": 60, "network_reserved_bytes": 0,
                                 "new_artifact_bytes": 2**25, "minimum_free_bytes": 0,
                                 "maximum_line_bytes": 2**20, "maximum_text_bytes": 2**20},
                      "files": files, "sources": sources, "source_families": [], "counting_policy": {}}
            config_path = base / "config.json"
            config_path.write_text(json.dumps(config))
            command = [sys.executable, str(ROOT / "scripts/run_corpus_count.py"), "--config", str(config_path), "--local-only"]
            for _ in range(2):
                subprocess.run(command, check=True, capture_output=True, text=True)
            summary = json.loads((base / "report/summary.json").read_text())
            expected = sum(len(t.encode()) for t in texts)
            self.assertEqual(summary["totals"]["raw_records"], 4)
            self.assertEqual(summary["totals"]["raw_tokens"], 2 * expected)
            self.assertEqual(summary["totals"]["unique_tokens"], expected)
            self.assertEqual(summary["totals"]["unique_dna_tokens"], 4)
            for axis in ["acquisition_routes", "content_categories"]:
                for metric in ["raw_records", "raw_tokens", "unique_records", "unique_tokens"]:
                    self.assertEqual(sum(v[metric] for v in summary[axis].values()), summary["totals"][metric])
            self.assertTrue(all(s["complete_frozen_input_scan"] for s in summary["sources"].values()))
            self.assertIsNone(summary["final_retained_biology_tokens"])
            self.assertIsNone(summary["near_deduplicated_tokens"])
            self.assertIsNone(summary["whole_available_biology_total"])


if __name__ == "__main__":
    unittest.main()
