#!/usr/bin/env python3
"""Mechanical consistency checks for a survey firm TOR written in the template's structure.

Usage: python check_tor.py tor.md [--recipient-executed] [--json]

Reads Markdown text only. For a Word TOR, convert it to Markdown first (markitdown, extract-text, or pandoc).

Checks: placeholders left, required sections, activity numbering across duties, deliverables and payment,
payment shares and selection weights adding to 100, deliverable dates against the contract period, percentages
to reconcile, and required clauses. Results are candidates: confirm them in context. Reads the file only.
"""
import re
import sys
import json
from datetime import date
from pathlib import Path

MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
SECTIONS = [("Background", r"background"), ("Scope of work", r"scope of work"), ("Duties and responsibilities", r"duties"),
            ("Deliverables and timeline", r"deliverables and timeline"), ("Data deliverables", r"data deliverables"),
            ("Qualifications", r"qualifications"), ("Confidentiality, ownership, re-use", r"confidential"),
            ("Ethical provisions", r"^\W*\d*\.?\s*ethical provisions"), ("Budget, contract, payment", r"budget|payment schedule"),
            ("Selection criteria", r"selection criteria"), ("Downstream work", r"downstream"),
            ("Ethical provisions annex", r"annex.*ethical")]
CLAUSES = [("ownership by the commissioning institution", r"property of the world bank", "bank"),
           ("data security standards", r"data security standards", ""), ("informed consent required", r"informed consent", ""),
           ("review board compliance", r"institutional review board|\birb\b", ""), ("recruit more trainees than needed", r"more interviewers|recruit more|more .* than will", ""),
           ("reserve enumerators", r"reserve", ""), ("spot checks or back-checks", r"spot.?check|back.?check", ""),
           ("daily upload and backup", r"submitted to the server daily|daily", ""), ("weekly reports", r"weekly report", ""),
           ("remedy for integrity failure", r"repetition of the work|not paying|integrity", ""),
           ("no third-party use without written approval", r"third part", "")]


def load(path):
    p = Path(path)
    if p.suffix.lower() not in (".md", ".txt", ".markdown"):
        sys.exit("check_tor.py reads Markdown only. Convert the file first: markitdown tor.docx -o tor.md (or extract-text, or pandoc -t gfm).")
    return p.read_text(encoding="utf-8")


SECTION = re.compile(r"^#{1,3}\s*(\d+\.\s|ANNEX|Annex)")


def split_sections(text):
    secs, cur = {}, "(front)"
    for l in text.splitlines():
        if SECTION.match(l) or re.match(r"^ANNEX", l):
            cur = l.lstrip("# ").strip()
            secs[cur] = []
        else:
            secs.setdefault(cur, []).append(l)
    return secs


def find(secs, rx):
    for k, v in secs.items():
        if re.search(rx, k, re.I):
            return k, v
    return None, []


def rows(lines):
    out = []
    for l in lines:
        if l.startswith("|") and not re.match(r"^\|\s*-{2,}", l):
            out.append([c.strip() for c in l.strip().strip("|").split(" | ")])
    return out


def num(s):
    m = re.search(r"\d+(?:\.\d+)?", re.sub(r"[\*\[\]]", "", s or ""))
    return float(m.group()) if m else None


def pdate(s):
    s = s.replace(",", " ")
    m = re.search(r"([A-Za-z]{3})[a-z]*\s+(\d{1,2})\s+(\d{4})", s)
    if m and m.group(1).lower() in MONTHS:
        return date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2)))
    m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})[a-z]*\s+(\d{4})", s)
    if m and m.group(2).lower() in MONTHS:
        return date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1)))
    return None


def pmonth(s):
    m = re.search(r"([A-Za-z]{3})[a-z]*\s+(\d{4})", s or "")
    return (int(m.group(2)), MONTHS[m.group(1).lower()]) if m and m.group(1).lower() in MONTHS else None


def expand(a, b):
    return set(range(int(a), int(b or a) + 1))


