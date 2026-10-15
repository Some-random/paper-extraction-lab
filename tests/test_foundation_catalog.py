"""Token accounting remains numeric, sourced, and distinct from data counts."""
import copy
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundation_catalog import TOKEN_FIELDS, render, token_amount, validate_token_budgets


def entry():
    data = json.loads((ROOT / 'reports/bio_foundation_review_2026-10-15/review.json').read_text())
    return copy.deepcopy(next(e for e in data['models'] if e['id'] == 'biomedlm'))


class TokenAccountingChecks(unittest.TestCase):
    def test_corpus_and_exposure_are_separate_numeric_csv_rows(self):
        model = entry()
        data = dict(models=[model], training_studies=[], method_references=[], corpora=[])
        before = copy.deepcopy(data)
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.assertEqual(render(data, directory), 1)
            table = (directory / 'README.md').read_text()
            self.assertIn('Online-paper tokens | Web-URL tokens | Existing-dataset tokens', table)
            self.assertNotIn('| Data summary |', table)
            self.assertIn('34.6B', table)
            self.assertIn('300B', table)
            with (directory / 'catalog.csv').open(newline='') as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['existing_datasets_tokens'], '34600000000')
            self.assertEqual(rows[1]['existing_datasets_tokens'], '300000000000')
            self.assertEqual(rows[0]['count_basis'], 'Corpus')
            self.assertEqual(rows[1]['count_basis'], 'Training exposure')
            snapshots = {p.relative_to(directory): p.read_bytes() for p in directory.rglob('*') if p.is_file()}
            render(data, directory)
            self.assertEqual(snapshots, {p.relative_to(directory): p.read_bytes() for p in directory.rglob('*') if p.is_file()})
        self.assertEqual(data, before)

    def test_unknown_is_not_zero_and_bounds_are_visible(self):
        self.assertEqual(token_amount(dict(status='not_reported', tokens=None)), 'NR')
        self.assertEqual(token_amount(dict(status='reported', tokens=26000000000, relation='greater_than')), '>26B')
        self.assertEqual(token_amount(dict(status='reported', tokens=25600000000, relation='at_least')), '≥25.6B')
        self.assertEqual(token_amount(dict(status='explicit_zero', tokens=0, relation='exact')), '0')
        bad = entry()
        bad['token_budgets'][0]['counts']['existing_datasets'] = dict(status='not_reported', tokens=0, note='Unknown')
        with self.assertRaises(ValueError):
            validate_token_budgets(bad)

    def test_non_token_units_and_unsupported_calculations_are_rejected(self):
        bad = entry()
        bad['token_budgets'][0]['counts']['existing_datasets']['unit'] = 'papers'
        with self.assertRaises(ValueError):
            validate_token_budgets(bad)
        bad = entry()
        quantity = bad['token_budgets'][0]['counts']['existing_datasets']
        quantity['status'] = 'derived'
        with self.assertRaises(ValueError):
            validate_token_budgets(bad)

    def test_allocation_and_source_evidence_are_required(self):
        bad = entry()
        bad['token_budgets'][0]['counts']['total']['tokens'] = 1
        with self.assertRaises(ValueError):
            validate_token_budgets(bad)
        bad = entry()
        bad['token_budgets'][0]['sources'] = []
        with self.assertRaises(ValueError):
            validate_token_budgets(bad)
        bad = entry()
        del bad['token_budgets'][0]['counts']['web_urls']
        with self.assertRaises(ValueError):
            validate_token_budgets(bad)

    def test_entire_registry_has_complete_typed_accounting(self):
        data = json.loads((ROOT / 'reports/bio_foundation_review_2026-10-15/review.json').read_text())
        all_entries = [e for group in ('models', 'training_studies', 'method_references', 'corpora') for e in data[group]]
        self.assertEqual(len(all_entries), 41)
        for model in all_entries:
            with self.subTest(model=model['id']):
                validate_token_budgets(model)
                for budget in model['token_budgets']:
                    self.assertEqual(set(budget['counts']), set(TOKEN_FIELDS))


if __name__ == '__main__':
    unittest.main()
