#!/usr/bin/env python3
"""Count the words each skill loads, to keep token use low.

Usage: python tools/check_budget.py [repo folder]

Budgets (suggestions, not standards): description 90 words or fewer; SKILL.md 800 words or fewer; each reference file
1,500 words or fewer, or a table of contents. A typical run loads one description per installed skill, the SKILL.md of the
skill used, and one or two references. Scripts and assets cost nothing until read.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
LIM = {"desc": 90, "skill": 800, "ref": 1500}
bad = 0
print(f"{'skill':26} {'desc':>5} {'SKILL.md':>9} {'largest reference':>26}")
for sk in sorted(p for p in root.iterdir() if (p / "SKILL.md").exists()):
    t = (sk / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r'description:\s*"(.*?)"\n', t, re.S)
    dw = len(m.group(1).split()) if m else 0
    sw = len(t.split())
    refs = sorted(((len(f.read_text(encoding="utf-8").split()), f.name) for f in (sk / "references").glob("*.md")), reverse=True) if (sk / "references").exists() else []
    big = refs[0] if refs else (0, "-")
    flag = [x for x, v, k in (("description", dw, "desc"), ("SKILL.md", sw, "skill"), (big[1], big[0], "ref")) if v > LIM[k]]
    bad += bool(flag)
    print(f"{sk.name:26} {dw:5} {sw:9} {big[0]:>8} {big[1]:<17}" + (f"  OVER: {', '.join(flag)}" if flag else ""))
print("\nAll within budget." if not bad else f"\n{bad} skill(s) over a suggested budget.")
