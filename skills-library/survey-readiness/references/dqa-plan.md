# Data quality assurance plan review

**Basis:** DIME Wiki *Data Quality Assurance Plan* and *High Frequency Checks*; Impact Analytics survey review resources.
**Documents:** DQA plan, list of checks, protocol for data checks, check code, monitoring responsibilities.
**Rule:** check coverage, feasibility, and who acts on what. The plan should be shared with every stakeholder, including the firm, before data collection starts.

| ID | What to check | Severity | Fix |
|---|---|---|---|
| DQA-001 | Plan names its main risks: respondent fatigue, enumerator error or fabrication, and weak quality control by the team itself | Important | Add risks |
| DQA-002 | Survey design defences used: constraints and relevance in the form, preloaded data where available, case management for pre-assigned interviews | Important | Add to the instrument and plan |
| DQA-003 | Field management defences: accompaniment or shadowing by the team early in fieldwork, team leader observation forms, daily tracking sheets for completed interviews and units not found | Important | Add them |
| DQA-004 | Back-checks: random coverage across every enumerator and team, roughly 10% of interviews with a higher share (about 20%) in the first weeks, plus missing respondents, flagged observations, and suspected cheaters | Blocker if no back-check plan | Add back-check protocol with coverage and timing |
| DQA-005 | High-frequency checks are specified. Compare the plan with `hfc-checklist.md` and list every core check that is missing | Blocker if none exist | Add the missing checks |
| DQA-013 | The plan names the tool and who runs it daily or weekly: iehfc (R, with a point-and-click app), ipacheck (Stata), or SurveyCTO built-in monitoring | Important | Name the tool and owner |
| DQA-006 | Check code exists and has been tested on pilot data before fieldwork | Important | Write and test |
| DQA-007 | Each check has frequency, owner, rule or threshold, and action when it fails | Important | Fill gaps |
| DQA-008 | Feedback to enumerators and supervisors is given after interviews, not during, with a path for repeated problems | Important | Add protocol |
| DQA-009 | The form collects the paradata the checks need (start and end time, device and enumerator ID, GPS) | Important | Add fields |
| DQA-010 | Roles of the team and the firm match the TOR, including data delivery frequency and corrections | Important | Reconcile |
| DQA-011 | Plan for incomplete interviews, re-interviews, corrections, and a change log | Minor | Add protocol |
| DQA-012 | Plan is feasible for budget, connectivity, and staffing | Minor | Prioritize |

**Link:** iehfc for setting up checks: https://github.com/dime-worldbank/iehfc (see `links.md`).

**Ask if missing:** which paradata the form records; who runs checks and how often.
