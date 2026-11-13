#!/usr/bin/env python3
"""Print a compact outline of an XLSForm so a form can be read without loading the whole workbook.

Usage: python form_outline.py form.xlsx [--lang English] [--choices] [--calcs]

One line per question: row | number | name | type | label | relevant | constraint | required.
Groups print as "== group: label (name) | relevant: ...". With --choices, option lists print under each select
question. Calculate and metadata fields are skipped unless --calcs. Reads the file only; never changes it.
"""
import re
import sys
from openpyxl import load_workbook

META = {"start", "end", "today", "deviceid", "subscriberid", "simserial", "phonenumber", "username", "audit", "text audit",
        "speed violations list", "speed violations count", "caseid", "comments", "email", "hidden"}


def hn(h):
    h = str(h or "").strip()
    if "::" in h:
        a, b = h.split("::", 1)
        return a.strip().lower().replace(" ", "_") + "::" + b.strip().lower()
    return h.lower().replace(" ", "_")


def outline(path, lang=None, choices=False, calcs=False):
    wb = load_workbook(path, data_only=True, read_only=True)
    rows = [[("" if v is None else str(v).strip()) for v in r] for r in wb["survey"].iter_rows(values_only=True)]
    hdr = [hn(h) for h in rows[0]]
    langs = sorted({h.split("::", 1)[1] for h in hdr if h.startswith("label::") and h.split("::", 1)[1] != "stata"})
    pick = lambda p: next((hdr.index(w) for w in ((f"{p}::{lang.lower()}" if lang else None), p) if w and w in hdr),
                          next((i for i, h in enumerate(hdr) if h.startswith(p + "::") and "stata" not in h), None))
    ci = {k: pick(k) for k in ("label", "constraint_message")}
    get = lambda r, k: (r[hdr.index(k)] if k in hdr and hdr.index(k) < len(r) else "")
    lab = lambda r: r[ci["label"]] if ci["label"] is not None and ci["label"] < len(r) else ""
    lists = {}
    if choices and "choices" in wb.sheetnames:
        cr = [[("" if v is None else str(v).strip()) for v in r] for r in wb["choices"].iter_rows(values_only=True)]
        ch = [hn(h) for h in cr[0]]
        li = ch.index("list_name")
        vi = ch.index("value") if "value" in ch else ch.index("name")
        la = next((ch.index(w) for w in ((f"label::{lang.lower()}" if lang else None), "label") if w and w in ch),
                  next((i for i, h in enumerate(ch) if h.startswith("label::") and "stata" not in h), None))
        for r in cr[1:]:
            if r[li]:
                lists.setdefault(r[li], []).append(f"{r[vi]}={r[la] if la is not None else ''}")
    out, nq, depth, recs = [], 0, 0, []
    for n, r in enumerate(rows[1:], start=2):
        if not any(r):
            continue
        t, name = get(r, "type"), get(r, "name")
        parts = t.replace("_", " ").split()
        b = " ".join(parts[:2]) if parts and parts[0] in ("begin", "end", "select") and len(parts) > 1 else (parts[0] if parts else "")
        rel = get(r, "relevance") or get(r, "relevant")
        if b in ("begin group", "begin repeat"):
            out.append(f"{'  ' * depth}== {b.split()[1]}: {lab(r) or name} ({name}) | row {n}" + (f" | relevant: {rel}" if rel else ""))
            recs.append({"kind": "group", "depth": depth, "row": n, "name": name, "label": lab(r) or name, "rel": rel})
            depth += 1
            continue
        if b in ("end group", "end repeat"):
            depth = max(0, depth - 1)
            continue
        if b.startswith("calculate"):
            if calcs:
                out.append(f"{'  ' * depth}{n} | calc | {name} | {get(r, 'calculation')[:90]}" + (f" | relevant: {rel}" if rel else ""))
            continue
        if b in META or b.startswith(("sensor", "speed")) or not name:
            continue
        if b != "note":
            nq += 1
        num = get(r, "question_number") or (re.match(r"^\s*((?:[A-Za-z]{1,3})?\d+(?:\.\d+)*[a-z]?)\b", lab(r)) or [0, ""])[1]
        cm = get(r, "constraint")
        out.append(f"{'  ' * depth}{n} | {num} | {name} | {t[:38]} | {lab(r)[:140]} | {rel} | {cm} | {'req' if get(r, 'required').lower() in ('yes', 'true', '1') else ''}")
        recs.append({"kind": "note" if b == "note" else "question", "depth": depth, "row": n, "number": num, "name": name, "type": t, "label": lab(r), "rel": rel, "constraint": cm})
        if choices and b.startswith("select") and len(t.split()) > 1 and t.split()[1] in lists:
            out.append(f"{'  ' * (depth + 1)}options: " + "; ".join(lists[t.split()[1]])[:300])
    head = [f"# {path.split('/')[-1]}: {nq} questions; languages {langs or ['(single)']}; label language used: {lang or 'first available'}",
            "# row | number | name | type | label | relevant | constraint | required"]
    return head, out, recs, nq, langs


def main(path, lang, choices, calcs):
    head, out, _, _, _ = outline(path, lang, choices, calcs)
    print("\n".join(head + out))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    a = sys.argv
    main(a[1], a[a.index("--lang") + 1] if "--lang" in a else None, "--choices" in a, "--calcs" in a)
