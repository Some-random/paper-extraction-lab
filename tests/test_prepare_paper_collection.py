import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("prepare_paper_collection", ROOT / "scripts/prepare_paper_collection.py")
prepare = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prepare)


def xml(pmcid="123", kind="pmc", pmid="456", doi="10.1234/ABC"):
    return (f'<article><front><article-meta><article-id pub-id-type="{kind}">{pmcid}</article-id>'
            f'<article-id pub-id-type="pmid">{pmid}</article-id>'
            f'<article-id pub-id-type="doi">{doi}</article-id></article-meta></front>'
            '<body><sec><p>Biological research.</p></sec></body></article>')


class PreparationTests(unittest.TestCase):
    def test_identifier_variants(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.xml"
            for kind, value in [("pmc", "123"), ("pmcaid", "123"), ("pmcid", "PMC00123")]:
                path.write_text(xml(value, kind))
                result = prepare.article_header(path)
                self.assertEqual(result["pmcid"], "PMC123")
                self.assertEqual(result["pmid"], "456")
                self.assertEqual(result["doi"], "10.1234/abc")

    def test_source_presence_preserves_variants_bad_xml_and_ignores_abstracts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            own = root / "own"
            for folder in ["one/PMC123", "two/PMC123", "PMC789", "PMC999"]:
                (own / folder).mkdir(parents=True)
            (own / "one/PMC123/source.xml").write_text(xml())
            (own / "two/PMC123/source.xml").write_text(xml())
            (own / "PMC789/source.xml").write_text("<article>broken")
            (own / "PMC999/selected_metadata.json").write_text('{"pmcid":"PMC999"}')
            old = root / "old.csv"
            old.write_text("pmcid,pmid,has_sections\nPMC500,100,1\nPMC500,100,1\nPMC600,200,0\n")
            summary = prepare.prepare(root / "out", None, [], [own], old)
            self.assertEqual(summary["native_catalog_variants"], 2)
            self.assertEqual(summary["native_catalog_unique_pmcids"], 1)
            self.assertEqual(summary["presence_unique_pmcids"], 3)
            with (root / "out/presence_ids.csv").open() as handle:
                ids = {row["pmcid"] for row in csv.DictReader(handle)}
            self.assertEqual(ids, {"PMC123", "PMC789", "PMC500"})
            self.assertIn("sha256", summary["frozen_inputs"]["source_catalog.json"])
            with self.assertRaises(FileExistsError):
                prepare.prepare(root / "out", None, [], [own], old)

    def test_external_symlink_cannot_become_reusable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            own = root / "own/PMC123"
            own.mkdir(parents=True)
            outside = root / "outside.xml"
            outside.write_text(xml())
            (own / "source.xml").symlink_to(outside)
            summary = prepare.prepare(root / "out", None, [], [own.parent])
            self.assertEqual(summary["native_catalog_variants"], 0)
            self.assertEqual(summary["presence_unique_pmcids"], 0)
            self.assertEqual(summary["counters"]["outside_explicit_roots"], 1)

    def test_metadata_bound_cannot_turn_huge_frontmatter_into_catalog_record(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paper = root / "own/PMC123"
            paper.mkdir(parents=True)
            (paper / "source.xml").write_text('<article><front>' + ' ' * 10000)
            summary = prepare.prepare(root / "out", None, [], [paper.parent], maximum_metadata_bytes=64)
            self.assertEqual(summary["native_catalog_variants"], 0)
            self.assertEqual(summary["presence_unique_pmcids"], 1)

    def test_valid_abstract_only_xml_does_not_block_fulltext_acquisition(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paper = root / "own/PMC123"
            paper.mkdir(parents=True)
            (paper / "source.xml").write_text(xml().split("<body>")[0] + "</article>")
            summary = prepare.prepare(root / "out", None, [], [paper.parent])
            self.assertEqual(summary["native_catalog_variants"], 0)
            self.assertEqual(summary["presence_unique_pmcids"], 0)
            self.assertEqual(summary["counters"]["abstract_only_native_paths_excluded"], 1)


if __name__ == "__main__":
    unittest.main()
