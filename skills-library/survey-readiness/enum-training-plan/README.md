# Enumerator Training Plan

`enum-training-plan` is a reusable AI-agent skill for planning an enumerator training. It builds an agenda from the days and constraints you give it, adds the quizzes, final test, field practice, scoring, and selection steps, and reminds you of the elements to use for testing.

**Scope:** universal. It follows Development Impact Wiki guidance on enumerator training.
**Status:** draft for feedback.

| What you give | What you get |
|---|---|
| Training days, restrictions, trainees, languages, survey details | An agenda by day and time, a quiz plan, a final test outline, a field practice plan with the observation checklist, a selection plan, a logistics list, and open decisions |

It never assumes your training days or restrictions. It asks.

## Suggested workflow

1. Prepare the enumerator manual (see `enum-manual`).
2. Run this skill to plan the training around it.
3. Share the draft agenda with the survey firm and supervisors.
4. After the pilot, update the manual and rerun this skill if the agenda changes.

## Quick start

```text
your-project/
└── .agents/
    └── skills/
        └── enum-training-plan/
```

```text
Read .agents/skills/enum-training-plan/SKILL.md and use it to plan the enumerator
training for our [SURVEY].
```

## How it works

1. **Questions:** the agent asks for training days and dates, restrictions, trainees and positions, languages, mode, modules, experience, practice options, and who marks and selects. Free text is accepted.
2. **Build:** it places the standard blocks and fits them to your days. If the days are too few, it shows what is cut and the risk, and asks you to choose.
3. **Check:** a script checks that the agenda covers protocols, questionnaire, tablets, confidentiality, practice, a quiz each day after the first, a final test, and selection, and that days are not too long.
4. **Deliver:** Markdown, and Word if you ask.

## Elements for testing

Understanding of materials. Reading in each survey language. Understanding of questions and scales. Numeracy and tablet entry. A quiz each day on the previous day's topics, marked the same day. A final test aimed at weak areas. Field practice scored with the observation checklist. Participation scored 1 to 5. Train more than needed and keep a reserve.

## Requirements

Python 3 for the agenda checker. Without code execution the agent can still plan in the chat but cannot run the check. Word output needs `pandoc` or the docx skill.

## Limitations

- The wiki page is dated June 2024. Check it for current guidance.
- The wiki figures (for example about four hours a day for remote training) are examples from the wiki, not rules.
- It plans the training. It does not write the quizzes or the final test. Ask for them as a follow-up.

## Folder contents

- `SKILL.md`: the instructions the agent follows.
- `references/`: the training elements and how to build the agenda.
- `scripts/check_agenda.py`: the agenda checker.
- `tests/`: a complete and an incomplete sample agenda, and `run_tests.py`.

## Feedback

Please send comments to Impact Analytics. Useful feedback: elements missing from the agenda, sessions that do not fit your survey type, and checks that are too strict.
