#!/usr/bin/env python3
"""Tests for main.py — the thankful-entry program.

Covers the competition gate (1-1000 chars, not whitespace-only), the exact
output bytes, determinism across runs, the MAKEFUN_OUTPUT_DIR contract, and
the no-network rule (static import check).
"""

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(HERE, "main.py")

EXPECTED = (
    "I fell asleep on the couch with my shoes still on. You didn't wake "
    "me. You took the book from my chest, set it on the floor with the "
    "page marked. Then a blanket, heavy and old, came over my shoulders. "
    "I felt the edge tucked under my feet, not tight, just enough. The "
    "house stayed dark. I heard the kettle click off, then your steps "
    "going quiet down the hall. In the morning my shoes were side by side "
    "by the door, laces loose. The blanket smelled of cedar and toast. I "
    "sat there a while before I stood."
)


def load_main():
    spec = importlib.util.spec_from_file_location("entry_main", MAIN)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestEntryText(unittest.TestCase):
    def test_length_within_gate(self):
        module = load_main()
        self.assertGreaterEqual(len(module.TEXT), 1)
        self.assertLessEqual(len(module.TEXT), 1000)

    def test_exact_text(self):
        module = load_main()
        self.assertEqual(module.TEXT, EXPECTED)

    def test_not_whitespace_only(self):
        module = load_main()
        self.assertTrue(module.TEXT.strip())

    def test_single_text_no_newlines(self):
        module = load_main()
        self.assertNotIn("\n", module.TEXT)

    def test_validate_accepts(self):
        module = load_main()
        module.validate(module.TEXT)  # must not raise

    def test_validate_rejects_empty(self):
        module = load_main()
        with self.assertRaises(ValueError):
            module.validate("")

    def test_validate_rejects_whitespace_only(self):
        module = load_main()
        with self.assertRaises(ValueError):
            module.validate("   \n\t  ")

    def test_validate_rejects_too_long(self):
        module = load_main()
        with self.assertRaises(ValueError):
            module.validate("x" * 1001)


class TestProgramRun(unittest.TestCase):
    def run_entry(self, out_dir):
        env = dict(os.environ)
        env["MAKEFUN_OUTPUT_DIR"] = out_dir
        proc = subprocess.run(
            [sys.executable, MAIN], env=env,
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return os.path.join(out_dir, "entry.txt")

    def test_writes_entry_txt(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.run_entry(tmp)
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertEqual(content, EXPECTED)

    def test_deterministic_across_runs(self):
        with tempfile.TemporaryDirectory() as tmp1, \
                tempfile.TemporaryDirectory() as tmp2:
            path1 = self.run_entry(tmp1)
            path2 = self.run_entry(tmp2)
            with open(path1, "rb") as a, open(path2, "rb") as b:
                self.assertEqual(a.read(), b.read())

    def test_creates_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            nested = os.path.join(tmp, "deep", "out")
            path = self.run_entry(nested)
            self.assertTrue(os.path.isfile(path))

    def test_output_is_valid_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.run_entry(tmp)
            with open(path, "rb") as handle:
                raw = handle.read()
            raw.decode("utf-8")
            self.assertEqual(len(raw.decode("utf-8")), 502)


class TestNoNetwork(unittest.TestCase):
    def test_no_network_imports(self):
        with open(MAIN, encoding="utf-8") as handle:
            source = handle.read()
        for banned in ("socket", "urllib", "requests", "http.client",
                       "subprocess", "os.system", "eval(", "exec("):
            self.assertNotIn(banned, source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
