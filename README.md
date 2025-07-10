# PsychBooks

This repository hosts several openly licensed psychology textbooks. Each book is stored in a separate directory containing a `content.md` file and images referenced from that text.

## Dataset Preparation

Use the script below to transform the markdown sources into a single machine readable dataset. The output is suitable for downstream tasks such as question generation.

An optional `-o` argument lets you choose a custom output path.

```bash
python scripts/prepare_dataset.py -o my_dataset.jsonl
```

## Tutor Model

After preparing the dataset you can build a simple tutor model and launch an interactive session.

```bash
python scripts/generate_questions.py -i dataset.jsonl -o questions.jsonl \
    -l 500        # create up to 500 questions
python train_tutor.py                       # build tutor_model.json
python interactive_tutor.py                 # start the tutor
```

The question generator accepts optional `--input`, `--output`, and `--limit`
flags. When omitted it looks for `dataset.jsonl` and writes `questions.jsonl`
while processing up to 100 paragraphs.

Quality checks rely on a small psychology lexicon stored in `psych_terms.txt`.
If this file is present, candidate questions must include at least two of these
keywords and the answer length must fall between 7 and 30 words.

The tutor now assigns a concept to each question based on the subject of the prompt. During an interactive session your knowledge is updated per concept so you receive a mastery summary at the end.

