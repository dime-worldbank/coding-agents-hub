---
name: enum-training-plan
description: "Build an enumerator training plan and agenda. Use whenever the user wants to plan, schedule, or check an enumerator or field staff training: agenda by day, quizzes, the final test, field practice, the observation checklist, participation scoring, enumerator selection, and logistics. Asks the team for training days, restrictions, trainees, languages, and survey details, and never assumes them. Uses Development Impact Wiki guidance. Pairs with the enumerator manual."
---

# Enumerator training plan

Scope: universal. Based on Development Impact Wiki guidance (`references/components.md`). Never assume. Ask. Write short sentences.

## Steps

1. **Ask.** Read `project-brief.md` first if it exists. Use tappable questions (ask_user_input) with free text, one turn, skipping what is known. The list is in `references/agenda-building.md`. At minimum: how many training days and which dates, restrictions (rest days, holidays, venue, daily hours, remote or in person), number of trainees and positions, languages, survey mode, modules and complexity, enumerator experience, practice options, and who marks and selects. Do not choose any of these for the team.
2. **Read the inputs the team shares.** If a questionnaire form is shared, ask the team to confirm it holds no respondent data, then convert it to Markdown (`markitdown form.xlsx -o form.md`, or `extract-text`), keep the type, name, label, relevant and constraint columns, and read the modules and skip rules from that. Or ask for the manual. If a manual exists, use its protocols and modules.
3. **Build** the agenda with `references/agenda-building.md`: frame, fixed blocks, breaks, then each session with time, topic, objective, method, materials, lead. Load `references/components.md` once for the elements to include.
4. **Check** with `python scripts/check_agenda.py agenda.md --days N --hours-per-day H` (add `--one-day-ok` for a one-day training). Fix every MISSING and FAIL. Look at each CHECK.
5. **Deliver** the plan as Markdown. Offer Word (`pandoc plan.md -o plan.docx`, or the docx skill). Include, after the agenda table: the quiz plan, the final test outline, the field practice plan with the observation checklist, the selection plan, the logistics list, and the open decisions.
6. **Remind the team** of the elements to use for testing (end of `agenda-building.md`).

## If the days are too few

Do not cut silently. Show what is cut and the risk of each cut. Give options and a recommendation. Ask the team to choose.

## Report style

Lead with the agenda table. Then list open decisions: every item the team has not answered. Mark any suggested duration as a suggestion to confirm. Do not state wiki figures as rules.

## Keep it light

Load each reference once. Write the agenda in a file, show the table in chat. Do not paste the observation checklist or scoring rubric into chat unless asked. They go in the file.
