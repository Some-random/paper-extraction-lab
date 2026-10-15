"""Deterministic, source-linked title/author expansion of JATS citations.

No language model, external lookup, citation-policy comparison or recursive
paper download is involved. Unstructured references stay explicit when no
source-checked metadata is supplied.
"""
from __future__ import annotations

import copy
import re
from collections import Counter

from lxml import etree


def plain(node):
    return re.sub(r'\s+', ' ', ''.join(node.itertext())).strip() if node is not None else ''


def citation_payload(ref):
    alternatives = ref.find('citation-alternatives')
    parent = alternatives if alternatives is not None else ref
    for name in ('element-citation', 'mixed-citation', 'nlm-citation'):
        found = parent.find(name)
        if found is not None:
            return found
    return parent


class CitationIndex:
    def __init__(self, tree, pmcid, paths, source_sha256, overrides=None):
        self.paths = paths
        self.pmcid = pmcid
        self.bibliography = []
        self.by_xml_id = {}
        self.replacements = {}
        self.tail_replacements = {}
        self.mentions = []
        overrides = overrides or {}
        for number, ref in enumerate(tree.xpath('//ref-list/ref')):
            xml_id = ref.get('id') or f'unidentified-reference-{number}'
            payload = citation_payload(ref)
            title_node = next((payload.find('.//' + n) for n in
                               ('article-title', 'chapter-title', 'data-title')
                               if payload.find('.//' + n) is not None), None)
            title = plain(title_node)
            title_kind = etree.QName(title_node).localname if title_node is not None else None
            groups = payload.findall('.//person-group')
            author_groups = [g for g in groups if g.get('person-group-type') in (None, 'author')]
            author_nodes = [n for g in author_groups for n in g
                            if n.tag in {'name', 'string-name', 'collab'}]
            if not groups:
                author_nodes = payload.xpath('.//name | .//string-name | .//collab')
            authors = []
            for n in author_nodes:
                surname = plain(n.find('surname'))
                given = plain(n.find('given-names'))
                authors.append(dict(name=' '.join(x for x in (given, surname) if x) or plain(n),
                                    surname=surname or None, given_names=given or None,
                                    collective=n.tag == 'collab'))
            year = plain(payload.find('.//year')) or None
            raw = plain(payload)
            status = 'structured_source_metadata'
            if xml_id in overrides:
                override = overrides[xml_id]
                # Each manually segmented field must have literal source evidence.
                for literal in override['required_source_literals']:
                    if literal not in raw:
                        raise ValueError(f'Citation override lacks source evidence: {pmcid}:{xml_id}: {literal}')
                fields = [override['title']] + [a.get('surname') or a['name'] for a in override.get('authors', [])]
                if override.get('year'):
                    fields.append(override['year'])
                if any(field not in raw for field in fields):
                    raise ValueError(f'Citation override lacks source evidence for a title/author/year field: {pmcid}:{xml_id}')
                title = override['title']
                authors = override.get('authors', [])
                year = override.get('year')
                title_kind = override.get('title_kind', 'article-title')
                status = 'source_checked_segmentation_of_unstructured_reference'
            if not title and payload.get('publication-type') in {'book', 'report', 'web', 'software'}:
                title = plain(payload.find('source'))
                title_kind = 'source' if title else None
            identifiers = {}
            for item in payload.findall('.//pub-id'):
                kind = item.get('pub-id-type')
                if kind:
                    identifiers.setdefault(kind, plain(item))
            record = dict(id=f'{pmcid}:ref:{xml_id}', xml_id=xml_id,
                          label=plain(ref.find('label')), title=title or None,
                          title_kind=title_kind, authors=authors, year=year,
                          source_author_list_has_et_al=bool(payload.xpath('.//etal')) or bool(re.search(r'\bet al\.', raw)),
                          identifiers=identifiers, raw_reference_text=raw,
                          metadata_status=status if title else 'unstructured_reference_preserved',
                          source_xpath=paths[ref], source_xml_sha256=source_sha256)
            record['normalized_identifiers'] = {
                kind: re.sub(r'^https?://(?:dx\.)?doi\.org/', '', value, flags=re.I).strip().casefold()
                if kind == 'doi' else value.strip().upper() if kind == 'pmcid' else value.strip()
                for kind, value in identifiers.items()}
            self.bibliography.append(record)
            if xml_id in self.by_xml_id:
                raise ValueError(f'Duplicate bibliography ID: {pmcid}:{xml_id}')
            self.by_xml_id[xml_id] = record
        self._numeric = {}
        labels = Counter(r['label'].strip().rstrip('.') for r in self.bibliography)
        for record in self.bibliography:
            label = record['label'].strip().rstrip('.')
            if label.isdigit() and labels[label] == 1:
                self._numeric[int(label)] = record['xml_id']
        self._collect_mentions(tree, source_sha256)

    def format_reference(self, xml_id):
        record = self.by_xml_id.get(xml_id)
        if record is None:
            return f'[bib_ref]Unresolved source reference {self.pmcid}:{xml_id}[/bib_ref]'
        if not record['title']:
            return '[bib_ref]' + record['raw_reference_text'] + '[/bib_ref]'
        authors = record['authors']
        author = (authors[0].get('surname') or authors[0]['name']) if authors else 'author not supplied'
        if len(authors) > 1 or record['source_author_list_has_et_al']:
            author += ' et al.'
        return '[bib_ref]' + record['title'] + ' — ' + author + '[/bib_ref]'

    def _expand_range(self, first, last):
        left, right = self.by_xml_id.get(first), self.by_xml_id.get(last)
        if not left or not right:
            return None
        a, b = left['label'].strip().rstrip('.'), right['label'].strip().rstrip('.')
        if not a.isdigit() or not b.isdigit() or not 0 < int(b) - int(a) <= len(self.bibliography):
            return None
        values = list(range(int(a), int(b) + 1))
        if not all(i in self._numeric for i in values):
            return None
        return [self._numeric[i] for i in values]

    def _collect_mentions(self, tree, source_sha256):
        consumed = set()
        for node in tree.xpath('//xref[@ref-type="bibr"]'):
            path = self.paths[node]
            if path in consumed:
                continue
            group = [node]
            targets = (node.get('rid') or '').split()
            method = 'explicit_rid'
            following = node.getnext()
            if (len(targets) == 1 and following is not None and following.tag == 'xref'
                    and following.get('ref-type') == 'bibr'
                    and re.fullmatch(r'\s*[-–—]\s*', node.tail or '')
                    and len((following.get('rid') or '').split()) == 1):
                expanded = self._expand_range(targets[0], following.get('rid').strip())
                if expanded:
                    targets = expanded
                    group.append(following)
                    self.tail_replacements[path] = ''
                    method = 'explicit_numeric_range_with_complete_source_labels'
            elif (len(targets) == 2 and re.fullmatch(r'\s*\d+\s*[-–—]\s*\d+\s*', plain(node))):
                expanded = self._expand_range(*targets)
                if expanded:
                    targets, method = expanded, 'explicit_numeric_range_with_complete_source_labels'
            targets = list(dict.fromkeys(targets))
            replacement = ' '.join(self.format_reference(rid) for rid in targets)
            if not targets:
                replacement = '[bib_ref]Unresolved source citation: ' + plain(node) + '[/bib_ref]'
            mention = dict(id=f'{self.pmcid}:citation{len(self.mentions):04d}',
                source_xpaths=[self.paths[n] for n in group],
                raw_marker=''.join(plain(n) + ((n.tail or '') if n is not group[-1] else '') for n in group),
                explicit_rids=[rid for n in group for rid in (n.get('rid') or '').split()],
                target_xml_ids=targets, reference_ids=[f'{self.pmcid}:ref:{rid}' for rid in targets],
                unresolved_target_ids=[rid for rid in targets if rid not in self.by_xml_id],
                resolution_method=method, training_replacement=replacement,
                source_xml_sha256=source_sha256)
            self.mentions.append(mention)
            for i, n in enumerate(group):
                p = self.paths[n]
                consumed.add(p)
                self.replacements[p] = replacement if i == 0 else ''

    def mentions_in(self, node, *, exclude_floats=False):
        paths = {self.paths[x] for x in node.iter('xref')
                 if not exclude_floats or not any(a.tag in {'fig', 'table-wrap'}
                     for a in x.iterancestors() if a is not node)}
        return [m['id'] for m in self.mentions if paths.intersection(m['source_xpaths'])]

    def normalized_copy(self, node):
        if node is None:
            return None
        result = copy.deepcopy(node)
        pairs = list(zip(node.iter(), result.iter()))
        # A citation-only superscript is typography, not a scientific exponent.
        for original, cloned in pairs:
            if (original.tag == 'sup' and len(original)
                    and all(c.tag == 'xref' and c.get('ref-type') == 'bibr' for c in original)
                    and not re.sub(r'[\s,;–—\-()\[\]]', '', original.text or '')
                    and all(not re.sub(r'[\s,;–—\-()\[\]]', '', c.tail or '') for c in original)):
                cloned.tag = 'named-content'
        for original, cloned in pairs:
            path = self.paths.get(original)
            if path not in self.replacements:
                continue
            for child in list(cloned):
                cloned.remove(child)
            cloned.text = self.replacements[path]
            # Put title/author strings at normal baseline and keep adjacent prose separated.
            if cloned.text:
                cloned.text = ' ' + cloned.text + ' '
            if path in self.tail_replacements:
                cloned.tail = self.tail_replacements[path]
        return result
