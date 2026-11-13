#!/usr/bin/env python3
"""Extract a paper questionnaire (Word, Excel, PDF) into a normalized item list.

Usage: python extract_paper.py paper.(docx|xlsx|pdf) [--out items.json] [--show N]

Each item: section, number, text, choices [{code, label}], response_type, notes,
kind (question | script), source. Static reading only; never executes the file.
Tables are read by column headers (number, question, response options, skip or
notes). Text that is not in a table is read line by line. Results are candidates:
confirm them in context before reporting, and say what could not be read.
"""
import re
import sys
import json
from pathlib import Path

ID_HDR = {"no", "no.", "q", "q#", "q no", "q.no", "number", "#", "id", "qn", "ref", "question no",
          "question number", "q. no", "qno", "item", "variable", "nr"}
TXT_HDR = {"question", "questions", "question text", "text", "label", "item text", "wording"}
CHO_HDR = {"response", "responses", "response options", "options", "choices", "answer", "answers",
           "codes", "response categories", "categories", "answer options", "coding", "response codes"}
NOTE_HDR = {"skip", "skip pattern", "skip to", "instructions", "instruction", "notes", "note",
            "enumerator", "routing", "filter", "go to", "skip instructions", "enumerator notes",
            "interviewer instructions", "programming notes"}
SKIP_SHEETS = {"main", "cover", "toc", "contents", "instructions", "readme", "version", "changelog"}
TYPE_WORDS = {"open", "text", "open text", "numeric", "number", "integer", "decimal", "date", "time",
              "open-ended", "open ended", "free text", "gps", "photo", "numeric (integer)"}
GLYPHS = "☐□○◯▢■●•▪-–—*"
CHOICE_LINE = re.compile(
    r"^\s*(?:[" + re.escape(GLYPHS) + r"]\s*|\[\s*\]\s*|\(\s*\)\s*)?"
    r"(?P<code>-?\d{1,3}|[a-zA-Z])\s*(?:[=.):]|\s-\s)\s*(?P<label>\S.*?)\s*$")
GLYPH_ONLY = re.compile(r"^\s*(?:[" + re.escape("☐□○◯▢") + r"]|\[\s*\]|\(\s*\))\s*(?P<label>\S.*?)\s*$")
Q_LINE = re.compile(r"^\s*(?P<num>(?:Q\s?)?[A-Za-z]{0,3}\d+(?:\.\d+)*[a-z]?)\s*[.):\-]?\s+(?P<text>\S.*?)\s*$")
HEADING = re.compile(r"^\s*(module|section|part)\s+[\w.]+", re.I)


def norm(s):
    return re.sub(r"\s+", " ", (s or "").replace("\xa0", " ")).strip()


def parse_choice_text(cell):
    """Split a response cell into choices, or return (choices, response_type)."""
    cell = (cell or "").replace("\r", "")
    pieces = [p.strip() for p in re.split(r"\n|;", cell) if p.strip()]
    if not pieces:
        return [], None
    if len(pieces) == 1 and pieces[0].lower().strip(" .") in TYPE_WORDS:
        return [], pieces[0].lower().strip(" .")
    out = []
    for p in pieces:
        m = CHOICE_LINE.match(p)
        if m:
            out.append({"code": m.group("code"), "label": norm(m.group("label"))})
        else:
            g = GLYPH_ONLY.match(p)
            out.append({"code": None, "label": norm(g.group("label") if g else p)})
    return out, None


def map_header(row):
    cols = {}
    for i, c in enumerate(row):
        h = norm(c).lower().strip(":")
        if h in ID_HDR and "id" not in cols: cols["id"] = i
        elif h in TXT_HDR and "text" not in cols: cols["text"] = i
        elif h in CHO_HDR and "choices" not in cols: cols["choices"] = i
        elif h in NOTE_HDR and "notes" not in cols: cols["notes"] = i
    return cols if "text" in cols or ("id" in cols and "choices" in cols) else None


