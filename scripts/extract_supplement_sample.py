"""Inventory real supplementary files; parse two bounded XLSX source tables.

Serial downloads, no OCR, no teacher/model generation. Original workbooks stay
on RustFS; GitHub receives full TSV sheets, source metadata and readable previews.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import zipfile
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit, urlunsplit

from lxml import etree
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
RUN = 'pmc_native_v4_citations_2026-10-15'
PAPERS = ['PMC13651886', 'PMC13655163', 'PMC13645648']
SELECTED = {('PMC13645648', 'MOESM3'), ('PMC13645648', 'MOESM4'), ('PMC13645648', 'MOESM5')}
MAX_FILE = 8 * 1024**2
MAX_DOWNLOAD = 16 * 1024**2
MAX_REPORT = 16 * 1024**2
MAX_NONEMPTY_CELLS = 200000
MAX_WORKBOOK_XML = 64 * 1024**2


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def scalar(value):
    return value.isoformat() if isinstance(value, (date, datetime)) else value


def public_url(value):
    parts = urlsplit(value)
    return urlunsplit(('https', parts.netloc + '.s3.amazonaws.com', parts.path, parts.query, '')) if parts.scheme == 's3' else value


def parse_workbook(path, directory):
    with zipfile.ZipFile(path) as archive:
        if sum(i.file_size for i in archive.infolist()) > MAX_WORKBOOK_XML:
            raise ValueError('Workbook expanded XML exceeds bounded sample limit')
    workbook = load_workbook(path, read_only=False, data_only=False, keep_links=False)
    sheets = []
    cell_count = 0
    for index, ws in enumerate(workbook.worksheets):
        if ws.max_row > 100000 or ws.max_column > 500:
            raise ValueError('Worksheet extent exceeds bounded sample limit')
        stem = f'sheet{index + 1:02d}'
        tsv = directory / (stem + '.tsv')
        cells_path = directory / (stem + '.cells.jsonl')
        nonempty_rows, nonempty_cells, formula_count = 0, 0, 0
        value_types, date_cells = Counter(), []
        preview = []
        with tsv.open('w', newline='') as output, cells_path.open('w') as cell_output:
            writer = csv.writer(output, delimiter='\t', lineterminator='\n')
            writer.writerow(['source_row'] + [get_column_letter(c) for c in range(1, ws.max_column + 1)])
            for row in ws.iter_rows():
                populated = [c for c in row if c.value is not None]
                if not populated:
                    continue
                nonempty_rows += 1
                nonempty_cells += len(populated)
                cell_count += len(populated)
                if cell_count > MAX_NONEMPTY_CELLS:
                    raise ValueError('Workbook has more cells than the bounded sample permits')
                values = [scalar(c.value) if c.value is not None else '' for c in row]
                writer.writerow([row[0].row] + values)
                for cell in populated:
                    formula_count += cell.data_type == 'f'
                    value_types[cell.data_type] += 1
                    if isinstance(cell.value, (date, datetime)):
                        date_cells.append(dict(coordinate=cell.coordinate, value=scalar(cell.value),
                                               number_format=cell.number_format))
                    cell_output.write(json.dumps(dict(coordinate=cell.coordinate,
                        value=scalar(cell.value), data_type=cell.data_type,
                        number_format=cell.number_format), ensure_ascii=False) + '\n')
                if len(preview) < 20:
                    preview.append([row[0].row] + values)
        sheets.append(dict(name=ws.title, worksheet_number=index + 1,
            source_extent_rows=ws.max_row, source_extent_columns=ws.max_column,
            nonempty_rows=nonempty_rows, nonempty_cells=nonempty_cells, formula_cells=formula_count,
            merged_ranges=[str(r) for r in ws.merged_cells.ranges],
            cell_type_counts=dict(value_types), date_typed_cells=len(date_cells),
            first_date_cells=date_cells[:20],
            complete_tsv=tsv.name, source_cells_jsonl=cells_path.name,
            source_tsv_sha256=hashlib.sha256(tsv.read_bytes()).hexdigest(),
            preview_rows=preview, extraction_status='all_nonempty_rows_exported',
            value_policy='stored values/formulas, not formula evaluation; date-typed cells use ISO representation; original row/column coordinates retained; no gene-name repair'))
    workbook.close()
    return sheets


def run():
    experiment = ROOT / 'experiments' / RUN / 'supplements'
    report = ROOT / 'reports' / RUN / 'supplements'
    experiment.mkdir(parents=True, exist_ok=True)
    report.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(experiment).free < 32 * 1024**3:
        raise RuntimeError('Shared-storage free-space floor reached')
    inventory = []
    for pmcid in PAPERS:
        source = ROOT / 'experiments/pmc_cns_biology_2026-10-14/papers' / pmcid / 'source.xml'
        tree = etree.parse(str(source), etree.XMLParser(resolve_entities=False, no_network=True))
        metadata = json.loads(source.with_name('source_metadata.json').read_text())
        urls = {Path(unquote(urlsplit(u).path)).name: u for u in metadata['media_urls']}
        for number, element in enumerate(tree.xpath('//supplementary-material')):
            hrefs = element.xpath('.//@*[local-name()="href"]')
            for href in hrefs:
                filename = Path(href).name
                record = dict(pmcid=pmcid, xml_id=element.get('id') or f'supplement-{number+1}',
                    label=' '.join(element.xpath('.//label//text()')),
                    caption=re.sub(r'\s+', ' ', ' '.join(element.xpath('.//caption//text()'))).strip(),
                    filename=filename, extension=Path(filename).suffix.lower(),
                    source_xml_xpath=tree.getpath(element), source_xml_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                    source_url=public_url(urls[filename]) if filename in urls else None,
                    status='inventoried; not downloaded or parsed')
                inventory.append(record)
    downloaded = 0
    for item in inventory:
        if (item['pmcid'], item['xml_id']) not in SELECTED:
            continue
        directory = experiment / item['pmcid'] / item['xml_id']
        directory.mkdir(parents=True, exist_ok=True)
        original = directory / item['filename']
        if not item['source_url']:
            item['status'] = 'deferred; no exact source media URL'
            continue
        if not original.exists():
            head = subprocess.run(['curl', '--head', '--fail', '--location', '--silent', '--show-error',
                '--connect-timeout', '8', '--max-time', '20', item['source_url']], capture_output=True, text=True)
            lengths = re.findall(r'(?im)^content-length:\s*(\d+)', head.stdout)
            if lengths:
                item['source_content_length'] = int(lengths[-1])
                if item['source_content_length'] > min(MAX_FILE, MAX_DOWNLOAD-downloaded):
                    item['status'] = 'deferred; source size exceeds bounded download limit'
                    continue
            temporary = original.with_suffix('.partial')
            result = subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
                '--connect-timeout', '8', '--max-time', '40', '--max-filesize', str(min(MAX_FILE, MAX_DOWNLOAD-downloaded)),
                item['source_url'], '-o', str(temporary)], capture_output=True, text=True)
            downloaded += temporary.stat().st_size if temporary.exists() else 0
            if result.returncode:
                item['status'] = 'deferred; bounded download failed'
                item['download_error'] = result.stderr[:200]
                temporary.unlink(missing_ok=True)
                continue
            temporary.rename(original)
        raw = original.read_bytes()
        expected = parse_qs(urlsplit(item['source_url']).query).get('md5', [''])[0]
        if not expected or hashlib.md5(raw).hexdigest() != expected.zfill(32):
            raise ValueError('Supplement lacks a passing official media checksum')
        item.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), manifest_md5=expected,
                    manifest_checksum_passed=True, original_workbook=str(original.relative_to(ROOT)))
        try:
            item['sheets'] = parse_workbook(original, directory)
        except ValueError as error:
            item['status'] = 'deferred after source download: ' + str(error)
            continue
        item['status'] = 'parsed_all_sheets_and_nonempty_rows'
        target = report / item['pmcid'] / item['xml_id']
        target.mkdir(parents=True, exist_ok=True)
        for sheet in item['sheets']:
            shutil.copyfile(directory / sheet['complete_tsv'], target / sheet['complete_tsv'])
        write_json(target / 'workbook.json', item)
        lines = ['# ' + (item['label'] or item['xml_id']), item['caption'],
                 'All nonempty source rows are exported in the TSV files below. The first TSV '
                 'column is the original worksheet row; remaining columns retain Excel letter coordinates. '
                 'Blank rows are omitted, with their original row numbers preserved in subsequent rows. '
                 'The displayed first 20 nonempty rows are explicitly a preview, not the full export.',
                 'Source: **' + item['pmcid'] + '** · original article license **CC BY**. '
                 'Publisher workbook retained unchanged on RustFS. [Manifest and checksums](workbook.json).']
        for sheet in item['sheets']:
            lines += ['## ' + sheet['name'].rstrip(),
                '**' + str(sheet['nonempty_rows']) + ' nonempty rows × ' + str(sheet['source_extent_columns']) +
                ' source columns; ' + str(sheet['nonempty_cells']) + ' populated cells.** '
                '[Complete TSV](' + sheet['complete_tsv'] + ').',
                '```text\n' + '\n'.join('\t'.join(str(v) for v in r).rstrip('\t') for r in sheet['preview_rows']) + '\n```']
            if sheet['date_typed_cells']:
                lines.append('Source quality flag: **' + str(sheet['date_typed_cells']) +
                    ' date-typed cells** are rendered in ISO form. Coordinates and source number formats '
                    'are listed in workbook.json. No gene identifiers are guessed or repaired.')
        (target / 'README.md').write_text('\n\n'.join(lines) + '\n')
        print(json.dumps(dict(pmcid=item['pmcid'], supplement=item['xml_id'], bytes=len(raw),
            sheets=len(item['sheets']), nonempty_rows=sum(s['nonempty_rows'] for s in item['sheets']),
            nonempty_cells=sum(s['nonempty_cells'] for s in item['sheets']))), flush=True)
    summary = dict(inventoried_files=len(inventory), formats=dict(Counter(i['extension'] for i in inventory)),
                   parsed_workbooks=sum(i['status']=='parsed_all_sheets_and_nonempty_rows' for i in inventory),
                   retained_source_workbook_bytes=sum(i.get('bytes', 0) for i in inventory),
                   new_download_bytes=downloaded, maximum_download_bytes=MAX_DOWNLOAD,
                   download_accounting_scope='this invocation; existing source workbooks are reused',
                   generated_or_inferred_values=False, inventory=inventory)
    write_json(experiment / 'inventory.json', summary)
    write_json(report / 'inventory.json', summary)
    lines = ['# Real supplementary biological tables',
        'The main-article XML tables are complete, but do not include the paper\'s separate spreadsheet files. '
        'This inventory exposes that coverage boundary and adds two bounded, original biological workbooks.',
        '**' + str(len(inventory)) + ' linked supplementary files**: ' + json.dumps(summary['formats']) + '. '
        '**' + str(summary['parsed_workbooks']) + ' workbooks fully parsed.** Other files are listed with their actual status.',
        '| Paper | Source label/file | Contents | Status / complete parsed sheets |\n| --- | --- | --- | --- |']
    for item in inventory:
        link = item['status']
        if item['status'] == 'parsed_all_sheets_and_nonempty_rows':
            link = '[Read full-sheet links and preview](' + item['pmcid'] + '/' + item['xml_id'] + '/README.md)'
        lines.append('| ' + item['pmcid'] + ' | ' + (item['label'] or item['filename']) + ' | ' +
                     item['caption'].replace('|','\\|') + ' | ' + link + ' |')
    lines += ['[Machine-readable inventory, source URLs and hashes](inventory.json). '
        'Spreadsheet values are extracted, not interpreted or checked for biological correctness. '
        'Main-text citations and original figure/context records are available in the [three-paper results](../README.md).']
    (report / 'README.md').write_text('\n\n'.join(lines[:3]) + '\n\n' + '\n'.join(lines[3:]) + '\n')
    if sum(p.stat().st_size for p in report.rglob('*') if p.is_file()) > MAX_REPORT:
        raise RuntimeError('Supplement review export exceeds byte budget')
    print(json.dumps({k:v for k,v in summary.items() if k!='inventory'},indent=2))


if __name__ == '__main__':
    run()
