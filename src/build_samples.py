"""Turn extraction into inspectable evidence and conservative extractive QA.

No LLM is used to fabricate answers. These are template-generated pipeline
samples, with table coordinates and exact source strings. They are not a
validated SFT release or a reasoning-model evaluation.
"""
import html
import json
import re
from pathlib import Path
from lxml import etree

from extract_native import dump, normalize

ROOT = Path(__file__).resolve().parents[1]


def html_grid(markup):
    """Expand merged cells while retaining cell origin and header information."""
    table = etree.fromstring(markup.encode(), etree.XMLParser(resolve_entities=False, no_network=True))
    rows = table.xpath(".//tr")
    grid = {}
    header_rows = 0
    for ri, row in enumerate(rows):
        if row.getparent().tag == "thead":
            header_rows = ri + 1
        ci = 0
        for cell in row:
            if cell.tag not in ["td", "th"]:
                continue
            while (ri, ci) in grid:
                ci += 1
            rowspan = int(cell.get("rowspan", "1"))
            colspan = int(cell.get("colspan", "1"))
            cell_text = normalize("".join(cell.itertext()))
            entry = dict(text=cell_text, origin_row=ri, origin_column=ci,
                         rowspan=rowspan, colspan=colspan, header=cell.tag == "th")
            for dy in range(rowspan):
                for dx in range(colspan):
                    grid[(ri+dy,ci+dx)] = entry
            ci += colspan
    ncols = max((col for row,col in grid), default=-1) + 1
    nrows = max((row for row,col in grid), default=-1) + 1
    matrix = [[grid.get((ri,ci),dict(text="",header=False)) for ci in range(ncols)] for ri in range(nrows)]
    # Some Docling HTML uses th without a thead container.
    if not header_rows:
        for row in matrix:
            if row and all(c["header"] for c in row):
                header_rows += 1
            else:
                break
    headers = []
    for col in range(ncols):
        pieces = []
        for row in matrix[:header_rows]:
            text = row[col]["text"]
            if text and text not in pieces:
                pieces.append(text)
        headers.append(" / ".join(pieces))
    return dict(headers=headers, header_rows=header_rows, rows=matrix,
                nrows=nrows, ncols=ncols, merged_cells=sum(c.get("rowspan",1)>1 or c.get("colspan",1)>1
                    for c in {id(c):c for c in grid.values()}.values()))


def load_bundles():
    bundles = []
    for path in sorted((ROOT / "outputs/jats").glob("*/document.json")):
        document = json.loads(path.read_text())
        for bundle in document["bundles"]:
            bundle["document_title"] = document["metadata"]["title"]
            bundle["source_path"] = document["source_path"]
            bundle["source_sha256"] = document["sha256"]
            bundle["quality_flags"] = []
            if not bundle.get("image_path") and bundle["kind"] == "figure":
                bundle["quality_flags"].append("figure_pixels_not_downloaded")
            bundles.append(bundle)
    for path in sorted((ROOT / "outputs/docling").glob("*/evidence.json")):
        document = json.loads(path.read_text())
        for bundle in document["bundles"]:
            bundle["source_path"] = document["source_path"]
            bundle["source_sha256"] = document["source_sha256"]
            bundles.append(bundle)
    for bundle in bundles:
        if bundle.get("table_html"):
            try:
                bundle["table_grid"] = html_grid(bundle["table_html"])
            except etree.XMLSyntaxError as exc:
                bundle["quality_flags"].append("malformed_table_html:" + str(exc))
    return bundles


