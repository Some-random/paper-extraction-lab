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
