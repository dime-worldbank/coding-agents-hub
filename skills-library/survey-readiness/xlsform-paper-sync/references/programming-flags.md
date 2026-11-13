> **Used by xlsform-paper-sync.** Severity mapping for the report: Critical = Mandatory; High and Medium = Priority; Low = Suggested. Apply by reading the form Markdown (see `four-columns.md`). No script is used. For how to write or change form syntax, load the SurveyCTO skill first (see `surveycto-skill.md`).

# Survey programming flags

Apply rules contextually. A pattern is not a finding when surrounding logic
already controls the risk or the behavior is documented and intended.

**AI implementation** values:

- **Yes:** intended behavior is established by the form itself; safe to fix after approval.
- **Conditional:** a specific missing fact or survey-team decision is needed first.
- **No:** a design or methodological decision; the agent does not offer it as a fix.

Report one finding per root cause under the most specific ID. Consolidate
repeated instances and list representative rows.

## Structure and naming (mechanical)

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---:|---|---|
| STRUCT-001 | Missing `survey` sheet, or select questions with no `choices` sheet | Critical | Restore the missing sheet. | Conditional |
| STRUCT-002 | Unbalanced `begin`/`end` group or repeat | High | Close or remove the stray row; confirm intended nesting. | Conditional |
| NAME-001 | Duplicate variable names | High | Rename so every name is unique; update all references. | Conditional |
| NAME-002 | Names with spaces/special characters, starting with a digit, or missing | Medium | Rename to valid, stable names; update references. | Yes |

## Choice lists (mechanical)

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---:|---|---|
| LIST-001 | `select_*` references a list not in `choices` | Critical | Add the list or correct the name. Do not invent options. | Conditional |
| LIST-002 | Duplicate choice names within a list | High | Make names unique; confirm which code is correct. | Conditional |
| LIST-003 | List defined but never used | Low | Remove or document. | Yes |
| LIST-004 | List with a single option | Low | Confirm whether options are missing. | Conditional |

## Skip logic and references (mechanical)

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---:|---|---|
| LOGIC-001 | Expression references an undefined `${var}` | Critical | Fix the reference after confirming the intended variable. | Conditional |
| LOGIC-002 | `relevant`/`calculation`/`required` references a variable defined later | High | Move the question or the dependency so the referenced value exists first. | Conditional |
| LOGIC-003 | `relevant` references its own question | High | Remove the self-reference; confirm intended condition. | Conditional |
| LOGIC-004 | Condition tests a value absent from the source list (likely unreachable) | Critical | Correct to a valid choice name; confirm the intended code. | Conditional |
| LOGIC-005 | `select_multiple` compared with `=` or `!=` | High | Use `selected(${var}, 'value')`. | Yes |
| LOGIC-006 | `choice_filter` uses a column not in `choices` | High | Add the column or correct the filter. | Conditional |

## Skip logic (judgment)

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---:|---|---|
| LOGIC-007 | A follow-up question lacks a `relevant` that matches its universe (asked of everyone though only some qualify, or the reverse) | High | Add or correct the condition once the universe is confirmed. | Conditional |
| LOGIC-008 | Required question is reachable only through a condition that can never be met, so interviews cannot be completed | Critical | Fix the condition or relax `required`. | Conditional |
| LOGIC-009 | Contradictory conditions between a question and its enclosing group | High | Consolidate to one clear condition. | Conditional |
| LOGIC-010 | Missing skip for "Don't know"/"Refused" paths, so respondents are routed into follow-ups that do not apply | Medium | Add a condition that excludes those responses. | Conditional |
| LOGIC-011 | Calculation divides by a value that can be 0 or blank, or uses an unguarded `if` | Medium | Add a guard such as `if(${x} != 0, ..., '')`. | Conditional |
| LOGIC-012 | Same condition repeated across many rows rather than set once on a group | Low | Move to a group-level `relevant`. | Yes |
| LOGIC-013 | Repeat group with no `repeat_count` or an unbounded count | Medium | Set a count tied to the roster variable. | Conditional |

## Validation and data capture

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---:|---|---|
| VALID-001 | `integer`/`decimal` with no constraint (age, counts, quantities, prices) | Low; Medium for age, area, quantity, or money | Add a plausible range. The range is a survey team decision. | No |
| VALID-002 | Constraint without a constraint message | Low | Add a clear message in every language. | Conditional |
| VALID-003 | No `required` column, or no question enforced | Medium | Confirm which questions must be answered, then set `required`. | Conditional |
| VALID-004 | `select_multiple` with "None"/"Don't know" but no exclusivity constraint | Medium | Add a constraint, e.g. `not(selected(., 'none') and count-selected(.) > 1)`. | Yes |
| VALID-007 | Open-ended `text` used where a coded list would do, or with no length/format check | Low | Confirm whether a list or regex constraint is appropriate. | Conditional |
| VALID-006 | Identifiers (household ID, phone, date of birth) with no format or uniqueness check | Medium | Add a regex or lookup validation. | Conditional |


More flags (translation, field readiness, best practice, ietestform-aligned checks, additional and added checks) are in `programming-flags-config.md`.
