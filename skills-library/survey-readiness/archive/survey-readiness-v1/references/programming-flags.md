> **Used by survey-readiness.** Severity mapping for the report: Critical = Blocker; High and Medium = Important; Low = Minor. Run `scripts/inspect_xlsform.py` first; the "AI implementation" column says whether Claude can safely apply a fix (Yes, Conditional, No).

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

## Skip logic (judgment; the script cannot detect these)

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

## Translation

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---:|---|---|
| LANG-001 | Label, hint, or constraint message missing in some languages | Medium | Supply the missing translation. Do not machine-translate without a flag for review. | Conditional |
| LANG-002 | Choice labels missing in some languages | Medium | Supply the missing translation. | Conditional |
| LANG-003 | Translated text appears to differ in meaning from the source (e.g. different recall period or units) | High | Flag for bilingual review. | No |

## Field-readiness and paradata

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---:|---|---|
| META-001 | No `start`/`end` timestamps | Medium | Add them so duration checks are possible. | Yes |
| META-002 | No `deviceid` (or enumerator ID question) | Low | Add for device- and enumerator-level checks. | Yes |
| META-003 | No `form_id` or `version` in settings | Medium; Low for version alone | Set both so deployed versions are traceable. | Conditional |
| FIELD-001 | No audit/GPS paradata where the study design calls for them | Low | Confirm with the survey team; consider SurveyCTO `audit` or `geopoint`. | No |
| FIELD-002 | Sensitive variables (names, phone, GPS) not flagged for de-identification (SurveyCTO `publishable` column or equivalent) | Medium | Mark sensitive fields and document the disclosure plan. | No |
| FIELD-003 | Very long single form with no module-level structure or progress cues | Low | Consider groups and notes; assess respondent burden. | No |

## Question-level design issues

Wording, recall periods, sensitive questions, and flow are checked in `questionnaire-design.md` (DES-*). Do not repeat them here.

## DECDI conventions (checked by the script where possible)

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---|---|---|
| STATA-001 | No `label:stata` column in `survey` or `choices` | Medium | Add the column. The team supplies the labels. | Conditional |
| STATA-002 | Stata labels longer than 80 characters (Stata truncates) or non-ASCII | Low | Shorten. | Conditional |
| CODE-001 | Don't know, Refused, or Other coded differently across choice lists | Low | Adopt one scheme across the instrument. | Conditional |
| META-004 | No encryption key (`public_key`) in settings, meaning encryption at rest is not enabled (SurveyCTO) | Medium; Blocker in the survey-readiness verdict when personal data are collected | Enable at form creation. It cannot be added to an existing form. Report once, in the ethics and data security area (ETH-014), and do not repeat it under programming. | No |
| ELEC-001 | Consent is not first, or the form continues when consent is refused | Critical | Gate all later groups on consent, or end the form. | Conditional |
| ELEC-002 | Groups used sparingly: one group per module at the top level only, shared `relevant` conditions on groups | Low | Restructure. | Yes |
| ELEC-003 | Repeat groups over previous choices and dynamic choice lists are built with `choice_filter` or `repeat_count` tied to the roster | Medium | Fix the repeat source. | Conditional |
| ELEC-004 | Printable questionnaire tabs and the `survey` sheet disagree (question text, choices, or skip instructions) | High | Reconcile against the final instrument. | Conditional |

**Reading workbooks with linked tabs.** If `name` or `label` cells are formulas linking to
printable tabs, the script reads cached values. If it warns about uncalculated formulas,
open and save the file in Excel, then re-run.

## ietestform-aligned checks (script)

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---|---|---|
| STRUCT-003 | `end group`/`end repeat` closes the wrong type, has no name, or its name differs from its begin | Medium; High for wrong type | Name each end to match its begin. | Yes |
| NAME-003 | Name longer than 32 characters, or 32 minus 2 per repeat depth inside repeats | Medium | Shorten. | Conditional |
| NAME-004 | Name inside a repeat could collide with `name_1` after export | Low | Rename. | Conditional |
| NAME-005 | Leading or trailing space in a name, list name, or type | Low | Trim. | Yes |
| LIST-005 | Choice names are not integers | Low | Use integer codes. | Conditional |
| LIST-006 | Choice has a label without a name, or the reverse | Medium | Complete it. | Conditional |
| LIST-007 | Same label used for different names within a list | Low | Check for a copy-paste error. | Conditional |
| SYNTAX-001 | Outdated `position()` or `jr:choice-name()` | Medium | Replace with `index()` or `choice-label()`. | Yes |
| VALID-003 | Input fields not required (GPS fields reported separately as Low) | Medium | Allow non-answers as choices and use relevance. | Conditional |
| VALID-005 | Required note with no relevance (enumerator cannot proceed) | Critical | Make it not required, or add a relevance condition. | Conditional |

## Style Guide conventions (Impact Analytics SurveyCTO Style Guide)

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---|---|---|
| NAME-006 | Names with uppercase or characters other than a-z, 0-9, `_`. The guide recommends `module_varname_add`, lowercase, 32 characters or fewer | Low | Rename to the convention and update references. | Conditional |
| STYLE-001 | No blank rows between top-level modules | Low | Add blank rows between modules. | Yes |
| STYLE-002 | Form version not a date-time (`yymmddhhmm`) set by formula, so a new upload may not be greater than the server version | Low | Set version by formula. | Yes |
| STYLE-003 | A label or hint shows `${var}` of a select field, so the enumerator sees the code, not the label | Medium | Load the choice label into a calculate field and reference that. | Conditional |
| STYLE-004 | Begin and end fields not both named and labelled, so groups are hard to match (also STRUCT-003) | Low | Name and label both. | Yes |
| STYLE-005 | Rows not colour-coded by field type, or the form was not built from the DECDI XLSForm Template (visual; not script-checked) | Low | Use the template. | No |
| STYLE-006 | Module prefix in names does not follow the project's abbreviations | Low | Apply the naming document. | Conditional |
| LIST-005 | (Style Guide reason) Non-numeric choice values make skips fragile: a string such as "Factory Worker" fails a match on a case difference | Low | Use numeric codes. | Conditional |
| CODE-001 | Special codes differ from the Style Guide scheme: -99 Don't know, -88 Refused, -9 Other, the same in every list | Low | Recode to the scheme and update skip logic that tests those values. | Conditional |

**Not script-checked (need the template or a visual review):** colour coding, use of the DECDI XLSForm Template, and module abbreviations from the variable naming conventions document, neither of which has been provided.

## Additional programming flags

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---|---|---|
| HINT-001 | Enumerator instructions sit in the label text (for example starting with "Enumerator:") instead of the hint column | Low | Move to the hint column, separate from text read aloud. | Yes |
| HINT-002 | Complex questions have no enumerator hint (definitions, rounding rules, probes) | Low | Add hints where the pilot showed confusion. | Conditional |
| META-005 | Form collects subscriber ID, SIM serial, or phone number | Low | Treat as personal data; keep out of publishable fields and include in the de-identification plan. | Conditional |
| META-006 | A personal-data field (name, phone, address, GPS) is marked publishable | Medium | Remove the publishable flag. | Yes |

**Other platforms.** The script reads XLSForms (SurveyCTO, ODK, KoboToolbox). For other platforms (for example CSPro or Survey Solutions), review the platform-neutral items by hand: consent gating, skip logic and universes, constraints, required fields, translations, paradata, special codes, and encryption.

**Interview path size.** The script reports field counts for the shortest path (fields always shown) and the longest path (all conditional fields shown), with repeat groups counted once. These are bounds, not timings. Ask the team for pilot timings.
