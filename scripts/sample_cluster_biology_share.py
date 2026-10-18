#!/usr/bin/env python3
"""Sample uniform rows within every local Parquet shard, without copying shards."""
from __future__ import annotations

import bisect
import hashlib
import json
import os
import random
import shutil
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

os.environ['TOKENIZERS_PARALLELISM'] = 'false'
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import pyarrow as pa
import pyarrow.parquet as pq
from tokenizers import Tokenizer
from corpus_count import sha256

OUT = ROOT / 'experiments/biology_share_2026-10-18'
PST = timezone(timedelta(hours=-8))
SEED = 2026101801


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, default=str) + '\n')
    temporary.replace(path)


def main():
    if (OUT / 'sample.jsonl').exists():
        raise SystemExit('Sample already exists; preserve the frozen selection.')
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.time()
    previous_plan = json.loads((OUT / 'plan.json').read_text()) if (OUT / 'plan.json').exists() else None
    if previous_plan:
        started = datetime.fromisoformat(previous_plan['started_at_pst']).timestamp()
    pa.set_cpu_count(2)
    pa.set_io_thread_count(1)
    if hasattr(os, 'sched_getaffinity'):
        os.sched_setaffinity(0, set(sorted(os.sched_getaffinity(0))[:2]))
    config = json.loads((ROOT / 'config/corpus_count_2026-10-17.json').read_text())
    tokenizer_path = ROOT / config['tokenizer_path']
    if sha256(tokenizer_path) != config['tokenizer_sha256']:
        raise ValueError('Counting tokenizer identity mismatch')
    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    inventory_path = ROOT / 'experiments/cluster_data_inventory_2026-10-18/hf_payloads.json'
    inventory = json.loads(inventory_path.read_text())
    definitions = [(inventory[2], 'smollm_fineweb_edu_dedup', 2, 220_000_000_000),
                   (inventory[0], 'fineweb_edu_10bt', 4, 10_000_000_000)]
    rng = random.Random(SEED)
    files = []
    for entry, corpus, per_shard, reported_tokens in definitions:
        revision = entry['revisions'][0]
        for item in sorted(revision['files'], key=lambda x: x['path']):
            path = Path(item['realpath'])
            if path.stat().st_size != item['bytes']:
                raise ValueError('Source size changed: ' + item['path'])
            with pq.ParquetFile(path, pre_buffer=False) as source:
                metadata = source.metadata
                n = metadata.num_rows
                selection = sorted(rng.sample(range(n), min(per_shard, n)))
                ends, total = [], 0
                for group in range(metadata.num_row_groups):
                    total += metadata.row_group(group).num_rows
                    ends.append(total)
                picks = []
                for row in selection:
                    group = bisect.bisect_right(ends, row)
                    offset = row - (ends[group - 1] if group else 0)
                    picks.append({'row_index': row, 'row_group': group, 'offset': offset})
                group_ids = {pick['row_group'] for pick in picks}
                compressed = sum(metadata.row_group(g).column(i).total_compressed_size
                                 for g in group_ids for i in range(metadata.num_columns))
                files.append({'corpus': corpus, 'shard_id': item['path'], 'source_path': str(path),
                              'revision': revision['revision'], 'bytes': item['bytes'],
                              'source_mtime_ns': path.stat().st_mtime_ns, 'shard_rows': n,
                              'reported_corpus_tokens': reported_tokens, 'picks': picks,
                              'selected_rowgroup_compressed_bytes': compressed})
    total_read = sum(item['selected_rowgroup_compressed_bytes'] for item in files)
    if total_read > 4 * 2**30:
        raise ValueError('Sample exceeds four-GiB planned compressed-rowgroup read allowance')
    plan = {'seed': SEED, 'sampling': 'Uniform rows without replacement within each complete shard inventory',
            'started_at_pst': previous_plan['started_at_pst'] if previous_plan else datetime.now(PST).isoformat(), 'inventory_sha256': sha256(inventory_path),
            'tokenizer_sha256': config['tokenizer_sha256'], 'pyarrow_version': pa.__version__,
            'planned_rowgroup_compressed_bytes': total_read,
            'limits': {'runtime_seconds': 1800, 'rowgroup_compressed_bytes': 4 * 2**30,
                       'new_artifact_bytes': 256 * 2**20, 'minimum_free_bytes': 32 * 2**30},
            'files': files}
    if previous_plan and plan != previous_plan:
        raise ValueError('Frozen sampling plan changed on retry')
    if not previous_plan:
        write_json(OUT / 'plan.json', plan)
    print(json.dumps({'planned_shards': len(files), 'planned_docs': sum(len(f['picks']) for f in files),
                      'planned_compressed_read_bytes': total_read}), flush=True)
    records = []
    for index, item in enumerate(files):
        if time.time() - started > plan['limits']['runtime_seconds']:
            raise TimeoutError('Sampling runtime allowance reached; frozen plan retained')
        if shutil.disk_usage(OUT).free < plan['limits']['minimum_free_bytes']:
            raise OSError('Filesystem free-space floor reached')
        if (OUT / 'STOP').exists():
            raise RuntimeError('Sampling stop requested')
        current = Path(item['source_path']).stat()
        if current.st_size != item['bytes'] or current.st_mtime_ns != item['source_mtime_ns']:
            raise ValueError('Frozen source file changed during sampling')
        by_group = {}
        for pick in item['picks']:
            by_group.setdefault(pick['row_group'], []).append(pick)
        with pq.ParquetFile(item['source_path'], pre_buffer=False) as source:
            for group, picks in by_group.items():
                try:
                    table = source.read_row_group(group, use_threads=False)
                    read_error = None
                except OSError as exc:
                    table = None
                    read_error = f'{type(exc).__name__}: {exc}'
                    print(json.dumps({'unreadable_shard': item['shard_id'], 'row_group': group}), flush=True)
                for pick in picks:
                    identifier = item['corpus'] + ':' + str(index) + ':' + str(pick['row_index'])
                    base = {'sample_id': identifier, 'corpus': item['corpus'],
                            'shard_id': item['shard_id'], 'shard_rows': item['shard_rows'],
                            'row_index': pick['row_index'], 'row_group': group}
                    if read_error:
                        bounds = None
                        metadata = source.metadata
                        for column in range(metadata.num_columns):
                            col = metadata.row_group(group).column(column)
                            if col.path_in_schema.endswith('token_count') and col.statistics and col.statistics.has_min_max:
                                bounds = {'minimum': col.statistics.min, 'maximum': col.statistics.max}
                        records.append({**base, 'readable': False, 'label': None,
                                        'source_tokens': 0, 'target_tokens': 0,
                                        'zero_count_meaning': 'Out-of-readable-domain contribution, not actual token length',
                                        'source_token_length_bounds': bounds, 'read_error': read_error})
                        continue
                    original = table.slice(pick['offset'], 1).to_pylist()[0]
                    text = original['text']
                    metadata = original.get('metadata') or original
                    source_tokens = metadata.get('token_count')
                    if not isinstance(source_tokens, int) or source_tokens <= 0 or not text.strip():
                        raise ValueError('Missing token count or empty selected document')
                    record = {**base, 'readable': True,
                              'source_id': original.get('id'), 'url': metadata.get('url'),
                              'source_tokens': source_tokens,
                              'target_tokens': len(tokenizer.encode(text, add_special_tokens=False).ids),
                              'text_sha256': hashlib.sha256(text.encode()).hexdigest(), 'text': text}
                    records.append(record)
                del table
        if index % 20 == 0:
            write_json(OUT / 'progress.json', {'status': 'sampling', 'shards_read': index + 1,
                       'shards_total': len(files), 'documents': len(records),
                       'elapsed_seconds': time.time() - started})
            print(json.dumps({'shards': index + 1, 'documents': len(records)}), flush=True)
    records.sort(key=lambda x: (x['corpus'], x['shard_id'], x['row_index']))
    raw = ''.join(json.dumps(r, ensure_ascii=False, default=str) + '\n' for r in records)
    if len(raw.encode()) > plan['limits']['new_artifact_bytes']:
        raise ValueError('Sample exceeds local artifact allowance')
    temporary = OUT / 'sample.jsonl.tmp'
    temporary.write_text(raw)
    temporary.replace(OUT / 'sample.jsonl')
    # Disperse both sources among three independent primary annotation queues.
    for partition in range(3):
        subset = [r for r in records if r['readable']][partition::3]
        (OUT / f'review_{partition}.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in subset))
    write_json(OUT / 'progress.json', {'status': 'sample_complete', 'shards_read': len(files),
               'documents': len(records), 'elapsed_seconds': time.time() - started,
               'sample_sha256': sha256(OUT / 'sample.jsonl'), 'sample_bytes': len(raw.encode()),
               'actual_category_labels': 'Pending document review; no prevalence inferred from keywords'})
    print(json.dumps({'status': 'sample_complete', 'documents': len(records),
                      'seconds': time.time() - started, 'sample_bytes': len(raw.encode())}), flush=True)


if __name__ == '__main__':
    main()
