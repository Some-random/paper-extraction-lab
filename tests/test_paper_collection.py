"""Offline checks for reuse, frozen budgets and transactional paper counting."""
import hashlib
import importlib.util
import io
import json
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import requests
from tokenizers import Tokenizer, models, pre_tokenizers
from urllib3.exceptions import ProtocolError, ReadTimeoutError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("paper_collection", ROOT / "scripts/run_paper_collection.py")
collection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collection)


def source(pmcid="PMC101", doi="10.test/existing", body=None, id_kind="pmc"):
    body = body or ("A protein and gene participate in cellular metabolism. " * 15)
    return (f'<article article-type="research-article"><front><article-meta>'
            f'<article-id pub-id-type="{id_kind}">{pmcid}</article-id>'
            f'<article-id pub-id-type="pmid">{pmcid[3:]}</article-id>'
            f'<article-id pub-id-type="doi">{doi}</article-id>'
            '<title-group><article-title>Gene and protein cellular biology</article-title></title-group>'
            '<permissions><license license-type="source-license"><license-p>Source terms.</license-p></license></permissions>'
            f'</article-meta></front><body><p>{body}</p></body></article>').encode()


class PaperCollectionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        tok = Tokenizer(models.WordLevel({"[UNK]": 0}, unk_token="[UNK]"))
        tok.pre_tokenizer = pre_tokenizers.Whitespace()
        self.tokenizer = self.root / "tokenizer.json"
        tok.save(str(self.tokenizer))
        self.catalog = self.root / "catalog.json"
        self.catalog.write_text("[]")
        self.config_path = self.root / "config.json"
        self.config = {"run_id": "offline-test", "destination": str(self.root / "run"),
                       "source_catalog": str(self.catalog), "tokenizer_path": str(self.tokenizer),
                       "tokenizer_sha256": hashlib.sha256(self.tokenizer.read_bytes()).hexdigest(),
                       "target_new_papers": 1, "existing_pipeline_bytes": 0,
                       "limits": {"runtime_seconds": 120, "network_bytes": 32 * collection.MIB,
                                  "new_artifact_bytes": 128 * collection.MIB, "minimum_free_bytes": 0,
                                  "max_xml_bytes": 2 * collection.MIB, "max_text_bytes": collection.MIB,
                                  "max_document_gzip_bytes": 4 * collection.MIB,
                                  "maximum_pipeline_data_bytes": 1024 * collection.MIB}}
        self.workers = []

    def tearDown(self):
        for worker in self.workers:
            try:
                worker.session.close()
                worker.ledger.db.close()
                worker.lock.close()
            except (sqlite3.ProgrammingError, ValueError):
                pass
        self.temporary.cleanup()

    def add_source(self, raw, name="source.xml", pmcid="PMC101"):
        path = self.root / name
        path.write_bytes(raw)
        rows = json.loads(self.catalog.read_text())
        rows.append({"pmcid": pmcid, "path": str(path), "bytes": path.stat().st_size,
                     "mtime_ns": path.stat().st_mtime_ns})
        self.catalog.write_text(json.dumps(rows))
        return path

    def worker(self):
        self.config_path.write_text(json.dumps(self.config))
        worker = collection.Worker(self.config_path)
        self.workers.append(worker)
        return worker

    def test_local_reuse_outputs_provenance_without_network_or_source_copy(self):
        original = source(id_kind="pmcaid")
        path = self.add_source(original)
        worker = self.worker()
        worker.session.get = MagicMock(side_effect=AssertionError("Network must not be used"))
        self.assertEqual(worker.execute(local_only=True), 0)
        summary = json.loads((worker.run / "summary.json").read_text())
        self.assertEqual(summary["reused_processed_papers"], 1)
        self.assertEqual(summary["selected_records"], 1)
        self.assertGreater(summary["raw_tokens"], 100)
        self.assertEqual(summary["network_bytes"], 0)
        self.assertEqual(path.read_bytes(), original)
        self.assertFalse((worker.run / "raw").exists())
        payload = next((worker.run / "parsed").rglob("document.json.gz"))
        parsed = json.loads(collection.gzip.decompress(payload.read_bytes()))
        self.assertEqual(parsed["source_locator"], str(path))
        self.assertEqual(parsed["source_xml_sha256"], hashlib.sha256(original).hexdigest())
        self.assertEqual(parsed["source_metadata"]["licenses"][0]["attributes"]["license-type"], "source-license")
        worker.session.get.assert_not_called()

    def test_all_known_pmcids_and_dois_skip_before_xml_network_fetch(self):
        self.add_source(source())
        presence = self.root / "presence.csv"
        presence.write_text("pmcid,pmid,doi\nPMC777,777,10.test/other\n")
        self.config["presence_ids_csv"] = str(presence)
        worker = self.worker()
        worker.seed_known()
        worker.discover = MagicMock()
        worker.metadata = MagicMock(return_value={"pmcid": "PMC202", "doi": "https://doi.org/10.TEST/EXISTING", "xml_url": "must-not-fetch"})
        worker.fetch = MagicMock(side_effect=AssertionError("Existing XML must not be downloaded"))
        with worker.ledger.db:
            worker.ledger.db.execute("INSERT INTO candidates(pmcid,stratum) VALUES('PMC777','test')")
            worker.ledger.db.execute("INSERT INTO candidates(pmcid,stratum) VALUES('PMC202','test')")
        worker.new()
        self.assertEqual(worker.metadata.call_count, 1)
        worker.fetch.assert_not_called()
        self.assertEqual(dict(worker.ledger.db.execute("SELECT kind,count FROM events")),
                         {"known_pmcid_skips": 1, "known_secondary_identifier_skips": 1})
        self.assertTrue(worker.ledger.known({"pmid": "101"}))

    def test_source_versions_preserved_and_text_hash_duplicates_counted_once(self):
        self.add_source(source(), "one.xml")
        self.add_source(source(body="A protein and gene participate in cellular metabolism.  " * 15), "two.xml")
        worker = self.worker()
        worker.seed_known()
        worker.reused()
        rows = list(worker.ledger.db.execute("SELECT source_hash,kept,selected_kept FROM records"))
        self.assertEqual(len(rows), 2)
        self.assertNotEqual(rows[0][0], rows[1][0])
        self.assertEqual(sum(row[1] for row in rows), 1)
        self.assertEqual(sum(row[2] for row in rows), 1)
        worker.publish(force=True)
        summary = json.loads((worker.run / "summary.json").read_text())
        self.assertEqual(summary["raw_records"], 2)
        self.assertEqual(summary["exact_unique_records"], 1)

    def test_record_failure_rolls_back_counts_and_resume_cursor(self):
        worker = self.worker()
        with worker.ledger.db:
            worker.ledger.db.execute("INSERT INTO catalog(row_number,pmcid,path,status) VALUES(1,'PMC1','unused','indexed')")
        malformed = {"source_key": "PMC1:hash", "pmcid": "PMC1", "source_xml_sha256": "hash",
                     "route": "reused", "selected": True, "selection_reason": None,
                     "measurements": {"normalized_sha256": "text", "tokens": 10}}
        with self.assertRaises(KeyError):
            worker.ledger.append(malformed, "catalog", 1)
        self.assertEqual(worker.ledger.db.execute("SELECT COUNT(*) FROM records").fetchone()[0], 0)
        self.assertEqual(worker.ledger.db.execute("SELECT status FROM catalog").fetchone()[0], "indexed")

    def test_frozen_mtime_change_is_rejected_and_no_source_is_overwritten(self):
        path = self.add_source(source())
        worker = self.worker()
        path.write_bytes(source(body="Changed biology protein gene text. " * 30))
        worker.seed_known()
        row = worker.ledger.db.execute("SELECT status,error FROM catalog").fetchone()
        self.assertEqual(row, ("rejected", "local_xml_changed_since_catalog_freeze"))
        self.assertIn(b"Changed biology", path.read_bytes())

    def test_identifier_mismatch_rejected_before_tokenization(self):
        self.add_source(source(pmcid="PMC999"))
        worker = self.worker()
        worker.seed_known()
        worker.reused()
        self.assertEqual(worker.ledger.db.execute("SELECT status,error FROM catalog").fetchone(),
                         ("rejected", "native_pmcid_mismatch"))
        self.assertEqual(worker.ledger.db.execute("SELECT COUNT(*) FROM records").fetchone()[0], 0)

    def test_retry_failure_is_bounded_and_failed_body_bytes_remain_charged(self):
        worker = self.worker()
        with worker.ledger.db:
            worker.ledger.set("known_index_complete", 1)
        def response():
            context = MagicMock()
            response = context.__enter__.return_value
            response.status_code = 200
            response.headers = {"Content-Length": "8"}
            response.raw.read.side_effect = [b"1234", requests.ReadTimeout("offline failure")]
            return context
        worker.session.get = MagicMock(side_effect=lambda *args, **kwargs: response())
        with patch.object(collection.time, "sleep"):
            with self.assertRaises(collection.TransportUnavailable):
                worker.fetch("https://example.invalid/test", worker.run / "raw.xml", 16)
        self.assertEqual(worker.session.get.call_count, 3)
        self.assertEqual(worker.state["network_body_bytes"], 12)
        self.assertEqual(worker.state["network_charged_bytes"], 48)
        self.assertTrue(worker.state["network_body_bytes_is_lower_bound"])
        self.assertFalse((worker.run / "raw.xml").exists())

    def test_actual_urllib3_raw_reader_errors_retry_and_preserve_conservative_charges(self):
        worker = self.worker()
        with worker.ledger.db:
            worker.ledger.set("known_index_complete", 1)
        for error in (ReadTimeoutError(None, "/test", "read stalled"), ProtocolError("incomplete response")):
            with self.subTest(error=type(error).__name__):
                before_charged = worker.state["network_charged_bytes"]
                before_measured = worker.state["network_body_bytes"]
                def response():
                    context = MagicMock()
                    response = context.__enter__.return_value
                    response.status_code = 200
                    response.headers = {"Content-Length": "8"}
                    response.raw.read.side_effect = [b"1234", error]
                    return context
                worker.session.get = MagicMock(side_effect=lambda *args, **kwargs: response())
                with patch.object(collection.time, "sleep"):
                    with self.assertRaisesRegex(collection.TransportUnavailable, type(error).__name__):
                        worker.fetch("https://example.invalid/test", worker.run / "raw.xml", 16)
                self.assertEqual(worker.session.get.call_count, 3)
                self.assertEqual(worker.state["network_body_bytes"], before_measured + 12)
                self.assertEqual(worker.state["network_charged_bytes"], before_charged + 48)
                persisted = json.loads(worker.state_path.read_text())
                self.assertEqual(persisted["network_charged_bytes"], worker.state["network_charged_bytes"])
                self.assertTrue(persisted["network_body_bytes_is_lower_bound"])
                self.assertFalse((worker.run / "raw.xml").exists())

    def test_budget_and_original_deadline_survive_resume(self):
        worker = self.worker()
        deadline = worker.state["deadline_epoch"]
        worker.state.update(started_epoch=time.time() - 1000, network_charged_bytes=37, network_body_bytes=37)
        worker.persist()
        worker.session.close()
        worker.ledger.db.close()
        worker.lock.close()
        resumed = self.worker()
        self.assertEqual(resumed.state["network_charged_bytes"], 37)
        self.assertLess(resumed.state["deadline_epoch"], deadline)
        with self.assertRaisesRegex(collection.StopCollection, "runtime_limit"):
            resumed.guard()

    def test_network_requires_complete_index_and_honors_byte_reservation(self):
        worker = self.worker()
        worker.session.get = MagicMock()
        with self.assertRaisesRegex(RuntimeError, "complete local identifier index"):
            worker.fetch("https://example.invalid", worker.run / "none", 100)
        with worker.ledger.db:
            worker.ledger.set("known_index_complete", 1)
        worker.state["network_charged_bytes"] = worker.limits["network_bytes"] - 10
        with self.assertRaisesRegex(collection.StopCollection, "network_budget"):
            worker.fetch("https://example.invalid", worker.run / "none", 100)
        worker.session.get.assert_not_called()

    def test_catalog_checksum_change_prevents_worker_initialization(self):
        self.config["source_catalog_sha256"] = "0" * 64
        self.config_path.write_text(json.dumps(self.config))
        with self.assertRaisesRegex(ValueError, "Frozen input checksum mismatch"):
            collection.Worker(self.config_path)

    def test_probe_stops_before_network_and_parse_errors_do_not_stall_cursor(self):
        self.add_source(source(), "valid.xml")
        self.add_source(source(pmcid="PMC102", doi="10.test/new", body="short"), "short.xml", "PMC102")
        worker = self.worker()
        worker.session.get = MagicMock(side_effect=AssertionError("Diagnostic must not acquire"))
        self.assertEqual(worker.execute(max_local_papers=1), 0)
        summary = json.loads((worker.run / "summary.json").read_text())
        self.assertEqual(summary["stop_reason"], "local_probe_limit")
        self.assertEqual(summary["raw_records"], 1)
        worker.session.get.assert_not_called()

    def test_downloaded_xml_remains_resumable_when_processing_stops_before_commit(self):
        worker = self.worker()
        worker.seed_known()
        worker.discover = MagicMock()
        raw = source(pmcid="PMC202", doi="10.test/new")
        directory = worker.run / "raw/PMC202"
        worker.write(directory / "source.xml", raw)
        metadata = {"pmcid": "PMC202", "pmid": "202", "doi": "10.test/new", "version": 3,
                    "xml_url": "https://pmc-oa-opendata.s3.amazonaws.com/source.xml?md5=" + hashlib.md5(raw).hexdigest()}
        worker.metadata = MagicMock(return_value=metadata)
        worker.session.get = MagicMock(side_effect=AssertionError("Archived XML must be reused"))
        with worker.ledger.db:
            worker.ledger.db.execute("INSERT INTO candidates(pmcid,stratum) VALUES('PMC202','test')")
        with patch.object(worker, "process", side_effect=collection.StopCollection("test_pause")):
            with self.assertRaisesRegex(collection.StopCollection, "test_pause"):
                worker.new()
        self.assertFalse(worker.ledger.known({"pmcid": "PMC202"}))
        self.assertEqual(worker.ledger.db.execute("SELECT status FROM candidates").fetchone()[0], "pending")
        worker.new()
        self.assertTrue(worker.ledger.known({"pmcid": "PMC202"}))
        self.assertEqual(worker.ledger.db.execute("SELECT status FROM candidates").fetchone()[0], "processed")
        self.assertEqual(worker.ledger.db.execute("SELECT route,selected FROM records").fetchone(), ("new", 1))
        worker.session.get.assert_not_called()

    def test_native_parse_failure_is_recorded_and_later_paper_still_processes(self):
        self.add_source(source().replace(b"<body>", b"<notbody>").replace(b"</body>", b"</notbody>"), "invalid.xml")
        self.add_source(source(pmcid="PMC202", doi="10.test/new"), "valid.xml", "PMC202")
        worker = self.worker()
        worker.seed_known()
        worker.reused()
        self.assertEqual(list(worker.ledger.db.execute("SELECT status FROM catalog ORDER BY row_number")),
                         [("rejected",), ("processed",)])
        self.assertEqual(worker.ledger.db.execute("SELECT pmcid FROM records").fetchone()[0], "PMC202")


if __name__ == "__main__":
    unittest.main()
