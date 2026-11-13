#!/usr/bin/env python3
"""Create, show, and check the project brief shared by the survey skills.

Usage: python brief.py init [project-brief.md]   write a blank brief
       python brief.py check [project-brief.md]  list missing or invalid fields
       python brief.py show [project-brief.md]   print the fields that are filled

The brief is a short list of "key: value" lines. Blank means the team has not said. Never fill a blank by guessing.
"""
import re
import sys
from datetime import date
from pathlib import Path

FIELDS = [("survey_name", None), ("country", None),
          ("survey_type", {"household", "school", "phone", "facility", "firm", "panel follow-up", "records retrieval", "other"}),
          ("mode", {"tablet", "paper", "phone"}), ("instrument", {"new", "adapted", "follow-up"}),
          ("executed_by", {"world bank", "government", "other", "not applicable"}), ("firm_hired", {"yes", "no"}),
          ("units", None), ("respondents", None), ("sample_size", None), ("languages", None),
          ("platform", {"surveycto", "odk", "kobo", "other"}), ("data_collection_start", "date"), ("data_collection_end", "date"),
          ("panel", {"yes", "no"}), ("style_guide", {"yes", "no"}), ("files", None), ("updated", None)]
PII = re.compile(r"\+?\d[\d\s().-]{8,}|@[\w.-]+\.\w+")


def read(path):
    vals = {}
    for l in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", l)
        if m:
            vals[m.group(1)] = m.group(2).strip()
    return vals


def main(cmd, path):
    if cmd == "init":
        if Path(path).exists():
            sys.exit(f"{path} already exists. Not overwritten.")
        Path(path).write_text("# Project brief\n" + "".join(f"{k}:\n" for k, _ in FIELDS), encoding="utf-8")
        print(f"Wrote {path}")
        return
    v = read(path)
    if cmd == "show":
        for k, _ in FIELDS:
            if v.get(k):
                print(f"{k}: {v[k]}")
        return
    bad = []
    for k, rule in FIELDS:
        val = v.get(k, "")
        if not val:
            bad.append(("EMPTY", k, "not given yet"))
        elif rule == "date":
            try:
                date.fromisoformat(val)
            except ValueError:
                bad.append(("INVALID", k, f"'{val}' is not YYYY-MM-DD"))
        elif isinstance(rule, set) and val.lower() not in rule:
            bad.append(("INVALID", k, f"'{val}' is not one of {sorted(rule)}"))
        if val and PII.search(val):
            bad.append(("PRIVACY", k, "looks like a phone number or email. Remove it"))
    unknown = [k for k in v if k not in dict(FIELDS)]
    for k in unknown:
        bad.append(("UNKNOWN", k, "not a brief field"))
    s, e = v.get("data_collection_start"), v.get("data_collection_end")
    try:
        if s and e and date.fromisoformat(e) < date.fromisoformat(s):
            bad.append(("INVALID", "data_collection_end", "is before the start"))
    except ValueError:
        pass
    print(f"# {path}: {len(FIELDS) - sum(1 for k, _ in FIELDS if not v.get(k))} of {len(FIELDS)} fields filled")
    for s_, k, d in bad:
        print(f"{s_:8} | {k} | {d}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("init", "check", "show"):
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "project-brief.md")
