import argparse
import json
import os
import re
import random
import pathlib

ROOT = os.path.dirname(os.path.dirname(__file__))
DEFAULT_INPUT = os.path.join(ROOT, 'dataset.jsonl')
DEFAULT_OUTPUT = os.path.join(ROOT, 'questions.jsonl')

# --- DOMAIN LEXICON --------------------------------------------------------
LEXICON_PATH = pathlib.Path(__file__).parent.parent / 'psych_terms.txt'
if LEXICON_PATH.exists():
    PSYCH_TERMS = {
        w.strip().lower()
        for w in LEXICON_PATH.read_text().splitlines()
        if w.strip()
    }
else:
    PSYCH_TERMS = set()

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
    return False


def score_domain(text: str) -> int:
    """Count how many psychology keywords appear in text."""
    tokens = re.findall(r"\b[a-z]+\b", text.lower())
    return sum(1 for t in tokens if t in PSYCH_TERMS)


def create_question(text: str):
    """Generate a Q-A pair if the text contains a clear psychology definition."""
    if text.strip().istitle() and " " not in text:
        return None, None

    patterns = [
        r"(.+?)\s+(is|are)\s+(.*)",
        r"(.+?)\s+(refers)\s+to\s+(.*)",
        r"(.+?)\s+(can\s+be\s+defined\s+as)\s+(.*)",
    ]

    for s in re.split(r"[.;?!]\s+", text):
        s = s.strip()
        if _invalid_sentence(s):
            continue
        for pat in patterns:
            m = re.match(pat, s, re.IGNORECASE)
            if not m:
                continue
            subj, verb, desc = (
                m.group(1).strip(),
                m.group(2).lower(),
                m.group(3).strip(),
            )

            if len(desc.split()) < 7 or len(desc.split()) > 30:
                continue
            if score_domain(subj + " " + desc) < 2:
                continue

            stem = random.choice(
                [
                    lambda x, y: f"What {y} {x}?",
                    lambda x, _: f"Define {x}.",
                    lambda x, y: f"In psychology, what {y} {x}?",
                ]
            )
            question = stem(subj, verb)
            answer = f"{subj} {verb} {desc.rstrip('.')}."
            return question, answer
    return None, None


def main(args: argparse.Namespace) -> None:
    with open(args.input, 'r', encoding='utf-8') as in_f, \
         open(args.output, 'w', encoding='utf-8') as out_f:
        for idx, line in enumerate(in_f):
            if args.limit and idx >= args.limit:
                break
            record = json.loads(line)
            q, a = create_question(record['text'])
            if q:
                out_f.write(
                    json.dumps(
                        {
                            'book': record['book'],
                            'paragraph_index': record['paragraph_index'],
                            'question': q,
                            'answer': a,
                        }
                    )
                    + '\n'
                )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate flashcard questions')
    parser.add_argument('-i', '--input', default=DEFAULT_INPUT,
                        help='Path to dataset JSONL')
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT,
                        help='Path to output questions JSONL')
    parser.add_argument('-l', '--limit', type=int, default=None,
                        help='Maximum number of paragraphs to process')
    args = parser.parse_args()
    main(args)
