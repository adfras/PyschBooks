import json
import os
import re

INPUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset.jsonl')
OUTPUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'questions.jsonl')

SENTENCE_RE = re.compile(r'(?<=[.!?]) +')


def create_question(text):
    sentences = SENTENCE_RE.split(text)
    for s in sentences:
        s = s.strip()
        # pattern: "X is ..." or "X are ..."
        m = re.match(r'(.+?)\s+(is|are)\s+(.*)', s, flags=re.IGNORECASE)
        if m and len(m.group(1).split()) <= 6:
            subject = m.group(1).strip()
            description = m.group(3).rstrip('.').strip()
            q = f"What {m.group(2)} {subject}?"
            a = f"{subject} {m.group(2)} {description}."
            return q, a
    return None, None


def main():
    with open(INPUT, 'r', encoding='utf-8') as in_f, open(OUTPUT, 'w', encoding='utf-8') as out_f:
        for idx, line in enumerate(in_f):
            if idx >= 100:
                break
            record = json.loads(line)
            q, a = create_question(record['text'])
            if q:
                out_f.write(json.dumps({'book': record['book'],
                                         'paragraph_index': record['paragraph_index'],
                                         'question': q,
                                         'answer': a}) + '\n')


if __name__ == '__main__':
    main()
