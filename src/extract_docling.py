"""Sequential Docling extraction, source crops, and evidence binding.

One document is submitted at a time. The pilot disables pipeline prefetching
and uses two CPU threads; no GPU or remote inference is required.
"""
import argparse
import hashlib
import json
import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("HF_HOME", str(ROOT / "cache/huggingface"))
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "0")
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")

# A single experiment should not spawn concurrent model-file download tasks.
import huggingface_hub
_snapshot_download = huggingface_hub.snapshot_download
def sequential_snapshot(*args, **kwargs):
    kwargs["max_workers"] = 1
    return _snapshot_download(*args, **kwargs)
huggingface_hub.snapshot_download = sequential_snapshot

import torch
torch.set_num_threads(2)
torch.set_num_interop_threads(1)

from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import PictureItem, TableItem

from extract_native import dump, normalize, references


def make_converter(ocr):
    options = PdfPipelineOptions()
    options.accelerator_options = AcceleratorOptions(num_threads=2, device=AcceleratorDevice.CPU)
    options.do_ocr = ocr
    if ocr:
        options.ocr_options = RapidOcrOptions(force_full_page_ocr=True, lang=["en"],
            rapidocr_params={"EngineConfig.onnxruntime.intra_op_num_threads": 2,
                             "EngineConfig.onnxruntime.inter_op_num_threads": 1,
                             "Global.model_root_dir": str(ROOT / "cache/rapidocr")})
    options.do_table_structure = True
    options.generate_page_images = True
    options.generate_picture_images = True
    options.images_scale = 1.5
    # New threaded pipelines can otherwise prefetch many pages inside one document.
    for name, value in [("layout_batch_size", 1), ("ocr_batch_size", 1),
                        ("table_batch_size", 1), ("queue_max_size", 1)]:
        if hasattr(options, name):
            setattr(options, name, value)
    return DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options)})


def provenance(item):
    if not item.prov:
        return None
    p = item.prov[0]
    return dict(page=p.page_no, bbox=p.bbox.model_dump(mode="json"), charspan=list(p.charspan))


def convert(converter, doc_id, source, output, page_range=None, ocr=False):
    start = time.monotonic()
    kwargs = dict(page_range=page_range) if page_range else {}
    result = converter.convert(source, **kwargs)
    doc = result.document
    output.mkdir(parents=True, exist_ok=True)
    # This JSON retains table spans and precise provenance; Markdown alone is lossy.
    doc.save_as_json(output / "docling.json")
    (output / "document.md").write_text(doc.export_to_markdown())
    elements, visuals = [], []
    for index, (item, _level) in enumerate(doc.iterate_items()):
        identity = f"{doc_id}:docling:{item.self_ref}"
        if isinstance(item, (PictureItem, TableItem)):
            kind = "table" if isinstance(item, TableItem) else "figure"
            caption = item.caption_text(doc)
            label_matches = references(caption)
            img_name = f"{kind}_{index:03d}.png"
            img = item.get_image(doc)
            if img is not None:
                img.save(output / img_name)
            entry = dict(id=identity, document_id=doc_id, kind=kind,
                         source_provenance=provenance(item), caption=caption,
                         label=label_matches[0] if len(label_matches) == 1 else None,
                         label_candidates=label_matches,
                         image_path=str((output/img_name).relative_to(ROOT)) if img is not None else None,
                         caption_ref_ids=[r.cref for r in item.captions],
                         source_ref=item.self_ref, structure_method="Docling")
            if isinstance(item, TableItem):
                entry["table_html"] = item.export_to_html(doc=doc)
                entry["table_cells"] = [cell.model_dump(mode="json") for cell in item.data.table_cells]
                entry["row_count"] = item.data.num_rows
                entry["column_count"] = item.data.num_cols
                (output/f"table_{index:03d}.html").write_text(entry["table_html"])
            visuals.append(entry)
        elif hasattr(item, "text"):
            label = str(item.label.value) if hasattr(item.label, "value") else str(item.label)
            elements.append(dict(id=identity, kind=label, text=item.text,
                                 source_provenance=provenance(item),
                                 references=references(item.text), source_ref=item.self_ref))
    caption_ref_ids = {ref for v in visuals for ref in v["caption_ref_ids"]}
    for visual in visuals:
        matched = [e for e in elements if visual["label"] and visual["label"] in e["references"]
                   and e["kind"] not in ["caption", "page_header", "page_footer"]
                   and e["source_ref"] not in caption_ref_ids]
        visual["referring_paragraph_ids"] = [e["id"] for e in matched]
        visual["referring_paragraphs"] = matched
        visual["binding_method"] = "Docling_caption_attachment+explicit_label_mentions"
        flags = []
        if not visual["caption"]:
            flags.append("missing_caption")
        if visual["label"] is None:
            flags.append("ambiguous_or_missing_label")
        if not visual["image_path"]:
            flags.append("missing_visual_crop")
        if not matched:
            flags.append("no_explicit_referring_text_found")
        if visual["caption"] and "Lorem ipsum" in visual["caption"]:
            flags.append("placeholder_text_in_caption")
        visual["quality_flags"] = flags
        visual["status"] = "source_extracted; semantic_and_visual_review_pending"
    summary = dict(document_id=doc_id, status=str(result.status.value),
                   pages=len(doc.pages), text_elements=len(elements),
                   figures=sum(v["kind"] == "figure" for v in visuals),
                   tables=sum(v["kind"] == "table" for v in visuals),
                   with_caption=sum(bool(v["caption"]) for v in visuals),
                   with_referring_text=sum(bool(v["referring_paragraphs"]) for v in visuals),
                   seconds=round(time.monotonic()-start,3), do_ocr=ocr)
    dump(output / "evidence.json", dict(document_id=doc_id, source_path=str(source.relative_to(ROOT)),
         source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), method="Docling_standard",
         summary=summary, elements=elements, bundles=visuals))
    print(json.dumps(summary), flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", action="append")
    parser.add_argument("--page-start", type=int)
    parser.add_argument("--page-end", type=int)
    parser.add_argument("--ocr", action="store_true")
    args = parser.parse_args()
    converter = make_converter(args.ocr)
    summaries = []
    docs = args.doc or ["ryze", "llava_med"]
    for doc_id in docs:
        source = ROOT / "inputs" / f"{doc_id}.pdf"
        page_range = (args.page_start, args.page_end) if args.page_start and args.page_end else None
        output = ROOT / "outputs/docling" / doc_id
        summaries.append(convert(converter, doc_id, source, output, page_range, args.ocr))
    dump(ROOT / "outputs/docling_last_run.json", dict(workers=1, cpu_threads=2, gpu_count=0, documents=summaries))


if __name__ == "__main__":
    main()
