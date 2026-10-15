"""Bounded, resumable PMC download -> JATS -> full-paper olmOCR 2 batch.

One document/network/inference worker; cached weights; no teacher API/training.
Original PDF/XML and raw OCR are retained. Only disposable page rasters and
incomplete HTTP temporary files are removed. Every completed stage is durable.
"""
import argparse
import copy
import csv
import fcntl
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from lxml import etree
import pypdfium2 as pdfium
from bio_table_metrics import semantic_text, parse_table, table_records, compare
from evaluate_bio_tools import bind_captions

ROOT = Path(__file__).resolve().parents[1]
PST = timezone(timedelta(hours=-8))
S3 = 'https://pmc-oa-opendata.s3.amazonaws.com'
ESEARCH = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
BIO = {
    'gene': r'\bgenes?\b|\bgenom\w*|\bgenetic\w*|\btranscript\w*|\bRNA\b|\bDNA\b',
    'protein': r'\bproteins?\b|\bpeptides?\b|\bantibod\w*|\benzym\w*',
    'organism': r'\bmice\b|\bmouse\b|\bneur\w*|\bbrain\b|\btissue\w*|\bbacter\w*|\bmicrobi\w*',
    'disease': r'\bcancer\w*|\btumou?r\w*|\bmelanoma\b|\bdisease\w*|\bimmun\w*|\bfibrosis\b|\bsenescen\w*',
    'cell': r'\bcells?\b|\bcellular\b|\bhuman\w*|\bpatients?\b|\bclinical\w*|\bbiolog\w*',
}


def now():
    return datetime.now(PST).isoformat()


def json_write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temp.replace(path)


def text(node):
    if node is None:
        return ''
    return re.sub(r'[ \t\r\n]+', ' ', semantic_text(node)).strip()


def label_id(label, kind):
    match = re.search(r'(?:Table|Figure|Fig\.?)\s*([Ss]?\d+[A-Za-z]?)', label, re.I)
    return kind + ':' + match[1].casefold() if match else None


def public_url(url):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme == 's3':
        return urllib.parse.urlunsplit(('https', parts.netloc + '.s3.amazonaws.com',
            urllib.parse.quote(urllib.parse.unquote(parts.path), safe='/'), parts.query, ''))
    return url


def native_document(path, pmcid):
    tree = etree.parse(str(path), etree.XMLParser(resolve_entities=False, no_network=True))
    # Normalize namespace names only in the derived parsing view; originals stay byte-identical.
    nodes = list(tree.iter())
    paths = {node: tree.getpath(node) for node in nodes if isinstance(node.tag, str)}
    for node in nodes:
        if isinstance(node.tag, str):
            node.tag = etree.QName(node).localname
    meta = tree.find('front/article-meta')
    if meta is None or tree.find('body') is None:
        raise ValueError('No parseable JATS article metadata/body')
    paragraphs = []
    for i, p in enumerate(tree.xpath('(//body//p | //back//p)[not(ancestor::fig) and not(ancestor::table-wrap)]')):
        refs = sorted({rid for x in p.findall('.//xref') for rid in (x.get('rid') or '').split()})
        headings = [text(s.find('title')) for s in p.iterancestors('sec')]
        paragraphs.append(dict(id=pmcid + ':p' + str(i), text=text(p), section_path=list(reversed(headings)),
            source_xpath=paths[p], referenced_xml_ids=refs,
            source_region='back' if any(a.tag == 'back' for a in p.iterancestors()) else 'body'))
    evidence = []
    for i, node in enumerate(tree.xpath('//fig | //table-wrap')):
        kind = 'table' if node.tag == 'table-wrap' else 'figure'
        xml_id = node.get('id') or kind + '_' + str(i)
        label = text(node.find('label'))
        item = dict(id=pmcid + ':' + xml_id, xml_id=xml_id, kind=kind, label=label,
            normalized_label=label_id(label, kind), caption=text(node.find('caption')),
            notes=text(node.find('table-wrap-foot')), source_xpath=paths[node],
            referring_paragraphs=[p for p in paragraphs if xml_id in p['referenced_xml_ids']],
            binding_method='explicit_JATS_xref', source_branch='native_JATS_reference',
            graphics=[g.get('{http://www.w3.org/1999/xlink}href') or g.get('href') for g in node.findall('.//graphic')],
            quality_flags=['visual_semantics_unverified'] if kind == 'figure' else [])
        table = node.find('.//table')
        if table is not None:
            markup = copy.deepcopy(table)
            etree.cleanup_namespaces(markup)
            item['table_html'] = etree.tostring(markup, encoding='unicode')
            try:
                if len(table.findall('.//tr')) > 150:
                    raise ValueError('Reference exceeds the 150-row diagnostic adapter limit')
                item['scientific_grid'] = parse_table(item['table_html'])
                item['logical_table'] = table_records(item['scientific_grid'])
            except Exception as exc:
                item['quality_flags'].append('table_adapter_unscored: ' + str(exc))
        elif kind == 'table':
            item['quality_flags'].append('No machine-readable source table grid')
        evidence.append(item)
    sections = []
    for node in tree.xpath('//body//sec | //back//sec'):
        sections.append(dict(title=text(node.find('title')), section_type=node.get('sec-type'), source_xpath=paths[node]))
    abstract = ' '.join(text(a) for a in meta.findall('abstract'))
    title = text(meta.find('title-group/article-title'))
    identifiers = {node.get('pub-id-type'): text(node) for node in meta.findall('article-id')}
    md = ['# ' + title, '\n## Abstract\n' + abstract]
    def walk(node, level=2):
        if not isinstance(node.tag, str):
            return
        if node.tag in ['sec', 'app']:
            heading = text(node.find('title'))
            if heading:
                md.append('\n' + '#' * min(level, 6) + ' ' + heading)
            for child in node:
                if child.tag != 'title':
                    walk(child, level + 1)
        elif node.tag == 'p':
            md.append(text(node))
        elif node.tag == 'ref-list':
            md.append('\n## ' + (text(node.find('title')) or 'References'))
            for child in node.findall('ref'):
                md.append(text(child))
        elif node.tag in ['fig', 'table-wrap']:
            md.append(text(node.find('label')) + '. ' + text(node.find('caption')))
            table = node.find('.//table')
            if table is not None:
                md.append(etree.tostring(table, encoding='unicode'))
            notes = text(node.find('table-wrap-foot'))
            if notes:
                md.append(notes)
        else:
            for child in node:
                walk(child, level)
    walk(tree.find('body'))
    back = tree.find('back')
    if back is not None:
        walk(back)
    # Retain visuals stored outside the body, a common publisher convention.
    for node in tree.xpath('//fig[not(ancestor::body) and not(ancestor::back)] | //table-wrap[not(ancestor::body) and not(ancestor::back)]'):
        walk(node)
    return dict(pmcid=pmcid, title=title, abstract=abstract, identifiers=identifiers,
        parser_schema_version=2,
        article_type=tree.getroot().get('article-type'), language=tree.getroot().get('{http://www.w3.org/XML/1998/namespace}lang'),
        sections=sections, paragraphs=paragraphs, evidence=evidence,
        native_markdown='\n\n'.join(part for part in md if part),
        source_branch='native_JATS_reference; never included in OCR prompts',
        validation_note='Source-derived structure/notation; no independent scientific validation.')


