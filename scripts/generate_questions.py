import json
import os
import re
import random

INPUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset.jsonl')
OUTPUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'questions.jsonl')

SENTENCE_RE = re.compile(r'(?<=[.!?]) +')

STOP_SUBJECTS = {
    'i', 'we', 'you', 'he', 'she', 'it', 'they', 'there',
    'this', 'that', 'these', 'those'
}

PATTERNS = [
    (r"(.+?)\s+(is|are)\s+(.*)", None),
    (r"(.+?)\s+refers\s+to\s+(.*)", "is"),
    (r"(.+?)\s+can\s+be\s+defined\s+as\s+(.*)", "is"),
]


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
    if text.strip().istitle() and ' ' not in text:
        return None, None
    sentences = SENTENCE_RE.split(text)
    for s in sentences:
        s = s.strip()
        if _invalid_sentence(s):
            continue
        m = None
        verb = None
        description = None
        for pat, default in PATTERNS:
            m = re.match(pat, s, flags=re.IGNORECASE)
            if m:
                if default is None:
                    verb = m.group(2)
                    description = m.group(3)
                else:
                    verb = default
                    description = m.group(2)
                break
        if not m:
            continue
        subject = m.group(1).strip()
        description = description.rstrip('.').strip()
        if len(subject.split()) > 6:
            continue
        if not re.match(r'^[A-Za-z][A-Za-z -]*$', subject):
            continue
        if subject.lower() in STOP_SUBJECTS:
            continue
        if len(description.split()) < 5 or len(description.split()) > 20:
            continue
        stems = [
            lambda subj, verb: f"What {verb} {subj}?",
            lambda subj, verb: f"Define {subj}.",
            lambda subj, verb: f"In psychology, what {verb} {subj}?",
        ]
        q = random.choice(stems)(subject, verb)
        a = f"{subject} {verb} {description}."
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
