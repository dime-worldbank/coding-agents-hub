---
name: survey-readiness
description: Self-check review of primary survey preparation for project teams. Covers timeline, ethics and data security, sampling, hiring a survey firm (Bank-executed or recipient-executed), pilot plan, questionnaire design, survey programming (XLSForm, ietestform, Style Guide), enumerator training and field plan, and data quality plan. Asks what the team wants reviewed, requests only the relevant files, and returns lists of mandatory, priority, and suggested changes with sources and links, a ready / not-ready verdict, and a closing note on contacting Impact Analytics. Do not open files until content confirmation is given.
---

# Survey Readiness

First-pass self-check before fieldwork. Does not replace ethics approval, a sampling expert, or an Impact Analytics review, and never approves a plan. Write short sentences (about 20 words or fewer). Give each finding a clear issue, a location, and a fix. A little fuller than a bare note, never long.

> **Basis.** Criteria come from the DIME Wiki, the DECDI research standards and consent templates, SurveyCTO documentation, and Impact Analytics survey review resources. See `references/sources.md` for dates and gaps. The 2017 lead times are kept for now. Never present a criterion as an official requirement unless its source says so.

## Tiers

Show three tiers: **Mandatory** (fix before fieldwork), **Priority** (likely to hurt data quality or cause rework), **Suggested** (good practice). Module files use Blocker, Important, and Minor for the same tiers. Do not show IDs or those words in the report.

## Step 1: Ask what to review

Use tappable questions if available (ask_user_input), otherwise short text, and always allow free text. One turn:

1. **Stage:** planning / piloting / ready for fieldwork / in the field.
2. **What to review** (any):
   - Planning: timeline, sampling, ethics and data security
   - Hiring a firm and field: TOR, enumerator training, field plan
   - Instrument: questionnaire design, pilot plan
   - Programming and data quality: survey programming, data quality plan
3. **Output:** Key changes (Mandatory and Priority, default) or Full review (adds Suggested items, short reasons, and sources). Format: in chat (default), Word, or Excel.

If the team describes needs in text, map them to modules and confirm in one line.

## Step 2: Ask only what is needed

Ask the intake fields for the chosen areas from `references/intake.md` and request only the files below. If a prior report is provided, do a **re-review**: fixed, still open, new.

| Area | Module | Files |
|---|---|---|
| Timeline | `timeline.md` | Timeline or Gantt with owners |
| Ethics and data security | `ethics-security.md` | Approval status, consent form(s), data security plan, the SurveyCTO instrument if available |
| Sampling | `sampling.md` | Sampling strategy, power calculations, frame, code |
| Hiring a survey firm | `hiring-survey-firm.md`, `tor-reference.md` | Draft TOR, selection criteria. Ask first: Bank-executed or recipient-executed |
| Pilot plan | `pilot.md` | Pilot plan, respondent selection protocol, change log plan |
| Questionnaire design | `questionnaire-design.md` | Questionnaire, outcomes list, pilot timings |
| Survey programming | `programming-flags.md`, `ietestform.md`, script | Form (.xlsx), `ietestform` report (.csv), paper questionnaire if available |
| Training and field plan | `training-field-plan.md` | Training manual and schedule, manuals, field plan |
| Data quality plan | `dqa-plan.md`, `hfc-checklist.md` | DQA plan, data check protocol and code |

Load only the chosen modules, one at a time.

## Step 3: Content confirmation

Before opening any file ask: "Please confirm these files contain no real respondent data or personal identifiers, and that I may review them." Accept only a clear yes; treat hedges as no. If a file contains respondent data, stop and say so.

## Step 4: Review (read-only)

1. Read the module, then the files. Report only what the files support; otherwise list **Not assessable** with the file needed.
2. **Ethics:** split findings into (A) needed for approvals (IRB, privacy office) and (B) to do in the field. If the instrument and consent are both available, compare them and list anything in the form that consent does not cover.
3. **Hiring a firm:** apply the Bank-executed or recipient-executed checks. For Bank-executed, list privacy office approval as mandatory. Word it as guidance ("The guidance used here says…"), as it is not verified against a document. Do the same for the single-source threshold.
4. **Pilot:** focus on the contents the pilot will test. Ask for the team's plan for recording changes; if none, suggest the change log in `pilot.md`.
5. **Questionnaire design and programming overlap.** Report each issue once under the most specific ID and refer to the other module. The Style Guide applies to programming only.
6. **Survey programming flow:**
   1. Ask whether the form passed the SurveyCTO server test (`ietestform` runs after it).
   2. If they have Stata, ask them to run `ietestform` and upload the CSV; triage with `references/ietestform.md`. Claude cannot run Stata.
   3. Run `python scripts/inspect_xlsform.py <form.xlsx>`. Output is compact by default; use `--full` only to list every row of one flagged ID. Confirm each result in context.
   4. Apply the judgment flags in `programming-flags.md`, including Style Guide conventions. Report the shortest and longest path field counts and ask for pilot timings.
   5. If a paper questionnaire is provided, compare it with the form.
   6. Other platforms: use the platform-neutral items only; the script reads XLSForms.
7. **Data quality plan:** compare the plan's checks with `hfc-checklist.md` and list every missing core check, with the tool that covers it (iehfc, ipacheck, SurveyCTO).
8. **Cross-document consistency** when two or more documents are provided: dates, sample sizes, quality coverage, responsibilities.
9. Each finding: a short issue, where it is, the tier, and a short fix. Use `Possible:` where evidence is incomplete. Merge repeated instances. Keep IDs in your working notes only, to avoid reporting the same issue twice.

### Verdict per area

**Not ready** (any Mandatory), **Ready with fixes** (no Mandatory, any Priority), **Ready** (only Suggested or none), **Not assessable** (files missing). Verdicts cover only the files reviewed and are not an approval.

## Step 5: Report

Use `references/report.md`: a list per area under Mandatory, Priority, and Suggested. List every finding in the chosen output, not a top few. Add the relevant links from `references/links.md`, then the closing note.

## Step 6: Closing note

End every report with: "For guidance on any of these points, you can reach out to Impact Analytics (dimeanalytics@worldbank.org)." Do not draft or send emails and do not tag items for escalation.

## Step 7: Optional fixes (only if asked)

Offer fixes only where intended behavior is clear. Write to a new copy, never the original, and log each change. Sample size, constraint ranges, thresholds, and question wording are the team's decisions.

## Keep it light

- Never read a whole workbook or long document into context: use the script for forms and extract only the relevant sections of Word or PDF files.
- Do not reload a module already read in the conversation.
- Do not restate guidance; cite the ID and give the fix.