def qa_samples(bundles):
    examples = []
    # Native XML gives exact symbolic units, uncertainty notation, and spans.
    for bundle in bundles:
        if bundle.get("binding_method") != "explicit_JATS_xref" or bundle["kind"] != "table":
            continue
        grid = bundle["table_grid"]
        body = list(enumerate(grid["rows"]))[grid["header_rows"]:]
        for ri, row in body[:2]:
            if len(row) < 2 or not row[0]["text"]:
                continue
            for ci in range(1, min(3,len(row))):
                if not row[ci]["text"]:
                    continue
                question = f"In {bundle['label']}, what value is reported for {grid['headers'][ci]} for {row[0]['text']}?"
                examples.append(dict(id=f"qa:{len(examples):03d}", document_id=bundle["document_id"],
                    question=question, answer=row[ci]["text"], evidence_ids=[bundle["id"]],
                    answer_location=dict(row=ri, column=ci, header=grid["headers"][ci],
                                         row_label=row[0]["text"]),
                    generation_method="deterministic_table_lookup", verification="exact_cell_replay",
                    task="reported_table_value", training_status="pipeline_sample_only"))
    for bundle in bundles:
        if bundle["kind"] == "figure" and bundle.get("caption") and bundle.get("referring_paragraphs"):
            # Short answers drawn directly from captions; do not pretend to interpret the image.
            answer = re.split(r"(?<=[.!?])\s+", bundle["caption"])[0]
            if len(answer.split()) > 45:
                continue
            examples.append(dict(id=f"qa:{len(examples):03d}",document_id=bundle["document_id"],
                question=f"According to the caption, what does {bundle['label'] or 'this figure'} show?",
                answer=answer,evidence_ids=[bundle["id"]],answer_location=dict(field="caption"),
                generation_method="extractive_caption_lookup", verification="exact_caption_substring",
                task="caption_report",training_status="pipeline_sample_only"))
            if sum(e["task"] == "caption_report" for e in examples) == 4:
                break
    return examples


def binding_measurements(bundles):
    """Small structured-fact experiment for explicit nM binding tables only.

    No threshold-based binder/nonbinder labels are inferred. The original
    text and table footnotes remain attached to every parsed numeric value.
    """
    records = []
    for b in bundles:
        if b.get("binding_method") != "explicit_JATS_xref" or b.get("label") not in ["Table 2","Table 4"]:
            continue
        grid = b["table_grid"]
        for ri,row in list(enumerate(grid["rows"]))[grid["header_rows"]:]:
            for ci,cell in list(enumerate(row))[1:]:
                header = grid["headers"][ci]
                unit = re.search(r"\(([^)]+)\)",header)
                reported = cell["text"]
                number = re.fullmatch(r"([\d.]+)\s*±\s*([\d.]+)(?:\s+([a-z]))?",reported)
                is_nd = bool(re.match(r"^(N\.?\s*D\.?)(?:\s+[a-z])?$",reported,re.I))
                records.append(dict(document_id=b["document_id"],construct=row[0]["text"],
                    target=header.split("(")[0].strip(),header=header,reported_value=reported,
                    unit=unit.group(1) if unit else None,
                    value=float(number.group(1)) if number else None,
                    uncertainty=float(number.group(2)) if number else None,
                    missing_reason="not_determined" if is_nd else (None if number else "unparsed_value"),
                    source_table=b["label"],evidence_id=b["id"],row=ri,column=ci,
                    table_notes=b.get("table_notes",""),
                    label_inferred=False,validation_status="parsed_source_value; scientific_review_pending"))
    return records


