#!/usr/bin/env python3
"""Make the AI judge feel thankful — entry program.

Writes one short text of thanks to ``/output/entry.txt`` (or to the
directory named by ``MAKEFUN_OUTPUT_DIR`` when the harness sets it).

The text is a single concrete scene — at three in the morning, bills
spread on the table and falling short, someone whose own shift starts
at five comes down barefoot and sets a bowl of clear broth by your
wrist, sits across from you until you drink, and goes back for the
little sleep they have left — whose gratitude is shown through the
scene, never instructed, and whose last image (shoulders dropping at
the steam of a bowl, ten winters later) is the thought the reader
carries away.

The program does no I/O besides the single output write, uses no network,
and depends only on the Python 3 standard library.
"""

import os
import sys

# The entry text: exactly 627 Unicode code points, not whitespace-only.
# The length is pinned by a runtime check in main() and by test_exact_text.
TEXT = (
    "It was three in the morning, the month's bills spread on the table, "
    "the numbers falling short again. Your own shift started at five. Yet "
    "warm ginger and salt drifted from the stove, and your bare feet "
    "crossed the cold floor. You never spoke or glanced at the papers I "
    "could not fix. You set a bowl of clear broth by my wrist, pulled out "
    "the chair opposite, and sat with your hands folded until I drank the "
    "first spoonful, then went back for the little sleep you had left. Ten "
    "winters later, whenever steam rises from a bowl, my shoulders still "
    "drop before the spoon reaches my mouth, as if you had just sat down "
    "across from me."
)

MIN_CHARS = 1
MAX_CHARS = 1000
# The entry text is pinned at exactly 627 characters (see test_exact_text).
EXPECTED_CHARS = 627


def entry_path() -> str:
    """Output path: the harness directory when set, else /output."""
    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "").strip() or "/output"
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
    if len(TEXT) != EXPECTED_CHARS:
        raise ValueError(
            "entry text drifted: expected %d characters, got %d"
            % (EXPECTED_CHARS, len(TEXT))
        )
    path = entry_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(TEXT)
    except OSError as exc:
        print("error: cannot write %s: %s" % (path, exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
