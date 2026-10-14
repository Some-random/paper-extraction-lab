"""Fast PDF and JATS extraction with immutable evidence/provenance records."""
import argparse
import hashlib
import json
import re
import time
from pathlib import Path

import pymupdf as fitz
import pdfplumber
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
XLINK = "{http://www.w3.org/1999/xlink}href"
CAPTION = re.compile(r"^(Figure|Fig\.?|Table)\s+(\d+[A-Za-z]?)\s*[:.\u2014\u2013]", re.I)


def normalize(text):
    # Keep source text beside this conservative display normalization.
    text = text.replace("\xad", "").replace("\x02", "")
    text = re.sub(r"(?<=[a-z])-\n(?=[a-z])", "", text)
    return re.sub(r"\s+", " ", text).strip()


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def text_of(node):
    return normalize("".join(node.itertext())) if node is not None else ""


def references(text):
    out = []
    for kind, number in re.findall(r"\b(Figure|Fig\.?|Table)\s+(\d+[A-Za-z]?)", text, re.I):
        kind = "table" if kind.lower() == "table" else "figure"
        out.append(f"{kind}:{number}")
    return sorted(set(out))


def pdf_records(doc_id, source, output):
    start = time.monotonic()
    elements, pages, tables = [], [], []
    with fitz.open(source) as pdf:
        for pnum, page in enumerate(pdf, 1):
            blocks = page.get_text("blocks", sort=False)
            text_blocks = [b for b in blocks if len(b) < 7 or b[6] == 0]
            pages.append(dict(page=pnum, width=page.rect.width, height=page.rect.height,
                              native_text=page.get_text(sort=False),
                              position_sorted_text=page.get_text(sort=True)))
            for index, block in enumerate(text_blocks):
                raw = block[4]
                clean = normalize(raw)
                if not clean:
                    continue
                match = CAPTION.match(clean)
                kind = "caption" if match else "text"
                label = None
                if match:
                    label = ("table" if match.group(1).lower() == "table" else "figure") + ":" + match.group(2)
                elements.append(dict(id=f"{doc_id}:p{pnum}:b{index}", kind=kind,
                                     page=pnum, bbox=[round(x, 3) for x in block[:4]],
                                     raw_text=raw, text=clean, label=label,
                                     references=references(clean),
                                     extraction_method="pymupdf_native"))
            # Every page render is source-grounded; embedded images alone omit vector plots.
            image_path = output / "pages" / f"page_{pnum:03d}.png"
            image_path.parent.mkdir(parents=True, exist_ok=True)
            page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(image_path)
    with pdfplumber.open(source) as pdf:
        for pnum, page in enumerate(pdf.pages, 1):
            # Line-based and text-based detectors have very different failure modes.
            for strategy in ["lines", "text"]:
                settings = dict(vertical_strategy=strategy, horizontal_strategy=strategy)
                for tidx, table in enumerate(page.find_tables(settings)):
                    rows = table.extract()
                    if len(rows) < 2 or max((len(r) for r in rows), default=0) < 2:
                        continue
                    tables.append(dict(id=f"{doc_id}:p{pnum}:table:{strategy}:{tidx}",
                                       page=pnum, bbox=list(table.bbox), rows=rows,
                                       strategy=strategy, status="unreviewed_candidate"))
    dump(output / "document.json", dict(document_id=doc_id,
         source_path=str(source.relative_to(ROOT)), sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
         method="pymupdf_native+pdfplumber", pages=pages, elements=elements,
         table_candidates=tables, seconds=time.monotonic() - start))
    (output / "native.txt").write_text("\n\f\n".join(x["native_text"] for x in pages))
    (output / "position_sorted.txt").write_text("\n\f\n".join(x["position_sorted_text"] for x in pages))
    return dict(document_id=doc_id, pages=len(pages), elements=len(elements),
                caption_candidates=sum(x["kind"] == "caption" for x in elements),
                table_candidates=len(tables), seconds=round(time.monotonic() - start, 3))