def rows_to_items(rows, section, source, items, warn, state=None):
    """Turn table rows (lists of strings) into items. Handles header or no header.
    state remembers the last header mapping so a table that continues on a new page still parses."""
    state = state if state is not None else {}
    cols = None
    start = 0
    for i, r in enumerate(rows[:4]):
        cols = map_header(r)
        if cols:
            start = i + 1
            break
    if not cols and state.get("cols") and rows and max(len(r) for r in rows) == state.get("ncols"):
        cols = state["cols"]  # continuation of a table from the previous page
    elif not cols:
        n = max(len(r) for r in rows) if rows else 0
        if n < 2:
            return
        cols = {"id": 0, "text": 1}
        if n >= 3: cols["choices"] = 2
        if n >= 4: cols["notes"] = 3
        warn.append(f"{source}: no header row found; assumed columns number, question, responses, notes")
    state["cols"], state["ncols"] = cols, max(len(r) for r in rows)
    cur_section = section
    last = state.get("last")  # carried over from the previous table if it continued
    for ri, r in enumerate(rows[start:], start + 1):
        cells = [norm(c) for c in r]
        nonempty = [c for c in cells if c]
        if not nonempty:
            continue
        only = nonempty[0] if len(nonempty) == 1 else None
        if only and (len(r) == 1 or HEADING.match(only) or only.isupper()
                     or (cells.index(only) == cols.get("id", -1) and not cells[cols.get("text", 1)])):
            cur_section = only  # merged or single-cell row: a section heading
            continue
        g = lambda k: cells[cols[k]] if k in cols and cols[k] < len(cells) else ""
        num, text = g("id"), g("text")
        raw_choices = r[cols["choices"]] if "choices" in cols and cols["choices"] < len(r) else ""
        choices, rtype = parse_choice_text(raw_choices)
        notes = g("notes")
        if text and not num and last is not None and not last["text"].rstrip().endswith(("?", ".", ":")) \
                and not re.match(r"^[A-Z]", text):
            last["text"] = (last["text"] + " " + text).strip()  # question text wrapped across a page break
            last["choices"] += choices
            if notes: last["notes"] = (last["notes"] + " " + notes).strip()
            continue
        if not text and not num and last is not None and (choices or notes):
            # continuation row: more options or notes for the previous question
            last["choices"] += choices
            if notes: last["notes"] = (last["notes"] + " " + notes).strip()
            continue
        if not text and num and len(nonempty) == 1:
            cur_section = num
            continue
        item = {"section": cur_section, "number": num or None, "text": text, "choices": choices,
                "response_type": rtype, "notes": notes, "kind": "question",
                "source": f"{source} row {ri}"}
        if not text:
            continue
        items.append(item)
        last = item
        state["last"] = item


def parse_lines(lines, section, source, items, warn):
    """Read paragraph text: numbered questions, choice lines, headings, scripts."""
    cur = None
    cur_section = section
    for ln, (line, is_heading) in enumerate(lines, 1):
        line = norm(line)
        if not line:
            continue
        if is_heading or HEADING.match(line):
            cur_section = line
            cur = None
            continue
        m_ch = CHOICE_LINE.match(line)
        m_gl = GLYPH_ONLY.match(line)
        m_q = Q_LINE.match(line)
        looks_choice = bool(cur) and (m_gl or (m_ch and len(line) < 70 and "?" not in line and
                                              (not m_q or re.fullmatch(r"-?\d{1,3}", m_q.group("num")) is not None
                                               and "." not in m_q.group("num") and len(m_q.group("text")) < 45
                                               and not m_q.group("text").endswith("?"))))
        if looks_choice:
            if m_gl and not m_ch:
                cur["choices"].append({"code": None, "label": norm(m_gl.group("label"))})
            else:
                cur["choices"].append({"code": m_ch.group("code"), "label": norm(m_ch.group("label"))})
            continue
        if m_q and (re.search(r"[A-Za-z]\d|\d\.\d|^Q", m_q.group("num")) or m_q.group("text").endswith(("?", ":"))
                    or len(m_q.group("text")) > 25):
            cur = {"section": cur_section, "number": m_q.group("num"), "text": m_q.group("text"),
                   "choices": [], "response_type": None, "notes": "", "kind": "question",
                   "source": f"{source} line {ln}"}
            items.append(cur)
            continue
        if cur and re.match(r"^(\(?\s*(if|skip|go to|enumerator|note|probe|read)\b)", line, re.I):
            cur["notes"] = (cur["notes"] + " " + line).strip()
            continue
        prev_script = bool(items) and items[-1]["kind"] == "script" and items[-1]["section"] == cur_section and cur is None
        if prev_script:
            items[-1]["text"] += " " + line  # wrapped text block continues
        elif len(line) >= 80:
            items.append({"section": cur_section, "number": None, "text": line, "choices": [],
                          "response_type": None, "notes": "", "kind": "script", "source": f"{source} line {ln}"})
            cur = None
        elif cur and not cur["choices"]:
            cur["text"] = (cur["text"] + " " + line).strip()  # wrapped question text
    return cur_section


