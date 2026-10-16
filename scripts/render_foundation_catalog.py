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
                 'budget_breakdown': 'Token budget breakdown',
                 'figures': 'Figure handling', 'citations': 'Citation handling'}
TOKEN_FIELDS = ('online_papers', 'web_urls', 'existing_datasets', 'total')
TOKEN_HEADER = '| Model / stage | What is counted | Online-paper tokens | Web-URL tokens | Existing-dataset tokens | Total tokens | Source |'
TOKEN_SEPARATOR = '|---|---|---:|---:|---:|---:|---|'
TOKEN_RELATIONS = {'exact': '', 'approximate': '≈', 'greater_than': '>', 'at_least': '≥'}
QUALITY_LABELS = {'strong': 'Strong', 'solid': 'Solid', 'mixed': 'Mixed', 'weak': 'Weak'}
QUALITY_ORDER = {rating: rank for rank, rating in enumerate(QUALITY_LABELS)}
QUALITY_DIMENSIONS = {'contribution': 'Contribution and originality',
                      'technical_soundness': 'Technical soundness', 'evaluation': 'Evaluation',
                      'reproducibility': 'Reproducibility', 'clarity': 'Clarity and limitations'}


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


def overview_amount(amount, *, total=False):
    if amount['status'] == 'not_reported':
        return 'Not reported' if total else '—'
    return token_amount(amount)


def modality_amount(item):
    if item['tokens'] is None:
        return 'NR'
    return token_amount(dict(status='reported', tokens=item['tokens'],
                             relation=item.get('relation', 'exact')))


def modality_groups(profile):
    """Resolve display groups from their source items without copying token counts."""
    by_name = {item['name']: item for item in profile['items']}
    groups = profile.get('overview_groups') or [
        {'label': item.get('short_label', item['name']), 'members': [item['name']]}
        for item in profile['items']]
    return [(group, [by_name[name] for name in group['members']]) for group in groups]


def modality_group_amount(items):
    if len(items) == 1:
        return modality_amount(items[0])
    relation = 'approximate' if any(i.get('relation') == 'approximate' for i in items) else 'exact'
    return token_amount(dict(status='reported', tokens=sum(i['tokens'] for i in items), relation=relation))


def modality_overview(entry):
    profile = entry['modality_profile']
    if not profile['items']:
        return 'Text only'
    if all(item['measurement'] == 'presence' for item in profile['items']):
        encoders = '; '.join(item.get('short_label', item['name']).removeprefix('Later ')
                             for item in profile['items'])
        return cell('Text-only CPT; ' + encoders + ' used later')
    lines = []
    for group, items in modality_groups(profile):
        amount = modality_group_amount(items)
        label = f"{group['label']}: {'not reported' if amount == 'NR' else amount}"
        if group.get('show_parts'):
            parts = '; '.join(f"{item.get('short_label', item['name'])} {modality_amount(item)}"
                              for item in items)
            label += ' (' + parts + ')'
        lines.append(cell(label))
    if profile.get('overview_note'):
        note = profile['overview_note'].removesuffix('; image share NR.')
        lines.append(cell(re.sub(r'\bNR\b', 'not reported', note)))
    return '<br>'.join(lines)


def composition_summary(entry, *, include_sources=True):
    composition = entry['corpus_composition']
    terms = ' + '.join(f"{modality_amount(item)} {item['label'].lower()}" for item in composition['components'])
    total = token_amount(overview_budget(entry)['counts']['total'])
    refs = (' · '.join(f"[{source['label']}]({source['url']})" for source in composition['sources'])
            if include_sources else '')
    return f"**{entry['name']}’s full corpus adds up: {terms} = {total}.** {refs}".rstrip()


def model_description(entry, value):
    """State initialization once in the from-scratch section, preserving raw records."""
    if entry['presentation']['section'] == 'from_scratch':
        return re.sub(r'^Random weights;\s*', '', value)
    return value


