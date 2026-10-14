"""Add linebreak/power-aware silver-reference cells before GPU inference."""
import hashlib
import json
import shutil
import sys
from datetime import datetime,timedelta,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from bio_table_metrics import parse_table,table_records,compare
EXP=ROOT/'experiments/bio_tool_comparison_v1'
ref_path=EXP/'reference/elements.json'
manifest_path=EXP/'inputs/manifest.json'
for path in [ref_path,manifest_path]:
    backup=path.with_name(path.stem+'_original_grid_v0.json')
    if not backup.exists():
        shutil.copy2(path,backup)
refs=json.loads(ref_path.read_text())
for source in refs:
    if source['kind']!='table':
        continue
    source['scientific_grid']=parse_table(source['table_html'])
    source['logical_table']=table_records(source['scientific_grid'])
    own=compare(source,source['table_html'])
    assert own['matched']==own['total'],source['id']
    assert own['header_matched']==own['header_total'],source['id']
    print(source['id'],own['total'],own['header_total'])
ref_path.write_text(json.dumps(refs,ensure_ascii=False,indent=2)+'\n')
manifest=json.loads(manifest_path.read_text())
manifest['reference']['body_value_cells']=sum(sum(len(row['cells']) for row in r['logical_table']['records']) for r in refs if r['kind']=='table')
manifest['reference']['refined_at_pst']=datetime.now(timezone(timedelta(hours=-8))).isoformat()
manifest['reference']['normalization']='Source logical cells: preserve line breaks, spans, powers and signs; full-width group labels become row context, not body values. Align row labels and column positions; whole multi-value cell must match.'
manifest['reference']['amendment']='Original flat-grid reference is retained as *_original_grid_v0.json. Source-only refinement after CPU extraction and before GPU inference/scoring; no model results were used to select expected values.'
manifest['reference']['sha256']=hashlib.sha256(ref_path.read_bytes()).hexdigest()
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('FROZEN',manifest['reference']['body_value_cells'],'source logical value cells')
