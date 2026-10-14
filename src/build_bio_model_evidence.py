"""Bundle extracted PDF evidence without silently replacing it with gold XML."""
import json
import re
from pathlib import Path
from evaluate_bio_tools import bind_captions,caption_candidates
from bio_table_metrics import parse_table,table_records

ROOT=Path(__file__).resolve().parents[1]
EXP=ROOT/'experiments/bio_tool_comparison_v1'


def mentions(text):
    matches=[]
    for m in re.finditer(r'\b(Table|Figure|Fig\.?)\s*(\d+)(?:[A-Za-z])?\b',text or '',re.I):
        key=('table' if m[1].lower()=='table' else 'figure')+':'+m[2]
        if key not in matches:
            matches.append(key)
    return matches


def main():
    manifest=json.loads((EXP/'inputs/manifest.json').read_text())
    records=[];counts={}
    for tool in ['docling','docling_rapidocr','olmocr','mineru','glmocr_docling']:
        results=[];paragraphs=[]
        for case in manifest['cases']:
            path=EXP/'runs'/tool/case['id']/'result.json'
            if not path.exists():
                continue
            result=json.loads(path.read_text());results.append((case,result,path))
            text_blocks=result.get('blocks') or []
            if not text_blocks:
                # Remove generated table markup and image alt text so those
                # elements are not misrepresented as referring body prose.
                body=re.sub(r'<table\b.*?</table>','',result['markdown'],flags=re.I|re.S)
                body=re.sub(r'!\[[^\]]*\]\([^)]*\)','',body)
                text_blocks=[dict(text=p,type='generated_markdown_paragraph') for p in body.split('\n\n')]
            for i,b in enumerate(text_blocks):
                if b.get('type') not in ['text','paragraph','section_header','footnote','table_footnote','generated_markdown_paragraph']:
                    continue
                text=b.get('text') or b.get('content') or ''
                if not text or re.match(r'^\s*(Table|Figure|Fig\.?)\s*\d+\s*[.:]',text,re.I):
                    continue
                labels=mentions(text)
                if labels:
                    paragraphs.append(dict(id=f"{tool}:{case['id']}:p{i}",text=text,
                        document_id=case['document_id'],source_page=case['source_page'],
                        bbox=b.get('bbox'),labels=labels,extracted_block_type=b.get('type')))
        for case,result,path in results:
            for kind,list_key in [('table','tables'),('figure','figures')]:
                bound=bind_captions(result,case,kind)
                for index,item in enumerate(result[list_key]):
                    b=bound.get(index);label=b['label'] if b else None
                    context=[p for p in paragraphs if label and p['document_id']==case['document_id'] and label in p['labels']]
                    flags=[]
                    if not b:
                        flags.append('unbound_or_missing_caption_label')
                    if not context:
                        flags.append('no_explicit_referring_text_on_selected_pages')
                    record=dict(id=f"{tool}:{case['id']}:{kind}:{index}",tool=tool,
                        document_id=case['document_id'],source_page=case['source_page'],kind=kind,
                        label=label,caption=b['text'] if b else '',bbox=item.get('bbox'),
                        extracted_item=item,referring_paragraphs=context,
                        source_pdf=case['source_pdf'],
                        source_pdf_sha256=next(d['pdf_sha256'] for d in manifest['documents'] if d['document_id']==case['document_id']),
                        full_source_page_image=case['image'],raw_extraction_path=str(path.relative_to(ROOT)),
                        binding=b,reference_XML_used_for_repair=False,
                        context_scope='nine selected diagnostic pages; full paper context may be incomplete',
                        semantic_status='extracted model output; scientific review pending')
                    if kind=='table':
                        try:
                            record['extracted_logical_table']=table_records(parse_table(item['html']))
                        except Exception as exc:
                            flags.append('unparseable_table:'+type(exc).__name__)
                    else:
                        flags.append('figure_region_or_panel_completeness_not_independently_verified')
                        if item.get('annotation'):
                            flags.append('generated_figure_annotation_not_validated_chart_data')
                    record['quality_flags']=flags;records.append(record)
        counts[tool]=dict(completed_pages=len(results),bundles=sum(r['tool']==tool for r in records))
    out=EXP/'evidence'
    (out/'pdf_model_bundles.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
    (out/'pdf_model_summary.json').write_text(json.dumps(counts,indent=2)+'\n')
    print(json.dumps(counts))


if __name__=='__main__':
    main()
