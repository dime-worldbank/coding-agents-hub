#!/usr/bin/env python3
"""Compare a paper questionnaire with a programmed XLSForm: flow, wording, choices, skip logic, constraints.

Usage: python compare_forms.py items.json form.xlsx [--lang English] [--out discrepancies.xlsx] [--calcs] [--list-langs]

items.json comes from extract_paper.py. Works for two kinds of paper:
  specification style (variable names and form expressions printed): matched by variable name first,
  then wording; skip logic, constraints and required flags are compared directly.
  respondent style (wording only): matched by wording in order; skip and range notes are listed to confirm.
Compares ONE language: the one the two files share. If several are shared, pass --lang (ask the team).
Every row is a candidate. Confirm in context before reporting.
"""
import re
import sys
import json
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment

NON_DATA = {"begin group", "end group", "begin repeat", "end repeat", "calculate", "calculate_here", "calculate here", "note",
            "start", "end", "today", "deviceid", "subscriberid", "simserial", "phonenumber", "username", "audit",
            "text audit", "speed violations list", "speed violations count", "caseid", "comments", "email", "hidden"}
STOP = set("the a an of to in is are you your do does did for and or".split())
TIME_WORDS = r"(day|days|week|weeks|month|months|year|years|hour|hours|today|yesterday|last|past|ago|ever|never|current|usual)"
PRE_RX = re.compile(r"(?:search|pulldata)\(\s*['\"]([^'\"]+)['\"]|jr://file(?:-csv)?/([^'\")\s]+)")
SKIP_WORDS = re.compile(r"\b(skip|go to|goto|if|only|ask|continue|end)\b", re.I)
RANGE_WORDS = re.compile(r"\b\d+\s*(?:-|to|\u2013)\s*\d+|between|at least|at most|no more than|minimum|maximum|must be|valid|range|\bmax\b|\bmin\b", re.I)


def hnorm(h):
    h = str(h or "").strip()
    if "::" in h:
        a, b = h.split("::", 1)
        return a.strip().lower().replace(" ", "_") + "::" + b.strip().lower()
    return h.lower().replace(" ", "_")


def base(t):
    parts = (t or "").replace("_", " ").split()
    if not parts:
        return ""
    return " ".join(parts[:2]) if parts[0] in ("begin", "end") and len(parts) > 1 else parts[0] if parts[0] not in ("select",) else " ".join(parts[:2])


