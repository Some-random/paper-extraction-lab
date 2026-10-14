"""Count a defined CNS journal corpus with sequential official PMC ESearch calls.

This inventories search matches, not successful downloads. PDF object presence
must subsequently be checked in the official S3 article-version metadata.
"""
import argparse
import csv
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'reports/pmc_cns_availability_2026-10-13'
API = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
PST = timezone(timedelta(hours=-8))
FILTERS = {
    'pmc_public_records': '',
    'xml_text_mining_candidates': ' AND (open_access[filter] OR author_manuscript[filter])',
    'open_access_candidates': ' AND open_access[filter]',
    'open_access_with_pdf_candidates': ' AND open_access[filter] AND "has pdf"[filter]',
}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def journal_query(names, aliases=None):
    # Explicit journal field and quoted names avoid body/reference/title matches.
    aliases = aliases or {}
    names = [alias for name in names for alias in aliases.get(name, [name])]
    return '(' + ' OR '.join('"' + ' '.join(name.replace('&', '').split()) + '"[journal]' for name in sorted(set(names))) + ')'


def search(query, sample_size=0):
    token = hashlib.sha256((query + ':' + str(sample_size)).encode()).hexdigest()
    cache = DEST / 'api' / (token + '.json')
    if cache.exists():
        return json.loads(cache.read_text())
    url = API + '?' + urllib.parse.urlencode(dict(db='pmc', term=query,
        retmode='json', retmax=sample_size, tool='paper_extraction_lab'))
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'paper-extraction-lab/0.1 (sequential PMC availability inventory)'})
            with urllib.request.urlopen(req, timeout=40) as response:
                raw = json.load(response)
            result = raw['esearchresult']
            if 'error' in raw or 'error' in result:
                raise RuntimeError(json.dumps(raw))
            if result.get('warninglist', {}).get('quotedphrasesnotfound') or result.get('errorlist'):
                raise RuntimeError('Resolve journal/query warnings before reporting counts: ' + json.dumps(result))
            record = dict(query=query, url=url, checked_at_pst=datetime.now(PST).isoformat(),
                          count=int(result['count']), response=raw)
            write_json(cache, record)
            time.sleep(0.4)
            return record
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == 2:
                raise
            print('API retry: ' + str(exc), flush=True)
            time.sleep(2 + attempt * 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--flagships-only', action='store_true')
    args = parser.parse_args()
    scope = json.loads((ROOT / 'config/pmc_cns_scope.json').read_text())
    rows = [dict(label=j['name'], scope='flagship', names=j['aliases']) for j in scope['flagships']]
    flagship_names = [n for j in scope['flagships'] for n in j['aliases']]
    rows.append(dict(label='Flagships combined', scope='flagship_union', names=flagship_names))
    if not args.flagships_only:
        rows.extend(dict(label=j['name'], scope='related_example', names=j['aliases']) for j in scope['examples'])
        rows.extend(dict(label=name, scope='curated_related_set', names=names) for name, names in scope['related_sets'].items())
        all_names = flagship_names + [n for names in scope['related_sets'].values() for n in names]
        rows.append(dict(label='Selected related journals combined', scope='curated_related_union', names=all_names))
        rows.append(dict(label='Selected related journals excluding Scientific Reports',
            scope='curated_related_union_without_scientific_reports',
            names=[name for name in all_names if name != 'Scientific Reports']))
    report = dict(started_at_pst=datetime.now(PST).isoformat(), source=API,
        scope_definition=scope, definitions={
            'pmc_public_records': 'PMC search matches excluding embargoed records; includes author manuscripts and multiple article types.',
            'xml_text_mining_candidates': 'Public PMC matches in the OA subset or Author Manuscript Dataset, eligible for the official XML/text retrieval route.',
            'open_access_candidates': 'Public PMC matches in the Open Access Subset; licenses vary.',
            'open_access_with_pdf_candidates': 'OA subset plus the PMC has-PDF filter; candidate count, not an object-verified download count.',
        }, limitations=[
            'Search matches are not confirmed file downloads. Validate S3 versions and their xml_url/pdf_url/media_urls before ingestion.',
            'Author manuscripts without CC licenses have XML/text but not PDF/media/supplemental objects in the official distribution.',
            'Deduplicate by PMCID/DOI and distinguish accepted manuscripts from final published versions.',
            'Related journal lists are explicit, curated targets rather than an exhaustive publisher catalogue.',
            'No biology-only, original-research-only, retraction or correction exclusions were applied to these availability counts.',
        ], rows=[])
    for row in rows:
        item = {**row, 'queries': {}}
        base = journal_query(row['names'], scope.get('journal_query_aliases')) + ' NOT "pmc embargo"[filter]'
        for key, suffix in FILTERS.items():
            result = search('(' + base + ')' + suffix)
            item[key] = result['count']
            item['queries'][key] = {k: result[k] for k in ['query', 'url', 'checked_at_pst']}
            print(row['label'] + ' | ' + key + ' = ' + str(result['count']), flush=True)
        assert item['open_access_with_pdf_candidates'] <= item['open_access_candidates'] <= item['xml_text_mining_candidates'] <= item['pmc_public_records']
        report['rows'].append(item)
        write_json(DEST / 'availability.json', report)
    report['completed_at_pst'] = datetime.now(PST).isoformat()
    write_json(DEST / 'availability.json', report)
    with (DEST / 'availability.csv').open('w', newline='') as output:
        fields = ['label', 'scope'] + list(FILTERS)
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(report['rows'])
    print('Saved ' + str(DEST / 'availability.json'), flush=True)


if __name__ == '__main__':
    main()
