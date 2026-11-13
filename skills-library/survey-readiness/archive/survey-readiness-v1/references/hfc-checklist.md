# High-frequency checks: coverage checklist

Compare the team's DQA plan against this list. Report every **core** check that is
missing, then any recommended ones, with the tool that covers it. **Draft list:**
compiled from the five check types in `iehfc` and common high-frequency check
practice (as in `ipacheck` and SurveyCTO monitoring); confirm the core/recommended
split with Impact Analytics.

Set up: iehfc (R package with a Shiny app, no coding needed): https://github.com/dime-worldbank/iehfc.
Other tools: ipacheck (Stata) https://github.com/PovertyAction/high-frequency-checks; SurveyCTO built-in monitoring (see `links.md`).
Checks should be coded in parallel with questionnaire design and programming, tested on pilot data, and run from the first day of fieldwork. Prioritise checks most likely to affect data quality.

| Check | Level | Covered by iehfc |
|---|---|---|
| Duplicate IDs and repeated interviews | Core | Yes (duplicate check) |
| Outliers in numeric fields (SD or IQR), single and grouped variables | Core | Yes (outlier detection) |
| Enumerator monitoring: submissions, completion rate, average responses | Core | Yes (enumerator monitoring) |
| Progress by administrative unit over time | Core | Yes (administrative unit summary) |
| Unit-level tracking: who was visited, by whom, complete or not | Core | Yes (unit of observation tracking) |
| Interview duration, overall and by enumerator, including very short interviews | Core | Partly (average responses; duration needs the start/end fields) |
| Missing values and item non-response by field and enumerator | Core | Partly |
| Consent and refusal rates by enumerator and area | Core | Partly |
| Don't know and refusal rates by enumerator | Recommended | No |
| Skip-logic and constraint violations in submitted data | Recommended | No |
| Interviews started or ended at implausible times, or on device-date errors | Recommended | No |
| GPS checks against the expected location | Recommended | No |
| Straight-lining and very low variance across a block of questions | Recommended | No |
| "Other, specify" text review and new categories | Recommended | No |
| Back-check comparison with original interviews | Core (see DQA-004) | No |
| Field comments or text-audit review | Recommended | No |
| Sample and target progress against the plan | Core | Partly (administrative unit summary) |

**Reporting a gap:** one line per missing check: check, why it matters, tool that covers it, and the paradata it needs (see DQA-009).
