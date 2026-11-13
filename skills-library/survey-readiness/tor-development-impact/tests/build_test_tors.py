#!/usr/bin/env python3
"""Fill the template with invented values (tor-filled-ok.md) and plant errors (tor-broken.md).
Run from this folder: python build_test_tors.py"""
import re
from pathlib import Path

HERE = Path(__file__).parent
tpl = (HERE.parent / "assets" / "tor-template.md").read_text(encoding="utf-8")
body = tpl.split("END OF INSTRUCTIONS:", 1)[1].split("-->", 1)[1]
lines = [l for l in body.splitlines() if "[[OPTIONAL" not in l and not l.startswith("> Drafting note")]
text = "\n".join(lines)
dates = iter(["Oct 24, 2026", "Oct 24, 2026", "Nov 1, 2026", "Oct 24, 2026", "Oct 24, 2026", "Nov 1, 2026", "Nov 1, 2026", "Jan 10, 2027", "Jan 10, 2027", "Jan 10, 2027"])
months = iter(["November 2026", "November 2026", "November 2026", "February 2027", "March 2027"])


def fill(m):
    s = m.group(1)
    if re.fullmatch(r"\d+(\.\d+)?", s) or re.fullmatch(r"\d+\s*(to|\u2013|-)\s*\d+", s):
        return s
    if s.startswith("date"):
        return next(dates)
    if s == "month and year":
        return next(months)
    return {"unit": "school", "units": "schools"}.get(s, "Sample value")


ok = re.sub(r"\[\[(.+?)\]\]", fill, text)
(HERE / "tor-filled-ok.md").write_text(ok, encoding="utf-8")
b = ok
b = re.sub(r"\n## 8\. Ethical Provisions\n.*?(?=\n## 9\.)", "\n", b, flags=re.S)                 # ethics section removed
b = b.replace("| On approval of deliverables for Activities 3\u20134 | 25% |", "| On approval of deliverables for Activities 3\u20134 | 20% |")  # payment adds to 95
b = re.sub(r"(?m)^\| 5 \|.*\n(\|  \|.*\n){3}", "", b)                                                  # no deliverables for Activity 5
b = b.replace("| 1.1 Strong capacity and experience in implementing large surveys, preferably in Sample value, especially in the study regions, and in Sample value | 20 |",
              "| 1.1 Strong capacity and experience in implementing large surveys, preferably in Sample value, especially in the study regions, and in Sample value | 25 |")
b = re.sub(r"(\(c\) Final roster[^\n]*?\| )Nov 1, 2026", r"\1Mar 15, 2027", b)                      # late deliverable
b = b.replace("The contract will end in March 2027", "The contract will end in January 2027")
b += "\nStray placeholder: [[to be confirmed]]\n"
(HERE / "tor-broken.md").write_text(b, encoding="utf-8")
print("built tor-filled-ok.md and tor-broken.md")