def read_docx(path, items, warn):
    import docx
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    d = docx.Document(path)
    section = "(no section)"
    buf = []
    tcount = 0

    def flush():
        nonlocal buf
        if buf:
            parse_lines(buf, section, "docx", items, warn)
            buf = []

    for child in d.element.body.iterchildren():
        tag = child.tag.split("}")[1]
        if tag == "p":
            p = Paragraph(child, d)
            style = (p.style.name or "") if p.style is not None else ""
            is_h = style.lower().startswith(("heading", "title"))
            if is_h and p.text.strip():
                flush()
                section = norm(p.text)
            else:
                buf.append((p.text, False))
        elif tag == "tbl":
            flush()
            tcount += 1
            t = Table(child, d)
            rows = []
            for row in t.rows:
                seen, cells = set(), []
                for c in row.cells:
                    if id(c._tc) in seen:
                        continue
                    seen.add(id(c._tc))
                    cells.append(c.text)
                rows.append(cells)
            rows_to_items(rows, section, f"docx table {tcount}", items, warn)
    flush()
    if tcount == 0:
        warn.append("No tables found; read paragraphs only")


def read_xlsx(path, items, warn):
    from openpyxl import load_workbook
    wb = load_workbook(path, data_only=True)
    empty_formula = 0
    for ws in wb.worksheets:
        if ws.title.strip().lower() in SKIP_SHEETS:
            continue
        rows = [[("" if v is None else str(v)) for v in r] for r in ws.iter_rows(values_only=True)]
        rows = [r for r in rows if any(c.strip() for c in r)]
        if not rows:
            continue
        rows_to_items(rows, ws.title, f"sheet '{ws.title}'", items, warn)
    wb2 = load_workbook(path, data_only=False)
    for ws in wb2.worksheets:
        for r in ws.iter_rows():
            for c in r:
                if isinstance(c.value, str) and c.value.startswith("="):
                    v = wb[ws.title][c.coordinate].value
                    if v is None: empty_formula += 1
    if empty_formula:
        warn.append(f"{empty_formula} formula cells have no cached value; open and save the workbook in Excel, then re-run")


def read_pdf(path, items, warn):
    import pdfplumber
    any_text = False
    state = {}
    section = "(no section)"
    with pdfplumber.open(path) as pdf:
        for pi, page in enumerate(pdf.pages, 1):
            tables = [t for t in page.find_tables() if t.extract() and len(t.extract()) >= 1
                      and max(len(r) for r in t.extract()) >= 2]
            blocks = []  # (top, kind, payload)
            for tb in tables:
                blocks.append((tb.bbox[1], "table", tb))
            for ln in page.extract_text_lines():
                any_text = True
                cy = (ln["top"] + ln["bottom"]) / 2
                if any(tb.bbox[1] - 1 <= cy <= tb.bbox[3] + 1 for tb in tables):
                    continue
                blocks.append((ln["top"], "line", ln["text"]))
            blocks.sort(key=lambda b: b[0])
            pending = []
            for _, kind, payload in blocks:
                if kind == "line":
                    pending.append((payload, bool(HEADING.match(payload))))
                else:
                    if pending:
                        section = parse_lines(pending, section, "pdf", items, warn) or section
                        pending = []
                    rows = [[c or "" for c in r] for r in payload.extract()]
                    rows_to_items(rows, section, f"pdf page {pi} table", items, warn, state)
            if pending:
                section = parse_lines(pending, section, "pdf", items, warn) or section
    if not any_text:
        warn.append("PDF has no text layer (scanned). Read it page by page as images or ask for the Word or Excel version")



# ---------------- specification-style paper (variable names and form expressions printed) ----------------
SPEC_Q = re.compile(r"^(?P<num>[A-Za-z]{0,3}\d+(?:\.\d+)*[a-z]?)(?:\s{2,}|\t+)(?P<name>[A-Za-z_]\w*)(?:\s{2,}|\t+)"
                    r"(?P<type>[a-z_]+(?: \S+)?)(?:\s{2,}|\t+)?(?P<req>Required)?\s*$")
