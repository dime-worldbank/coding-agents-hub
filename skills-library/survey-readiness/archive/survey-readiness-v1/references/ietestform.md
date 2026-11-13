# ietestform: how to use and triage its report

`ietestform` is a Stata command in the `iefieldkit` package (`ssc install iefieldkit`).
It tests ODK and SurveyCTO forms for errors that could interrupt fieldwork and for
best practices, and writes a CSV report. Run it only after the form passes the
SurveyCTO server's built-in test.

```
ietestform, surveyform("form.xlsx") report("report.csv")
```

Claude cannot run Stata in this environment. Ask the team to run it and upload the
CSV. Triage the report into the review: map each flag to the ID below, merge
duplicates, and ask the team whether intentional exceptions (for example GPS fields)
are deliberate.

| `ietestform` test | Skill ID | Notes |
|---|---|---|
| Non-note fields not required | VALID-003 | Allow non-answers as choices and use relevance for legitimate skips. GPS fields may be intentionally optional |
| Note fields marked required | VALID-005 | The enumerator cannot move past it. Acceptable only as an error trap with a relevance condition |
| Unmatched or mistyped begin/end, missing or mismatched end names | STRUCT-002, STRUCT-003 | |
| No `label:stata` column in survey or choices | STATA-001 | |
| Stata labels over 80 characters | STATA-002 | |
| Variable names over 32 characters, including repeat suffixes (limit 32 minus 2 per repeat depth; 3 if a group has more than 9 questions) | NAME-003 | |
| Repeat-group suffix collisions (for example `myvar` and `myvar_1`) | NAME-004 | |
| Leading or trailing spaces | NAME-005 | |
| Non-numeric choice names or values | LIST-005 | |
| Unused choice lists | LIST-003 | Often a typo in a list name |
| Duplicate name or value, or one label with different codes | LIST-002, LIST-007 | |
| Choice with a label but no name, or the reverse | LIST-006 | |
| Outdated `position()` or `jr:choice-name()` | SYNTAX-001 | Use `index()` and `choice-label()` |
| Encryption not enabled | META-004 | |

What `ietestform` does not check, and the skill adds: undefined or forward `${var}`
references, unreachable skips, `selected()` misuse, choice filters, translations,
paradata fields, consent gating, and comparison to the paper questionnaire.

The page for `ietestform` has no date; confirm the command's current test list with
`help ietestform` (see `sources.md`).
