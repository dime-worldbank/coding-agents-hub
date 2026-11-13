#!/usr/bin/env python3
"""Check build_timeline.py against the sample plan. Usage (from this folder): python run_tests.py"""
import json, subprocess, sys, tempfile
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).parent
S = HERE.parent / "scripts" / "build_timeline.py"
plan = json.load(open(HERE / "sample-plan.json"))
fails = []


def run(*a):
    return subprocess.run([sys.executable, str(S), *a], capture_output=True, text=True).stdout


def ex(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if not ok else ""))
    if not ok:
        fails.append(name)


def rows(out):
    r = {}
    for l in out.splitlines():
        if l.startswith("| S"):
            p = [x.strip() for x in l.strip().strip("|").split(" | ")]
            r[p[0]] = {"start": date.fromisoformat(p[4]), "end": date.fromisoformat(p[5]), "notes": p[6] if len(p) > 6 else ""}
    return r


steps = {s["id"]: s for s in plan["steps"]}
b = rows(run(str(HERE / "sample-plan.json"), "--mode", "backward", "--today", "2026-11-16"))
ex("anchor starts on the target date", b["S19"]["start"] == date(2027, 3, 1))
ex("no step ends after a successor starts", all(b[p]["end"] <= b[s["id"]]["start"] for s in plan["steps"] for p in s["after"]))
ex("durations match the plan", all((b[i]["end"] - b[i]["start"]).days == steps[i]["weeks"] * 7 for i in steps if i != "S19"))
ex("fieldwork overlap with school holidays is flagged", "overlaps School holidays" in b["S19"]["notes"])
tight = run(str(HERE / "sample-plan.json"), "--mode", "backward", "--today", "2027-01-15")
ex("shortfall reported when today is too late", "does not fit" in tight)
late = rows(run(str(HERE / "sample-plan.json"), "--mode", "backward", "--today", "2027-01-15"))
ex("steps that start before today are flagged", any("before today" in v["notes"] for v in late.values()))
f = run(str(HERE / "sample-plan.json"), "--mode", "forward", "--today", "2026-11-16")
fr = rows(f)
longest = {}
for s in plan["steps"]:
    longest[s["id"]] = max([longest[p] for p in s["after"]] + [0]) + s["weeks"]
ex("forward plan gives the longest chain as the earliest start",
   fr["S19"]["start"] == date(2026, 11, 16) + timedelta(weeks=longest["S19"]), f"{fr['S19']['start']} vs chain {longest['S19']} weeks")
ex("forward plan reports days too late against the target", "too late" in f or "slack" in f)
x = Path(tempfile.mkdtemp()) / "s.md"
run(str(HERE / "sample-plan.json"), "--md", str(x), "--today", "2026-11-16")
ex("Markdown schedule written as a table", x.exists() and x.read_text().startswith("| ID | Step") and x.read_text().count("\n") == 13)
bad = dict(plan); bad["steps"] = plan["steps"] + [{"id": "S20", "name": "x", "after": ["S99"]}]
p = Path(tempfile.mkdtemp()) / "bad.json"; json.dump(bad, open(p, "w"))
r = subprocess.run([sys.executable, str(S), str(p)], capture_output=True, text=True)
ex("unknown predecessor is reported", r.returncode != 0 and "unknown step" in (r.stderr + r.stdout))
print("\nAll tests passed." if not fails else f"\n{len(fails)} test(s) failed.")
sys.exit(1 if fails else 0)
