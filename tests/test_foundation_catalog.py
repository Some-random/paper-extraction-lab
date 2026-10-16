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


def entry(name='biomedlm'):
    data = json.loads((ROOT / 'reports/bio_foundation_review_2026-10-15/review.json').read_text())
    return copy.deepcopy(next(e for group in ('models', 'training_studies', 'method_references', 'corpora')
                              for e in data[group] if e['id'] == name))


class TokenAccountingChecks(unittest.TestCase):
    def test_corpus_and_exposure_are_separate_numeric_csv_rows(self):
        model = entry()
        data = dict(models=[model], training_studies=[], method_references=[], corpora=[])
        before = copy.deepcopy(data)
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.assertEqual(render(data, directory), 1)
            table = (directory / 'README.md').read_text()
            self.assertIn('Online-paper tokens / origin | Web-URL tokens | Existing-dataset tokens', table)
            self.assertNotIn('| Data summary |', table)
            self.assertIn('34.6B', table)
            self.assertEqual(table.count('[BioMedLM]('), 1)
            detail = (directory / 'papers/biomedlm.md').read_text()
            self.assertIn('34.6B', detail)
            self.assertIn('300B', detail)
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

    def test_overview_separates_cpt_initialization_and_preserves_archived_evidence(self):
        data = json.loads((ROOT / 'reports/bio_foundation_review_2026-10-15/review.json').read_text())
        all_entries = [e for group in ('models', 'training_studies', 'method_references', 'corpora') for e in data[group]]
        cpt = {e['id'] for e in all_entries if e['presentation']['section'] == 'cpt'}
        scratch = {e['id'] for e in all_entries if e['presentation']['section'] == 'from_scratch'}
        self.assertEqual(len(cpt), 11)
        self.assertEqual(scratch, {'biogpt', 'biomedlm', 'pubmedbert', 'biolinkbert', 'galactica'})
        self.assertTrue({'biomed_enriched', 'pmc_intercpt', 'bio_posttraining'} <= cpt)
        self.assertTrue(cpt.isdisjoint({'txgemma', 'txllm', 'bioreason', 'meditron', 'olmo3', 'ryze'}))
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            render(data, directory)
            overview = (directory / 'README.md').read_text()
            for e in all_entries:
                target = f"(papers/{e['id']}.md)"
                self.assertEqual(overview.count(target), int(e['id'] in cpt | scratch))
                self.assertTrue((directory / f"papers/{e['id']}.md").exists())
            for hidden in ('catalog.csv', 'review.json', 'verification.json',
                           'Training-data and curation studies', 'Method context',
                           'Medical context', 'bio-evaluation', 'What is counted'):
                self.assertNotIn(hidden, overview)
            gravity = next(e for e in all_entries if e['id'] == 'gravity_bio')
            budget = next(b for b in gravity['token_budgets'] if b['id'] == gravity['presentation']['budget_id'])
            self.assertEqual(budget['counts']['total']['status'], 'not_reported')
            self.assertEqual(budget['counts']['web_urls']['status'], 'not_reported')

    def test_mixed_data_requires_explicit_scope_and_quantity_type(self):
        data = json.loads((ROOT / 'reports/bio_foundation_review_2026-10-15/review.json').read_text())
        model = copy.deepcopy(next(e for e in data['models'] if e['id'] == 'biomatrix'))
        self.assertIn('general', model['presentation']['data_scope'])
        self.assertIn('FineWeb-Edu', model['presentation']['biology_scope_note'])
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            single = dict(models=[model], training_studies=[], method_references=[], corpora=[])
            render(single, directory)
            with (directory / 'catalog.csv').open(newline='') as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row['quantity_type'], 'dataset')
            self.assertIn('general', row['data_scope'])
            del model['presentation']['data_scope']
            with self.assertRaises(ValueError):
                render(single, directory)

    def test_unknown_is_not_zero_and_bounds_are_visible(self):
        self.assertEqual(token_amount(dict(status='not_reported', tokens=None)), 'NR')
        self.assertEqual(token_amount(dict(status='reported', tokens=26000000000, relation='greater_than')), '>26B')
        self.assertEqual(token_amount(dict(status='reported', tokens=25600000000, relation='at_least')), '≥25.6B')
        self.assertEqual(token_amount(dict(status='explicit_zero', tokens=0, relation='exact')), '0')
        bad = entry()
        bad['token_budgets'][0]['counts']['existing_datasets'] = dict(status='not_reported', tokens=0, note='Unknown')
        with self.assertRaises(ValueError):
            validate_token_budgets(bad)

    def test_biomatrix_bound_includes_all_identified_dataset_buckets(self):
        data = json.loads((ROOT / 'reports/bio_foundation_review_2026-10-15/review.json').read_text())
        model = next(e for e in data['models'] if e['id'] == 'biomatrix')
        counts = model['token_budgets'][0]['counts']
        amount = counts['existing_datasets']
        self.assertEqual(amount['tokens'], 176_700_000_000)
        self.assertEqual(amount['tokens'], 25_600_000_000 + 77_400_000_000 + 73_700_000_000)
        self.assertEqual(amount['status'], 'derived')
        self.assertEqual(amount['relation'], 'at_least')
        self.assertEqual(counts['total']['tokens'], 304_400_000_000)
        self.assertEqual(counts['online_papers']['status'], 'not_reported')
        self.assertEqual(counts['web_urls']['status'], 'not_reported')
        validate_token_budgets(model)

    def test_overall_paper_assessment_requires_all_five_dimensions_and_sources(self):
        model = entry()
        single = dict(models=[model], training_studies=[], method_references=[], corpora=[])
        self.assertTrue(model['author_institutions']['authors'])
        self.assertIn('The Pile: PubMed Central', model['dataset_sources']['names'])
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            render(single, directory)
            page = (directory / 'papers/biomedlm.md').read_text()
            self.assertIn('## Overall paper assessment', page)
            self.assertIn('**Contribution and originality:**', page)
            self.assertIn('**Technical soundness:**', page)
            self.assertIn('**Evaluation:**', page)
            self.assertIn('**Reproducibility:**', page)
            self.assertIn('**Clarity and limitations:**', page)
            self.assertNotIn('## Evidence assessment', page)
            self.assertIn('## Authors and institutions', page)
            self.assertIn('## Existing-dataset sources', page)
            original = copy.deepcopy(model['paper_quality'])
            model['paper_quality']['sources'] = []
            with self.assertRaises(ValueError):
                render(single, directory)
            model['paper_quality'] = copy.deepcopy(original)
            del model['paper_quality']['dimensions']['contribution']
            with self.assertRaises(ValueError):
                render(single, directory)
            model['paper_quality'] = copy.deepcopy(original)
            model['paper_quality']['overall'] = 'prestigious institution'
            with self.assertRaises(ValueError):
                render(single, directory)

    def test_paper_origins_distinguish_direct_downloads_from_imported_corpora(self):
        direct, reused = entry('biobert'), entry('biomedlm')
        single = dict(models=[direct, reused], training_studies=[], method_references=[], corpora=[])
        original_budgets = [copy.deepcopy(e['token_budgets']) for e in single['models']]
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            render(single, directory)
            overview = (directory / 'README.md').read_text()
            self.assertIn('PubMed abstracts; PMC full text', overview)
            self.assertIn('0<br>[via The Pile PubMed components (reused)]', overview)
            with (directory / 'catalog.csv').open(newline='') as handle:
                rows = list(csv.DictReader(handle))
            imported = next(row for row in rows if row['id'] == 'biomedlm')
            self.assertEqual(imported['direct_paper_sources'], '')
            self.assertEqual(imported['reused_paper_sources'], 'The Pile PubMed components')
            self.assertEqual(imported['online_papers_tokens'], '0')
            self.assertEqual(imported['existing_datasets_tokens'], '34600000000')
        self.assertEqual([e['token_budgets'] for e in single['models']], original_budgets)

    def test_modalities_keep_domain_buckets_and_later_encoder_inputs_distinct(self):
        matrix, nature, later = entry('biomatrix'), entry('naturelm'), entry('biomedgpt')
        single = dict(models=[matrix, nature, later], training_studies=[], method_references=[], corpora=[])
        original_budgets = [copy.deepcopy(e['token_budgets']) for e in single['models']]
        self.assertTrue(any(i['tokens'] == 36_000_000_000 and i['measurement'] == 'modality'
                            for i in matrix['modality_profile']['items']))
        self.assertTrue(any(i['tokens'] == 65_200_000_000 and i['measurement'] == 'domain_bucket'
                            for i in nature['modality_profile']['items']))
        self.assertTrue(all(i['measurement'] == 'presence' and i['tokens'] is None
                            for i in later['modality_profile']['items']))
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            render(single, directory)
            overview = (directory / 'README.md').read_text()
            self.assertIn('| Other modalities | Overall paper assessment |', overview)
            self.assertIn('None in literature CPT; later biological encoders', overview)
            self.assertIn('already included in the acquisition columns', overview)
            with (directory / 'catalog.csv').open(newline='') as handle:
                rows = list(csv.DictReader(handle))
            matrix_row = next(row for row in rows if row['id'] == 'biomatrix')
            self.assertEqual(matrix_row['total_tokens'], '304400000000')
            self.assertEqual(matrix_row['existing_datasets_tokens'], '176700000000')
        self.assertEqual([e['token_budgets'] for e in single['models']], original_budgets)

    def test_modalities_require_provenance_and_cannot_infer_tokens_from_presence(self):
        for mutation in ('sources', 'items', 'amount', 'presence'):
            model = entry('biomatrix')
            profile = model['modality_profile']
            if mutation == 'sources':
                profile['sources'] = []
            elif mutation == 'items':
                del profile['items']
            elif mutation == 'amount':
                profile['items'][0]['tokens'] = -1
            else:
                profile['items'][0]['measurement'] = 'presence'
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                single = dict(models=[model], training_studies=[], method_references=[], corpora=[])
                with self.assertRaises(ValueError):
                    render(single, Path(temporary))

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
