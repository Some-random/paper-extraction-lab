"""Scientific content/provenance regression checks for native training views."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from lxml import etree
from tokenizers import Tokenizer, models, pre_tokenizers
from native_training import scientific_text, table_grid, parse_jats, interleaved_records, pack_text


def tokenizer():
    tok = Tokenizer(models.WordLevel({'[UNK]': 0}, unk_token='[UNK]'))
    tok.pre_tokenizer = pre_tokenizers.Whitespace()
    return tok


class ScientificSourceChecks(unittest.TestCase):
    def test_cited_titles_authors_ranges_and_source_typography(self):
        source = b'''<article><front><article-meta><title-group><article-title>Test</article-title></title-group></article-meta></front><body>
        <p>Evidence<sup><xref ref-type="bibr" rid="R1">1</xref>&#8211;<xref ref-type="bibr" rid="R3">3</xref></sup>; P = 10<sup>-10</sup>.</p>
        <fig id="F1"><caption><p>Caption <xref ref-type="bibr" rid="R2">2</xref>.</p></caption></fig>
        <table-wrap id="T1"><caption><p>Table caption.</p></caption><table><tbody><tr><td>ACGT</td><td><xref ref-type="bibr" rid="R2">2</xref></td></tr></tbody></table></table-wrap>
        </body><back><ref-list>
        <ref id="R1"><label>1</label><element-citation><person-group person-group-type="author"><name><surname>Hsu</surname><given-names>Y.</given-names></name><name><surname>Fuchs</surname></name></person-group><article-title>Building skin</article-title><year>2022</year><pub-id pub-id-type="doi">10.test/skin</pub-id></element-citation></ref>
        <ref id="R2"><label>2</label><citation-alternatives><element-citation><person-group><name><surname>Jones</surname></name></person-group><article-title>Protein mechanisms</article-title></element-citation><mixed-citation>DUPLICATE TITLE</mixed-citation></citation-alternatives></ref>
        <ref id="R3"><label>3</label><element-citation><person-group><collab>Genome Consortium</collab></person-group><article-title>Genome study</article-title></element-citation></ref>
        </ref-list></back></article>'''
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'source.xml'
            path.write_bytes(source)
            doc = parse_jats(path, 'PAPER', tokenizer())
            paragraph = next(b for b in doc['blocks'] if b['kind'] == 'paragraph')
            self.assertIn('1', paragraph['text'])
            self.assertIn('Building skin — Hsu et al.', paragraph['training_text'])
            self.assertIn('Protein mechanisms — Jones', paragraph['training_text'])
            self.assertIn('Genome study — Genome Consortium', paragraph['training_text'])
            self.assertEqual(paragraph['training_text'].count('[bib_ref]'), 3)
            self.assertNotIn('^([bib_ref]', paragraph['training_text'])
            self.assertIn('10^(-10)', paragraph['training_text'])
            self.assertNotIn('DUPLICATE TITLE', paragraph['training_text'])
            self.assertEqual(doc['citation_mentions'][0]['target_xml_ids'], ['R1', 'R2', 'R3'])
            self.assertEqual(doc['bibliography'][0]['identifiers']['doi'], '10.test/skin')
            self.assertEqual(len(doc['bibliography'][0]['authors']), 2)
            figure = next(v for v in doc['visuals'] if v['kind'] == 'figure')
            self.assertIn('Protein mechanisms — Jones', figure['caption_training_text'])
            table = next(v for v in doc['visuals'] if v['kind'] == 'table')
            self.assertIn('Protein mechanisms — Jones', table['table']['text_tsv'])
            self.assertEqual(table['table']['cells'][1]['text'], '2')
            self.assertEqual(path.read_bytes(), source)

    def test_missing_citation_metadata_is_preserved_and_unknown_targets_are_explicit(self):
        source = b'''<article><front><article-meta><title-group><article-title>Test</article-title></title-group></article-meta></front><body><p>See <xref ref-type="bibr" rid="R1 MISSING">1, 2</xref>.</p></body><back><ref-list><ref id="R1"><label>1</label><mixed-citation>Unstructured source citation.</mixed-citation></ref></ref-list></back></article>'''
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'source.xml'
            path.write_bytes(source)
            doc = parse_jats(path, 'PAPER', tokenizer())
            self.assertIn('[bib_ref]Unstructured source citation.[/bib_ref]', doc['blocks'][0]['training_text'])
            self.assertIn('PAPER:MISSING', doc['blocks'][0]['training_text'])
            self.assertEqual(doc['unresolved_citations'][0]['unresolved_target_ids'], ['MISSING'])

    def test_reference_segmentation_requires_source_evidence(self):
        source = b'''<article><front><article-meta><title-group><article-title>Test</article-title></title-group></article-meta></front><body><p>Text.</p></body><back><ref-list><ref id="R1"><mixed-citation>Actual source.</mixed-citation></ref></ref-list></back></article>'''
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'source.xml'
            path.write_bytes(source)
            with self.assertRaisesRegex(ValueError, 'lacks source evidence'):
                parse_jats(path, 'PAPER', tokenizer(), citation_overrides={'R1': {
                    'title': 'Invented title', 'required_source_literals': ['Invented title']}})

    def test_table_without_caption_is_retained(self):
        source = b'''<article><front><article-meta><title-group><article-title>Test</article-title></title-group></article-meta></front><body><table-wrap id="T1"><label>Table 1</label><table><tbody><tr><td>ACGTACGT</td><td>0.00000000012</td></tr></tbody></table></table-wrap></body></article>'''
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'source.xml'
            path.write_bytes(source)
            doc = parse_jats(path, 'PAPER', tokenizer())
            self.assertEqual(len(doc['blocks']), 1)
            self.assertEqual(doc['blocks'][0]['kind'], 'table')
            self.assertIn('ACGTACGT\t0.00000000012', doc['blocks'][0]['training_text'])

    def test_formula_alternatives_and_exponents_are_not_flattened_twice(self):
        root = etree.fromstring(b'<p>P &lt; 1.2 x 10<sup>-10</sup>; '
            b'<alternatives><tex-math>x^2</tex-math><math><msup><mi>x</mi><mn>2</mn></msup></math></alternatives></p>')
        result = scientific_text(root)
        self.assertIn('10^(-10)', result)
        self.assertEqual(result.count('x^2'), 1)
        self.assertNotIn('x2', result)

    def test_rowspan_origins_and_paragraph_cell_boundaries(self):
        root = etree.fromstring(b'<table><thead><tr><th>Protein</th><th>n</th></tr></thead>'
            b'<tbody><tr><td><p>Gene-Derived</p><p>Protein Groups</p></td><td rowspan="2">199</td></tr>'
            b'<tr><td>Second example</td></tr></tbody></table>')
        g = table_grid(root, root.getroottree())
        self.assertEqual(g['occupancy'][1][1], g['occupancy'][2][1])
        self.assertEqual(sum(c['text'] == '199' for c in g['cells']), 1)
        self.assertEqual(g['cells'][2]['text'], 'Gene-Derived Protein Groups')
        self.assertEqual(g['cells'][3]['column_header_path'], ['n'])
        self.assertEqual(g['text_tsv'].count('199'), 1)
        self.assertIn('[merged from r1c1]', g['text_tsv'])

    def test_nonadjacent_context_is_not_stitched_and_cotext_is_not_duplicated(self):
        source = b'''<article><front><article-meta><title-group><article-title>Test</article-title></title-group><abstract><p>Abstract.</p></abstract></article-meta></front>
        <body><sec><title>Results</title><p>Both <xref ref-type="fig" rid="F1 F2">figures</xref> show measurements.</p><p>An unrelated passage.</p><p>Later <xref ref-type="fig" rid="F1">Fig. 1</xref> discusses controls.</p><fig id="F1"><label>Fig. 1</label><caption><p>First caption.</p></caption></fig><fig id="F2"><label>Fig. 2</label><caption><p>Second caption.</p></caption></fig></sec></body><back><ref-list><ref id="R1">A reference.</ref></ref-list></back></article>'''
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'source.xml'
            path.write_bytes(source)
            doc = parse_jats(path, 'TEST', tokenizer())
            records = interleaved_records(doc)
            self.assertEqual(len(records), 2)
            self.assertEqual(set(records[0]['visual_ids']), {'TEST:F1', 'TEST:F2'})
            self.assertEqual(len(records[0]['context_block_ids']), 1)
            self.assertNotIn('unrelated', records[0]['context_text'])
            self.assertTrue(any(b['exclusion_reason'] == 'bibliography' for b in doc['excluded_blocks']))
            self.assertEqual(path.read_bytes(), source)

    def test_chunk_splitting_preserves_source_and_respects_budget(self):
        value = 'β-catenin 1.2×10^(-10) ACGTACGT 67 days. ' * 30
        doc = {'pmcid': 'TEST', 'title': 'Test', 'source_xml_sha256': 'hash', 'blocks': [
            {'id': 'b1', 'training_text': value, 'source_xpath': '/article/body/p', 'section_path': ['Results']} ]}
        tok = tokenizer()
        chunks = pack_text(doc, tok, 32)
        self.assertTrue(all(c['token_count'] <= 32 for c in chunks))
        parts = [f for c in chunks for f in c['fragments']]
        self.assertEqual(''.join(f['text'] for f in parts), value)
        self.assertTrue(all(f['text'] == value[f['char_start']:f['char_end']] for f in parts))

    def test_nested_publisher_floats_do_not_leak_into_prose(self):
        source = b'''<article><front><article-meta><title-group><article-title>Test</article-title></title-group></article-meta></front>
        <body><p>Before <xref ref-type="fig" rid="F1">Fig. 1</xref>.<fig id="F1"><label>Fig. 1</label><caption><p>CAPTION ONLY <xref ref-type="fig" rid="F2">Fig. 2</xref>.</p></caption></fig> After the floating object.<table-wrap id="T1"><label>Table 1</label><caption><p>TABLE CAPTION</p></caption><table><tbody><tr><td>SECRET CELL</td></tr></tbody></table></table-wrap> Final prose.</p><fig id="F2"><caption><p>Other caption.</p></caption></fig></body></article>'''
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'source.xml'
            path.write_bytes(source)
            doc = parse_jats(path, 'TEST', tokenizer())
            prose = [b for b in doc['blocks'] if b['kind'] == 'paragraph']
            self.assertEqual(len(prose), 1)
            self.assertIn('After the floating object.', prose[0]['text'])
            self.assertIn('Final prose.', prose[0]['text'])
            self.assertNotIn('CAPTION ONLY', prose[0]['text'])
            self.assertNotIn('SECRET CELL', prose[0]['text'])
            self.assertEqual([r['rid'] for r in prose[0]['references']], ['F1'])
            self.assertEqual(sum(b['kind'] == 'table' for b in doc['blocks']), 1)
            self.assertEqual(sum(b['kind'] == 'caption' for b in doc['blocks']), 3)


if __name__ == '__main__':
    unittest.main()
