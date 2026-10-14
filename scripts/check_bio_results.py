"""Check experiment provenance, completeness, and evidence-export invariants."""
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXP=ROOT/'experiments/bio_tool_comparison_v1'
sys.path.insert(0,str(ROOT/'src'))
from bio_table_metrics import compare


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest=json.loads((EXP/'inputs/manifest.json').read_text())
    for d in manifest['documents']:
        assert digest(ROOT/d['pdf_path'])==d['pdf_sha256']
        assert digest(ROOT/d['xml_path'])==d['xml_sha256']
    assert digest(EXP/'reference/elements.json')==manifest['reference']['sha256']
    assert digest(EXP/'reference/figure_labels.json')==manifest['reference']['figure_label_sha256']
    refs=json.loads((EXP/'reference/elements.json').read_text())
    for source in refs:
        if source['kind']=='table':
            own=compare(source,source['table_html'])
            assert own['matched']==own['quantity_and_value_matched']==own['total']
    table=next(r for r in refs if r['id']=='her2_affibody:table:4')
    bad_value=compare(table,table['table_html'].replace('0.33','3.3',1))
    assert bad_value['matched']<bad_value['total']
    bad_entity=compare(table,table['table_html'].replace('Z-ABD-DM1','Z-ABD-DM2',1))
    assert bad_entity['matched']<bad_entity['total']
    bad_unit=compare(table,table['table_html'].replace('nM','nm',1))
    assert bad_unit['matched']==bad_unit['total'] and bad_unit['quantity_and_value_matched']<bad_unit['total']
    temp_table=next(r for r in refs if r['id']=='plasma_peptides:table:1')
    bad_sign=compare(temp_table,temp_table['table_html'].replace('−23 ± 1','23 ± 1',1))
    assert bad_sign['matched']<bad_sign['total']
    bad_scale=compare(temp_table,temp_table['table_html'].replace('10<sup>5</sup>','10<sup>4</sup>',1))
    assert bad_scale['matched']==bad_scale['total'] and bad_scale['quantity_and_value_matched']<bad_scale['total']
    for case in manifest['cases']:
        for key in ['image','page_pdf','page_image_pdf']:
            assert digest(ROOT/case[key])==case[key+'_sha256']
    report=json.loads((EXP/'reports/comparison.json').read_text())
    assert len(report['tools'])==5
    for entry in report['tools']:
        s=entry['summary'];tool=s['tool']
        assert s['pages_completed']==9,(tool,s['pages_completed'])
        assert s['logical_cells_checked']==243
        assert s['quantity_and_value_matched']<=s['caption_bound_matched']<=s['best_matrix_matched']<=243
        for case in manifest['cases']:
            path=EXP/'runs'/tool/case['id']/'result.json';r=json.loads(path.read_text())
            assert r['case_id']==case['id'] and r['source_page']==case['source_page']
            assert r['reference_xml_in_prompt'] is False and r['batch_size']==1
            if tool in ['olmocr','mineru','glmocr_docling']:
                assert r['gpu_visible_devices']=='0'
                assert r['precision']=='bfloat16'
                model='glmocr' if tool=='glmocr_docling' else tool
                pinned=json.loads((EXP/'models'/f'{model}.json').read_text())
                assert r['model_record']['revision']==pinned['revision']
            assert (path.parent/'raw.md').exists()
    bundles=[json.loads(line) for line in (EXP/'evidence/bundles.jsonl').read_text().splitlines()]
    by_id={b['id']:b for b in bundles}
    assert len(bundles)==34 and len(by_id)==34
    for b in bundles:
        assert b['referring_paragraphs'] and b['images']
        assert all((ROOT/i['path']).exists() for i in b['images'])
    qa=[json.loads(line) for line in (EXP/'evidence/qa_samples.jsonl').read_text().splitlines()]
    for q in qa:
        table=by_id[q['evidence_ids'][0]]['logical_table'];loc=q['source_location']
        row=next(r for r in table['records'] if r['key']==loc['row_key'])
        assert q['answer']==row['cells'][loc['column']-1]
    result=dict(provenance_checked=True,metric_corruption_controls_passed=['numeric_value','entity_label','unit_case','negative_sign','scale_exponent'],papers=3,cases_per_tool=9,tools=5,
        fixed_logical_cells_per_tool=243,source_bundles=34,replayed_lookup_examples=len(qa),
        token_limit_cases={e['summary']['tool']:e['summary']['token_limit_cases'] for e in report['tools']},
        note='Integrity/replay validation, not independent scientific validation or a global benchmark.')
    (EXP/'reports/verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':
    main()
