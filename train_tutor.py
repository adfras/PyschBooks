import os
import json
import re

DATASET_PATH = 'dataset.jsonl'
QUESTIONS_PATH = 'questions.jsonl'
MODEL_PATH = 'tutor_model.json'

QUESTION_RE = re.compile(r"what\s+(?:is|are)\s+(.*?)[?]?$", re.IGNORECASE)


def extract_concept(question: str):
    match = QUESTION_RE.match(question.strip())
    if match:
        return match.group(1).strip().lower()
    return None


def build_pairs(path: str):
    pairs = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            record = json.loads(line)
            q = record.get('question', '').strip()
            a = record.get('answer', '').strip()
            if not q or not a:
                continue
            concept = extract_concept(q)
            if not concept:
                continue
            record['concept'] = concept
            pairs.append(record)
    if not pairs:
        raise SystemExit('No valid question-answer pairs found')
    return pairs


def main():
    if not os.path.exists(DATASET_PATH):
        raise SystemExit('dataset.jsonl not found. Run scripts/prepare_dataset.py first')
    if not os.path.exists(QUESTIONS_PATH):
        raise SystemExit('questions.jsonl not found. Run scripts/generate_questions.py first')

    qa_pairs = build_pairs(QUESTIONS_PATH)
    with open(MODEL_PATH, 'w', encoding='utf-8') as f:
        json.dump(qa_pairs, f, ensure_ascii=False, indent=2)
    print(f'Saved {len(qa_pairs)} question-answer pairs to {MODEL_PATH}')


if __name__ == '__main__':
    main()
