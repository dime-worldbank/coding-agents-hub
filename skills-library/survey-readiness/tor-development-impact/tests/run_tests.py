#!/usr/bin/env python3
"""Check the TOR checker and the Markdown to Word converter. Usage (from this folder): python run_tests.py"""
import subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).parent
S = HERE.parent / "scripts"
fails = []


def run(*a):
    return subprocess.run([sys.executable if str(a[0]).endswith(".py") else "node", *map(str, a)], capture_output=True, text=True)


def expect(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if not ok and detail else ""))
    if not ok:
        fails.append(name)


run(HERE / "build_test_tors.py")
ok = run(S / "check_tor.py", HERE / "tor-filled-ok.md").stdout
bad_ok = [l for l in ok.splitlines()[1:] if not l.startswith("ok")]
expect("filled TOR passes all checks except figures to reconcile", all("Percentages to reconcile" in l or "Deliverables dated before" in l for l in bad_ok), "\n".join(bad_ok))
br = run(S / "check_tor.py", HERE / "tor-broken.md").stdout
for label, needle in (("missing ethics section found", "MISSING | Section: Ethical provisions |"), ("payment total found", "Payment shares add to 100 | shares"),
                      ("activity without deliverable found", "Every activity has a deliverable | no deliverable row for activity [5]"),
                      ("selection weight mismatch found", "Selection weights add up"), ("late deliverable found", "Last deliverable is inside the work period"),
                      ("contract end before completion found", "Contract end is not before completion"), ("stray placeholder found", "Placeholders left")):
    line = next((l for l in br.splitlines() if needle in l), "")
    expect(label, bool(line) and not line.startswith("ok"), line)
expect("payment total is 95", "add to 95" in br)
d = Path(tempfile.mkdtemp())
t = d / "out.docx"
r = subprocess.run(["node", str(S / "md_to_docx.js"), str(HERE / "tor-filled-ok.md"), str(t)], capture_output=True, text=True,
                   env={**__import__("os").environ, "NODE_PATH": subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()})
expect("Markdown converts to Word", t.exists() and t.stat().st_size > 5000, r.stderr[-200:])
if t.exists():
    back = d / "back.md"
    subprocess.run(f"extract-text {t} > {back}", shell=True)
    again = run(S / "check_tor.py", back).stdout
    bad = [l for l in again.splitlines()[1:] if not l.startswith("ok") and "Percentages" not in l and "dated before" not in l]
    expect("Word file converted back to Markdown passes the same checks", not bad, "\n".join(bad))
word = run(S / "check_tor.py", t)
expect("a Word file is refused with a conversion hint", "Markdown only" in (word.stdout + word.stderr) or word.returncode != 0)
print("\nAll tests passed." if not fails else f"\n{len(fails)} test(s) failed.")
sys.exit(1 if fails else 0)
