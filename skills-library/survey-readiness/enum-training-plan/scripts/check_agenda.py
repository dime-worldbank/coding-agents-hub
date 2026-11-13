#!/usr/bin/env python3
"""Check a training agenda (Markdown table) for the elements a Development Impact enumerator training should include.

Usage: python check_agenda.py agenda.md [--days N] [--hours-per-day H] [--one-day-ok]

Table columns: Day | Time | Session | Objective | Method | Materials | Lead. Time looks like 08:30-09:15.
Checks: days match; daily hours within limit; a break on long days; every session has a lead; and the presence of
protocols, questionnaire, tablet use, practice, confidentiality, quizzes (day 2 onward), a final test, field practice
with feedback, and selection. Results are candidates. Judge them in context.
"""
import re
import sys
from collections import defaultdict


def minutes(t):
    m = re.match(r"\s*(\d{1,2}):(\d{2})\s*[-\u2013\u2014to]+\s*(\d{1,2}):(\d{2})", t or "")
    return (int(m.group(3)) * 60 + int(m.group(4))) - (int(m.group(1)) * 60 + int(m.group(2))) if m else None


ELEMENTS = [("survey protocols", r"protocol"), ("questionnaire content", r"questionnaire|module"), ("tablet or device use", r"tablet|device|surveycto|paper form"),
            ("confidentiality", r"confidential|anonymity|privacy"), ("classroom practice", r"classroom|mock|role.?play|team exercise|practice"),
            ("field practice", r"field practice|practice interview|pilot interview"), ("feedback on practice", r"feedback|debrief"),
            ("final test", r"final test|final assessment"), ("enumerator selection", r"selection|certif"), ("roles and responsibilities", r"roles|responsibilit")]


def main(path, days, hpd, one_day_ok):
    rows, hdr = [], None
    for l in open(path, encoding="utf-8"):
        if not l.startswith("|") or re.match(r"^\|\s*-{2,}", l):
            continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if hdr is None and "session" in [x.lower() for x in c]:
            hdr = [x.lower() for x in c]
        elif hdr:
            rows.append(dict(zip(hdr, c)))
    if not rows:
        sys.exit("No agenda table found. Expected columns: Day | Time | Session | Objective | Method | Materials | Lead")
    out = []

    def add(s, c, d):
        out.append((s, c, d))
    byday = defaultdict(list)
    for r in rows:
        byday[r.get("day", "")].append(r)
    nd = len(byday)
    if days:
        add("ok" if nd == days else "FAIL", "Days in the agenda", f"{nd} day(s) in the table; {days} stated")
    for day, rs in byday.items():
        tot = sum(minutes(r.get("time", "")) or 0 for r in rs)
        brk = any(re.search(r"break|lunch|rest|meal", r.get("session", ""), re.I) for r in rs)
        if hpd and tot > hpd * 60:
            add("FAIL", f"Day {day} length", f"{tot / 60:.1f} hours of sessions; limit {hpd}")
        if tot > 240 and not brk:
            add("CHECK", f"Day {day} breaks", f"{tot / 60:.1f} hours with no break or lunch row")
    nolead = [r.get("session", "")[:40] for r in rows if not r.get("lead") and not re.search(r"break|lunch|rest", r.get("session", ""), re.I)]
    add("FAIL" if nolead else "ok", "Every session has a lead", f"no lead for: {'; '.join(nolead[:4])}" if nolead else "yes")
    text = {k: " ".join(r.get("session", "") + " " + r.get("objective", "") for r in v) for k, v in byday.items()}
    alltext = " ".join(text.values())
    for name, rx in ELEMENTS:
        have = re.search(rx, alltext, re.I)
        add("ok" if have else ("CHECK" if nd == 1 and one_day_ok else "MISSING"), f"Element: {name}", "present" if have else "not found in the agenda")
    quiz_days = [k for k, t in text.items() if re.search(r"quiz", t, re.I)]
    order = list(byday)
    need = order[1:]
    miss = [d for d in need if d not in quiz_days]
    if nd > 1:
        add("MISSING" if miss else "ok", "A quiz on each day after the first", f"no quiz on day(s) {miss}" if miss else "yes")
    else:
        add("CHECK" if one_day_ok else "MISSING", "Quizzes", "one-day agenda: confirm how understanding is tested")
    last = text[order[-1]] if order else ""
    add("ok" if re.search(r"final test|final assessment", last, re.I) or nd == 1 else "CHECK", "Final test on the last training day", "found" if re.search(r"final test|final assessment", last, re.I) else "not on the last day")
    add("ok" if re.search(r"rest", alltext, re.I) or nd == 1 else "CHECK", "Rest time between days or sessions", "found" if re.search(r"rest", alltext, re.I) else "not stated")
    bad = [o for o in out if o[0] != "ok"]
    print(f"# {path}: {len(out)} checks, {len(bad)} to review")
    for s, c, d in out:
        print(f"{s:7} | {c} | {d}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    a = sys.argv
    get = lambda k: float(a[a.index(k) + 1]) if k in a else None
    main(a[1], int(get("--days")) if get("--days") else None, get("--hours-per-day"), "--one-day-ok" in a)
