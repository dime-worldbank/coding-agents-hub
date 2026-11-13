# XLSForm Paper Sync

`xlsform-paper-sync` is a reusable AI-agent skill for checking and converting survey forms. It works with XLSForm files (SurveyCTO, ODK, KoboToolbox) and with paper questionnaires in Word, Excel (one tab per module is fine), or PDF.

**Scope:** universal. Development Impact best practices and the `ietestform` tests are built in and on by default. The Impact Analytics SurveyCTO Style Guide checks are optional.
**Status:** draft for feedback. Tested on invented files only. The new Markdown method has had one reading test, not a full evaluation.

It does four things:

| Task | What you get |
|---|---|
| Review a programmed form | Mandatory, Priority, and Suggested changes, with a verdict |
| Compare paper and programmed versions | A table of every discrepancy by section, as Excel: flow, wording, choice lists, skip logic, constraints |
| Create a form from a paper questionnaire | A draft XLSForm, written with the SurveyCTO skill, and a list of decisions for your team |
| Create a paper questionnaire from a form | A Word file, with skip logic in plain words |

It is a first pass and a drafting aid. It does not approve a form and does not replace a pilot. It reads files without changing them and writes only to new copies.

## Suggested workflow

1. **Draft the paper questionnaire** (or the form first, if that is how your team works).
2. **Create one from the other** if you want a starting point, then fix the draft with your team.
3. **Compare** the two versions. Fix every difference, or record why it is deliberate.
4. **Review the programmed form** before the pilot, and again after changes.
5. **Pilot**, then repeat steps 3 and 4 on the revised files.
6. Run the comparison one last time on the final files before fieldwork.

## Quick start

Copy the complete `xlsform-paper-sync/` folder into your project's skills directory, or upload it as a zip. Do not copy only `SKILL.md`: the skill also needs `references/` and `scripts/`.

```text
your-project/
└── .agents/
    └── skills/
        └── xlsform-paper-sync/
```

Then prompt the agent:

```text
Read .agents/skills/xlsform-paper-sync/SKILL.md and use it to compare the paper
questionnaire at [PATH] with the programmed form at [PATH].
```

Or say what you need: "does our form match the questionnaire?", "review my SurveyCTO form", "make a form from this Word questionnaire", "make a paper version of this form".

Before starting, make sure the files hold no respondent data or personal identifiers. The agent asks you to confirm before it reads anything. Some apps show the agent a file as soon as you upload it, so check files before uploading.

## Requirements

- **No custom Python.** Nothing in this skill parses or rebuilds documents with code of its own. Files are converted to Markdown with `markitdown` (the Markdown Converter approach: `uvx markitdown file -o file.md`). The agent works from the Markdown. Outputs are written as Markdown first and then converted.
- **Converters:** `markitdown` is the first choice. If it is not available, or fails on a file type, the skill falls back to `extract-text`, `pandoc`, or `pdftotext`. In the environment used for testing, markitdown read Excel and PDF but not Word (the docx extra was missing), and `uvx` had no network, so the Word fallbacks were used.
- **Column helper:** `scripts/pick_columns.sh` is a small shell and awk script that keeps only the columns that matter from a converted form. It changes no file.
- **Output files:** `pandoc` or the docx skill for Word. The xlsx skill for Excel. These are the only steps that write a file, and they write from the Markdown.
- **Claude app:** code execution and file creation must be switched on. Check Anthropic's current documentation for the steps. Without them the agent cannot convert files or create the outputs.
- **SurveyCTO skill (needed only to create a form):** SurveyCTO publishes an agent skill with SurveyCTO syntax and an XLSForm template: https://github.com/surveycto/surveycto-agent-skill. This skill will not draft a form without it. SurveyCTO says its skill suits desktop agents (Claude Cowork, Claude Code, Codex) and works best with its MCP server. Check your organisation's data security and AI policies before connecting any server.

## How it works

1. **Questions:** The agent asks what you need, what files you have, and what output you want. Free text is accepted.
2. **Confirmation:** It asks you to confirm the files hold no personal data. It reads nothing until you say yes.
3. **Check:** The agent converts the files to Markdown, reduces the form to the columns that matter, and reads them in chunks, keeping a ledger so nothing is skipped.
4. **Report:** You get a verdict (for reviews) or a table by section (for comparisons).
5. **Your decision:** Nothing changes until you approve it.
6. **Optional fixes:** Approved, mechanical fixes go into a copy. Each change is logged, and the checks run again.

## Understanding the report

**Review verdicts**

| Verdict | Meaning |
|---|---|
| Not ready | At least one mandatory change. |
| Ready with fixes | No mandatory changes, but priority ones. |
| Ready | Only suggestions, or nothing. |

