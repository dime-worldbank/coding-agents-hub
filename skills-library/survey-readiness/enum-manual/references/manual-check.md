# Checking the manual

Check by reading the draft. No script parses the manual. Say at the end which checks you did.

## Sections

The manual has a section for each of: study purpose and objectives; roles and responsibilities; survey protocols or field procedures; using the tablet or device; description of the questions; key terms; frequently asked questions; support and escalation. A missing one is a gap unless the team said it does not apply. Say which you dropped and why.

## Protocol topics

Check the protocols section covers, or the team says it does not apply: consent; respondent or unit selection; refusals and non-response; replacement; revisits or call-backs; data upload and backup; confidentiality. A topic that is not mentioned is a question for the team, not an error.

## Coverage of the form

1. Every form module (top-level group) has a heading or a clear section in the manual.
2. List the questions the manual does not mention:
   ```
   scripts/unmentioned.sh manual-draft.md survey.md
   ```
   It skips groups, notes, calculate fields and metadata fields, and counts a question as mentioned if its name appears as a whole word. A manual may describe several questions together. Look at each listed question and either add it, say it is covered by a group, or ask the team.
3. State the count: "11 of 11 questions mentioned" or "4 of 11. The rest are not described."

## Open items

Count the `[TO CONFIRM` notes with `grep -c "TO CONFIRM" manual-draft.md`. List them for the team, grouped by section. There must be no `[[double bracket]]` placeholder left.

## Report

Sections present and missing. Protocol topics not covered. Questions not mentioned. Open items. What you did not check (for example whether protocols are correct: only the team knows).
