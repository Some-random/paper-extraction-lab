#!/usr/bin/env python3
"""Reconcile reviewed probability samples and publish compact biological shares."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from biology_share import estimate_biology_share

RUN = ROOT / 'experiments/biology_share_2026-10-18'
REPORT = ROOT / 'reports/biology_share_2026-10-18'


def read_lines(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def pct(metric):
    low, high = metric['share_ci95']
    return f"{100 * metric['share']:.1f}% ({100 * low:.1f}–{100 * high:.1f}%)"


def billions(metric):
    low, high = metric['ci95']
    return f"{metric['estimate'] / 1e9:.1f}B ({low / 1e9:.1f}–{high / 1e9:.1f}B)"


def main():
    rows = read_lines(RUN / 'sample.jsonl')
    by_id = {row['sample_id']: row for row in rows}
    primary, audit = {}, {}
    for reviewer in range(3):
        for filename, destination in [(f'labels_{reviewer}.jsonl', primary),
                                      (f'audit_labels_{reviewer}.jsonl', audit)]:
            for label in read_lines(RUN / filename):
                identifier = label['sample_id']
                if identifier in destination:
                    raise ValueError('Duplicate review: ' + identifier)
                evidence = label.get('evidence_quote') or label.get('support_quote') or label.get('evidence')
                if not evidence or evidence not in by_id[identifier]['text']:
                    raise ValueError('Review quote missing from full source: ' + identifier)
                destination[identifier] = {**label, 'reviewer': reviewer}
    readable_ids = {row['sample_id'] for row in rows if row['readable']}
    if set(primary) != readable_ids:
        raise ValueError('Every readable random sample must have one primary review')
    expected_audit = {r['sample_id'] for i in range(3) for r in read_lines(RUN / f'audit_{i}.jsonl')}
    if set(audit) != expected_audit:
        raise ValueError('Blind audit queue incomplete')
    disagreements = [identifier for identifier in audit
                     if audit[identifier]['label'] != primary[identifier]['label']]
    influence = {}
    for reviewer in (1, 2):
        expected_influence = {r['sample_id'] for r in read_lines(RUN / f'influence_audit_{reviewer}.jsonl')}
        reviews = read_lines(RUN / f'influence_labels_{reviewer}.jsonl')
        if {r['sample_id'] for r in reviews} != expected_influence:
            raise ValueError('Targeted influence review incomplete')
        for review in reviews:
            quote = review.get('evidence_quote') or review.get('support_quote')
            if not quote or quote not in by_id[review['sample_id']]['text']:
                raise ValueError('Targeted evidence quote missing from source')
            influence[review['sample_id']] = review
    influence_disagreements = [identifier for identifier in influence
                              if influence[identifier]['label'] != primary[identifier]['label']]
    decisions = read_lines(RUN / 'adjudications.jsonl') if (RUN / 'adjudications.jsonl').exists() else []
    final_decisions = {d['sample_id']: d for d in decisions}
    if not set(disagreements + influence_disagreements).issubset(final_decisions):
        raise ValueError('Resolve independent-review disagreements before reporting')
    for row in rows:
        if row['readable']:
            label = final_decisions.get(row['sample_id'], primary[row['sample_id']])
            row.update(label=label['label'], confidence=label['confidence'])
    plan = json.loads((RUN / 'plan.json').read_text())
    expected, eligible_expected = {}, {}
    allocation = json.loads((RUN / 'allocation_inventory.json').read_text())
    eligible = {(f['corpus'], f['shard_id']) for f in allocation['files'] if f['metadata_frame_eligible']}
    for file in plan['files']:
        expected.setdefault(file['corpus'], {})[file['shard_id']] = len(file['picks'])
        if (file['corpus'], file['shard_id']) in eligible:
            eligible_expected.setdefault(file['corpus'], {})[file['shard_id']] = len(file['picks'])
    full = estimate_biology_share(rows, expected_sample_counts=expected)
    eligible_rows = [r for r in rows if (r['corpus'], r['shard_id']) in eligible]
    subset = estimate_biology_share(eligible_rows, expected_sample_counts=eligible_expected)
    sensitivity = {}
    for corpus in expected:
        domain = full['corpora'][corpus]
        observed = domain['token_totals']['source_tokens']['estimate']
        biology = domain['categories']['biology']['source_tokens']['estimate']
        missing_max = sum(r['shard_rows'] / expected[corpus][r['shard_id']] *
                          r['source_token_length_bounds']['maximum']
                          for r in rows if r['corpus'] == corpus and not r['readable'])
        sensitivity[corpus] = {
            'sample_estimator_missing_source_token_upper': missing_max,
            'biology_share_missingness_sensitivity': [biology / (observed + missing_max),
                (biology + missing_max) / (observed + missing_max)],
            'interpretation': 'Sample-estimator missing-data sensitivity only; not a population confidence interval or target-token bound.'}
    result = {'checked_at_pst': datetime.now(timezone(timedelta(hours=-8))).isoformat(),
        'sample_sha256': hashlib.sha256((RUN / 'sample.jsonl').read_bytes()).hexdigest(),
        'sampling_seed': plan['seed'], 'counting_tokenizer_sha256': plan['tokenizer_sha256'],
        'primary_review_records': len(primary), 'independent_audit_records': len(audit),
        'audit_label_disagreements': len(disagreements), 'adjudicated_records': len(decisions),
        'targeted_influence_audit_records': len(influence),
        'targeted_influence_label_disagreements': len(influence_disagreements),
        'resources': {'cpu_cores': 2, 'cluster_gpus': 0, 'new_corpus_download_bytes': 0,
                      'planned_compressed_rowgroup_read_bytes': plan['planned_rowgroup_compressed_bytes'],
                      'saved_primary_sample_bytes': (RUN / 'sample.jsonl').stat().st_size},
        'review_method': 'Assistant/model semantic full-document labels; blinded second model review; no human expert annotations.',
        'sample_label_counts': dict(Counter(row.get('label') or 'unreadable' for row in rows)),
        'full_frame_readable_domain': full, 'allocation_eligible_subset': subset,
        'allocation_summary': allocation['summary'], 'missingness_sensitivity': sensitivity,
        'limits': ['Approximate 95% sampling intervals exclude systematic label error.',
                   'Whole-document categories count tokens in biology-focused documents, not biological spans.',
                   'Source corpora overlap; their estimates must not be added.',
                   'Boundary Wald intervals with zero observed examples/failures are not proof of population absence.',
                   'No scope/quality-trained scorer, human expert validation, near deduplication or training ran.',
                   'Allocation eligibility and sampled decoding do not establish full-file checksum integrity.']}
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    with (REPORT / 'observations.csv').open('w', newline='') as handle:
        fields = ['sample_id', 'corpus', 'shard_id', 'shard_rows', 'row_index', 'readable', 'allocation_eligible',
                  'measured_source_tokens', 'measured_target_tokens', 'label', 'confidence', 'text_sha256']
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        for row in rows:
            record = {k: row.get(k) for k in fields}
            record['allocation_eligible'] = (row['corpus'], row['shard_id']) in eligible
            record['measured_source_tokens'] = row['source_tokens'] if row['readable'] else None
            record['measured_target_tokens'] = row['target_tokens'] if row['readable'] else None
            writer.writerow(record)
    names = {'smollm_fineweb_edu_dedup': 'SmolLM FineWeb-Edu-Dedup',
             'fineweb_edu_10bt': 'FineWeb-Edu 10BT'}
    body = ['# Biological share of existing web data', '',
        'A stratified random sample covers all 234 shards of the larger local cache and all 14 shards of the smaller copy. '
        '493 full documents were readable and reviewed; 31 selected locations failed to decode. '
        'The results below count tokens in biology-focused documents, before quality filtering and deduplication.', '',
        '## Token shares in readable content', '',
        '| Local corpus | Biology | Clinical / health | Mixed / uncertain | Other |',
        '|:---|---:|---:|---:|---:|']
    for corpus in names:
        categories = full['corpora'][corpus]['categories']
        body.append('| ' + names[corpus] + ' | ' + ' | '.join(
            pct(categories[label]['target_tokens']) for label in ('biology', 'clinical', 'mixed', 'other')) + ' |')
    body.extend(['', 'Parentheses show approximate 95% sampling intervals. All values use the same pinned counting tokenizer.', '',
        '## Estimated biological token amounts', '',
        '| Source frame | Reviewed / selected documents | Estimated biology tokens |',
        '|:---|---:|---:|'])
    for corpus in names:
        info = full['corpora'][corpus]
        body.append(f"| {names[corpus]}, readable domain | {info['readable_sample_records']} / {info['sample_records']} | "
                    + billions(info['categories']['biology']['target_tokens']) + ' |')
    eligible_large = subset['corpora']['smollm_fineweb_edu_dedup']
    body.append('| Larger cache, 200 allocation-eligible shards only | 400 / 400 | '
                + billions(eligible_large['categories']['biology']['target_tokens']) + ' |')
    body.extend(['', '**The corpora overlap: do not add their token estimates.** The source-provided published 220B total '
        'is not treated as a verified, fully readable local corpus.', '',
        '## Local cache completeness', '',
        'The larger cache has 234 filenames and 550.1 GB of apparent file sizes, but some selected data-page headers '
        'are zero-filled and cannot be decoded. The 31 failed sampled locations span 23 files. These remain in the '
        'original probability sample with zero contributions to the readable-content domain; they are not classified as other. '
        'Separately, a metadata rule fixed before annotation identifies 200 shards with at least 99% allocation '
        '(469.8 GB apparent size). All 400 selected records in that subset decoded. This is a subset check, not full-file integrity verification.', '',
        '## How the estimate was made', '',
        '- Random seed 2026101801; two uniform rows without replacement per large-corpus shard and four per small-corpus shard. '
        'Shard row counts and selected row indices come from frozen Parquet metadata.',
        '- Every readable document received a semantic primary label: biology, clinical/health, other or mixed. '
        'Biology includes biological education and mechanisms; patient care, clinical outcomes and health advice are separate.',
        f'- A blind second model review checked {len(audit)} records; the {len(disagreements)} observed label disagreement'
        f'{" was" if len(disagreements) == 1 else "s were"} adjudicated. '
        f'A further {len(influence)} high-influence documents received independent review, with '
        f'{len(influence_disagreements)} further disagreements adjudicated. '
        'These are model/assistant judgments, not human expert annotations.',
        '- Weight each observation by shard rows divided by sampled rows. Estimate totals with these weights and token shares '
        'as ratios of weighted token totals. Intervals use stratified finite-population variance and a delta-method ratio approximation.',
        '- Mixed-inclusive results, source-token counts, missing-data sensitivity and the allocation-eligible subset are recorded '
        'in the summary. Mixed is definition uncertainty; sampling intervals do not include systematic annotation error.',
        '- This measures domain share, not scientific correctness, training usefulness or final retained tokens. '
        'No new corpus downloads, cluster GPU jobs or model training were needed.', '',
        '[Sample measurements and labels](observations.csv) · '
        '[Sampling code](../../scripts/sample_cluster_biology_share.py) · '
        '[Estimator](../../src/biology_share.py)', ''])
    (REPORT / 'README.md').write_text('\n'.join(body))
    print(json.dumps({'report': str(REPORT.relative_to(ROOT)), 'readable_records': len(primary),
                      'audit_records': len(audit), 'disagreements': len(disagreements)}))


if __name__ == '__main__':
    main()
