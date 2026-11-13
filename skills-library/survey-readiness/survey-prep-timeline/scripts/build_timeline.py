#!/usr/bin/env python3
"""Schedule survey preparation steps backward from a start of data collection, or forward from today.

Usage: python build_timeline.py plan.json [--mode backward|forward] [--md schedule.md] [--today YYYY-MM-DD]

plan.json:
{"anchor_step": "S19", "anchor_date": "2027-03-01", "from_date": "2026-11-16",
 "steps": [{"id": "S01", "name": "...", "owner": "...", "weeks": 4, "after": ["S00"], "done": false, "done_date": "2026-10-01",
            "field": false}],
 "blackouts": [{"name": "Rainy season", "from": "2027-01-10", "to": "2027-03-20"}]}

Date arithmetic only. Output is a Markdown table (printed, and written with --md). For Excel, convert the
Markdown with the xlsx skill. Durations come from the team (see references/steps.md for suggested ranges to confirm).
backward: latest start and finish of each step so data collection starts on anchor_date, and the shortfall if today is too late.
forward: earliest start and finish from from_date, and the earliest possible start of data collection.
"""
import sys
import json
from datetime import date, timedelta
from pathlib import Path


def d(s):
    return date.fromisoformat(s) if s else None


def topo(steps):
    order, seen, tmp = [], set(), set()
    byid = {s["id"]: s for s in steps}

    def visit(i):
        if i in seen:
            return
        if i in tmp:
            raise SystemExit(f"Circular dependency at {i}")
        tmp.add(i)
        for p in byid[i].get("after", []):
            if p not in byid:
                raise SystemExit(f"Step {i} comes after unknown step {p}")
            visit(p)
        tmp.discard(i)
        seen.add(i)
        order.append(i)
    for s in steps:
        visit(s["id"])
    return order, byid


def schedule(plan, mode, today):
    steps = plan["steps"]
    order, byid = topo(steps)
    succ = {i: [] for i in byid}
    for s in steps:
        for p in s.get("after", []):
            succ[p].append(s["id"])
    anchor = plan.get("anchor_step") or order[-1]
    out = {}
    if mode == "backward":
        end_by = d(plan["anchor_date"])
        for i in reversed(order):
            s = byid[i]
            if i == anchor:
                out[i] = {"start": end_by, "end": end_by}
                continue
            nxt = [out[x]["start"] for x in succ[i] if x in out]
            fin = min(nxt) if nxt else end_by
            out[i] = {"end": fin, "start": fin - timedelta(weeks=s.get("weeks", 0))}
    else:
        base = d(plan.get("from_date")) or today
        for i in order:
            s = byid[i]
            if s.get("done"):
                e = d(s.get("done_date")) or base
                out[i] = {"start": e, "end": e}
                continue
            prev = [out[p]["end"] for p in s.get("after", [])]
            st = max(prev + [base])
            out[i] = {"start": st, "end": st + timedelta(weeks=s.get("weeks", 0))}
        out[anchor]["start"] = out[anchor]["end"] = max([out[p]["end"] for p in byid[anchor].get("after", [])] + [base])
    return order, byid, out, anchor


def flags(plan, order, byid, out, anchor, mode, today):
    notes = {i: [] for i in order}
    for i in order:
        s = byid[i]
        if not s.get("owner"):
            notes[i].append("no owner")
        if s.get("done"):
            notes[i].append("done")
            continue
        if mode == "backward" and out[i]["start"] < today and i != anchor:
            notes[i].append(f"latest start is {(today - out[i]['start']).days} days before today")
        for b in plan.get("blackouts", []):
            if (s.get("field") or i == anchor) and out[i]["start"] <= d(b["to"]) and out[i]["end"] >= d(b["from"]):
                notes[i].append(f"overlaps {b['name']}")
    return notes


def main(path, mode, md, today):
    plan = json.load(open(path))
    order, byid, out, anchor = schedule(plan, mode, today)
    notes = flags(plan, order, byid, out, anchor, mode, today)
    if mode == "backward":
        first = min(out[i]["start"] for i in order if not byid[i].get("done"))
        short = (today - first).days
        print(f"# Backward plan. Data collection starts {plan['anchor_date']}. Earliest step must start {first}"
              + (f", which is {short} days before today ({today}): the plan does not fit by about {short // 7} weeks" if short > 0 else f" ({(first - today).days} days from today)"))
    else:
        print(f"# Forward plan from {plan.get('from_date') or today}. Earliest possible start of data collection: {out[anchor]['start']}")
        if plan.get("anchor_date"):
            gap = (d(plan["anchor_date"]) - out[anchor]["start"]).days
            print(f"# Target {plan['anchor_date']}: " + (f"{gap} days of slack" if gap >= 0 else f"{-gap} days too late"))
    head = ["ID", "Step", "Owner", "Weeks", "Start", "End", "Notes"]
    table = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for i in sorted(order, key=lambda k: (out[k]["start"], out[k]["end"])):
        s = byid[i]
        table.append("| " + " | ".join(str(x).replace("|", "/") for x in [i, s["name"], s.get("owner", ""), s.get("weeks", ""), out[i]["start"], out[i]["end"], "; ".join(notes[i])]) + " |")
    print("\n".join(table))
    if md:
        Path(md).write_text("\n".join(table) + "\n", encoding="utf-8")
        print(f"Wrote {md}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    a = sys.argv
    get = lambda k, dv=None: a[a.index(k) + 1] if k in a else dv
    main(a[1], get("--mode", "backward"), get("--md"), d(get("--today")) or date.today())
