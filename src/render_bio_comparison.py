"""Create a small offline, inspectable experiment report with source evidence."""
import html
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXP=ROOT/'experiments/bio_tool_comparison_v1'
DEST=EXP/'reports/results.html'


def esc(value):
    return html.escape(str(value if value is not None else ''))


def href(path):
    return esc(os.path.relpath(ROOT/path,DEST.parent))


def main():
    report=json.loads((EXP/'reports/comparison.json').read_text())
    manifest=json.loads((EXP/'inputs/manifest.json').read_text())
    refs=json.loads((EXP/'reference/elements.json').read_text())
    evidence=json.loads((EXP/'evidence/summary.json').read_text())
    findings_path=EXP/'reports/findings.json'
    findings=json.loads(findings_path.read_text()) if findings_path.exists() else {}
    names={'docling':'Docling (digital PDF)','docling_rapidocr':'Docling + RapidOCR (image-only)',
        'olmocr':'olmOCR-2-7B-1025','mineru':'MinerU2.5-Pro-2605',
        'glmocr_docling':'GLM-OCR + Docling regions'}
    summaries=[]
    for item in report['tools']:
        s=item['summary'];total=s['logical_cells_checked']
        rate=f"{100*s['caption_bound_matched']/total:.1f}%" if total else 'pending'
        summaries.append('<tr>'+''.join('<td>'+esc(v)+'</td>' for v in [names[s['tool']],
            f"{s['pages_completed']}/9",f"{s['caption_bound_matched']}/{total} ({rate})",
            f"{s['quantity_and_value_matched']}/{total}",
            f"{s['best_matrix_matched']}/{total}",f"{s['perfect_caption_bound_tables']}/{s['checked_tables']}",
            f"{s['header_matched']}/{s['header_total']}",
            f"{s['power_header_preservation']['matched']}/{s['power_header_preservation']['total']}",
            f"{s['optional_figure_label_coverage']['matched']}/46" if s['optional_figure_label_coverage']['annotations_available'] else 'not produced',
            f"{s['page_seconds_total']:.1f}",s['peak_gpu_allocated_gib']])+'</tr>')
    cards=[]
    for source in refs:
        for item in report['tools']:
            e=next((e for e in item['elements'] if e['source_id']==source['id']),None)
            if e is None:
                continue
            if source['kind']=='figure':
                case=next(c for c in manifest['cases'] if c['id']==source['case_id'])
                raw=json.loads((ROOT/e['raw_result_path']).read_text())
                annotation='\n\n'.join(f.get('annotation') or '' for f in raw['figures'])
                labels=[c for c in item['figure_label_checks'] if c['source_id']==source['id']]
                label_html=''.join('<li>'+esc(c['label'])+' — '+('found' if c['matched'] else 'absent')+'</li>' for c in labels)
                cards.append('<article data-tool="'+esc(item['summary']['tool'])+'" data-doc="'+esc(source['document_id'])+'"><h2>'+esc(names[item['summary']['tool']])+' · '+esc(source['id'])+'</h2><p>Caption '+('recovered' if e['caption_recovered'] else 'missing')+'; word recall '+esc(e['caption_word_recall'])+'.</p><p>'+esc(source['caption'])+'</p><p><a href="'+href(case['image'])+'">Rendered source page</a> · <a href="'+href(e['raw_result_path'])+'">Raw extraction JSON</a></p><details><summary>Visible-label checks</summary><ul>'+label_html+'</ul></details><details><summary>Generated figure annotations on this page</summary><p class=note>Annotations may span detected panels or multiple figures. Captions and body text are excluded from label checks. This does not validate chart values.</p><pre>'+esc(annotation or 'No generated figure annotation retained for this page.')+'</pre></details></article>')
                continue
            checks=e['caption_bound_checks'].get('cells',[])
            if checks:
                body=''.join('<tr class="'+('ok' if c['matched'] else 'fail')+'">'+
                    ''.join('<td>'+esc(v)+'</td>' for v in [c['row_key'],c['header'],c['expected'],c['actual'],
                    'match' if c['matched'] else 'mismatch'])+'</tr>' for c in checks)
            else:
                body='<tr class=fail><td colspan=5>No table could be bound to this source label.</td></tr>'
            case=next(c for c in manifest['cases'] if c['id']==source['case_id'])
            header='<p>'+esc(e['caption_bound_matched'])+'/'+esc(e['total'])+' value cells; best candidate '+esc(e['best_matrix_matched'])+'/'+esc(e['total'])+'.</p>'
            links='<p><a href="'+href(case['image'])+'">Rendered source page</a> · <a href="'+href(e['raw_result_path'])+'">Raw extraction JSON</a></p>'
            caption='<p>'+esc(source['caption'])+'</p>'
            content='<details><summary>Cell comparison</summary><div class=scroll><table><thead><tr><th>Source row</th><th>Quantity / unit</th><th>Source XML</th><th>Extractor</th><th>Check</th></tr></thead><tbody>'+body+'</tbody></table></div></details>'
            cards.append('<article data-tool="'+esc(item['summary']['tool'])+'" data-doc="'+esc(source['document_id'])+'"><h2>'+esc(names[item['summary']['tool']])+' · '+esc(source['id'])+'</h2>'+header+caption+links+content+'</article>')
    docs=''.join('<li><a href="'+esc(d['pdf_url'])+'">'+esc(d['title'])+'</a> — pages '+esc(', '.join(str(p) for p in d['selected_pages']))+'</li>' for d in manifest['documents'])
    tool_opts=''.join('<option value="'+esc(t['summary']['tool'])+'">'+esc(names[t['summary']['tool']])+'</option>' for t in report['tools'])
    doc_opts=''.join('<option value="'+esc(d['document_id'])+'">'+esc(d['document_id'])+'</option>' for d in manifest['documents'])
    parts=['<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Biology paper extraction comparison</title>',
        '<style>body{font:16px/1.55 system-ui;max-width:1250px;margin:32px auto;padding:0 22px;color:#14202b;background:#f7f8fa}h1,h2{line-height:1.2}h2{font-size:20px}table{border-collapse:collapse;font-size:13px;background:white}th,td{border:1px solid #dce0e4;padding:7px 10px;text-align:left;vertical-align:top;white-space:pre-wrap}th{background:#edf1f5}.scroll{overflow:auto}article{background:white;border:1px solid #dce0e4;padding:18px;margin:16px 0;border-radius:8px}.fail td:last-child{color:#a52525;font-weight:bold}.ok td:last-child{color:#236744}summary{cursor:pointer;font-weight:600}select{font:inherit;padding:6px;margin-right:12px}.controls{position:sticky;top:0;background:#f7f8fa;padding:14px 0}a{color:#185bb0}.note{font-size:14px;color:#46515e}code{font-size:13px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}</style>',
        '<h1>Biology paper extraction comparison</h1><p>Three experimental biology papers, nine fixed source pages, 12 tables and six figures. Ryze and OLMo are method references; neither is in this test corpus.</p>',
        '<p><strong>'+esc(findings.get('recommendation',''))+'</strong></p>',
        '<div class=scroll><table><thead><tr>'+''.join('<th>'+esc(h)+'</th>' for h in ['Executed method','Pages','Reference-matched labelled cells','Also passed quantity/unit header checks','Best matrix (oracle)','Perfect tables','Strict headers','Power-bearing headers','Figure labels (optional)','Page seconds','Peak allocated GPU GiB'])+'</tr></thead><tbody>'+''.join(summaries)+'</tbody></table></div>',
        '<details><summary>How the two cell scores are calculated</summary><p>The denominator is 243 logical body cells from publisher XML. A labelled cell passes when the model output binds to the source table caption, the row/group identifier and column count match, and the value matches at the same column after equivalent typography and TeX formatting are normalized. Numbers, uncertainty, signs and identifier punctuation are preserved. The second score counts the subset whose quantity/unit header also passes conservative notation checks, including numeric powers. These are custom diagnostics, not official olmOCR-bench scores or a semantic verifier.</p><p>olmOCR 2: 201/243 (82.7%) labelled cells; 183/243 (75.3%) with header checks. For example, −23 ± 1 matches -23 \\pm 1, but a ΔG° (kJ mol⁻¹) header reduced to Thermodynamic fails the second check. The 18-cell difference comes from the first two plasma-protein tables. <a href="metric_definitions.json">Full definitions and recorded example</a>.</p></details>',
        '<p class=note>'+esc(report['metrics_note'])+' Timing excludes downloads and includes per-page extraction; model/pipeline initialization is recorded separately. CPU baselines use two CPU threads; VLMs use one H200. Transformers timing is not optimized serving throughput. GLM-OCR is a custom Docling-layout hybrid, rather than its official SDK.</p>',
        '<ul>'+''.join('<li>'+esc(v)+'</li>' for v in findings.get('observations',[]))+'</ul>',
        '<p class=note>'+esc(findings.get('limitations',''))+'</p>',
        '<p>The independent structured-source branch produced '+esc(evidence['bundles'])+' evidence bundles ('+esc(evidence['figures'])+' figures, '+esc(evidence['tables'])+' tables), all with explicit referring paragraphs and source pages. '+esc(evidence['lookup_qa_replayed'])+'/'+esc(evidence['lookup_qa_samples'])+' deterministic lookup examples replay exactly. These are pipeline examples, not teacher-generated reasoning or a validated training dataset.</p>',
        '<p><a href="comparison.json">Full checks and failure details</a> · <a href="../inputs/manifest.json">Frozen inputs and hashes</a> · <a href="../evidence/bundles.jsonl">Source-native evidence</a> · <a href="../evidence/pdf_model_bundles.jsonl">PDF model evidence</a> · <a href="../evidence/qa_samples.jsonl">Lookup examples</a> · <a href="verification.json">Integrity checks</a></p>',
        '<details><summary>Test papers</summary><ul>'+docs+'</ul></details>',
        '<p class=note>Public reference benchmarks cover different tasks and versions: <a href="https://github.com/opendatalab/OmniDocBench">OmniDocBench</a> evaluates text, formulas, tables and reading order; <a href="https://github.com/allenai/olmocr/blob/main/olmocr/bench/README.md">olmOCR-bench</a> tests text presence/absence, order, neighboring table cells and rendered math. This nine-page source-derived check does not rank all available tools.</p>',
        '<details><summary>Current public benchmark context and method references</summary><p>The maintainer-reported OmniDocBench v1.6_full leaderboard checked on October 13, 2026 lists '+esc(', '.join(f"{r['method']} {r['score']}" for r in findings.get('wider_ecosystem',{}).get('reported_overall',[])))+'. These public scores are distinct from this biology experiment. TeleOCR, OvisOCR2 and PaddleOCR-VL-1.6 were reviewed, not executed here.</p><ul>'+''.join('<li><a href="'+esc(r['url'])+'">'+esc(r['title'])+'</a></li>' for r in findings.get('references',[]))+'</ul><p><a href="findings.json">Full findings and protocol notes</a> · <a href="mineru_identifier_error_audit.json">43-cell identifier error audit</a></p></details>',
        '<div class=controls><label>Method <select id=tool><option value=all>All executed methods</option>'+tool_opts+'</select></label><label>Paper <select id=doc><option value=all>All papers</option>'+doc_opts+'</select></label></div>',
        ''.join(cards),
        '<script>const t=document.getElementById("tool"),d=document.getElementById("doc");function filter(){for(const a of document.querySelectorAll("article"))a.hidden=(t.value!=="all"&&a.dataset.tool!==t.value)||(d.value!=="all"&&a.dataset.doc!==d.value)}t.onchange=d.onchange=filter;</script></html>']
    DEST.write_text(''.join(parts))
    print(str(DEST))


if __name__=='__main__':
    main()
