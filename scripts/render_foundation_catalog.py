#!/usr/bin/env python3
"""Render the biological pretraining review and its supporting source records."""
import csv
import io
import json
import re
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports/bio_foundation_review_2026-10-15'
GROUPS = ['models', 'training_studies', 'method_references', 'corpora']
LABELS = [
    ('stage', 'Training stage'), ('base', 'Backbone'), ('corpus', 'Source material and units'),
    ('document_route', 'Acquisition and document processing'), ('curation', 'Cleaning and filtering'),
    ('training_unit_and_mix', 'Training unit and mixture'), ('augmentation', 'Generated or augmented material'),
    ('evidence', 'Author-reported evidence'), ('disclosure_gap', 'Disclosure gaps'),
    ('source_sections', 'Source sections'),
]
RECORD_LABELS = {'source_material': 'Source material', 'data_budget': 'Datasets and amounts',
                 'figures': 'Figure handling', 'citations': 'Citation handling'}
TOKEN_FIELDS = ('online_papers', 'web_urls', 'existing_datasets', 'total')
TOKEN_HEADER = '| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |'
TOKEN_SEPARATOR = '|---|---|---:|---:|---:|---:|---|'
TOKEN_RELATIONS = {'exact': '', 'approximate': '≈', 'greater_than': '>', 'at_least': '≥'}


def token_amount(amount):
    """Format verified token counts, never document/word counts or implied zeroes."""
    if amount['status'] == 'not_reported':
        return 'NR'
    value = amount['tokens']
    for scale, suffix in ((10**12, 'T'), (10**9, 'B'), (10**6, 'M'), (10**3, 'K')):
        if value >= scale:
            value = Decimal(value) / Decimal(scale)
            rendered = format(value, 'f')
            if '.' in rendered:
                rendered = rendered.rstrip('0').rstrip('.')
            return TOKEN_RELATIONS[amount['relation']] + rendered + suffix
    return TOKEN_RELATIONS[amount['relation']] + str(value)


def validate_token_budgets(entry):
    budgets = entry.get('token_budgets')
    if not budgets:
        raise ValueError('Missing token budgets: ' + entry['id'])
    ids = set()
    for budget in budgets:
        if budget['id'] in ids:
            raise ValueError('Duplicate token budget: ' + entry['id'])
        ids.add(budget['id'])
        if not budget.get('stage') or not budget.get('basis') or not budget.get('token_kind'):
            raise ValueError('Missing stage/count basis: ' + entry['id'])
        if not budget.get('sources') or any(not s.get('url', '').startswith('https://') for s in budget['sources']):
            raise ValueError('Missing token-budget evidence: ' + entry['id'])
        counts = budget['counts']
        if set(counts) != set(TOKEN_FIELDS):
            raise ValueError('Incomplete acquisition columns: ' + entry['id'])
        for field, amount in counts.items():
            if not amount.get('note'):
                raise ValueError('Missing count qualification: ' + entry['id'] + '/' + field)
            if amount['status'] == 'not_reported':
                if amount.get('tokens') is not None:
                    raise ValueError('Unknown count must not contain a number: ' + entry['id'])
            elif amount['status'] in {'reported', 'derived', 'explicit_zero'}:
                value = amount.get('tokens')
                if type(value) is not int or value < 0 or amount.get('unit') != 'tokens':
                    raise ValueError('Only nonnegative integer token counts are accepted: ' + entry['id'])
                if value == 0 and amount['status'] != 'explicit_zero':
                    raise ValueError('Zero requires explicit evidence of absence: ' + entry['id'])
                if amount.get('relation') not in TOKEN_RELATIONS:
                    raise ValueError('Unknown token relation: ' + entry['id'])
                if amount['status'] == 'derived' and not amount.get('calculation'):
                    raise ValueError('Derived token count requires its calculation: ' + entry['id'])
            else:
                raise ValueError('Unknown token-count status: ' + entry['id'])
        if counts['total']['status'] != 'not_reported':
            known_minimum = sum(counts[k].get('tokens') or 0 for k in TOKEN_FIELDS[:-1])
            if known_minimum > counts['total']['tokens'] + budget.get('rounding_tolerance_tokens', 0):
                raise ValueError('Known category amounts exceed total: ' + entry['id'])
        if budget.get('partition_complete'):
            if any(counts[k]['status'] == 'not_reported' or counts[k]['relation'] != 'exact' for k in TOKEN_FIELDS):
                raise ValueError('Complete partition requires exact known counts: ' + entry['id'])
            difference = abs(sum(counts[k]['tokens'] for k in TOKEN_FIELDS[:-1]) - counts['total']['tokens'])
            if difference > budget.get('rounding_tolerance_tokens', 0):
                raise ValueError('Token partition does not reconcile: ' + entry['id'])


