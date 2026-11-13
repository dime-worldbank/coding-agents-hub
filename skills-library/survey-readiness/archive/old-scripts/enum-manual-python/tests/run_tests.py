#!/usr/bin/env python3
"""Check the manual checker and the outline tool. Usage (from this folder): python run_tests.py"""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
S = HERE.parent / "scripts"
fails = []


def run(script, *a):
    return subprocess.run([sys.executable, str(S / script), *map(str, a)], capture_output=True, text=True).stdout


def has(out, status, text):
    return any(l.startswith(status) and text in l for l in out.splitlines())


def ex(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"\n{detail}" if not ok else ""))
    if not ok:
        fails.append(name)


ok = run("check_manual.py", HERE / "manual-ok.md", HERE / "form.xlsx", "--lang", "English")
ex("complete manual has no missing sections or modules", not any(l.startswith(("MISSING", "FAIL")) for l in ok.splitlines()), ok)
ex("open TO CONFIRM items are listed", has(ok, "CHECK", "Items marked TO CONFIRM"))
g = run("check_manual.py", HERE / "manual-gaps.md", HERE / "form.xlsx", "--lang", "English")
ex("missing FAQ section found", has(g, "MISSING", "Frequently asked questions"))
ex("missing module found", has(g, "MISSING", "Every form module is covered") and "Module C Health" in g)
ex("uncovered questions listed", has(g, "CHECK", "Questions mentioned by name or number") and "hh_sex" in g)
ex("missing replacement protocol noted", has(g, "CHECK", "Protocol topic: replacement"))
o = run("form_outline.py", HERE / "form.xlsx", "--lang", "English", "--choices")
ex("outline lists the questions and options", "11 questions" in o and "options:" in o)
print("\nAll tests passed." if not fails else f"\n{len(fails)} test(s) failed.")
sys.exit(1 if fails else 0)
