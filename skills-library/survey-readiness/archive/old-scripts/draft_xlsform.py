#!/usr/bin/env python3
"""Draft an XLSForm from a paper questionnaire (items.json from extract_paper.py).

Usage: python draft_xlsform.py items.json --out draft.xlsx [--template xlsform-template.xlsx]
                               [--prefixes "Module 2=hh,Module 3=farm"] [--lang English] [--development impact]

--development impact applies Development Impact / World Bank conventions: Don't know, Refused and Other coded -99, -88
and -9, and an empty label:stata column. Without it, paper codes are kept (see
references/development impact-conventions.md).

Writes a DRAFT. Question types are guesses from wording and options. Consent text,
constraints, skip logic, encryption key, and Stata labels are left for the team: see
the "todo" sheet. Syntax authority is the SurveyCTO skill; if its template is given
(--template), its worksheets and formatting are kept and only rows are filled in.
"""
import re
import sys
import json
from pathlib import Path
from openpyxl import load_workbook, Workbook

SPECIAL = [(r"^(don'?t know|dk|do not know|not sure)\b", "-99"), (r"^(refus\w*|no answer)\b", "-88"),
           (r"^other\b", "-9")]


def slug(s, n=24):
    s = re.sub(r"\$\{[^}]+\}", "", s.lower())
    words = [w for w in re.findall(r"[a-z0-9]+", s) if w not in {"the", "a", "an", "of", "you", "your", "do", "did", "does", "is", "are", "what", "how", "which", "have", "in", "to", "for", "and", "or", "many", "much"}]
    return "_".join(words[:3])[:n] or "q"


def guess_type(q):
    t, ch, rt = q["text"].lower(), q["choices"], (q["response_type"] or "")
    if ch:
        multi = re.search(r"select all|all that apply|multiple answers|more than one", t + " " + q["notes"].lower())
        return ("select_multiple" if multi else "select_one"), "choice"
    if rt in ("date",) or re.search(r"\bdate\b|\bwhen did\b", t): return "date", "date"
    if rt in ("numeric", "number", "integer", "decimal") or re.search(r"\bhow many\b|\bnumber of\b|\bage\b|\bhow old\b|\bhow often.*times\b", t):
        return ("decimal" if re.search(r"hectare|acre|kg|amount|price|cost|income|area|size|litre|liter|percent", t) else "integer"), "number"
    if "gps" in rt or "gps" in t: return "geopoint", "gps"
    return "text", "text"


def special_code(label, development impact=False):
    if not development impact:
        return None
    for pat, code in SPECIAL:
        if re.search(pat, label.strip().lower()):
            return code
    return None


