---
name: enum-manual
description: "Write an enumerator manual (field manual) for a survey. Use whenever the user wants to create, draft, or update an enumerator or field manual, interviewer instructions, or a field protocol: study objectives, roles, survey protocols, tablet instructions, question-by-question guidance from the questionnaire, key terms, FAQs, and escalation. Asks the team for details section by section, reads the programmed form, and never invents protocols. Works for interview surveys and records retrieval."
---

# Enumerator manual

Scope: universal. Based on Development Impact Wiki guidance and a worked field protocol example (`references/manual-structure.md`). Never assume or invent a rule, number, date, name, or contact. Ask. Write short sentences.

## Steps

1. **Ask.** Read `project-brief.md` first if it exists. Tappable questions (ask_user_input) with free text, one turn, skipping what is known: survey type (interview or records retrieval), mode, language of the manual, what the team can share (programmed form, protocol or TOR, field plan, sample manuals), and output (Markdown plus Word). Then work section by section.
2. **Confirm files.** Before reading any file, ask: "Please confirm these files contain no respondent data or personal identifiers, and that I may use them." Accept only a clear yes. Do not copy staff phone numbers or names from a shared protocol unless asked.
3. **Read the form as Markdown, in pieces** (`references/question-guidance.md`): convert with `markitdown`, reduce with `scripts/pick_columns.sh`, read about 150 rows at a time. No custom Python reads files.
4. **Collect protocol details** with `references/manual-structure.md`: ask for each applicable section, three or four questions per turn. Use what the team shared first. Offer the wiki guidance as a starting point and label it so.
5. **Draft** into `manual-draft.md`, section by section. Show only a one-line summary of each finished section, not the text. Use `[TO CONFIRM: ...]` for every gap. Copy consent text only from the approved form.
6. **Check** by reading, with `references/manual-check.md` and `scripts/unmentioned.sh manual-draft.md survey.md`. Fix every gap. Look at each question not mentioned.
7. **Deliver:** Markdown first, then Word with `pandoc manual-draft.md -o manual.docx` (or the docx skill). Give the team both. List every open `[TO CONFIRM]` item and the follow-ups: the training plan (`enum-training-plan`), and updating the manual after the pilot.

## Keep it light

Load each reference once. Work in the file. Do not paste the reduced form or the full manual into chat. Do not restate guidance.
