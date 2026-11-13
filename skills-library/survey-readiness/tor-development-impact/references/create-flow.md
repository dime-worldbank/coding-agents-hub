# Creating a TOR from the template

Start from `assets/tor-template.md`. It is the Development Impact reference TOR with `[[placeholders]]` for details the team supplies. Copy it to the project folder as `tor-draft.md`, delete the instruction block (everything above the line `END OF INSTRUCTIONS`), and edit the copy. Never edit the template.

## Keep what is standard

Keep the standard text unless the team gives a reason to change it: the Development Impact paragraph in Section 1, the training components, Section 7 (confidentiality, ownership, re-use), Section 8 (ethics), the integrity clause, and Annex C.1. If the team changes standard text, say so in one line ("Standard text changed: ...") and ask them to confirm.

## What to ask, in this order

Ask only what the draft still needs. Use tappable questions where available, with free text allowed. Never assume or invent a detail.

1. **Who hires the firm:** the World Bank, or a government, ministry, or statistics office. This changes Sections 7 and 9 (see below).
2. **The study:** what is evaluated, in which country, which round (baseline, midline, follow-up).
3. **Instruments:** each instrument, its respondent, its length, and the number of interviews. Sampling unit (schools, households, firms).
4. **Place and time:** districts or regions, month of data collection, mode (face-to-face or phone), who buys the SurveyCTO server.
5. **Activities:** show the five standard activities (permits, translation and pilot, field procedure plan, recruitment and training, data collection). Ask which to keep, edit, or remove, and whether there is a later phase or a panel. Offer to edit any activity through chat.
6. **Dates:** each deliverable date, work start, work end, contract end.
7. **Qualifications and selection criteria:** country and sector wording, languages, panel experience, and the weights.
8. **Payment:** milestones and shares. Show the reference split only as an example, and ask.
9. **Quality figures:** pilot size, reserve enumerators, spot-check and re-visit percentages, and the research team's own check share. Show the reference figures only as examples.

## Editing

- Work one section at a time. Replace placeholders in the file. Show only the changed section in chat, not the whole TOR.
- Keep numbering consistent. If an activity is added or removed, update Section 3, the deliverables table, and the payment table together.
- Remove every `[[OPTIONAL: ...]]` block the team does not want. Keep the ones it does, without the marker text.
- Remove drafting notes (lines starting `> Drafting note`) once the point is settled.
- After each section, say how many placeholders remain.

## If a government or statistics office hires the firm

Do not use the "property of the World Bank" wording in Section 7 or the Bank wording in Section 9 without asking. Ask what the recipient's contract says on data ownership, confidentiality, ethics, and security. The TOR must give the research team written access to the data, the instrument, quality-check outputs, and field reports. Ask which procurement rules apply and whether the timeline allows for them.

## Finish

1. Run `python scripts/check_tor.py tor-draft.md` (add `--recipient-executed` for a government hire). Fix every FAIL and MISSING. Look at each CHECK.
2. Run `node scripts/md_to_docx.js tor-draft.md tor.docx` to make the Word file. If the docx package is missing, use `pandoc tor-draft.md -o tor.docx`.
3. Convert the Word file back to Markdown (`markitdown tor.docx -o check.md`, or `extract-text`) and run `check_tor.py` on that, to confirm nothing was lost.
4. Give the team the Word file and the Markdown file, and list any open decisions.
