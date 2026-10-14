"""Ryze-inspired GLM-OCR region recognition, using Docling layout proposals.

This is a hybrid, not the official PP-DocLayoutV3 GLM-OCR SDK. Its input
regions come only from the already-run Docling extractor, never gold XML.
Every text/table region is independently re-read from the rendered page.
"""
import argparse
import copy
import json
import os
import time
from pathlib import Path
os.environ.setdefault('OMP_NUM_THREADS','2')
os.environ.setdefault('MKL_NUM_THREADS','2')
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
ROOT=Path(__file__).resolve().parents[1]
EXP=ROOT/'experiments/bio_tool_comparison_v1'
os.environ.setdefault('HF_HOME',str(ROOT/'cache/huggingface'))
from run_bio_tool import save
from evaluate_bio_tools import normalized_bbox


def main():
    import torch
    from PIL import Image
    from transformers import AutoProcessor,GlmOcrForConditionalGeneration
    parser=argparse.ArgumentParser();parser.add_argument('--case',action='append')
    args=parser.parse_args()
    assert torch.cuda.device_count()==1
    torch.set_num_threads(2);torch.set_num_interop_threads(1);torch.manual_seed(0)
    record=json.loads((EXP/'models/glmocr.json').read_text())
    start=time.monotonic()
    model=GlmOcrForConditionalGeneration.from_pretrained(record['path'],dtype=torch.bfloat16,
        attn_implementation='sdpa',local_files_only=True).eval().to('cuda:0')
    processor=AutoProcessor.from_pretrained(record['path'],local_files_only=True)
    setup=time.monotonic()-start
    manifest=json.loads((EXP/'inputs/manifest.json').read_text())
    for case in manifest['cases']:
        if args.case and case['id'] not in args.case:
            continue
        out=EXP/'runs/glmocr_docling'/case['id'];out.mkdir(parents=True,exist_ok=True)
        if (out/'result.json').exists():
            print('CACHED '+case['id'],flush=True);continue
        base=json.loads((EXP/'runs/docling'/case['id']/'result.json').read_text())
        result=copy.deepcopy(base)
        image=Image.open(ROOT/case['image']).convert('RGB')
        torch.cuda.synchronize();torch.cuda.reset_peak_memory_stats();start=time.monotonic()
        region_records=[]
        def recognize(item,task,index,max_tokens):
            bb=normalized_bbox(item.get('bbox'),case)
            if bb is None:
                return ''
            w,h=image.size;pad=0.004
            box=[max(0,int((bb[0]-pad)*w)),max(0,int((bb[1]-pad)*h)),
                 min(w,int((bb[2]+pad)*w)),min(h,int((bb[3]+pad)*h))]
            crop=image.crop(box)
            crop_path=out/f'{task}_{index:03d}.png';crop.save(crop_path)
            prompt={'text':'Text Recognition:','table':'Table Recognition:','figure':'Text Recognition:'}[task]
            messages=[dict(role='user',content=[dict(type='image',image=crop),dict(type='text',text=prompt)])]
            inputs=processor.apply_chat_template(messages,tokenize=True,add_generation_prompt=True,
                return_dict=True,return_tensors='pt').to('cuda:0')
            region_start=time.monotonic()
            with torch.inference_mode():
                outputs=model.generate(**inputs,max_new_tokens=max_tokens,do_sample=False)
            new=outputs[:,inputs['input_ids'].shape[-1]:]
            text=processor.batch_decode(new,skip_special_tokens=True)[0]
            raw_path=out/f'{task}_{index:03d}.txt';raw_path.write_text(text+'\n')
            region_records.append(dict(type=task,index=index,prompt=prompt,input_bbox=bb,
                crop_bbox_pixels=box,image_path=str(crop_path.relative_to(ROOT)),
                raw_text_path=str(raw_path.relative_to(ROOT)),generated_tokens=new.shape[1],
                token_limit=new.shape[1]==max_tokens,seconds=round(time.monotonic()-region_start,3)))
            print('REGION '+case['id']+' '+task+' '+str(index)+' '+str(new.shape[1]),flush=True)
            return text
        for index,block in enumerate(result['blocks']):
            if block.get('type') in ['page_header','page_footer']:
                continue
            block['native_text_before_ocr']=block['text']
            block['text']=recognize(block,'text',index,4096)
            block['recognition_method']='GLM-OCR:Text Recognition:'
        for index,table in enumerate(result['tables']):
            table['native_html_before_ocr']=table['html']
            table['html']=recognize(table,'table',index,8192)
            table['native_caption_before_ocr']=table['caption']
            table['caption']=''  # The common binder attaches the newly read captions.
            # Read a fixed strip above every detected table to recover captions
            # that the layout engine omitted. No expected labels are supplied.
            bb=normalized_bbox(table.get('bbox'),case)
            if bb and bb[1]>0:
                context=dict(id=f'glm_caption_context:{index}',type='text',
                    bbox=[max(0,bb[0]-0.02),max(0,bb[1]-0.085),min(1,bb[2]+0.02),bb[1]],
                    region_kind='fixed_above_table_context')
                context['text']=recognize(context,'text',1000+index,2048)
                result['blocks'].append(context)
        for index,figure in enumerate(result['figures']):
            figure['annotation']=recognize(figure,'figure',index,3072)
            figure['annotation_kind']='visible_text_OCR; not validated chart digitization'
            figure['native_caption_before_ocr']=figure['caption'];figure['caption']=''
        # All raw native values are preserved above, but not mixed into the OCR Markdown.
        markdown='\n\n'.join([b['text'] for b in result['blocks']]+[t['html'] for t in result['tables']])
        torch.cuda.synchronize();gpu_seconds=time.monotonic()-start
        result.update(tool='glmocr_docling',markdown=markdown,status='token_limit' if any(r['token_limit'] for r in region_records) else 'completed',
            elapsed_seconds=round(gpu_seconds+base['elapsed_seconds'],3),
            recognition_seconds=round(gpu_seconds,3),layout_seconds=base['elapsed_seconds'],
            setup_seconds=round(setup+base['setup_seconds'],3),
            peak_gpu_allocated_gib=round(torch.cuda.max_memory_allocated()/2**30,3),
            gpu_visible_devices=os.environ.get('CUDA_VISIBLE_DEVICES'),batch_size=1,
            reference_xml_in_prompt=False,input_mode='rendered_page_regions_from_Docling_layout',
            pipeline_note='Custom Docling-layout + GLM-OCR region hybrid; official GLM-OCR PP-DocLayoutV3 SDK not executed.',
            regions=region_records)
        import transformers
        result['model_record']=record
        result['runtime_versions']=dict(torch=torch.__version__,transformers=transformers.__version__)
        result['precision']='bfloat16';result['attention_implementation']='sdpa'
        (out/'raw.md').write_text(markdown);save(out/'result.json',result)
        print(json.dumps({k:result[k] for k in ['tool','case_id','status','elapsed_seconds','peak_gpu_allocated_gib']}),flush=True)


if __name__=='__main__':
    main()