SPEC_NOTE = re.compile(r"^Note\s+(?P<num>\S+)(?:\s{2,}|\t+)(?P<name>[A-Za-z_]\w*)(?:\s{2,}|\t+)note\s*$")
SPEC_LABEL = re.compile(r"^(?P<num>[A-Za-z]{0,3}\d+(?:\.\d+)*[a-z]?)\s*:\s*(?P<text>.*)$")
SPEC_CHOICE = re.compile(r"^[\u25cb\u25ef\u2610\u25a1\u25cf]\s*(?P<v>\S+)\s*(?:\t|\s{2,})\s*(?P<l>.*?)\s*$")
SPEC_KEY = re.compile(r"^(?P<k>Appearance|Constraint message|Constraint|Ask whole group if|Ask if|Relevant if|Relevance|Hint|Default|Choice filter|Repeat count)\s*:\s*(?P<v>.*)$", re.I)
SPEC_EXT = re.compile(r"^Choices are loaded at run time from\s+(?P<f>\S+)", re.I)
HEAD_NAME = re.compile(r"^(?P<label>.*?)\s*\[(?P<name>[A-Za-z_]\w*)\]\s*$")


def looks_spec(d):
    n = 0
    for p in d.paragraphs:
        if SPEC_Q.match(p.text.strip()) or SPEC_NOTE.match(p.text.strip()):
            n += 1
            if n >= 3:
                return True
    return False


def new_item(section, group, num, name, qtype, req, grel, src, kind="question"):
    t = (qtype or "").split()
    return {"section": section, "group": group, "number": num, "name": name, "qtype": t[0] if t else "",
            "list_name": t[1] if len(t) > 1 else "", "required": bool(req), "text": "", "choices": [],
            "response_type": None, "notes": "", "kind": kind, "source": src, "relevance": "",
            "group_relevance": list(grel), "constraint": "", "constraint_message": "", "appearance": "",
            "hint": "", "choice_file": "", "choice_filter": ""}


def read_docx_spec(path, items, warn):
    import docx
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    d = docx.Document(path)
    section, gstack, cur, lastkey, unparsed, tcount = "(no section)", {}, None, None, 0, 0

    def grel():
        return [g["rel"] for _, g in sorted(gstack.items()) if g.get("rel")]

    for child in d.element.body.iterchildren():
        tag = child.tag.split("}")[1]
        if tag == "tbl":
            tcount += 1
            t = Table(child, d)
            hdr = [c.text.strip().lower() for c in t.rows[0].cells] if t.rows else []
            if "name" in hdr and "calculation" in hdr:
                ni, ci = hdr.index("name"), hdr.index("calculation")
                ri = hdr.index("relevance") if "relevance" in hdr else None
                for r in t.rows[1:]:
                    cells = [c.text.strip() for c in r.cells]
                    if len(cells) > max(ni, ci) and cells[ni]:
                        it = new_item("(calculate fields)", "", None, re.sub(r"\s*\(here\)\s*$", "", cells[ni]), "calculate",
                                      False, [], f"docx table {tcount}", kind="calculate")
                        it["calculation"] = cells[ci]
                        it["relevance"] = cells[ri] if ri is not None and len(cells) > ri else ""
                        items.append(it)
            continue
        if tag != "p":
            continue
        p = Paragraph(child, d)
        txt = p.text.strip()
        if not txt:
            continue
        style = (p.style.name or "") if p.style is not None else ""
        m = re.match(r"heading\s*(\d)", style.lower())
        if m:
            lvl = int(m.group(1))
            hm = HEAD_NAME.match(txt)
            label = hm.group("label").strip() if hm else txt
            name = hm.group("name") if hm else ""
            if lvl == 1:
                section, gstack = norm(label), {1: {"name": name, "label": label, "rel": ""}}
            else:
                for k in [k for k in gstack if k >= lvl]:
                    del gstack[k]
                gstack[lvl] = {"name": name, "label": label, "rel": ""}
            cur, lastkey = None, None
            continue
        mq, mn = SPEC_Q.match(txt), SPEC_NOTE.match(txt)
        if mn or (mq and mq.group("type").split()[0] in SPEC_TYPES):
            g = mq or mn
            qt = "note" if mn else g.group("type")
            cur = new_item(section, " > ".join(x["name"] for _, x in sorted(gstack.items()) if x["name"]), g.group("num"),
                           g.group("name"), qt, bool(mq and mq.group("req")), grel(), f"docx line", "script" if mn else "question")
            items.append(cur)
            lastkey = "label"
            continue
        mk = SPEC_KEY.match(txt)
        if mk:
            k, v = mk.group("k").lower(), mk.group("v").strip()
            if k == "ask whole group if":
                if gstack:
                    gstack[max(gstack)]["rel"] = v
                lastkey = None
            elif cur is not None:
                field = {"appearance": "appearance", "constraint message": "constraint_message", "constraint": "constraint",
                         "ask if": "relevance", "relevant if": "relevance", "relevance": "relevance", "hint": "hint",
                         "default": "default", "choice filter": "choice_filter", "repeat count": "repeat_count"}[k]
                cur[field] = v
                lastkey = field
            continue
        if cur is not None:
            me = SPEC_EXT.match(txt)
            if me:
                cur["choice_file"], cur["choices"] = me.group("f"), []
                lastkey = None
                continue
            mc = SPEC_CHOICE.match(txt)
            if mc:
                if not cur["choice_file"]:
                    cur["choices"].append({"code": mc.group("v"), "label": mc.group("l")})
                lastkey = "choice"
                continue
            ml = SPEC_LABEL.match(txt)
            if ml and ml.group("num") == cur["number"] and not cur["text"]:
                cur["text"] = ml.group("text").strip()
                lastkey = "label"
                continue
            if lastkey == "label":
                cur["text"] += "\n" + txt
                continue
            if lastkey in ("constraint_message", "hint"):
                cur[lastkey] += " " + txt
                continue
        unparsed += 1
    qn = sum(1 for i in items if i["kind"] == "question")
    if unparsed:
        warn.append(f"{unparsed} paragraph(s) in the specification-style paper were not recognised (not counted as questions)")
    warn.append(f"Read as a specification-style paper: variable names and form expressions are compared directly ({qn} questions)")


