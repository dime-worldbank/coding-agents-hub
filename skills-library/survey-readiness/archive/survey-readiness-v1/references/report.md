# Report format

Write in short sentences, about 20 words or fewer. Be clear, a little fuller than a bare note, never long.
Do not show finding IDs, "Escalate" tags, or severity words like Blocker. Use the three tiers below.
Cite sources by short page name, for example "Development Impact Wiki: Survey Pilot".

## Header

Project, areas reviewed, stage, and files reviewed (one line each).

## Verdicts

One line per area: Not ready, Ready with fixes, Ready, or Not assessable.
Add: "Verdicts cover only the files reviewed and are not an approval."

## Findings (one block per area)

```
### <Area>: <Verdict>

**Mandatory** (fix before fieldwork)
- <What is wrong>. <Where>. Fix: <short fix>.

**Priority** (likely to hurt data quality or cause rework)
- ...

**Suggested** (worth considering)
- ...
```

- **Key changes (default):** show Mandatory and Priority only. End with "N suggested items not shown. Ask for the full review to see them."
- **Full review (on request):** show all three. Add one short "Why:" sentence to Mandatory and Priority items, and a source.
- Order items by importance. Merge repeated instances into one item with example rows.
- Use `Possible:` when the files do not settle the point.
- If a tier is empty, write "None."

### Ethics and data security

Split each tier into two labelled groups:
- *Needed for approvals* (ethics board, privacy office).
- *To do in the field.*

### Points that rest on a stated rule

For the single-source threshold and privacy office approval, write "The guidance used here says…".
Do not present them as verified requirements.

## Also include

- **Not assessable:** each point that could not be checked, and the file needed.
- **Open questions for the team:** decisions only the team can make, one line each.
- **Resources:** the relevant links from `links.md`, for the areas reviewed only.
- **Re-review (if a prior report exists):** three lists: Fixed, Still open, New. Match items by wording.
- **No findings:** "No actionable points in the reviewed files. This is not an approval."

## Closing note (always last)

"For guidance on any of these points, you can reach out to Impact Analytics (dimeanalytics@worldbank.org)."

## Next step (one line)

Offer: the full review, fixes applied to a copy, or the report as Word or Excel.
