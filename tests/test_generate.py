import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.generate_questions import create_question

def test_simple():
    q, a = create_question("Memory is the process of storing information for later retrieval.")
    assert q is not None
    assert "Memory" in q
    assert "process of storing" in a


def test_skip_pronoun_subject():
    q, a = create_question(
        "This type of information is explicitly stored and retrieved."
    )
    assert q is None
    assert a is None


def test_domain_filter():
    q, a = create_question(
        "Their flippers are not very efficient for moving across the hot sand, yet they continue onward, instinctively."
    )
    assert q is None
    assert a is None


def test_valid_psych_question():
    q, a = create_question(
        "Classical conditioning refers to learning through association between specific stimuli and observable responses."
    )
    assert q is not None
    assert "Classical conditioning" in q
    assert "learning through association" in a

