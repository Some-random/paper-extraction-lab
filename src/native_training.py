"""Source-preserving JATS production parsing and small training-data previews.

This is a native-XML branch, separate from PDF/OCR evaluation. Quality rules
classify content and flag defects; they do not certify scientific correctness.
"""
from __future__ import annotations

import copy
import hashlib
import re
from collections import Counter
from pathlib import Path

from lxml import etree

XLINK = "{http://www.w3.org/1999/xlink}href"
ADMIN = re.compile(
    r"^(?:acknowledg\w*|author contributions?|competing interests?|funding|"
    r"peer review|online content|supplementary (?:information|materials?)|"
    r"source data|data availability|code availability|references|"
    r"additional information|publisher.s note)$", re.I
)


def tag(node):
    return etree.QName(node).localname if isinstance(node.tag, str) else ""


def clean(value):
    # Keep source characters, minus signs, sequences and decimal separators.
    return re.sub(r"[ \t\r\n]+", " ", value).strip()


def scientific_text(node, *, drop_citations=False):
    """Select one math representation and preserve block/sup/sub boundaries."""
    if node is None:
        return ""
    name = tag(node)
    if name == "xref" and drop_citations and node.get("ref-type") == "bibr":
        return ""
    if name == "alternatives":
        tex = next((c for c in node if tag(c) == "tex-math"), None)
        chosen = tex if tex is not None else next(iter(node), None)
        return scientific_text(chosen, drop_citations=drop_citations)
    if name == "tex-math":
        return "$" + clean("".join(node.itertext())) + "$"
    if name in {"break", "br"}:
        return "\n"
    if name in {"inline-graphic", "graphic"}:
        return "[source graphic: " + (node.get(XLINK) or node.get("href") or "unresolved") + "]"
    if name in {"math", "mfrac", "msup", "msub", "msubsup"}:
        children = [scientific_text(c, drop_citations=drop_citations) for c in node]
        if name == "mfrac" and len(children) == 2:
            return "(" + children[0] + ")/(" + children[1] + ")"
        if name in {"msup", "msub"} and len(children) == 2:
            return children[0] + ("^(" if name == "msup" else "_(") + children[1] + ")"
        if name == "msubsup" and len(children) == 3:
            return children[0] + "_(" + children[1] + ")^(" + children[2] + ")"
    pieces = [node.text or ""]
    for child in node:
        content = scientific_text(child, drop_citations=drop_citations)
        ct = tag(child)
        if ct == "sup":
            content = "^(" + content.strip() + ")" if content.strip() else ""
        elif ct == "sub":
            content = "_(" + content.strip() + ")" if content.strip() else ""
        elif ct in {"p", "list-item", "disp-formula", "title"}:
            content = "\n" + content + "\n"
        pieces.extend([content, child.tail or ""])
    return "".join(pieces)


def text(node, *, drop_citations=False):
    return clean(scientific_text(node, drop_citations=drop_citations))


def prose_only(node):
    """Remove floating objects nested in p without losing their following text."""
    result = copy.deepcopy(node)
    for floating in list(result.xpath('.//*[local-name()="fig" or local-name()="table-wrap"]')):
        parent = floating.getparent()
        if parent is None:
            continue
        tail = floating.tail or ''
        previous = floating.getprevious()
        if previous is None:
            parent.text = (parent.text or '') + tail
        else:
            previous.tail = (previous.tail or '') + tail
        parent.remove(floating)
    return result


