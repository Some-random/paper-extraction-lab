"""Small source-based extraction checks, separate from generated-answer checks."""
import json
import re
from pathlib import Path
from lxml import etree

from extract_native import dump, normalize
from build_samples import html_grid

ROOT = Path(__file__).resolve().parents[1]


def canonical(text):
    return re.sub(r"\s+", "", str(text)).replace("\u2212","-").replace("\u2011","-").casefold()


def check_rows(matrix, expected):
    results = []
    for gold in expected:
        candidates = [row for row in matrix if row and canonical(row[0]) == canonical(gold[0])]
        observed = candidates[0] if len(candidates) == 1 else []
        for col, target in enumerate(gold[1:],1):
            actual = observed[col] if len(observed)>col else None
            results.append(dict(row_label=gold[0],column=col,expected=target,actual=actual,
                                passed=actual is not None and canonical(actual)==canonical(target)))
    return results


def main():
    gold = json.loads((ROOT / "inputs/gold_checks.json").read_text())
    bundles = json.loads((ROOT / "outputs/evidence_bundles.json").read_text())
    samples = [json.loads(x) for x in (ROOT / "outputs/qa_samples.jsonl").read_text().splitlines()]
    table_results, ordering_results = [], []
    for target in gold["tables"]:
        native_path = ROOT / "outputs/native" / target["document_id"] / "document.json"
        if native_path.exists():
            native = json.loads(native_path.read_text())
            candidates = [t for t in native["table_candidates"] if t["page"]==target["page"]]
            for strategy in ["lines","text"]:
                options = [(t["id"],check_rows(t["rows"],target["rows"])) for t in candidates if t["strategy"]==strategy]
                if options:
                    identity, checks = max(options,key=lambda x:sum(c["passed"] for c in x[1]))
                else:
                    identity, checks = None,check_rows([],target["rows"])
                table_results.append(dict(method="pdfplumber_"+strategy,document_id=target["document_id"],
                    table=target["label"],passed=sum(c["passed"] for c in checks),total=len(checks),
                    table_candidate_id=identity,checks=checks,
                    note="Best detected table candidate by diagnostic score; optimistic baseline selection, no caption binding implied."))
        for doc_id in [target["document_id"],"ryze_scan_p5"]:
            candidates = [b for b in bundles if b["document_id"]==doc_id and b.get("label")=="table:2"]
            matrix = []
            if len(candidates)==1:
                matrix = [[c["text"] for c in row] for row in candidates[0].get("table_grid",{}).get("rows",[])]
            checks = check_rows(matrix,target["rows"])
            table_results.append(dict(method="Docling_OCR" if doc_id.endswith("scan_p5") else "Docling_native_text",
                document_id=doc_id,table=target["label"],passed=sum(c["passed"] for c in checks),
                total=len(checks),checks=checks,matching_bundles=len(candidates)))
            if doc_id.endswith('scan_p5'):
                options=[b for b in bundles if b['document_id']==doc_id and b['kind']=='table']
                best=max((check_rows([[c['text'] for c in row] for row in b.get('table_grid',{}).get('rows',[])],target['rows'])
                          for b in options),key=lambda cs:sum(c['passed'] for c in cs),default=check_rows([],target['rows']))
                table_results.append(dict(method='Docling_OCR_best_matrix_ignoring_caption',document_id=doc_id,
                    table=target['label'],passed=sum(c['passed'] for c in best),total=len(best),checks=best,
                    note='Optimistic matrix check separates OCR/table cell quality from the observed wrong caption attachment.'))
                hybrid_path=ROOT/'outputs/hybrid_evidence.json'
                if hybrid_path.exists():
                    hybrid=json.loads(hybrid_path.read_text())
                    item=next((b for b in hybrid if b['document_id']==doc_id and b.get('label')=='table:2'),None)
                    matrix=[]
                    if item and item.get('table_html'):
                        matrix=[[c['text'] for c in row] for row in html_grid(item['table_html'])['rows']]
                    checks=check_rows(matrix,target['rows'])
                    table_results.append(dict(method='hybrid_OCR_geometry_binding',document_id=doc_id,
                        table=target['label'],passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                        note='Caption reassigned by same-page horizontal overlap and conservative distance; repair is flagged for review.'))
    for target in gold["reading_order"]:
        native_path=ROOT/'outputs/native'/target['document_id']/'document.json'
        if native_path.exists():
            native=json.loads(native_path.read_text())
            page=next(p for p in native['pages'] if p['page']==target['page'])
            texts=[('PyMuPDF_original',page['native_text']),('PyMuPDF_position_sorted',page['position_sorted_text'])]
        else:
            texts=[]
        for doc_id in [target['document_id'],'ryze_scan_p5']:
            docling_path=ROOT/'outputs/docling'/doc_id/'evidence.json'
            if docling_path.exists():
                doc=json.loads(docling_path.read_text())
                texts.append(('Docling_'+doc_id,' '.join(e['text'] for e in doc['elements']
                             if e.get('source_provenance') and e['source_provenance']['page']==(1 if doc_id.endswith('scan_p5') else target['page']))))
        for method,text in texts:
            normalized=canonical(text)
            before=normalized.find(canonical(target['before']))
            after=normalized.find(canonical(target['after']))
            ordering_results.append(dict(method=method,document_id=target['document_id'],
                before=target['before'],after=target['after'],passed=before>=0 and after>before,
                before_index=before,after_index=after))
    jats=json.loads((ROOT/'outputs/jats/affibody/document.json').read_text())
    visual_ids={b['xml_id'] for b in jats['bundles']}
    all_refs={rid for p in jats['elements'] for rid in p['xml_reference_ids']}
    unresolved=sorted(all_refs-visual_ids)
    qa_failures=[]
    indexed={b['id']:b for b in bundles}
    for q in samples:
        if len(q['evidence_ids'])!=1 or q['evidence_ids'][0] not in indexed:
            qa_failures.append(dict(id=q['id'],reason='unresolved_evidence_id'))
            continue
        b=indexed[q['evidence_ids'][0]]
        if q['task']=='reported_table_value':
            loc=q['answer_location']
            observed=b['table_grid']['rows'][loc['row']][loc['column']]['text']
            valid=observed==q['answer']
        else:
            valid=q['answer'] in b['caption']
        if not valid:
            qa_failures.append(dict(id=q['id'],reason='answer_not_replayable_from_evidence'))
    # Source XML provides a silver reference for the matching publisher PDF.
    silver=[]
    for source in jats['bundles']:
        if source['kind']!='table':
            continue
        label=source['label'].replace('Table ','table:')
        candidates=[b for b in bundles if b['document_id']=='affibody' and b['kind']=='table'
                    and b.get('binding_method')!='explicit_JATS_xref' and b.get('label')==label]
        b=candidates[0] if len(candidates)==1 else None
        expected=html_grid(source['table_html'])
        body=expected['rows'][expected['header_rows']:]
        observed=[[c['text'] for c in row] for row in b['table_grid']['rows']] if b and b.get('table_grid') else []
        checks=check_rows(observed,[[c['text'] for c in row] for row in body])
        silver.append(dict(table=label,passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                           source='native JATS silver reference; PDF/XML version or footnote differences may affect exact match'))
    audit=dict(scope=gold['scope'],table_cell_checks=table_results,reading_order_checks=ordering_results,
        jats_structural_check=dict(figures=sum(b['kind']=='figure' for b in jats['bundles']),
            tables=sum(b['kind']=='table' for b in jats['bundles']),unresolved_visual_references=unresolved,
            visual_labels_unique=len(visual_ids)==len(jats['bundles']),
            merged_header_preserved=any(html_grid(b['table_html'])['merged_cells'] for b in jats['bundles'] if b['kind']=='table')),
        affibody_pdf_vs_xml_cells=silver,
        qa_transport_check=dict(total=len(samples),passed=len(samples)-len(qa_failures),failures=qa_failures,
            limitation='Checks exact extraction-to-answer replay, not factual correctness or visual reasoning.'),
        bundle_count=len(bundles),sample_count=len(samples))
    dump(ROOT/'outputs/audit.json',audit)
    print(json.dumps(dict(tables=[{k:v for k,v in x.items() if k in ['method','passed','total']} for x in table_results],
                          qa=audit['qa_transport_check'],jats=audit['jats_structural_check'])),flush=True)
    if qa_failures or unresolved:
        raise SystemExit('Evidence integrity checks failed')


if __name__=='__main__':
    main()
