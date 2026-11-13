#!/usr/bin/env python3
"""Mechanical checks for XLSForm instruments (ODK / KoboToolbox / SurveyCTO).

Usage: python inspect_xlsform.py form.xlsx [--json] [--full] [--style-guide]

--style-guide adds the optional Impact Analytics SurveyCTO Style Guide checks: white space between
modules, lowercase a-z0-9_ names, special codes -99/-88/-9, form version format, and choice labels
loaded by calculate. Best-practice checks (including ietestform tests) always run.
See references/style-guide.md.

Static analysis only. Reads the .xlsx, never executes it. Prints one finding per
line: ID | severity | sheet:row | name | evidence. Flag IDs match
references/programming-flags.md. Results are candidates for the reviewer to confirm
in context; they are not final findings.
"""
import re
import sys
import json
from collections import defaultdict, Counter
from openpyxl import load_workbook

REF = re.compile(r"\$\{([^}]+)\}")
NAME_OK = re.compile(r"^[A-Za-z_][A-Za-z0-9_\-.]*$")
NO_DATA = {"note", "begin group", "end group", "begin repeat", "end repeat",
           "begin_group", "end_group", "begin_repeat", "end_repeat", "calculate",
           "start", "end", "today", "deviceid", "username", "phonenumber",
           "subscriberid", "simserial", "audit", "hidden", "comments", "caseid",
           "email", "text audit", "sensor_stream", "calculate_here"}
EXCLUSIVE = re.compile(r"\b(none|don'?t know|dk|refus\w*|no answer|not applicable|n/?a)\b", re.I)


ALIASES = {"relevance": "relevant", "constraint_msg": "constraint_message",
           "choice filter": "choice_filter", "list name": "list_name"}


def norm_header(h):
    """Normalize a column header: trim, lowercase the base name, spaces to
    underscores (keeps label::Language case), and map SurveyCTO aliases."""
    if h is None:
        return ""
    h = str(h).strip()
    if "::" in h:
        base, lang = h.split("::", 1)
        return base.strip().lower().replace(" ", "_") + "::" + lang.strip()
    h = h.lower().replace(" ", "_")
    return ALIASES.get(h, h)


def read_sheet(wb, name):
    if name not in wb.sheetnames:
        return None, []
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return [], []
    header = [norm_header(h) for h in rows[0]]
    out = []
    unresolved = 0
    for i, r in enumerate(rows[1:], start=2):
        d = {header[j]: ("" if v is None else str(v).strip())
             for j, v in enumerate(r) if j < len(header) and header[j]}
        d["_row"] = i
        d["_ws"] = [header[j] for j, v in enumerate(r)
                    if j < len(header) and header[j] in ("name", "list_name", "type")
                    and isinstance(v, str) and v != v.strip()]
        if any(v.startswith("=") for k, v in d.items() if not k.startswith("_")):
            unresolved += 1
        if any(v for k, v in d.items() if not k.startswith("_")):
            out.append(d)
    if unresolved:
        sys.stderr.write(f"WARNING: sheet '{name}' has {unresolved} rows with uncalculated formulas. "
                         "Open and save the file in Excel so values are cached, then re-run.\n")
    return header, out