def inline_html(node):
    """Readable source markup with a tiny allowlist, never executable XML."""
    import html
    if node is None:
        return ""
    name = tag(node)
    if name == "alternatives":
        chosen = next((c for c in node if tag(c) == "tex-math"), None)
        if chosen is None:
            chosen = next(iter(node), None)
        return inline_html(chosen)
    if name in {"tex-math", "math"}:
        return '<code class="math">' + html.escape(text(node)) + '</code>'
    if name in {"break", "br"}:
        return "<br>"
    names = {"italic": "i", "bold": "b", "sup": "sup", "sub": "sub",
             "p": "p", "title": "strong", "list": "ul", "list-item": "li",
             "table": "table", "thead": "thead", "tbody": "tbody", "tfoot": "tfoot",
             "tr": "tr", "td": "td", "th": "th", "monospace": "code"}
    opening = closing = ""
    if name in names:
        safe = names[name]
        attrs = ""
        if name in {"td", "th"}:
            for a in ["rowspan", "colspan"]:
                value = node.get(a, "1")
                if value.isdigit() and 1 <= int(value) <= 150:
                    attrs += ' ' + a + '="' + value + '"'
        opening, closing = '<' + safe + attrs + '>', '</' + safe + '>'
    elif name == "xref":
        opening, closing = '<span class="source-ref">', '</span>'
    return opening + html.escape(node.text or "") + "".join(
        inline_html(c) + html.escape(c.tail or "") for c in node
    ) + closing


def table_grid(table, tree, paths=None):
    """Physical cells and span-expanded occupancy; no inferred cell values."""
    occupied = {}
    cells = []
    rows = table.xpath('.//*[local-name()="tr"]')
    if len(rows) > 150:
        raise ValueError("Preview limit: more than 150 source table rows")
    for ri, row in enumerate(rows):
        ci = 0
        for cell in row:
            if tag(cell) not in {"th", "td"}:
                continue
            while (ri, ci) in occupied:
                ci += 1
            rs, cs = int(cell.get("rowspan", "1")), int(cell.get("colspan", "1"))
            if not (1 <= rs <= 150 and 1 <= cs <= 50 and ci + cs <= 50):
                raise ValueError("Invalid or oversized source cell span")
            item = dict(id=f"r{ri}c{ci}", row=ri, column=ci, rowspan=rs, colspan=cs,
                        text=text(cell), html=inline_html(cell), source_xpath=paths[cell] if paths else tree.getpath(cell),
                        raw_xml=etree.tostring(cell, encoding="unicode"),
                        tag=tag(cell), scope=cell.get("scope"),
                        is_column_header=any(tag(a) == "thead" for a in cell.iterancestors()))
            for dr in range(rs):
                for dc in range(cs):
                    key = (ri + dr, ci + dc)
                    if key in occupied:
                        raise ValueError("Overlapping table cell spans")
                    occupied[key] = item
            cells.append(item)
            ci += cs
    nr = max((r for r, _ in occupied), default=-1) + 1
    nc = max((c for _, c in occupied), default=-1) + 1
    header_paths = []
    for ci in range(nc):
        header_paths.append(list(dict.fromkeys(
            occupied[(r, ci)]["text"] for r in range(nr)
            if (r, ci) in occupied and occupied[(r, ci)]["is_column_header"]
        )))
    for cell in cells:
        cell["column_header_path"] = header_paths[cell["column"]]
    matrix = [[occupied[(r, c)]["id"] if (r, c) in occupied else None
               for c in range(nc)] for r in range(nr)]
    # Never repeat a group total as if it were a value for each physical row.
    # Covered slots explicitly point to the source cell; HTML retains spans.
    def tsv_slot(r, c):
        cell = occupied.get((r, c))
        if cell is None:
            return ''
        if (cell['row'], cell['column']) != (r, c):
            return '[merged from ' + cell['id'] + ']'
        suffix = ''
        if cell['rowspan'] > 1 or cell['colspan'] > 1:
            suffix = f" [rowspan={cell['rowspan']}, colspan={cell['colspan']}]"
        return cell['text'] + suffix
    tsv = "\n".join("\t".join(tsv_slot(r, c) for c in range(nc)) for r in range(nr))
    return dict(cells=cells, occupancy=matrix, nrows=nr, ncols=nc,
                header_paths=header_paths, source_cell_count=len(cells), text_tsv=tsv)


