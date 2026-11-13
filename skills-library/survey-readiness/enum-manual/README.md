# Enumerator Manual

`enum-manual` is a reusable AI-agent skill for writing an enumerator manual (field manual). It reads your programmed form, asks you for the details only your team knows, and drafts the manual section by section. It never invents a protocol.

**Scope:** universal. It follows Development Impact Wiki guidance on what a field manual contains, and a worked field protocol example for records retrieval.
**Status:** draft for feedback.

| What you give | What you get |
|---|---|
| Your programmed form, any protocols or TOR, and answers to its questions | A manual in Markdown and Word: objectives, roles, protocols, tablet instructions, question-by-question guidance, key terms, FAQs, and escalation |

Anything you have not told it stays a visible `[TO CONFIRM]` note.

## Suggested workflow

1. Finish the programmed form, or a stable draft.
2. Run this skill. Answer the questions section by section.
3. Review the draft with the survey firm and supervisors. Resolve the `[TO CONFIRM]` items.
4. Plan the training around the manual (see `enum-training-plan`).
5. Update the manual and its FAQs after the pilot and again after training.

## Quick start

```text
your-project/
└── .agents/
    └── skills/
        └── enum-manual/
```

```text
Read .agents/skills/enum-manual/SKILL.md and use it to write the enumerator manual
for our [SURVEY]. The programmed form is at [PATH].
```

Before starting, make sure the form and any protocols you share hold no respondent data or personal identifiers. The agent asks you to confirm.

## How it works

1. **Questions:** survey type, mode, language, and what you can share. Free text is accepted.
2. **Confirmation:** you confirm the files hold no personal data.
3. **Form:** the form is converted to Markdown and cut down to the columns that matter (type, name, label, relevant, constraint, required), then read about 150 rows at a time. The agent never loads the whole workbook.
4. **Details:** the agent asks for each applicable section, a few questions per turn.
5. **Draft:** it writes the manual to a file and tells you only a one-line summary per section.
6. **Check:** the agent checks the draft by reading: required sections, protocol topics, module coverage, and open items. A small shell script lists the form questions the manual does not mention.

## What the check reports

Missing sections. Form modules the manual does not cover. The questions the manual does not mention by name. Protocol topics not covered (consent, respondent selection, refusals, replacement, revisits, upload and backup, confidentiality). Open `[TO CONFIRM]` items.

## Requirements

- **No custom Python.** The form is converted to Markdown with `markitdown` (or `extract-text` if it fails) and read as Markdown. `scripts/pick_columns.sh` and `scripts/unmentioned.sh` are small shell scripts that change no file.
- **Word file:** `pandoc` or the docx skill. The manual is written as Markdown first.
- Without code execution the agent can draft from what you paste, but it cannot convert the form.

## Limitations

- It writes the manual from your answers and files. It does not know your protocols.
- Consent text must come from your approved consent form.
- The worked example is a records retrieval protocol. Interview surveys use the same structure with different protocol content.
- A manual that describes questions in groups will show a lower mention rate. That is not an error.
- There is no script to match questions for the agent. It reads the reduced form and the draft. On a large form that takes many chunks and a lot of tokens.

## Folder contents

- `SKILL.md`: the instructions the agent follows.
- `references/`: the manual structure, how to describe the questions, and how to check the manual.
- `scripts/`: `pick_columns.sh` (keeps the columns that matter from the converted form) and `unmentioned.sh` (lists questions the manual does not mention).
- `tests/`: a sample form with its Markdown version, a complete and an incomplete sample manual, and `check_scripts.sh`.
- The earlier Python scripts are in `archive/old-scripts/enum-manual-python/` at the top of the repository. They are not used.

## Feedback

Please send comments to Impact Analytics. Useful feedback: sections your manuals always need that are missing, and protocols the questions should cover.
