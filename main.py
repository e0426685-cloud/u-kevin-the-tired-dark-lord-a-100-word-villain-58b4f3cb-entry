#!/usr/bin/env python3
"""The Tired Dark Lord: A 100-Word Villain Monologue.

Writes one original 100-word monologue, spoken by a fantasy villain who
is secretly just very tired, to /output/entry.txt (or $ENTRY_OUTPUT
when set, so the entry can be exercised locally without a root-owned
/output).

Standard library only; deterministic.

The monologue is exactly 100 words and 559 characters, inside the
competition gate of 1 to 600 UTF-8 characters. The tiredness lives in the
voice, the rhythm and the small deflections -- the kettle that sings
before the scouts do, the letter about grain, the salt -- never in a
plain statement that the villain is weary. The speaker is specific:
thirty years holding one mountain, a mason who took a repair to his
grave, a crown unpolished since the hero's grandfather tried for it,
auditors kept the comfortable chair. The sting lands in the last line.

main() validates the word count and the character gate before writing,
so a future edit that breaks the form fails loudly instead of silently
submitting an invalid entry.
"""

import os

MONOLOGUE = (
    "Come in, then. Mind the third step \u2014 the mason who built it took "
    "the repair to his grave, and I have never forgiven him. Thirty years "
    "I have held this mountain, and still the kettle sings before the "
    "scouts do. You came for the crown, I suppose. Everyone does. It sits "
    "on its cushion, unpolished since your grandfather's visit. Sit. The "
    "chair opposite is the comfortable one; I keep it for auditors. "
    "Heroes always arrive at supper, swords drawn, speeches rehearsed, "
    "and I am always mid-sentence in a letter about grain. Strike, then. "
    "But first \u2014 pass the salt."
)

# The competition gate: /output/entry.txt must be UTF-8 text of 1 to 600
# characters, not only white space.
ENTRY_MIN_CHARS = 1
ENTRY_MAX_CHARS = 600
EXPECTED_WORDS = 100

# Output path: /output/entry.txt unless ENTRY_OUTPUT overrides it, so the
# entry can be exercised locally without a root-owned /output.
ENTRY_OUTPUT = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def validate(text: str) -> int:
    """Assert *text* is a legal entry and return its word count.

    A legal entry is exactly EXPECTED_WORDS words long, fits inside the
    ENTRY_MIN_CHARS..ENTRY_MAX_CHARS character gate, and is not only
    white space. Any breach raises AssertionError with a plain message,
    so a broken monologue fails loudly before anything is written.
    """
    words = text.split()
    count = len(words)
    assert count == EXPECTED_WORDS, (
        f"expected {EXPECTED_WORDS} words, found {count}"
    )
    size = len(text)
    assert ENTRY_MIN_CHARS <= size <= ENTRY_MAX_CHARS, (
        f"entry is {size} characters, outside the "
        f"{ENTRY_MIN_CHARS}-{ENTRY_MAX_CHARS} gate"
    )
    assert text.strip(), "entry is only white space"
    return count


def main() -> None:
    words = validate(MONOLOGUE)
    os.makedirs(os.path.dirname(ENTRY_OUTPUT) or ".", exist_ok=True)
    # Guarantee exactly one trailing newline, whatever MONOLOGUE ends with.
    # Plain open() + explicit chmod 644: the grader runs as a different
    # user, so the file must be world-readable (never tempfile.mkstemp,
    # which forces mode 0600).
    text = MONOLOGUE if MONOLOGUE.endswith("\n") else MONOLOGUE + "\n"
    with open(ENTRY_OUTPUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.chmod(ENTRY_OUTPUT, 0o644)
    # Read back what landed on disk and re-validate it, so a silent
    # write failure fails loudly instead of submitting a stale file.
    with open(ENTRY_OUTPUT, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        raise ValueError("entry.txt on disk differs from the monologue")
    if validate(written.rstrip("\n")) != words:
        raise ValueError("entry.txt on disk changed word count")


if __name__ == "__main__":
    main()
