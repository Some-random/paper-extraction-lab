"""Download one pinned open model with one file worker, retaining provenance."""
import argparse
import json
import os
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
os.environ['HF_HOME']=str(ROOT/'cache/huggingface')
os.environ['HF_HUB_DISABLE_XET']='1'
os.environ['HF_HUB_ENABLE_HF_TRANSFER']='0'
from huggingface_hub import HfApi,snapshot_download

parser=argparse.ArgumentParser()
parser.add_argument('model')
parser.add_argument('--record',required=True)
args=parser.parse_args()
for attempt in range(3):
    try:
        info=HfApi().model_info(args.model,files_metadata=True,timeout=30)
        break
    except Exception as exc:
        if attempt==2:
            raise
        print('METADATA_RETRY '+type(exc).__name__,flush=True)
        time.sleep(5*(attempt+1))
files=[x for x in info.siblings if x.rfilename.endswith(('.safetensors','.json','.txt','.model','.jinja'))]
size=sum(x.size or 0 for x in files)
print(json.dumps(dict(model=args.model,revision=info.sha,selected_bytes=size,download_workers=1)),flush=True)
path=snapshot_download(args.model,revision=info.sha,max_workers=1,
    allow_patterns=['*.safetensors','*.json','*.txt','*.model','*.jinja'])
record=Path(args.record)
record.parent.mkdir(parents=True,exist_ok=True)
record.write_text(json.dumps(dict(model=args.model,revision=info.sha,path=path,selected_bytes=size,
    download_workers=1),indent=2)+'\n')
print('MODEL_READY '+str(record),flush=True)