Changes come in three lists: **Mandatory** (fix before fieldwork), **Priority** (likely to hurt data quality or cause rework), **Suggested** (good practice). Verdicts cover only the files reviewed. They are not an approval.

**Comparison results:** Not aligned, Aligned with minor differences, or Aligned (in the questions read). The report says how many questions were read on each side, which language was compared, and what was not checked.

## Whether the agent can apply a fix

| Category | Meaning |
|---|---|
| `Yes` | The intended behavior is clear from the form. The agent can fix it after you approve. |
| `Conditional` | You must decide or supply something first. |
| `No` | A design or method decision, such as a constraint range or question wording. |

For Conditional items the report includes a copy-and-edit form. Reply with `approve`, `change: [alternative]`, `provide: [information]`, `defer`, or `discuss`. A short reply works:

```text
1: provide: all except 2.4
3: defer
```

A blank or unclear response stays unresolved.

## The comparison in more detail

- **Two kinds of paper.** A *specification-style* paper prints variable names, field types, `Required`, and form expressions. It is matched by variable name first, then wording. A *respondent-style* paper has wording and skip notes only. It is matched by wording and order.
- **A ledger.** The agent works module by module. Every paper question and every form question gets a row: matched, differs, on paper only, or in form only. It checks that the counts reconcile for each module before it moves on.
- **Flow.** Judged by wording and order within each module. Question numbers are a weak signal.
- **Wording.** In the one language both files share. If several are shared, the agent asks which one.
- **Choices.** The options on paper are compared with the `choices` sheet rows for the list named in the `type` column: labels, values, order, and options on one side only. When a list loads from a file, the agent asks you to share that file. Until then it reports the list as not checked.
- **Skip logic and constraints.** The effective condition (group plus question) and the constraint are compared with the paper's rule. The agent decides whether two forms of the same rule route the same people.
- **Not compared:** calculate fields (unless asked), metadata fields, notes other than consent and introduction text, the contents of preload files, and other languages. The report says so.
- A scanned PDF cannot be converted to text. The agent reads the pages as images, or you provide the Word or Excel original.

## Creating one version from the other

- **Paper to form:** needs the SurveyCTO skill. The agent writes the form as Markdown tables (`survey`, `choices`, `settings`), applies the best practices, keeps the question count equal to the paper, and then converts it to xlsx. It runs the review and the comparison on the result as a check. Set the encryption key before the first upload. It cannot be added to an existing form.
- **Form to paper:** the agent writes the paper as Markdown, one table per module, then converts it to Word. You choose respondent style or specification style.
- Both are drafts.

## Optional Style Guide checks

Tell the agent your team follows the Impact Analytics SurveyCTO Style Guide. It then also checks white space between modules, lowercase names, special codes -99, -88, -9, the version format, and choice labels loaded by a calculate field. See `references/style-guide.md`.

## Limitations

- It checks only the files provided. It does not run your form on a server or test it on a device.
- It does not judge whether questions are well designed, only whether they match and are correctly programmed.
- **There is no script to count or match for the agent.** The agent does that by reading. On a large form that takes many chunks and a lot of tokens. The ledger and the count reconciliation are there to catch a skipped question. A mistake is still possible, so the report states which checks were run.
- The review focuses on the `name`, `label`, `relevant`, and `constraint` columns. Other columns (hints, appearance, translations into other languages, metadata fields) are read only if you ask.
- The `#` row number from the converted form is approximate. Issues are located by variable name.
- It does not estimate interview length. Ask the team for pilot timings.
- The form reduction helper can only keep columns that exist. If a column has a different header, the helper says it was not found.
- Blank rows between modules are not visible in the Markdown, so that Style Guide item cannot be checked this way.
- For other platforms (CSPro, Survey Solutions) the agent reviews only the platform-neutral items.
- Some sources are dated. See `references/links.md`.

## Folder contents

- `SKILL.md`: the instructions the agent follows.
- `references/`: reading and writing files as Markdown, the four-column review, the comparison method, the creation steps, the report format, the Style Guide, and links.
- `scripts/pick_columns.sh`: the column helper (shell and awk).
- `tests/`: invented paper and form files with planted differences, Markdown versions of each, the expected results, and a record of one reading test.
- The earlier Python scripts are in `archive/old-scripts/xlsform-python-v2/` at the top of the repository. They are not used.

## Feedback

Please send comments to Impact Analytics. Useful feedback includes:

- Discrepancies the comparison missed, or false alarms (send the question text, not respondent data).
- Paper layouts the reader could not parse.
- Checks that should move between Mandatory, Priority, and Suggested.
- Whether the report length and tone work for project teams.
