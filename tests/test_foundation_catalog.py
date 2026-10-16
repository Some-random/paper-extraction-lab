"""Token accounting remains numeric, sourced, and distinct from data counts."""
import copy
import csv
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundation_catalog import TOKEN_FIELDS, render, token_amount, validate_token_budgets
from source_inventory import build_source_inventory


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
            self.assertIn('Paper tokens /<br>origin | Dataset tokens /<br>sources', table)
            self.assertNotIn('Direct web tokens', table)
            self.assertNotIn('| Data summary |', table)
            self.assertIn('34.6B', table)
            self.assertEqual(table.count('| BioMedLM (2024)<br>'), 1)
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
            self.assertEqual(rows[0]['paper_year'], '2024')
            self.assertIn('arxiv.org/abs/2403.18421', rows[0]['paper_year_source'])
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
            self.assertNotIn('Random weights;', overview)
            self.assertIn('| Model /<br>architecture |', overview)
            for eid in scratch:
                page = (directory / f'papers/{eid}.md').read_text()
                self.assertIn('**Architecture:**', page)
                self.assertNotIn('Random weights;', page)
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

    def test_source_inventory_keeps_legacy_scenarios_separate_from_current_amounts(self):
        report = ROOT / 'reports/bio_foundation_review_2026-10-15'
        data = json.loads((report / 'review.json').read_text())
        estimate = json.loads((report / 'starter_corpus_estimate.json').read_text())
        before = copy.deepcopy((data, estimate))
        central = estimate['scenarios']['central']
        self.assertAlmostEqual(sum(central['research_starter_content_tokens'].values()),
                               central['research_starter_total_tokens'])
        self.assertAlmostEqual(sum(central['acquisition_route_tokens'].values()),
                               central['research_starter_total_tokens'])
        storage = estimate['storage']
        for total, allowance in zip(storage['central_overall_working_bytes'],
                                    storage['text_sequence_processing_allowance_GiB']):
            self.assertAlmostEqual(total, storage['central_paper_pdf_figure_bytes_proxy'] + allowance * 2**30)
        self.assertGreaterEqual(storage['recommended_initial_capacity_tib'] * 2**40,
                                max(storage['central_overall_working_bytes']))
        self.assertGreater(estimate['paper_availability']['broader_xml_candidates'],
                           estimate['paper_availability']['journal_subset_xml_candidates'])
        self.assertGreater(estimate['paper_availability']['archive_article_records_rounded'],
                           estimate['paper_availability']['broader_xml_candidates'])
        volume = estimate['paper_text_scenarios']
        self.assertEqual(volume['gross_text_tokens'],
                         [volume['candidate_papers'] * n for n in volume['assumed_tokens_per_paper']])
        self.assertIsNone(estimate['current_web_and_record_inventory']['web_research_retention'])
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            render(data, directory, starter_estimate=estimate)
            overview = (directory / 'README.md').read_text()
            self.assertEqual(overview.rsplit('\n## ', 1)[1].splitlines()[0], 'Available training data')
            self.assertNotIn('49.1B', overview)
            self.assertNotIn('reserve about 4TiB', overview)
            self.assertNotIn('12.5 million', overview)
            self.assertNotIn('552,024', overview)
            self.assertIn('197–340B candidate', overview)
            self.assertIn('complete biological-corpus total is not yet established', overview)
            self.assertIn('85.7B', overview)
            self.assertIn('37.0B', overview)
            self.assertIn('8.8T reported nucleotide positions', overview)
            self.assertIn('87 source families', overview)
            inventory_page = (directory / 'source_inventory.md').read_text()
            for family in estimate['aggregation']['families']:
                self.assertIn(family['name'], inventory_page)
            self.assertTrue(all(not source['included_in_starter_forecast']
                                for source in estimate['larger_source_inventory']))
            for removed in ('GPU-hours', '**Processing:**', 'Direct web tokens'):
                self.assertNotIn(removed, overview)
            with (directory / 'catalog.csv').open(newline='') as handle:
                rows = list(csv.DictReader(handle))
            for group in ('models', 'training_studies', 'method_references', 'corpora'):
                for study in data[group]:
                    for budget in study['token_budgets']:
                        exported = next(row for row in rows if row['id'] == study['id']
                                        and row['budget_id'] == budget['id'])
                        for route in TOKEN_FIELDS:
                            tokens = budget['counts'][route].get('tokens')
                            self.assertEqual(exported[route + '_tokens'], '' if tokens is None else str(tokens))
        self.assertEqual((data, estimate), before)

    def test_full_source_register_does_not_add_aliases_or_invent_missing_counts(self):
        report = ROOT / 'reports/bio_foundation_review_2026-10-15'
        data = json.loads((report / 'review.json').read_text())
        estimate = json.loads((report / 'starter_corpus_estimate.json').read_text())
        registry = build_source_inventory(data, estimate)
        self.assertIsNone(registry['complete_biology_only_unique_total'])
        self.assertEqual(registry['unresolved_study_source_details'], [])
        self.assertEqual(len([row for row in registry['families'] if row['id'] == 'uniprot']), 1)
        self.assertEqual({row['id'] for row in registry['components']}, {'pmc','finefineweb','biocollection'})
        self.assertAlmostEqual(registry['quantified_candidate_subtotal_low'],
                               sum(row['low'] for row in registry['components']))
        matrix = next(e for e in data['models'] if e['id'] == 'biomatrix')
        matrix['dataset_sources']['names'].append('UniProt')
        repeated = build_source_inventory(data, estimate)
        self.assertEqual(registry['quantified_candidate_subtotal_high'], repeated['quantified_candidate_subtotal_high'])
        matrix['dataset_sources']['names'].append('A new unregistered source')
        with self.assertRaisesRegex(ValueError, 'Unmapped named source'):
            build_source_inventory(data, estimate)

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
            self.assertIn('0<br>via The Pile PubMed components (reused)', overview)
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
            self.assertIn('| Other modalities /<br>tokens | Total<br>tokens | Paper<br>assessment |', overview)
            self.assertIn('Text-only CPT; molecule/protein encoders used later', overview)
            self.assertIn('already included in the acquisition columns', overview)
            self.assertIn('Protein: 77.4B (1D 36B; 3D 38.5B; other 2.9B)', overview)
            self.assertIn('Molecule: 73.7B (1D 32.1B; 3D 17.6B; other 24B)', overview)
            self.assertIn('Cross-entity: 48B (1D 17.1B; 3D 11.4B; other 19.5B)', overview)
            self.assertIn('DNA: 19.8B', overview)
            self.assertIn('RNA: 27.5B', overview)
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

    def test_quality_sort_with_alphabetical_ties_and_later_author_column(self):
        data = json.loads((ROOT / 'reports/bio_foundation_review_2026-10-15/review.json').read_text())
        all_entries = [e for group in ('models', 'training_studies', 'method_references', 'corpora')
                       for e in data[group]]
        quality_order = {'strong': 0, 'solid': 1, 'mixed': 2, 'weak': 3}
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            render(data, directory)
            overview = (directory / 'README.md').read_text()
            for title, section in (('Continued pretraining', 'cpt'),
                                   ('Pretraining from scratch: comparison', 'from_scratch')):
                part = overview.split('## ' + title + '\n', 1)[1].split('\n## ', 1)[0]
                actual = re.findall(r'^\| .*?\[Notes\]\(papers/([a-z0-9_]+)\.md\) \|$', part, flags=re.M)
                expected = [e['id'] for e in sorted(
                    (e for e in all_entries if e['presentation']['section'] == section),
                    key=lambda e: (quality_order[e['paper_quality']['overall']], e['name'].casefold()))]
                self.assertEqual(actual, expected)
            header = next(line for line in overview.splitlines() if line.startswith('| Model /'))
            self.assertGreater(header.index('Authors /<br>institutions'), header.index('Paper<br>assessment'))
            self.assertGreater(header.index('Authors /<br>institutions'), header.index('Total<br>tokens'))
            self.assertLess(header.index('Other modalities /<br>tokens'), header.index('Total<br>tokens'))

    def test_biomatrix_full_composition_reconciles_without_adding_routes_twice(self):
        model = entry('biomatrix')
        components = {c['label']: c['tokens'] for c in model['corpus_composition']['components']}
        self.assertEqual(components, {'Text': 105_300_000_000, 'Protein data': 77_400_000_000,
                                      'Molecule data': 73_700_000_000, 'Cross-entity data': 48_000_000_000})
        self.assertEqual(sum(components.values()), model['token_budgets'][0]['counts']['total']['tokens'])
        self.assertEqual(sum(i['tokens'] for i in model['modality_profile']['items']), 199_100_000_000)
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            single = dict(models=[model], training_studies=[], method_references=[], corpora=[])
            render(single, directory)
            overview = (directory / 'README.md').read_text()
            self.assertIn('105.3B text + 77.4B protein data + 73.7B molecule data + 48B cross-entity data = 304.4B', overview)
            self.assertIn('127.7B source split unknown', overview)
            detail = (directory / 'papers/biomatrix.md').read_text()
            self.assertIn('## Full corpus composition', detail)
            model['corpus_composition']['components'][0]['tokens'] += 1
            with self.assertRaisesRegex(ValueError, 'does not reconcile'):
                render(single, directory)

    def test_modality_overview_cannot_double_count_or_sum_unknowns(self):
        for mutation in ('overlap', 'unknown_member', 'unknown_count'):
            model = entry('biomatrix')
            profile = model['modality_profile']
            if mutation == 'overlap':
                profile['overview_groups'][1]['members'].append('Protein 1D sequences')
            elif mutation == 'unknown_member':
                profile['overview_groups'][0]['members'][0] = 'Invented sequence bucket'
            else:
                profile['items'][0]['tokens'] = None
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                single = dict(models=[model], training_studies=[], method_references=[], corpora=[])
                with self.assertRaises(ValueError):
                    render(single, Path(temporary))

    def test_galactica_record_totals_do_not_replace_unknown_sequence_counts(self):
        model = entry('galactica')
        items = {i['name']: i for i in model['modality_profile']['items']}
        self.assertEqual(items['UniProt protein records']['tokens'], 600_000_000)
        self.assertEqual(items['PubChem molecule records']['tokens'], 1_000_000_000)
        self.assertEqual(items['RefSeq genome records']['tokens'], 100_000_000)
        self.assertIsNone(items['Protein sequences']['tokens'])
        self.assertIsNone(items['Molecular SMILES']['tokens'])
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            single = dict(models=[model], training_studies=[], method_references=[], corpora=[])
            render(single, directory)
            overview = (directory / 'README.md').read_text()
            self.assertIn('Protein records: ≈600M', overview)
            self.assertIn('Molecule records: ≈1B', overview)
            self.assertIn('pure sequence/SMILES shares not reported', overview)

    def test_overview_consolidates_links_and_keeps_unknowns_distinct_from_zero(self):
        data = json.loads((ROOT / 'reports/bio_foundation_review_2026-10-15/review.json').read_text())
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            render(data, directory)
            overview = (directory / 'README.md').read_text()
            self.assertNotRegex(overview, r'\bNR\b|†|‡')
            self.assertNotIn('repeated passes', overview)
            self.assertNotIn('token positions', overview.lower())
            rows = [line for line in overview.splitlines()
                    if line.startswith('| ') and '[Notes]' in line]
            self.assertEqual(len(rows), 16)
            for row in rows:
                columns = [c.strip() for c in row.strip('|').split('|')]
                self.assertEqual(len(columns), 8)
                self.assertTrue(all('](' not in c for c in columns[:-1]))
                links = re.findall(r'\[([^]]+)\]\(([^)]+)\)', columns[-1])
                self.assertEqual([label for label, _ in links], ['Paper', 'Notes'])
                self.assertEqual(len({url for _, url in links}), 2)
            unknown = next(row for row in rows if row.startswith('| BioBERT (2019)<br>'))
            self.assertIn('| —<br>PubMed abstracts; PMC full text | — | Text only | Not reported |', unknown)
            known_zero = next(row for row in rows if row.startswith('| BioMedLM (2024)<br>'))
            self.assertIn('| 0<br>via The Pile PubMed components (reused) | 34.6B', known_zero)
            self.assertIn('Figure images: not reported', overview)
            # Detailed pages and numeric exports retain all original accounting distinctions.
            detail = (directory / 'papers/biomedlm.md').read_text()
            self.assertIn('Training exposure', detail)
            self.assertIn('300B', detail)
            with (directory / 'catalog.csv').open(newline='') as handle:
                exported = list(csv.DictReader(handle))
            unknown_row = next(row for row in exported if row['id'] == 'biobert')
            self.assertEqual(unknown_row['online_papers_status'], 'not_reported')
            self.assertEqual(unknown_row['online_papers_tokens'], '')

    def test_processing_recipe_stays_separate_from_the_catalog(self):
        data = json.loads((ROOT / 'reports/bio_foundation_review_2026-10-15/review.json').read_text())
        self.assertNotIn('extraction_plan', data)
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            render(data, directory)
            overview = (directory / 'README.md').read_text()
            self.assertNotIn('## What we need to do', overview)
            self.assertNotIn('Next implementation:', overview)
            self.assertNotIn('Build main-content', overview)
            self.assertEqual(overview.count('[Processing recipe](data_pipeline.md)'), 1)
        pipeline = (ROOT / 'reports/bio_foundation_review_2026-10-15/data_pipeline.md').read_text()
        self.assertNotIn('```mermaid', pipeline)
        self.assertNotRegex(pipeline, r'!\[[^\]]*\]\(')
        references = re.findall(r'\[([^\]]+)\]\((https://[^)]+)\)', pipeline)
        self.assertTrue(any('arxiv.org/html/2506.04178' in url for _, url in references))
        self.assertTrue(any('arxiv.org/html/2512.13961' in url for _, url in references))
        self.assertTrue(any('openathena.ai/blog/marin-data-pipeline-overview/' in url
                            for _, url in references))
        self.assertIn('> [!IMPORTANT]', pipeline)
        self.assertEqual(pipeline.count('**References:**'), 6)
        self.assertEqual(re.findall(r'^## ([1-6])\.', pipeline, flags=re.M), list('123456'))
        self.assertNotIn('Method basis:', pipeline)
        self.assertNotIn('**7.', pipeline)
        self.assertNotRegex(pipeline, r'Ryze|XLM-RoBERTa|\b(?:NEXT|WORKING|TO BUILD|PENDING)\b')

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
