# Reading and writing files: Markdown first

No custom Python reads or writes documents in this skill. Every shared file is converted to Markdown and read as Markdown. Every output is written as Markdown first and then converted to Word or Excel. The Markdown is the working copy.

## Convert what the team shares

1. Try `markitdown <file> -o <file>.md`. The Markdown Converter skill uses `uvx markitdown <file> -o <file>.md` and works the same way. It reads Word, Excel, PDF, and PowerPoint. In Excel files each sheet becomes a `## sheet name` heading with a table.
2. If markitdown fails (no network for `uvx`, or an error about a missing extra such as docx or pdf), use a fallback:
   - Word, Excel: `extract-text <file>`, or for Word `pandoc -t gfm --wrap=none <file>.docx -o <file>.md`.
   - PDF with a text layer: `pdftotext -layout <file>.pdf <file>.md`.
   - Scanned PDF: read the pages as images (see the pdf-reading skill). Do not report from a scan unless every page was read.
3. Say which converter you used. Check the result: count the questions per section and compare with what the file visibly holds. If a section is short, read that part again with a fallback converter.

In the environment this skill was tested in, markitdown read Excel and PDF but not Word (the docx extra was missing), and `uvx` had no network. The Word fallbacks worked.

## Reduce the form before reading it

A converted XLSForm has every column of every sheet. Do not read it whole. Keep the columns that matter:

```
scripts/pick_columns.sh form.md "type,name,label::<language>,relevant,constraint,required,calculation" survey > survey.md
scripts/pick_columns.sh form.md "list_name,value,label::<language>,filter" choices > choices.md
```

- Find the languages: `grep -m1 '^| type' form.md | tr '|' '\n' | grep -i label`.
- The focus is `name`, `label`, `relevant`, and `constraint`. `type` is kept so groups, select lists, and preload files can be read. `required` is kept for reviews and for papers that print it. `calculation` is kept because undefined references, outdated functions, and divisions by zero hide there. For a review of a multilingual form, also keep each other `label::<language>` column (to check translations exist) and `publishable` (personal data). Add `hint` or `appearance` only if the team asks.
- `#` counts the data rows in a sheet. The spreadsheet row is about `#` plus one. Locate an issue by its `name`, not its row.
- Read the helper's messages. "No column ..." means that check cannot be done from the reduced file. Never hide them. The choices sheet may call its value column `name` or `value`: the helper accepts either.
- `NaN` cells are blanked and escaped underscores are restored. The helper is plain shell and awk. It changes no file.

## Read in chunks

Read at most about 150 form rows, or one or two paper sections, at a time: `sed -n '1,150p' survey.md`. Write what you found into the working file before you read the next chunk. Keep every reading step in a file, not in your head.

## Write outputs as Markdown first

- Discrepancy tables, reports, paper questionnaires, and form drafts are written as Markdown files in the project folder.
- Then convert:
  - **Word:** `pandoc <file>.md -o <file>.docx`, or the docx skill for a styled file.
  - **Excel:** follow the xlsx skill, using the Markdown tables as the source. Sheet names and headers must match exactly. A form needs sheets named `survey`, `choices`, and `settings`.
- Check the result: convert the new file back with `markitdown` and confirm the row counts match the Markdown.
- Give the team the readable Markdown version too.

The conversion step is the only place a file is written. Do not write custom code to parse or rebuild the content.

## Privacy

The converted Markdown holds the same content as the source. Keep it in the project folder and do not paste it into chat.
