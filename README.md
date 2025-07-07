# PyschBooks

This repository hosts several openly licensed psychology textbooks. Each book is stored in a separate directory containing a `content.md` file and images referenced from that text.

## Dataset Preparation

Use the script below to transform the markdown sources into a single machine readable dataset. The output is suitable for downstream tasks such as question generation.

```bash
python scripts/prepare_dataset.py
```

The script creates `dataset.jsonl` with one paragraph per line. Image references are retained in a list under the `images` key.
