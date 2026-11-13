#!/usr/bin/env python3
"""Check an enumerator manual (Markdown) for required sections and for coverage of the questionnaire.

Usage: python check_manual.py manual.md [form.xlsx] [--lang English]

Checks: required sections present; every form module (group) is covered; how many questions are mentioned by name or
number; placeholders left ([TO CONFIRM: ...]). Results are candidates. A manual may describe several questions together.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from form_outline import outline

REQUIRED = [("Study purpose and objectives", r"purpose|objectives|study overview"), ("Roles and responsibilities", r"roles"),
            ("Survey protocols or field procedures", r"protocol|field procedure"), ("Using the tablet or device", r"tablet|device|surveycto|sync"),
            ("Description of the questions", r"question|form reference|field-by-field"), ("Key terms", r"key terms|glossary"),
            ("Frequently asked questions", r"faq|frequently asked"), ("Support and escalation", r"support|escalat|contact")]
PROTO = [("consent", r"consent"), ("respondent or unit selection", r"select|eligib|sample"), ("refusals or non-response", r"refus|non-?response|not available|absent"),
         ("replacement", r"replac|substitut"), ("revisits or call-backs", r"revisit|call-?back|re-?visit|follow-?up"), ("data upload and backup", r"upload|sync|backup|back up"),
         ("confidentiality", r"confidential|privacy|anonym")]


def main(path, form, lang):
    text = Path(path).read_text(encoding="utf-8")
    heads = [l.lstrip("# ").strip() for l in text.splitlines() if l.startswith("#")]
    out = []

    def add(s, c, d):
        out.append((s, c, d))
    for name, rx in REQUIRED:
        h = next((x for x in heads if re.search(rx, x, re.I)), None)
        add("ok" if h else "MISSING", f"Section: {name}", h or "no heading found")
    for name, rx in PROTO:
        add("ok" if re.search(rx, text, re.I) else "CHECK", f"Protocol topic: {name}", "mentioned" if re.search(rx, text, re.I) else "not mentioned. Ask the team whether it applies")
    ph = re.findall(r"\[TO CONFIRM[^\]]*\]", text)
    add("CHECK" if ph else "ok", "Items marked TO CONFIRM", f"{len(ph)} open item(s)" if ph else "none")
    left = re.findall(r"\[\[.+?\]\]", text)
    if left:
        add("FAIL", "Placeholders left", f"{len(left)} placeholder(s) in double brackets")
    if form:
        _, _, recs, nq, langs = outline(form, lang)
        low = text.lower()
        groups = [r for r in recs if r["kind"] == "group" and r["depth"] == 0]
        miss = [g["label"] for g in groups if g["label"].lower() not in low and g["name"].lower() not in low]
        add("MISSING" if miss else "ok", "Every form module is covered", f"not found: {'; '.join(miss[:5])}" if miss else f"{len(groups)} module(s) found")
        qs = [r for r in recs if r["kind"] == "question"]
        unc = [q for q in qs if q["name"].lower() not in low and not (q["number"] and re.search(r"(?<![\w.])" + re.escape(q["number"].lower()) + r"(?![\w.])", low))]
        pct = 100 * (len(qs) - len(unc)) / len(qs) if qs else 100
        add("ok" if not unc else "CHECK", "Questions mentioned by name or number", f"{len(qs) - len(unc)} of {len(qs)} ({pct:.0f}%)" + (f"; not mentioned: {', '.join(q['name'] for q in unc[:8])}" if unc else ""))
    bad = [o for o in out if o[0] != "ok"]
    print(f"# {Path(path).name}: {len(out)} checks, {len(bad)} to review")
    for s, c, d in out:
        print(f"{s:7} | {c} | {d}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    a = sys.argv
    form = a[2] if len(a) > 2 and not a[2].startswith("--") else None
    main(a[1], form, a[a.index("--lang") + 1] if "--lang" in a else None)
