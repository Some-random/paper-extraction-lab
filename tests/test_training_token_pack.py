import array
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("training_token_pack", ROOT / "scripts/prepare_training_token_pack.py")
packer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(packer)


class FakeTokenizer:
    def token_to_id(self, text):
        return 15 if text == "<|endoftext|>" else None

    def encode(self, text, add_special_tokens):
        return SimpleNamespace(ids=[int(word) for word in text.split()])


class TokenPackTests(unittest.TestCase):
    def fixture(self, directory, target=8):
        root = Path(directory)
        source = root / "archived"
        source.mkdir()
        tokenizer = root / "qwen3-4b-base-pinned" / "tokenizer.json"
        tokenizer.parent.mkdir()
        tokenizer.write_bytes(b"test fixture tokenizer")
        db = sqlite3.connect(source / "papers.sqlite3")
        db.execute("CREATE TABLE records(source_key TEXT,pmcid TEXT,source_hash TEXT,normalized_hash TEXT,"
                   "tokens INTEGER,selected_kept INTEGER,details TEXT)")
        for index, selected in ((1, True), (2, True), (3, False)):
            pmcid = f"PMC{index}"
            source_hash = hashlib.sha256(pmcid.encode()).hexdigest()
            text = "1 2 3 4" if index == 1 else "5 6 7 8"
            canonical = source / f"{index}.jsonl.gz"
            canonical.write_bytes(gzip.compress((json.dumps(dict(id=pmcid, source_xml_sha256=source_hash,
                                                    text=text, selected=selected)) + "\n").encode()))
            details = dict(canonical_locator=str(canonical), licenses=["CC-BY"])
            db.execute("INSERT INTO records VALUES(?,?,?,?,?,?,?)",
                       (str(index), pmcid, source_hash, f"text-{index}", 4, int(selected), json.dumps(details)))
        db.commit()
        db.close()
        config = root / "config.json"
        config.write_text(json.dumps(dict(run_id="archived", destination="archived",
                           tokenizer_path=str(tokenizer), tokenizer_sha256=packer.sha256(tokenizer))))
        args = SimpleNamespace(source_config=config, output_dir=root / "pack", tokens=target,
                               maximum_artifact_bytes=512 * packer.MIB, minimum_free_bytes=64 * packer.GIB,
                               maximum_runtime_seconds=3600, vocabulary_size=16,
                               tokenizer_path=None, tokenizer_sha256=None)
        return root, args

    def test_exact_bounded_pack_has_provenance_eos_and_final_partial_record(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, args = self.fixture(temporary)
            original_hash = packer.sha256(root / "archived/papers.sqlite3")
            with patch.object(packer, "ROOT", root), patch.object(packer.shutil, "disk_usage",
                      return_value=SimpleNamespace(free=100 * packer.GIB)):
                manifest = packer.pack(args, tokenizer=FakeTokenizer())
            packed = array.array("I")
            with (args.output_dir / "tokens.uint32").open("rb") as stream:
                packed.fromfile(stream, 8)
            self.assertEqual(list(packed), [1, 2, 3, 4, 15, 5, 6, 7])
            self.assertEqual(manifest["token_count"], 8)
            self.assertEqual(manifest["bytes"], 32)
            self.assertEqual(manifest["source_records"], 2)
            self.assertEqual(manifest["pack_sha256"], packer.sha256(args.output_dir / "tokens.uint32"))
            self.assertEqual(packer.sha256(root / "archived/papers.sqlite3"), original_hash)
            rows = [json.loads(line) for line in (args.output_dir / "records.jsonl").read_text().splitlines()]
            self.assertFalse(rows[0]["final_document_truncated"])
            self.assertTrue(rows[1]["final_document_truncated"])
            self.assertEqual(rows[1]["token_start"], 5)
            self.assertEqual(rows[1]["licenses"], ["CC-BY"])

    def test_input_exhaustion_is_failure_instead_of_document_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, args = self.fixture(temporary, target=30)
            with patch.object(packer, "ROOT", root), patch.object(packer.shutil, "disk_usage",
                      return_value=SimpleNamespace(free=100 * packer.GIB)):
                with self.assertRaisesRegex(RuntimeError, "no replay"):
                    packer.pack(args, tokenizer=FakeTokenizer())
            self.assertFalse((args.output_dir / "manifest.json").exists())
            self.assertEqual((args.output_dir / "tokens.uint32.partial").stat().st_size, 40)

    def test_free_space_and_provenance_guards_prevent_completed_pack(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, args = self.fixture(temporary)
            with patch.object(packer, "ROOT", root), patch.object(packer.shutil, "disk_usage",
                      return_value=SimpleNamespace(free=63 * packer.GIB)):
                with self.assertRaisesRegex(RuntimeError, "free-space"):
                    packer.pack(args, tokenizer=FakeTokenizer())
            self.assertFalse((args.output_dir / "manifest.json").exists())

    def test_existing_pack_and_tokenizer_hash_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, args = self.fixture(temporary)
            args.output_dir.mkdir()
            (args.output_dir / "tokens.uint32").write_bytes(b"preserve")
            with patch.object(packer, "ROOT", root):
                with self.assertRaises(FileExistsError):
                    packer.pack(args, tokenizer=FakeTokenizer())
            self.assertEqual((args.output_dir / "tokens.uint32").read_bytes(), b"preserve")

    def test_default_pack_is256_mib_and_budget_rejects_unbounded_outputs(self):
        args = packer.arguments(["--output-dir", "new-pack"])
        self.assertEqual(args.tokens * 4, 256 * packer.MIB)
        with self.assertRaises(SystemExit):
            packer.arguments(["--output-dir", "new-pack", "--maximum-artifact-bytes", str(513 * packer.MIB)])


if __name__ == "__main__":
    unittest.main()
