"""Freeze a biology-only corpus, diagnostic pages and source-based references."""
import hashlib
import json
import re
import sys
from datetime import datetime,timedelta,timezone
from pathlib import Path

import pymupdf as fitz
from lxml import etree

ROOT=Path(__file__).resolve().parents[1]
EXP=ROOT/'experiments/bio_tool_comparison_v1'
sys.path.insert(0,str(ROOT/'src'))
from extract_native import text_of,normalize,dump
from build_samples import html_grid

SOURCES={
 'her2_affibody':dict(pages=[8,11,12],pmcid='PMC8617914',
   doi='10.3390/pharmaceutics13111974',url='https://mdpi-res.com/d_attachment/pharmaceutics/pharmaceutics-13-01974/article_deploy/pharmaceutics-13-01974.pdf'),
 'cd69':dict(pages=[5,6,8],pmcid='PMC8476556',doi='10.1038/s41598-021-97694-6',
   url='https://www.nature.com/articles/s41598-021-97694-6.pdf'),
 'plasma_peptides':dict(pages=[5,6,8],pmcid='PMC9918186',doi='10.3390/ijms24032836',
   url='https://mdpi-res.com/d_attachment/ijms/ijms-24-02836/article_deploy/ijms-24-02836.pdf'),
}


def key(label):
    match=re.search(r'(Figure|Fig\.?|Table)\s*(\d+)',label,re.I)
    return ('table' if match.group(1).lower()=='table' else 'figure')+':'+match.group(2) if match else None


def main():
    documents=[]; cases=[]; reference=[]
    for doc_id,settings in SOURCES.items():
        pdf_path=EXP/'inputs'/f'{doc_id}.pdf'
        xml_path=EXP/'inputs'/f'{doc_id}.xml'
        tree=etree.parse(str(xml_path),etree.XMLParser(resolve_entities=False,no_network=True))
        title=text_of(tree.find('front/article-meta/title-group/article-title'))
        pdf=fitz.open(pdf_path)
        captions={}
        for pnum,page in enumerate(pdf,1):
            for block in page.get_text('blocks'):
                if block[6]!=0:
                    continue
                match=re.match(r'^\s*(Table|Figure|Fig\.)\s+(\d+)\s*[.:]',block[4])
                if match:
                    label=key(match.group(0))
                    captions[label]=dict(page=pnum,bbox=list(block[:4]),text=normalize(block[4]))
        record=dict(document_id=doc_id,title=title,pages=len(pdf),selected_pages=settings['pages'],
            pmcid=settings['pmcid'],doi=settings['doi'],pdf_url=settings['url'],
            xml_url=f"https://www.ebi.ac.uk/europepmc/webservices/rest/{settings['pmcid']}/fullTextXML",
            pdf_path=str(pdf_path.relative_to(ROOT)),xml_path=str(xml_path.relative_to(ROOT)),
            pdf_sha256=hashlib.sha256(pdf_path.read_bytes()).hexdigest(),xml_sha256=hashlib.sha256(xml_path.read_bytes()).hexdigest())
        documents.append(record)
        for pnum in settings['pages']:
            page=pdf[pnum-1]
            case_id=f'{doc_id}_p{pnum:03d}'
            image_path=EXP/'inputs/pages'/f'{case_id}.png'
            image_path.parent.mkdir(parents=True,exist_ok=True)
            page.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(image_path)
            single_path=EXP/'inputs/pages'/f'{case_id}.pdf'
            single=fitz.open(); single.insert_pdf(pdf,from_page=pnum-1,to_page=pnum-1)
            single.save(single_path); single.close()
            cases.append(dict(id=case_id,document_id=doc_id,source_page=pnum,
                source_pdf=str(pdf_path.relative_to(ROOT)),page_pdf=str(single_path.relative_to(ROOT)),
                image=str(image_path.relative_to(ROOT)),native_text=page.get_text(),
                width=page.rect.width,height=page.rect.height,
                evaluation_labels=[label for label,cap in captions.items() if cap['page']==pnum]))
        for node in tree.xpath('//fig | //table-wrap'):
            label=key(text_of(node.find('label')))
            cap=captions.get(label)
            if not cap or cap['page'] not in settings['pages']:
                continue
            xml_id=node.get('id')
            related=[]
            for index,p in enumerate(tree.xpath('//body//p[not(ancestor::fig) and not(ancestor::table-wrap)]')):
                if any(xml_id in (x.get('rid') or '').split() for x in p.findall('.//xref')):
                    related.append(dict(id=f'{doc_id}:xml:p{index}',text=text_of(p),xpath=tree.getpath(p)))
            item=dict(id=f'{doc_id}:{label}',document_id=doc_id,case_id=f"{doc_id}_p{cap['page']:03d}",
                kind='table' if node.tag=='table-wrap' else 'figure',label=label,
                caption=text_of(node.find('caption')),caption_source_bbox=cap['bbox'],
                xml_id=xml_id,source_xpath=tree.getpath(node),referring_paragraphs=related,
                table_notes=text_of(node.find('table-wrap-foot')))
            table=node.find('.//table')
            if table is not None:
                item['table_html']=etree.tostring(table,encoding='unicode')
                item['grid']=html_grid(item['table_html'])
            reference.append(item)
        pdf.close()
    table_cells=sum((r['grid']['nrows']-r['grid']['header_rows'])*(r['grid']['ncols']-1) for r in reference if r['kind']=='table')
    manifest=dict(frozen_at_pst=datetime.now(timezone(timedelta(hours=-8))).isoformat(),
        scope='Three empirical biology papers; method papers excluded. Nine exploratory diagnostic pages, frozen before GPU model inference.',
        documents=documents,cases=cases,
        reference=dict(method='native publisher JATS silver reference plus rendered-page anchors',
            path='experiments/bio_tool_comparison_v1/reference/elements.json',
            figures=sum(r['kind']=='figure' for r in reference),tables=sum(r['kind']=='table' for r in reference),
            body_value_cells=table_cells),
        metrics=['body_cell_exact_match_best_matrix','body_cell_exact_match_caption_bound',
                 'table_header_preservation','caption_text_recall','scientific_notation_and_missing_values',
                 'elapsed_inference_seconds','peak_gpu_allocated_gib'],
        fairness=dict(input_pages_identical=True,native_xml_provided_to_models=False,
            tool_specific_preprocessing='Official/documented rendering and prompts; recorded per run',
            all_workers=1,max_gpus=1,allowed_tools=['Docling','Docling_RapidOCR','olmOCR-2','MinerU2.5-Pro']))
    dump(EXP/'inputs/manifest.json',manifest); dump(EXP/'reference/elements.json',reference)
    print(json.dumps(dict(papers=len(documents),cases=len(cases),tables=manifest['reference']['tables'],
                          figures=manifest['reference']['figures'],body_value_cells=table_cells)),flush=True)


if __name__=='__main__':
    main()
