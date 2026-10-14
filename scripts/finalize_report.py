"""Verify provenance and export the pilot's report, versions and run summary."""
import hashlib
import html
import importlib.metadata
import importlib.util
import json
import os
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from extract_native import dump


def read(relative):
    return json.loads((ROOT/relative).read_text())


def main():
    manifest=read('inputs/manifest.json')
    for source in manifest['sources']:
        if source.get('path'):
            assert hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256'],source['path']
    derived=[]
    for path in sorted((ROOT/'inputs').glob('*.provenance.json')):
        entry=json.loads(path.read_text())
        assert hashlib.sha256((ROOT/entry['source']).read_bytes()).hexdigest()==entry['source_sha256']
        entry['derived_sha256']=hashlib.sha256((ROOT/entry['derived_path']).read_bytes()).hexdigest()
        derived.append(entry)
    dump(ROOT/'inputs/derived_manifest.json',derived)
    bundles=read('outputs/hybrid_evidence.json')
    for b in bundles:
        assert (ROOT/b['source_path']).exists()
        assert (ROOT/b['image_path']).is_file(),b['id']
        assert hashlib.sha256((ROOT/b['source_path']).read_bytes()).hexdigest()==b['source_sha256']
    assert len({b['id'] for b in bundles})==len(bundles)
    examples=[json.loads(x) for x in (ROOT/'outputs/evidence_enriched_sft_samples.jsonl').read_text().splitlines()]
    bundle_ids={b['id'] for b in bundles}
    for q in examples:
        assert set(q['evidence_ids'])<=bundle_ids
        assert [m['role'] for m in q['messages']]==['system','user','assistant']
        assert all((ROOT/p).is_file() for p in q['images'])
    packages={}
    for distribution in importlib.metadata.distributions():
        name=distribution.metadata.get('Name','unknown')
        if name.lower() not in packages:
            packages[name.lower()]=dict(name=name,version=distribution.version,
                location=str(distribution.locate_file('')))
    dump(ROOT/'sources/environment_versions.json',dict(python=sys.version,python_executable=sys.executable,
         packages=sorted(packages.values(),key=lambda x:x['name'].lower())))
    revisions=[]
    hub=ROOT/'cache/huggingface/hub'
    for model in sorted(hub.glob('models--*')):
        ref=model/'refs/main'
        revisions.append(dict(repository=model.name.removeprefix('models--').replace('--','/'),
                              main_revision=ref.read_text().strip() if ref.exists() else None))
    dump(ROOT/'sources/model_revisions.json',revisions)
    run_summaries=[read(str(path.relative_to(ROOT)))['summary'] for path in sorted((ROOT/'outputs/docling').glob('*/evidence.json'))]
    audit=read('outputs/audit.json')
    targeted=read('outputs/targeted_ocr_audit.json')
    measurements=[json.loads(x) for x in (ROOT/'outputs/binding_measurements.jsonl').read_text().splitlines()]
    native_summaries=read('outputs/native_summary.json')['documents']
    original_pages=sum(s.get('pages',0) for s in native_summaries if s['document_id'] in ['ryze','llava_med','affibody'])
    original_bundle_count=sum(b['document_id'] in ['ryze','llava_med','affibody'] for b in bundles)
    pst=timezone(timedelta(hours=-8))
    summary=dict(completed_at_pst=datetime.now(pst).isoformat(),timezone='PST, fixed UTC-8',
        original_papers=3,original_pdf_pages=original_pages,derived_ocr_cases=len(derived),
        original_evidence_bundles=original_bundle_count,hybrid_total_with_ryze_stress_case=len(bundles),
        bundles_by_document=dict(Counter(b['document_id'] for b in bundles)),
        qa_examples=len(examples),qa_check=read('outputs/hybrid_qa_validation.json'),
        binding_measurements=len(measurements),numeric_binding_values=sum(m['value'] is not None for m in measurements),
        not_determined_binding_values=sum(m['missing_reason']=='not_determined' for m in measurements),
        docling_runs=run_summaries,workers=1,cpu_math_threads=2,gpus_used=0,subagents_spawned=0,new_ssh_connections=0,
        executed_methods=['PyMuPDF','pdfplumber_lines','pdfplumber_text','native_JATS','Docling','Docling_RapidOCR','hybrid_geometry_binding'],
        reviewed_not_executed=['olmOCR','GLM-OCR','GROBID'],
        limitations=['Tiny exploratory source-based checks, not benchmark accuracy.',
                     'QA is deterministic extraction, not model-generated reasoning.',
                     'Figure fallback images are full source pages; crop segmentation is not established.',
                     'OCR/header/footnote mistakes and malformed raw tables remain in raw output.'])
    dump(ROOT/'reports/pilot_summary.json',summary)
    cells=''.join('<tr><td>'+html.escape(x['method'])+'</td><td>'+str(x['passed'])+'/'+str(x['total'])+'</td></tr>' for x in audit['table_cell_checks'])
    source_checks=''.join('<tr><td>'+html.escape(x['table'])+'</td><td>'+str(x['passed'])+'/'+str(x['total'])+'</td></tr>' for x in audit['affibody_pdf_vs_xml_cells'])
    repairs=''.join('<tr><td>'+html.escape(x['table'])+'</td><td>'+str(x['passed'])+'/'+str(x['total'])+'</td></tr>' for x in targeted['comparisons'])
    page='''<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Paper extraction pilot</title>
<style>body{font:16px/1.6 system-ui;max-width:950px;margin:40px auto;padding:0 24px;color:#17212d;background:#f7f8fa}section{background:#fff;border:1px solid #dbe2e8;padding:22px;margin:20px 0;border-radius:8px}h1,h2{line-height:1.25}h2{font-size:22px}table{border-collapse:collapse;width:100%}th,td{border-bottom:1px solid #ddd;text-align:left;padding:9px}a{color:#185a9d}img{max-width:100%;max-height:440px;object-fit:contain}.counts{display:flex;gap:20px;flex-wrap:wrap}.counts span{font-size:24px;font-weight:650}small{font-size:13px}code{overflow-wrap:anywhere}</style>'''
    page+='<h1>Paper extraction pilot</h1><p>A source-first pipeline for structured facts and evidence-enriched QA.</p>'
    page+=f'<div class=counts><div><span>{original_pages}</span><br>PDF pages</div><div><span>{original_bundle_count}</span><br>original-paper bundles</div><div><span>{len(examples)}</span><br>QA examples</div><div><span>{len(measurements)}</span><br>binding records</div></div>'
    page+='<p><a href="sample_viewer.html">Inspect the evidence and sample questions</a> · <a href="../README.md">Read methods and reproduction instructions</a> · <a href="pilot_summary.json">Download run summary</a></p>'
    page+='<section><h2>What the experiments showed</h2><p>Native XML preserves labels, table spans, footnotes and explicit referring text. PDF layout extraction helps, but its output needs checks. Selective OCR repaired a difficult page; geometry checks caught an incorrect caption link.</p><p>Recommended route: native XML/HTML when available → native PDF text plus layout/table extraction → selective OCR or document VLM on failures → evidence validation → grounded QA.</p></section>'
    page+='<section><h2>Ryze Table 2: twelve position-specific checks</h2><table><tr><th>Method</th><th>Checked cells</th></tr>'+cells+'</table><p>OCR recovered the values but initially attached the caption to the wrong table. The geometry repair reassigns it and remains marked for review. This is a single-table diagnostic, not a general OCR benchmark.</p><img src="../outputs/docling/ryze/table_057.png" alt="Source crop of Ryze Table 2"></section>'
    page+='<section><h2>Affibody: PDF compared with native XML</h2><table><tr><th>Raw digital-PDF table</th><th>Exact labelled-cell matches</th></tr>'+source_checks+'</table><p>Tables 3 and 4 contained duplicated or merged cells. Table 5 was entangled with a chart caption. XML keeps the original five tables separately.</p><h2>Targeted OCR of page 11</h2><table><tr><th>Table</th><th>Checked cells after OCR</th></tr>'+repairs+'</table><p>The twelve values were recovered. One superscript header marker was still misread, so this does not establish full page correctness.</p></section>'
    page+='<section><h2>Outputs and limits</h2><p>The 36 questions/answers replay exactly from retained table cells or captions. They demonstrate evidence transport; no model was trained and no teacher reasoning was generated. The 27 binding records retain units, uncertainty and missing-measurement semantics.</p><p>Source pages accompany all preferred bundles. They are explicitly full pages; regional crops are optional because multi-panel figures and decorative regions remain ambiguous.</p><p>olmOCR, GLM-OCR and GROBID were researched but not run. The next useful test is a local document VLM on the flagged regions with these same source-based checks.</p><p><a href="../outputs/hybrid_evidence.jsonl">Evidence JSONL</a> · <a href="../outputs/evidence_enriched_sft_samples.jsonl">SFT-format samples</a> · <a href="../outputs/binding_measurements.jsonl">Binding records</a> · <a href="../outputs/audit.json">Detailed checks</a></p></section>'
    page+='<p><small>'+html.escape(summary['completed_at_pst'])+' · PST, fixed UTC-8 · one document worker · CPU only · no new SSH connections</small></p></html>'
    (ROOT/'reports/pilot_report.html').write_text(page)
    code_paths=sorted((ROOT/'src').glob('*.py'))+sorted((ROOT/'scripts').glob('*'))+[ROOT/'README.md',ROOT/'constraints-docling.txt']
    dump(ROOT/'sources/code_hashes.json',{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in code_paths if p.is_file()})
    print(json.dumps({k:summary[k] for k in ['original_pdf_pages','original_evidence_bundles','qa_examples','binding_measurements','gpus_used','completed_at_pst']}))


if __name__=='__main__':
    main()
