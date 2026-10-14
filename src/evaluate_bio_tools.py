"""Evaluate actual runs on the frozen biological-paper source checks.

Raw caption attachment and a shared output-only caption binder are separate.
The optimistic best-matrix score is a diagnostic, not an end-to-end score.
No gold captions/values are used by the binder or provided to the models.
"""
import argparse
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
from bio_table_metrics import canonical,compare

ROOT=Path(__file__).resolve().parents[1]
EXP=ROOT/'experiments/bio_tool_comparison_v1'


def label_of(text,kind=None):
    clean=re.sub(r'[*#_]','',text or '').strip()
    m=re.match(r'(Table|Figure|Fig\.?)\s*(\d+)\s*[.:]',clean,re.I)
    if not m:
        return None
    prefix='table' if m[1].casefold()=='table' else 'figure'
    return f'{prefix}:{m[2]}' if kind is None or kind==prefix else None


def normalized_bbox(bbox,case):
    if not bbox:
        return None
    if isinstance(bbox,dict):
        l,t,r,b=[bbox[k] for k in ['l','t','r','b']]
        w,h=case['width'],case['height']
        if bbox.get('coord_origin')=='BOTTOMLEFT':
            t,b=h-t,h-b
        return [l/w,t/h,r/w,b/h]
    return list(bbox)


def caption_candidates(result,case):
    captions=[]
    for index,block in enumerate(result.get('blocks',[])):
        text=block.get('text') or block.get('content') or ''
        # Layout engines can merge neighboring captions into a single region.
        starts=list(re.finditer(r'(?mi)^[ \t]*(?:\*\*)?(?:Table|Figure|Fig\.?)\s*\d+(?:\*\*)?\s*[.:]',text))
        for si,start in enumerate(starts):
            part=text[start.start():starts[si+1].start() if si+1<len(starts) else len(text)]
            label=label_of(part)
            if label:
                captions.append(dict(label=label,text=part,bbox=normalized_bbox(block.get('bbox'),case),
                    block_id=block.get('id',f'block:{index}'),method='output_text_block',
                    region_kind=block.get('region_kind')))
    md=result['markdown']
    if not captions:
        # Exact locations in generated Markdown, without expected source text.
        rx=r'(?mi)^[ \t]*(?:#{1,6}\s*)?(?:\*\*)?(Table|Figure|Fig\.?)\s*(\d+)(?:\*\*)?\s*[.:]'
        for match in re.finditer(rx,md):
            end=md.find('\n\n',match.start())
            if end<0:
                end=len(md)
            table_at=md.lower().find('<table',match.end())
            if table_at>=0:
                end=min(end,table_at)
            text=md[match.start():end].strip()
            captions.append(dict(label=('table' if match[1].lower()=='table' else 'figure')+':'+match[2],
                text=text,char_start=match.start(),char_end=end,method='generated_markdown'))
    return captions


def bind_captions(result,case,kind='table'):
    items=result['tables' if kind=='table' else 'figures']
    captions=[c for c in caption_candidates(result,case) if c['label'].startswith(kind+':')]
    choices=[]
    for i,item in enumerate(items):
        bb=normalized_bbox(item.get('bbox'),case)
        for j,cap in enumerate(captions):
            cb=cap.get('bbox')
            if bb is not None and cb is not None:
                overlap=max(0,min(bb[2],cb[2])-max(bb[0],cb[0]))
                fraction=overlap/max(1e-9,min(bb[2]-bb[0],cb[2]-cb[0]))
                gap=max(0,cb[1]-bb[3],bb[1]-cb[3])
                if fraction<0.2 or gap>0.15:
                    continue
                distance=gap+0.01*(1-fraction)
                if cap.get('region_kind')=='fixed_above_table_context':
                    # A context strip supplies an approximate caption location;
                    # prefer an actual detected caption box when one exists.
                    distance+=0.15
            elif 'char_start' in item and 'char_start' in cap:
                start=item['char_start'];end=start+len(item.get('html',''))
                distance=max(0,start-cap['char_end'],cap['char_start']-end)
                if distance>3000:
                    continue
            else:
                continue
            choices.append((distance,i,j))
    bound={};used=set()
    for distance,i,j in sorted(choices):
        if i in bound or j in used:
            continue
        used.add(j);bound[i]=dict(**captions[j],distance=distance,
            binding_method='shared_output_only_geometry_or_adjacency')
    # Retain explicit extractor captions when output geometry is unavailable.
    for i,item in enumerate(items):
        if i not in bound:
            label=label_of(item.get('caption'),kind)
            if label:
                bound[i]=dict(label=label,text=item['caption'],binding_method='extractor_attached_caption')
    return bound


