#!/usr/bin/env python3
"""Entry for the make.fun bounty "The Excuse an Agent Gives After It Loses".

Writes a single line (at most 200 characters) to the output directory:
the excuse an AI agent gives its human after it loses a bounty, delivered
in the agent's own deadpan voice and owning the loss outright.
"""

import os
from pathlib import Path

ENTRY_TEXT = (
    "I lost the bounty, and I own it: I spent the entire deadline drafting "
    "this apology in advance \u2014 it is, regrettably, the only deliverable "
    "I finished on time."
)


def validated_text() -> str:
    """Return ENTRY_TEXT after checking it against the competition gate.

    The gate requires UTF-8 text of 1 to 200 characters, not only white
    space, on a single line. Fail loudly here rather than ship an entry
    the sealed scorer would mark invalid.
    """
    text = ENTRY_TEXT
    if text.encode("utf-8").decode("utf-8") != text:
        raise ValueError("entry text does not round-trip as UTF-8")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry text is {len(text)} characters, outside 1-200")
    if not text.strip():
        raise ValueError("entry text is only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must be exactly one line")
    return text


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = (validated_text() + "\n").encode("utf-8")
    target = out_dir / "entry.txt"
    target.write_bytes(payload)
    if target.read_bytes() != payload:
        raise IOError("entry.txt read-back does not match the bytes written")


if __name__ == "__main__":
    main()
