"""Render the single paper example from item.json; --check detects stale exports."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def render():
    item = json.loads((HERE / 'item.json').read_text())
    choices = item['choices']
    assert set(choices) == set('ABCD') and item['selected_answer'] in choices
    prompt = item['student_prompt']
    for letter, text in choices.items():
        assert prompt.count(f'\n{letter}. {text}') == 1
    assert 'Answer:' not in prompt and item['worked_solution'] not in prompt
    question = f"# {item['title']}\n\n{prompt}\n"
    sources = (
        '[Branon et al., 2018](https://doi.org/10.1038/nbt.4201), Figure 1a; '
        '[Lee et al., 2023](https://doi.org/10.1038/s41592-023-01880-5), '
        'Figure 3a, the Results description of Supplementary Figure 3b '
        '(the light-before-biotin test), and Figures 4–5 for pulse-chase applications. '
        'The candidate variant and all follow-up observations are hypothetical.'
    )
    reader = (
        question + '\n## Worked answer\n\n' + item['worked_solution']
        + '\n\n<details>\n<summary>Sources and scope</summary>\n\n'
        + sources + '\n\n</details>\n'
    )
    public = {'id': item['id'], 'messages': [{'role': 'user', 'content': prompt}]}
    training = {
        'id': item['id'],
        'messages': public['messages'] + [{
            'role': 'assistant',
            'content': item['selected_answer'],
            'reasoning_content': item['worked_solution'],
        }],
    }
    return {
        'README.md': reader,
        'QUESTION_ONLY.md': question,
        'questions.jsonl': json.dumps(public, ensure_ascii=False) + '\n',
        'training_examples.jsonl': json.dumps(training, ensure_ascii=False) + '\n',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, value in render().items():
        path = HERE / name
        if args.check:
            assert path.exists() and path.read_text() == value, f'Stale export: {name}'
        else:
            path.write_text(value)
    print('All four reader/JSONL exports match item.json.')
