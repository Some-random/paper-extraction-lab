import json
import sys
import tempfile
import unittest
import subprocess
import hashlib
import io
from types import SimpleNamespace
from pathlib import Path

from tokenizers import Tokenizer, models, pre_tokenizers
import zstandard

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from corpus_count import Ledger, canonical_paper_text, inspect_text


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

    def test_captions_tables_and_notes_are_counted_once_with_real_jats_parser(self):
        from native_training import parse_jats
        source = b'''<article><front><article-meta><title-group><article-title>A gene study</article-title></title-group></article-meta></front>
        <body><p>Measured protein function.</p>
        <fig id="F1"><caption><p>UNIQUE_CAPTION.</p></caption></fig>
        <table-wrap id="T1"><caption><p>UNIQUE_TABLE_CAPTION.</p></caption><table><tbody><tr><td>UNIQUE_CELL</td></tr></tbody></table>
        <table-wrap-foot><p>UNIQUE_FOOTNOTE.</p></table-wrap-foot></table-wrap></body></article>'''
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "source.xml"
            path.write_bytes(source)
            document = parse_jats(path, "PMC_TEST", self.tokenizer)
            text = canonical_paper_text(document)
            for marker in ("UNIQUE_CAPTION", "UNIQUE_TABLE_CAPTION", "UNIQUE_CELL", "UNIQUE_FOOTNOTE"):
                self.assertEqual(text.count(marker), 1, marker)
            self.assertEqual(path.read_bytes(), source)
            document["visuals"].append({"id": "floating", "caption_training_text": "Floating caption"})
            self.assertEqual(canonical_paper_text(document).count("Floating caption"), 1)

    def test_audited_correction_preserves_other_sources_and_cannot_repeat_subtraction(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            ledger = Ledger(base / "counts.sqlite3", "manifest", "tokenizer")
            paper, web = {"id": "paper", "source": "pmc"}, {"id": "web", "source": "web"}
            ledger.register([paper, web])
            ledger.append(paper, [(1, inspect_text("Caption Caption", self.tokenizer), {"id": "PMC1"})])
            ledger.append(web, [(1, inspect_text("Web content", self.tokenizer), {})])
            audit = base / "audit.json"
            ledger.retire_file("paper", "corrected-sha", audit)
            self.assertEqual(ledger.totals()["web"]["raw_tokens"], len("Web content"))
            self.assertEqual(ledger.totals()["pmc"]["raw_tokens"], 0)
            self.assertEqual(ledger.file_state("paper")[1], 0)
            ledger.append(paper, [(1, inspect_text("Caption", self.tokenizer), {"id": "PMC1"})])
            ledger.retire_file("paper", "corrected-sha", audit)
            self.assertEqual(ledger.totals()["pmc"]["raw_tokens"], len("Caption"))
            self.assertEqual(json.loads(audit.read_text())["superseded_records"][0]["tokens"], len("Caption Caption"))
            extension = {"id": "new_paper", "source": "pmc", "sha256": "newhash"}
            ledger.register_extension(extension)
            ledger.register_extension(extension)
            self.assertEqual(ledger.extensions(), [extension])
            with self.assertRaisesRegex(ValueError, "input changed"):
                ledger.register_extension({**extension, "sha256": "different"})
            ledger.close()

    def test_correction_refuses_to_silently_change_cross_file_dedup_representatives(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            ledger = Ledger(base / "counts.sqlite3", "manifest", "tokenizer")
            first, second = {"id": "paper", "source": "pmc"}, {"id": "dataset", "source": "import"}
            ledger.register([first, second])
            m = inspect_text("Identical text", self.tokenizer)
            ledger.append(first, [(1, m, {})])
            ledger.append(second, [(1, m, {})])
            with self.assertRaisesRegex(ValueError, "external deduplication"):
                ledger.retire_file("paper", "new", base / "audit.json")
            self.assertEqual(ledger.totals()["pmc"]["unique_tokens"], m["tokens"])
            ledger.close()

    def test_pmc_version_selection_does_not_require_pdf_or_assume_version_one(self):
        from pmc_count_expansion import choose_metadata, RejectedPaper
        manuscript = {"version": 4, "is_manuscript": "yes", "xml_url": "manuscript.xml"}
        published = {"version": 2, "is_manuscript": "no", "xml_url": "published.xml"}
        retracted = {"version": 6, "is_retracted": "yes", "xml_url": "retracted.xml"}
        self.assertEqual(choose_metadata([manuscript, retracted, published]), published)
        with self.assertRaises(RejectedPaper):
            choose_metadata([retracted])

    def test_clinical_title_screen_keeps_mechanistic_disease_biology(self):
        from pmc_count_expansion import clinical_title_reason
        for title in ["Endomyocardial biopsy in clinical decision making", "New insights into clinical trial for colostrinin",
                      "Burden of illness in amino acid decarboxylase deficiency", "Randomised, controlled trial",
                      "Cardioverter defibrillator implantation"]:
            self.assertIsNotNone(clinical_title_reason(title), title)
        for title in ["Biochemical Properties and Biological Functions of FET Proteins",
                      "Epigenetic regulation of immune checkpoint signaling by microbial metabolites",
                      "Gene regulation in patients with cancer", "Cytokine-induced memory NK cells"]:
            self.assertIsNone(clinical_title_reason(title), title)

    def test_pmc_fetch_accounts_shared_and_paper_budgets_without_reset(self):
        from pmc_count_expansion import PaperExpansion
        with tempfile.TemporaryDirectory() as temporary:
            worker = SimpleNamespace(state={"network_reserved_bytes": 100, "network_body_bytes": 100,
                                           "new_artifact_bytes": 0},
                config={"limits": {"network_reserved_bytes": 2**20, "new_artifact_bytes": 2**25}},
                guard=lambda: None, persist=lambda: None)
            class ByteStream(io.BytesIO):
                def read(self, size=-1, decode_content=False):
                    return super().read(size)
            response = SimpleNamespace(status_code=200, headers={"Content-Length": "7"},
                                       raw=ByteStream(b"example"), raise_for_status=lambda: None)
            class Context:
                def __enter__(self):
                    self_reserved = worker.state["network_reserved_bytes"]
                    if self_reserved != 164:
                        raise AssertionError("HTTP reservation was not persisted before reading")
                    return response
                def __exit__(self, *args):
                    return False
            expansion = object.__new__(PaperExpansion)
            expansion.worker = worker
            expansion.plan = {"maximum_new_paper_download_bytes": 2**20}
            expansion.progress = {"downloaded_bytes": 50, "reserved_bytes": 50}
            expansion.session = SimpleNamespace(get=lambda *args, **kwargs: Context())
            destination = Path(temporary) / "raw"
            self.assertEqual(expansion.fetch("https://example.test", destination, 64), b"example")
            self.assertEqual(worker.state["network_reserved_bytes"], 107)
            self.assertEqual(worker.state["network_body_bytes"], 107)
            self.assertEqual(expansion.progress["downloaded_bytes"], 57)
            self.assertEqual(expansion.progress["reserved_bytes"], 57)
            expansion.fetch("https://example.test", destination, 64)
            self.assertEqual(worker.state["network_body_bytes"], 107)

    def test_pmc_adapter_preserves_xml_and_counts_source_views_once_without_media_download(self):
        from pmc_count_expansion import PaperExpansion
        with tempfile.TemporaryDirectory(dir=ROOT / "experiments") as temporary:
            base = Path(temporary)
            paragraph = "Gene expression regulates protein function in cells. " * 20
            raw = ('<article article-type="research-article"><front><article-meta><title-group><article-title>Protein gene regulation</article-title></title-group>'
                '<abstract><p>Genes and proteins regulate cells.</p></abstract></article-meta></front><body><p>' + paragraph + '</p>'
                '<fig id="F1"><caption><p>CAPTION_ONCE.</p></caption></fig>'
                '<table-wrap id="T1"><table><tbody><tr><td>CELL_ONCE</td></tr></tbody></table></table-wrap></body></article>').encode()
            metadata = {"pmcid": "PMC_TEST", "version": 2, "license_code": "CC BY", "doi": "10.test/1",
                        "title": "Protein gene regulation", "xml_url": "https://example.test/source.xml?md5=" + hashlib.md5(raw).hexdigest(),
                        "media_urls": ["https://example.test/figure.jpg"]}
            expansion = object.__new__(PaperExpansion)
            expansion.root = base / "pmc_expansion"
            expansion.plan = {"maximum_xml_bytes": 2**20, "accepted_article_types": ["research-article"], "maximum_table_rows": 2000}
            expansion.overrides = {}
            expansion.known_dois = set()
            expansion.worker = SimpleNamespace(tokenizer=self.tokenizer,
                config_path=ROOT / "config/corpus_count_2026-10-17.json", config={"limits": {"maximum_text_bytes": 2**20}})
            calls = []
            expansion.metadata = lambda *args: metadata
            def fetch(url, path, maximum):
                calls.append(url)
                path.write_bytes(raw)
                return raw
            expansion.fetch = fetch
            item = expansion.acquire({"pmcid": "PMC_TEST", "stratum": "test"})
            record = json.loads(Path(item["path"]).read_text())
            self.assertEqual(record["text"].count("CAPTION_ONCE"), 1)
            self.assertEqual(record["text"].count("CELL_ONCE"), 1)
            self.assertEqual(record["version"], 2)
            self.assertEqual(record["source_xml_sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual((Path(item["path"]).parent / "source.xml").read_bytes(), raw)
            self.assertEqual(calls, [metadata["xml_url"]])
            metadata["xml_url"] = "https://example.test/source.xml?md5=incorrect"
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                expansion.acquire({"pmcid": "PMC_TEST", "stratum": "test"})

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
