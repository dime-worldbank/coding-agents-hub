---
name: xlsform-paper-sync
description: "Review, compare, and create survey forms (XLSForm: SurveyCTO, ODK, Kobo). Use whenever the user has a programmed form or a paper, Word, or Excel questionnaire to check, compare, or convert: review a form's name, label, relevant, and constraint columns; compare paper and programmed versions (flow, wording, choice lists, skip logic, constraints); create a form from paper (needs the SurveyCTO skill); create paper from a form. Converts files to Markdown first and works from the Markdown. Reads files without changing them."
---

# XLSForm and paper sync

Scope: universal. Best practices (including the ietestform tests) are on by default. The Impact Analytics SurveyCTO Style Guide is optional (`references/style-guide.md`).

First-pass checker and drafting aid. It does not approve a form or replace a pilot. Write short sentences. Give each point an issue, a place, and a fix. Never assume. Ask.

## How it works

No custom Python reads or writes documents. Convert every shared file to Markdown and always work from the Markdown. Write every output as Markdown first, then convert to Word or Excel. Details and commands: `references/reading-files.md`.

The form review focuses on the **name, label, relevant, and constraint** columns (with `type`, `calculation`, and the `choices` sheet for lists).

## Four tasks

| Task | Method |
|---|---|
| Review a form | `references/four-columns.md`, then `programming-flags*.md` and `ietestform-rules.md` for a full review |
| Compare paper and form | `references/comparison-method.md`: a ledger, module by module |
| Create a form from paper | Needs the SurveyCTO skill. Write Markdown tables, then convert to xlsx (`references/authoring.md`) |
| Create paper from a form | Write Markdown, then convert to docx (`references/authoring.md`) |

Read `project-brief.md` first if it exists (languages, platform, Style Guide). Load only the reference the task needs, once.

## Step 1: Ask

Tappable questions if available (ask_user_input), always with free text. One turn, skipping what is known:
1. Task (one or more of the four).
2. Files: programmed form, paper version (Word, Excel with a tab per module, PDF), approved or still changing.
3. Output: key changes in chat (default) or full review; discrepancy table as Excel (default) or Word.
4. Reviews: platform, whether personal data are collected, stage, whether the team follows the Style Guide.

## Step 2: Confirm the files are safe

Before reading any file, ask: "Please confirm these files contain no real respondent data or personal identifiers, and that I may review them." Accept only a clear yes. If a file holds respondent data, stop and say so. If an app already shows the file on upload, say so, do not analyse it until confirmed, and never repeat personal data.

## Step 3: Convert, reduce, work

1. Convert each file to Markdown (`markitdown`, with the fallbacks in `reading-files.md`). Say which converter you used.
2. Reduce the form with `scripts/pick_columns.sh`. Never read the whole converted form.
3. Work in chunks of about 150 form rows or one or two paper sections. Write findings into a working file before the next chunk. Never rely on memory across chunks.
4. **Review:** apply `four-columns.md` to every chunk. **Compare:** keep the ledger and reconcile counts per module. **Create:** stop if the SurveyCTO skill is missing when creating a form.
5. Report each issue once. Use `Possible:` only where the files do not settle it. Merge repeats with example names.

## Step 4: Report

Use `references/report-format.md`. Verdict, then lists or tables. No internal IDs or severity words. Add "Not checked" (including which checks you did not run) and "Open questions for the team". For each item Claude could fix, say whether it can apply the fix: **Yes**, **Conditional**, or **No**. Offer the copy-and-edit response form for Conditional items. Write the discrepancy table as Markdown, then convert it to Excel. Give the team the Markdown too.

## Step 5: Fixes (only if asked)

Apply approved fixes to a new copy, written as Markdown first and then converted. Log each change (name, before, after). Constraint ranges, thresholds, and wording are the team's decisions. Review the result again. If tracked in Git, remind the team to commit the copy on a branch.

## Keep it light

Read the reduced form, never the whole file. Do not paste converted files into chat. Do not restate guidance. Do not say two versions match unless counts reconcile, every High row is resolved, and every check was done.