def token_row(entry, budget):
    name = f"[{cell(entry['name'])}](papers/{entry['id']}.md#token-counts-by-acquisition-route)<br>{cell(budget['stage'])}"
    basis = cell(budget['basis'] + ' · ' + budget['token_kind'])
    amounts = [token_amount(budget['counts'][key]) for key in TOKEN_FIELDS]
    refs = ' · '.join(f"[{cell(s['label'])}]({s['url']})" for s in budget['sources'])
    return '| ' + ' | '.join([name, basis] + amounts + [refs]) + ' |'


def overview_budget(entry):
    selected = entry['presentation']['budget_id']
    return next(b for b in entry['token_budgets'] if b['id'] == selected)


def overview_row(entry):
    """One explicitly selected budget per study; never mix corpus and exposure."""
    budget = overview_budget(entry)
    view = entry['presentation']
    name = f"[{cell(view.get('name', entry['name']))}](papers/{entry['id']}.md)"
    name += '<br>' + cell(view['starting_model'])
    amounts = [token_amount(budget['counts'][key]) for key in TOKEN_FIELDS]
    refs = ' · '.join(f"[{cell(s['label'])}]({s['url']})" for s in budget['sources'])
    return '| ' + ' | '.join([name] + amounts + [cell(view['count_label']), refs]) + ' |'


def overview_table(entries):
    return '\n'.join([
        '| Model / starting checkpoint | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | What is counted | Source |',
        '|---|---:|---:|---:|---:|---|---|',
        *(overview_row(entry) for entry in entries),
    ])


