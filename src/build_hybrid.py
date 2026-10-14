"""Prefer explicit XML; combine PDF captions, layout tables, and source pages.

Full-page image fallback retains vector figures and multi-panel content when
the layout model emits incomplete or ambiguous crops. It is explicitly a
full page, not a claim that an individual figure was correctly segmented.
"""
import copy
import json
from pathlib import Path
import re

from extract_native import CAPTION, dump, normalize

ROOT = Path(__file__).resolve().parents[1]


def caption_label(text):
    match=CAPTION.match(normalize(text))
    if not match:
        return None
    return ('table' if match.group(1).lower()=='table' else 'figure')+':'+match.group(2)


def overlap(first,second):
    width=max(0,min(first['r'],second['r'])-max(first['l'],second['l']))
    return width/max(1,min(first['r']-first['l'],second['r']-second['l']))


def spatially_consistent(bundle,elements):
    prov=bundle.get('source_provenance')
    if not prov:
        return False
    caption_elements=[e for e in elements if e['source_ref'] in bundle.get('caption_ref_ids',[])]
    return bool(caption_elements) and all(e.get('source_provenance') and
        e['source_provenance']['page']==prov['page'] and
        overlap(prov['bbox'],e['source_provenance']['bbox'])>0.35 for e in caption_elements)


def main():
    jats=json.loads((ROOT/'outputs/jats/affibody/document.json').read_text())
    native=json.loads((ROOT/'outputs/native/affibody/document.json').read_text())
    output=[]
    for b in jats['bundles']:
        item=copy.deepcopy(b)
        key=caption_label(b['label']+'.')
        anchor=next((e for e in native['elements'] if e.get('label')==key),None)
        item['id']='affibody:hybrid:'+b['xml_id']
        item['source_path']=jats['source_path']
        item['source_sha256']=jats['sha256']
        item['method']='native_JATS+source_PDF_page'
        item['canonical_label']=key
        item['quality_flags']=[]
        if anchor:
            item['image_path']=f"outputs/native/affibody/pages/page_{anchor['page']:03d}.png"
            item['image_scope']='full_source_page'
            item['image_provenance']=dict(source_path=native['source_path'],sha256=native['sha256'],page=anchor['page'])
        else:
            item['quality_flags'].append('no_matching_source_page')
        output.append(item)
    layout_flags=[]
    for doc_id in ['ryze','llava_med','ryze_scan_p5']:
        native=json.loads((ROOT/'outputs/native'/doc_id/'document.json').read_text())
        parsed=json.loads((ROOT/'outputs/docling'/doc_id/'evidence.json').read_text())
        captions={e['label']:e for e in native['elements'] if e['kind']=='caption'}
        for b in parsed['bundles']:
            primary=caption_label(b.get('caption',''))
            if primary and primary not in captions:
                cap=next((e for e in parsed['elements'] if e['source_ref'] in b['caption_ref_ids']),None)
                captions[primary]=dict(text=b['caption'],page=b['source_provenance']['page'],
                                       source_provenance=cap['source_provenance'] if cap else None,
                                       extraction_method='Docling_caption')
            if b.get('caption') and not spatially_consistent(b,parsed['elements']):
                layout_flags.append(dict(document_id=doc_id,region_id=b['id'],
                    flag='caption_spatial_conflict',caption=b['caption'][:180]))
        for label,cap in captions.items():
            kind=label.split(':')[0]
            page=cap['page']
            related=[e for e in native['elements'] if e['kind']=='text' and label in e['references']]
            if not related:
                related=[e for e in parsed['elements'] if e['kind'] not in ['caption','page_header','page_footer']
                         and label in e['references'] and caption_label(e['text']) is None]
            item=dict(id=f'{doc_id}:hybrid:{label}',document_id=doc_id,kind=kind,label=label,
                canonical_label=label,caption=cap['text'],caption_provenance=cap,
                source_path=native['source_path'],source_sha256=native['sha256'],
                method='native_PDF_caption+Docling_structure+source_page',
                image_path=f'outputs/native/{doc_id}/pages/page_{page:03d}.png',image_scope='full_source_page',
                referring_paragraphs=related,referring_paragraph_ids=[e['id'] for e in related],
                binding_method='explicit_label_mentions',quality_flags=[],
                status='source_extracted; scientific_and_visual_review_pending')
            options=[b for b in parsed['bundles'] if b['kind']==kind and b['source_provenance']['page']==page
                     and caption_label(b.get('caption',''))==label and spatially_consistent(b,parsed['elements'])]
            if not options and kind=='table' and cap.get('source_provenance'):
                capbox=cap['source_provenance']['bbox']
                nearby=[]
                for candidate in parsed['bundles']:
                    prov=candidate['source_provenance']
                    if candidate['kind']!=kind or prov['page']!=page or overlap(capbox,prov['bbox'])<0.6:
                        continue
                    box=prov['bbox']
                    # Both are Docling BOTTOMLEFT coordinates. Support captions
                    # either above or below the table, with a conservative gap.
                    gap=max(0,max(capbox['b'],box['b'])-min(capbox['t'],box['t']))
                    primary=caption_label(candidate.get('caption',''))
                    if gap<=60 and (primary is None or primary==label):
                        nearby.append(candidate)
                if len(nearby)==1:
                    options=nearby
                    item['binding_method']='explicit_label_mentions+caption_geometry_repair'
                    item['quality_flags'].append('caption_geometry_repaired; review_pending')
            if len(options)==1:
                region=options[0]
                item['region_crop']=region['image_path']
                item['region_provenance']=region['source_provenance']
                if kind=='table':
                    item['table_html']=region['table_html']
                    item['table_cells']=region['table_cells']
            elif kind=='table':
                item['quality_flags'].append('table_structure_unresolved')
            if not related:
                item['quality_flags'].append('no_explicit_referring_text_found')
            output.append(item)
    # Also audit layout regions for the XML-backed paper without replacing XML.
    parsed=json.loads((ROOT/'outputs/docling/affibody/evidence.json').read_text())
    for b in parsed['bundles']:
        if b.get('caption') and not spatially_consistent(b,parsed['elements']):
            layout_flags.append(dict(document_id='affibody',region_id=b['id'],flag='caption_spatial_conflict',caption=b['caption'][:180]))
        primary=caption_label(b.get('caption',''))
        if primary and primary.split(':')[0]!=b['kind']:
            layout_flags.append(dict(document_id='affibody',region_id=b['id'],flag='caption_and_region_type_conflict',caption=b['caption'][:180]))
    dump(ROOT/'outputs/hybrid_evidence.json',output)
    (ROOT/'outputs/hybrid_evidence.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in output))
    dump(ROOT/'outputs/layout_binding_flags.json',layout_flags)
    print(json.dumps(dict(hybrid_bundles=len(output),source_page_images=sum(bool(b.get('image_path')) for b in output),
                          layout_binding_flags=len(layout_flags))),flush=True)


if __name__=='__main__':
    main()