SPEC_TYPES = {"select_one", "select_multiple", "text", "integer", "decimal", "date", "datetime", "time", "geopoint",
              "geotrace", "geoshape", "image", "audio", "video", "barcode", "range", "rank", "file", "acknowledge",
              "calculate", "note", "string", "select_one_from_file", "select_multiple_from_file", "select_one_external"}

STOPS = {"en": "the of and to in is are you your do did how what which many have has any for with".split(),
         "fr": "le la les des du de un une est sont vous votre avez avez-vous combien quel quelle pour avec dans que qui".split(),
         "es": "el la los las del de un una es son usted su tiene cuantos cual para con en que quien".split(),
         "pt": "o a os as do da de um uma e são você seu tem quantos qual para com em que quem".split()}


def guess_language(items):
    txt = " ".join(i["text"] for i in items if i["kind"] == "question")[:20000].lower()
    words = re.findall(r"[a-zàâçéèêëîïôûùüÿñãõ-]+", txt)
    scores = {k: sum(1 for w in words if w in set(v)) for k, v in STOPS.items()}
    tot = sum(scores.values()) or 1
    best = max(scores, key=scores.get)
    return {"guess": {"en": "English", "fr": "French", "es": "Spanish", "pt": "Portuguese"}[best] if scores[best] >= 5 else "unknown",
            "share": round(scores[best] / tot, 2), "scores": scores}


def main(path, out=None, show=8):
    p = Path(path)
    items, warn = [], []
    ext = p.suffix.lower()
    if ext == ".docx":
        import docx as _d
        (read_docx_spec if looks_spec(_d.Document(p)) else read_docx)(p, items, warn)
    elif ext in (".xlsx", ".xlsm"): read_xlsx(p, items, warn)
    elif ext == ".pdf": read_pdf(p, items, warn)
    else:
        print(f"Unsupported file type {ext}. Convert .doc to .docx first.")
        sys.exit(2)
    qs = [i for i in items if i["kind"] == "question"]
    lang = guess_language(items)
    result = {"source": p.name, "format": ext.lstrip("."), "warnings": warn, "language_guess": lang, "items": items}
    if out:
        Path(out).write_text(json.dumps(result, indent=1, ensure_ascii=False))
    secs = {}
    for i in qs:
        secs[i["section"]] = secs.get(i["section"], 0) + 1
    print(f"# {p.name}: {len(qs)} questions, {sum(1 for i in items if i['kind']=='script')} text blocks, "
          f"{len(secs)} sections; {sum(1 for i in qs if i['choices'])} questions have choices")
    print(f"# Paper language (guess from stop words): {lang['guess']}")
    for s, n in secs.items():
        print(f"#   {s}: {n}")
    for w in warn:
        print(f"WARNING: {w}")
    if len(qs) == 0:
        print("WARNING: no questions found. Look at the file directly before relying on this.")
    for i in qs[:show]:
        ch = "; ".join(f"{c['code']}={c['label']}" if c["code"] else c["label"] for c in i["choices"][:6])
        print(f"{i['number'] or '-'} | {i['text'][:70]} | {ch[:60]}")
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    a = sys.argv
    out = a[a.index("--out") + 1] if "--out" in a else None
    show = int(a[a.index("--show") + 1]) if "--show" in a else 8
    main(a[1], out, show)