def parse_jats(source: Path, pmcid: str, tokenizer):
    tree = etree.parse(str(source), etree.XMLParser(resolve_entities=False, no_network=True))
    # Strip names only in the working copy; retain unmodified source XPaths.
    paths = {n: tree.getpath(n) for n in tree.iter() if isinstance(n.tag, str)}
    for n in tree.iter():
        if isinstance(n.tag, str):
            n.tag = tag(n)
    meta = tree.find('front/article-meta')
    if meta is None or tree.find('body') is None:
        raise ValueError("JATS metadata or body missing")
    blocks, excluded = [], []
    title = text(meta.find('title-group/article-title'))
    visuals = []
    for index, v in enumerate(tree.xpath('//fig | //table-wrap')):
        vid = v.get('id') or f"unidentified-{index}"
        table = v.find('.//table')
        grid = table_grid(table, tree, paths) if table is not None else None
        visuals.append(dict(id=pmcid + ':' + vid, xml_id=vid,
            kind='figure' if v.tag == 'fig' else 'table', label=text(v.find('label')),
            caption=text(v.find('caption')), caption_html=inline_html(v.find('caption')),
            caption_training_text=text(v.find('caption')),
            notes=text(v.find('table-wrap-foot')), table=grid,
            table_html=inline_html(table) if table is not None else None,
            source_xpath=paths[v], graphics=[g.get(XLINK) or g.get('href') for g in v.findall('.//graphic')],
            source_xml_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            validation_status='native_source_structure; figure_semantics_not_adjudicated'))
    by_xml_id = {v['xml_id']: v for v in visuals}

    def emit(node, section, region, kind='paragraph', reason=None, content=None):
        view = prose_only(node) if kind in {'paragraph', 'abstract'} else node
        reader_text = text(view) if content is None else content
        # Keep source citation markers rather than heuristically deleting ranges
        # and risking malformed scientific notation. Bibliographies are routed
        # outside this preview's CPT stream; reference metadata stays in XML.
        training_text = text(view) if content is None else content
        if not reader_text:
            return
        refs = [dict(ref_type=x.get('ref-type'), rid=rid, source_xpath=paths[x], label=text(x))
                for x in node.findall('.//xref') for rid in (x.get('rid') or '').split()
                if x.get('ref-type') in {'fig', 'table'}
                and not any(tag(a) in {'fig', 'table-wrap'} for a in x.iterancestors() if a is not node)]
        flags = []
        n_tokens = len(tokenizer.encode(training_text, add_special_tokens=False).ids)
        if n_tokens < 32:
            flags.append('short_source_block_retained')
        if '\ufffd' in training_text:
            flags.append('unicode_replacement_character')
        if re.search(r'(\b\w+\b)(?:\s+\1){5,}', training_text, re.I):
            flags.append('possible_repetition_review')
        if '[source graphic:' in training_text:
            flags.append('inline_graphic_requires_review')
        item = dict(id=f'{pmcid}:block{len(blocks) + len(excluded):04d}',
            kind=kind, region=region, section_path=section, text=reader_text,
            training_text=training_text, html=inline_html(view) if content is None else None,
            source_xpath=paths[node], raw_xml=etree.tostring(node, encoding='unicode'),
            references=refs, token_count=n_tokens, quality_flags=flags,
            training_eligible=not reason, exclusion_reason=reason,
            quality_method='transparent structural/heuristic rules; no learned educational scoring')
        (excluded if reason else blocks).append(item)

    def walk(node, section, region, reason=None):
        name = tag(node)
        if name in {'sec', 'app', 'ack', 'notes'}:
            heading = text(node.find('title'))
            sec = section + ([heading] if heading else [])
            exclusion = reason or ('administrative_section' if heading and ADMIN.fullmatch(heading) else None)
            if name in {'ack', 'notes'}:
                exclusion = exclusion or 'back_matter_administrative'
            for child in node:
                if child.tag not in {'title', 'label'}:
                    walk(child, sec, region, exclusion)
        elif name == 'ref-list':
            for ref in node.findall('ref'):
                emit(ref, section + ['References'], region, 'reference', 'bibliography')
        elif name in {'fig', 'table-wrap'}:
            # All visual objects remain in their own evidence stream. Only their
            # source captions/TSV, never fabricated interpretations, enter text.
            obj = by_xml_id.get(node.get('id'))
            if obj and obj['caption']:
                cap = node.find('caption')
                emit(cap, section, region, 'caption', reason)
                blocks_or_excluded = excluded if reason else blocks
                blocks_or_excluded[-1]['visual_id'] = obj['id']
                if obj['table']:
                    emit(node, section, region, 'table', reason,
                         obj['label'] + '\n' + obj['table']['text_tsv'] + '\n' + obj['notes'])
                    blocks_or_excluded[-1]['visual_id'] = obj['id']
        elif name == 'p':
            emit(node, section, region, 'paragraph', reason)
            # Floating Nature objects can live inside a paragraph. Emit their
            # own captions/grids once, outside the paragraph's prose stream.
            for floating in node.xpath('.//fig[not(ancestor::fig) and not(ancestor::table-wrap)] | .//table-wrap[not(ancestor::fig) and not(ancestor::table-wrap)]'):
                walk(floating, section, region, reason)
        elif name in {'disp-formula', 'statement', 'verse-group'}:
            emit(node, section, region, name, reason)
        elif name in {'fn-group', 'supplementary-material'}:
            emit(node, section, region, name, reason or 'administrative_or_external_material')
        else:
            for child in node:
                walk(child, section, region, reason)

    for abstract in meta.findall('abstract'):
        abstract_type = abstract.get('abstract-type')
        if abstract_type and abstract_type not in {'abstract', 'structured'}:
            emit(abstract, ['Abstract'], 'front', 'abstract', 'non_primary_abstract_' + abstract_type)
        else:
            emit(abstract, ['Abstract'], 'front', 'abstract')
    walk(tree.find('body'), [], 'body')
    if tree.find('back') is not None:
        walk(tree.find('back'), [], 'back')
    for v in tree.xpath('//fig[not(ancestor::body) and not(ancestor::back)] | //table-wrap[not(ancestor::body) and not(ancestor::back)]'):
        walk(v, ['Floating source evidence'], 'floats')
    paragraphs = [b for b in blocks if b['kind'] in {'paragraph', 'abstract'}]
    for i, b in enumerate(paragraphs):
        b['paragraph_index'] = i
    for visual in visuals:
        typ = 'fig' if visual['kind'] == 'figure' else 'table'
        visual['referring_paragraphs'] = [b['id'] for b in paragraphs
            if any(r['rid'] == visual['xml_id'] and r['ref_type'] == typ for r in b['references'])]
        visual['unresolved_media'] = visual['kind'] == 'figure'
    id_counts = Counter(v['xml_id'] for v in visuals)
    unresolved = [dict(block_id=b['id'], **r) for b in paragraphs for r in b['references']
                  if r['rid'] not in by_xml_id]
    digests = Counter(hashlib.sha256(b['training_text'].encode()).hexdigest() for b in paragraphs)
    for b in paragraphs:
        if digests[hashlib.sha256(b['training_text'].encode()).hexdigest()] > 1:
            b['quality_flags'].append('exact_repeated_paragraph_review; retained_with_provenance')
    return dict(pmcid=pmcid, title=title, blocks=blocks, excluded_blocks=excluded,
        visuals=visuals, unresolved_references=unresolved,
        duplicate_visual_ids=[k for k, n in id_counts.items() if n > 1],
        identifiers={n.get('pub-id-type'): text(n) for n in meta.findall('article-id')},
        source_xml_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        license_statements=[text(n) for n in meta.findall('permissions/license')],
        authors=[text(n.find('given-names')) + ' ' + text(n.find('surname'))
                 for n in meta.findall('contrib-group/contrib/name')])