def main(path, as_json=False, style_guide=False):
    wb = load_workbook(path, read_only=True, data_only=True)  # cached values: names may be formulas
    findings = []

    def add(fid, sev, sheet, row, name, ev):
        findings.append({"id": fid, "severity": sev,
                         "location": f"{sheet}:{row}" if row else sheet,
                         "name": name, "evidence": ev})

    s_hdr, survey = read_sheet(wb, "survey")
    c_hdr, choices = read_sheet(wb, "choices")
    st_hdr, settings = read_sheet(wb, "settings")

    if survey is None:
        add("STRUCT-001", "Critical", "workbook", None, "", "No 'survey' sheet found")
        print_out(findings, as_json)
        return
    uses_select = any(r.get("type", "").startswith(("select_one", "select_multiple")) for r in survey)
    if choices is None and uses_select:
        add("STRUCT-001", "Critical", "workbook", None, "", "Select questions exist but no 'choices' sheet found")
        choices = []

    lists = defaultdict(list)
    for c in choices or []:
        lists[c.get("list_name") or c.get("list name", "")].append(c)
    c_cols = set(c_hdr or [])

    names, qtype = {}, {}
    in_repeat = []
    prev_row, top_groups = 0, []
    scoped = {}  # (parent path, lowercase name) -> first row, for duplicate detection
    stack, used_lists = [], set()
    END_TYPES = {"end group", "end repeat", "end_group", "end_repeat"}
    for r in survey:
        t = re.sub(r"\s+", " ", r.get("type", "")).strip()
        n = r.get("name", "")
        base = t.split(" ")[0] if t else ""
        row = r["_row"]
        gap = row - prev_row if prev_row else 2
        prev_row = row
        if t.startswith("begin") and not stack:
            top_groups.append(gap > 1)
        is_end = t in END_TYPES
        if t.startswith("begin"):
            stack.append((t, n, row))
        elif is_end:
            if not stack:
                add("STRUCT-002", "High", "survey", row, n, f"'{t}' with no matching begin")
            else:
                bt, bn, brow = stack.pop()
                bk, ek = bt.replace("_", " "), t.replace("_", " ")
                if bk.split(" ")[1] != ek.split(" ")[1]:
                    add("STRUCT-003", "High", "survey", row, n, f"'{t}' closes '{bt}' from row {brow}: wrong type")
                elif not n:
                    add("STRUCT-003", "Low", "survey", row, "", f"'{t}' has no name (should match '{bn}', row {brow})")
                elif n != bn:
                    add("STRUCT-003", "Medium", "survey", row, n, f"'{t}' name does not match its begin ('{bn}', row {brow})")
        if n and not is_end:
            key = (tuple(g[1] for g in stack[:-1] if t.startswith("begin")) if t.startswith("begin")
                   else tuple(g[1] for g in stack), n.lower())
            if key in scoped:
                add("NAME-001", "High", "survey", row, n,
                    f"Duplicate name within the same group (case-insensitive); first defined at row {scoped[key]}")
            else:
                scoped[key] = row
            if n not in names:
                names[n] = row
                qtype[n] = t
            depth = sum(1 for g in stack if g[0].replace("_", " ") == "begin repeat")
            if t.replace("_", " ") == "begin repeat":
                depth -= 1
            is_begin = t.startswith("begin")
            limit = 32 if is_begin else 32 - 2 * depth
            if len(n) > limit:
                add("NAME-003", "Medium", "survey", row, n,
                    f"{'Group' if is_begin else 'Name'} is {len(n)} chars; limit is {limit}"
                    + ("" if is_begin else f" (Stata 32, less repeat suffixes at depth {depth})"))
            elif depth and not is_begin and len(n) > 32 - 3 * depth:
                add("NAME-003", "Low", "survey", row, n,
                    f"Possible: {len(n)} chars may exceed 32 once repeat suffixes reach 2 digits (depth {depth})")
            if depth and not is_begin:
                in_repeat.append((n, row, depth))
            if not NAME_OK.match(n):
                add("NAME-002", "Medium", "survey", row, n,
                    "Name contains spaces/special characters or starts with a digit")
        elif not n and t and not is_end and base != "note":
            add("NAME-002", "High", "survey", row, "", f"Row of type '{t}' has no name")

        if base in ("select_one", "select_multiple") and len(t.split(" ")) > 1:
            lst = t.split(" ")[1]
            used_lists.add(lst)
            if lst not in lists:
                add("LIST-001", "Critical", "survey", row, n, f"List '{lst}' not found in choices sheet")
            elif base == "select_multiple":
                excl = [o for o in lists[lst]
                        if EXCLUSIVE.search(o.get("label", "") or o.get("label::English", ""))]
                if excl and not r.get("constraint", ""):
                    add("VALID-004", "Medium", "survey", row, n,
                        "select_multiple has exclusive-type option(s) "
                        f"({', '.join(o.get('name', '') for o in excl)}) but no constraint")
        if base in ("integer", "decimal") and not r.get("constraint", ""):
            add("VALID-001", "Low", "survey", row, n, f"{base} with no constraint (plausible range not enforced)")
        if r.get("constraint", "") and not any(
                v for k, v in r.items() if k.startswith("constraint_message") and v):
            add("VALID-002", "Low", "survey", row, n, "Constraint has no constraint_message")
        if r.get("choice_filter", "") and c_hdr is not None:
            for m in re.finditer(r"\b([A-Za-z_][\w\-]*)\s*(?:=|!=|<=|>=|<|>)", r["choice_filter"]):
                col = m.group(1)
                if col not in c_cols:
                    add("LOGIC-006", "High", "survey", row, n,
                        f"choice_filter uses '{col}', which is not a column in choices")

    for t, n, row in stack:
        add("STRUCT-002", "High", "survey", row, n, f"'{t}' never closed")

    all_lower = {k.lower() for k in names}
    for n, row, depth in in_repeat:
        rx = re.compile(rf"^{re.escape(n.lower())}(_\d+)+$")
        clash = next((o for o in all_lower if rx.match(o)), None)
        if clash:
            add("NAME-004", "Low", "survey", row, n, f"In a repeat group; export suffix could collide with '{clash}'")

    for sheet_name, rows_ in (("survey", survey), ("choices", choices or [])):
        for r in rows_:
            if r.get("_ws"):
                add("NAME-005", "Low", sheet_name, r["_row"], r.get("name", ""),
                    f"Leading or trailing space in: {', '.join(r['_ws'])}")

    # Logic references and reachability
    for r in survey:
        n, row = r.get("name", ""), r["_row"]
        for col in ("relevant", "constraint", "calculation", "default", "choice_filter",
                    "required", "repeat_count"):
            expr = r.get(col, "")
            if not expr:
                continue
            for ref in set(REF.findall(expr)):
                ref0 = ref.split("/")[-1].strip()
                if ref0 == ".":
                    continue
                if ref0 not in names:
                    add("LOGIC-001", "Critical", "survey", row, n, f"{col} references undefined '${{{ref0}}}'")
                elif ref0 == n and col == "relevant":
                    add("LOGIC-003", "High", "survey", row, n, "relevant references the question itself")
                elif col in ("relevant", "calculation", "required") and names[ref0] > row:
                    add("LOGIC-002", "High", "survey", row, n,
                        f"{col} references '{ref0}' defined later (row {names[ref0]})")
        expr = r.get("relevant", "")
        if expr:
            for m in re.finditer(r"\$\{([^}]+)\}\s*(=|!=)\s*['\"]([^'\"]*)['\"]", expr):
                v, op, val = m.groups()
                t = qtype.get(v, "")
                if t.startswith("select_multiple"):
                    add("LOGIC-005", "High", "survey", row, n,
                        f"'{v}' is select_multiple; use selected(${{{v}}}, '{val}') instead of {op}")
                check_value(add, row, n, v, val, t, lists, f"'{v}' {op} '{val}'")
            for m in re.finditer(r"selected\(\s*\$\{([^}]+)\}\s*,\s*['\"]([^'\"]*)['\"]\s*\)", expr):
                v, val = m.groups()
                check_value(add, row, n, v, val, qtype.get(v, ""), lists, f"selected(${{{v}}}, '{val}')")

    for r in survey:
        for col in ("relevant", "constraint", "calculation", "default", "choice_filter", "label"):
            expr = r.get(col, "")
            if "position(" in expr:
                add("SYNTAX-001", "Medium", "survey", r["_row"], r.get("name", ""), f"{col} uses position(); use index()")
            if "jr:choice-name(" in expr:
                add("SYNTAX-001", "Medium", "survey", r["_row"], r.get("name", ""),
                    f"{col} uses jr:choice-name(); use choice-label()")

    for lst, opts in lists.items():
        seen = {}
        non_num = [o for o in opts if o.get("name", "") and not re.fullmatch(r"-?\d+", o["name"])]
        if non_num:
            add("LIST-005", "Low", "choices", non_num[0]["_row"], lst,
                f"{len(non_num)} choice name(s) are not integers (e.g. '{non_num[0]['name']}'); Stata value labels need integers")
        lab_col = next((h for h in (c_hdr or []) if h == "label" or h.startswith("label::")), None)
        if lab_col:
            for o in opts:
                if bool(o.get(lab_col, "")) != bool(o.get("name", "")):
                    add("LIST-006", "Medium", "choices", o["_row"], lst, "Choice has a label but no name, or a name but no label")
            seen_lab = {}
            for o in opts:
                lb = o.get(lab_col, "")
                if lb and lb in seen_lab and seen_lab[lb] != o.get("name", ""):
                    add("LIST-007", "Low", "choices", o["_row"], lst, f"Same label '{lb[:30]}' used for different names")
                seen_lab.setdefault(lb, o.get("name", ""))
        for o in opts:
            nm = o.get("name", "")
            if nm in seen:
                add("LIST-002", "High", "choices", o["_row"], lst,
                    f"Duplicate choice name '{nm}' (first at row {seen[nm]})")
            else:
                seen[nm] = o["_row"]
        if len(opts) == 1:
            add("LIST-004", "Low", "choices", opts[0]["_row"], lst, "List has a single option")
        if lst and lst not in used_lists:
            add("LIST-003", "Low", "choices", opts[0]["_row"], lst, "List defined but not used by any question")

    q_rows = [r for r in survey if r.get("type", "").split(" ")[0] not in NO_DATA and r.get("name")]
    if q_rows:
        if "required" not in (s_hdr or []):
            add("VALID-003", "Medium", "survey", None, "", "No 'required' column; no question is enforced")
        else:
            not_req = [r for r in q_rows if r.get("required", "").lower() not in ("yes", "true", "true()", "1")]
            if not_req:
                geo = [r for r in not_req if r["type"].split(" ")[0].startswith("geo")]
                other = [r for r in not_req if r not in geo]
                if other:
                    ex = ", ".join(f"{r['name']} (row {r['_row']})" for r in other[:4])
                    add("VALID-003", "Medium", "survey", other[0]["_row"], "",
                        f"{len(other)} of {len(q_rows)} input fields are not required (e.g. {ex}). "
                        "Allow non-answers as choices and use relevance for legitimate skips")
                if geo:
                    add("VALID-003", "Low", "survey", geo[0]["_row"], "",
                        f"{len(geo)} GPS field(s) not required. Fine if a deliberate choice")
    for r in survey:
        if r.get("type", "") == "note" and r.get("required", "").lower() in ("yes", "true", "true()", "1") \
                and not r.get("relevant", ""):
            add("VALID-005", "Critical", "survey", r["_row"], r.get("name", ""),
                "Required note with no relevance: the enumerator cannot move past it, so the interview cannot be submitted")

    langs = {m.group(2) for h in (s_hdr or []) if (m := re.match(r"^(label)::(.+)$", h))}
    if len(langs) > 1:
        for r in survey:
            if not r.get("type") or r["type"] in END_TYPES:
                continue
            filled = {l for l in langs if r.get(f"label::{l}", "")}
            if filled and filled != langs:
                add("LANG-001", "Medium", "survey", r["_row"], r.get("name", ""),
                    f"Label missing for: {', '.join(sorted(langs - filled))}")


    # --- Hints, device identifiers, publishable personal data
    ENUM_RX = re.compile(r"^\s*[\[(]?\s*(enumerator|interviewer|surveyor)\b\s*[:\-\]]|\b(enumerator|interviewer)\s*:", re.I)
    for r in survey:
        lab = r.get("label", "") or next((v for k, v in r.items() if k.startswith("label::") and v), "")
        if lab and ENUM_RX.search(lab):
            add("HINT-001", "Low", "survey", r["_row"], r.get("name", ""),
                "Label contains an enumerator instruction; move it to the hint column")
    ids = [r for r in survey if r.get("type", "") in ("subscriberid", "simserial", "phonenumber")]
    if ids:
        add("META-005", "Low", "survey", ids[0]["_row"], "",
            f"Collects device identifiers ({', '.join(sorted({r['type'] for r in ids}))}); treat as personal data")
    PII_RX = re.compile(r"name|phone|mobile|address|gps|lat|lon|geo|dob|birth|national_?id", re.I)
    if "publishable" in (s_hdr or []):
        for r in survey:
            if r.get("publishable", "").lower() in ("yes", "true", "1") and (
                    PII_RX.search(r.get("name", "")) or r.get("type", "").startswith("geo")):
                add("META-006", "Medium", "survey", r["_row"], r.get("name", ""),
                    "Possible personal data marked publishable (readable without the private key)")

    # --- Duplicate question numbers shown in labels (first label column)
    lab_key = next((h for h in (s_hdr or []) if (h == "label" or h.startswith("label:")) and "stata" not in h), None)
    if lab_key:
        seen_n = defaultdict(list)
        for r in survey:
            m = re.match(r"^\s*((?:[A-Za-z]{1,3})?\d+(?:\.\d+)+[a-z]?)\b", r.get(lab_key, ""))
            if m and r.get("type", "").split(" ")[0] not in ("begin", "end", "begin_group", "begin_repeat"):
                seen_n[m.group(1)].append(r["_row"])
        dup = {k: v for k, v in seen_n.items() if len(v) > 1}
        if dup:
            ex = "; ".join(f"{k} on rows {', '.join(map(str, v[:3]))}" for k, v in list(dup.items())[:3])
            add("NUM-001", "Medium", "survey", list(dup.values())[0][0], "",
                f"{len(dup)} question number(s) appear more than once in labels. e.g. {ex}")

    # --- Style Guide checks (only with --style-guide)
    if style_guide:
        if len(top_groups) >= 3 and sum(1 for g in top_groups if not g) >= len(top_groups) / 2:
            add("STYLE-001", "Low", "survey", None, "",
                f"{sum(1 for g in top_groups if not g)} of {len(top_groups)} top-level groups have no blank row before them (white space between modules aids reading)")
        bad_names = [n for n in names if re.search(r"[A-Z]|[^a-z0-9_]", n)]
        if bad_names:
            add("NAME-006", "Low", "survey", None, "",
                f"{len(bad_names)} name(s) use uppercase or characters other than a-z, 0-9, _ (e.g. {', '.join(bad_names[:4])})")
    for r in (survey if style_guide else []):
        hit = None
        for col, v in r.items():
            if col == "label" or col.startswith("label::") or col.startswith("hint"):
                for ref in sorted(set(REF.findall(v))):
                    if qtype.get(ref.strip(), "").startswith(("select_one", "select_multiple")):
                        hit = hit or (col, ref)
        if hit:
            add("STYLE-003", "Medium", "survey", r["_row"], r.get("name", ""),
                f"{hit[0]} shows ${{{hit[1]}}}, a select field: enumerators will see the code, not the choice label. Load the label with a calculate field")

    # --- Best-practice checks on by default (Development Impact Wiki: SurveyCTO Coding Practices, Data Security)
    STATA_COLS = ("label:stata", "label::stata", "stata", "stata_label", "stata_labels")
    for sheet_name, hdr, rows_ in (("survey", s_hdr, survey), ("choices", c_hdr, choices)):
        if hdr is None or (sheet_name == "choices" and not rows_):
            continue
        col = next((h for h in STATA_COLS if h in hdr), None)
        if col is None:
            add("STATA-001", "Medium", sheet_name, None, "",
                "No Stata label column (add 'label:stata', English, max 80 chars)")
            continue
        bad = [(r["_row"], r.get(col, "")) for r in rows_
               if r.get(col, "") and (len(r[col]) > 80 or not r[col].isascii())]
        if bad:
            ex = "; ".join(f"row {i}: '{v[:40]}'" for i, v in bad[:3])
            add("STATA-002", "Low", sheet_name, bad[0][0], "",
                f"{len(bad)} Stata label(s) over 80 characters or non-ASCII. e.g. {ex}")

    # Special codes per the Style Guide: -99 Don't know, -88 Refused, -9 Other
    if style_guide:
        label_col = next((h for h in (c_hdr or []) if h == "label" or h.startswith("label::")), None)
        if label_col:
            kinds = {"Don't know": (re.compile(r"\bdon'?t know\b|\bdk\b", re.I), "-99"),
                     "Refused / prefer not to answer": (re.compile(r"\brefus\w*|prefer not|no answer", re.I), "-88"),
                     "Other": (re.compile(r"^\s*other\b", re.I), "-9")}
            for kind, (rx, expected) in kinds.items():
                codes = Counter(o.get("name", "") for opts in lists.values() for o in opts
                                if rx.search(o.get(label_col, "")))
                wrong = {c: n for c, n in codes.items() if c != expected}
                if wrong:
                    add("CODE-001", "Low", "choices", None, kind,
                        f"Style Guide code is {expected}; found " +
                        ", ".join(f"{c} (x{n})" for c, n in sorted(wrong.items(), key=lambda x: -x[1])[:6]))

    # Encryption at rest (SurveyCTO: public key set when the form is created)
    if settings is not None and "settings" in wb.sheetnames:
        if "public_key" not in (st_hdr or []):
            add("META-004", "Medium", "settings", None, "",
                "No public_key column; if this is a SurveyCTO form, encryption at rest is not enabled "
                "(recommended whenever personal data are collected). It can only be set when the form is created")
        elif not (settings[0].get("public_key") if settings else ""):
            add("META-004", "Medium", "settings", None, "",
                "public_key is empty; encryption at rest is not enabled (recommended whenever personal data are collected)")

    types = {r.get("type", "").split(" ")[0] for r in survey}
    missing = [m for m in ("start", "end") if m not in types]
    if missing:
        add("META-001", "Medium", "survey", None, "",
            f"No {'/'.join(missing)} timestamp field(s); interview duration cannot be computed")
    if "deviceid" not in types:
        add("META-002", "Low", "survey", None, "", "No deviceid field; device-level quality checks not possible")
    srow = settings[0] if settings else {}
    if not (srow.get("form_id") or srow.get("id_string")):
        add("META-003", "Medium", "settings", None, "", "No form_id set")
    ver = srow.get("version", "")
    if style_guide and ver and not re.fullmatch(r"\d{10}", ver):
        add("STYLE-002", "Low", "settings", None, "",
            f"version '{ver}' is not in yymmddhhmm form; Style Guide recommends a date-time version set by formula so each upload is greater than the last")
    if not srow.get("version"):
        add("META-003", "Low", "settings", None, "", "No version set; deployed versions cannot be told apart in the data")

    # Field counts for the shortest and longest path (bounds, repeats counted once)
    pstack, always, total, rep_total = [], 0, 0, 0
    for r in survey:
        t = re.sub(r"\s+", " ", r.get("type", "")).strip()
        tk = t.replace("_", " ") if t.startswith(("begin", "end")) else t
        if tk.startswith("begin"):
            pstack.append((tk == "begin repeat", bool(r.get("relevant", ""))))
        elif tk in ("end group", "end repeat"):
            if pstack:
                pstack.pop()
        elif r.get("name") and tk.split(" ")[0] not in NO_DATA:
            total += 1
            cond = any(x[1] for x in pstack) or bool(r.get("relevant", ""))
            always += 0 if cond else 1
            rep_total += 1 if any(x[0] for x in pstack) else 0

    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    findings.sort(key=lambda f: (order[f["severity"]], f["id"]))
    summary = {"data_questions": len(q_rows), "choice_lists": len(lists),
               "path": {"shortest_fields_always_shown": always, "longest_fields_all_shown": total,
                        "of_which_in_repeat_groups": rep_total},
               "languages": sorted(langs), "counts": dict(Counter(f["severity"] for f in findings)), "style_guide_checks": style_guide}
    print_out(findings, as_json, summary)