def overview_row(entry):
    """One explicitly selected budget per study; never mix corpus and exposure."""
    budget = overview_budget(entry)
    view = entry['presentation']
    name = cell(view.get('name', entry['name']))
    name += f" ({entry['publication']['year']})"
    name += '<br>' + cell(model_description(entry, view['starting_model']))
    amounts = [overview_amount(budget['counts'][key], total=key == 'total') for key in TOKEN_FIELDS]
    origins = entry['paper_text_origins']
    names = origins['direct']
    if names:
        origin_text = '; '.join(names[:3])
        if len(names) > 3:
            origin_text += f" (+{len(names) - 3})"
    elif origins['reused']:
        origin_text = 'via ' + '; '.join(origins['reused'][:2]) + ' (reused)'
    else:
        origin_text = origins['unspecified']
    amounts[0] += '<br>' + cell(origin_text)
    datasets = entry['dataset_sources']['names']
    if datasets:
        preview = '<br>'.join(datasets[:3])
        if len(datasets) > 3:
            preview += f" (+{len(datasets) - 3})"
        amounts[2] += '<br>' + cell(preview)
    if entry.get('corpus_composition'):
        counts = budget['counts']
        remainder = counts['total']['tokens'] - sum(counts[key].get('tokens') or 0 for key in TOKEN_FIELDS[:-1])
        remainder_label = modality_amount({'tokens': remainder})
        amounts[3] += f"<br>{remainder_label} source split unknown"
    credits = entry['author_institutions']
    authors = cell(credits['authors_short']) + '<br>' + cell(credits['institutions_short'])
    review = entry['paper_quality']
    assessment = f"**{QUALITY_LABELS[review['overall']]}**<br>{cell(review['headline'])}"
    modalities = modality_overview(entry)
    refs = f"[Paper]({budget['sources'][0]['url']})<br>[Notes](papers/{entry['id']}.md)"
    # The overview omits direct-web counts; detailed pages and exports retain them.
    return '| ' + ' | '.join([name, amounts[0], amounts[2], modalities, amounts[3],
                             assessment, authors, refs]) + ' |'


def overview_table(entries, *, from_scratch=False):
    model_label = 'architecture' if from_scratch else 'starting checkpoint'
    return '\n'.join([
        f'| Model /<br>{model_label} | Paper tokens /<br>origin | Dataset tokens /<br>sources | Other modalities /<br>tokens | Total<br>tokens | Paper<br>assessment | Authors /<br>institutions | Source |',
        '|:---|:---|:---|:---|:---|:---|:---|:---|',
        *(overview_row(entry) for entry in entries),
    ])


