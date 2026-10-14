"""Compare the targeted Affibody OCR repair to the article's XML tables."""
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from audit_samples import check_rows
from build_samples import html_grid
from extract_native import dump

scan=json.loads((ROOT/'outputs/docling/affibody_scan_p11/evidence.json').read_text())
jats=json.loads((ROOT/'outputs/jats/affibody/document.json').read_text())
records=[]
for label in ['Table 3','Table 4']:
    source=next(b for b in jats['bundles'] if b['label']==label)
    gold=html_grid(source['table_html'])
    expected=[[c['text'] for c in row] for row in gold['rows'][gold['header_rows']:]]
    target=label.replace('Table ','table:')
    matching=[b for b in scan['bundles'] if b.get('label')==target]
    observed=[[c['text'] for c in row] for row in html_grid(matching[0]['table_html'])['rows']] if len(matching)==1 else []
    checks=check_rows(observed,expected)
    records.append(dict(table=label,passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks))
dump(ROOT/'outputs/targeted_ocr_audit.json',dict(document='affibody_scan_p11',source_page=11,
    derived_scan_dpi=144,comparisons=records,
    limitation='Targeted exploratory repair test selected after the native-text failure; not held-out evaluation.',
    remaining_issue='Table 3 header superscript a was recognized as ª; cell checks do not validate all header or footnote characters.'))
print(json.dumps([dict(table=x['table'],passed=x['passed'],total=x['total']) for x in records]))
