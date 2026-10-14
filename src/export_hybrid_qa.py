"""Evidence-enriched message-format samples, without model training."""
import json
from pathlib import Path
from build_samples import html_grid, make_viewer
from extract_native import dump

ROOT=Path(__file__).resolve().parents[1]


def main():
    bundles=json.loads((ROOT/'outputs/hybrid_evidence.json').read_text())
    for b in bundles:
        if b.get('table_html'):
            b['table_grid']=html_grid(b['table_html'])
    by_id={b['id']:b for b in bundles}
    samples=[]
    raw=[json.loads(x) for x in (ROOT/'outputs/qa_samples.jsonl').read_text().splitlines()]
    for q in raw:
        q['id']='hybrid:'+q['id']
        q['evidence_ids']=[x.replace('affibody:xml:','affibody:hybrid:') for x in q['evidence_ids']]
        if all(x in by_id for x in q['evidence_ids']):
            samples.append(q)
    # Additional PDF-derived examples are only from the visually checked Ryze
    # Table 2, never from the known malformed or caption-conflicted raw tables.
    b=next(b for b in bundles if b['document_id']=='ryze' and b.get('label')=='table:2')
    grid=b['table_grid']
    for ri,row in list(enumerate(grid['rows']))[grid['header_rows']:]:
        for ci,cell in list(enumerate(row))[1:]:
            samples.append(dict(id=f'hybrid:qa:{len(samples):03d}',document_id='ryze',
                question=f"In Table 2, what {grid['headers'][ci]} value is reported for {row[0]['text']}?",
                answer=cell['text'],evidence_ids=[b['id']],answer_location=dict(row=ri,column=ci,
                    header=grid['headers'][ci],row_label=row[0]['text']),
                generation_method='deterministic_table_lookup',verification='exact_cell_replay',
                task='reported_table_value',training_status='pipeline_sample_only'))
    records=[]
    for q in samples:
        b=by_id[q['evidence_ids'][0]]
        if q['task']=='reported_table_value':
            assert q['answer']==b['table_grid']['rows'][q['answer_location']['row']][q['answer_location']['column']]['text']
        else:
            assert q['answer'] in b['caption']
        evidence='Caption: '+b['caption']
        if b.get('table_html'):
            evidence+='\nTable structure:\n'+b['table_html']
        if b.get('table_notes'):
            evidence+='\nTable footnotes: '+b['table_notes']
        evidence+='\nReferring paragraphs:\n'+'\n'.join(p.get('text','') for p in b.get('referring_paragraphs',[]))
        records.append(dict(id=q['id'],evidence_ids=q['evidence_ids'],
            source_sha256=b['source_sha256'],generation_method=q['generation_method'],
            review_status='Pipeline demonstration; no semantic or visual-model verification',
            messages=[dict(role='system',content='Answer using the supplied paper evidence. Preserve reported units, uncertainty, footnotes and missing-value distinctions. If unsupported, say so.'),
                      dict(role='user',content=q['question']+'\n\n'+evidence),
                      dict(role='assistant',content=q['answer'])],
            images=[b['image_path']] if q['task']=='caption_report' else [],
            image_scope='full_source_page' if q['task']=='caption_report' else None))
    for name,data in [('hybrid_qa_samples.jsonl',samples),('evidence_enriched_sft_samples.jsonl',records)]:
        (ROOT/'outputs'/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data))
    dump(ROOT/'outputs/hybrid_qa_validation.json',dict(total=len(samples),exact_replay_passed=len(samples),
         model_training_performed=False,model_generated_answers=False,
         limitation='Exact source lookup/replay verifies transport only; no reasoning or general benchmark score.'))
    make_viewer(bundles,samples)
    print(json.dumps(dict(hybrid_qa=len(samples),message_format_examples=len(records),exact_replay_passed=len(samples))),flush=True)


if __name__=='__main__':
    main()