def build(items_path, out, template, prefixes, lang, development impact=False):
    data = json.loads(Path(items_path).read_text())
    qs = [i for i in data["items"] if i["kind"] == "question"]
    scripts = [i for i in data["items"] if i["kind"] == "script"]
    todo = []
    survey, choices, used_names, lists = [], [], set(), {}
    pref = {k.strip().lower(): v.strip() for k, v in (p.split("=", 1) for p in prefixes.split(",") if "=" in p)} if prefixes else {}
    sections = []
    for q in qs:
        if q["section"] not in sections: sections.append(q["section"])
    survey.append(["start", "start", "", "", ""]); survey.append(["end", "end", "", "", ""])
    survey.append(["deviceid", "deviceid", "", "", ""])
    todo.append(["Settings", "public_key", "Encryption cannot be added after the form is created. Generate the key before first upload (SurveyCTO encryption setup) and store the private key safely", "Team"])
    todo.append(["Settings", "version / form_id", "Set form_id; version by formula (yymmddhhmm)", "Team"])
    consent_done = False
    consent_var, yes_code = None, "1"
    for si, sec in enumerate(sections, 1):
        title_words = re.findall(r"[a-z0-9]+", re.sub(r"^(module|section|part)\s+\w+\s*[:.\-]?\s*", "", sec.lower())) or [f"m{si}"]
        sp = next((v for k, v in pref.items() if k in sec.lower()), None) or title_words[0][:5]
        todo.append([sec, "module prefix", f"Prefix '{sp}' was guessed from the module title. Replace with the project's abbreviation (naming document)", "Team"]) if sp == title_words[0][:5] and not pref else None
        gname = f"{sp}"
        survey.append(["", "", "", "", ""])  # blank row between modules
        is_consent = "consent" in sec.lower()
        gate = f"${{{consent_var}}}={yes_code}" if consent_var and not is_consent else ""
        survey.append(["begin group", gname, sec, "", gate])
        if gate:
            todo.append([sec, "consent gate", f"Module shows only if {consent_var} = {yes_code}. Confirm", "Team"])
        if is_consent:
            for sc in [s for s in scripts if s["section"] == sec]:
                survey.append(["note", f"{sp}_script", sc["text"], "", ""])
            todo.append([sec, "Consent text", "Check the note text against the approved consent form before use", "Team"])
        for q in qs:
            if q["section"] != sec: continue
            t, kind = guess_type(q)
            name = f"{sp}_{slug(q['text'])}"
            base, k = name, 2
            while name in used_names:
                name = f"{base}_{k}"; k += 1
            used_names.add(name)
            name = name[:32]
            ttxt = t
            if kind == "choice":
                key = tuple((c["code"], c["label"]) for c in q["choices"])
                if key not in lists:
                    lname = f"{sp}_{slug(q['text'], 14)}"
                    base_l, k2 = lname, 2
                    while lname in {v for v in lists.values()}:
                        lname = f"{base_l}_{k2}"; k2 += 1
                    lists[key] = lname
                    for i, c in enumerate(q["choices"], 1):
                        code = special_code(c["label"], development impact) or (c["code"] if c["code"] and re.fullmatch(r"-?\d+", c["code"]) else str(i))
                        if c["code"] and special_code(c["label"], development impact) and c["code"] != special_code(c["label"], development impact):
                            todo.append([sec, lname, f"'{c['label']}' coded {c['code']} on paper; set to {special_code(c['label'], development impact)} per the Style Guide scheme. Update any skip logic", "Team"])
                        choices.append([lname, code, c["label"], ""])
                ttxt = f"{t} {lists[key]}"
            label = (f"{q['number']} " if q["number"] else "") + q["text"]
            survey.append([ttxt, name, label, "yes", ""])
            if is_consent and not consent_var and t == "select_one":
                consent_var = name
                yes = next((c for c in q["choices"] if re.match(r"^yes\b", c["label"].strip().lower())), None)
                yes_code = (yes["code"] if yes and yes["code"] else "1"); consent_done = True
            todo.append([sec, name, f"Type guessed as {t}" + (f"; paper note: {q['notes']}" if q["notes"] else "") +
                         ("; add a constraint (range) if numeric" if kind == "number" else ""), "Team"])
        survey.append(["end group", gname, "", "", ""])
    if not consent_done:
        todo.insert(0, ["Consent", "consent gate", "Confirm consent comes first and later groups only show if consent = 1 (add relevant on each module group)", "Team"])
    if template and Path(template).exists():
        wb = load_workbook(template)
        ws = wb["survey"]
        hdr = [str(c.value or "").strip().lower().replace(" ", "_") for c in ws[1]]
        lcol = next((i for i, h in enumerate(hdr) if h == f"label::{lang.lower()}" or h == "label" or h.startswith("label")), 2)
        for r in survey:
            row = [""] * len(hdr)
            def put(col, v):
                if col in hdr: row[hdr.index(col)] = v
            put("type", r[0]); put("name", r[1]); row[lcol] = r[2]; put("required", r[3]); put("relevant", r[4]) if "relevant" in hdr else put("relevance", r[4])
            ws.append(row)
        cs = wb["choices"]
        chdr = [str(c.value or "").strip().lower().replace(" ", "_") for c in cs[1]]
        cl = next((i for i, h in enumerate(chdr) if h.startswith("label")), 2)
        for r in choices:
            row = [""] * len(chdr)
            row[chdr.index("list_name")] = r[0]; row[chdr.index("value") if "value" in chdr else chdr.index("name")] = r[1]; row[cl] = r[2]
            cs.append(row)
    else:
        wb = Workbook(); ws = wb.active; ws.title = "survey"
        ws.append(["type", "name", f"label::{lang}", "required", "relevant"])
        for r in survey: ws.append(r)
        cs = wb.create_sheet("choices"); cs.append(["list_name", "name", f"label::{lang}"] + (["label:stata"] if development impact else []))
        for r in choices: cs.append(r if development impact else r[:3])
        st = wb.create_sheet("settings"); st.append(["form_title", "form_id", "version", "public_key"]); st.append(["DRAFT form", "draft_form", "", ""])
    td = wb.create_sheet("todo")
    td.append(["Where", "Item", "What the team must decide or check", "Owner"])
    for r in todo: td.append(r)
    td.column_dimensions["C"].width = 90
    wb.save(out)
    print(f"Draft written: {out}. {len([s for s in survey if s[1] and s[0] not in ('begin group','end group','start','end','deviceid','note')])} questions, "
          f"{len(set(c[0] for c in choices))} choice lists, {len(todo)} to-do items. Template used: {bool(template and Path(template).exists())}")


if __name__ == "__main__":
    if len(sys.argv) < 3 or "--out" not in sys.argv:
        print(__doc__); sys.exit(1)
    a = sys.argv
    get = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    build(a[1], get("--out"), get("--template"), get("--prefixes", ""), get("--lang", "English"), "--development impact" in a)
