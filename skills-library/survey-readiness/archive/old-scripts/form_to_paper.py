#!/usr/bin/env python3
"""Create a printable paper questionnaire (Word) from a programmed XLSForm.

Usage: python form_to_paper.py form.xlsx --out paper.docx [--lang English] [--title "Survey name"]

One section per top-level group, a table per module: number, question, response options,
skip or notes. Skip logic is translated into plain words where the pattern is simple;
anything else is shown as the raw expression and marked for a person to check.
"""
import re
import sys
from openpyxl import load_workbook
import docx
from docx.shared import Pt, Cm
from docx.enum.section import WD_ORIENT

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from compare_forms import load_form  # noqa: E402


def readable(expr, num_by_name, choices_by_name):
    if not expr:
        return ""
    e, flagged = expr, False
    def sel(m):
        n = m.group(1); v = m.group(2)
        lab = next((c["label"] for c in choices_by_name.get(n, []) if c["code"] == v), v)
        return f'Q{num_by_name.get(n, n)} includes "{lab}"'
    e = re.sub(r"selected\(\s*\$\{(\w+)\}\s*,\s*'([^']*)'\s*\)", sel, e)
    def cmp_(m):
        n, op, v = m.group(1), m.group(2), m.group(3).strip("'\"")
        lab = next((c["label"] for c in choices_by_name.get(n, []) if c["code"] == v), None)
        word = {"=": "is", "!=": "is not"}.get(op, op)
        return f'Q{num_by_name.get(n, n)} {word} "{lab}"' if lab else f"Q{num_by_name.get(n, n)} {word} {v}"
    e = re.sub(r"\$\{(\w+)\}\s*(=|!=|<=|>=|<|>)\s*('[^']*'|\"[^\"]*\"|-?\d+(?:\.\d+)?)", cmp_, e)
    e = re.sub(r"\$\{(\w+)\}", lambda m: f"Q{num_by_name.get(m.group(1), m.group(1))}", e)
    e = e.replace(" and ", " AND ").replace(" or ", " OR ")
    if re.search(r"[(){}]|\bpulldata\b|\bcount\b|\bif\(", e):
        flagged = True
    return f"Ask if: {e}" + (" [CHECK: complex condition, confirm wording]" if flagged else "")


def build(form, out, lang, title):
    items = [i for i in load_form(form, lang) if i["kind"] in ("question", "note")]
    num_by_name, mods = {}, {}
    for it in items:
        mods.setdefault(it["section"], []).append(it)
    for mi, (sec, its) in enumerate(mods.items(), 1):
        qi = 0
        for it in its:
            if it["kind"] == "question":
                qi += 1
                it["auto_num"] = f"{mi}.{qi}"
                num_by_name[it["name"]] = it["number"] or it["auto_num"]
    choices_by_name = {it["name"]: it["choices"] for it in items}
    d = docx.Document()
    s = d.sections[0]
    s.orientation = WD_ORIENT.LANDSCAPE; s.page_width, s.page_height = s.page_height, s.page_width
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"): setattr(s, m, Cm(1.8))
    st = d.styles["Normal"]; st.font.name = "Arial"; st.font.size = Pt(10)
    d.add_heading(title, 0)
    d.add_paragraph("Generated from the programmed form. Check against the approved protocol before use.")
    for sec, its in mods.items():
        d.add_heading(sec, 1)
        for it in [i for i in its if i["kind"] == "note"]:
            d.add_paragraph(re.sub(r"\$\{[^}]+\}", "[...]", it["label"]))
        qs = [i for i in its if i["kind"] == "question"]
        if not qs:
            continue
        t = d.add_table(rows=1, cols=4); t.style = "Table Grid"
        for c, h in zip(t.rows[0].cells, ["No.", "Question", "Response options", "Skip / notes"]):
            c.text = h
            for r in c.paragraphs[0].runs: r.font.bold = True
        for it in qs:
            r = t.add_row().cells
            label = re.sub(r"^\s*(?:Q\s?)?[A-Za-z]{0,3}\d+(?:\.\d+)*[a-z]?\s*[.):\-]?\s+", "", it["label"])
            r[0].text = it["number"] or it["auto_num"]
            r[1].text = re.sub(r"\$\{[^}]+\}", "[...]", label)
            if it["choices"]:
                r[2].text = "\n".join(f"{c['code']} = {c['label']}" for c in it["choices"])
            else:
                r[2].text = {"integer": "Numeric (whole number)", "decimal": "Numeric", "date": "Date", "text": "Open text",
                             "geopoint": "GPS"}.get(it["base"], it["base"])
            notes = [readable(it["relevant"], num_by_name, choices_by_name)]
            if it["hint"]: notes.append("Enumerator note: " + it["hint"])
            if it["base"] == "select_multiple": notes.append("Select all that apply")
            r[3].text = "\n".join(n for n in notes if n)
        t.autofit = False
        widths = [Cm(1.6), Cm(9.5), Cm(7), Cm(6.5)]
        for col, w in zip(t.columns, widths): col.width = w
        for row in t.rows:
            for c, w in zip(row.cells, widths): c.width = w
    d.save(out)
    print(f"Paper version written: {out}: {sum(len([i for i in v if i['kind']=='question']) for v in mods.values())} questions in {len(mods)} modules")


if __name__ == "__main__":
    if len(sys.argv) < 3 or "--out" not in sys.argv:
        print(__doc__); sys.exit(1)
    a = sys.argv
    get = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    build(a[1], get("--out"), get("--lang", "English"), get("--title", "Questionnaire"))
