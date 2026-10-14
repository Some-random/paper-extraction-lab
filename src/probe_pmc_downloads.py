"""Verify a few official PMC S3 PDF/XML downloads, sequentially and without OCR."""
import hashlib
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from inventory_pmc_cns import DEST, PST, ROOT, journal_query, search, write_json

S3 = 'https://pmc-oa-opendata.s3.amazonaws.com'


def get_bytes(url):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme == 's3':
        # Official metadata uses s3:// URLs; anonymous HTTPS is also supported.
        url = urllib.parse.urlunsplit(('https', parts.netloc + '.s3.amazonaws.com',
            urllib.parse.quote(urllib.parse.unquote(parts.path), safe='/'), parts.query, ''))
    request = urllib.request.Request(url, headers={'User-Agent': 'paper-extraction-lab/0.1 (sequential PMC download verification)'})
    with urllib.request.urlopen(request, timeout=40) as response:
        return response.read()


def metadata_for(pmcid):
    cached = DEST / 'download_probe' / pmcid / 'metadata.json'
    if cached.exists():
        raw = cached.read_bytes()
        metadata = json.loads(raw)
        return [(metadata, raw, S3 + '/metadata/' + pmcid + '.' + str(metadata['version']) + '.json')]
    url = S3 + '/?' + urllib.parse.urlencode({'list-type': 2, 'prefix': 'metadata/' + pmcid + '.'})
    listing = ET.fromstring(get_bytes(url))
    keys = [node.text for node in listing.findall('.//{*}Key') if node.text.endswith('.json')]
    records = []
    for key in keys:
        raw = get_bytes(S3 + '/' + key)
        metadata = json.loads(raw)
        records.append((metadata, raw, S3 + '/' + key))
    # Prefer publisher version when available, then a version with a PDF.
    return sorted(records, key=lambda item: (str(item[0].get('is_manuscript')).lower() in ['yes', 'true', '1'],
        not bool(item[0].get('pdf_url')), -int(item[0].get('version', 1))))


def pdf_pages(path):
    import pypdfium2
    doc = pypdfium2.PdfDocument(str(path))
    pages = len(doc)
    doc.close()
    return pages


def main():
    previous = DEST / 'download_probe.json'
    archive = DEST / 'download_probe_url_adapter_initial.json'
    if previous.exists() and not archive.exists():
        archive.write_bytes(previous.read_bytes())
    scope = json.loads((ROOT / 'config/pmc_cns_scope.json').read_text())
    targets = scope['flagships'] + [j for j in scope['examples'] if j['name'] != 'Scientific Reports']
    report = {'checked_at_pst': datetime.now(PST).isoformat(),
        'purpose': 'Availability verification of actual files; no OCR inference or representative biology sampling.',
        'document_workers': 1, 'records': [], 'attempts': []}
    for journal in targets:
        query = journal_query(journal['aliases']) + ' AND open_access[filter] AND "has pdf"[filter] AND hasabstract NOT "pmc embargo"[filter]'
        candidates = search(query, sample_size=3)['response']['esearchresult']['idlist']
        for uid in candidates:
            pmcid = 'PMC' + uid
            try:
                options = metadata_for(pmcid)
                chosen = next((item for item in options if item[0].get('pdf_url') and item[0].get('xml_url')), None)
                if chosen is None:
                    report['attempts'].append({'journal': journal['name'], 'pmcid': pmcid,
                        'status': 'No official metadata version with both PDF and XML objects'})
                    continue
                metadata, raw_meta, meta_url = chosen
                out = DEST / 'download_probe' / pmcid
                out.mkdir(parents=True, exist_ok=True)
                (out / 'metadata.json').write_bytes(raw_meta)
                raw_pdf = get_bytes(metadata['pdf_url'])
                assert raw_pdf.startswith(b'%PDF-'), 'Downloaded object is not a PDF'
                (out / 'source.pdf').write_bytes(raw_pdf)
                raw_xml = get_bytes(metadata['xml_url'])
                xml = ET.fromstring(raw_xml)
                assert xml.tag.rsplit('}', 1)[-1] == 'article'
                (out / 'source.xml').write_bytes(raw_xml)
                item = {'journal': journal['name'], 'pmcid': pmcid, 'doi': metadata.get('doi'),
                    'title': metadata.get('title'), 'citation': metadata.get('citation'),
                    'version': metadata.get('version'), 'is_manuscript': metadata.get('is_manuscript'),
                    'license_code': metadata.get('license_code'), 'metadata_url': meta_url,
                    'pdf_url': metadata['pdf_url'], 'xml_url': metadata['xml_url'],
                    'pdf_bytes': len(raw_pdf), 'xml_bytes': len(raw_xml),
                    'pdf_pages': pdf_pages(out / 'source.pdf'),
                    'article_type': xml.get('article-type'),
                    'pdf_sha256': hashlib.sha256(raw_pdf).hexdigest(),
                    'xml_sha256': hashlib.sha256(raw_xml).hexdigest(),
                    'local_directory': str(out.relative_to(ROOT)), 'download_status': 'verified',
                    'ocr_status': 'not_run'}
                report['records'].append(item)
                print(json.dumps({k: item[k] for k in ['journal', 'pmcid', 'pdf_pages', 'license_code', 'article_type', 'download_status']}), flush=True)
                break
            except Exception as exc:
                report['attempts'].append({'journal': journal['name'], 'pmcid': pmcid,
                    'status': type(exc).__name__ + ': ' + str(exc)})
                print('Download probe: ' + journal['name'] + ' ' + pmcid + ' ' + str(exc), flush=True)
        write_json(DEST / 'download_probe.json', report)
    report['completed_at_pst'] = datetime.now(PST).isoformat()
    report['journals_verified'] = len(report['records'])
    report['journals_requested'] = len(targets)
    write_json(DEST / 'download_probe.json', report)


if __name__ == '__main__':
    main()
