# Report format

Write short sentences, about 20 words or fewer. Give each point an issue, a place, and a fix. Never show internal IDs (such as LOGIC-001) or the words Critical, High, Medium, or Low in the report. Keep IDs in your working notes.
Cite sources by short name when it helps ("SurveyCTO docs: expressions", "Development Impact Wiki: SurveyCTO Coding Practices").

## Header (one line each)

Task, files reviewed, platform, stage, and what was not checked.

## Review of a programmed form

**Verdict:** Not ready (any Mandatory), Ready with fixes (no Mandatory, any Priority), Ready (only Suggested or none). Add: "Verdicts cover only the files reviewed and are not an approval."

```
**Mandatory** (fix before fieldwork)
- <issue>. <sheet and row>. Fix: <short fix>. AI can apply: Yes | Conditional | No.

**Priority** (likely to hurt data quality or cause rework)
- ...

**Suggested**
- ...
```

- Key changes (default): Mandatory and Priority, then "N suggested items not shown. Ask for the full review."
- Full review: all three tiers, plus one "Why:" sentence on Mandatory and Priority items.
- Merge repeated instances into one item with example rows. Use `Possible:` when the file does not settle it.
- If a tier is empty, write "None."
- Do not estimate interview length from field counts. Ask for pilot timings.

Tier mapping from the flag tables: Critical = Mandatory; High and Medium = Priority; Low = Suggested.

### Conditional items: response form

After the report, if any item is Conditional, add a short copy-and-edit form. Start with: "Reply with approve, change: [alternative], provide: [information], defer, or discuss." Then one block per item:

```
1. Required fields (survey sheet): which questions must be answered?

Agent recommendation or information needed:
Confirm which questions may be skipped by the enumerator. I will set the rest to required.

Your response:
```

Accept a short reply such as "1: provide: all except 2.4" or "2: defer". Treat blank or unclear answers as unresolved. Use numbered items, not IDs.

## Comparison of paper and programmed versions

```
**Result:** Not aligned | Aligned with minor differences | Aligned (in the questions read)
Read: <N> paper questions, <M> form questions, <K> matched. Language compared: <language>. Not read: <what and why>.
Flow: <one line per section: matched, in the same order, moved, missing>

### <Section>
| Paper no. | Form row | Check | Paper | Form | Suggested response |
```

- One table per section. High and Medium rows in the chat, all rows in `discrepancies.xlsx`. Say how many Low rows are not shown.
- After the tables, give a short note for each of: **flow** (sections where the order really differs), **wording** (meaning changes), **choices** (including preload files not checked and the files requested), **skip logic**, **constraints and required fields**, and **consent and introduction text**. Name doubtful matches you dropped.
- The result line is "Aligned" only if counts agree, no High row remains, and each of the checks above was done.
