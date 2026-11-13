# Survey programming flags, part 2

Same rules and severity mapping as `programming-flags.md`.

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

Wording, recall periods, sensitive questions, and flow are not reviewed by this skill. Differences between the paper wording and the form are covered by the comparison (`comparison-method.md`).

## Best-practice checks (on by default)

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---|---|---|
| STATA-001 | No `label:stata` column in `survey` or `choices` | Medium | Add the column. The team supplies the labels. | Conditional |
| STATA-002 | Stata labels longer than 80 characters (Stata truncates) or non-ASCII | Low | Shorten. | Conditional |
| META-004 | No encryption key (`public_key`) in settings, meaning encryption at rest is not enabled (SurveyCTO) | Medium; Mandatory when personal data are collected | Enable at form creation. It cannot be added to an existing form. Report once. | No |
| ELEC-001 | Consent is not first, or the form continues when consent is refused | Critical | Gate all later groups on consent, or end the form. | Conditional |
| ELEC-002 | Groups used sparingly: one group per module at the top level only, shared `relevant` conditions on groups | Low | Restructure. | Yes |
| ELEC-003 | Repeat groups over previous choices and dynamic choice lists are built with `choice_filter` or `repeat_count` tied to the roster | Medium | Fix the repeat source. | Conditional |
| ELEC-004 | Printable questionnaire tabs and the `survey` sheet disagree (question text, choices, or skip instructions) | High | Reconcile against the final instrument. | Conditional |

**Reading workbooks with linked tabs.** If `name` or `label` cells are formulas linking to printable tabs, the converter reads cached values. If cells show NaN where text should be, ask the team to open and save the file in Excel, then convert again.

## ietestform-aligned checks (see `ietestform-rules.md`)

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

## Additional programming flags

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---|---|---|
| HINT-001 | Enumerator instructions sit in the label text (for example starting with "Enumerator:") instead of the hint column | Low | Move to the hint column, separate from text read aloud. | Yes |
| HINT-002 | Complex questions have no enumerator hint (definitions, rounding rules, probes) | Low | Add hints where the pilot showed confusion. | Conditional |
| META-005 | Form collects subscriber ID, SIM serial, or phone number | Low | Treat as personal data; keep out of publishable fields and include in the de-identification plan. | Conditional |
| META-006 | A personal-data field (name, phone, address, GPS) is marked publishable | Medium | Remove the publishable flag. | Yes |

**Other platforms.** These checks read XLSForms (SurveyCTO, ODK, KoboToolbox). For other platforms (for example CSPro or Survey Solutions), review the platform-neutral items by hand: consent gating, skip logic and universes, constraints, required fields, translations, paradata, special codes, and encryption.

**Interview length.** Do not estimate interview length from field counts. Ask the team for pilot timings.

## Added checks

| ID | What to detect | Severity | Recommended response | AI implementation |
|---|---|---|---|---|
| NUM-001 | The same question number appears on more than one question label | Medium | Renumber. Also compare with the paper version. | Conditional |
| NAME-003 | Group names are checked as well as field names (limit 32 characters) | Medium | Shorten. | Conditional |

**Style Guide checks** (white space, name format, special codes, version format, choice labels loaded by calculate) are optional. See `style-guide.md` and run the script with `--style-guide`.