class LimitReached(Exception):
    pass


class Rejected(Exception):
    pass


class Batch:
    def __init__(self, config):
        self.config = config
        self.dest = ROOT / config['destination']
        self.dest.mkdir(parents=True, exist_ok=True)
        self.lock = (self.dest / 'worker.lock').open('a+')
        fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        state_path = self.dest / 'state.json'
        self.state = json.loads(state_path.read_text()) if state_path.exists() else dict(
            batch_id=config['batch_id'], started_at_pst=now(), downloaded_response_bytes=0,
            papers=[], rejected=[], events=[], status='starting')
        if state_path.exists():
            self.state.setdefault('resume_history', []).append(dict(resumed_at_pst=now(),
                prior_status=self.state.get('status'), prior_limit_reason=self.state.get('limit_reason'),
                prior_error=self.state.get('error')))
            for name in ['finished_at_pst', 'limit_reason', 'error']:
                self.state.pop(name, None)
        self.state.update(pid=os.getpid(), last_started_at_pst=now(), status='running', stage='initializing')
        deadline = datetime.fromisoformat(config['stop_before_pst'])
        runtime_end = datetime.now(PST) + timedelta(hours=config['maximum_runtime_hours'])
        # Resuming does not reset the cumulative overnight runtime allowance.
        original_end = datetime.fromisoformat(self.state['started_at_pst']) + timedelta(hours=config['maximum_runtime_hours'])
        self.end = min(deadline, runtime_end, original_end)
        self.state['stop_at_pst'] = self.end.isoformat()
        json_write(self.dest / 'config.json', config)
        self.persist()

    def size(self):
        return sum(p.stat().st_size for p in self.dest.rglob('*') if p.is_file())

    def guard(self, reserve=0):
        if (self.dest / 'STOP').exists():
            raise LimitReached('User stop file requested')
        if datetime.now(PST) >= self.end:
            raise LimitReached('Runtime/deadline limit reached')
        if self.size() + reserve + self.config.get('finalization_margin_bytes', 8 * 2**20) > self.config['maximum_artifact_bytes']:
            raise LimitReached('Artifact storage cap reached')
        fs = os.statvfs(self.dest)
        if fs.f_bavail * fs.f_frsize - reserve < self.config['minimum_free_bytes']:
            raise LimitReached('Shared filesystem free-space floor reached')

    def persist(self):
        self.state['updated_at_pst'] = now()
        self.state['artifact_bytes'] = self.size()
        self.state['native_parsed_papers'] = sum(p.get('native_status') == 'completed' for p in self.state['papers'])
        self.state['ocr_complete_papers'] = sum(p.get('ocr_status') == 'completed' for p in self.state['papers'])
        self.state['ocr_partial_papers'] = sum(p.get('ocr_status') == 'partial' for p in self.state['papers'])
        self.state['ocr_pages_completed'] = sum(p.get('ocr_pages_completed', 0) for p in self.state['papers'])
        json_write(self.dest / 'state.json', self.state)
        self.report()

    def event(self, message):
        print(now() + ' ' + message, flush=True)
        self.state['events'].append(dict(time_pst=now(), message=message))
        self.state['events'] = self.state['events'][-100:]
        self.persist()

    def request(self, url, maximum, output=None):
        if self.config.get('http_backend') in ('python310_bridge', 'python_bridge'):
            return self.bridge_request(url, maximum, output)
        return self.direct_request(url, maximum, output)

    def bridge_request(self, url, maximum, output=None):
        self.guard(maximum if output else 1_048_576)
        temp = output.with_name(output.name + '.part') if output else None
        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(2):
            child = None
            try:
                network_left = self.config['maximum_download_bytes'] - self.state['downloaded_response_bytes']
                if network_left <= 0:
                    raise LimitReached('Network payload cap reached')
                admitted = min(maximum, network_left)
                python = ROOT / self.config.get('http_python', '.venv/bin/python')
                child = subprocess.Popen([str(python), str(ROOT / 'src/pmc_http_fetch.py'), public_url(url), str(admitted)],
                    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                header = json.loads(child.stdout.readline())
                expected = int(header.get('content_length', 0))
                if not header.get('ok'):
                    if expected > maximum:
                        raise Rejected('Object exceeds per-file byte cap')
                    if expected > network_left:
                        raise LimitReached('Network payload cap reached')
                    if header.get('http_status') and not header.get('retryable', True):
                        raise Rejected('HTTP ' + str(header['http_status']) + ': source object unavailable')
                    raise urllib.error.URLError(header.get('error', 'HTTPS bridge failed'))
                total = 0
                chunks = []
                handle = temp.open('wb') if temp else None
                try:
                    while total < admitted:
                        chunk = child.stdout.read(min(262144, admitted - total))
                        if not chunk:
                            break
                        total += len(chunk)
                        self.state['downloaded_response_bytes'] += len(chunk)
                        if handle:
                            handle.write(chunk)
                        else:
                            chunks.append(chunk)
                    child.wait(timeout=40)
                    if child.returncode:
                        raise urllib.error.URLError('HTTPS bridge exited: ' + child.stderr.read().decode(errors='replace')[:300])
                    if expected and total != expected:
                        raise urllib.error.URLError('Incomplete HTTP object')
                    if not expected and total == admitted:
                        raise LimitReached('Unknown-length object exhausted the available byte budget')
                finally:
                    if handle:
                        handle.close()
                if temp:
                    temp.replace(output)
                    self.persist()
                    return output.read_bytes()
                return b''.join(chunks)
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt:
                    raise
                time.sleep(2)
            finally:
                if child and child.poll() is None:
                    child.terminate()
                    child.wait(timeout=10)
                if temp and temp.exists():
                    temp.unlink()

    def direct_request(self, url, maximum, output=None):
        self.guard(maximum if output else 1_048_576)
        url = public_url(url)
        temp = output.with_name(output.name + '.part') if output else None
        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(2):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'paper-extraction-lab/0.2 (one-worker PMC research batch)'})
                with urllib.request.urlopen(req, timeout=35) as response:
                    expected = int(response.headers.get('Content-Length', '0'))
                    if expected > maximum:
                        raise Rejected('Object exceeds per-file byte cap')
                    if expected and self.state['downloaded_response_bytes'] + expected > self.config['maximum_download_bytes']:
                        raise LimitReached('Network payload cap reached')
                    chunks = []
                    total = 0
                    handle = temp.open('wb') if temp else None
                    try:
                        while True:
                            network_left = self.config['maximum_download_bytes'] - self.state['downloaded_response_bytes']
                            file_left = maximum - total
                            if expected and total == expected:
                                break
                            if network_left <= 0:
                                raise LimitReached('Network payload cap reached')
                            if file_left <= 0:
                                raise Rejected('Unknown-length object exhausted its per-file cap')
                            chunk = response.read(min(262144, network_left, file_left))
                            if not chunk:
                                break
                            total += len(chunk)
                            self.state['downloaded_response_bytes'] += len(chunk)
                            if total > maximum:
                                raise Rejected('Object exceeds per-file byte cap')
                            if self.state['downloaded_response_bytes'] > self.config['maximum_download_bytes']:
                                raise LimitReached('Network payload cap reached')
                            if handle:
                                handle.write(chunk)
                            else:
                                chunks.append(chunk)
                        if expected and total != expected:
                            raise ValueError('Incomplete HTTP object')
                    finally:
                        if handle:
                            handle.close()
                if temp:
                    temp.replace(output)
                    self.persist()
                    return output.read_bytes()
                return b''.join(chunks)
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt:
                    raise
                self.state['events'].append(dict(time_pst=now(), message='HTTP retry: ' + str(exc)))
                time.sleep(2)
            finally:
                if temp and temp.exists():
                    temp.unlink()

    def metadata(self, pmcid):
        url = S3 + '/?' + urllib.parse.urlencode({'list-type': 2, 'prefix': 'metadata/' + pmcid + '.'})
        listing = etree.fromstring(self.request(url, 1_048_576))
        keys = [n.text for n in listing.findall('.//{*}Key') if n.text.endswith('.json')]
        choices = []
        for key in keys:
            raw = self.request(S3 + '/' + key, 1_048_576)
            row = json.loads(raw)
            if row.get('pdf_url') and row.get('xml_url'):
                choices.append((row, raw, S3 + '/' + key))
        if not choices:
            raise Rejected('No distributed version with PDF and XML')
        choices.sort(key=lambda x: (str(x[0].get('is_manuscript')).casefold() in ['true', 'yes', '1'], -int(x[0].get('version', 1))))
        return choices[0]

    def download(self, url, path, maximum):
        raw = path.read_bytes() if path.exists() else self.request(url, maximum, path)
        expected = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query).get('md5')
        if expected and hashlib.md5(raw).hexdigest().casefold() != expected[0].casefold():
            raise ValueError('Metadata MD5 mismatch; retained source needs inspection')
        return raw

    def candidates(self, journal):
        path = self.dest / 'api' / (re.sub(r'\W+', '_', journal['name']) + '.json')
        if path.exists():
            return json.loads(path.read_text())['response']['esearchresult']['idlist']
        titles = '(' + ' OR '.join('"' + n + '"[journal]' for n in journal['query_names']) + ')'
        biology = '(' + ' OR '.join('"' + w + '"[tiab]' for w in self.config['biology_query_terms']) + ')'
        query = titles + ' AND ' + biology + ' AND open_access[filter] AND "has pdf"[filter] AND hasabstract NOT "pmc embargo"[filter] NOT (articletyperetraction OR articletypecorrection OR hasretractionin)'
        url = ESEARCH + '?' + urllib.parse.urlencode(dict(db='pmc', term=query, retmode='json',
            retmax=self.config['candidate_ids_per_journal'], tool='paper_extraction_lab'))
        raw = json.loads(self.request(url, 4_194_304))
        result = raw['esearchresult']
        if result.get('errorlist') or result.get('warninglist', {}).get('quotedphrasesnotfound'):
            raise ValueError('PMC query must be resolved: ' + json.dumps(result))
        json_write(path, dict(query=query, url=url, checked_at_pst=now(), response=raw))
        time.sleep(0.4)
        return result['idlist']

    def acquire(self):
        self.state['stage'] = 'download_and_native_parse'
        self.persist()
        # Refresh checkpoints made before appendix/back-matter extraction was added.
        # The old derived files remain available; original sources never change.
        for paper in self.state['papers']:
            out = ROOT / paper['source_directory']
            previous = json.loads((out / 'native_document.json').read_text())
            if previous.get('parser_schema_version') == 2:
                continue
            self.guard(8 * 2**20)
            old_schema = any('source_region' not in p for p in previous.get('paragraphs', []))
            if old_schema:
                for name in ['native_document.json', 'fullpaper_native.md', 'source_evidence.jsonl']:
                    path = out / name
                    archive = path.with_name(path.stem + '_before_appendix_fix' + path.suffix)
                    if not archive.exists():
                        archive.write_bytes(path.read_bytes())
            document = native_document(out / 'source.xml', paper['pmcid'])
            self.save_native(out, paper, document)
            if old_schema:
                self.event('REFRESH NATIVE ' + paper['pmcid'] + ' retained appendix/back-matter context')
        self.persist()
        counts = Counter(p['journal'] for p in self.state['papers'])
        seen = {p['pmcid'] for p in self.state['papers']} | {p['pmcid'] for p in self.state['rejected']
            if 'pmcid' in p and not p.get('retryable') and not any(term in p.get('reason', '') for term in ['URLError', 'TimeoutError'])}
        dois = {(p.get('doi') or '').casefold() for p in self.state['papers'] if p.get('doi')}
        queues = []
        for journal in self.config['journals']:
            if counts[journal['name']] >= self.config['papers_per_journal']:
                continue
            try:
                queues.append((journal, iter(self.candidates(journal))))
            except LimitReached:
                raise
            except Exception as exc:
                self.event('Candidate search failed for ' + journal['name'] + ': ' + str(exc))
        active = list(queues)
        while active and len(self.state['papers']) < self.config['target_papers']:
            remaining = []
            for journal, ids in active:
                self.guard(32 * 2**20)
                if counts[journal['name']] >= self.config['papers_per_journal']:
                    continue
                try:
                    uid = next(ids)
                except StopIteration:
                    continue
                remaining.append((journal, ids))
                pmcid = 'PMC' + uid
                if pmcid in seen:
                    continue
                seen.add(pmcid)
                out = self.dest / 'papers' / pmcid
                out.mkdir(parents=True, exist_ok=True)
                try:
                    meta, raw_meta, meta_url = self.metadata(pmcid)
                    (out / 'source_metadata.json').write_bytes(raw_meta)
                    if str(meta.get('is_retracted')).casefold() in ['true', 'yes', '1']:
                        raise Rejected('Retracted record')
                    doi = meta.get('doi') or ''
                    if doi.casefold() in dois:
                        raise Rejected('Duplicate DOI')
                    raw_xml = self.download(meta['xml_url'], out / 'source.xml', self.config['maximum_xml_bytes'])
                    native = native_document(out / 'source.xml', pmcid)
                    if native['article_type'] not in self.config['accepted_article_types']:
                        raise Rejected('Article type: ' + str(native['article_type']))
                    if native['language'] and native['language'].casefold() not in ['en', 'eng', 'en-us', 'en-gb']:
                        raise Rejected('Non-English article')
                    bio_text = native['title'] + ' ' + native['abstract']
                    markers = [key for key, pattern in BIO.items() if re.search(pattern, bio_text, re.I)]
                    if len(markers) < 2 or not any(m != 'cell' for m in markers):
                        raise Rejected('Insufficient biology title/abstract markers: ' + ','.join(markers))
                    required = self.config.get('required_biology_marker_groups', [])
                    if required and not any(m in required for m in markers):
                        raise Rejected('No required research-biology marker: ' + ','.join(markers))
                    raw_pdf = self.download(meta['pdf_url'], out / 'source.pdf', self.config['maximum_pdf_bytes'])
                    if not raw_pdf.startswith(b'%PDF-'):
                        raise ValueError('Source object is not a PDF')
                    pdf = pdfium.PdfDocument(str(out / 'source.pdf'))
                    pages = len(pdf)
                    pdf.close()
                    if pages > self.config['maximum_pdf_pages_per_paper']:
                        raise Rejected('PDF exceeds ' + str(self.config['maximum_pdf_pages_per_paper']) + ' pages')
                    record = dict(pmcid=pmcid, journal=journal['name'], doi=doi, title=native['title'],
                        pdf_pages=pages, source_directory=str(out.relative_to(ROOT)),
                        source_pdf=str((out / 'source.pdf').relative_to(ROOT)), source_xml=str((out / 'source.xml').relative_to(ROOT)),
                        pdf_url=meta['pdf_url'], xml_url=meta['xml_url'], metadata_url=meta_url,
                        pdf_sha256=hashlib.sha256(raw_pdf).hexdigest(), xml_sha256=hashlib.sha256(raw_xml).hexdigest(),
                        pdf_bytes=len(raw_pdf), xml_bytes=len(raw_xml), license_code=meta.get('license_code'),
                        version=meta.get('version'), is_manuscript=meta.get('is_manuscript'),
                        article_type=native['article_type'], biology_markers=markers,
                        native_status='completed', ocr_status='pending', ocr_pages_completed=0,
                        sections=len(native['sections']), paragraphs=len(native['paragraphs']),
                        figures=sum(e['kind'] == 'figure' for e in native['evidence']),
                        tables=sum(e['kind'] == 'table' for e in native['evidence']),
                        elements_with_referring_paragraphs=sum(bool(e['referring_paragraphs']) for e in native['evidence']),
                        table_cells_checked=0, matched_labelled_cells=0, matched_with_header_checks=0,
                        acquired_at_pst=now())
                    self.save_native(out, record, native)
                    self.state['papers'].append(record)
                    if doi:
                        dois.add(doi.casefold())
                    counts[journal['name']] += 1
                    self.event('NATIVE ' + pmcid + ' ' + journal['name'] + ' pages=' + str(pages))
                except LimitReached:
                    raise
                except Exception as exc:
                    self.state['rejected'].append(dict(pmcid=pmcid, journal=journal['name'], reason=type(exc).__name__ + ': ' + str(exc),
                        retryable=isinstance(exc, (urllib.error.URLError, TimeoutError))))
                    self.event('SKIP ' + pmcid + ' ' + str(exc))
                if len(self.state['papers']) >= self.config['target_papers']:
                    break
            active = remaining

    def save_native(self, out, paper, native):
        native.update(source_pdf=paper['source_pdf'], source_xml=paper['source_xml'],
            source_pdf_sha256=paper['pdf_sha256'], source_xml_sha256=paper['xml_sha256'])
        (out / 'fullpaper_native.md').write_text(native.pop('native_markdown') + '\n')
        json_write(out / 'native_document.json', native)
        (out / 'source_evidence.jsonl').write_text(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in native['evidence']))
        paper.update(native_parser_schema_version=native['parser_schema_version'],
            sections=len(native['sections']), paragraphs=len(native['paragraphs']),
            figures=sum(e['kind'] == 'figure' for e in native['evidence']),
            tables=sum(e['kind'] == 'table' for e in native['evidence']),
            elements_with_referring_paragraphs=sum(bool(e['referring_paragraphs']) for e in native['evidence']))

    def evaluate(self, paper):
        out = ROOT / paper['source_directory']
        native = json.loads((out / 'native_document.json').read_text())
        outputs = []
        candidates = defaultdict(list)
        whole = []
        spans = []
        offset = 0
        for path in sorted((out / 'olmocr').glob('page_*/result.json')):
            result = json.loads(path.read_text())
            outputs.append(result)
            natural = re.sub(r'\A---\s*\n.*?\n---\s*\n', '', result['markdown'], count=1, flags=re.S)
            whole.append(natural)
            spans.append(dict(start=offset, end=offset + len(natural), page=result['source_page'], status=result['status']))
            offset += len(natural) + 2
            bound = bind_captions(result, {})
            for index, binding in bound.items():
                candidates[binding['label']].append(dict(page=result['source_page'], index=index,
                    table=result['tables'][index], binding=binding, inference_status=result['status']))
        (out / 'fullpaper_olmocr.md').write_text('\n\n'.join(whole))
        json_write(out / 'olmocr_document.json', dict(pmcid=paper['pmcid'], source_pdf=paper['source_pdf'],
            text='\n\n'.join(whole), page_spans=spans, model=self.config['model'],
            model_revision=self.config['model_revision'], complete=len(outputs) == paper['pdf_pages'] and all(r['status'] == 'completed' for r in outputs),
            reference_xml_in_prompt=False, runner_scope='checkpoint plus official prompt; not full production pipeline'))
        checks = []
        demos = []
        for source in native['evidence']:
            if source['kind'] != 'table' or 'logical_table' not in source:
                continue
            total = sum(len(r['cells']) for r in source['logical_table']['records'])
            found = candidates.get(source['normalized_label'], [])
            # Select using generated structure/adjacency only, never reference values.
            def rank(item):
                try:
                    rows = parse_table(item['table']['html'])['nrows']
                except Exception:
                    rows = 0
                return (-rows, item['binding']['distance'], item['page'], item['index'])
            chosen = min(found, key=rank) if found else None
            values = compare(source, chosen['table']['html']) if chosen else dict(matched=0, total=total, quantity_and_value_matched=0)
            check = dict(source_id=source['id'], label=source['label'],
                candidate_page=chosen['page'] if chosen else None, total=total,
                matched=values['matched'], with_header_checks=values.get('quantity_and_value_matched', 0),
                source_xpath=source['source_xpath'], cells=values.get('cells', []),
                error=values.get('error'), binding=chosen['binding'] if chosen else None,
                note='Exploratory silver-reference checks; fixed row/column matching. Split multipage tables can fail this adapter.')
            checks.append(check)
            if chosen and chosen['inference_status'] == 'completed':
                for cell in values.get('cells', []):
                    if cell.get('quantity_and_value_matched') and cell['header'] and cell['expected']:
                        demos.append(dict(pmcid=paper['pmcid'], question='In ' + source['label'] + ', what is reported for ' + cell['header'] + ' for ' + cell['row_key'] + '?',
                            answer=cell['expected'], evidence_id=source['id'], source_pdf=paper['source_pdf'],
                            source_page=chosen['page'], source_xpath=source['source_xpath'],
                            row_key=cell['row_key'], column=cell['column'], caption=source['caption'],
                            referring_paragraphs=source['referring_paragraphs'],
                            validation='Source cell replay plus OCR value/header agreement; not independent annotation.',
                            training_status='Diagnostic lookup only; not teacher reasoning or approved training data.'))
                        if len(demos) >= 6:
                            break
        json_write(out / 'table_checks.json', dict(pmcid=paper['pmcid'], checks=checks))
        (out / 'lookup_qa_diagnostics.jsonl').write_text(''.join(json.dumps(d, ensure_ascii=False) + '\n' for d in demos[:6]))
        paper.update(table_cells_checked=sum(c['total'] for c in checks), matched_labelled_cells=sum(c['matched'] for c in checks),
            matched_with_header_checks=sum(c['with_header_checks'] for c in checks), lookup_qa_diagnostics=min(len(demos), 6),
            table_check_note='Silver-reference heuristic diagnostics, not general OCR accuracy.')

    def ocr(self):
        from run_bio_tool import vlm_setup, vlm_extract
        import torch
        import transformers
        from PIL import Image
        self.state['stage'] = 'olmocr_full_papers'
        self.persist()
        self.guard(16 * 2**20)
        setup = vlm_setup('olmocr')
        if setup[3]['model'] != self.config['model'] or setup[3]['revision'] != self.config['model_revision']:
            raise RuntimeError('Cached model does not match the batch model/revision')
        json_write(self.dest / 'runtime.json', dict(model_record=setup[3], torch=torch.__version__, transformers=transformers.__version__,
            visible_gpu=os.environ.get('CUDA_VISIBLE_DEVICES'), document_workers=1, inference_batch_size=1,
            precision='bfloat16', render_dpi=144, longest_image_edge=1288, reference_xml_in_prompt=False))
        # Shortest first ensures complete papers under an overnight deadline.
        order = sorted(self.state['papers'], key=lambda p: (p['pdf_pages'], p['pmcid']))
        for paper in self.state['papers']:
            page_files = list((ROOT / paper['source_directory'] / 'olmocr').glob('page_*/result.json'))
            paper['ocr_pages_completed'] = len(page_files)
        self.persist()
        page_count = self.state['ocr_pages_completed']
        for paper in order:
            if paper['ocr_status'] == 'completed':
                continue
            if page_count + paper['pdf_pages'] - paper.get('ocr_pages_completed', 0) > self.config['maximum_ocr_pages']:
                paper['ocr_status'] = 'deferred_page_budget'
                self.persist()
                continue
            self.guard(8 * 2**20)
            out = ROOT / paper['source_directory']
            pdf = pdfium.PdfDocument(str(out / 'source.pdf'))
            paper['ocr_status'] = 'partial'
            paper['ocr_started_at_pst'] = now()
            self.state['active_paper'] = paper['pmcid']
            try:
                for number in range(1, len(pdf) + 1):
                    page_out = out / 'olmocr' / ('page_' + str(number).zfill(4))
                    if (page_out / 'result.json').exists():
                        continue
                    self.guard(8 * 2**20)
                    page_out.mkdir(parents=True, exist_ok=True)
                    page = pdf[number - 1]
                    bitmap = page.render(scale=2)
                    image = bitmap.to_pil().convert('RGB')
                    bitmap.close(); page.close()
                    image.thumbnail((1288, 1288), Image.Resampling.LANCZOS)
                    raster = self.dest / 'temporary_page.png'
                    image.save(raster)
                    image.close()
                    image_hash = hashlib.sha256(raster.read_bytes()).hexdigest()
                    remaining = (self.end - datetime.now(PST)).total_seconds()
                    timeout = max(0.5, min(self.config['maximum_page_inference_seconds'], remaining))
                    torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
                    start = time.monotonic()
                    try:
                        result = vlm_extract('olmocr', setup, dict(image=str(raster.relative_to(ROOT))), page_out, generation_timeout_seconds=timeout)
                    finally:
                        if raster.exists():
                            raster.unlink()
                    torch.cuda.synchronize()
                    result.update(pmcid=paper['pmcid'], source_page=number, source_pdf=paper['source_pdf'],
                        source_pdf_sha256=paper['pdf_sha256'], input_image_sha256=image_hash,
                        render_dpi=144, input_image_retained=False, input_image_reproducible_from_source_pdf=True,
                        elapsed_seconds=round(time.monotonic() - start, 3),
                        peak_gpu_allocated_gib=round(torch.cuda.max_memory_allocated() / 2**30, 3),
                        reference_xml_in_prompt=False, model_revision=self.config['model_revision'])
                    (page_out / 'raw.md').write_text(result['markdown'])
                    json_write(page_out / 'result.json', result)
                    paper['ocr_pages_completed'] += 1
                    page_count += 1
                    self.event('OCR ' + paper['pmcid'] + ' page=' + str(number) + '/' + str(len(pdf)) + ' ' + result['status'])
                self.evaluate(paper)
                statuses = [json.loads(p.read_text())['status'] for p in (out / 'olmocr').glob('page_*/result.json')]
                paper['ocr_status'] = 'completed' if len(statuses) == paper['pdf_pages'] and all(s == 'completed' for s in statuses) else 'partial'
                paper['ocr_finished_at_pst'] = now()
                self.event('PAPER ' + paper['pmcid'] + ' ' + paper['ocr_status'])
            except LimitReached:
                self.evaluate(paper)
                raise
            except Exception as exc:
                paper['ocr_status'] = 'partial' if paper['ocr_pages_completed'] else 'failed'
                paper['ocr_error'] = type(exc).__name__ + ': ' + str(exc)
                traceback.print_exc()
                self.evaluate(paper)
                self.event('OCR ERROR ' + paper['pmcid'] + ' ' + str(exc))
            finally:
                pdf.close()
                self.persist()
        self.state.pop('active_paper', None)

    def report(self):
        rows = []
        exports = self.dest / 'exports'
        exports.mkdir(exist_ok=True)
        papers = self.state['papers']
        fields = ['pmcid', 'journal', 'title', 'pdf_pages', 'native_status', 'ocr_status', 'ocr_pages_completed',
            'figures', 'tables', 'elements_with_referring_paragraphs', 'table_cells_checked', 'matched_labelled_cells',
            'matched_with_header_checks', 'license_code', 'source_pdf', 'source_xml']
        with (exports / 'papers.csv').open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction='ignore')
            writer.writeheader(); writer.writerows(papers)
        for paper in papers:
            directory = 'papers/' + paper['pmcid'] + '/'
            links = '<a href="' + directory + 'source.pdf">PDF</a> · <a href="' + directory + 'source.xml">XML</a> · <a href="' + directory + 'fullpaper_native.md">Native text</a> · <a href="' + directory + 'source_evidence.jsonl">Evidence</a>'
            if (self.dest / directory / 'olmocr_document.json').exists():
                links += ' · <a href="' + directory + 'fullpaper_olmocr.md">OCR text</a> · <a href="' + directory + 'table_checks.json">Table checks</a>'
            values = [paper['pmcid'], paper['journal'], paper['title'], paper['pdf_pages'], paper['ocr_status'],
                str(paper['ocr_pages_completed']) + '/' + str(paper['pdf_pages']),
                str(paper['figures']) + '/' + str(paper['tables']),
                str(paper['matched_labelled_cells']) + '/' + str(paper['table_cells_checked']),
                str(paper['matched_with_header_checks']) + '/' + str(paper['table_cells_checked'])]
            rows.append('<tr>' + ''.join('<td>' + html.escape(str(value)) + '</td>' for value in values) + '<td>' + links + '</td></tr>')
        page = ['<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>PMC biology batch</title>',
            '<style>body{font:16px/1.5 system-ui;max-width:1300px;margin:30px auto;padding:0 20px;color:#14202b}table{border-collapse:collapse;font-size:13px}td,th{border:1px solid #ddd;padding:8px;text-align:left;vertical-align:top}th{background:#eef2f6}.scroll{overflow:auto}.note{color:#506070}a{color:#185bb0}</style>',
            '<h1>PMC biology download and extraction batch</h1><p><strong>Status: ' + html.escape(self.state['status']) + ' / ' + html.escape(self.state.get('stage', '')) + '</strong>. Updated ' + html.escape(self.state.get('updated_at_pst', now())) + ' (fixed PST).</p>',
            '<p>' + str(len(papers)) + '/' + str(self.config['target_papers']) + ' papers downloaded and parsed from JATS; ' + str(self.state.get('ocr_complete_papers', 0)) + ' complete olmOCR 2 papers; ' + str(self.state.get('ocr_pages_completed', 0)) + ' OCR pages retained.</p>',
            '<p>Limits: 1 worker, 1 GPU, ' + str(self.config['maximum_ocr_pages']) + ' OCR pages, 2 GiB new batch artifacts, 1 GiB downloaded response bodies, six hours. Stop by ' + html.escape(self.state['stop_at_pst']) + ' PST. Current artifacts: ' + f"{self.state.get('artifact_bytes', 0) / 2**20:.1f}" + ' MiB; network payload: ' + f"{self.state.get('downloaded_response_bytes', 0) / 2**20:.1f}" + ' MiB.</p>',
            '<p class=note>Selected biology title/abstract markers and research article types; journal-balanced candidate collection with shortest-first whole-paper OCR. Exploratory sample, not representative. Original PDF/XML, versions, licenses and hashes are preserved. XML never enters OCR prompts. Figure interpretation remains unverified. Lookup QA is a deterministic diagnostic; no teacher synthesis or model training was run.</p>',
            '<p><a href="state.json">Live state</a> · <a href="config.json">Exact limits/scope</a> · <a href="exports/papers.csv">Paper manifest CSV</a> · <a href="worker.log">Worker log</a></p>' +
            ('<p><a href="exports/summary.json">Final resource and extraction summary</a></p>' if (exports / 'summary.json').exists() else ''),
            '<div class=scroll><table><thead><tr>' + ''.join('<th>' + h + '</th>' for h in ['PMCID', 'Journal', 'Title', 'PDF pages', 'OCR status', 'OCR pages', 'Figures/tables', 'Matched labelled cells', 'Also passed header checks', 'Files']) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>',
            '<p class=note>Cell checks use source-derived JATS logical tables, fixed row/group labels and column positions, and conservative typography/header checks. Multi-page table assembly and unusual source markup may be unsupported. Missing captions and deferred/partial OCR can lower these diagnostic counts; they are not paper-level scientific validation.</p>',
            '<p>Recent events:</p><ul>' + ''.join('<li>' + html.escape(e['time_pst'] + ' ' + e['message']) + '</li>' for e in self.state['events'][-12:]) + '</ul></html>']
        (self.dest / 'report.html').write_text(''.join(page))

    def finish_exports(self):
        exports = self.dest / 'exports'
        native_text = []
        ocr_text = []
        evidence = []
        demos = []
        for paper in self.state['papers']:
            out = ROOT / paper['source_directory']
            native_text.append(json.dumps(dict(pmcid=paper['pmcid'], source_branch='native_JATS', text_path=str((out / 'fullpaper_native.md').relative_to(ROOT)),
                source_xml=paper['source_xml'], source_xml_sha256=paper['xml_sha256'], license_code=paper['license_code'],
                training_status='Unreviewed candidate export; no training performed'), ensure_ascii=False))
            evidence.append(json.dumps(dict(pmcid=paper['pmcid'], evidence_path=str((out / 'source_evidence.jsonl').relative_to(ROOT))), ensure_ascii=False))
            if (out / 'olmocr_document.json').exists():
                doc = json.loads((out / 'olmocr_document.json').read_text())
                doc.pop('text')
                ocr_text.append(json.dumps(dict(**doc, text_path=str((out / 'fullpaper_olmocr.md').relative_to(ROOT)),
                    license_code=paper['license_code'], training_status='Unreviewed candidate export; no training performed'), ensure_ascii=False))
                demos.append(json.dumps(dict(pmcid=paper['pmcid'], qa_path=str((out / 'lookup_qa_diagnostics.jsonl').relative_to(ROOT))), ensure_ascii=False))
        for name, lines in [('native_fullpapers', native_text), ('olmocr_fullpapers', ocr_text), ('source_evidence_manifest', evidence), ('lookup_qa_manifest', demos)]:
            (exports / (name + '.jsonl')).write_text('\n'.join(lines) + ('\n' if lines else ''))
        pages = []
        for paper in self.state['papers']:
            pages.extend(json.loads(p.read_text()) for p in (ROOT / paper['source_directory'] / 'olmocr').glob('page_*/result.json'))
        finished = [p for p in self.state['papers'] if p.get('ocr_status') == 'completed']
        totals = {name: sum(p.get(name, 0) for p in finished) for name in
            ['table_cells_checked', 'matched_labelled_cells', 'matched_with_header_checks', 'lookup_qa_diagnostics']}
        json_write(exports / 'summary.json', dict(
            status=self.state['status'], updated_at_pst=now(), stop_at_pst=self.state['stop_at_pst'],
            downloaded_and_native_parsed_papers=len(self.state['papers']),
            journal_counts=dict(Counter(p['journal'] for p in self.state['papers'])),
            source_pdf_pages=sum(p['pdf_pages'] for p in self.state['papers']),
            complete_ocr_papers=len(finished), ocr_status_counts=dict(Counter(p['ocr_status'] for p in self.state['papers'])),
            retained_ocr_pages=len(pages), page_status_counts=dict(Counter(p['status'] for p in pages)),
            page_inference_seconds=round(sum(p.get('elapsed_seconds', 0) for p in pages), 3),
            maximum_peak_gpu_allocated_gib=max((p.get('peak_gpu_allocated_gib', 0) for p in pages), default=0),
            source_figures=sum(p['figures'] for p in self.state['papers']),
            source_tables=sum(p['tables'] for p in self.state['papers']),
            source_elements_with_referring_paragraphs=sum(p['elements_with_referring_paragraphs'] for p in self.state['papers']),
            complete_paper_table_diagnostics=totals, downloaded_response_bytes=self.state['downloaded_response_bytes'],
            artifact_bytes=self.size(), model=self.config['model'], model_revision=self.config['model_revision'],
            evaluation_note='Exploratory source-derived table checks, not an independently annotated benchmark; figures unverified.',
            limitations=['Table adapter may not support split/multipage tables or unusual markup.',
                'Complete OCR means all PDF pages reached model EOS; semantic completeness is unverified.',
                'Selected biology starter corpus, not a representative or exhaustive CNS sample.']))

    def run(self, native_only=False):
        try:
            self.acquire()
            if not self.state['papers']:
                raise RuntimeError('No eligible biology papers were acquired')
            if self.state['papers'] and not native_only:
                self.ocr()
            self.state.update(status='completed', stage='finished', finished_at_pst=now())
        except LimitReached as exc:
            self.state.update(status='limited', stage='finished', limit_reason=str(exc), finished_at_pst=now())
            print('LIMIT ' + str(exc), flush=True)
        except Exception as exc:
            self.state.update(status='failed', error=type(exc).__name__ + ': ' + str(exc), finished_at_pst=now())
            traceback.print_exc()
        finally:
            raster = self.dest / 'temporary_page.png'
            if raster.exists():
                raster.unlink()
            self.finish_exports()
            self.persist()
            print(json.dumps({key: self.state.get(key) for key in ['status', 'native_parsed_papers', 'ocr_complete_papers', 'ocr_pages_completed', 'artifact_bytes', 'limit_reason', 'error']}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=str(ROOT / 'config/pmc_overnight_2026-10-14.json'))
    parser.add_argument('--native-only', action='store_true')
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text())
    if config['document_workers'] != 1 or config['cpu_threads'] != 2:
        raise ValueError('This batch must retain the authorized one-worker/two-CPU-thread limits')
    batch = Batch(config)
    batch.run(args.native_only)
    if batch.state['status'] == 'failed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