def main(path, recipient, as_json):
    text = load(path)
    secs = split_sections(text)
    res = []

    def add(check, status, detail):
        res.append({"check": check, "status": status, "detail": detail})

    ph = re.findall(r"\[\[(.+?)\]\]", text)
    add("Placeholders left", "FAIL" if ph else "ok", f"{len(ph)} placeholder(s) still in brackets, e.g. " + "; ".join(p[:40] for p in ph[:4]) if ph else "none")
    notes = len(re.findall(r"drafting note", text, re.I))
    if notes:
        add("Drafting notes left", "FAIL", f"{notes} drafting note(s) still present")
    for name, rx in SECTIONS:
        k, _ = find(secs, rx)
        add(f"Section: {name}", "ok" if k else "MISSING", k or "no heading found")
    # activities
    _, duties = find(secs, r"duties")
    acts = {int(m.group(1)) for l in duties for m in [re.match(r"^\W*Activity\s+(\d+)\s*[:.]", l)] if m}
    _, deliv = find(secs, r"deliverables and timeline")
    drows = rows(deliv)
    d_acts, dates, cur = set(), [], None
    for r in drows[1:]:
        n = num(r[0]) if r and r[0].strip() else None
        if n is not None:
            cur = int(n)
            d_acts.add(cur)
        d = pdate(r[-1]) if r else None
        if d:
            dates.append(d)
    _, bud = find(secs, r"budget|payment schedule")
    pay_total, covered, items = 0.0, set(), []
    for l in bud:
        if (l.startswith("|") or l.lstrip().startswith("-")) and "%" in l and not re.search(r"total", l, re.I) and not re.search(r"^\|\s*-{2,}", l):
            cells = [c.strip() for c in l.strip().strip("|").split(" | ")] if l.startswith("|") else [l]
            share = num(cells[-1]) if l.startswith("|") else num(re.search(r"\d+\s*%", l).group() if re.search(r"\d+\s*%", l) else "")
            if share is None:
                continue
            pay_total += share
            items.append(share)
            for m in re.finditer(r"Activit(?:y|ies)\s+(\d+)(?:\s*(?:\u2013|-|to)\s*(\d+))?", l):
                covered |= expand(m.group(1), m.group(2))
    add("Activities in duties", "ok" if acts else "FAIL", f"Activities {sorted(acts)}" if acts else "none found")
    miss_d = sorted(acts - d_acts)
    extra_d = sorted(d_acts - acts)
    add("Every activity has a deliverable", "FAIL" if miss_d else "ok", f"no deliverable row for activity {miss_d}" if miss_d else "yes")
    if extra_d:
        add("Deliverables for unknown activities", "FAIL", f"deliverables table has activity {extra_d} not in the duties")
    miss_p = sorted(acts - covered)
    add("Every activity is covered by a payment milestone", "FAIL" if miss_p else "ok", f"no milestone covers activity {miss_p}" if miss_p else "yes")
    if items:
        add("Payment shares add to 100", "ok" if abs(pay_total - 100) < 0.01 else "FAIL", f"shares {items} add to {pay_total:g}")
    else:
        add("Payment shares add to 100", "FAIL", "no payment shares found")
    # selection weights
    _, sel = find(secs, r"selection criteria")
    srows = rows(sel)
    groups, cur_sum, sub_ok, total = [], 0.0, True, None
    detail = []
    for r in srows[1:]:
        if len(r) < 4:
            continue
        label, w = re.sub(r"[\*]", "", r[1] + " " + r[2]).strip().lower(), num(r[3])
        if "sub" in label and "total" in label:
            ok = w is not None and abs(w - cur_sum) < 0.01
            sub_ok &= ok
            if not ok:
                detail.append(f"subtotal {w:g} but sub-criteria add to {cur_sum:g}" if w is not None else "subtotal missing")
            groups.append(cur_sum)
            cur_sum = 0.0
        elif label.startswith("total") or label == "total":
            total = w
        elif re.match(r"\d+\.\d+", r[2].strip()) and w is not None:
            cur_sum += w
    gsum = sum(groups)
    add("Selection weights add up", "ok" if sub_ok and total is not None and abs(gsum - 100) < 0.01 and abs(total - 100) < 0.01 else "FAIL",
        "; ".join(detail + ([f"criteria add to {gsum:g}"] if abs(gsum - 100) >= 0.01 else []) + ([f"stated total {total:g}"] if total is not None and abs(total - 100) >= 0.01 else [])) or "sub-criteria, subtotals and total agree")
    # dates
    bt = " ".join(bud)
    sm = pmonth(re.search(r"start work in ([^.,]+)", bt, re.I).group(1)) if re.search(r"start work in ([^.,]+)", bt, re.I) else None
    cm = pmonth(re.search(r"complete the work by ([^.,]+)", bt, re.I).group(1)) if re.search(r"complete the work by ([^.,]+)", bt, re.I) else None
    em = pmonth(re.search(r"contract will end in ([^.,]+)", bt, re.I).group(1)) if re.search(r"contract will end in ([^.,]+)", bt, re.I) else None
    if dates and cm:
        last = max(dates)
        add("Last deliverable is inside the work period", "ok" if (last.year, last.month) <= cm else "FAIL", f"last deliverable {last}; work ends {cm[0]}-{cm[1]:02d}")
    if cm and em:
        add("Contract end is not before completion", "ok" if em >= cm else "FAIL", f"completion {cm[0]}-{cm[1]:02d}, contract end {em[0]}-{em[1]:02d}")
    if dates and sm and min(dates) and (min(dates).year, min(dates).month) < sm:
        add("Deliverables dated before the start of work", "CHECK", f"earliest deliverable {min(dates)}; work starts {sm[0]}-{sm[1]:02d}. Fine for permits and plans if intended")
    if not dates:
        add("Deliverable dates", "CHECK", "no dates found in the deliverables table")
    # percentages to reconcile
    figs = []
    for name, rx in (("Duties", r"duties"), ("Data quality", r"data deliverables"), ("Payment", r"budget|payment schedule")):
        _, ls = find(secs, rx)
        for l in ls:
            for m in re.finditer(r"(\d+(?:\s*(?:\u2013|-|to)\s*\d+)?)\s*(?:percent|%)", re.sub(r"[\[\]]", "", l)):
                ctx = re.sub(r"\s+", " ", l[max(0, m.start() - 50):m.end() + 40]).strip()
                if "payment" not in name.lower() or not (l.startswith("|") or l.lstrip().startswith("-")):
                    figs.append(f"{name}: {m.group(1)} percent ... {ctx[:90]}")
    add("Percentages to reconcile", "CHECK" if figs else "ok", " || ".join(figs[:8]) if figs else "none")
    low = text.lower()
    for label, rx, only in CLAUSES:
        if only == "bank" and recipient:
            continue
        add(f"Clause: {label}", "ok" if re.search(rx, low) else "MISSING", "present" if re.search(rx, low) else "no matching text found")
    if as_json:
        print(json.dumps(res, indent=1))
        return
    bad = [r for r in res if r["status"] != "ok"]
    print(f"# {Path(path).name}: {len(res)} checks, {len(bad)} to review")
    for r in res:
        print(f"{r['status']:7} | {r['check']} | {r['detail']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], "--recipient-executed" in sys.argv, "--json" in sys.argv)
