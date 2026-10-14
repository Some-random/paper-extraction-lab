"""Same rendered pages as text-free PDFs for the dedicated OCR baseline."""
import hashlib
import json
import shutil
from pathlib import Path
import pymupdf as fitz

ROOT=Path(__file__).resolve().parents[1]
EXP=ROOT/'experiments/bio_tool_comparison_v1'
path=EXP/'inputs/manifest.json'
manifest=json.loads(path.read_text())
for case in manifest['cases']:
    image=ROOT/case['image']
    output=image.with_name(image.stem+'_image_only.pdf')
    pdf=fitz.open()
    page=pdf.new_page(width=case['width'],height=case['height'])
    page.insert_image(page.rect,filename=str(image))
    assert not page.get_text()
    pdf.save(output);pdf.close()
    case['page_image_pdf']=str(output.relative_to(ROOT))
    case['image_sha256']=hashlib.sha256(image.read_bytes()).hexdigest()
    case['page_pdf_sha256']=hashlib.sha256((ROOT/case['page_pdf']).read_bytes()).hexdigest()
    case['page_image_pdf_sha256']=hashlib.sha256(output.read_bytes()).hexdigest()
manifest['fairness']['input_modes']='Docling: digital one-page PDF; dedicated Docling+RapidOCR: text-free PDF of the exact 144-dpi rendered page; VLMs: same rendered page with documented model preprocessing.'
manifest['fairness']['ocr_baseline_note']='The initial OCR-on-digital diagnostic retained duplicate native table text. Preserved as docling_rapidocr_digital; the main OCR baseline is rerun on text-free rendered PDFs.'
path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
run=EXP/'runs/docling_rapidocr'
backup=EXP/'runs/docling_rapidocr_digital'
if run.exists() and not backup.exists():
    run.rename(backup)
log=EXP/'logs/docling_rapidocr.log'
if log.exists():
    shutil.copy2(log,EXP/'logs/docling_rapidocr_digital.log')
print('Prepared 9 text-free PDFs; original digital-OCR outputs preserved.')
