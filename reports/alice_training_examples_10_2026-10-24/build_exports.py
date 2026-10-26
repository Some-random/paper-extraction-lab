#!/usr/bin/env python3
"""Render and validate Alice10 exports from the ten canonical Markdown pages."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import posixpath
import re
from pathlib import Path


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def jsonl(rows: list[dict]) -> str:
    return ''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows)


def plain(text: str) -> str:
    text = re.sub(r'<details>.*?</details>', '', text, flags=re.S)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.M)
    text = re.sub(r'^```[^\n]*\n|^```\s*$', '', text, flags=re.M)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return text.replace('**', '').strip() + '\n'


def aggregate_links(text: str) -> str:
    """Rebase links from an examples/ page into the collection-root render."""
    def replace(match: re.Match) -> str:
        target = match.group(1)
        if target.startswith('#') or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
            return match.group(0)
        path, marker, fragment = target.partition('#')
        rebased = posixpath.normpath(posixpath.join('examples', path))
        return '](' + rebased + (marker + fragment if marker else '') + ')'
    return re.sub(r'\]\(([^)]+)\)', replace, text)


def render(root: Path) -> dict[str, str]:
    revision = json.loads((root / 'revision_v6.json').read_text())
    review = json.loads((root / 'review_v6.json').read_text())
    internal = json.loads((root / 'internal/assessment_rubrics.json').read_text())
    assert review['status'] == 'assistant_review_passed'
    assert revision['format'] == 'open_response'
    questions, training, verification, provenance, docs = [], [], [], [], []
    table = io.StringIO(newline='')
    writer = csv.writer(table, lineterminator='\n')
    writer.writerow(['example', 'question_topic', 'question_and_answer', 'format'])
    for i in range(1, 11):
        item_id = f'example-{i:02d}'
        rel = f'examples/{item_id}.md'
        text = (root / rel).read_text()
        assert text.startswith(f'# {i}. '), rel
        title = text.splitlines()[0].split('. ', 1)[1]
        assert text.count('\n## Question\n') == 1, rel
        assert text.count('\n## Answer\n') == 1, rel
        assert '\n## Assessment rubric\n' not in text, (rel, 'grading rubric in reader-facing page')
        question = text.split('\n## Question\n', 1)[1].split('\n## Answer\n', 1)[0].strip()
        answer, notes = text.split('\n## Answer\n', 1)[1].split('<details>', 1)
        answer = answer.strip()
        rubric = internal['examples'][item_id]['assessment_rubric']
        assert '</details>' in notes, rel
        assert question and answer and rubric, rel
        assert 'Final answer:' not in question and 'Choices:' not in question, rel
        assert rubric.count('\n- ') + int(rubric.startswith('- ')) >= 3, rel
        references = re.findall(r'\]\((https?://[^)]+)\)', notes)
        assert references, rel
        if 4 <= i <= 8:
            sequence = ''.join(re.findall(r'```text\n(.*?)\n```', question, flags=re.S)).replace('\n', '').replace(' ', '')
            assert sequence and sha(sequence) == revision['retained_sequence_sha256'][item_id], rel
        elif '```text' in question:
            raise AssertionError((rel, 'unused full sequence retained'))
        assert sha(text) == review['reviewed_example_sha256'][item_id], (rel, 'unreviewed edit')
        purpose = revision['purposes'][item_id]
        questions.append({'schema': 'alice10-open-response-v6', 'id': item_id, 'title': title,
                          'format': 'open_response', 'purpose': purpose,
                          'student_prompt': question, 'question': question})
        training.append({'schema': 'alice10-training-example-v6', 'id': item_id,
                         'authoring_method': 'source_aware_assistant_revision',
                         'messages': [{'role': 'user', 'content': question},
                                      {'role': 'assistant', 'content': answer}]})
        verification.append({'schema': 'alice10-reference-review-v6', 'id': item_id,
                             'format': 'open_response', 'reference_answer': answer,
                             'assessment_rubric': rubric, 'review_status': 'assistant_review_passed',
                             'review_scope': 'source consistency, evidence use and worked-answer completeness',
                             'student_prompt_sha256': sha(question), 'reference_answer_sha256': sha(answer),
                             'expert_human_validation': False, 'training_gain_measured': False})
        provenance.append({'id': item_id, 'revision': 6, 'method': 'source_aware_assistant_revision',
                           'purpose': purpose, 'source_references': references,
                           'canonical_page': rel, 'canonical_page_sha256': sha(text),
                           'student_prompt_sha256': sha(question), 'reference_answer_sha256': sha(answer),
                           'earlier_version': f"https://github.com/Some-random/paper-extraction-lab/blob/{revision['previous_commit']}/reports/alice_training_examples_10_2026-10-24/{rel}"})
        writer.writerow([i, title, rel, 'open_response'])
        docs.append(aggregate_links(text.strip()))
    all_md = '# Ten protein reasoning problems and worked answers\n\n' + '\n\n---\n\n'.join(docs) + '\n'
    questions_md = '# Ten protein reasoning problems\n\nWorked answers are in ALL_EXAMPLES.md.\n\n'
    questions_md += '\n\n---\n\n'.join(f"# {i}. {row['title']}\n\n{row['student_prompt']}" for i, row in enumerate(questions, 1)) + '\n'
    prov = {'schema': 'alice10-provenance-v6', 'current_revision': 6,
            'authoring_method': 'source_aware_assistant_revision', 'examples': provenance,
            'previous_commit': revision['previous_commit'], 'revision_record': 'revision_v6.json',
            'review_record': 'review_v6.json', 'new_teacher_api_calls': 0,
            'presentation_record': 'presentation_update_v1.json',
            'expert_human_review_performed': False, 'student_training_released': False,
            'training_gain_measured': False}
    return {'ALL_EXAMPLES.md': all_md, 'ALL_EXAMPLES.txt': plain(all_md),
            'QUESTIONS_ONLY.md': questions_md, 'QUESTIONS_ONLY.txt': plain(questions_md),
            'questions.jsonl': jsonl(questions), 'training_examples.jsonl': jsonl(training),
            'verification.jsonl': jsonl(verification), 'selection.csv': table.getvalue(),
            'selection_provenance.json': json.dumps(prov, ensure_ascii=False, indent=2) + '\n'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='validate without writing')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    outputs = render(root)
    pages = {root / name: text for name, text in outputs.items() if name.endswith('.md')}
    pages.update({path: path.read_text() for path in (root / 'examples').glob('example-*.md')})
    for path, text in pages.items():
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith('#') or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            local = (path.parent / target.split('#', 1)[0]).resolve()
            assert local.exists() or local in {p.resolve() for p in pages}, (str(path), 'broken local link', target)
    for name, text in outputs.items():
        path = root / name
        if args.check:
            assert path.read_text() == text, (name, 'stale export')
        else:
            path.write_text(text)
    total = sum((root / name).stat().st_size for name in outputs)
    print(json.dumps({'status': 'passed', 'examples': 10, 'exports': len(outputs),
                      'export_bytes': total, 'mode': 'check' if args.check else 'build'}))


if __name__ == '__main__':
    main()
