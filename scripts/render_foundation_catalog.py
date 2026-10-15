#!/usr/bin/env python3
"""Render the one shared literature registry into GitHub Markdown and CSV."""
import csv
import io
import json
import re
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


def clean(value):
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', value).replace('**', '').replace('`', '')


def cell(value):
    return value.replace('|', '\\|').replace('\n', '<br>')


def summarize(entry):
    value = clean(entry.get('corpus') or entry.get('document_route') or 'See source notes; source budget not separately established.')
    return value if len(value) <= 230 else value[:227].rsplit(' ', 1)[0] + '…'


def render(data, directory=REPORT):
    all_entries = [(kind, e) for kind in GROUPS for e in data.get(kind, [])]
    ids = [e['id'] for _, e in all_entries]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate catalog IDs')
    pages = directory / 'papers'
    pages.mkdir(exist_ok=True)
    for kind, entry in all_entries:
        eid = entry['id']
        if not re.fullmatch(r'[a-z0-9_]+', eid) or not entry.get('sources'):
            raise ValueError('Invalid ID or missing source: ' + eid)
        body = [f"# {entry['name']}", '[Shared literature catalog](../README.md)',
                entry.get('category', ''),
                'This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.']
        if entry.get('scope_group') == 'Medical context retained from earlier review':
            body.append('Historical medical context. Clinical-note acquisition is outside the biological research corpus scope.')
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
        'Reported corpus size, training exposure, words, examples and image tokens retain their '
        'original units. **NR means not separately reported, not zero.** Source discrepancies and '
        'paper versions remain explicit. This consolidation reuses existing evidence; it is not '
        'a fresh search or a model benchmark.',
    ]
    for title, values in groups:
        intro.append('## ' + title)
        if title.startswith('Medical context'):
            intro.append('Retained as historical references. Clinical-note acquisition is outside this project’s biological research scope.')
        if title.startswith('Method context'):
            intro.append('General recipes are identified separately; their whole PDF/token pools are not treated as biological-literature budgets.')
        lines = ['| Model / study / corpus | Stage | Data summary |', '|---|---|---|']
        for _, e in values:
            lines.append(f"| [{cell(e['name'])}](papers/{e['id']}.md) | {cell(e.get('stage', 'See source'))} | {cell(summarize(e))} |")
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
    writer = csv.DictWriter(stream, fieldnames=['id', 'name', 'kind', 'scope', 'stage', 'data_summary', 'details', 'primary_sources'])
    writer.writeheader()
    for kind, e in all_entries:
        writer.writerow({'id':e['id'], 'name':e['name'], 'kind':kind,
            'scope':e.get('scope_group',e.get('category','')), 'stage':e.get('stage',''),
            'data_summary':clean(e.get('corpus',e.get('document_route','NR'))),
            'details':f"papers/{e['id']}.md", 'primary_sources':' ; '.join(s['url'] for s in e['sources'])})
    (directory / 'catalog.csv').write_text(stream.getvalue())
    return len(all_entries)


if __name__ == '__main__':
    print(f'Rendered {render(json.loads((REPORT / "review.json").read_text()))} unique catalog entries')
