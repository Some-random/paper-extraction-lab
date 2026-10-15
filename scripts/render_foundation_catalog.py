#!/usr/bin/env python3
"""Render the one shared literature registry into GitHub Markdown and CSV."""
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
TOKEN_HEADER = '| Model / stage | Count basis | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |'
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
    pages = directory / 'papers'
    pages.mkdir(exist_ok=True)
    for kind, entry in all_entries:
        eid = entry['id']
        body = [f"# {entry['name']}", '[Shared literature catalog](../README.md)',
                entry.get('category', ''),
                'This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.']
        if entry.get('scope_group') == 'Medical context retained from earlier review':
            body.append('Historical medical context. Clinical-note acquisition is outside the biological research corpus scope.')
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
        if entry.get('related_project_notes'):
            body.append('## Related evaluation notes')
            body.append('\n'.join(f"- [{s['title']}]({s['url']})" for s in entry['related_project_notes']))
        body.append('Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.')
        (pages / (eid + '.md')).write_text('\n\n'.join(body) + '\n')

    groups = [
        ('Biological research and science models', [(k,e) for k,e in all_entries if k == 'models' and e.get('scope_group') != 'Medical context retained from earlier review']),
        ('Training-data and curation studies', [(k,e) for k,e in all_entries if k == 'training_studies']),
        ('Reusable corpora', [(k,e) for k,e in all_entries if k == 'corpora']),
        ('Method context', [(k,e) for k,e in all_entries if k == 'method_references']),
        ('Medical context retained from earlier review', [(k,e) for k,e in all_entries if k == 'models' and e.get('scope_group') == 'Medical context retained from earlier review']),
    ]
    intro = [
        '# Shared biological foundation-model literature catalog',
        'This is the shared literature home for **paper-extraction-lab** and **bio-evaluation**. '
        'Each model or study has one page combining its paper links, datasets and amounts, '
        'document processing, filtering, augmentation, figure/citation handling and known gaps.',
        f"**{len(data['models'])} model-family entries, {len(data['training_studies'])} training-data studies, "
        f"{len(data['corpora'])} reusable corpora and {len(data['method_references'])} method references.** "
        'These are catalog entries, not a count of distinct publications or an exhaustive census.',
        'The previous source review, dataset breakdown and additional-coverage table are merged here. '
        'The entries below include TheBioCollection/Gravity-bio, NatureLM, BioMatrix, BioReason, '
        'BioReason-Pro, SciReasoner, LOGOS and the earlier models.',
        '[Download the catalog as CSV](catalog.csv) · [Structured source registry](review.json)',
        '[Token-count verification](token_budget_verification.json)',
        'The tables report **token amounts for each acquisition category**, with separate rows for corpus '
        'size and training exposure where those are available. Extraction, filtering, original '
        'paper/example counts and further qualifications are in each linked model page.',
        '## Token-count legend',
        '- **Online-paper tokens:** paper/abstract text acquired directly from publication repositories '
        'or publishers, including their PDF, XML, LaTeX or bibliographic-text exports.\n'
        '- **Web-URL tokens:** non-paper website content collected directly from live pages or raw web archives.\n'
        '- **Existing-dataset tokens:** imported, already assembled corpora or datasets, including '
        'literature/web corpora and biological databases. For example, paper text imported through '
        'S2ORC or The Pile is counted here, not again under online papers. The route is assessed at '
        'the reviewed study\'s acquisition/curation stage; releasing a new corpus does not itself make '
        'all of its inputs existing-dataset tokens.\n'
        '- **NR:** the category-specific token count is not disclosed or cannot be established from '
        'the inspected evidence; it is **not zero**. A known source without a separable token budget '
        'still receives NR.\n'
        '- **0:** the described stage has no separate acquisition through that route. For example, '
        'an exclusively reused paper dataset has zero direct-paper tokens, even though its content is literature.\n'
        '- **K / M / B / T:** thousand / million / billion / trillion tokens. **≈** denotes an '
        'approximate reported amount; **> / ≥** denotes a lower bound, not a complete category total.\n'
        '- **Corpus** counts retained data; **training exposure** counts sampled tokens and may '
        'include repeated passes. Planned schedules are labeled **scheduled token positions**, '
        'not measured training exposure. **Text + image** totals remain labeled; image pairs, '
        'words, bytes and documents are never converted into token counts.\n'
        '- A total can include unallocated, generated, code, book or private-source tokens. Missing '
        'category counts are not filled by subtracting known columns from the total. Counts '
        'from different rows/stages/models must not be added. Source-specific tokenizers and rounding remain unchanged.',
    ]
    for title, values in groups:
        intro.append('## ' + title)
        if title.startswith('Medical context'):
            intro.append('Retained as historical references. Clinical-note acquisition is outside this project’s biological research scope.')
        if title.startswith('Method context'):
            intro.append('General recipes are identified separately; their whole PDF/token pools are not treated as biological-literature budgets.')
        lines = [TOKEN_HEADER, TOKEN_SEPARATOR]
        for _, e in values:
            lines.extend(token_row(e, budget) for budget in e['token_budgets'])
        intro.append('\n'.join(lines))
    intro.extend([
        '## Acquisition and representation guides',
        '- [Biological source planning and provenance](source_planning.md)\n'
        '- [Web acquisition and reusable web corpora](web_acquisition.md)\n'
        '- [Executed eight-record web-corpus probe](web_sample.md)\n'
        '- [Original figures, captions and context](figure_handling.md)\n'
        '- [Citation provenance and the historical three-paper audit](citations_and_cpt_sources.md)\n'
        '- [Current three-paper extraction outputs](../pmc_native_v4_citations_2026-10-15/README.md)\n'
        '- [Paused 500-paper acquisition batch](../pmc_native_500_2026-10-15/README.md)',
        '## Maintenance',
        'Update the existing entry in [review.json](review.json), then run '
        '` .venv/bin/python scripts/render_foundation_catalog.py ` from the project root. '
        'The Markdown pages and CSV are generated views of that one registry. '
        'Add source versions and disclosure gaps to the same entry instead of creating another “coverage update” table. '
        'Evaluation protocols and raw runs retain their original project provenance and link here for literature notes.',
    ])
    (directory / 'README.md').write_text('\n\n'.join(intro) + '\n')
    stream = io.StringIO()
    fields = ['id', 'budget_id', 'name', 'kind', 'scope', 'stage', 'count_basis', 'token_kind']
    for key in TOKEN_FIELDS:
        fields.extend([key + '_tokens', key + '_relation', key + '_status'])
    fields.extend(['details', 'primary_sources', 'qualification'])
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader()
    for kind, e in all_entries:
        for budget in e['token_budgets']:
            row = {'id':e['id'], 'budget_id':budget['id'], 'name':e['name'], 'kind':kind,
                'scope':e.get('scope_group',e.get('category','')), 'stage':budget['stage'],
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
