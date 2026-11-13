# Creating one version from the other

Claude writes the new version as Markdown first, then converts it. No custom Python is used. Never overwrite an input. Tell the team the output is a draft.

## Paper to programmed form

1. **The SurveyCTO skill is required.** Look in the available skills for a SurveyCTO skill (see `surveycto-skill.md`). If it is not installed, stop. Tell the team to install it from the link in `links.md` and do not draft the form.
2. Convert the paper to Markdown (`reading-files.md`). Read it one section at a time.
3. **Ask** (tappable, free text allowed, never assume): module prefixes; languages; whether consent text comes from an approved consent form; whether the team follows the Style Guide; whether to add GPS or audit paradata; whether any lists load from files.
4. Follow the SurveyCTO skill for syntax, field types, and the template. Apply the best practices in `four-columns.md`: numeric choice values, a consent gate before later modules, `start`, `end`, and `deviceid`, constraints from paper ranges, `relevant` from paper skip notes (mark each as to confirm).
5. Write the form as `form-draft.md` with three tables under the headings `## survey`, `## choices`, and `## settings`, using the same column headers as an XLSForm. In a Markdown table cell, write a pipe as `\|` and avoid line breaks. Keep `relevant` expressions starting with `${`, not `=`.
6. Count: questions on paper in, questions in the draft out. They must agree. List any that do not.
7. Review the draft with `four-columns.md`, then run the full comparison against the paper as a round-trip check.
8. Convert to `form-draft.xlsx` with the xlsx skill (exact sheet names and headers). Convert it back with `markitdown` and confirm the row counts match the draft.
9. The draft cannot know: the encryption key (set it **before the first upload**; it cannot be added later), constraint ranges the paper omits, calculations, and the contents of preload files.

## Programmed form to paper

1. Convert the form to Markdown and reduce it (`reading-files.md`). Read it module by module, with the choices.
2. Ask whether the team wants a respondent-style paper (wording and skip notes only) or a specification-style paper (also variable names, types, `Required`, constraints, appearance). The specification style compares most cleanly with the form.
3. Write `paper-draft.md`: one section per module, with number, question, answer options with codes, and skip notes. Write skip conditions in plain words ("Ask if Q3.1 is Yes"). Where a condition is too complex to put in words, print the expression and mark it [CHECK].
4. Count: form questions in, paper questions out.
5. Convert with `pandoc paper-draft.md -o paper.docx`, or the docx skill for a styled file. Render the file to an image and fix layout problems. Run the comparison as a round-trip check.

## After either direction

Offer the full comparison and the review on the result.
