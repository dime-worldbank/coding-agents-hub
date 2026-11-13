#!/usr/bin/env python3
"""Run the skill's checks on the invented test files and compare with the expected results.
Usage (from this folder): python run_tests.py   Needs openpyxl, python-docx, pdfplumber."""
import json, subprocess, sys, tempfile
from pathlib import Path
from openpyxl import load_workbook

HERE = Path(__file__).parent
S = HERE.parent / "scripts"
tmp = Path(tempfile.mkdtemp())
fails = []


def run(*a):
    return subprocess.run([sys.executable, *map(str, a)], capture_output=True, text=True)


def checks(xlsx):
    ws = load_workbook(xlsx)["Discrepancies"]
    return sorted(r[1] for r in ws.iter_rows(min_row=2, values_only=True))


def expect(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if not ok else ""))
    if not ok:
        fails.append(name)


RESP = sorted(["Paper text block differs from form note", "Choices differ", "On paper, not in form", "Type differs", "Choices differ",
               "Wording differs: possible change in meaning", "Choice codes differ", "Order differs", "Question number differs",
               "Minor wording difference", "In form, not on paper"])
for ext in ("docx", "xlsx", "pdf"):
    run(S / "extract_paper.py", HERE / f"paper-questionnaire.{ext}", "--out", tmp / f"i_{ext}.json")
    out = tmp / f"d_{ext}.xlsx"
    r = run(S / "compare_forms.py", tmp / f"i_{ext}.json", HERE / "programmed-form.xlsx", "--out", out)
    got = checks(out)
    want = [c for c in RESP if not (ext == "xlsx" and c.startswith("Paper text block"))]
    expect(f"respondent-style paper ({ext}): planted differences found", got == sorted(want), f"got {got}")

SPEC = sorted(["Constraint differs", "Choices differ", "Skip logic differs", "Wording differs: possible change in meaning", "On paper, not in form",
               "Required differs", "Order differs", "In form, not on paper", "Variable name differs", "Choice codes differ", "Type differs",
               "Calculation differs", "Preload file differs"])
run(S / "extract_paper.py", HERE / "spec-paper.docx", "--out", tmp / "spec.json")
r = run(S / "compare_forms.py", tmp / "spec.json", HERE / "spec-form.xlsx", "--calcs", "--out", tmp / "spec.xlsx")
expect("specification-style paper: planted differences found", checks(tmp / "spec.xlsx") == SPEC, f"got {checks(tmp / 'spec.xlsx')}")
expect("shared language chosen without asking", "Using the language both files share" in r.stdout)
d = json.load(open(tmp / "spec.json")); d["language_guess"] = {"guess": "unknown"}; json.dump(d, open(tmp / "unk.json", "w"))
r = run(S / "compare_forms.py", tmp / "unk.json", HERE / "spec-form.xlsx", "--out", tmp / "x.xlsx")
expect("asks the team when the shared language is unclear", r.returncode == 3 and "ASK THE TEAM" in r.stdout)

r = run(S / "inspect_xlsform.py", HERE / "planted-errors-form.xlsx", "--full")
ids = {l.split(" | ")[0] for l in r.stdout.splitlines() if " | " in l}
need = {"LIST-001", "LOGIC-001", "VALID-005", "LIST-002", "LOGIC-002", "LOGIC-005", "NAME-001", "LANG-001", "META-001", "META-004",
        "META-006", "STATA-001", "SYNTAX-001", "VALID-003", "VALID-004"}
expect("form review finds the planted errors", need <= ids, f"missing {sorted(need - ids)}")
expect("Style Guide checks are off by default", not ({"CODE-001", "STYLE-002"} & ids) and "Style Guide checks not run" in r.stdout)
r2 = run(S / "inspect_xlsform.py", HERE / "planted-errors-form.xlsx", "--full", "--style-guide")
expect("Style Guide checks run with --style-guide", "CODE-001" in r2.stdout and "STYLE-002" in r2.stdout)

from openpyxl import Workbook
wb = Workbook(); ws = wb.active; ws.title = "survey"
ws.append(["type", "name", "label::English", "required"])
for row in (["begin group", "this_group_name_is_definitely_longer_than_thirty_two", "M", ""], ["text", "a", "5.4 One", "yes"],
            ["text", "b", "5.4 Two", "yes"], ["end group", "this_group_name_is_definitely_longer_than_thirty_two", "", ""]):
    ws.append(row)
wb.create_sheet("choices").append(["list_name", "name", "label::English"]); wb.create_sheet("settings").append(["form_title", "form_id", "version"])
wb.save(tmp / "names.xlsx")
r = run(S / "inspect_xlsform.py", tmp / "names.xlsx", "--full")
expect("long group names flagged", "NAME-003" in r.stdout and "Group is" in r.stdout)
expect("duplicate question numbers flagged", "NUM-001" in r.stdout)
r = run(S / "form_outline.py", HERE / "spec-form.xlsx", "--lang", "English", "--choices")
expect("form outline lists 11 questions", "11 questions" in r.stdout)
print("\nAll tests passed." if not fails else f"\n{len(fails)} test(s) failed.")
sys.exit(1 if fails else 0)