def norm_text(s):
    s = re.sub(r"\$\{[^}]+\}", " ", s or "")
    s = re.sub(r"^\s*(?:Q\s?)?[A-Za-z]{0,3}\d+(?:\.\d+)*[a-z]?\s*[.):\-]?\s+", "", s)
    s = re.sub(r"^\s*(enumerator|interviewer)\s*:\s*", "", s, flags=re.I | re.M)
    s = re.sub(r"[^\w\s]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def pipes(s):
    return sorted(set(re.findall(r"\$\{([^}]+)\}", s or "")))


def toks(s):
    return set(s.split()) - STOP


def sim(a, b, ta, tb):
    if not a or not b:
        return 0.0
    u = ta | tb
    j = len(ta & tb) / len(u) if u else 0.0
    if j < 0.2 and a != b:
        return 0.0
    return 0.6 * SequenceMatcher(None, a, b).ratio() + 0.4 * j


def sig_tokens(s):
    t = norm_text(s)
    return (set(re.findall(r"\d+", t)), set(re.findall(TIME_WORDS, t)), set(re.findall(r"\b(not|never|no|none)\b", t)))


def split_and(expr):
    out, depth, cur, i = [], 0, "", 0
    expr = expr or ""
    while i < len(expr):
        ch = expr[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if depth == 0 and re.match(r"\s+and\s+", expr[i:], re.I):
            out.append(cur)
            cur = ""
            i += re.match(r"\s+and\s+", expr[i:], re.I).end()
            continue
        cur += ch
        i += 1
    out.append(cur)
    return [c for c in out if c.strip()]


def nexpr(e):
    s = (e or "").strip().replace('"', "'")
    s = re.sub(r"\s+", "", s)
    while s.startswith("(") and s.endswith(")") and s.count("(") == s.count(")") and "(" not in s[1:-1].replace("()", "") + ")" * 0 and False:
        s = s[1:-1]
    while len(s) > 2 and s[0] == "(" and s[-1] == ")" and _balanced(s[1:-1]):
        s = s[1:-1]
    return s


def _balanced(s):
    d = 0
    for ch in s:
        d += ch == "("
        d -= ch == ")"
        if d < 0:
            return False
    return d == 0


def conj_set(parts):
    out = set()
    for p in parts:
        for c in split_and(p):
            out.add(nexpr(c))
    return out


def readable(e):
    s = e or ""
    s = re.sub(r"selected\(\s*\$\{([^}]+)\}\s*,\s*'?([^')]+)'?\s*\)", r"\1 includes \2", s)
    s = re.sub(r"\$\{([^}]+)\}", r"\1", s)
    s = s.replace("!=", " is not ").replace(">=", " at least ").replace("<=", " at most ")
    s = re.sub(r"(?<![<>!])=", " is ", s)
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- form
def load_form(path, lang):
    wb = load_workbook(path, data_only=True)
    ws = wb["survey"]
    rows = [[("" if v is None else str(v).strip()) for v in r] for r in ws.iter_rows(values_only=True)]
    hdr = [hnorm(h) for h in rows[0]]
    langs = sorted({h.split("::", 1)[1] for h in hdr if h.startswith("label::") and h.split("::", 1)[1] != "stata"})

    def col(prefix):
        for want in (f"{prefix}::{lang.lower()}" if lang else None, prefix):
            if want and want in hdr:
                return hdr.index(want)
        return next((i for i, h in enumerate(hdr) if h.startswith(prefix + "::") and "stata" not in h), None)

    c = {k: col(k) for k in ("label", "hint", "constraint_message")}
    idx = {k: (hdr.index(k) if k in hdr else None) for k in ("type", "name", "relevance", "relevant", "constraint", "required",
                                                             "appearance", "choice_filter", "calculation", "question_number",
                                                             "repeat_count", "default")}

    def g(r, k):
        i = idx.get(k) if k in idx else c.get(k)
        return r[i] if i is not None and i < len(r) else ""

    fields, notes, calcs, stack, pre = [], [], {}, [], defaultdict(list)
    for n, r in enumerate(rows[1:], start=2):
        if not any(r):
            continue
        t, name = g(r, "type"), g(r, "name")
        b = base(t)
        rel = g(r, "relevance") or g(r, "relevant")
        for cell in r:
            for m in PRE_RX.finditer(cell):
                pre[m.group(1) or m.group(2)].append((name, n))
        if b in ("select one from file", "select multiple from file", "select one external") and len(t.split()) > 1:
            pre[t.split()[1]].append((name, n))
        if b in ("begin group", "begin repeat"):
            stack.append({"name": name, "rel": rel, "label": g(r, "label") or name, "row": n})
            continue
        if b in ("end group", "end repeat"):
            if stack:
                stack.pop()
            continue
        eff = [s["rel"] for s in stack if s["rel"]]
        module = (stack[0]["label"] if stack else "(top level)")
        if b.startswith("calculate"):
            calcs[name] = {"row": n, "calculation": g(r, "calculation"), "rel": rel, "eff": eff}
            continue
        if b == "note":
            notes.append({"row": n, "name": name, "label": g(r, "label"), "module": module})
            continue
        if b in NON_DATA or b.startswith(("sensor", "speed")) or not name:
            continue
        label = g(r, "label")
        parts = t.split()
        num = g(r, "question_number") or (re.match(r"^\s*((?:[A-Za-z]{1,3})?\d+(?:\.\d+)*[a-z]?)\b", label) or [None, ""])[1]
        fields.append({"row": n, "name": name, "type": t, "base": b, "list": parts[1] if len(parts) > 1 else "",
                       "label": label, "rel": rel, "eff": eff + ([rel] if rel else []), "constraint": g(r, "constraint"),
                       "cmsg": g(r, "constraint_message"), "required": g(r, "required").lower() in ("yes", "true", "1"),
                       "appearance": g(r, "appearance"), "choice_filter": g(r, "choice_filter"), "number": num, "module": module})
    lists = defaultdict(list)
    if "choices" in wb.sheetnames:
        cr = [[("" if v is None else str(v).strip()) for v in r] for r in wb["choices"].iter_rows(values_only=True)]
        ch = [hnorm(h) for h in cr[0]]
        li = ch.index("list_name") if "list_name" in ch else None
        vi = ch.index("value") if "value" in ch else (ch.index("name") if "name" in ch else None)
        fi = ch.index("filter") if "filter" in ch else None
        lab = None
        for want in ((f"label::{lang.lower()}" if lang else None), "label"):
            if want and want in ch:
                lab = ch.index(want)
                break
        if lab is None:
            lab = next((i for i, h in enumerate(ch) if h.startswith("label::") and "stata" not in h), None)
        for r in cr[1:]:
            if li is not None and vi is not None and r[li]:
                lists[r[li]].append({"value": r[vi], "label": r[lab] if lab is not None else "", "filter": r[fi] if fi is not None and fi < len(r) else ""})
    return {"fields": fields, "notes": notes, "calcs": calcs, "lists": lists, "langs": langs, "pre": pre}


# ---------------------------------------------------------------- matching
def wording_dp(P, F, pi, fi, thr=0.55):
    """Order-preserving weighted alignment of paper indices pi with form indices fi. Returns list of (p, f)."""
    n, m = len(pi), len(fi)
    S = [[0.0] * m for _ in range(n)]
    for a in range(n):
        for b in range(m):
            S[a][b] = sim(P[pi[a]]["_n"], F[fi[b]]["_n"], P[pi[a]]["_t"], F[fi[b]]["_t"])
    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    for a in range(1, n + 1):
        for b in range(1, m + 1):
            best = max(dp[a - 1][b], dp[a][b - 1])
            if S[a - 1][b - 1] >= thr:
                best = max(best, dp[a - 1][b - 1] + S[a - 1][b - 1])
            dp[a][b] = best
    out, a, b = [], n, m
    while a > 0 and b > 0:
        if S[a - 1][b - 1] >= thr and abs(dp[a][b] - (dp[a - 1][b - 1] + S[a - 1][b - 1])) < 1e-9:
            out.append((pi[a - 1], fi[b - 1]))
            a -= 1
            b -= 1
        elif dp[a - 1][b] >= dp[a][b - 1]:
            a -= 1
        else:
            b -= 1
    return out[::-1]


def lis_keep(pairs):
    """pairs sorted by paper index; keep the longest run with increasing form index. Returns set of pairs kept."""
    import bisect
    tails, tail_idx, prev = [], [], [-1] * len(pairs)
    for k, (_, f) in enumerate(pairs):
        pos = bisect.bisect_left(tails, f)
        if pos == len(tails):
            tails.append(f)
            tail_idx.append(k)
        else:
            tails[pos], tail_idx[pos] = f, k
        prev[k] = tail_idx[pos - 1] if pos > 0 else -1
    keep, k = set(), tail_idx[-1] if tail_idx else -1
    while k >= 0:
        keep.add(pairs[k])
        k = prev[k]
    return keep


def tcat(t):
    return {"integer": "number", "decimal": "number", "string": "text"}.get(t, t)


def compare(items_path, form_path, lang, calcs_on=False):
    data = json.load(open(items_path))
    form = load_form(form_path, lang)
    P = [i for i in data["items"] if i["kind"] == "question"]
    scripts = [i for i in data["items"] if i["kind"] == "script"]
    F = form["fields"]
    for p in P:
        p["_n"], p["_t"] = norm_text(p["text"]), toks(norm_text(p["text"]))
    for f in F:
        f["_n"], f["_t"] = norm_text(f["label"]), toks(norm_text(f["label"]))
    spec = sum(1 for p in P if p.get("name")) >= max(3, 0.5 * len(P))
    pairs = []
    if spec:
        by_name = {f["name"].lower(): k for k, f in enumerate(F)}
        used = set()
        for a, p in enumerate(P):
            k = by_name.get((p.get("name") or "").lower())
            if k is not None and k not in used:
                pairs.append((a, k))
                used.add(k)
        left_p = [a for a in range(len(P)) if a not in {x for x, _ in pairs}]
        left_f = [k for k in range(len(F)) if k not in used]
        pairs += wording_dp(P, F, left_p, left_f, 0.7)
    else:
        pairs = wording_dp(P, F, list(range(len(P))), list(range(len(F))))
    # second pass: leftovers matched by wording alone, ignoring order (these are moved questions)
    mp, mf = {a for a, _ in pairs}, {k for _, k in pairs}
    cand = sorted(((sim(P[a]["_n"], F[k]["_n"], P[a]["_t"], F[k]["_t"]), a, k)
                   for a in range(len(P)) if a not in mp for k in range(len(F)) if k not in mf), reverse=True)
    for sc, a, k in cand:
        if sc < (0.7 if spec else 0.6):
            break
        if a not in mp and k not in mf:
            pairs.append((a, k))
            mp.add(a)
            mf.add(k)
    pairs.sort()
    matched_p, matched_f = {a for a, _ in pairs}, {k for _, k in pairs}
    keep = lis_keep(pairs) if pairs else set()
    rows, skip_rows, cons_rows = [], [], []

    def add(sec, check, conf, p, f, diff, pv, fv, sug):
        rows.append([sec, check, conf, (p or {}).get("number") or "", (f or {}).get("row") or "", (f or {}).get("name") or (p or {}).get("name") or "",
                     diff, pv, fv, sug])

    for a, k in pairs:
        p, f = P[a], F[k]
        sec = p["section"]
        if (a, k) not in keep:
            add(sec, "Order differs", "Medium", p, f, "Question sits in a different position relative to its neighbours", p["text"][:150], f["label"][:150], "Confirm the intended order and align the two versions")
        if spec and p.get("name") and p["name"].lower() != f["name"].lower():
            add(sec, "Variable name differs", "Medium", p, f, f"paper {p['name']} vs form {f['name']}", p["name"], f["name"], "Confirm which name is correct")
        if p["_n"] != f["_n"]:
            ps, fs = sig_tokens(p["text"]), sig_tokens(f["label"])
            r = SequenceMatcher(None, p["_n"], f["_n"]).ratio()
            if ps != fs:
                d = "; ".join(f"{nm} paper {sorted(x)} vs form {sorted(y)}" for nm, x, y in zip(("numbers", "time words", "negation"), ps, fs) if x != y)
                add(sec, "Wording differs: possible change in meaning", "High", p, f, d, p["text"][:200], f["label"][:200], "Check meaning; align the wording")
            elif r >= 0.9:
                add(sec, "Minor wording difference", "Low", p, f, f"Similarity {r:.2f}", p["text"][:200], f["label"][:200], "Align or accept")
            else:
                add(sec, "Wording differs", "Medium", p, f, f"Similarity {r:.2f}", p["text"][:200], f["label"][:200], "Align the wording")
        if pipes(p["text"]) != pipes(f["label"]) and spec:
            add(sec, "Piped value differs", "Medium", p, f, f"paper {pipes(p['text'])} vs form {pipes(f['label'])}", "", "", "Check which answers the text shows")
        pn, fnum = (p.get("number") or "").upper().lstrip("Q"), (f.get("number") or "").upper().lstrip("Q")
        if pn and fnum and pn != fnum:
            add(sec, "Question number differs", "Low", p, f, f"paper {p['number']} vs form {f['number']}", p["number"], f["number"], "Renumber or confirm it is deliberate")
        # type
        if spec and p.get("qtype"):
            if tcat(base(p["qtype"])) != tcat(f["base"]):
                add(sec, "Type differs", "Medium", p, f, f"paper {p['qtype']} vs form {f['base']}", p["qtype"], f["base"], "Confirm the field type")
            elif p.get("list_name") and f["list"] and p["list_name"] != f["list"] and not p.get("choice_file"):
                add(sec, "Choice list differs", "Medium", p, f, f"paper list {p['list_name']} vs form list {f['list']}", p["list_name"], f["list"], "Confirm the list")
        else:
            rt = p.get("response_type")
            if rt in ("numeric", "number", "integer") and tcat(f["base"]) == "text":
                add(sec, "Type differs", "Medium", p, f, "Paper expects a number; form is text", rt, f["base"], "Use a numeric field")
            if re.search(r"select all|all that apply", p["text"], re.I) and f["base"] == "select one":
                add(sec, "Type differs", "Medium", p, f, "Paper says select all that apply; form is select_one", "select all", f["base"], "Use select_multiple")
        # choices
        if f["base"] in ("select one", "select multiple"):
            fo = form["lists"].get(f["list"], [])
            if p.get("choice_file"):
                pass  # preload list: reported on the Preload files sheet
            elif p["choices"]:
                pl = [(c["code"] or "", norm_text(c["label"])) for c in p["choices"]]
                fl = [(o["value"], norm_text(o["label"])) for o in fo]
                pset, fset = {x[1] for x in pl}, {x[1] for x in fl}
                only_p, only_f = sorted(pset - fset), sorted(fset - pset)
                if only_p or only_f:
                    d = "; ".join(x for x in ((f"on paper only: {', '.join(only_p)}" if only_p else ""), (f"in form only: {', '.join(only_f)}" if only_f else "")) if x)
                    add(sec, "Choices differ", "High", p, f, d, "; ".join(f"{c}={l}" for c, l in pl)[:200], "; ".join(f"{c}={l}" for c, l in fl)[:200], "Add or remove the option, or confirm it is deliberate")
                else:
                    pc, fc = {l: c for c, l in pl}, {l: c for c, l in fl}
                    bad = [(l, pc[l], fc[l]) for l in pc if pc[l] and fc.get(l) and pc[l] != fc[l]]
                    if bad:
                        add(sec, "Choice codes differ", "Medium", p, f, "; ".join(f"{l}: paper {a} vs form {b}" for l, a, b in bad[:4]), "", "", "Align the codes; check skip logic that uses them")
                    elif [l for _, l in pl] != [l for _, l in fl]:
                        add(sec, "Choice order differs", "Low", p, f, "Same options in a different order", "", "", "Align the order")
            elif spec:
                add(sec, "Choices missing on paper", "Medium", p, f, "Form has a choice list; none is printed on paper", "", f["list"], "Add the options to the paper version")
        # skip logic and constraints
        if spec:
            pe = list(p.get("group_relevance") or []) + ([p["relevance"]] if p.get("relevance") else [])
            if conj_set(pe) != conj_set(f["eff"]):
                kind = "Skip logic: on form only" if not pe else "Skip logic: on paper only" if not f["eff"] else "Skip logic differs"
                add(sec, kind, "High", p, f, "Effective conditions (group plus question) do not match",
                    readable(" AND ".join(pe)), readable(" AND ".join(f["eff"])), "Check both route the same respondents")
            if nexpr(p.get("constraint")) != nexpr(f["constraint"]):
                add(sec, "Constraint differs", "High", p, f, "paper vs form constraint expressions differ", p.get("constraint", ""), f["constraint"], "Confirm the valid range or rule")
            elif p.get("constraint_message") and f["cmsg"] and norm_text(p["constraint_message"]) != norm_text(f["cmsg"]):
                add(sec, "Constraint message differs", "Low", p, f, "Message wording differs", p["constraint_message"][:150], f["cmsg"][:150], "Align the message")
            if bool(p.get("required")) != bool(f["required"]):
                add(sec, "Required differs", "Medium", p, f, f"paper required={bool(p.get('required'))} vs form required={f['required']}", "", "", "Confirm whether the question must be answered")
            if (p.get("appearance") or "").strip() != (f["appearance"] or "").strip():
                add(sec, "Appearance differs", "Low", p, f, "", p.get("appearance", ""), f["appearance"], "Confirm the display setting")
        else:
            note = p.get("notes", "")
            if (note and SKIP_WORDS.search(note)) or f["eff"]:
                skip_rows.append([sec, p["number"] or "", f["row"], note, readable(" AND ".join(f["eff"]))])
            if (note and RANGE_WORDS.search(note)) or f["constraint"]:
                cons_rows.append([sec, p["number"] or "", f["row"], note if RANGE_WORDS.search(note or "") else "", f["constraint"], f["required"]])
    for a, p in enumerate(P):
        if a not in matched_p:
            add(p["section"], "On paper, not in form", "High", p, None, "No form question has similar wording" + ("" if not p.get("name") else f" and no field named {p['name']}"), p["text"][:200], "", "Add the question to the form or confirm it was dropped")
    for k, f in enumerate(F):
        if k not in matched_f and f["label"].strip():
            add(f["module"], "In form, not on paper", "High", None, f, f"Field '{f['name']}' has no paper counterpart", "", f["label"][:200], "Add the question to the paper version or confirm it is internal")
    # consent and notes
    fnotes = [(norm_text(n["label"]), n) for n in form["notes"] if n["label"]]
    for s in scripts:
        st = norm_text(s["text"])
        if len(st) < 80 or not fnotes:
            continue
        named = next((n for _, n in fnotes if s.get("name") and n["name"].lower() == s["name"].lower()), None)
        bs, bn = max(((SequenceMatcher(None, st, ft).ratio(), n) for ft, n in fnotes), key=lambda x: x[0])
        if named:
            bs, bn = SequenceMatcher(None, st, norm_text(named["label"])).ratio(), named
        if bs < 0.97:
            add(s["section"], "Paper text block differs from form note", "Medium" if bs > 0.5 else "Low", s, {"row": bn["row"], "name": bn["name"]},
                f"Best similarity {bs:.2f}", s["text"][:200], bn["label"][:200], "Compare the consent or introduction wording line by line")
    # calculate fields (optional)
    if calcs_on:
        for c in [i for i in data["items"] if i["kind"] == "calculate"]:
            fc = form["calcs"].get(c["name"])
            if not fc:
                add("(calculate fields)", "On paper, not in form", "High", c, None, f"Calculate field {c['name']} not found", c.get("calculation", "")[:200], "", "Add or confirm")
            elif nexpr(c.get("calculation")) != nexpr(fc["calculation"]):
                add("(calculate fields)", "Calculation differs", "Medium", c, {"row": fc["row"], "name": c["name"]}, "Expressions differ", c.get("calculation", "")[:200], fc["calculation"][:200], "Confirm the formula")
    # preload files
    pre_rows = []
    stem = lambda x: re.sub(r"\.csv$", "", x.lower())
    paper_files = {stem(p["choice_file"]): p["choice_file"] for p in P if p.get("choice_file")}
    form_files = {stem(k): k for k in form["pre"]}
    miss_f = [(st, fn) for st, fn in form_files.items() if paper_files and st not in paper_files]
    miss_p = [(st, fn) for st, fn in paper_files.items() if st not in form_files]
    for st, fn in form_files.items():
        uses = form["pre"][fn]
        pre_rows.append([fn, ", ".join(sorted({u[0] for u in uses if u[0]}))[:120], "on paper" if st in paper_files else "not named on paper", "Ask the team to share this file"])
    for st, fn in miss_p:
        if not any(st == x for x, _ in miss_f):
            pre_rows.append([fn, "", "on paper only", "Paper names a file the form does not use"])
    for i in range(max(len(miss_f), len(miss_p))):
        pf = miss_p[i][1] if i < len(miss_p) else ""
        ff = miss_f[i][1] if i < len(miss_f) else ""
        uses = form["pre"][ff] if ff else [("", None)]
        add("(preload files)", "Preload file differs", "Medium", None, {"row": uses[0][1], "name": uses[0][0]},
            f"Paper names {pf or 'no file'}; form uses {ff or 'no file'}", pf, ff, "Confirm the source of the list and share the file")
    # flow summary by paper section
    flow = []
    secs = []
    for p in P:
        if p["section"] not in secs:
            secs.append(p["section"])
    for s in secs:
        idx = [a for a, p in enumerate(P) if p["section"] == s]
        m = [a for a in idx if a in matched_p]
        inorder = [a for a in m if next(pr for pr in pairs if pr[0] == a) in keep]
        flow.append([s, len(idx), len(m), len(inorder), len(m) - len(inorder), len(idx) - len(m)])
    form_only = defaultdict(int)
    for k, f in enumerate(F):
        if k not in matched_f and f["label"].strip():
            form_only[f["module"]] += 1
    summary = {"paper_q": len(P), "form_q": len(F), "matched": len(pairs), "mode": "variable names then wording" if spec else "wording and order",
               "lang": lang, "flow": flow, "form_only": dict(form_only), "form_langs": form["langs"], "warnings": data.get("warnings", [])}
    return rows, skip_rows, cons_rows, pre_rows, summary


HDR = ["Section", "Check", "Confidence", "Paper no.", "Form row", "Variable", "Difference", "Paper", "Form", "Suggested response"]


def write_xlsx(path, rows, skip_rows, cons_rows, pre_rows, s):
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    ws.append(["Paper questions read", s["paper_q"]])
    ws.append(["Form questions read", s["form_q"]])
    ws.append(["Matched", s["matched"]])
    ws.append(["Matching method", s["mode"]])
    ws.append(["Language compared", s["lang"]])
    ws.append([])
    ws.append(["Flow by section", "Paper questions", "Matched", "In same order", "Moved", "Not in form"])
    for r in s["flow"]:
        ws.append(r)
    ws.append([])
    ws.append(["Form fields with no paper match, by form module", ""])
    for k, v in s["form_only"].items():
        ws.append([k, v])
    ws.append([])
    ws.append(["Not checked: calculate fields (unless --calcs), metadata fields, notes other than consent or introduction text, "
               "contents of preload files, and every language other than the one compared."])
    for c in ws[7]:
        c.font = Font(bold=True)
    ws.column_dimensions["A"].width = 52
    d = wb.create_sheet("Discrepancies")
    d.append(HDR)
    order = {"High": 0, "Medium": 1, "Low": 2}
    secs = [x[0] for x in s["flow"]]
    for r in sorted(rows, key=lambda r: (secs.index(r[0]) if r[0] in secs else 99, order[r[2]])):
        d.append(r)
    fill = {"High": "F8CBAD", "Medium": "FFE699", "Low": "E2EFDA"}
    for row in d.iter_rows(min_row=2):
        row[2].fill = PatternFill("solid", fgColor=fill[row[2].value])
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    for c in d[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="D9D9D9")
    for i, w in enumerate([22, 30, 11, 9, 9, 22, 45, 45, 45, 38]):
        d.column_dimensions[chr(65 + i)].width = w
    d.freeze_panes = "A2"
    for name, head, data in (("Skip logic to confirm", ["Section", "Paper no.", "Form row", "Paper skip note", "Form condition (plain)"], skip_rows),
                             ("Constraints to confirm", ["Section", "Paper no.", "Form row", "Paper range or rule", "Form constraint", "Form required"], cons_rows),
                             ("Preload files", ["File", "Used by", "On paper?", "Action"], pre_rows)):
        w = wb.create_sheet(name)
        w.append(head)
        for r in data:
            w.append(r)
        for c in w[1]:
            c.font = Font(bold=True)
        for i in range(len(head)):
            w.column_dimensions[chr(65 + i)].width = 40
        for row in w.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def main(items_path, form_path, lang, out, calcs, list_langs):
    data = json.load(open(items_path))
    langs = load_form(form_path, None)["langs"]
    guess = (data.get("language_guess") or {}).get("guess", "unknown")
    common = [l for l in langs if l.lower() == guess.lower()]
    if list_langs or lang is None:
        print(f"Form languages: {langs or ['(single, no label:: columns)']}. Paper language guess: {guess}.")
        if list_langs:
            return
        if len(langs) <= 1:
            lang = langs[0] if langs else ""
        elif len(common) == 1:
            lang = common[0]
            print(f"Using the language both files share: {lang}")
        else:
            print(f"ASK THE TEAM: which language should be compared? Options: {', '.join(langs)}")
            sys.exit(3)
    rows, skip_rows, cons_rows, pre_rows, s = compare(items_path, form_path, lang, calcs)
    out = out or "discrepancies.xlsx"
    write_xlsx(out, rows, skip_rows, cons_rows, pre_rows, s)
    hi = sum(1 for r in rows if r[2] == "High")
    print(f"Paper questions read: {s['paper_q']}. Form questions read: {s['form_q']}. Matched: {s['matched']}. Method: {s['mode']}. Language: {lang or 'single'}.")
    print(f"Discrepancies: {len(rows)} (High {hi}, Medium {sum(1 for r in rows if r[2]=='Medium')}, Low {sum(1 for r in rows if r[2]=='Low')}). "
          f"Skip logic notes to confirm: {len(skip_rows)}. Constraint notes to confirm: {len(cons_rows)}. Preload files: {len(pre_rows)}.")
    for sec, n, m, io, mv, nf in s["flow"]:
        print(f"Flow | {sec}: {n} on paper, {m} matched, {io} in the same order, {mv} moved, {nf} not in form")
    for r in rows:
        if r[2] == "High":
            print(f"High | {r[1]} | paper {r[3] or '-'} | row {r[4] or '-'} | {r[5]} | {r[6][:90]}")
    print(f"Wrote {out}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    a = sys.argv
    get = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    main(a[1], a[2], get("--lang"), get("--out"), "--calcs" in a, "--list-langs" in a)
