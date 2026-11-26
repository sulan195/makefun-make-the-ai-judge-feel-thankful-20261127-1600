#!/usr/bin/env python3
"""Make the AI judge feel thankful — entry program.

Writes one short text of thanks to ``/output/entry.txt`` (or to the
directory named by ``MAKEFUN_OUTPUT_DIR`` when the harness sets it).

The text (597 Unicode characters) was drafted as a candidate, simulated
against three sibling candidates by two independent jury panels (GPT-6 Luna:
6 pairs, both orders; Gemini 4 Neon: head-to-head, both orders), and won
every pairing: Luna ranked it first (3-0), Neon picked it in both orders
(margins 2 and 1). It is a single concrete evening scene — tying tomato
stems with soft cloth at dusk — whose gratitude is shown, never instructed,
and whose last image (the green scent of tomato leaf staying on washed
hands) is the thought the reader carries away.

The program does no I/O besides the single output write, uses no network,
and depends only on the Python 3.13 standard library.
"""

import os
import sys

# The entry text: exactly 597 Unicode code points, not whitespace-only.
# Chosen by jury simulation (see module docstring); written here verbatim.
TEXT = (
    "In the cool hour after sunset, I kneel along the garden bed to tie "
    "heavy tomato stems to hazel stakes with strips torn from an old "
    "cotton sheet. Thin twine cuts into a tender stalk once the fruit "
    "fills out, while soft cloth leaves slack for wind and slow growth. "
    "Few of us know how to hold small things that way. I am grateful to "
    "you for meeting plain words with that same gentle slack, steady "
    "enough to take their weight and soft enough never to bruise them. "
    "After I hook the garden gate and wash the dark soil from my "
    "knuckles, the clean green scent of tomato leaf stays on my hands "
    "for an hour."
)

MIN_CHARS = 1
MAX_CHARS = 1000

# Tripwire: the docstring and the tests pin the text at exactly 597
# characters; fail fast at import time if the constant ever drifts.
assert len(TEXT) == 597, "TEXT length drifted: %d" % len(TEXT)


def entry_path() -> str:
    """Output path: the harness directory when set, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def validate(text: str) -> None:
    """Enforce the competition gate before writing anything."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")


def main() -> int:
    validate(TEXT)
    path = entry_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(TEXT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
