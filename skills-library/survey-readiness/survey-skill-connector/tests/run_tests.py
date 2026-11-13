#!/usr/bin/env python3
"""Check brief.py. Usage (from this folder): python run_tests.py"""
import subprocess, sys, tempfile
from pathlib import Path

S = Path(__file__).parent.parent / "scripts" / "brief.py"
d = Path(tempfile.mkdtemp())
fails = []


def run(*a):
    return subprocess.run([sys.executable, str(S), *map(str, a)], capture_output=True, text=True)


def ex(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)


p = d / "project-brief.md"
run("init", p)
ex("blank brief is created", p.exists() and "survey_name:" in p.read_text())
ex("a second init does not overwrite", run("init", p).returncode != 0)
r = run("check", p).stdout
ex("empty fields are listed", r.count("EMPTY") == 18)
p.write_text("# Project brief\nsurvey_name: Test\ncountry: Zambia\nsurvey_type: school\nmode: tablet\ndata_collection_start: 2027-03-01\ndata_collection_end: 2027-02-01\n"
             "sample_size: call 0977123456\nplatform: surveycto\nexecuted_by: moon\nextra_field: x\n")
r = run("check", p).stdout
ex("invalid value found", "INVALID  | executed_by" in r)
ex("end before start found", "end date" not in r and "is before the start" in r)
ex("phone number flagged", "PRIVACY  | sample_size" in r)
ex("unknown field flagged", "UNKNOWN  | extra_field" in r)
ex("show prints only filled fields", run("show", p).stdout.count("\n") == 9)
print("\nAll tests passed." if not fails else f"\n{len(fails)} test(s) failed.")
sys.exit(1 if fails else 0)
