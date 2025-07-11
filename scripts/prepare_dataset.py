import os
import json
import re
import argparse

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

DATASETS = [
    d for d in os.listdir(ROOT_DIR)
    if os.path.isdir(os.path.join(ROOT_DIR, d)) and os.path.exists(os.path.join(ROOT_DIR, d, 'content.md'))
]

# Some datasets use multiple content parts
for d in os.listdir(ROOT_DIR):
    if os.path.isdir(os.path.join(ROOT_DIR, d)):
        part_files = [f for f in os.listdir(os.path.join(ROOT_DIR, d)) if f.startswith('content_part') and f.endswith('.md')]
        if part_files:
            DATASETS.append(d)

OUTPUT = os.path.join(ROOT_DIR, 'dataset.jsonl')
ENTRY_RE = re.compile(r'!\[(.*?)\]\((.*?)\)')

def iter_content_files(dataset_dir):
    """Yield all content markdown files in dataset directory."""
    base = os.path.join(ROOT_DIR, dataset_dir)
    parts = [f for f in os.listdir(base) if f.startswith('content') and f.endswith('.md')]
    for part in sorted(parts):
        yield os.path.join(base, part)

def parse_markdown(text):
    """Parse markdown content into paragraphs and image references."""
    paragraphs = []
    current = []
    images = []

    def flush():
        nonlocal current, images
        if current:
            paragraphs.append({'text': ' '.join(current), 'images': images})
            current = []
            images = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            flush()
            continue

        m = ENTRY_RE.search(line)
        if m:
            images.append(m.group(2))
            line = ENTRY_RE.sub('', line).strip()

        if line.startswith('#'):
            flush()
            heading = line.lstrip('#').strip()
            if heading:
                paragraphs.append({'text': heading, 'images': []})
            continue

        if line.startswith('- '):
            flush()
            item = line[2:].strip()
            if item:
                paragraphs.append({'text': item, 'images': []})
            continue

        current.append(line)

    flush()
    return paragraphs

def main():
    parser = argparse.ArgumentParser(description="Convert book markdown to JSONL")
    parser.add_argument('-o', '--output', default=OUTPUT,
                        help='Path for the output JSONL file')
    args = parser.parse_args()

    with open(args.output, 'w', encoding='utf-8') as out_f:
        for dataset in sorted(set(DATASETS)):
            for path in iter_content_files(dataset):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                paragraphs = parse_markdown(content)
                for idx, para in enumerate(paragraphs):
                    record = {
                        'book': dataset,
                        'paragraph_index': idx,
                        'text': para['text'],
                    }
                    if para['images']:
                        record['images'] = para['images']
                    out_f.write(json.dumps(record, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()