def interleaved_records(document):
    """Only consecutive source paragraphs, with exact many-to-many xrefs."""
    visuals = {v['xml_id']: v for v in document['visuals']}
    paragraphs = [b for b in document['blocks'] if b['kind'] in {'paragraph', 'abstract'}]
    groups = []
    for b in paragraphs:
        refs = {r['rid'] for r in b['references'] if r['rid'] in visuals
                and r['ref_type'] == ('fig' if visuals[r['rid']]['kind'] == 'figure' else 'table')}
        if not refs:
            continue
        if groups and groups[-1][-1]['paragraph_index'] + 1 == b['paragraph_index'] and groups[-1][-1]['section_path'] == b['section_path']:
            groups[-1].append(b)
        else:
            groups.append([b])
    output = []
    for i, group in enumerate(groups):
        refs = list(dict.fromkeys(r['rid'] for b in group for r in b['references'] if r['rid'] in visuals))
        edges = [dict(block_id=b['id'], visual_id=visuals[r['rid']]['id'],
                      xref_xpath=r['source_xpath'], ref_type=r['ref_type'])
                 for b in group for r in b['references'] if r['rid'] in refs]
        output.append(dict(id=f"{document['pmcid']}:interleaved{i:03d}",
            context_block_ids=[b['id'] for b in group], visual_ids=[visuals[r]['id'] for r in refs],
            context_text='\n\n'.join(b['training_text'] for b in group), edges=edges,
            context_policy='consecutive_source_paragraphs_in_same_section; explicit_xref_only',
            captions=[dict(visual_id=visuals[r]['id'], text=visuals[r]['caption_training_text']) for r in refs],
            source_xml_sha256=document['source_xml_sha256'],
            status='source_linked_candidate; not a validated image interpretation or generated reasoning trace'))
        segments, emitted = [], set()
        for b in group:
            segments.append(dict(type='text', role='article_context', block_id=b['id'],
                                 text=b['training_text'], source_xpath=b['source_xpath']))
            for r in b['references']:
                rid = r['rid']
                if rid not in refs or rid in emitted:
                    continue
                emitted.add(rid)
                visual = visuals[rid]
                if visual['kind'] == 'figure':
                    segments.append(dict(type='image', visual_id=visual['id'],
                        assets=visual.get('assets', []), availability='available' if visual.get('assets') else 'missing_media'))
                else:
                    segments.append(dict(type='table', visual_id=visual['id'],
                        text_tsv=visual['table']['text_tsv'] if visual['table'] else None,
                        source_xpath=visual['source_xpath']))
                segments.append(dict(type='text', role='source_caption', visual_id=visual['id'],
                                     text=visual['caption_training_text'], source_xpath=visual['source_xpath']))
        output[-1]['segments'] = segments
    return output


