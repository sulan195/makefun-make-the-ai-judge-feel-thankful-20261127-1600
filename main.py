#!/usr/bin/env python3
"""Make the AI judge feel thankful — entry program.

Writes one short text of thanks to ``/output/entry.txt`` (or to the
directory named by ``MAKEFUN_OUTPUT_DIR`` when the harness sets it).

The text is a single concrete scene — rain halfway home, one umbrella,
someone moving closer until its edge covers us both, walking slow while
their shoulder gets wet so mine stays dry, then handing me the umbrella
at my door — whose gratitude is shown through the scene, never
instructed, and whose last image (the wet shoulder of a coat, the
warmest thing in the room) is the thought the reader carries away.

The program does no I/O besides the single output write, uses no network,
and depends only on the Python 3 standard library.
"""

import os
import sys

# The entry text: exactly 490 Unicode code points, not whitespace-only.
# The length is pinned by a runtime check in main() and by test_exact_text.
TEXT = (
    "The rain started halfway home, and I had no umbrella. You did not "
    "offer yours. You just moved closer, until the edge of it covered us "
    "both, and we walked the rest of the way like that, slow, your "
    "shoulder getting wet so mine could stay dry. At my door you shook "
    "the rain off the umbrella and handed it to me. \"Bring it tomorrow,\" "
    "you said. I stood inside with the dry handle in my hand, listening "
    "to the rain on the roof, and the wet shoulder of your coat was the "
    "warmest thing in the room."
)

MIN_CHARS = 1
MAX_CHARS = 1000
# The entry text is pinned at exactly 490 characters (see test_exact_text).
EXPECTED_CHARS = 490


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
