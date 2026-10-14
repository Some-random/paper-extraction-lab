"""Build source-native Ryze-style evidence packages for the actual bio corpus.

This structured-XML branch is separate from PDF tool evaluation. Explicit
JATS cross-references link source captions/tables to interpreting paragraphs.
Figures include honestly labeled full-page evidence, not invented crops.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
import pymupdf as fitz
from lxml import etree
from extract_native import text_of
from bio_table_metrics import parse_table,table_records

ROOT=Path(__file__).resolve().parents[1]
EXP=ROOT/'experiments/bio_tool_comparison_v1'
OUT=EXP/'evidence';OUT.mkdir(parents=True,exist_ok=True)


def label_key(text):
    m=re.search(r'(Table|Figure|Fig\.?)\s*(\d+)',text,re.I)
    return ('table' if m[1].lower()=='table' else 'figure')+':'+m[2] if m else None


def main():
    manifest=json.loads((EXP/'inputs/manifest.json').read_text())
    bundles=[]
    for document in manifest['documents']:
        doc_id=document['document_id']
        tree=etree.parse(str(ROOT/document['xml_path']),etree.XMLParser(resolve_entities=False,no_network=True))
        pdf=fitz.open(ROOT/document['pdf_path'])
        anchors={}
        for pnum,page in enumerate(pdf,1):
            for block in page.get_text('blocks'):
                if block[6]!=0:
                    continue
                m=re.match(r'^\s*(Table|Figure|Fig\.)\s+(\d+)\s*[.:]',block[4])
                if not m:
                    continue
                key=label_key(m[0]);anchors.setdefault(key,[]).append(dict(page=pnum,bbox=list(block[:4]),native_text=block[4]))
        paragraphs=tree.xpath('//body//p[not(ancestor::fig) and not(ancestor::table-wrap)]')
        for node in tree.xpath('//fig | //table-wrap'):
            label=text_of(node.find('label'));key=label_key(label);xml_id=node.get('id')
            context=[]
            for i,p in enumerate(paragraphs):
                if any(xml_id in (x.get('rid') or '').split() for x in p.findall('.//xref')):
                    section=p.xpath('ancestor::sec[1]/title')
                    context.append(dict(id=f'{doc_id}:xml:p{i}',text=text_of(p),
                        xpath=tree.getpath(p),section=text_of(section[0]) if section else '',
                        binding_method='explicit_JATS_xref'))
            source_anchors=anchors.get(key,[])
            flags=[]
            images=[]
            for anchor in source_anchors:
                page=anchor['page'];image=OUT/'pages'/f'{doc_id}_p{page:03d}.png'
                image.parent.mkdir(parents=True,exist_ok=True)
                if not image.exists():
                    pdf[page-1].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(image)
                images.append(dict(path=str(image.relative_to(ROOT)),source_page=page,
                    scope='full_source_page',caption_bbox=anchor['bbox'],dpi=144))
            if not images:
                flags.append('no_native_PDF_caption_page_anchor')
            if node.tag=='fig':
                flags.append('full_page_visual; figure_region_not_independently_verified')
            if not context:
                flags.append('no_explicit_referring_paragraph')
            bundle=dict(id=f'{doc_id}:{key}',document_id=doc_id,document_title=document['title'],
                kind='table' if node.tag=='table-wrap' else 'figure',label=label,caption=text_of(node.find('caption')),
                table_notes=text_of(node.find('table-wrap-foot')),referring_paragraphs=context,
                source_xpath=tree.getpath(node),xml_id=xml_id,source_xml=document['xml_path'],
                source_xml_sha256=document['xml_sha256'],source_pdf=document['pdf_path'],
                source_pdf_sha256=document['pdf_sha256'],images=images,
                extraction_method='publisher JATS + explicit xref + native PDF caption-page anchors',
                source_branch='structured_publisher_source; excluded from PDF model inputs',
                quality_flags=flags,training_status='evidence pipeline sample; semantic review pending')
            table=node.find('.//table')
            if table is not None:
                bundle['table_html']=etree.tostring(table,encoding='unicode')
                bundle['scientific_grid']=parse_table(bundle['table_html'])
                bundle['logical_table']=table_records(bundle['scientific_grid'])
            bundles.append(bundle)
        pdf.close()
    samples=[]
    for b in bundles:
        if b['kind']!='table':
            continue
        table=b['logical_table']
        for row in table['records'][:1]:
            for ci,value in enumerate(row['cells'][:2],1):
                if not value:
                    continue
                samples.append(dict(id=f'qa:{len(samples):03d}',document_id=b['document_id'],
                    question=f"In {b['label']}, what is reported for {table['headers'][ci]} for {row['key']}?",
                    answer=value,evidence_ids=[b['id']],
                    source_location=dict(row_key=row['key'],column=ci,header=table['headers'][ci]),
                    generation_method='deterministic_source_table_lookup',
                    validation='exact_source_cell_replay; not teacher-generated reasoning',
                    training_status='pipeline example only'))
    facts=[]
    for b in bundles:
        if b['kind']!='table':
            continue
        table=b['logical_table']
        for row in table['records']:
            for ci,value in enumerate(row['cells'],1):
                facts.append(dict(document_id=b['document_id'],evidence_id=b['id'],row_key=row['key'],
                    quantity_header=table['headers'][ci],reported_value=value,column=ci,
                    source_cell_origins=row['cell_origins'][ci-1],notes=b['table_notes'],
                    numeric_conversion_performed=False,scientific_label_inferred=False))
    ablation=[dict(evidence_id=b['id'],caption_words=len(b['caption'].split()),
        referring_paragraphs=len(b['referring_paragraphs']),
        rich_context_words=len(b['caption'].split())+sum(len(p['text'].split()) for p in b['referring_paragraphs'])) for b in bundles]
    for name,records in [('bundles',bundles),('qa_samples',samples),('reported_cells',facts),('context_ablation',ablation)]:
        (OUT/f'{name}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
    # Verify every sample against its actual source table, not a copied answer field.
    by_id={b['id']:b for b in bundles}
    for q in samples:
        b=by_id[q['evidence_ids'][0]];loc=q['source_location']
        row=next(r for r in b['logical_table']['records'] if r['key']==loc['row_key'])
        assert q['answer']==row['cells'][loc['column']-1]
    result=dict(biological_papers=len(manifest['documents']),bundles=len(bundles),
        figures=sum(b['kind']=='figure' for b in bundles),tables=sum(b['kind']=='table' for b in bundles),
        with_explicit_context=sum(bool(b['referring_paragraphs']) for b in bundles),
        with_source_page=sum(bool(b['images']) for b in bundles),
        lookup_qa_samples=len(samples),lookup_qa_replayed=len(samples),reported_logical_cells=len(facts),
        caption_words_total=sum(a['caption_words'] for a in ablation),
        rich_context_words_total=sum(a['rich_context_words'] for a in ablation),
        note='Native-XML evidence branch; all raw references retained. Full-page image evidence does not constitute chart digitization or verified region extraction.')
    (OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':
    main()
