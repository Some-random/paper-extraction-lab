"""A controlled raster-only copy of an existing page; no new scientific content."""
import hashlib
import json
import argparse
from pathlib import Path
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--doc',default='ryze')
parser.add_argument('--page',type=int,default=5)
parser.add_argument('--output-id',default='ryze_scan_p5')
args=parser.parse_args()
source = ROOT / 'inputs' / (args.doc+'.pdf')
with fitz.open(source) as doc:
    page = doc[args.page-1]
    pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    output = fitz.open()
    new_page = output.new_page(width=page.rect.width, height=page.rect.height)
    new_page.insert_image(new_page.rect, stream=pixmap.tobytes("png"))
    target = ROOT / 'inputs' / (args.output_id+'.pdf')
    output.save(target)
    assert new_page.get_text().strip() == ""
    output.close()
(ROOT / 'inputs' / (args.output_id+'.provenance.json')).write_text(json.dumps(dict(
    source=str(source.relative_to(ROOT)), source_page=args.page,
    source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    derived_path=str(target.relative_to(ROOT)), dpi=144,
    reason="Controlled image-only stress case, not a naturally scanned paper",
    original_text_layer_removed=True),indent=2)+"\n")
print(target)