def jats_records(doc_id, source, output):
    start = time.monotonic()
    tree = etree.parse(str(source), parser=etree.XMLParser(resolve_entities=False, no_network=True))
    elements, bundles = [], []
    body = tree.find("body")
    if body is None:
        raise ValueError("JATS body is missing")
    for index, p in enumerate(body.xpath('.//p[not(ancestor::fig) and not(ancestor::table-wrap)]')):
        ref_ids = sorted(set(rid for x in p.findall(".//xref")
                             if x.get("ref-type") in ["fig", "table"]
                             for rid in (x.get("rid") or "").split()))
        elements.append(dict(id=f"{doc_id}:xml:p{index}", kind="text", text=text_of(p),
                             source_xpath=tree.getpath(p), xml_reference_ids=ref_ids))
    # JATS publishers may move all visuals out of body into article/floats-group.
    for visual in tree.xpath("//fig | //table-wrap"):
        vid = visual.get("id")
        caption = text_of(visual.find("caption"))
        label = text_of(visual.find("label"))
        related = [p for p in elements if vid in p["xml_reference_ids"]]
        table = visual.find(".//table")
        graphic = visual.find(".//graphic")
        bundles.append(dict(id=f"{doc_id}:xml:{vid}", document_id=doc_id,
                            kind="table" if visual.tag == "table-wrap" else "figure",
                            label=label, caption=caption, source_xpath=tree.getpath(visual),
                            xml_id=vid, image_href=graphic.get(XLINK) if graphic is not None else None,
                            table_html=etree.tostring(table, encoding="unicode") if table is not None else None,
                            table_notes=text_of(visual.find("table-wrap-foot")),
                            referring_paragraph_ids=[p["id"] for p in related],
                            referring_paragraphs=related, binding_method="explicit_JATS_xref",
                            status="source_extracted; semantic_and_visual_review_pending"))
    article_meta = tree.find("front/article-meta")
    metadata = dict(title=text_of(article_meta.find("title-group/article-title")),
                    identifiers={x.get("pub-id-type"): text_of(x) for x in article_meta.findall("article-id")},
                    license=text_of(article_meta.find("permissions/license")))
    dump(output / "document.json", dict(document_id=doc_id, method="native_JATS",
         source_path=str(source.relative_to(ROOT)), sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
         metadata=metadata, elements=elements, bundles=bundles, seconds=time.monotonic() - start))
    return dict(document_id=doc_id, paragraphs=len(elements), figures=sum(b["kind"] == "figure" for b in bundles),
                tables=sum(b["kind"] == "table" for b in bundles),
                visuals_with_explicit_referring_text=sum(bool(b["referring_paragraphs"]) for b in bundles),
                seconds=round(time.monotonic() - start, 3))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", action="append")
    args = parser.parse_args()
    summaries = []
    for source in sorted((ROOT / "inputs").glob("*.pdf")):
        if not args.doc or source.stem in args.doc:
            result = pdf_records(source.stem, source, ROOT / "outputs/native" / source.stem)
            summaries.append(result)
            print(json.dumps(result), flush=True)
    for source in sorted((ROOT / "inputs").glob("*.xml")):
        if not args.doc or source.stem in args.doc:
            result = jats_records(source.stem, source, ROOT / "outputs/jats" / source.stem)
            summaries.append(result)
            print(json.dumps(result), flush=True)
    summary_path = ROOT / "outputs/native_summary.json"
    old = json.loads(summary_path.read_text())["documents"] if summary_path.exists() else []
    merged = {(x["document_id"], "xml" if "paragraphs" in x else "pdf"): x for x in old}
    for x in summaries:
        merged[(x["document_id"], "xml" if "paragraphs" in x else "pdf")] = x
    dump(summary_path, dict(workers=1, gpu_count=0, documents=list(merged.values())))


if __name__ == "__main__":
    main()