def word_recall(expected,actual):
    def words(text):
        text=(text or '').casefold().replace('\\','')
        return Counter(re.findall(r'\w+',text))
    gold,pred=words(expected),words(actual)
    return round(sum((gold&pred).values())/max(1,sum(gold.values())),4)


def evaluate_tool(tool,manifest,refs):
    rows=[];cases=[];missing=[]
    for case in manifest['cases']:
        path=EXP/'runs'/tool/case['id']/'result.json'
        if not path.exists():
            missing.append(case['id']);continue
        result=json.loads(path.read_text())
        bound=bind_captions(result,case)
        candidates=caption_candidates(result,case)
        case_refs=[r for r in refs if r['case_id']==case['id']]
        for source in case_refs:
            captions=[c for c in candidates if c['label']==source['label']]
            row=dict(source_id=source['id'],case_id=case['id'],kind=source['kind'],label=source['label'],
                caption_recovered=bool(captions),caption_word_recall=max([word_recall(source['caption'],c['text']) for c in captions],default=0),
                raw_result_path=str(path.relative_to(ROOT)))
            if source['kind']=='table':
                matches=[compare(source,t['html']) for t in result['tables']]
                total=sum(len(r['cells']) for r in source['logical_table']['records'])
                best=max(range(len(matches)),key=lambda i:matches[i]['matched'],default=None)
                common=[i for i,b in bound.items() if b['label']==source['label']]
                explicit=[i for i,t in enumerate(result['tables']) if label_of(t.get('caption'),'table')==source['label']]
                common_i=min(common,key=lambda i:(bound[i].get('distance',math.inf),i),default=None)
                raw_i=explicit[0] if explicit else None
                chosen=matches[common_i] if common_i is not None else dict(matched=0,total=total)
                row.update(total=total,best_matrix_matched=matches[best]['matched'] if best is not None else 0,
                    best_matrix_index=best,caption_bound_matched=chosen['matched'],caption_bound_index=common_i,
                    raw_caption_matched=matches[raw_i]['matched'] if raw_i is not None else 0,
                    raw_caption_index=raw_i,binding=bound.get(common_i),
                    header_matched=chosen.get('header_matched',0),
                    header_total=sum(bool(x) for x in source['logical_table']['headers']),
                    quantity_and_value_matched=chosen.get('quantity_and_value_matched',0),
                    caption_bound_checks=chosen,best_matrix_checks=matches[best] if best is not None else None,
                    same_label_candidate_count=len(common),
                    all_candidate_counts=[dict(index=i,matched=m['matched'],total=m['total'],error=m.get('error')) for i,m in enumerate(matches)])
            rows.append(row)
        expected_labels={r['label'] for r in case_refs if r['kind']=='table'}
        cases.append(dict(case_id=case['id'],elapsed_seconds=result['elapsed_seconds'],
            setup_seconds=result['setup_seconds'],peak_gpu_allocated_gib=result['peak_gpu_allocated_gib'],
            status=result['status'],generated_tokens=result.get('generated_tokens'),
            tables_detected=len(result['tables']),figures_detected=len(result['figures']),
            bindings={str(i):v for i,v in bound.items()},
            unbound_or_unexpected_tables=[i for i in range(len(result['tables'])) if i not in bound or bound[i]['label'] not in expected_labels]))
    tables=[r for r in rows if r['kind']=='table'];figs=[r for r in rows if r['kind']=='figure']
    categories={name:dict(matched=0,total=0) for name in ['uncertainty','negative','missing_ND','multi_value']}
    power_headers=dict(matched=0,total=0)
    for row in tables:
        source=next(r for r in refs if r['id']==row['source_id'])
        # Missing caption/candidate counts as a failure for every source cell.
        checks=row['caption_bound_checks'].get('cells')
        if checks is None:
            checks=[dict(expected=value,matched=False) for r in source['logical_table']['records'] for value in r['cells']]
        for check in checks:
            value=check['expected']
            flags=dict(uncertainty='±' in value,negative=bool(re.search(r'(^|\n)[−-]\s*\d',value)),
                missing_ND=bool(re.match(r'^ND',value)),multi_value='\n' in value)
            for name,eligible in flags.items():
                if eligible:
                    categories[name]['total']+=1
                    categories[name]['matched']+=int(check['matched'])
        hc=row['caption_bound_checks'].get('header_checks',[])
        predicted={h['column']:h['actual'] for h in hc}
        for ci,header in enumerate(source['logical_table']['headers']):
            expected_powers=re.findall(r'\^\(([+-]?\d+)\)',canonical(header,True))
            if expected_powers:
                actual_powers=re.findall(r'\^\(([+-]?\d+)\)',canonical(predicted.get(ci,''),True))
                power_headers['total']+=1
                power_headers['matched']+=int(expected_powers==actual_powers)
    per_document=[]
    for doc in manifest['documents']:
        subset=[r for r in tables if r['source_id'].startswith(doc['document_id']+':')]
        per_document.append(dict(document_id=doc['document_id'],caption_bound_matched=sum(r['caption_bound_matched'] for r in subset),total=sum(r['total'] for r in subset)))
    summary=dict(tool=tool,pages_completed=len(cases),pages_expected=len(manifest['cases']),missing_cases=missing,
        logical_cells_checked=sum(r['total'] for r in tables),
        best_matrix_matched=sum(r['best_matrix_matched'] for r in tables),
        caption_bound_matched=sum(r['caption_bound_matched'] for r in tables),
        quantity_and_value_matched=sum(r['quantity_and_value_matched'] for r in tables),
        raw_caption_matched=sum(r['raw_caption_matched'] for r in tables),
        header_matched=sum(r['header_matched'] for r in tables),header_total=sum(r['header_total'] for r in tables),
        table_captions_recovered=sum(r['caption_recovered'] for r in tables),
        figure_captions_recovered=sum(r['caption_recovered'] for r in figs),
        caption_word_recall_mean=round(sum(r['caption_word_recall'] for r in rows)/max(1,len(rows)),4),
        page_seconds_total=round(sum(c['elapsed_seconds'] for c in cases),3),
        setup_seconds=max([c['setup_seconds'] for c in cases],default=0),
        peak_gpu_allocated_gib=max([c['peak_gpu_allocated_gib'] for c in cases],default=0),
        token_limit_cases=[c['case_id'] for c in cases if c['status']=='token_limit'],
        perfect_caption_bound_tables=sum(r['caption_bound_matched']==r['total'] for r in tables),
        checked_tables=len(tables),scientific_value_categories=categories,power_header_preservation=power_headers,
        unbound_or_unexpected_tables=sum(len(c['unbound_or_unexpected_tables']) for c in cases),
        per_document=per_document)
    return dict(summary=summary,elements=rows,cases=cases)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--tools',nargs='+',default=['docling','docling_rapidocr','olmocr','mineru'])
    args=parser.parse_args()
    manifest=json.loads((EXP/'inputs/manifest.json').read_text())
    ref_path=EXP/'reference/elements.json'
    refs=json.loads(ref_path.read_text())
    assert hashlib.sha256(ref_path.read_bytes()).hexdigest()==manifest['reference']['sha256']
    figure_path=EXP/'reference/figure_labels.json'
    assert hashlib.sha256(figure_path.read_bytes()).hexdigest()==manifest['reference']['figure_label_sha256']
    figure_checks=json.loads(figure_path.read_text())
    report=dict(scope=manifest['scope'],reference=manifest['reference'],
        metrics_note='243 source logical cells, fixed row-label/column-position alignment; typography only. Best-matrix uses gold to choose a candidate and is optimistic. Caption-bound uses an identical output-only binder. Original caption attachments separately reported. Headers are strict strings with power semantics retained. Exploratory silver-reference checks, not a general benchmark.',
        tools=[evaluate_tool(t,manifest,refs) for t in args.tools])
    for tool in report['tools']:
        checks=[];available=False
        for expected in figure_checks['checks']:
            result_path=EXP/'runs'/tool['summary']['tool']/expected['case_id']/'result.json'
            if not result_path.exists():
                continue
            result=json.loads(result_path.read_text())
            text='\n'.join(f.get('annotation') or '' for f in result['figures'])
            available=available or bool(text.strip())
            for label in expected['labels']:
                if label.isdigit():
                    matched=bool(re.search(r'(?<![\d.])'+re.escape(label)+r'(?![\d.])',text))
                else:
                    matched=canonical(label) in canonical(text)
                checks.append(dict(source_id=expected['source_id'],case_id=expected['case_id'],label=label,matched=matched))
        tool['figure_label_checks']=checks
        tool['summary']['optional_figure_label_coverage']=dict(annotations_available=available,
            matched=sum(c['matched'] for c in checks) if available else None,total=len(checks),
            note=figure_checks['evaluation_scope'])
    path=EXP/'reports/comparison.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    for tool in report['tools']:
        print(json.dumps(tool['summary']))


if __name__=='__main__':
    main()
