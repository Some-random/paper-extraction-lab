"""Run the bounded, serial native-XML preview on existing biology papers."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit, urlunsplit, unquote

os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')
from tokenizers import Tokenizer
import pymupdf
from PIL import Image

from native_training import parse_jats, interleaved_records, pack_text

ROOT = Path(__file__).resolve().parents[1]
PST = timezone(timedelta(hours=-8))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def write_jsonl(path, rows):
    path.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_url(value):
    parts = urlsplit(value)
    return urlunsplit(('https', parts.netloc + '.s3.amazonaws.com', parts.path, parts.query, '')) if parts.scheme == 's3' else value


def stable_text(value):
    return re.sub(r'\s+', '', value).replace('−', '-').replace('\u00ad', '').casefold()


def fetch_assets(document, metadata, output, config, accounting):
    urls = {Path(unquote(urlsplit(u).path)).name: u for u in metadata['media_urls']}
    assets = output / 'assets'
    assets.mkdir(exist_ok=True)
    for visual in document['visuals']:
        visual['assets'] = []
        for href in visual['graphics']:
            filename = Path(href).name
            original_url = urls.get(filename)
            if not original_url:
                visual.setdefault('quality_flags', []).append('no_exact_media_filename_in_source_manifest')
                continue
            path = assets / filename
            if not path.exists() and config.get('asset_cache_directory'):
                cached = ROOT / config['asset_cache_directory'] / document['pmcid'] / 'assets' / filename
                if cached.exists():
                    os.link(cached, path)
            expected = parse_qs(urlsplit(original_url).query).get('md5', [''])[0]
            remaining = config['maximum_download_bytes'] - accounting['asset_bytes']
            if remaining <= 0:
                raise RuntimeError('Preview media budget exhausted')
            cap = min(config['maximum_asset_bytes'], remaining)
            if not path.exists():
                if not config['fetch_figure_assets']:
                    continue
                temp = path.with_suffix(path.suffix + '.partial')
                result = subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
                    '--connect-timeout', '8', '--max-time', '20', '--max-filesize', str(cap), public_url(original_url), '-o', str(temp)],
                    capture_output=True, text=True)
                if result.returncode:
                    accounting.setdefault('media_download_failures', []).append(dict(
                        pmcid=document['pmcid'], filename=filename, error=result.stderr[:180]))
                    visual.setdefault('quality_flags', []).append('source_media_download_failed')
                    print('MEDIA_PENDING ' + filename + ': ' + result.stderr.strip()[:120], flush=True)
                    if temp.exists():
                        accounting['new_download_bytes'] += temp.stat().st_size
                        temp.unlink()
                    continue
                if temp.stat().st_size > cap:
                    raise RuntimeError('Figure exceeds byte cap')
                temp.rename(path)
                accounting['new_download_bytes'] += path.stat().st_size
            raw = path.read_bytes()
            if expected and hashlib.md5(raw).hexdigest() != expected.zfill(32):
                raise ValueError('Source media MD5 mismatch: ' + filename)
            with Image.open(path) as image:
                width, height = image.size
                image.verify()
            accounting['asset_bytes'] += len(raw)
            visual['assets'].append(dict(path=str(path.relative_to(ROOT)), source_url=public_url(original_url),
                source_filename=filename, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                manifest_md5=expected, manifest_checksum_passed=bool(expected), width=width, height=height,
                binding='exact XML graphic href and source manifest media filename'))
        visual['unresolved_media'] = visual['kind'] == 'figure' and not visual['assets']


def examples(document):
    """Review examples selected by source identifiers, not model confidence."""
    byid = {v['xml_id']: v for v in document['visuals']}
    blocks = document['blocks']
    out = []

    def table_example(vid, row_key, column, question):
        visual = byid[vid]
        grid = visual['table']
        match = [c for c in grid['cells'] if c['column'] == 0 and c['text'] == row_key]
        if len(match) != 1:
            raise ValueError('Expected a unique reviewed table row: ' + row_key)
        ri = match[0]['row']
        cell_id = grid['occupancy'][ri][column]
        cell = next(c for c in grid['cells'] if c['id'] == cell_id)
        out.append(dict(question=question, answer=cell['text'], type='source_table_lookup',
            source_visual_id=visual['id'], source_xpath=cell['source_xpath'],
            row_label=row_key, column_header_path=cell['column_header_path'], source_quote=cell['text'],
            required_pdf_literals=[cell['text']], validation='exact source-cell lookup; not a reasoning benchmark'))

    def passage_example(needle, question, answer, quote=None, literals=None):
        hits = [b for b in blocks if needle in b['text'] and b['kind'] in {'abstract', 'paragraph'}]
        if len(hits) != 1:
            raise ValueError('Expected unique source paragraph: ' + needle)
        block = hits[0]
        quote = quote or needle
        if quote not in block['text']:
            raise ValueError('Review quote is not an exact source span')
        out.append(dict(question=question, answer=answer, type='source_supported_reading_example',
            source_block_id=block['id'], source_xpath=block['source_xpath'], source_quote=quote,
            required_pdf_literals=literals or [quote],
            validation='assistant source check; not independent human adjudication or generated chain of thought'))

    if document['pmcid'] == 'PMC13651886':
        table_example('T1', 'Axin2', 1, 'What forward qPCR primer is listed for mouse Axin2?')
        table_example('T1', 'Axin2', 2, 'What reverse qPCR primer is listed for mouse Axin2?')
        table_example('T2', 'Cleaved caspase-3', 1, 'What concentration is listed for the cleaved caspase-3 antibody?')
    elif document['pmcid'] == 'PMC13655163':
        table_example('Tab1', 'Sample size', 1, 'What sample size is listed for the Sun et al. comparator study?')
        table_example('Tab2', 'Unique Proteins', 1, 'What count is listed for Unique Proteins in Table 2?')
        passage_example('We report putative causal associations between 13 proteins and 17 outcomes',
            'How does the abstract qualify its protein–outcome causal associations?',
            'The authors report putative causal associations between 13 proteins and 17 outcomes.',
            quote='We report putative causal associations between 13 proteins and 17 outcomes',
            literals=['13 proteins and 17 outcomes'])
    elif document['pmcid'] == 'PMC13645648':
        passage_example('median lifespan for the 8% RU condition (67',
            'What median lifespans were reported for lifelong versus early-adult Lsp2 knockdown in the 8% condition?',
            '67 days for lifelong knockdown and 63 days for early-adult knockdown; the authors state that their difference was not statistically significant.',
            quote='There was no statistical significance between adult-lifelong Lsp2 knockdown (8% RU) and early-adult-specific Lsp2 knockdown (8% 1\u2009week RU), although median lifespan for the 8% RU condition (67\u2009days) was greater than that for the 8%-1-week-RU condition (63\u2009days) (Fig. 4r).',
            literals=['67', '63', 'no statistical significance'])
        passage_example('when ePR was combined with early-adult-specific Lsp2 knockdown, lifespan was shortened',
            'Did combining early-life protein restriction with transient early-adult Lsp2 knockdown always extend lifespan?',
            'No. The authors report shortened lifespan for that combination.',
            quote='By contrast, when ePR was combined with early-adult-specific Lsp2 knockdown, lifespan was shortened (Fig. 4r; 1% ethanol versus 1% 1 week RU).',
            literals=['lifespan was shortened'])
        passage_example('Genetic silencing of Lsp2 phenocopies ePR',
            'What did the abstract report after genetic silencing of Lsp2?',
            'Reduced ribosomal-protein abundance and translation in early adulthood, with extended lifespan.',
            quote='Genetic silencing of Lsp2 phenocopies ePR, attenuating ribosomal-protein abundance and translational activity in early adulthood, and extending lifespan.',
            literals=['Genetic silencing of Lsp2 phenocopies ePR'])
    return out


def validate(document, chunks, interleaved, source):
    from lxml import etree
    original = etree.parse(str(source), etree.XMLParser(resolve_entities=False, no_network=True))
    blockmap = {b['id']: b for b in document['blocks']}
    fragments = {}
    for chunk in chunks:
        for f in chunk['fragments']:
            value = blockmap[f['block_id']]['training_text'][f['char_start']:f['char_end']]
            if value != f['text']:
                raise AssertionError('Fragment disagrees with source-derived block')
            fragments.setdefault(f['block_id'], []).append(f)
    for block in document['blocks']:
        parts = sorted(fragments.get(block['id'], []), key=lambda f: f['char_start'])
        if ''.join(f['text'] for f in parts) != block['training_text']:
            raise AssertionError('Packed text lost or duplicated source characters')
    links = [edge for r in interleaved for edge in r['edges']]
    for edge in links:
        nodes = original.xpath(edge['xref_xpath'], namespaces=original.getroot().nsmap if None not in original.getroot().nsmap else {})
        if len(nodes) != 1 or edge['visual_id'].split(':', 1)[1] not in (nodes[0].get('rid') or '').split():
            raise AssertionError('Image/context edge has no source xref')
    cells = [c for v in document['visuals'] if v['table'] for c in v['table']['cells']]
    for cell in cells:
        if len(original.xpath(cell['source_xpath'])) != 1:
            raise AssertionError('Source cell XPath does not resolve uniquely')
    cited_paths = []
    bibliography = {r['xml_id']: r for r in document['bibliography']}
    for entry in bibliography.values():
        nodes = original.xpath(entry['source_xpath'])
        if len(nodes) != 1 or nodes[0].get('id') != entry['xml_id']:
            raise AssertionError('Bibliography record has no matching source reference')
    for mention in document['citation_mentions']:
        for path in mention['source_xpaths']:
            nodes = original.xpath(path)
            if len(nodes) != 1 or nodes[0].get('ref-type') != 'bibr':
                raise AssertionError('Citation mention has no source bibliography marker')
            cited_paths.append(path)
        for rid in mention['target_xml_ids']:
            if rid not in bibliography and rid not in mention['unresolved_target_ids']:
                raise AssertionError('Unresolved citation target was not reported')
    expected_paths = [original.getpath(n) for n in original.xpath('//xref[@ref-type="bibr"]')]
    if sorted(cited_paths) != sorted(expected_paths):
        raise AssertionError('Source citation markers were lost or counted more than once')
    return dict(kind='structural/provenance checks, not independent accuracy',
        packed_blocks_reconstructed=len(fragments), eligible_blocks=len(document['blocks']),
        context_edges_verified_against_raw_xml=len(links), table_cells_with_resolving_xpaths=len(cells),
        unresolved_figure_table_refs=len(document['unresolved_references']),
        duplicate_visual_ids=document['duplicate_visual_ids'],
        bibliography_entries_with_source_xpaths=len(bibliography),
        source_citation_markers_verified=len(cited_paths),
        citation_mentions=len(document['citation_mentions']),
        expanded_numeric_citation_ranges=sum(m['resolution_method'].startswith('explicit_numeric_range') for m in document['citation_mentions']),
        unresolved_literature_citations=len(document['unresolved_citations']),
        references_without_titles=sum(not r['title'] for r in bibliography.values()),
        references_without_authors=sum(not r['authors'] for r in bibliography.values()),
        longest_text_chunk_tokens=max((c['token_count'] for c in chunks), default=0))


def run(config_path):
    started = time.monotonic()
    config = json.loads(config_path.read_text())
    if config['document_workers'] != 1 or config['gpu_count'] != 0:
        raise ValueError('This preview is CPU-only and serial')
    output = ROOT / config['destination']
    report = ROOT / config['report_directory']
    output.mkdir(parents=True, exist_ok=True)
    report.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(output).free < config['minimum_free_bytes']:
        raise RuntimeError('Shared-storage free-space floor reached')
    tokenizer = Tokenizer.from_file(str(ROOT / config['tokenizer_path']))
    citation_overrides = json.loads((ROOT / config['citation_metadata_path']).read_text())['papers'] if config.get('citation_metadata_path') else {}
    state = json.loads((ROOT / 'experiments' / config['batch'] / 'state.json').read_text())
    originals = {p['pmcid']: p for p in state['papers']}
    accounting = dict(asset_bytes=0, new_download_bytes=0)
    result, summaries, all_examples = [], [], []
    all_chunks, all_interleaved = [], []
    for choice in config['papers']:
        pid = choice['pmcid']
        record = originals[pid]
        directory = output / pid
        directory.mkdir(exist_ok=True)
        source = ROOT / record['source_xml']
        pdf_path = ROOT / record['source_pdf']
        if sha(source) != record['xml_sha256'] or sha(pdf_path) != record['pdf_sha256']:
            raise ValueError('Original paper hash changed')
        metadata = json.loads(source.with_name('source_metadata.json').read_text())
        doc = parse_jats(source, pid, tokenizer, citation_overrides=citation_overrides.get(pid))
        doc.update(journal=record['journal'], source_xml=record['source_xml'], source_pdf=record['source_pdf'],
            source_pdf_sha256=record['pdf_sha256'], pmc_url=f'https://pmc.ncbi.nlm.nih.gov/articles/{pid}/',
            source_pdf_url=public_url(metadata['pdf_url']), source_xml_url=public_url(metadata['xml_url']),
            featured_figure=choice['featured_figure'], selection_reason=choice['purpose'], license_code=metadata['license_code'])
        fetch_assets(doc, metadata, directory, config, accounting)
        chunks = pack_text(doc, tokenizer, config['maximum_text_chunk_tokens'])
        groups = interleaved_records(doc)
        review_examples = examples(doc)
        with pymupdf.open(pdf_path) as pdf:
            native_pages = [page.get_text() for page in pdf]
            for example in review_examples:
                matches = [[i + 1 for i, page in enumerate(native_pages) if stable_text(needle) in stable_text(page)]
                           for needle in example['required_pdf_literals']]
                example['pdf_text_literal_checks'] = [dict(literal=n, pages=m) for n, m in zip(example['required_pdf_literals'], matches)]
                example['pdf_text_corroboration'] = all(matches)
                example['pmcid'] = pid
                example['source_xml_sha256'] = record['xml_sha256']
                example['source_pdf_sha256'] = record['pdf_sha256']
                if not all(matches):
                    raise ValueError('Review example lacks PDF literal corroboration: ' + example['question'])
        checks = validate(doc, chunks, groups, source)
        baseline = json.loads(source.with_name('native_document.json').read_text())
        summary = dict(pmcid=pid, title=doc['title'], journal=doc['journal'],
            retained_blocks=len(doc['blocks']), retained_paragraphs=sum(b['kind'] in {'paragraph', 'abstract'} for b in doc['blocks']),
            excluded_blocks=len(doc['excluded_blocks']), exclusion_reasons=dict(Counter(b['exclusion_reason'] for b in doc['excluded_blocks'])),
            figures=sum(v['kind'] == 'figure' for v in doc['visuals']), tables=sum(v['kind'] == 'table' for v in doc['visuals']),
            downloaded_figure_assets=sum(len(v['assets']) for v in doc['visuals']),
            visuals_with_context=sum(bool(v['referring_paragraphs']) for v in doc['visuals']),
            text_chunks=len(chunks), text_tokens=sum(c['token_count'] for c in chunks),
            bibliography_entries=len(doc['bibliography']), citation_mentions=len(doc['citation_mentions']),
            interleaved_records=len(groups), review_examples=len(review_examples),
            baseline_paragraphs=len(baseline['paragraphs']), checks=checks,
            original_source_hashes_unchanged=sha(source) == record['xml_sha256'] and sha(pdf_path) == record['pdf_sha256'])
        doc['review_examples'] = review_examples
        doc['checks'] = checks
        doc['summary'] = summary
        write_json(directory / 'document.json', doc)
        write_json(directory / 'bibliography.json', doc['bibliography'])
        write_json(directory / 'citation_mentions.json', doc['citation_mentions'])
        write_jsonl(directory / 'text_chunks.jsonl', chunks)
        write_jsonl(directory / 'interleaved.jsonl', groups)
        write_jsonl(directory / 'excluded_blocks.jsonl', doc['excluded_blocks'])
        reader = ['# ' + doc['title']]
        section = None
        for block in doc['blocks']:
            if block['section_path'] != section:
                reader.append('## ' + ' / '.join(block['section_path']))
                section = block['section_path']
            reader.append(block['training_text'])
        (directory / 'clean_article.txt').write_text('\n\n'.join(reader) + '\n')
        all_chunks.extend(chunks)
        all_interleaved.extend(groups)
        result.append(doc)
        summaries.append(summary)
        all_examples.extend(review_examples)
        print(json.dumps(summary, ensure_ascii=False), flush=True)
    write_jsonl(output / 'text_chunks.jsonl', all_chunks)
    write_jsonl(output / 'interleaved.jsonl', all_interleaved)
    write_jsonl(output / 'visual_manifest.jsonl', [dict(pmcid=d['pmcid'],
        title=d['title'], license_code=d['license_code'], **v) for d in result for v in d['visuals']])
    write_json(output / 'config.json', config)
    write_json(output / 'documents.json', result)
    write_json(report / 'examples.json', all_examples)
    summary = dict(pipeline=config.get('pipeline', 'native_training_v4_cited_titles_authors'), created_at_pst=datetime.now(PST).isoformat(),
        papers=summaries, document_workers=1, gpu_count=0, model_inference=False, model_training=False,
        teacher_generation=False, tokenizer=config['tokenizer_note'],
        tokenizer_sha256=sha(ROOT / config['tokenizer_path']), maximum_text_chunk_tokens=config['maximum_text_chunk_tokens'],
        **accounting, seconds=round(time.monotonic() - started, 3),
        timing_scope='This invocation, including cache reuse. Figure acquisition may have occurred in an earlier invocation.',
        limitations=['Three selected papers; engineering diagnostics, not a representative benchmark.',
            'XML is the production source here, not an independently human-adjudicated gold reference.',
            'Exact source links and PDF text corroboration do not validate image interpretation or scientific claims.',
            'No learned educational classifier, entity linker, synthetic teacher, training-value ablation or new OCR run was executed.',
            'Interleaved records preserve source context but are not vision-tokenized or packed for a particular VLM.'])
    write_json(report / 'summary.json', summary)
    write_json(report / 'validation.json', [dict(pmcid=d['pmcid'], **d['checks']) for d in result])
    write_json(output / 'summary.json', summary)
    size = sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
    if size > config['maximum_artifact_bytes']:
        raise RuntimeError('Preview artifacts exceeded the configured bound')
    return output, result, summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'config/pmc_native_v4_citations.json')
    args = parser.parse_args()
    run(args.config)
