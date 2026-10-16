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


def overview_row(entry):
    """One explicitly selected budget per study; never mix corpus and exposure."""
    budget = overview_budget(entry)
    view = entry['presentation']
    name = f"[{cell(view.get('name', entry['name']))}](papers/{entry['id']}.md)"
    name += '<br>' + cell(view['starting_model'])
    if view['quantity_type'] == 'training':
        name += '<br>**Training tokens†**'
    elif view['quantity_type'] == 'positions':
        name += '<br>**Token positions‡**'
    amounts = [token_amount(budget['counts'][key]) for key in TOKEN_FIELDS]
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
    amounts[0] += f"<br>[{cell(origin_text)}](papers/{entry['id']}.md#paper-text-origins)"
    datasets = entry['dataset_sources']['names']
    if datasets:
        preview = '; '.join(datasets[:3])
        if len(datasets) > 3:
            preview += f" (+{len(datasets) - 3})"
        amounts[2] += f"<br>[{cell(preview)}](papers/{entry['id']}.md#existing-dataset-sources)"
    credits = entry['author_institutions']
    authors = cell(credits['authors_short']) + '<br>' + cell(credits['institutions_short'])
    review = entry['paper_quality']
    assessment = f"[{QUALITY_LABELS[review['overall']]}](papers/{entry['id']}.md#overall-paper-assessment)<br>{cell(review['headline'])}"
    modalities = f"[{cell(entry['modality_profile']['summary'])}](papers/{entry['id']}.md#other-modalities)"
    refs = ' · '.join(f"[{cell(s['label'])}]({s['url']})" for s in budget['sources'])
    return '| ' + ' | '.join([name, authors] + amounts + [modalities, assessment, refs]) + ' |'


def overview_table(entries):
    return '\n'.join([
        '| Model / starting checkpoint | Authors / institutions | Online-paper tokens / origin | Web-URL tokens | Existing-dataset tokens | Total reported tokens | Other modalities | Overall paper assessment | Source |',
        '|---|---|---:|---:|---:|---:|---|---|---|',
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
            profile = entry['modality_profile']
            body.append('## Other modalities')
            body.append(profile['note'])
            if profile['items']:
                lines = ['| Representation / domain | Reported tokens | Count definition |', '|---|---:|---|']
                for item in profile['items']:
                    amount = 'NR' if item['tokens'] is None else token_amount(
                        dict(status='reported', tokens=item['tokens'], relation=item.get('relation', 'exact')))
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
        '**These are reported source budgets, not uniformly biology-only token counts.** '
        'Some include clinical literature, general text, other sciences or non-text modalities. '
        'The modality descriptions and linked source notes identify that scope. A paper’s full training total cannot be '
        'treated as a biology-only amount when that subset is not separately reported.',
        '## Continued pretraining',
        'Each row names the starting checkpoint and reports one clearly identified token budget. '
        'Unmarked rows show **dataset tokens before training repeats**. '
        '**† Training tokens** include repeated passes; **‡ token positions** can include padding or '
        'a planned schedule. The linked study pages retain the full counts and source qualifications.',
        overview_table(selected('cpt')),
        'The authors/institutions column gives compact credits; the study pages retain the fuller lists. '
        'Dataset names appear below their token count; a “+N” link opens the longer source list. '
        '**Overall paper assessment** considers the contribution and originality, technical soundness, '
        'evaluation, reproducibility, and clarity of the whole paper in its publication context. '
        '**Strong:** substantial contribution, convincingly executed. **Solid:** worthwhile work with '
        'meaningful limits. **Mixed:** substantial strengths alongside weaknesses that constrain the '
        'overall case. **Weak:** fundamental problems dominate. These are provisional editorial judgments, '
        'not official reviewer scores; institutional prestige and relevance to this project do not determine them.',
        '### Reading the counts',
        '- **Online papers:** text acquired directly from publishers or publication repositories, '
        'including abstracts, XML, PDF and LaTeX. The names below each amount identify the source; '
        '“via … (reused)” means the text belongs in the existing-dataset column instead.\n'
        '- **Web URLs:** non-paper webpages acquired directly, including raw web archives.\n'
        '- **Existing datasets:** reused corpora and biological databases. Paper text imported through '
        'S2ORC or The Pile belongs here; it is not counted twice. These columns describe **how the study '
        'obtained the data**, not just what the text discusses.\n'
        '- **0** means the described data has no separate acquisition through that route. **NR** means '
        'the token amount is not reported or cannot be established. Neither a known source name nor a '
        'paper count supplies a missing token count.\n'
        '- **Dataset size** counts the prepared corpus before training repeats. **Tokens used in training** '
        'counts consumption, including repeated passes: a 10B-token dataset read three times gives '
        '30B training tokens, not 30B of distinct data. The former measures data volume; the latter '
        'measures how much training read it. For BioMedLM these figures are 34.6B and 300B.\n'
        '- **M / B** mean million / billion; **≈** means approximate; **> / ≥** indicate a lower bound. '
        'Tokenizers differ. Sequence/image tokens and planned token positions are labeled explicitly. '
        'A total may include material without a disclosed category split.',
        '**Other modalities** describes data already included in the acquisition columns; it is not an '
        'additional source category. Protein/DNA/RNA sequences, molecular strings, structure tokens and '
        'figure images are distinguished on each study page, with counts where reported. A “protein data” '
        'budget can include annotations and structures as well as sequence tokens. Later SFT/encoder '
        'inputs are explicitly distinguished from the counted CPT stage.',
        '**Why a category can be smaller than the total:** BioMatrix’s existing-dataset lower bound is '
        '**176.7B = 25.6B general text + 77.4B protein data + 73.7B molecule data**. '
        'The other **127.7B** comprises 79.7B scientific text and 48.0B cross-entity/interleaved data; '
        'their exact paper/web/dataset split is not disclosed. These are identified but unallocated '
        'components, not missing training tokens. See [the source breakdown](papers/biomatrix.md#token-budget-breakdown). '
        'Elsewhere, “≥” likewise means a lower bound, and a dataset name without a token amount remains NR. '
        'BioMatrix’s 25.6B general-text slice is FineWeb-Edu; '
        'BioMamba’s existing-dataset component is general replay. NatureLM and SciReasoner also '
        'cover sciences beyond biology. None of those whole-row totals is a verified biology-only budget.',
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
        'The [data preparation pipeline](data_pipeline.md) brings paper, web and reused-dataset inputs '
        'into the same source-linked records, then applies content selection, deduplication and token counting. '
        'It distinguishes existing implementation from proposed web-processing work. '
        'See also the guides to [biological sources](source_planning.md), '
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
                   'overview budget, with explicit content scope and quantity type. It must cite '
                   'initialization evidence. Keep every original budget '
                   'in `token_budgets`; selecting an overview row never changes a reported amount. '
                   'CPT studies belong with CPT models regardless of publication type. '
                   'Do not classify instruction tuning, contrastive learning or random initialization as CPT.',
                   'Overview entries also require `author_institutions`, `dataset_sources`, '
                   '`paper_text_origins`, `modality_profile` and `paper_quality`. Preserve attribution '
                   'sources and named inputs. Overall quality reviews cover contribution, soundness, '
                   'evaluation, reproducibility and clarity, with primary-source links. Keep historical '
                   '`evidence_assessment` records as provenance. Do not add modality totals to acquisition totals. '
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
    print(f'Rendered {render(json.loads((REPORT / "review.json").read_text()))} unique catalog entries')