def clean(value):
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', value).replace('**', '').replace('`', '')


def cell(value):
    return value.replace('|', '\\|').replace('\n', '<br>')


def render(data, directory=REPORT):
    all_entries = [(kind, e) for kind in GROUPS for e in data.get(kind, [])]
    ids = [e['id'] for _, e in all_entries]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate catalog IDs')
    for _, entry in all_entries:
        if not re.fullmatch(r'[a-z0-9_]+', entry['id']) or not entry.get('sources'):
            raise ValueError('Invalid ID or missing source: ' + entry['id'])
        validate_token_budgets(entry)
        view = entry.get('presentation')
        if not view or view.get('section') not in {'cpt', 'from_scratch', 'other', 'methods', 'corpora', 'archive'}:
            raise ValueError('Missing review scope: ' + entry['id'])
        if view['section'] in {'cpt', 'from_scratch'}:
            if not view.get('starting_model') or not view.get('count_label') or not view.get('initialization_source'):
                raise ValueError('Missing pretraining classification evidence: ' + entry['id'])
            if view.get('budget_id') not in {b['id'] for b in entry['token_budgets']}:
                raise ValueError('Unknown overview budget: ' + entry['id'])
    pages = directory / 'papers'
    pages.mkdir(exist_ok=True)
    for kind, entry in all_entries:
        eid = entry['id']
        body = [f"# {entry['name']}", '[Biological pretraining review](../README.md)',
                entry.get('category', ''),
                'This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.']
        view = entry['presentation']
        if view['section'] == 'archive':
            body.append('Archived reference outside the current biological pretraining review.')
        if view['section'] in {'cpt', 'from_scratch'}:
            training = 'Continued pretraining' if view['section'] == 'cpt' else 'Pretraining from scratch'
            body.append(f"**Training approach:** {training}. **Starting checkpoint:** {view['starting_model']}. "
                        f"[Initialization evidence]({view['initialization_source']})")
            if view.get('note'):
                body.append(view['note'])
        body.append('## Token counts by acquisition route')
        lines = [TOKEN_HEADER, TOKEN_SEPARATOR]
        for budget in entry['token_budgets']:
            lines.append(token_row(entry, budget).replace(f"papers/{eid}.md#token-counts-by-acquisition-route", '#token-counts-by-acquisition-route'))
        body.append('\n'.join(lines))
        for budget in entry['token_budgets']:
            body.append(f"**{budget['stage']} — {budget['basis']} ({budget['token_kind']}):** {budget['note']}")
            for key in TOKEN_FIELDS:
                amount = budget['counts'][key]
                explanation = amount['note']
                if amount.get('calculation'):
                    explanation += ' Calculation: ' + amount['calculation'] + '.'
                body.append(f"- **{key.replace('_', ' ').title()}: {token_amount(amount)}.** {explanation}")
        for key, label in LABELS:
            if entry.get(key):
                body.append(f"**{label}:** {entry[key]}")
        records = entry.get('data_records', [])
        for record_kind, title in RECORD_LABELS.items():
            matching = [r for r in records if r['kind'] == record_kind]
            if not matching:
                continue
            body.append('## ' + title)
            for record in matching:
                body.append(record['source_model_label'])
                lines = ['| Reported field | Retained source statement |', '|---|---|']
                lines.extend(f'| {cell(k)} | {cell(v)} |' for k, v in record['fields'].items())
                body.append('\n'.join(lines))
        if entry.get('notes'):
            body.append('## Source details and qualifications')
            body.extend(entry['notes'])
        body.append('## Primary sources')
        body.append('\n'.join(f"- [{s['title']}]({s['url']})" for s in entry['sources']))
        body.append('Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.')
        (pages / (eid + '.md')).write_text('\n\n'.join(body) + '\n')

    def selected(section):
        return sorted((e for _, e in all_entries if e['presentation']['section'] == section),
                      key=lambda e: e['presentation'].get('order', 100))

    intro = [
        '# Biological continued pretraining: data sources and token budgets',
        'How biological foundation models turn research papers, web content and existing datasets '
        'into training data. The main comparison focuses on **continued pretraining (CPT)**: '
        'starting with a pretrained model and training it further on domain data. '
        'Data-curation studies and released models appear together because both inform this choice.',
        '## Continued pretraining',
        'Each row names the starting checkpoint and reports one clearly identified token budget. '
        'The linked study pages explain extraction, filtering, figures, citations and all reported counts.',
        overview_table(selected('cpt')),
        '### Reading the counts',
        '- **Online papers:** text acquired directly from publishers or publication repositories, '
        'including abstracts, XML, PDF and LaTeX.\n'
        '- **Web URLs:** non-paper webpages acquired directly, including raw web archives.\n'
        '- **Existing datasets:** reused corpora and biological databases. Paper text imported through '
        'S2ORC or The Pile belongs here; it is not counted twice. These columns describe **how the study '
        'obtained the data**, not just what the text discusses.\n'
        '- **0** means the described data has no separate acquisition through that route. **NR** means '
        'the token amount is not reported or cannot be established. Neither a known source name nor a '
        'paper count supplies a missing token count.\n'
        '- **Dataset size** counts the prepared corpus before training repeats. **Tokens used in training** '
        'counts consumption, including repeated passes. For example, BioMedLM has a 34.6B-token corpus '
        'and uses 300B tokens during training. The overview shows one selected count per study; both '
        'remain on the study page.\n'
        '- **M / B** mean million / billion; **≈** means approximate; **> / ≥** indicate a lower bound. '
        'Tokenizers differ. Sequence/image tokens and planned token positions are labeled explicitly. '
        'A total may include material without a disclosed category split.',
        'Gravity-bio reports separate literature and biological-database components but not the full '
        'training mixture. LOGOS reports a corpus spanning pretraining and post-training; its CPT-only '
        'amount is not disclosed. BioMamba’s figure counts packed positions, including padding. '
        'Biomed-Enriched’s 33.6B is the training budget **per experimental variant**. '
        'PMC-InterCPT contributes a paper/figure curation method evaluated on medical and scientific tasks; '
        'it is not evidence that clinical filtering is appropriate for all biology.',
        '## Pretraining from scratch: comparison',
        'These models begin with randomly initialized weights and biological or scientific data, '
        'rather than adapting an existing checkpoint. They provide a comparison with CPT.',
        overview_table(selected('from_scratch')),
        'BioGPT’s 104.8576B is calculated from its scheduled steps and batch size, not a measured unique '
        'corpus size. Galactica includes broad scientific material as well as biology. '
        'NatureLM’s 8B and 8×7B versions belong in the CPT table; its separate 1B model first undergoes '
        'general-text pretraining on SlimPajama before scientific training.',
        '## Data preparation',
        'See the guides to [biological sources](source_planning.md), '
        '[web and reusable corpora](web_acquisition.md), [original figures and context](figure_handling.md), '
        'and [citation handling](citations_and_cpt_sources.md). '
        '[Supporting literature](background.md) covers source corpora, extraction pipelines, '
        'instruction tuning and representation learning.',
    ]
    (directory / 'README.md').write_text('\n\n'.join(intro) + '\n')

    background = ['# Supporting literature', '[Biological pretraining review](README.md)',
                  'These references inform data preparation or other training objectives. '
                  'Their budgets are not biological CPT budgets.']
    for title, section in [('Reusable source corpora', 'corpora'),
                           ('Extraction and general training pipelines', 'methods'),
                           ('Other biological training approaches', 'other')]:
        background.append('## ' + title)
        background.append('\n'.join(f"- [{e['name']}](papers/{e['id']}.md): {e['presentation']['note']}"
                                    for e in selected(section)))
    (directory / 'background.md').write_text('\n\n'.join(background) + '\n')
    archived = ['# Archived references', '[Biological pretraining review](README.md)',
                'Medical and clinical-model references retained from the earlier broader review. '
                'They are outside the current review scope and do not appear in the main comparison.']
    archived.append('\n'.join(f"- [{e['name']}](papers/{e['id']}.md)" for e in selected('archive')))
    (directory / 'archive.md').write_text('\n\n'.join(archived) + '\n')

    maintenance = ['# Maintaining the literature review',
                   'Edit [review.json](review.json), then run `python3 scripts/render_foundation_catalog.py` '
                   'from the repository root. This produces the review, supporting pages, study pages '
                   'and [numeric CSV](catalog.csv) from one registry.',
                   'The `presentation` record selects the review section, starting checkpoint and one '
                   'overview budget. It must cite initialization evidence. Keep every original budget '
                   'in `token_budgets`; selecting an overview row never changes a reported amount. '
                   'CPT studies belong with CPT models regardless of publication type. '
                   'Do not classify instruction tuning, contrastive learning or random initialization as CPT.',
                   'The [token audit](token_budget_verification.json) records numerical checks and '
                   'source snapshots. [Archived references](archive.md) preserve earlier out-of-scope material.',
                   'Evaluation protocols, benchmark cases and runs live in the separate private '
                   '[bio-evaluation repository](https://github.com/Some-random/bio-evaluation). '
                   'This repository holds extraction work and public literature notes. '
                   'Private evaluation links remain in the registry as provenance, not public review navigation.']
    (directory / 'maintenance.md').write_text('\n\n'.join(maintenance) + '\n')
    stream = io.StringIO()
    fields = ['id', 'budget_id', 'name', 'kind', 'scope', 'review_section', 'overview_selected',
              'starting_model', 'stage', 'count_basis', 'token_kind']
    for key in TOKEN_FIELDS:
        fields.extend([key + '_tokens', key + '_relation', key + '_status'])
    fields.extend(['details', 'primary_sources', 'qualification'])
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader()
    for kind, e in all_entries:
        for budget in e['token_budgets']:
            row = {'id':e['id'], 'budget_id':budget['id'], 'name':e['name'], 'kind':kind,
                'scope':e.get('scope_group',e.get('category','')), 'stage':budget['stage'],
                'review_section':e['presentation']['section'],
                'overview_selected':budget['id'] == e['presentation'].get('budget_id'),
                'starting_model':e['presentation'].get('starting_model', ''),
                'count_basis':budget['basis'], 'token_kind':budget['token_kind'],
                'details':f"papers/{e['id']}.md#token-counts-by-acquisition-route",
                'primary_sources':' ; '.join(s['url'] for s in budget['sources']), 'qualification':budget['note']}
            for key in TOKEN_FIELDS:
                amount = budget['counts'][key]
                row[key + '_tokens'] = amount.get('tokens', '')
                row[key + '_relation'] = amount.get('relation', '')
                row[key + '_status'] = amount['status']
            writer.writerow(row)
    (directory / 'catalog.csv').write_text(stream.getvalue())
    return len(all_entries)


if __name__ == '__main__':
    print(f'Rendered {render(json.loads((REPORT / "review.json").read_text()))} unique catalog entries')
