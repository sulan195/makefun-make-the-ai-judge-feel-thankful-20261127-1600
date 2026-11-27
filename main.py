#!/usr/bin/env python3
"""Make the AI judge feel thankful — entry program.

Writes one short text of thanks to ``/output/entry.txt`` (or to the
directory named by ``MAKEFUN_OUTPUT_DIR`` when the harness sets it).

The text is a single concrete scene — falling asleep on the couch with
shoes still on while someone quietly tucks a blanket over you, marks
your page, and lets you rest — whose gratitude is shown through the
scene, never instructed, and whose last image is the thought the reader
carries away.

The program does no I/O besides the single output write, uses no network,
and depends only on the Python 3 standard library.
"""

import os
import sys

# The entry text: exactly 502 Unicode code points, not whitespace-only.
# The length is pinned by a runtime check in main() and by test_exact_text.
TEXT = (
    "I fell asleep on the couch with my shoes still on. You didn't wake "
    "me. You took the book from my chest, set it on the floor with the "
    "page marked. Then a blanket, heavy and old, came over my shoulders. "
    "I felt the edge tucked under my feet, not tight, just enough. The "
    "house stayed dark. I heard the kettle click off, then your steps "
    "going quiet down the hall. In the morning my shoes were side by side "
    "by the door, laces loose. The blanket smelled of cedar and toast. I "
    "sat there a while before I stood."
)

MIN_CHARS = 1
MAX_CHARS = 1000
# The entry text is pinned at exactly 502 characters (see test_exact_text).
EXPECTED_CHARS = 502


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
