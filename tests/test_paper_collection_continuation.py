"""Offline checks for preserved ledger continuation and storage-only stopping."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from tokenizers import Tokenizer, models, pre_tokenizers

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("paper_continuation", ROOT / "scripts/run_paper_collection_continuation.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
base = module.base


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ContinuationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.workers = []
        tokenizer = Tokenizer(models.WordLevel({"[UNK]": 0}, unk_token="[UNK]"))
        tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
        tokenizer_path = self.root / "tokenizer.json"
        tokenizer.save(str(tokenizer_path))
        source = self.root / "source.xml"
        source.write_text('<article article-type="research-article"><front><article-meta>'
                          '<article-id pub-id-type="pmc">101</article-id>'
                          '<article-id pub-id-type="pmid">101</article-id>'
                          '<article-id pub-id-type="doi">10.1234/source</article-id>'
                          '<title-group><article-title>Gene and protein biology</article-title></title-group>'
                          '</article-meta></front><body><p>' + "A protein and gene control organism metabolism. " * 20 + '</p></body></article>')
        catalog = self.root / "catalog.json"
        catalog.write_text(json.dumps([{"pmcid": "PMC101", "path": str(source)}]))
        presence = self.root / "presence.csv"
        presence.write_text("pmcid,pmid,doi\n")
        old_config = {
            "run_id": "prior", "destination": str(self.root / "prior"),
            "source_catalog": str(catalog), "source_catalog_sha256": sha(catalog),
            "presence_ids_csv": str(presence), "presence_ids_csv_sha256": sha(presence),
            "tokenizer_path": str(tokenizer_path), "tokenizer_sha256": sha(tokenizer_path),
            "target_new_papers": 1, "existing_pipeline_bytes": 0,
            "query_topics": {"genes": ["gene", "protein"]},
            "limits": {"runtime_seconds": 120, "network_bytes": 256 * base.MIB,
                       "new_artifact_bytes": 256 * base.MIB, "minimum_free_bytes": 0,
                       "maximum_pipeline_data_bytes": 512 * base.MIB,
                       "max_xml_bytes": 2 * base.MIB, "max_text_bytes": base.MIB,
                       "max_document_gzip_bytes": 4 * base.MIB},
        }
        self.old_config_path = self.root / "old_config.json"
        self.old_config_path.write_text(json.dumps(old_config))
        old = base.Worker(self.old_config_path)
        self.assertEqual(old.execute(local_only=True), 0)
        self.prior = Path(old_config["destination"])
        summary_path = self.prior / "summary.json"
        summary = json.loads(summary_path.read_text())
        self.config = dict(old_config)
        self.config.update(run_id="continuation", destination=str(self.root / "continuation"), target_new_papers=None)
        self.config["limits"] = dict(old_config["limits"])
        self.config["limits"].pop("runtime_seconds")
        self.config["limits"]["control_plane_reserve_bytes"] = 0
        self.config["continuation"] = {
            "source_run": str(self.prior), "source_config": str(self.old_config_path),
            "source_config_sha256": sha(self.old_config_path), "source_summary": str(summary_path),
            "source_summary_sha256": sha(summary_path),
            "baseline_counts": {k: summary[k] for k in ("new_processed_papers", "new_selected_papers", "raw_tokens", "selected_exact_unique_tokens")},
        }
        self.config["continuation_discovery"] = {"version": "continuation_v1", "candidates_per_query": 10000, "query_years": [[2026, 2026]]}
        self.config_path = self.root / "continuation_config.json"

    def tearDown(self):
        for worker in self.workers:
            try:
                worker.close()
            except (sqlite3.ProgrammingError, ValueError):
                pass
        self.temporary.cleanup()

    def prepare(self):
        self.config_path.write_text(json.dumps(self.config))
        return module.prepare(self.config_path)

    def worker(self):
        self.prepare()
        worker = module.ContinuationWorker(self.config_path)
        self.workers.append(worker)
        return worker

    def test_backup_preserves_ids_records_hashes_and_prior_outputs(self):
        before = {name: sha(self.prior / name) for name in ("state.json", "summary.json", "papers.sqlite3")}
        result = self.prepare()
        self.assertEqual(result["copied_counts"]["records"], 1)
        self.assertEqual(result["copied_counts"]["known_pmcids"], 1)
        worker = module.ContinuationWorker(self.config_path)
        self.workers.append(worker)
        record = json.loads(worker.ledger.db.execute("SELECT details FROM records").fetchone()[0])
        self.assertTrue(str(record["document_locator"]).startswith(str(self.prior)))
        self.assertTrue(Path(record["document_locator"]).exists())
        self.assertTrue(worker.ledger.known({"doi": "10.1234/source"}))
        self.assertEqual(before, {name: sha(self.prior / name) for name in before})
        self.assertFalse((worker.run / "parsed").exists())

    def test_existing_identifiers_skip_before_any_network(self):
        worker = self.worker()
        worker.session.get = MagicMock(side_effect=AssertionError("No existing XML should be downloaded"))
        with worker.ledger.db:
            worker.ledger.db.execute("INSERT INTO candidates(pmcid,stratum) VALUES('PMC101','test')")
        worker.acquire_candidate("PMC101")
        self.assertEqual(worker.ledger.db.execute("SELECT status FROM candidates").fetchone()[0], "known")
        worker.session.get.assert_not_called()

    def test_guard_has_no_total_runtime_deadline_but_enforces_free_floor(self):
        worker = self.worker()
        self.assertIsNone(worker.state["deadline_epoch"])
        with patch.object(module.time, "time", return_value=10**12):
            worker.guard()
        worker.limits["minimum_free_bytes"] = 100
        disk = shutil._ntuple_diskusage(1000, 950, 50)
        with patch.object(module.shutil, "disk_usage", return_value=disk):
            with self.assertRaisesRegex(base.StopCollection, "free_space_floor"):
                worker.guard()

    def test_total_pipeline_limit_includes_preserved_baseline_and_copy(self):
        worker = self.worker()
        worker.config["existing_pipeline_bytes"] = worker.limits["maximum_pipeline_data_bytes"]
        with self.assertRaisesRegex(base.StopCollection, "pipeline_storage_limit"):
            worker.guard()

    def test_checkpoint_exit_preserves_network_budget_and_start_on_restart(self):
        worker = self.worker()
        worker.state.update(network_charged_bytes=1234, network_body_bytes=1234)
        started = worker.state["started_epoch"]
        worker.allocation_checkpoint = True
        self.assertEqual(worker.execute(), module.CHECKPOINT_EXIT)
        resumed = module.ContinuationWorker(self.config_path)
        self.workers.append(resumed)
        self.assertEqual(resumed.state["network_charged_bytes"], 1234)
        self.assertEqual(resumed.state["started_epoch"], started)
        self.assertFalse(resumed.allocation_checkpoint)
        self.assertIsNone(resumed.state["deadline_epoch"])

    def test_user_stop_does_not_request_requeue(self):
        worker = self.worker()
        (worker.run / "STOP").touch()
        self.assertEqual(worker.execute(), 0)
        self.assertEqual(worker.state["stop_reason"], "stop_requested")

    def test_inherited_pending_candidates_precede_expanded_search(self):
        worker = self.worker()
        with worker.ledger.db:
            worker.ledger.db.execute("INSERT INTO candidates(pmcid,stratum) VALUES('PMC202','inherited')")
        def consume(pmcid):
            with worker.ledger.db:
                worker.ledger.finish("candidates", pmcid, "processed")
        worker.acquire_candidate = MagicMock(side_effect=consume)
        def exhausted():
            self.assertEqual(worker.ledger.db.execute("SELECT status FROM candidates").fetchone()[0], "processed")
            return False
        worker.discover_next = MagicMock(side_effect=exhausted)
        worker.new()
        worker.acquire_candidate.assert_called_once_with("PMC202")

    def test_versioned_search_does_not_overwrite_prior_queries(self):
        worker = self.worker()
        with worker.ledger.db:
            worker.ledger.db.execute("INSERT INTO queries VALUES('genes_2026_2026','{}')")
        worker.fetch = MagicMock(return_value=json.dumps({"esearchresult": {"count": "1", "idlist": ["202"]}}).encode())
        self.assertTrue(worker.discover_next())
        names = {row[0] for row in worker.ledger.db.execute("SELECT name FROM queries")}
        self.assertEqual(names, {"genes_2026_2026", "continuation_v1:genes:2026:2026:r10000"})

    def test_interrupted_cached_xml_is_linked_and_original_survives_replacement(self):
        connection = sqlite3.connect(self.prior / "papers.sqlite3")
        connection.execute("INSERT INTO candidates(pmcid,stratum) VALUES('PMC202','pending')")
        connection.commit()
        connection.close()
        directory = self.prior / "raw/PMC202"
        directory.mkdir(parents=True)
        source = directory / "source.xml"
        source.write_bytes(b"preserved interrupted response")
        result = self.prepare()
        self.assertEqual(result["interrupted_cache_hardlinks"], 1)
        worker = module.ContinuationWorker(self.config_path)
        self.workers.append(worker)
        target = worker.run / "raw/PMC202/source.xml"
        self.assertEqual(source.stat().st_ino, target.stat().st_ino)
        worker.write(target, b"new atomic response")
        self.assertEqual(source.read_bytes(), b"preserved interrupted response")
        self.assertEqual(target.read_bytes(), b"new atomic response")

    def test_changed_config_is_rejected_after_preparation(self):
        self.prepare()
        self.config["limits"]["network_bytes"] += 1
        self.config_path.write_text(json.dumps(self.config))
        with self.assertRaisesRegex(ValueError, "config changed"):
            module.prepare(self.config_path)


if __name__ == "__main__":
    unittest.main()
