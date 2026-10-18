import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError:
    raise unittest.SkipTest('Install requirements-biology-share.txt for Parquet sampling checks')
from tokenizers import Tokenizer, models, pre_tokenizers

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from corpus_count import sha256


class BiologySamplingTests(unittest.TestCase):
    def test_corrupt_selected_rows_remain_in_probability_sample(self):
        spec = importlib.util.spec_from_file_location('sample_share_test', ROOT / 'scripts/sample_cluster_biology_share.py')
        sampler = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sampler)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'config').mkdir()
            inventory = root / 'experiments/cluster_data_inventory_2026-10-18'
            inventory.mkdir(parents=True)
            tokenizer = Tokenizer(models.WordLevel({'[UNK]': 0, 'gene': 1}, unk_token='[UNK]'))
            tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
            tokenizer_path = root / 'tokenizer.json'
            tokenizer.save(str(tokenizer_path))
            (root / 'config/corpus_count_2026-10-17.json').write_text(json.dumps({
                'tokenizer_path': str(tokenizer_path), 'tokenizer_sha256': sha256(tokenizer_path)}))
            table = pa.table({'id': ['a', 'b', 'c', 'd'], 'text': ['gene'] * 4,
                              'token_count': [1] * 4, 'url': ['https://example.invalid'] * 4})
            good, bad = root / 'good.parquet', root / 'bad.parquet'
            pq.write_table(table, good, row_group_size=2)
            pq.write_table(table, bad, row_group_size=2)
            with pq.ParquetFile(bad) as source:
                offsets = [source.metadata.row_group(g).column(i).data_page_offset
                           for g in range(source.num_row_groups)
                           for i in range(source.metadata.num_columns)]
            # Preserve footer, lengths and metadata while damaging actual pages,
            # reproducing the shared cache's misleading presence/format checks.
            with bad.open('r+b') as handle:
                for offset in offsets:
                    handle.seek(offset)
                    handle.write(b'\0' * 16)

            def entry(path):
                return {'revisions': [{'revision': 'frozen', 'files': [
                    {'path': path.name, 'realpath': str(path), 'bytes': path.stat().st_size}]}]}

            (inventory / 'hf_payloads.json').write_text(json.dumps([entry(good), {}, entry(bad)]))
            output = root / 'experiment'
            old_affinity = None
            import os
            if hasattr(os, 'sched_getaffinity'):
                old_affinity = os.sched_getaffinity(0)
            try:
                with patch.object(sampler, 'ROOT', root), patch.object(sampler, 'OUT', output), redirect_stdout(io.StringIO()):
                    sampler.main()
            finally:
                if old_affinity is not None:
                    os.sched_setaffinity(0, old_affinity)
            records = [json.loads(line) for line in (output / 'sample.jsonl').read_text().splitlines()]
            self.assertEqual(len(records), 6)  # Original n=2 bad + census n=4 good.
            unreadable = [row for row in records if not row['readable']]
            self.assertEqual(len(unreadable), 2)
            self.assertTrue(all(row['label'] is None and row['source_tokens'] == 0 for row in unreadable))
            self.assertTrue(all(row['source_token_length_bounds'] == {'minimum': 1, 'maximum': 1} for row in unreadable))
            self.assertEqual(len({row['row_index'] for row in unreadable}), 2)
            queue_ids = []
            for i in range(3):
                queue_ids.extend(json.loads(line)['sample_id'] for line in
                                 (output / f'review_{i}.jsonl').read_text().splitlines())
            self.assertEqual(len(queue_ids), 4)
            self.assertTrue(set(queue_ids).isdisjoint(row['sample_id'] for row in unreadable))


if __name__ == '__main__':
    unittest.main()
