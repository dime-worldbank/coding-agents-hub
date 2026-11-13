# ietestform rules, built into this skill

`ietestform` is a Stata command in `iefieldkit` that tests a SurveyCTO or ODK form for errors that
could interrupt fieldwork and for best practices. Its tests now run through
reading the form (`four-columns.md`) and the judgment flags. **Do not ask the team to run `ietestform` or to
upload its CSV.** If a team already has a report, treat it as extra evidence and do not repeat its items.

| What `ietestform` tests | Where it is checked here |
|---|---|
| Fields that are not required (GPS may be deliberate) | VALID-003 |
| Notes marked required with no relevance, so the enumerator cannot move on | VALID-005 |
| Begin and end groups or repeats unmatched, mistyped, or named differently | STRUCT-002, STRUCT-003 |
| No `label:stata` column in `survey` or `choices` | STATA-001 |
| Stata labels over 80 characters | STATA-002 |
| Variable names over 32 characters, counting repeat suffixes (32 minus 2 per repeat level; 3 if a group has more than 9 questions) | NAME-003 |
| Names that could collide after repeat export (`myvar`, `myvar_1`) | NAME-004 |
| Leading or trailing spaces | NAME-005 |
| Choice names that are not numbers | LIST-005 |
| Unused choice lists (often a typo in a list name) | LIST-003 |
| Duplicate choice names or values, or one label with different codes | LIST-002, LIST-007 |
| A choice with a label but no name, or the reverse | LIST-006 |
| Outdated `position()` or `jr:choice-name()` | SYNTAX-001 (use `index()` and `choice-label()`) |
| Encryption not enabled | META-004 (report under ethics and data security if that area is also in scope; otherwise here) |

## Checks this skill adds beyond `ietestform`

Undefined or forward `${var}` references, unreachable skips, `selected()` misuse, choice filters,
translations, paradata fields, consent gating, and comparison with the paper questionnaire.

## Status

The `ietestform` page has no date. The list above comes from the Development Impact Wiki page and may lag the command.
Tell the team this if they ask whether the list is complete.