def check_value(add, row, n, v, val, t, lists, desc):
    if val == "":  # ${x} != '' is an "is answered" test, not a choice comparison
        return
    if t.startswith(("select_one", "select_multiple")) and len(t.split()) > 1:
        lst = t.split()[1]
        if lists.get(lst) and val not in {o.get("name", "") for o in lists[lst]}:
            add("LOGIC-004", "Critical", "survey", row, n,
                f"{desc}: '{val}' is not a value in list '{lst}'. Question is likely unreachable")


def print_out(findings, as_json, summary=None):
    full = "--full" in sys.argv
    if as_json:
        print(json.dumps({"summary": summary, "findings": findings}, indent=2))
        return
    if summary:
        p = summary.get("path", {})
        print(f"# {summary['data_questions']} data questions, {summary['choice_lists']} choice lists, "
              f"languages={summary['languages'] or 'single'}; counts={summary['counts']}")
        if p:
            print(f"# Path bounds (fields, repeats counted once): shortest ~{p['shortest_fields_always_shown']}, "
                  f"longest ~{p['longest_fields_all_shown']} ({p['of_which_in_repeat_groups']} inside repeat groups)")
    if summary and not summary.get("style_guide_checks"):
        print("# Style Guide checks not run (add --style-guide if the team follows the Impact Analytics SurveyCTO Style Guide)")
    if not findings:
        print("No mechanical findings.")
        return
    if full:
        for f in findings:
            print(f"{f['id']} | {f['severity']} | {f['location']} | {f['name']} | {f['evidence']}")
        return
    # Compact: one line per ID with a count and up to 3 examples (use --full for every finding)
    groups = {}
    for f in findings:
        groups.setdefault((f["id"], f["severity"]), []).append(f)
    for (fid, sev), items in sorted(groups.items(), key=lambda kv: ({"Critical": 0, "High": 1, "Medium": 2, "Low": 3}[kv[0][1]], kv[0][0])):
        ex = "; ".join(f"{i['location']} {i['name']}".strip() for i in items[:3])
        print(f"{fid} | {sev} | x{len(items)} | e.g. {ex} | {items[0]['evidence'][:140]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], "--json" in sys.argv, "--style-guide" in sys.argv)
