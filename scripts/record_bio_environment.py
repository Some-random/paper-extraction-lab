"""Record selected runtime versions without importing or initializing models."""
import argparse
import hashlib
import json
import sys
from importlib.metadata import version,PackageNotFoundError
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXP=ROOT/'experiments/bio_tool_comparison_v1'
parser=argparse.ArgumentParser();parser.add_argument('name');args=parser.parse_args()
packages={}
for name in ['torch','torchvision','transformers','pymupdf','docling','docling-core',
             'rapidocr','mineru-vl-utils','numpy','Pillow','huggingface-hub','lxml']:
    try:
        packages[name]=version(name)
    except PackageNotFoundError:
        packages[name]=None
files=list((ROOT/'src').glob('*bio*.py'))+list((ROOT/'scripts').glob('*bio*.py'))+[
    ROOT/'src/run_glm_regions.py',ROOT/'src/extract_native.py',ROOT/'src/extract_docling.py',
    ROOT/'scripts/download_model_sequential.py']
record=dict(python=sys.version,executable=sys.executable,packages=packages,
    source_code_snapshot_at_report_completion={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
    note='Project-local packages with read-only reuse of an existing Torch runtime. Model identities/configurations are retained in individual raw run results. Evaluation formatting adapters were finalized after inspecting source/output syntax.')
path=EXP/'models'/f'environment_{args.name}.json';path.write_text(json.dumps(record,indent=2)+'\n')
print(str(path))
