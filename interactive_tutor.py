import json
import difflib
import random
import os

MODEL_PATH = 'tutor_model.json'


class StudentModel:
    def __init__(self, guess=0.25, slip=0.1, initial=0.2):
        self.knowledge = {}
        self.guess = guess
        self.slip = slip
        self.initial = initial

    def update(self, concept, correct):
        p = self.knowledge.get(concept, self.initial)
        if correct:
            numerator = p * (1 - self.slip)
            denominator = numerator + (1 - p) * self.guess
            p = numerator / denominator
        else:
            numerator = p * self.slip
            denominator = numerator + (1 - p) * (1 - self.guess)
            p = numerator / denominator
        self.knowledge[concept] = p
        return p


def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        raise SystemExit('Tutor model not found. Run train_tutor.py first.')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def ask_questions(pairs):
    student = StudentModel()
    random.shuffle(pairs)
    for qa in pairs:
        question = qa["question"]
        answer = qa["answer"]
        concept = qa.get("concept", question)
        print("\nQuestion:", question)
        user = input("Your answer: ").strip()
        similarity = difflib.SequenceMatcher(None, user.lower(), answer.lower()).ratio()
        correct = similarity >= 0.6
        if correct:
            print("Correct!")
        else:
            print("Incorrect.")
            print("Expected answer:", answer)
        mastery = student.update(concept, correct)
        print(f"Mastery for this concept: {mastery:.2f}")
        cont = input('Press Enter for next question or type "quit" to exit: ')
        if cont.strip().lower() == 'quit':
            break
    if student.knowledge:
        print("\nSummary of mastery:")
        for c, p in sorted(student.knowledge.items()):
            print(f"  {c}: {p:.2f}")


def main():
    qa_pairs = load_model()
    if not qa_pairs:
        print('Model contains no question-answer pairs.')
        return
    print('Interactive tutor starting. Type "quit" to exit.')
    ask_questions(qa_pairs)


if __name__ == '__main__':
    main()
