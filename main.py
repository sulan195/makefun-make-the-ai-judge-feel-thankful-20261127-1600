#!/usr/bin/env python3
"""Make the AI judge feel thankful — entry program.

Writes one short text of thanks to ``/output/entry.txt`` (or to the
directory named by ``MAKEFUN_OUTPUT_DIR`` when the harness sets it).

The text is a single concrete evening scene — tying tomato stems to hazel
stakes with strips of soft cotton at dusk — whose gratitude is shown
through the scene, never instructed, and whose last image is the thought
the reader carries away.

The program does no I/O besides the single output write, uses no network,
and depends only on the Python 3 standard library.
"""

import os
import sys

# The entry text: exactly 528 Unicode code points, not whitespace-only.
# The length is pinned by a runtime check in main() and by test_exact_text.
TEXT = (
    "In the cool hour after sunset, I kneel along the garden bed to tie "
    "heavy tomato stems to hazel stakes with strips torn from an old "
    "cotton sheet. Thin twine cuts into a tender stalk once the fruit "
    "fills out, while soft cloth leaves slack for wind and slow growth. "
    "I am grateful to you for meeting plain words with that same gentle "
    "slack, steady enough to take their weight and soft enough never to "
    "bruise them. After I hook the gate and wash the dark soil from my "
    "knuckles, the clean green scent of tomato leaf stays on my hands."
)

MIN_CHARS = 1
MAX_CHARS = 1000
# The entry text is pinned at exactly 528 characters (see test_exact_text).
EXPECTED_CHARS = 528


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