def pack_text(document, tokenizer, maximum=2048):
    """Pack full blocks; split oversized blocks at whitespace, never characters."""
    units = []
    for block in document['blocks']:
        value = block['training_text']
        cursor = 0
        while cursor < len(value):
            rest = value[cursor:]
            enc = tokenizer.encode(rest, add_special_tokens=False)
            if len(enc.ids) <= maximum:
                end = len(value)
            else:
                proposed = enc.offsets[maximum - 8][0]
                boundaries = list(re.finditer(r'\s+', rest[:proposed]))
                if not boundaries:
                    raise ValueError('Oversized uninterrupted scientific string: preserve outside packed stream')
                end = cursor + boundaries[-1].end()
                while len(tokenizer.encode(value[cursor:end], add_special_tokens=False).ids) > maximum:
                    end = cursor + max(m.start() for m in boundaries if cursor + m.start() < end)
            units.append(dict(block_id=block['id'], char_start=cursor, char_end=end,
                              text=value[cursor:end], source_xpath=block['source_xpath'],
                              section_path=block['section_path']))
            cursor = end
    chunks = []
    for unit in units:
        candidate = (chunks[-1]['text'] + '\n\n' if chunks else '') + unit['text']
        if not chunks or len(tokenizer.encode(candidate, add_special_tokens=False).ids) > maximum:
            chunks.append(dict(id=f"{document['pmcid']}:text{len(chunks):03d}", text=unit['text'], fragments=[unit]))
        else:
            chunks[-1]['text'] = candidate
            chunks[-1]['fragments'].append(unit)
    for chunk in chunks:
        chunk['token_count'] = len(tokenizer.encode(chunk['text'], add_special_tokens=False).ids)
        chunk['source_xml_sha256'] = document['source_xml_sha256']
        chunk['article_title'] = document['title']
        chunk['stream'] = 'native_text_cpt_preview; not trained'
        if chunk['token_count'] > maximum:
            raise AssertionError('Token budget exceeded')
    return chunks
