"""Run one extraction tool sequentially on the frozen biology page set.

Reference XML is never read by this inference runner. It is used only by the
separate evaluator. GPU visibility must be restricted to one device by the
launch command. Raw output and the exact runtime settings are retained.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXP=ROOT/'experiments/bio_tool_comparison_v1'
os.environ.setdefault('HF_HOME',str(ROOT/'cache/huggingface'))
os.environ.setdefault('HF_HUB_DISABLE_XET','1')
os.environ.setdefault('OMP_NUM_THREADS','2')
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
os.environ.setdefault('MKL_NUM_THREADS','2')


def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def docling_setup(ocr):
    from extract_docling import make_converter
    from docling.datamodel.base_models import InputFormat
    converter=make_converter(ocr)
    converter.initialize_pipeline(InputFormat.PDF)
    return converter


def docling_extract(converter,case,out):
    from docling_core.types.doc import PictureItem,TableItem
    result=converter.convert(ROOT/case.get('extraction_pdf',case['page_pdf']))
    doc=result.document
    doc.save_as_json(out/'raw_docling.json')
    markdown=doc.export_to_markdown()
    tables=[];figures=[];blocks=[]
    for index,(item,level) in enumerate(doc.iterate_items()):
        p=item.prov[0] if item.prov else None
        bbox=p.bbox.model_dump(mode='json') if p else None
        if isinstance(item,(TableItem,PictureItem)):
            kind='table' if isinstance(item,TableItem) else 'figure'
            image=item.get_image(doc)
            image_name=f'{kind}_{index:03d}.png'
            if image is not None:
                image.save(out/image_name)
            record=dict(id=item.self_ref,caption=item.caption_text(doc),bbox=bbox,
                        image_path=str((out/image_name).relative_to(ROOT)) if image is not None else None)
            if kind=='table':
                record['html']=item.export_to_html(doc=doc)
                tables.append(record)
            else:
                figures.append(record)
        elif hasattr(item,'text'):
            blocks.append(dict(id=item.self_ref,type=item.label.value,text=item.text,bbox=bbox))
    return dict(markdown=markdown,tables=tables,figures=figures,blocks=blocks,
                status=result.status.value,has_layout_geometry=True)


def vlm_setup(tool):
    import torch
    from transformers import AutoProcessor,Qwen2_5_VLForConditionalGeneration,Qwen2VLForConditionalGeneration
    if torch.cuda.device_count()!=1:
        raise RuntimeError('GPU launch must expose exactly one device')
    torch.set_num_threads(2);torch.set_num_interop_threads(1)
    torch.manual_seed(0)
    name='olmocr' if tool=='olmocr' else 'mineru'
    record=json.loads((EXP/'models'/f'{name}.json').read_text())
    if tool=='olmocr':
        selection=json.loads((ROOT/'config/extraction.json').read_text())
        if any(record[key]!=selection[key] for key in ['model','revision']):
            raise RuntimeError('olmOCR model record does not match the selected model and revision')
    model_class=Qwen2_5_VLForConditionalGeneration if tool=='olmocr' else Qwen2VLForConditionalGeneration
    model=model_class.from_pretrained(record['path'],torch_dtype=torch.bfloat16,
        attn_implementation='sdpa',local_files_only=True).eval().to('cuda:0')
    processor=AutoProcessor.from_pretrained(record['path'],use_fast=tool=='mineru',local_files_only=True)
    if tool=='mineru':
        from mineru_vl_utils import MinerUClient
        from mineru_vl_utils.vlm_client.base_client import SamplingParams
        params={kind:SamplingParams(temperature=0.0,max_new_tokens=8192,no_repeat_ngram_size=100)
                for kind in ['table','equation','image','chart','[default]','[layout]']}
        client=MinerUClient(backend='transformers',model=model,processor=processor,
            image_analysis=True,batch_size=1,max_concurrency=1,use_tqdm=False,
            sampling_params=params)
    else:
        client=None
    return model,processor,client,record


def vlm_extract(tool,setup,case,out,generation_timeout_seconds=None):
    import torch
    from PIL import Image
    model,processor,client,record=setup
    image=Image.open(ROOT/case['image']).convert('RGB')
    if tool=='mineru':
        from mineru_vl_utils.post_process import json2md
        objects=client.two_step_extract(image)
        blocks=[dict(b) if isinstance(b,dict) else (b.to_dict() if hasattr(b,'to_dict') else vars(b)) for b in objects]
        save(out/'raw_mineru.json',blocks)
        markdown=json2md(objects)
        tables=[dict(id=f'table:{index}',html=b.get('content') or '',bbox=b.get('bbox'),caption='')
                for index,b in enumerate(blocks) if b.get('type')=='table']
        figures=[dict(id=f'figure:{index}',annotation=b.get('content'),bbox=b.get('bbox'),caption='')
                 for index,b in enumerate(blocks) if b.get('type') in ['image','chart']]
        return dict(markdown=markdown,blocks=blocks,tables=tables,figures=figures,
                    has_layout_geometry=True,status='completed')
    image.thumbnail((1288,1288),Image.Resampling.LANCZOS)
    # Exact official olmOCR v4 no-anchoring prompt, retained with raw output.
    prompt=('Attached is one page of a document that you must process. '
      'Just return the plain text representation of this document as if you were reading it naturally. Convert equations to LateX and tables to HTML.\n'
      'If there are any figures or charts, label them with the following markdown syntax ![Alt text describing the contents of the figure](page_startx_starty_width_height.png)\n'
      'Return your output as markdown, with a front matter section on top specifying values for the primary_language, is_rotation_valid, rotation_correction, is_table, and is_diagram parameters.')
    messages=[dict(role='user',content=[dict(type='text',text=prompt),dict(type='image')])]
    text=processor.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
    inputs=processor(text=[text],images=[image],return_tensors='pt',padding=True)
    inputs={name:value.to('cuda:0') for name,value in inputs.items()}
    generation_options=dict(max_new_tokens=12288,do_sample=False)
    if generation_timeout_seconds is not None:
        generation_options['max_time']=generation_timeout_seconds
    with torch.inference_mode():
        generated=model.generate(**inputs,**generation_options)
    new=generated[:,inputs['input_ids'].shape[1]:]
    markdown=processor.batch_decode(new,skip_special_tokens=True)[0]
    (out/'prompt.txt').write_text(prompt+'\n')
    raw_tables=re.findall(r'<table\b[^>]*>.*?</table>',markdown,re.I|re.S)
    tables=[]
    for index,markup in enumerate(raw_tables):
        at=markdown.find(markup)
        tables.append(dict(id=f'table:{index}',html=markup,caption='',char_start=at,
                           preceding_text=markdown[max(0,at-2200):at],following_text=markdown[at+len(markup):at+len(markup)+1800]))
    figures=[dict(id=f'figure:{i}',annotation=m.group(1),image_target=m.group(2),
                  char_start=m.start(),caption='',geometry_status='model_proposal_unverified')
             for i,m in enumerate(re.finditer(r'!\[([^\]]*)\]\(([^)]+)\)',markdown))]
    eos=model.generation_config.eos_token_id
    eos_ids=set(eos if isinstance(eos,list) else [eos])
    ended=bool(new.shape[1]) and int(new[0,-1]) in eos_ids
    status='token_limit' if new.shape[1]==12288 else ('time_limit' if generation_timeout_seconds is not None and not ended else 'completed')
    return dict(markdown=markdown,tables=tables,figures=figures,blocks=[],has_layout_geometry=False,
        status=status,generated_tokens=new.shape[1],generation_timeout_seconds=generation_timeout_seconds,
        image_input_dimensions=list(image.size),prompt_method='official_olmOCR_v4_yaml_no_anchoring')


def main():
    selection=json.loads((ROOT/'config/extraction.json').read_text())
    parser=argparse.ArgumentParser(description='Extract frozen biology pages, defaulting to olmOCR 2.')
    parser.add_argument('--tool',choices=['docling','docling_rapidocr','olmocr','mineru'],
        default=selection['primary_tool'],help='Extraction method (default: %(default)s, selected in config/extraction.json)')
    parser.add_argument('--case',action='append')
    args=parser.parse_args()
    manifest=json.loads((EXP/'inputs/manifest.json').read_text())
    unknown=set(args.case or [])-{case['id'] for case in manifest['cases']}
    if unknown:
        parser.error('Unknown case IDs: '+', '.join(sorted(unknown)))
    cases=[case for case in manifest['cases'] if not args.case or case['id'] in args.case]
    pending=[]
    for case in cases:
        if (EXP/'runs'/args.tool/case['id']/'result.json').exists():
            print('CACHED '+args.tool+' '+case['id'],flush=True)
        else:
            pending.append(case)
    if not pending:
        return
    setup_start=time.monotonic()
    setup=docling_setup(args.tool=='docling_rapidocr') if args.tool.startswith('docling') else vlm_setup(args.tool)
    setup_seconds=time.monotonic()-setup_start
    gpu=args.tool in ['olmocr','mineru']
    for case in pending:
        out=EXP/'runs'/args.tool/case['id']
        out.mkdir(parents=True,exist_ok=True)
        if gpu:
            import torch
            torch.cuda.synchronize();torch.cuda.reset_peak_memory_stats()
        start=time.monotonic()
        inference_case=dict(case)
        if args.tool=='docling_rapidocr':
            inference_case['extraction_pdf']=case['page_image_pdf']
        result=docling_extract(setup,inference_case,out) if args.tool.startswith('docling') else vlm_extract(args.tool,setup,case,out)
        if gpu:
            torch.cuda.synchronize()
        elapsed=time.monotonic()-start
        result.update(tool=args.tool,case_id=case['id'],document_id=case['document_id'],source_page=case['source_page'],
            source_pdf=case['source_pdf'],elapsed_seconds=round(elapsed,3),
            setup_seconds=round(setup_seconds,3),peak_gpu_allocated_gib=round(torch.cuda.max_memory_allocated()/2**30,3) if gpu else 0,
            gpu_visible_devices=os.environ.get('CUDA_VISIBLE_DEVICES'),batch_size=1,
            reference_xml_in_prompt=False,
            input_mode='image_only_pdf' if args.tool=='docling_rapidocr' else ('digital_pdf' if args.tool=='docling' else 'rendered_page_image'))
        if gpu:
            import transformers
            result['model_record']=setup[3]
            result['runtime_versions']=dict(torch=torch.__version__,transformers=transformers.__version__)
            result['precision']='bfloat16';result['attention_implementation']='sdpa'
        (out/'raw.md').write_text(result['markdown'])
        save(out/'result.json',result)
        print(json.dumps({k:result.get(k) for k in ['tool','case_id','status','elapsed_seconds','peak_gpu_allocated_gib','generated_tokens']}),flush=True)


if __name__=='__main__':
    main()
