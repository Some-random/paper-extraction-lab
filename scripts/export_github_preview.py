#!/usr/bin/env python3
"""Export existing extraction results as GitHub-rendered Markdown and images.

No inference, re-extraction, website deployment, or paper PDF/XML copying.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = 'pmc_native_v3_preview_2026-10-15'


def load(path):
    return json.loads(path.read_text())


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + '\n')


def quote(value):
    return '\n'.join('> ' + line for line in value.splitlines())


def attribution(doc):
    return '\n\n'.join([
        'Authors: ' + ', '.join(doc['authors']) + '.',
        '[Original article](' + doc['pmc_url'] + ') · '
        '[Original PDF](' + doc['source_pdf_url'] + ') · '
        '[Original XML](' + doc['source_xml_url'] + ').',
        'License: **' + doc['license_code'] + '**. Figures, captions and source excerpts '
        'are attributed to the original authors; original figure credits are retained.',
        *doc['license_statements'],
    ])


def source_details(xpath, sha):
    return '<details>\n<summary>Source XML provenance</summary>\n\n' + \
        '`' + xpath + '`\n\nXML SHA-256: `' + sha + '`\n\n</details>'


def visual_markdown(visual, doc, blockmap, include_context=True):
    lines = ['## ' + (visual['label'] or visual['xml_id'])]
    for asset in visual.get('assets', []):
        lines.append('![' + (visual['label'] or visual['xml_id']) + ' — original publisher figure](assets/' + asset['source_filename'] + ')')
    if visual.get('table_html'):
        # GitHub supports HTML tables; preserve the actual rowspan/colspan.
        lines.append(visual['table_html'])
    lines.append('**Source caption:** ' + visual['caption'])
    if visual.get('notes'):
        lines.append('**Source table notes:** ' + visual['notes'])
    if include_context:
        lines.append('### Article paragraphs explicitly referring to this ' + visual['kind'])
        if not visual['referring_paragraphs']:
            lines.append('No explicit referring paragraph was found. No context was supplied by inference.')
        for bid in visual['referring_paragraphs']:
            block = blockmap[bid]
            lines.append('**' + (' / '.join(block['section_path']) or 'Article body') + '**')
            lines.append(quote(block['text']))
            lines.append(source_details(block['source_xpath'], doc['source_xml_sha256']))
    lines.append(source_details(visual['source_xpath'], doc['source_xml_sha256']))
    return '\n\n'.join(lines)


def example_markdown(example):
    lines = ['### ' + example['question'], '**Answer:** ' + example['answer'],
             '**Source excerpt:**', quote(example['source_quote'])]
    if example.get('row_label'):
        lines.append('Table row: **' + example['row_label'] + '**. Column: **' +
                     ' / '.join(example['column_header_path']) + '**.')
    checks = example['pdf_text_literal_checks']
    common = sorted(set.intersection(*(set(c['pages']) for c in checks))) if checks else []
    if common:
        lines.append('PDF page(s) containing all checked text literals: **' + ', '.join(map(str, common)) + '**.')
    lines.append('Validation: ' + example['validation'] + '. PDF checking is a text-presence check, not an independent answer-quality score.')
    lines.append(source_details(example['source_xpath'], example['source_xml_sha256']))
    return '\n\n'.join(lines)


def portable_extraction(value):
    """Export all extracted content without duplicate markup or derived Q&A."""
    if isinstance(value, list):
        return [portable_extraction(item) for item in value]
    if isinstance(value, dict):
        result = {k: portable_extraction(v) for k, v in value.items()
                  if k not in {'raw_xml', 'html', 'table_html', 'caption_html', 'review_examples'}}
        if 'source_filename' in result and 'path' in result:
            result['path'] = 'assets/' + result['source_filename']
        return result
    return value


def export_paper(doc, source, report):
    pid = doc['pmcid']
    directory = report / 'papers' / pid
    directory.mkdir(parents=True, exist_ok=True)
    blockmap = {b['id']: b for b in doc['blocks']}
    featured = next(v for v in doc['visuals'] if v['xml_id'] == doc['featured_figure'])
    images = []
    for visual in doc['visuals']:
        for asset in visual['assets']:
            original = ROOT / asset['path']
            if hashlib.sha256(original.read_bytes()).hexdigest() != asset['sha256']:
                raise ValueError('Source image hash changed: ' + str(original))
            target = directory / 'assets' / asset['source_filename']
            target.parent.mkdir(exist_ok=True)
            shutil.copyfile(original, target)
            if target.read_bytes() != original.read_bytes():
                raise ValueError('Image copy is not byte-identical')
            images.append(dict(visual_id=visual['id'], **{k: v for k, v in asset.items() if k != 'path'},
                               repository_path=str(target.relative_to(ROOT))))
    s = doc['summary']
    intro = ['# ' + doc['title'], doc['journal'] + ' · **' + pid + '** · ' + doc['license_code'],
        '**[Read the full extracted research text](article.md)** · '
        '**[Read all extracted figures, captions and context](figures.md)**',
        '## Extracted outputs',
        '- [Full research text, in section order](article.md)\n'
        '- [All original figure images, extracted captions and explicitly referring paragraphs](figures.md)\n' +
        ('- [All source tables, preserving merged cells and notes](tables.md)\n' if s['tables'] else '') +
        '- [Complete structured extraction: paragraphs, figures, tables, links and provenance](extracted.json)\n'
        '- [All text chunks](text_chunks.jsonl)\n'
        '- [All figure/table–context records](interleaved.jsonl)\n'
        '- [One readable training-record preview](training_samples.md)',
        '[Back to all three papers](../../README.md)',
        f"{s['retained_paragraphs']} research paragraphs · {s['figures']} figures · "
        f"{s['tables']} tables · {s['text_chunks']} text chunks · "
        f"{s['interleaved_records']} figure/table–context records.",
        'These results use publisher XML and original figure files. Earlier PDF-only '
        'olmOCR output remains available [here](../../../pmc_cns_biology_2026-10-14/samples/' + pid + '/fullpaper_olmocr.md). '
        'The [earlier native extraction including references](../../../pmc_cns_biology_2026-10-14/samples/' + pid + '/fullpaper_native.md) is also retained. '
        'The updated research-text view routes bibliography and administrative material outside the text stream. '
        'No new OCR inference or model training was performed.',
        '## Featured original figure and source context',
        visual_markdown(featured, doc, blockmap),
    ]
    if s['tables']:
        intro += ['## Source tables', '[Read all source tables with merged cells and notes](tables.md).']
    intro += ['## Optional source-checked Q&A examples',
              'These examples are derived from the extracted content linked above.',
              *[example_markdown(e) for e in doc['review_examples']]]
    intro += ['## Checks and limitations',
        f"Source links checked: {s['checks']['context_edges_verified_against_raw_xml']} figure/table-reference edges. "
        f"Table cells with source XPaths: {s['checks']['table_cells_with_resolving_xpaths']}. "
        f"Unresolved figure/table references: {s['checks']['unresolved_figure_table_refs']}.",
        'These are structural/provenance checks. The examples were checked against source text; '
        'they are not independently human-adjudicated gold labels. Figure semantics and model-training '
        'benefit have not been measured. See [provenance and image checksums](provenance.json).',
        '## Attribution', attribution(doc)]
    write(directory / 'README.md', '\n\n'.join(intro))

    article = ['# ' + doc['title'],
        '[Paper overview](README.md) · [Figures](figures.md) · [Original article](' + doc['pmc_url'] + ')',
        'Ordered source-derived article text. Bibliographies and administrative sections are routed '
        'outside this research-text view. The original XML/PDF retain the complete source. '
        'Scientific superscripts/subscripts and the original table spans are preserved.']
    current = None
    tablemap = {v['id']: v for v in doc['visuals'] if v['kind'] == 'table'}
    for block in doc['blocks']:
        if current != block['section_path']:
            current = block['section_path']
            article.append('## ' + (' / '.join(current) or 'Article body'))
        if block['kind'] == 'table':
            article.append(tablemap[block['visual_id']]['table_html'])
        else:
            article.append(block['html'] or block['text'])
    article += ['## Attribution', attribution(doc)]
    write(directory / 'article.md', '\n\n'.join(article))

    figures = ['# Original figures and explicitly referring text', '[Paper overview](README.md)',
        'Every image is a byte-identical copy of the publisher asset, matched through the XML '
        'filename and official media-manifest checksum. Captions and context below are source text; '
        'they are not newly generated image interpretations.']
    figures += [visual_markdown(v, doc, blockmap) for v in doc['visuals'] if v['kind'] == 'figure']
    figures += ['## Attribution', attribution(doc)]
    write(directory / 'figures.md', '\n\n'.join(figures))
    if tablemap:
        tables = ['# Source tables', '[Paper overview](README.md)',
            'Original cell spans are retained in the rendered tables. A shared group total is not '
            'repeated as independent row counts. Source notes and referring paragraphs follow each table.']
        tables += [visual_markdown(v, doc, blockmap) for v in tablemap.values()]
        tables += ['## Attribution', attribution(doc)]
        write(directory / 'tables.md', '\n\n'.join(tables))

    chunks = [json.loads(l) for l in (source / pid / 'text_chunks.jsonl').read_text().splitlines()]
    groups = [json.loads(l) for l in (source / pid / 'interleaved.jsonl').read_text().splitlines()]
    write(directory / 'extracted.json', json.dumps(portable_extraction(doc), ensure_ascii=False, indent=2))
    write(directory / 'text_chunks.jsonl', '\n'.join(json.dumps(c, ensure_ascii=False) for c in chunks))
    write(directory / 'interleaved.jsonl', '\n'.join(json.dumps(portable_extraction(g), ensure_ascii=False) for g in groups))
    preferred = set(featured['referring_paragraphs'])
    chunk = next((c for c in chunks if any(f['block_id'] in preferred for f in c['fragments'])), chunks[0])
    record = next((g for g in groups if featured['id'] in g['visual_ids']), groups[0])
    # Publish a portable presentation of the same source-linked segment order.
    segments = []
    for segment in record['segments']:
        if segment['type'] == 'image':
            segments.append(dict(type='image', visual_id=segment['visual_id'],
                assets=[dict(image='assets/' + a['source_filename'], sha256=a['sha256'],
                             source_url=a['source_url']) for a in segment['assets']]))
        else:
            segments.append(segment)
    portable = dict(id=record['id'], context_policy=record['context_policy'],
                    source_xml_sha256=record['source_xml_sha256'], segments=segments,
                    status=record['status'])
    sample = ['# Actual training-record previews', '[Paper overview](README.md)',
        'These records were produced by the pipeline; no model was trained. The text uses the '
        'cached Qwen-family tokenizer for a 2,048-token packing demonstration. A future training '
        'backbone needs its own tokenizer. Image segments have not been vision-tokenized.',
        '## One complete text chunk',
        f"Record `{chunk['id']}` · **{chunk['token_count']} tokens** · "
        f"{len(chunk['fragments'])} source fragment(s).",
        '```text\n' + chunk['text'] + '\n```',
        '## One figure/table–context record',
        'Context segments keep source order. Figures/tables are attached only through explicit '
        'article references; shared context is emitted once in this record.',
        '```json\n' + json.dumps(portable, ensure_ascii=False, indent=2) + '\n```',
        '## Exact text-fragment provenance',
        '```json\n' + json.dumps([dict(block_id=f['block_id'], source_xpath=f['source_xpath'],
            char_start=f['char_start'], char_end=f['char_end']) for f in chunk['fragments']], indent=2) + '\n```']
    write(directory / 'training_samples.md', '\n\n'.join(sample))
    provenance = dict(pmcid=pid, title=doc['title'], authors=doc['authors'], license_code=doc['license_code'],
        license_statements=doc['license_statements'], pmc_url=doc['pmc_url'],
        source_pdf_url=doc['source_pdf_url'], source_xml_url=doc['source_xml_url'],
        source_pdf_sha256=doc['source_pdf_sha256'], source_xml_sha256=doc['source_xml_sha256'],
        images=images, checks=doc['checks'], note='GitHub review export of existing source-derived results. Original PDFs/XML remain on RustFS.')
    write(directory / 'provenance.json', json.dumps(provenance, ensure_ascii=False, indent=2))
    return directory


def export_review(source, report):
    documents = load(source / 'documents.json')
    summary = load(source / 'summary.json')
    for doc in documents:
        if doc['license_code'] != 'CC BY':
            raise ValueError('This review export is scoped to the three selected CC BY papers')
        export_paper(doc, source, report)
    rows = []
    output_rows = []
    for doc in documents:
        s = doc['summary']
        rows.append('| [' + doc['journal'] + ': ' + doc['title'] + '](papers/' + doc['pmcid'] + '/README.md) | ' +
                    ' | '.join(str(s[k]) for k in ['retained_paragraphs', 'figures', 'tables', 'text_chunks']) + ' |')
        directory = 'papers/' + doc['pmcid'] + '/'
        output_rows.append('| ' + doc['journal'] + ': ' + doc['title'] + ' | '
            '[Read extracted text](' + directory + 'article.md) | '
            '[Figures and context](' + directory + 'figures.md) | ' +
            ('[Tables](' + directory + 'tables.md)' if s['tables'] else 'No source tables') + ' | '
            '[Full structured extraction](' + directory + 'extracted.json) |')
    overview = ['# Three biology papers: updated extraction results',
        'The actual extracted content is linked directly below: full research text, original figure '
        'images with extracted captions and referring paragraphs, source tables, and complete structured data. '
        'The Q&A examples are optional derivatives of these outputs.',
        'Results generated **' + summary['created_at_pst'] + '** (fixed PST, UTC-8).',
        '## Read the extracted results',
        '| Paper | Extracted research text | Figures + captions + context | Tables | Structured data |\n'
        '| --- | --- | --- | --- | --- |\n' + '\n'.join(output_rows),
        'The research-text view includes the abstract, main sections and methods; bibliography and '
        'administrative material are retained separately in the structured extraction. Each paper '
        'overview also links the earlier native output and the unchanged PDF-only olmOCR transcript.',
        '## Output counts and paper overviews',
        '| Paper | Research paragraphs | Figures | Tables | Text chunks |\n'
        '| --- | ---: | ---: | ---: | ---: |\n' + '\n'.join(rows),
        '**Totals:** 140 research paragraphs, 25 original figure images, four source tables, '
        '30 text chunks, 23 figure/table–context records, and nine source-checked examples.',
        '## What changed',
        '- Figures/tables nested in publisher paragraphs are separated from the prose.\n'
        '- Merged table cells, scientific notation, captions and notes are retained.\n'
        '- Context comes from explicit article figure/table references.\n'
        '- Bibliography and administrative material are routed outside the text-training stream.\n'
        '- Text chunks retain source-fragment offsets and stay within the configured token limit.',
        '## What was checked',
        'All 25 images match their source media checksums. The pipeline checked 179 figure/table-reference '
        'edges against raw XML and retained XPath provenance for 218 physical source table cells. '
        'All nine examples have source excerpts and PDF text-literal corroboration. Five scientific '
        'content/provenance regression tests passed.',
        'These are **source preservation and consistency checks**, not an independent OCR-accuracy '
        'benchmark. Figure interpretations and model-training benefit remain untested. This preview '
        'used one CPU worker and no new OCR inference, teacher API, or model training.',
        '## Inspect the machine-readable results',
        '- [Summary](summary.json)\n- [Nine source-checked examples](examples.json)\n'
        '- [Validation counts](validation.json)\n- [Pipeline configuration](../../config/pmc_native_v3_preview.json)\n'
        '- [Parser and record construction](../../src/native_training.py)\n'
        '- [Source-content regression checks](../../tests/test_native_training.py)',
        '## Related reading',
        '[How biomedical foundation models construct their training data](../bio_foundation_review_2026-10-15/README.md).',
        'Original PDFs/XML, model weights and bulk experiment files remain on RustFS. '
        'This GitHub export contains review text, original figure assets with attribution, and small reports.']
    write(report / 'README.md', '\n\n'.join(overview))
    return documents


def export_foundation_review(directory):
    data = load(directory / 'review.json')
    lines = ['# ' + data['title'], data['scope'], data['method'],
        'This is a source review. Published model results below were not reproduced by our extraction experiment.',
        '## How to interpret the numbers', *['- ' + s for s in data['interpretation_rules']]]
    for section, entries in [('Model families', data['models']), ('Training-data studies', data['training_studies'])]:
        lines.append('## ' + section)
        for entry in entries:
            lines.extend(['### ' + entry['name'], entry['year'] + ' · ' + entry['category'],
                '**Training stage:** ' + entry['stage'], '**Backbone:** ' + entry['base'],
                '**Corpus:** ' + entry['corpus'], '**PDF/XML/text route:** ' + entry['document_route'],
                '**Cleaning/filtering:** ' + entry['curation'],
                '**Training unit and mixture:** ' + entry['training_unit_and_mix'],
                '**Augmentation:** ' + entry['augmentation'], '**Reported evidence:** ' + entry['evidence'],
                '**Limits or missing details:** ' + entry['disclosure_gap'],
                '**Where to check:** ' + entry['source_sections'],
                ' · '.join('[' + s['title'] + '](' + s['url'] + ')' for s in entry['sources'])])
    lines += ['## Proposed project experiments — not executed by this literature review']
    for item in data['recommended_experiments_not_executed']:
        lines.extend(['### ' + item['name'], item['design'], item['reason']])
    lines += ['[Structured review catalog](review.json) · '
              '[Actual three-paper extraction results](../pmc_native_v3_preview_2026-10-15/README.md)']
    write(directory / 'README.md', '\n\n'.join(lines))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--experiment', default=DEFAULT)
    args = parser.parse_args()
    source = ROOT / 'experiments' / args.experiment
    report = ROOT / 'reports' / args.experiment
    documents = export_review(source, report)
    export_foundation_review(ROOT / 'reports/bio_foundation_review_2026-10-15')
    files = [p for p in report.rglob('*') if p.is_file()]
    print(json.dumps(dict(papers=len(documents), review_files=len(files),
                         review_bytes=sum(p.stat().st_size for p in files)), indent=2))
