# Survey Prep Timeline

`survey-prep-timeline` is a reusable AI-agent skill for planning the preparation of a primary survey. It lists every step that should happen before fieldwork, checks that none is missing, and builds a timeline from the date data collection must start, or from what is already done.

**Scope:** universal.
**Status:** draft for feedback.

| Task | What you get |
|---|---|
| Prep plan | Every step that applies to your survey, with gaps in your current plan and rules it breaks |
| Timeline backward | Latest start and end of each step so data collection starts on your date, and by how much you are short |
| Timeline forward | Earliest start and end of each step and the earliest possible start of data collection |

It never assumes your survey type, dates, or durations. It asks, and it uses suggested durations only if you confirm them.

## Suggested workflow

1. **Prep plan** at the very start, to see all the steps and who owns them.
2. **Timeline backward** once you know the date data collection must start.
3. **Timeline forward** when something slips, to see the new earliest start.
4. Rerun after each major change: approvals, procurement, or the pilot.

## Quick start

Copy the complete `survey-prep-timeline/` folder into your project's skills directory, or upload it as a zip.

```text
your-project/
└── .agents/
    └── skills/
        └── survey-prep-timeline/
```

Then prompt the agent:

```text
Read .agents/skills/survey-prep-timeline/SKILL.md and use it to plan the preparation
for our [SURVEY]. Data collection must start on [DATE].
```

## How it works

1. **Questions:** the agent asks the survey type, the start date, what is done, and your durations and blackout dates. Free text is accepted.
2. **Coverage:** it compares your steps with the step list and reports what is missing.
3. **Schedule:** it writes your steps, durations, and dependencies to a plan file and runs a script, so the dates are calculated, not estimated.
4. **Report:** a coverage list, the schedule as a Markdown table, flags, and open questions. Excel on request, made from the Markdown.

## What the flags mean

- **No owner:** a step has nobody named.
- **Latest start is N days before today:** the plan does not fit. The report says by how many weeks.
- **Overlaps a blackout:** a fieldwork step falls in a harvest, rainy season, holiday, election, or school term window you named.

## Durations

The suggested durations come from earlier Impact Analytics guidance (2017) and the Development Impact Wiki. Several are due for a refresh. Treat them as prompts for your team's own numbers.

## Requirements

Python 3 for the date script. It reads a small plan file and prints a Markdown table. It reads and writes no Word or Excel file. For Excel, the agent converts the Markdown with the xlsx skill. Without code execution the agent can build the plan and coverage list in the chat, but it will not calculate dates by hand.

## Limitations

- It plans preparation, not budgets or staffing.
- It does not know your approval or procurement times. You supply them.
- The step list assumes a primary survey with a research team. Remove steps that do not apply and say why.

## Folder contents

- `SKILL.md`: the instructions the agent follows.
- `references/steps.md`: the step list, rules, survey type notes, and sources.
- `scripts/build_timeline.py`: the scheduling script.
- `tests/`: a sample plan and `run_tests.py`.

## Feedback

Please send comments to Impact Analytics. Useful feedback: steps that are missing, durations that are out of date, and survey types the list does not fit.
