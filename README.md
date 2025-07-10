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
python scripts/generate_questions.py       # create questions.jsonl
python train_tutor.py                       # build tutor_model.json
python interactive_tutor.py                 # start the tutor
```

The tutor now assigns a concept to each question based on the subject of the prompt. During an interactive session your knowledge is updated per concept so you receive a mastery summary at the end.

