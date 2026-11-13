---
name: survey-prep-timeline
description: "Plan the preparation for a primary survey. Use whenever the user wants a survey prep plan or timeline: list every step needed before fieldwork and check none is missing, schedule steps backward from the date data collection must start, or work out the earliest possible start from what is already done. Covers ethics, sampling, questionnaire, pilot, programming, hiring a firm, manual, training, and quality plan. Asks the team for survey type, dates, and durations. Never assumes them."
---

# Survey prep timeline

Scope: universal. Never assume. Durations in `references/steps.md` are suggestions to confirm, not facts. Write short sentences.

## Three tasks

| Task | Method |
|---|---|
| Prep plan: every step, none missing | Compare the team's steps with `references/steps.md` |
| Timeline backward from the data collection start | `scripts/build_timeline.py plan.json --mode backward` |
| Timeline forward from what is done | `scripts/build_timeline.py plan.json --mode forward` |

Read `project-brief.md` first if it exists. Update it at the end with the start date and survey type.

## Step 1: Ask

Tappable questions if available (ask_user_input), always with free text. Skip what is known. One turn, up to three questions, then follow up:
1. Which task, and the survey type and mode (in-person household, school-based, phone, facility or firm, panel follow-up, records retrieval, other).
2. The date data collection must start, or whether it is open. Any fixed deadlines.
3. What is already done, and whether a firm will be hired.

Then ask, only as needed: instrument new, adapted, or a follow-up; whether the survey has been fielded in this place before; who writes the field plan; known blackout dates (harvest, rainy season, holidays, elections, school terms); the team's own durations for ethics approval, procurement, translation, programming, training; and who owns each step. If a team lacks a duration, show the suggested range, then ask them to choose or give their own.

## Step 2: Confirm documents

If the team shares an existing plan or Gantt, ask: "Please confirm it holds no personal identifiers and you may share it here." Accept only a clear yes.

## Step 3: Build

1. Load `references/steps.md` once. Mark each step as applies, does not apply (say why), or done.
2. **Coverage:** list steps the team's plan lacks, and rules it breaks (ethics before pilot, freeze before translation, procurement before firm-dependent steps, separate pilot, owners named).
3. **Timeline:** write `plan.json` with the confirmed durations, dependencies, owners, blackout dates, and `from_date` set to today (the script uses `from_date` before `--today`). Run the script (it prints a Markdown table, and `--md schedule.md` saves it). Do the date arithmetic with the script, never by hand.
4. Read the flags. A "does not fit" result is the main finding: say by how many weeks, and which steps can overlap or shorten. Do not shorten a step yourself. Ask the team.

## Step 4: Report

Short and usable: (1) coverage gaps; (2) the schedule as a table (step, owner, start, end); (3) flags (no owner, before today, overlaps blackout); (4) open questions, including every duration the team has not confirmed. If the team wants Excel, convert the Markdown schedule with the xlsx skill. If the plan does not fit, give two or three options with their trade-offs and a recommendation.

## Keep it light

Do not read documents you do not need. Use the script for dates. Do not restate the step list in chat. Show only steps that apply.