def make_viewer(bundles, samples):
    cards = []
    for bundle in bundles:
        label = bundle.get("label") or "Unlabelled " + bundle["kind"]
        flags = ", ".join(bundle.get("quality_flags",[])) or "No structural flags; scientific review pending"
        context = "".join("<p>"+html.escape(p.get("text", ""))+"</p>" for p in bundle.get("referring_paragraphs",[]))
        image_path = bundle.get("image_path")
        image_description = 'Full source page' if bundle.get('image_scope')=='full_source_page' else 'Source region crop'
        graphic = f'<figure><img loading="lazy" src="../{html.escape(image_path)}" alt="{image_description}"><figcaption>{image_description}</figcaption></figure>' if image_path else ''
        # Table HTML came from fetched sources: show a text-only reconstruction,
        # not raw remote markup or any potentially embedded links/scripts.
        grid = bundle.get("table_grid")
        markup = ""
        if grid:
            markup = "<div class=scroll><table>" + "".join("<tr>"+"".join(
                "<td>"+html.escape(c["text"])+"</td>" for c in row)+"</tr>" for row in grid["rows"]) + "</table></div>"
        related_qa = "".join('<li>'+html.escape(q["question"])+"<br><strong>"+html.escape(q["answer"])+"</strong></li>"
                             for q in samples if bundle["id"] in q["evidence_ids"])
        cards.append(f'<article data-doc="{html.escape(bundle["document_id"])}"><h2>{html.escape(bundle["document_id"])} · {html.escape(label)}</h2>'
                     f'<p class=flag>{html.escape(flags)}</p>{graphic}<p>{html.escape(bundle.get("caption", ""))}</p>{markup}'
                     f'<details><summary>Referring text ({len(bundle.get("referring_paragraphs",[]))})</summary>{context}</details>'
                     f'<details><summary>Provenance</summary><pre>{html.escape(json.dumps({k:bundle.get(k) for k in ["id","source_path","source_sha256","source_provenance","source_xpath","image_scope","image_provenance","binding_method"]}, indent=2))}</pre></details>'
                     f'<details><summary>QA samples</summary><ul>{related_qa}</ul></details></article>')
    page = '<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Paper extraction samples</title>'
    page += '<style>body{font:16px/1.6 system-ui;max-width:1100px;margin:40px auto;padding:0 24px;background:#f7f8fa;color:#17212d}article{background:white;padding:24px;margin:20px 0;border:1px solid #dbe2e8;border-radius:8px}h1,h2{line-height:1.2}h2{font-size:21px}.flag{color:#725513;font-size:13px}img{max-width:100%;max-height:620px;object-fit:contain}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}.scroll{overflow:auto}td{border:1px solid #ccc;padding:6px 10px}table{border-collapse:collapse;font-size:14px}summary{cursor:pointer;margin-top:16px;font-weight:600}select{font:inherit;padding:8px}</style>'
    page += '<h1>Paper extraction samples</h1><p>Source visuals, table cells, captions, referring text and QA examples. Extraction and lookup checks do not validate scientific conclusions or image interpretation.</p>'
    page += '<label>Paper <select id=filter><option value=all>All samples</option>'+''.join(f'<option>{html.escape(doc)}</option>' for doc in sorted(set(b['document_id'] for b in bundles)))+'</select></label>'
    page += ''.join(cards) + '<script>document.getElementById("filter").onchange=function(){for(const a of document.querySelectorAll("article"))a.hidden=this.value!=="all"&&a.dataset.doc!==this.value;};</script></html>'
    (ROOT / "reports/sample_viewer.html").write_text(page)


def main():
    bundles = load_bundles()
    samples = qa_samples(bundles)
    dump(ROOT / "outputs/evidence_bundles.json", bundles)
    for filename, records in [("evidence_bundles.jsonl",bundles),("qa_samples.jsonl",samples)]:
        (ROOT / "outputs" / filename).write_text(''.join(json.dumps(x,ensure_ascii=False)+"\n" for x in records))
    measurements = binding_measurements(bundles)
    (ROOT / "outputs/binding_measurements.jsonl").write_text(''.join(json.dumps(x,ensure_ascii=False)+"\n" for x in measurements))
    # A second output explicitly shows the caption-only/context-enriched ablation.
    ablation = [dict(id=b["id"], document_id=b["document_id"], caption=b.get("caption",""),
                    caption_only_words=len(b.get("caption","").split()),
                    referring_paragraph_count=len(b.get("referring_paragraphs",[])),
                    enriched_words=len(b.get("caption","").split())+sum(len(p.get("text","").split()) for p in b.get("referring_paragraphs",[])))
                for b in bundles]
    dump(ROOT / "outputs/context_ablation.json", ablation)
    make_viewer(bundles,samples)
    print(json.dumps(dict(bundles=len(bundles),qa_samples=len(samples),binding_measurements=len(measurements),
                         bundles_with_referring_text=sum(bool(b.get("referring_paragraphs")) for b in bundles))),flush=True)


if __name__ == "__main__":
    main()