def clean(value):
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', value).replace('**', '').replace('`', '')


def cell(value):
    return value.replace('|', '\\|').replace('\n', '<br>')


def starter_conclusion(estimate):
    """Present the calculable subtotal without implying that unresolved sources are zero."""
    summary = estimate['aggregation']
    components = {row['group']: row for row in summary['components']}
    billions = lambda value: f'{value / 1e9:.1f}B'
    low, high = summary['quantified_candidate_subtotal_low'], summary['quantified_candidate_subtotal_high']
    rows = [
        '| Source category | Quantified candidate tokens |', '|:---|---:|',
        f"| Paper text | {billions(components['papers']['low'])}–{billions(components['papers']['high'])} |",
        f"| Biology web text | {billions(components['web']['low'])} |",
        f"| Biological database records | {billions(components['records']['low'])} |",
        f"| **Quantified subtotal** | **{billions(low)}–{billions(high)}** |",
        '| Additional unique contributions from other sources | Not yet quantified |',
    ]
    return '\n\n'.join([
        '## Available training data',
        f"**Currently quantified: approximately {low / 1e9:.0f}–{high / 1e9:.0f}B candidate text/record tokens.** "
        '**The complete biological-corpus total is not yet established.** The table gives the supported subtotal; '
        'unmeasured contributions from other sources remain additional.',
        '\n'.join(rows),
        'These are approximate amounts in a common tokenizer, before biological scope filtering and '
        'cross-source deduplication. The paper estimate includes candidate material that may be excluded. '
        'Published training budgets cannot be added together because the studies reuse sources.',
        f"**Raw sequences and structures are tracked separately, at secondary priority.** "
        f"The genomic pool alone contains {summary['raw_sequence_nucleotide_positions'] / 1e12:.1f}T reported nucleotide positions. "
        'Nucleotides, protein residues and structural records are not added to the text-token subtotal.',
        f"The [complete source inventory](source_inventory.md) consolidates **{summary['family_count']} source families**, "
        'including the datasets underlying released collections, with their source papers and overlap qualifications. '
        '[Counting assumptions](source_planning.md).',
    ])


def render_source_inventory(data, estimate, directory):
    summary = estimate['aggregation']
    names = {e['id']: e['name'] for kind in GROUPS for e in data.get(kind, [])}
    components = {row['id']: row for row in summary['components']}
    groups = [('papers', 'Paper sources'), ('web', 'Web sources'),
              ('records', 'Biological database and task records'),
              ('raw', 'Raw sequences and structures'), ('general', 'General replay and other sciences')]
    body = ['# Complete source inventory', '[Biological pretraining review](README.md)',
            f"This register consolidates {summary['family_count']} source families named in the biological review "
            'and the documented inputs of TheBioCollection and OpenGenome2. Aliases and overlapping releases '
            'are grouped. It is a complete register of the named inputs in scope, not a claim that all their '
            'token amounts or unique contributions have been measured.',
            '**— means the additional token contribution is unmeasured, not zero.** '
            'The overview subtotal counts only the three components with a common-tokenizer estimate. '
            'A source appearing inside TheBioCollection is not evidence that the whole external database '
            'has been included or that importing it separately would add nothing.']
    for group, title in groups:
        body.append('## ' + title)
        lines = ['| Source family | Counted amount / role | Referencing studies or collection | Source |',
                 '|:---|:---|:---|:---|']
        for row in sorted((r for r in summary['families'] if r['group'] == group), key=lambda r:r['name'].casefold()):
            if row['id'] in components:
                component = components[row['id']]
                amount = f"{component['low']/1e9:.1f}B"
                if component['low'] != component['high']:
                    amount += f"–{component['high']/1e9:.1f}B"
            elif row['id'] == 'opengenome2':
                amount = '8.8T nucleotide positions; separate from text subtotal'
            elif row['id'] == 'olmo_pdfs':
                amount = '972B across all subjects; biology-only amount —'
            elif 'biocollection' in row['upstream_of']:
                amount = 'Represented in TheBioCollection; additional coverage —'
            elif 'opengenome2' in row['upstream_of']:
                amount = 'Represented in OpenGenome2; additional coverage —'
            else:
                amount = '—'
            use = [names.get(eid, 'Evo 2' if eid == 'evo2_reference' else eid) for eid in row['used_by']]
            use.extend('Input to ' + {'biocollection':'TheBioCollection', 'opengenome2':'OpenGenome2'}[parent]
                       for parent in row['upstream_of'])
            evidence = sorted(row['evidence'], key=lambda url: ('huggingface.co' not in url, url))[:2]
            sources = ' · '.join(f"[{'Repository' if 'github.com' in url else 'Paper' if 'arxiv.org' in url or 'mlr.press' in url else 'Source'}]({url})"
                                 for url in evidence)
            lines.append('| ' + ' | '.join([cell(row['name']), cell(amount + '. ' + row['treatment']),
                                            cell('; '.join(use)), sources]) + ' |')
        body.append('\n'.join(lines))
    if summary['unresolved_study_source_details']:
        body.append('## Remaining source-identification gaps')
        body.append(', '.join(names[eid] for eid in summary['unresolved_study_source_details']))
    body.append('[Aggregate calculation and definitions](source_planning.md).')
    (directory / 'source_inventory.md').write_text('\n\n'.join(body) + '\n')


def render(data, directory=REPORT, *, starter_estimate=None):
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
            publication = entry.get('publication', {})
            if (type(publication.get('year')) is not int or not 1900 <= publication['year'] <= 2100
                    or not publication.get('basis') or not publication.get('source', '').startswith('https://')):
                raise ValueError('Missing publication year or provenance: ' + entry['id'])
            if not view.get('starting_model') or not view.get('count_label') or not view.get('initialization_source'):
                raise ValueError('Missing pretraining classification evidence: ' + entry['id'])
            if view.get('budget_id') not in {b['id'] for b in entry['token_budgets']}:
                raise ValueError('Unknown overview budget: ' + entry['id'])
            if not view.get('data_scope') or view.get('quantity_type') not in {'dataset', 'training', 'positions', 'unknown'}:
                raise ValueError('Missing content scope or quantity type: ' + entry['id'])
            credits = entry.get('author_institutions', {})
            datasets = entry.get('dataset_sources', {})
            review = entry.get('paper_quality', {})
            if not all(credits.get(k) for k in ('authors_short', 'institutions_short', 'authors', 'institutions', 'source')):
                raise ValueError('Missing paper attribution: ' + entry['id'])
            if 'names' not in datasets or not datasets.get('source'):
                raise ValueError('Missing dataset-name provenance: ' + entry['id'])
            if (review.get('overall') not in QUALITY_LABELS or not review.get('headline')
                    or not review.get('summary') or not review.get('sources')
                    or any(not source.get('url', '').startswith('https://') for source in review.get('sources', []))
                    or set(review.get('dimensions', {})) != set(QUALITY_DIMENSIONS)
                    or not all(review['dimensions'].values())):
                raise ValueError('Missing overall-paper assessment: ' + entry['id'])
            origins = entry.get('paper_text_origins', {})
            modalities = entry.get('modality_profile', {})
            if (not all(k in origins for k in ('direct', 'reused', 'unspecified', 'note', 'source'))
                    or not isinstance(origins.get('direct'), list) or not isinstance(origins.get('reused'), list)
                    or not origins.get('note') or not origins.get('source', '').startswith('https://')):
                raise ValueError('Missing paper-origin provenance: ' + entry['id'])
            if (not modalities.get('summary') or not modalities.get('note') or not modalities.get('sources')
                    or not isinstance(modalities.get('items'), list)
                    or any(not source.get('url', '').startswith('https://') for source in modalities.get('sources', []))):
                raise ValueError('Missing modality provenance: ' + entry['id'])
            for item in modalities.get('items', []):
                if not item.get('name') or not item.get('note') or item.get('measurement') not in {'modality', 'domain_bucket', 'presence'}:
                    raise ValueError('Missing modality count definition: ' + entry['id'])
                value = item.get('tokens')
                if value is not None and (type(value) is not int or value < 0):
                    raise ValueError('Invalid modality token amount: ' + entry['id'])
                if item.get('relation', 'exact') not in TOKEN_RELATIONS:
                    raise ValueError('Unknown modality token relation: ' + entry['id'])
                if value is not None and item['measurement'] == 'presence':
                    raise ValueError('Modality presence alone cannot establish token counts: ' + entry['id'])
            names = [item['name'] for item in modalities['items']]
            if len(set(names)) != len(names):
                raise ValueError('Duplicate modality item: ' + entry['id'])
            seen = set()
            for group in modalities.get('overview_groups', []):
                members = group.get('members', [])
                if (not group.get('label') or not members or any(name not in names for name in members)
                        or len(set(members)) != len(members) or seen.intersection(members)):
                    raise ValueError('Overlapping or unknown modality display group: ' + entry['id'])
                seen.update(members)
            for _, members in modality_groups(modalities):
                if len(members) > 1 and any(item['tokens'] is None or item.get('relation', 'exact') not in
                                            {'exact', 'approximate'} for item in members):
                    raise ValueError('Cannot sum unknown or bounded modality counts: ' + entry['id'])
            if entry.get('corpus_composition'):
                composition = entry['corpus_composition']
                if (composition.get('budget_id') != view['budget_id'] or not composition.get('components')
                        or not composition.get('note') or not composition.get('sources')
                        or any(not source.get('url', '').startswith('https://') for source in composition.get('sources', []))):
                    raise ValueError('Missing corpus composition provenance: ' + entry['id'])
                for component in composition['components']:
                    if not component.get('label') or not component.get('note') or type(component.get('tokens')) is not int or component['tokens'] < 0:
                        raise ValueError('Invalid corpus composition amount: ' + entry['id'])
                total = overview_budget(entry)['counts']['total']
                if total['status'] == 'not_reported' or sum(c['tokens'] for c in composition['components']) != total['tokens']:
                    raise ValueError('Corpus composition does not reconcile with the total: ' + entry['id'])
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
            publication = entry['publication']
            body.append((f"**Paper year:** {publication['year']}. {publication['basis']} "
                         f"[Publication date]({publication['source']}). " + publication.get('note', '')).rstrip())
            training = 'Continued pretraining' if view['section'] == 'cpt' else 'Pretraining from scratch'
            model_label = 'Architecture' if view['section'] == 'from_scratch' else 'Starting checkpoint'
            body.append(f"**Training approach:** {training}. **{model_label}:** {model_description(entry, view['starting_model'])}. "
                        f"[Initialization evidence]({view['initialization_source']})")
            if view.get('note'):
                body.append(view['note'])
            body.append(f"**Data included in the overview amounts:** {view['data_scope']}. "
                        + view['biology_scope_note'])
            credits = entry['author_institutions']
            body.append('## Authors and institutions')
            body.append('**Authors:** ' + '; '.join(credits['authors']) + '.\n\n'
                        '**Institutions:** ' + '; '.join(credits['institutions']) + '.\n\n'
                        f"[Paper attribution]({credits['source']}). Names and affiliations follow the reviewed paper version.")
            review = entry['paper_quality']
            body.append('<a id="evidence-assessment"></a>\n\n## Overall paper assessment')
            body.append(f"**Overall: {QUALITY_LABELS[review['overall']]}.** {review['summary']} "
                        'This is our provisional technical judgment of the whole paper in its publication context, '
                        'not an official review score or an independent replication.')
            body.append('\n\n'.join(f"**{title}:** {review['dimensions'][key]}"
                                      for key, title in QUALITY_DIMENSIONS.items()))
            body.append('Sources: ' + ' · '.join(f"[{s['label']}]({s['url']})" for s in review['sources']))
            origins = entry['paper_text_origins']
            body.append('## Paper-text origins')
            body.append('**Direct paper sources:** ' + ('; '.join(origins['direct']) or 'No direct source established for this row')
                        + '.\n\n**Paper text via reused datasets:** ' + ('; '.join(origins['reused']) or 'No reused paper-text source established for this row')
                        + '.\n\n' + origins['note'] + f" [Source]({origins['source']})")
            if entry.get('corpus_composition'):
                composition = entry['corpus_composition']
                body.append('## Full corpus composition')
                body.append(composition_summary(entry))
                lines = ['| Corpus component | Tokens | What it includes |', '|---|---:|---|']
                lines.extend(f"| {cell(item['label'])} | {modality_amount(item)} | {cell(item['note'])} |"
                             for item in composition['components'])
                lines.append(f"| **Total** | **{token_amount(overview_budget(entry)['counts']['total'])}** | Sum of the four components above. |")
                body.append('\n'.join(lines))
                body.append(composition['note'])
                counts = overview_budget(entry)['counts']
                remainder = counts['total']['tokens'] - sum(counts[key].get('tokens') or 0 for key in TOKEN_FIELDS[:-1])
                body.append(f"The acquisition-route table assigns **{token_amount(counts['existing_datasets'])}** to existing datasets. "
                            f"The **{modality_amount({'tokens': remainder})}** remaining in mixed-source buckets has no disclosed "
                            'paper/web/dataset split. This is an allocation gap, not missing corpus content. '
                            'Adding modality counts to the existing-dataset column would count the same data twice.')
                body.append('Sources: ' + ' · '.join(f"[{s['label']}]({s['url']})" for s in composition['sources']))
            profile = entry['modality_profile']
            body.append('## Other modalities')
            body.append(profile['note'])
            if profile['items']:
                lines = ['| Representation / domain | Reported tokens | Count definition |', '|---|---:|---|']
                for item in profile['items']:
                    amount = modality_amount(item)
                    lines.append(f"| {cell(item['name'])} | {amount} | {cell(item['note'])} |")
                body.append('\n'.join(lines))
            body.append('Sources: ' + ' · '.join(f"[{s['label']}]({s['url']})" for s in profile['sources']))
            datasets = entry['dataset_sources']
            body.append('## Existing-dataset sources')
            body.append(('; '.join(datasets['names']) + '.' if datasets['names'] else 'No separately reused dataset identified for this overview row.')
                        + '\n\n' + datasets['note'] + f" [Source]({datasets['source']})")
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
                value = model_description(entry, entry[key]) if key == 'base' else entry[key]
                body.append(f"**{label}:** {value}")
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
        entries = [e for _, e in all_entries if e['presentation']['section'] == section]
        if section in {'cpt', 'from_scratch'}:
            return sorted(entries, key=lambda e: (QUALITY_ORDER[e['paper_quality']['overall']], e['name'].casefold()))
        return sorted(entries, key=lambda e: e['presentation'].get('order', 100))

    intro = [
        '# Biological continued pretraining: data sources and token budgets',
        'The comparison below focuses on **continued pretraining (CPT)**: '
        'starting with a pretrained model and training it further on domain data. '
        'Data-curation studies and released models appear together because both inform this choice.',
        'Counts follow each paper’s reported budget and may include general text, other sciences and '
        'biological sequences. The **Source** column links to the paper and detailed notes.',
        '[Processing recipe](data_pipeline.md).',
        '## Continued pretraining',
        'Both tables are sorted **Strong → Solid → Mixed → Weak**, alphabetically within each rating. '
        'Years indicate the first public paper or preprint; notes may review a later version.',
        overview_table(selected('cpt')),
        '**Quality** considers contribution, technical soundness, evaluation, reproducibility and clarity. '
        'Strong = convincing contribution; Solid = worthwhile with limits; Mixed = substantial strengths '
        'and weaknesses; Weak = fundamental problems. These are provisional judgments explained in the notes.',
        '### Reading the counts',
        '- **Sources:** paper tokens come from publication repositories; dataset tokens come from imported corpora or databases. '
        'Paper text imported through S2ORC or The Pile belongs in existing datasets.\n'
        '- **—** means an amount is unavailable or cannot be separated; **0** means no data through that '
        'route. Named sources can still have an unknown token count.\n'
        '- **M / B** mean million / billion; **≈** means approximate; **> / ≥** indicate a lower bound. '
        'Full dataset lists, counting methods and qualifications are in **Notes**.',
        '**Other modalities** are already included in the acquisition columns. **1D** means sequences; '
        '**3D** means structures. Domain and record totals can include annotations and text. '
        'Later-stage encoder inputs are identified separately.',
        '\n\n'.join(composition_summary(e, include_sources=False) for _, e in all_entries if e.get('corpus_composition')),
        'Of BioMatrix’s total, **176.7B** is identified as existing-dataset input. The other **127.7B** '
        '(79.7B scientific text + 48B cross-entity data) has no disclosed paper/web/dataset split. '
        'Those tokens are accounted for in the full composition; adding the modality column to '
        'the source columns would count them twice.',
        '## Pretraining from scratch: comparison',
        'These models begin with randomly initialized weights and biological or scientific data, '
        'rather than adapting an existing checkpoint. They provide a comparison with CPT.',
        overview_table(selected('from_scratch'), from_scratch=True),
        *([starter_conclusion(starter_estimate)] if starter_estimate is not None else []),
    ]
    (directory / 'README.md').write_text('\n\n'.join(intro) + '\n')
    if starter_estimate is not None:
        render_source_inventory(data, starter_estimate, directory)

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
                   'The source-inventory summary is separate from author-reported budgets. Its figures come from '
                   '`starter_corpus_estimate.json`; reproduce those with `scripts/estimate_starter_budget.py` '
                   'before rerendering. Keep current inventory amounts separate from the superseded '
                   'subset scenarios; the old 15% web retention assumption is not the current estimate. '
                   'Document scope, collection priorities and storage scaling in `source_planning.md`.',
                   'The complete source register is generated in `source_inventory.md` from '
                   '`scripts/source_inventory.py` and the named inputs in the review. Add mappings '
                   'for new sources; the estimator rejects unmapped labels. Keep unresolved token '
                   'amounts explicit and do not call the quantified subtotal a complete corpus total.',
                   'The `presentation` record selects the review section, starting checkpoint and one '
                   'overview budget, with explicit content scope and quantity type. It must cite '
                   'initialization evidence. Keep every original budget '
                   'in `token_budgets`; selecting an overview row never changes a reported amount. '
                   'CPT studies belong with CPT models regardless of publication type. '
                   'Do not classify instruction tuning, contrastive learning or random initialization as CPT.',
                   'The `publication` record stores the first public paper/preprint year and its source. '
                   'Show that year beside the model name; keep checkpoint-release dates and later '
                   'journal versions distinct in the detailed notes.',
                   'Overview entries also require `author_institutions`, `dataset_sources`, '
                   '`paper_text_origins`, `modality_profile` and `paper_quality`. Preserve attribution '
                   'sources and named inputs. Overall quality reviews cover contribution, soundness, '
                   'evaluation, reproducibility and clarity, with primary-source links. Keep historical '
                   '`evidence_assessment` records as provenance. Do not add modality totals to acquisition totals. '
                   'The overview shows numeric modality counts and sorts by overall quality, with alphabetical '
                   'ties. Optional modality display groups sum only disjoint, known component amounts; '
                   'corpus composition records must reconcile with the selected total. '
                   'Keep overview links in the Source column (one Paper link and one Notes link). '
                   'Direct-web counts remain in the registry, numeric export and detailed pages; omit that '
                   'sparse column from the overview. Use short wrapped headers, left-aligned text and one '
                   'dataset name per line so GitHub can size columns to their content. '
                   'Use a dash for unavailable category amounts and plain language for an unknown total. '
                   'Keep detailed counting definitions on study pages, without dagger markers in the overview. '
                   'Keep the processing recipe, concrete actions and supporting papers in '
                   '`data_pipeline.md`; the catalog overview links to that page. '
                   'A venue or institution name is not an overall-quality measurement. '
                   'Record numerical allocation corrections explicitly in the token audit.',
                   'The [token audit](token_budget_verification.json) records numerical checks and '
                   'source snapshots. [Archived references](archive.md) preserve earlier out-of-scope material.',
                   'Evaluation protocols, benchmark cases and runs live in the separate private '
                   '[bio-evaluation repository](https://github.com/Some-random/bio-evaluation). '
                   'This repository holds extraction work and public literature notes. '
                   'Private evaluation links remain in the registry as provenance, not public review navigation.']
    (directory / 'maintenance.md').write_text('\n\n'.join(maintenance) + '\n')
    stream = io.StringIO()
    fields = ['id', 'budget_id', 'name', 'kind', 'scope', 'review_section', 'overview_selected',
              'paper_year', 'paper_year_basis', 'paper_year_source',
              'starting_model', 'data_scope', 'quantity_type', 'authors', 'institutions',
              'existing_dataset_names', 'direct_paper_sources', 'reused_paper_sources', 'other_modalities',
              'overall_paper_quality', 'overall_review_summary',
              'stage', 'count_basis', 'token_kind']
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
                'paper_year': e.get('publication', {}).get('year', ''),
                'paper_year_basis': e.get('publication', {}).get('basis', ''),
                'paper_year_source': e.get('publication', {}).get('source', ''),
                'overview_selected':budget['id'] == e['presentation'].get('budget_id'),
                'starting_model':e['presentation'].get('starting_model', ''),
                'data_scope':e['presentation'].get('data_scope', ''),
                'quantity_type':e['presentation'].get('quantity_type', ''),
                'authors':'; '.join(e.get('author_institutions', {}).get('authors', [])),
                'institutions':'; '.join(e.get('author_institutions', {}).get('institutions', [])),
                'existing_dataset_names':'; '.join(e.get('dataset_sources', {}).get('names', [])),
                'direct_paper_sources':'; '.join(e.get('paper_text_origins', {}).get('direct', [])),
                'reused_paper_sources':'; '.join(e.get('paper_text_origins', {}).get('reused', [])),
                'other_modalities':e.get('modality_profile', {}).get('summary', ''),
                'overall_paper_quality':e.get('paper_quality', {}).get('overall', ''),
                'overall_review_summary':e.get('paper_quality', {}).get('summary', ''),
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
    data = json.loads((REPORT / 'review.json').read_text())
    estimate = json.loads((REPORT / 'starter_corpus_estimate.json').read_text())
    print(f'Rendered {render(data, starter_estimate=estimate)} unique catalog entries')
