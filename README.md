# PyschBooks

This repository hosts several openly licensed psychology textbooks. Each book is stored in a separate directory containing a `content.md` file and images referenced from that text.

## Dataset Preparation

Use the script below to transform the markdown sources into a single machine readable dataset. The output is suitable for downstream tasks such as question generation.
An optional `-o` argument lets you choose a custom output path.

```bash
python scripts/prepare_dataset.py -o my_dataset.jsonl
```

The script creates `dataset.jsonl` with one paragraph per line. Image references are retained in a list under the `images` key.

## Question Generation

An example rule-based question generator is provided. It scans the first 100 entries
of `dataset.jsonl` and outputs rudimentary questions to `questions.jsonl`:

```bash
python scripts/generate_questions.py
```

This script is intentionally simple but demonstrates how the dataset can be used
for automated content creation.
