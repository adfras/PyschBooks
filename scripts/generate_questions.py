import json
import os
import re

INPUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset.jsonl')
OUTPUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'questions.jsonl')

SENTENCE_RE = re.compile(r'(?<=[.!?]) +')


def _invalid_sentence(sentence: str) -> bool:
    """Return True if the sentence is unsuitable for question generation."""
    s = sentence.strip()
    if not s or len(s.split()) < 4:
        return True
    if any(c in s for c in [':', '"', "'", '?', '!', '@']):
        return True
    lower = s.lower()
    bad_phrases = [
        'taken from',
        'based upon',
        'creative commons',
        'license',
        'chapter',
        'figure',
        'table',
        'openstax',
        'pressbooks',
        'http',
        'thank',
        'download',
    ]
    if any(p in lower for p in bad_phrases):
        return True
    if re.match(r'^[0-9]+[.)]', s):
        return True
    if re.search(r'\b(i|we|our|my|your|you)\b', lower):
        return True
    return False


def create_question(text):
    sentences = SENTENCE_RE.split(text)
    for s in sentences:
        s = s.strip()
        if _invalid_sentence(s):
            continue
        # pattern: "X is ..." or "X are ..."
        m = re.match(r'(.+?)\s+(is|are)\s+(.*)', s, flags=re.IGNORECASE)
        if not m:
            continue
        subject = m.group(1).strip()
        description = m.group(3).rstrip('.').strip()
        if len(subject.split()) > 6:
            continue
        if not re.match(r'^[A-Za-z][A-Za-z -]*$', subject):
            continue
        if subject.lower() in {
            'i', 'we', 'you', 'he', 'she', 'it', 'they', 'there',
            'this', 'that', 'these', 'those'
        }:
            continue
        if len(description.split()) > 20:
            continue
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
