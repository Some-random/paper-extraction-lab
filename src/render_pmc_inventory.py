"""Render the PMC availability count, file probes and capacity scenarios offline."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'reports/pmc_cns_availability_2026-10-13'


def esc(value):
    return html.escape(str(value))


def main():
    report = json.loads((DEST / 'availability.json').read_text())
    probe = json.loads((DEST / 'download_probe.json').read_text())
    capacity = json.loads((DEST / 'capacity.json').read_text())
    group = next(row for row in report['rows'] if row['scope'] == 'curated_related_union')
    compact = next(row for row in report['rows'] if row['scope'] == 'curated_related_union_without_scientific_reports')
    body = []
    for row in report['rows']:
        label = '<a href="' + esc(row['queries']['pmc_public_records']['url']) + '">' + esc(row['label']) + '</a>'
        cells = [label] + [f"{row[key]:,}" for key in ['pmc_public_records', 'xml_text_mining_candidates', 'open_access_candidates', 'open_access_with_pdf_candidates']]
        body.append('<tr>' + ''.join('<td>' + value + '</td>' for value in cells) + '</tr>')
    files = []
    for row in probe['records']:
        directory = Path(row['local_directory']).relative_to(DEST.relative_to(ROOT))
        values = [esc(row['journal']), esc(row['pmcid']), esc(row['article_type']), str(row['pdf_pages']),
            esc(row['license_code']), 'accepted manuscript' if row['is_manuscript'] else 'publisher version',
            '<a href="' + esc(directory / 'source.pdf') + '">PDF</a> · <a href="' + esc(directory / 'source.xml') + '">XML</a> · <a href="' + esc(directory / 'metadata.json') + '">Metadata</a>']
        files.append('<tr>' + ''.join('<td>' + value + '</td>' for value in values) + '</tr>')
    scenarios = []
    for row in capacity['compute_scenarios']:
        values = [row['assumed_pages_per_paper'], round(row['papers_per_24_gpu_hours']), round(row['gpu_hours_per_1000_papers'], 1)]
        scenarios.append('<tr>' + ''.join('<td>' + esc(value) + '</td>' for value in values) + '</tr>')
    def table(headings, rows):
        return '<div class=scroll><table><thead><tr>' + ''.join('<th>' + esc(h) + '</th>' for h in headings) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
    content = [
        '<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>PMC CNS corpus availability</title>',
        '<style>body{font:16px/1.55 system-ui;max-width:1180px;margin:32px auto;padding:0 20px;color:#14202b;background:#f7f8fa}h1,h2{line-height:1.25}table{border-collapse:collapse;background:white;font-size:14px}th,td{padding:9px;border:1px solid #dce0e4;text-align:left;vertical-align:top}th{background:#edf1f5}.scroll{overflow:auto}a{color:#185bb0}.note{color:#46515e;font-size:14px}</style>',
        '<h1>PMC CNS corpus availability</h1>',
        '<p><strong>' + f"{group['open_access_with_pdf_candidates']:,}" + ' open-access PDF candidates</strong> across a selected set of 55 journal titles, including a historical predecessor. The user selected related journals as well as Cell, Nature and Science. These sets do not exhaust the publishers’ catalogues.</p>',
        '<p>Excluding Scientific Reports gives ' + f"{compact['open_access_with_pdf_candidates']:,}" + ' PDF candidates. This count has no biology-only or original-research-only filter; reviews, corrections and other article types can appear.</p>',
        '<p class=note>Official PMC ESearch counts checked October 13, 2026. Embargoed records are excluded. Counts were queried sequentially, so index updates can cause small differences between family sums and separately queried Boolean unions.</p>',
        table(['Journal / defined target set', 'Public PMC records', 'XML/text-mining candidates', 'OA subset candidates', 'OA + has-PDF candidates'], body),
        '<p>The XML/text-mining column uses open_access OR author_manuscript. The PDF column uses open_access AND has-PDF. It is a search-derived candidate count; each article version and its actual PDF object must be checked during ingestion. Non-CC author manuscripts are distributed as XML/text without PDF/media in the official dataset. <a href="https://pmc.ncbi.nlm.nih.gov/tools/cloud/">PMC file availability</a>.</p>',
        '<p><a href="availability.csv">Counts CSV</a> · <a href="availability.json">Counts, exact queries and scope</a> · <a href="capacity.json">Capacity assumptions</a></p>',
        '<h2>Actual file checks</h2><p>Six PDF/XML pairs were downloaded from the official PMC S3 dataset and checked against their recorded SHA256 and metadata MD5 hashes. These were availability probes. No OCR inference was run on them.</p>',
        table(['Journal', 'PMCID', 'Article type', 'PDF pages', 'License', 'Version type', 'Original files'], files),
        '<p><a href="download_probe.json">Download provenance and checks</a> · <a href="set_overlap_checks.json">Journal-set overlap checks</a></p>',
        '<h2>Single-GPU capacity scenarios</h2><p>The existing nine-page diagnostic took 150.412 seconds on one H200 using the sequential Transformers BF16 runner: about 16.7 seconds/page. Extrapolations below exclude downloads, retries, initialization and downstream QA. They are planning scenarios, not measured whole-paper throughput.</p>',
        table(['Assumed pages / paper', 'Papers / 24 GPU hours', 'GPU hours / 1,000 papers'], scenarios),
        '<p>The shared /data/rustfs1 filesystem currently has approximately ' + str(round(capacity['filesystem']['available_gib'])) + ' GiB free; this is not reserved space. At an assumed 5 MB/PDF, the ' + f"{group['open_access_with_pdf_candidates']:,}" + '-paper pool requires about ' + f"{group['open_access_with_pdf_candidates'] * 5_000_000 / 10**12:.2f}" + ' TB for PDFs alone, before XML, media and outputs.</p>',
        '<p>Large-scale processing requires a storage plan and a measured serving benchmark. Keep source XML alongside PDFs for independent validation of olmOCR 2 output, retain paper versions and licenses, and preserve the frozen nine-page comparison separately.</p></html>'
    ]
    (DEST / 'index.html').write_text(''.join(content))
    print(str(DEST / 'index.html'))


if __name__ == '__main__':
    main()
