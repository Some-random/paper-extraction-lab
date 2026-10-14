"""Build a portable reader and small review samples without changing extraction outputs."""
import argparse
import hashlib
import json
import re
import urllib.parse
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ['PMC13645648', 'PMC13655163', 'PMC13651886']


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def public_url(url):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme == 's3':
        return urllib.parse.urlunsplit(('https', parts.netloc + '.s3.amazonaws.com', parts.path, parts.query, ''))
    return url


def build(batch):
    source = ROOT / 'experiments' / batch
    report = ROOT / 'reports' / batch
    report.mkdir(exist_ok=True)
    state = json.loads((source / 'state.json').read_text())
    summary = json.loads((source / 'exports/summary.json').read_text())
    seconds = summary['page_inference_seconds'] / summary['retained_ocr_pages']
    mean_pages = summary['source_pdf_pages'] / len(state['papers'])
    download_minutes = (max(datetime.fromisoformat(p['acquired_at_pst']) for p in state['papers']) -
                        datetime.fromisoformat(state['started_at_pst'])).total_seconds() / 60
    scaling = dict(target_papers=500, observed_papers=len(state['papers']),
        measured_ocr_seconds_per_page=seconds, observed_source_pdf_pages_per_paper=mean_pages,
        estimated_source_pdf_pages=500 * mean_pages,
        estimated_ocr_hours_one_gpu=500 * mean_pages * seconds / 3600,
        observed_download_and_xml_minutes_including_debugging=download_minutes,
        linear_download_and_xml_hours=download_minutes * 10 / 60,
        batch_artifact_gib_times_ten=summary['artifact_bytes'] * 10 / 2**30,
        download_gib_times_ten=summary['downloaded_response_bytes'] * 10 / 2**30,
        assumptions=['Same hardware, one worker, similar article lengths and the current file/page filters.',
            'OCR processed the shorter papers first; the unprocessed pages may have different runtimes.',
            'Storage extrapolation reflects 1,000 OCR pages per 50 downloads; full OCR adds more output.',
            'Cached model weights are reused, not multiplied by the number of papers.',
            'Projection only; this does not launch or authorize a 500-paper run.'])
    save_json(report / 'scaling_estimate.json', scaling)
    categories = Counter()
    audited = []
    papers = []
    for record in state['papers']:
        out = ROOT / record['source_directory']
        native = json.loads((out / 'native_document.json').read_text())
        checks_path = out / 'table_checks.json'
        checks = json.loads(checks_path.read_text())['checks'] if checks_path.exists() else []
        for check in checks:
            if record['ocr_status'] != 'completed':
                continue
            if check['candidate_page'] is not None:
                category = 'bound_to_generated_table'
            elif re.search(r'(?:Table|Figure|Fig\.?)\s*([Ss]?\d+[A-Za-z]?)', check['label'], re.I):
                category = 'numeric_source_label_not_bound'
            else:
                category = 'source_label_missing_or_non_numeric'
            categories[category + '_tables'] += 1
            categories[category + '_cells'] += check['total']
            audited.append(dict(pmcid=record['pmcid'], category=category,
                label=check['label'], source_cells=check['total'], matched_cells=check['matched'],
                candidate_page=check['candidate_page']))
        qa_path = out / 'lookup_qa_diagnostics.jsonl'
        qa = [json.loads(line) for line in qa_path.read_text().splitlines()] if qa_path.exists() else []
        ocr_path = out / 'fullpaper_olmocr.md'
        evidence = [dict(kind=e['kind'], label=e['label'], caption=e['caption'],
            notes=e.get('notes', ''), table_html=e.get('table_html', ''),
            referring_paragraphs=[p['text'] for p in e['referring_paragraphs']],
            quality_flags=e['quality_flags'], source_xpath=e['source_xpath']) for e in native['evidence']]
        paper = dict(**record, source_pdf_url=public_url(record['pdf_url']),
            pmc_url='https://pmc.ncbi.nlm.nih.gov/articles/' + record['pmcid'] + '/',
            native_text=(out / 'fullpaper_native.md').read_text(),
            ocr_text=ocr_path.read_text() if ocr_path.exists() else '',
            evidence=evidence, checks=checks, qa=qa)
        papers.append(paper)
        if record['pmcid'] in SAMPLES:
            if record['license_code'] != 'CC BY':
                raise ValueError('Review samples are selected from CC BY articles: ' + record['pmcid'])
            sample = report / 'samples' / record['pmcid']
            sample.mkdir(parents=True, exist_ok=True)
            provenance = {key: record.get(key) for key in ['pmcid', 'title', 'journal', 'doi',
                'license_code', 'version', 'is_manuscript', 'pdf_sha256', 'xml_sha256',
                'metadata_url', 'pdf_pages', 'ocr_status']}
            provenance.update(pmc_url=paper['pmc_url'], source_pdf_url=paper['source_pdf_url'],
                note='Byte-identical derived-text copies for review; original PDF/XML and page outputs remain on RustFS.',
                files={})
            tree = etree.parse(str(out / 'source.xml'), etree.XMLParser(resolve_entities=False, no_network=True))
            provenance['authors'] = []
            for name in tree.xpath('//*[local-name()="contrib"][@contrib-type="author"]/*[local-name()="name"]'):
                given = ''.join(name.xpath('./*[local-name()="given-names"]/text()'))
                family = ''.join(name.xpath('./*[local-name()="surname"]/text()'))
                provenance['authors'].append((given + ' ' + family).strip())
            provenance['license_statements'] = [' '.join(n.itertext()).strip() for n in tree.xpath('//*[local-name()="license"]')]
            for filename in ['fullpaper_native.md', 'fullpaper_olmocr.md']:
                raw = (out / filename).read_bytes()
                (sample / filename).write_bytes(raw)
                assert (sample / filename).read_bytes() == raw
                provenance['files'][filename] = dict(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
            save_json(sample / 'provenance.json', provenance)
    audit = dict(source='Original, unchanged per-paper table_checks.json for complete OCR papers.',
        original_matched_cells=summary['complete_paper_table_diagnostics']['matched_labelled_cells'],
        original_checked_cells=summary['complete_paper_table_diagnostics']['table_cells_checked'],
        categories=dict(categories), tables=audited,
        findings=['The original matcher requires a period/colon after a numeric caption label.',
            'Observed generated captions include Table 1 | ... and Table 1 (continued) | ...; these are not bound.',
            'Missing source labels and KEY RESOURCES TABLE are unsupported by the numeric-label matcher.',
            'Of 1,211 source cells, 1,072 had no linked generated table; 91 of the remaining 139 passed the strict value and header checks.',
            'This is an audit of the existing score, not a repaired score or a general OCR accuracy estimate.',
            'No model output, source value or existing metric result was changed.'])
    save_json(report / 'table_diagnostic_audit.json', audit)
    payload = json.dumps(dict(summary=summary, scaling=scaling, audit=audit, papers=papers), ensure_ascii=False)
    payload = payload.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    page = HTML.replace('__DATA__', payload)
    (source / 'review.html').write_text(page)
    with zipfile.ZipFile(source / 'paper_review.zip', 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('review.html', page)
        archive.write(source / 'exports/papers.csv', 'papers.csv')
        archive.write(source / 'exports/summary.json', 'summary.json')
        archive.write(report / 'table_diagnostic_audit.json', 'table_diagnostic_audit.json')
        archive.write(report / 'scaling_estimate.json', 'scaling_estimate.json')
    print(json.dumps(dict(papers=len(papers), ocr_documents=sum(bool(p['ocr_text']) for p in papers),
        qa_examples=sum(len(p['qa']) for p in papers), audit=dict(categories),
        review_html_bytes=(source / 'review.html').stat().st_size,
        review_zip_bytes=(source / 'paper_review.zip').stat().st_size,
        estimated_500_paper_gpu_hours=scaling['estimated_ocr_hours_one_gpu']), indent=2))


HTML = r'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Review 50 biology papers</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f6f7f9;color:#1c2938;font:15px/1.55 system-ui,sans-serif}
header{background:#142b44;color:white;padding:24px 30px}h1{margin:0;font-size:27px}header p{margin:7px 0 0}
.layout{display:grid;grid-template-columns:320px minmax(0,1fr);gap:20px;padding:22px;max-width:1550px;margin:auto}
aside,main{background:white;border:1px solid #dbe1e8;border-radius:8px;padding:18px;min-width:0}
aside input,aside select{width:100%;padding:9px;margin-bottom:10px;font:inherit}#papers{height:420px;font-size:13px}
.tabs{display:flex;gap:7px;flex-wrap:wrap;margin:18px 0}.tabs button{background:#eef2f6;border:1px solid #bbc7d4;border-radius:5px;padding:9px 12px;cursor:pointer}
.tabs button.active{background:#175ba4;color:white}.pane{display:none}.pane.active{display:block}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.65 ui-monospace,monospace;background:#f7f9fb;padding:15px;border:1px solid #e1e6ec}
a{color:#125ba4}header a{color:#c5e3ff}.meta,.note{color:#566779}.notice{background:#fff5dc;padding:12px;border-left:4px solid #c48c00}
details{margin:12px 0;border:1px solid #dbe1e8;border-radius:5px;padding:12px}summary{cursor:pointer;font-weight:600}
table{border-collapse:collapse;width:100%;font-size:13px;margin:10px 0}th,td{border:1px solid #ccd6e0;padding:7px;text-align:left;vertical-align:top}th{background:#edf2f7}.table-wrap{overflow:auto}
.context{padding:10px;border-left:3px solid #b9c9da;background:#f6f8fa}h2{line-height:1.35;margin-top:0}
@media(max-width:850px){.layout{grid-template-columns:1fr;padding:10px}#papers{height:160px}header{padding:20px}}
</style></head><body><header><h1>50 biology papers: extraction review</h1>
<p>50 XML parses · 37 complete OCR papers · 1 partial · 12 deferred · 1,000 OCR pages</p>
<p>Everything below is embedded in this file. Original PDF / PMC links open the official source online.</p></header>
<div class="layout"><aside><label for="search">Search title, journal or PMCID</label><input id="search" placeholder="e.g. Nature, Wnt, PMC13655163">
<label for="status">OCR status</label><select id="status"><option value="">All papers</option><option>completed</option><option>partial</option><option>deferred_page_budget</option></select>
<select id="papers" size="18" aria-label="Select a paper"></select><p id="count" class="meta"></p>
<p class="notice">OCR completion means every page finished generating. Scientific accuracy and figure interpretation remain unverified.</p>
<p>500 similar papers: about <strong>3–5 GiB</strong> of batch artifacts and <strong>53 GPU hours</strong> for full OCR, plus downloading/XML parsing. These are extrapolations on the same hardware.</p>
<details><summary>Why the table score is low</summary><p>The existing caption matcher linked only 4 of 18 checked source tables. 1,072 of 1,211 source cells had no linked generated table. Of the 139 linked cells, 91 passed strict value/header checks.</p>
<p>The matcher misses captions such as “Table 1 | …” and unnumbered resource tables. The original results are preserved; this is not a general OCR accuracy score.</p></details></aside>
<main><h2 id="title"></h2><p id="meta" class="meta"></p><p id="links"></p><p id="paper-note" class="notice"></p>
<nav class="tabs"><button data-tab="ocr" class="active">olmOCR text</button><button data-tab="native">PMC XML text</button><button data-tab="evidence">Tables, captions & context</button><button data-tab="checks">Table checks</button><button data-tab="qa">Lookup QA</button></nav>
<section id="ocr" class="pane active"></section><section id="native" class="pane"></section><section id="evidence" class="pane"></section><section id="checks" class="pane"></section><section id="qa" class="pane"></section>
</main></div><script id="data" type="application/json">__DATA__</script><script>
'use strict';
const DATA=JSON.parse(document.getElementById('data').textContent);
const byId=id=>document.getElementById(id);
function el(tag,text,cls){const node=document.createElement(tag);if(text!==undefined)node.textContent=text;if(cls)node.className=cls;return node;}
function paragraph(parent,text,cls){parent.appendChild(el('p',text,cls));}
function tableHTML(raw){const wrap=el('div',undefined,'table-wrap');const parsed=new DOMParser().parseFromString(raw,'text/html');
 const allowed=new Set(['TABLE','THEAD','TBODY','TFOOT','TR','TH','TD','CAPTION','COLGROUP','COL','SUP','SUB','I','B','EM','STRONG','BR','P','SPAN']);
 function copy(node){if(node.nodeType===3)return document.createTextNode(node.textContent);if(node.nodeType!==1)return document.createDocumentFragment();
  if(['SCRIPT','STYLE','IFRAME','OBJECT','IMG','LINK'].includes(node.tagName))return document.createDocumentFragment();
  const clean=allowed.has(node.tagName)?document.createElement(node.tagName.toLowerCase()):document.createDocumentFragment();
  if(clean.nodeType===1)for(const key of ['rowspan','colspan'])if(/^\d+$/.test(node.getAttribute(key)||''))clean.setAttribute(key,node.getAttribute(key));
  for(const child of node.childNodes)clean.appendChild(copy(child));return clean;}
 for(const child of parsed.body.childNodes)wrap.appendChild(copy(child));return wrap;}
function sourceLink(parent,label,url){const a=el('a',label);a.href=url;a.target='_blank';a.rel='noopener';parent.appendChild(a);parent.appendChild(document.createTextNode('  ·  '));}
function show(id){const p=DATA.papers.find(p=>p.pmcid===id);if(!p)return;
 byId('title').textContent=p.title;byId('meta').textContent=p.pmcid+' · '+p.journal+' · '+p.pdf_pages+' PDF pages · '+p.license_code;
 byId('links').replaceChildren();sourceLink(byId('links'),'Original PDF',p.source_pdf_url);sourceLink(byId('links'),'PMC article / attribution',p.pmc_url);if(p.doi)sourceLink(byId('links'),'DOI','https://doi.org/'+p.doi);
 byId('paper-note').textContent='OCR: '+p.ocr_status+' ('+p.ocr_pages_completed+'/'+p.pdf_pages+' pages attempted). '+p.figures+' source figures, '+p.tables+' source tables. Captions and referring paragraphs below come from JATS; XML was never in the OCR prompt.';
 byId('ocr').replaceChildren(el('pre',p.ocr_text||'OCR was deferred by the page budget. The complete native XML text is available in the next tab.'));
 byId('native').replaceChildren(el('pre',p.native_text));
 byId('evidence').replaceChildren();
 for(const e of p.evidence){const d=el('details');d.appendChild(el('summary',(e.label||'Unnumbered '+e.kind)+' · '+e.kind));paragraph(d,e.caption);if(e.table_html)d.appendChild(tableHTML(e.table_html));if(e.notes)paragraph(d,e.notes);
  if(e.kind==='figure')paragraph(d,'The figure itself is in the original PDF. No visual interpretation was validated.','notice');
  paragraph(d,'Explicitly referring source paragraphs: '+e.referring_paragraphs.length,'meta');for(const text of e.referring_paragraphs)paragraph(d,text,'context');paragraph(d,'Source XML: '+e.source_xpath,'meta');if(e.quality_flags.length)paragraph(d,e.quality_flags.join('; '),'note');byId('evidence').appendChild(d);}
 if(!p.evidence.length)paragraph(byId('evidence'),'No figure/table elements found in the source XML.');
 byId('checks').replaceChildren();paragraph(byId('checks'),'These are the original, unchanged diagnostics. An unbound table has no transcription comparison, even though the original end-to-end denominator includes its source cells.','notice');
 for(const c of p.checks){const d=el('details');d.appendChild(el('summary',(c.label||'Unnumbered table')+' · '+c.matched+'/'+c.total+' matched · '+(c.candidate_page===null?'no generated table linked':'PDF page '+c.candidate_page)));
  paragraph(d,'Passed value + header checks: '+c.with_header_checks+'. '+(c.error||''));if(c.binding)paragraph(d,'Caption binding: '+c.binding.text);
  if(c.cells&&c.cells.length){const t=el('table');const tr=el('tr');for(const label of ['Row','Column/header','Source value','OCR value','Value + header pass'])tr.appendChild(el('th',label));t.appendChild(tr);
   for(const cell of c.cells){const row=el('tr');for(const text of [cell.row_key,cell.header,cell.expected,cell.actual===null?'(missing)':cell.actual,cell.quantity_and_value_matched?'yes':'no'])row.appendChild(el('td',String(text)));t.appendChild(row);}const wrap=el('div',undefined,'table-wrap');wrap.appendChild(t);d.appendChild(wrap);}byId('checks').appendChild(d);}
 if(!p.checks.length)paragraph(byId('checks'),'No scored source-table checks for this paper. See evidence quality flags and OCR status.');
 byId('qa').replaceChildren();paragraph(byId('qa'),'Deterministic source-table lookup diagnostics with OCR value/header agreement. These are not teacher reasoning or an approved training dataset.','notice');
 for(const q of p.qa){const d=el('details');d.appendChild(el('summary',q.question));paragraph(d,q.answer);paragraph(d,'Evidence: '+q.evidence_id+' · PDF page '+q.source_page,'meta');paragraph(d,q.caption);for(const ref of q.referring_paragraphs)paragraph(d,ref.text,'context');byId('qa').appendChild(d);}
 if(!p.qa.length)paragraph(byId('qa'),'No lookup QA passed the current diagnostic gate for this paper.');}
function filter(){const query=byId('search').value.trim().toLowerCase();const status=byId('status').value;const previous=byId('papers').value;
 const rows=DATA.papers.filter(p=>(!status||p.ocr_status===status)&&(!query||(p.title+' '+p.journal+' '+p.pmcid).toLowerCase().includes(query)));
 byId('papers').replaceChildren();for(const p of rows){const o=el('option',p.pmcid+' · '+p.title);o.value=p.pmcid;byId('papers').appendChild(o);}byId('count').textContent=rows.length+' / '+DATA.papers.length+' papers';
 if(rows.length){byId('papers').value=rows.some(p=>p.pmcid===previous)?previous:rows[0].pmcid;show(byId('papers').value);}}
byId('papers').addEventListener('change',()=>show(byId('papers').value));byId('search').addEventListener('input',filter);byId('status').addEventListener('change',filter);
for(const button of document.querySelectorAll('[data-tab]'))button.addEventListener('click',()=>{for(const b of document.querySelectorAll('[data-tab]'))b.classList.toggle('active',b===button);for(const section of document.querySelectorAll('.pane'))section.classList.toggle('active',section.id===button.dataset.tab);});
filter();byId('papers').value='PMC13651886';show('PMC13651886');
</script></body></html>'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', default='pmc_cns_biology_2026-10-14')
    build(parser.parse_args().batch)
