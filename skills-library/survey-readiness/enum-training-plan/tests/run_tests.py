#!/usr/bin/env python3
"""Check the agenda checker. Usage (from this folder): python run_tests.py"""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
S = HERE.parent / "scripts" / "check_agenda.py"
fails = []


def run(*a):
    return subprocess.run([sys.executable, str(S), *map(str, a)], capture_output=True, text=True).stdout


def has(out, status, text):
    return any(l.startswith(status) and text in l for l in out.splitlines())


def ex(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"\n{detail}" if not ok else ""))
    if not ok:
        fails.append(name)


ok = run(HERE / "agenda-ok.md", "--days", "3", "--hours-per-day", "8")
ex("complete agenda has nothing missing", not any(l.startswith(("MISSING", "FAIL")) for l in ok.splitlines()), ok)
g = run(HERE / "agenda-gaps.md", "--days", "3", "--hours-per-day", "8")
for label, st, needle in (("missing final test found", "MISSING", "Element: final test"), ("missing selection found", "MISSING", "Element: enumerator selection"),
                          ("missing confidentiality found", "MISSING", "Element: confidentiality"), ("missing day 3 quiz found", "MISSING", "A quiz on each day after the first"),
                          ("overlong day found", "FAIL", "Day 2 length"), ("session with no lead found", "FAIL", "Every session has a lead")):
    ex(label, has(g, st, needle), g)
one = run(HERE / "agenda-ok.md", "--days", "2")
ex("wrong day count found", has(one, "FAIL", "Days in the agenda"))
print("\nAll tests passed." if not fails else f"\n{len(fails)} test(s) failed.")
sys.exit(1 if fails else 0)
