# Survey skills

Reusable AI-agent skills for preparing a primary survey. Each skill stands alone. Install only what you need.

| Skill | Does | Scope | Status |
|---|---|---|---|
| `xlsform-paper-sync` | Reviews a form's name, label, relevant and constraint columns. Compares paper and programmed versions: flow, wording, choice lists, skip logic, constraints. Creates a form from paper (with the SurveyCTO skill) or paper from a form. Works from Markdown, no custom Python | Universal. Best practices on by default, Style Guide optional | Draft, one reading test on invented files |
| `survey-prep-timeline` | Lists every prep step and checks none is missing. Builds a timeline backward from the data collection start, or forward from what is done | Universal | Draft, built |
| `enum-manual` | Writes an enumerator manual from your form and your answers. Works from Markdown, no custom Python | Universal | Draft, built |
| `enum-training-plan` | Builds a training agenda, quiz and test plan, field practice plan, and selection steps | Universal | Draft, built |
| `tor-development-impact` | Creates a survey firm TOR from the standard template, edited in chat, or reviews a TOR | Development Impact | Draft, built |
| `survey-skill-connector` | Routes requests to the skills above and carries a shared project brief | Universal | Draft, built |
| `hfc-plan` | Data quality plan and high-frequency checks | Universal | Planned, on hold |

Scope labels: **universal** works for any team; **Development Impact** assumes Development Impact standards and templates; **WBG** would assume World Bank procedures (none yet).

## How they fit together

Start with `survey-skill-connector` if you are not sure where to begin. It creates a short `project-brief.md` that the other skills read, so you are not asked the same thing twice. Suggested order: objectives and sampling, ethics, questionnaire, pilot, programmed form (`xlsform-paper-sync`), TOR (`tor-development-impact`), manual (`enum-manual`), training (`enum-training-plan`), data quality plan. `survey-prep-timeline` runs through all of it.

Ethics, sampling, the pilot plan, and questionnaire design have no skill yet. The connector gives pointers.

## Keeping token use low

- Descriptions are about 70 to 80 words. Each `SKILL.md` is a short router of 350 to 750 words. References load only when the task needs them, once.
- `xlsform-paper-sync` and `enum-manual` convert files to Markdown and reduce the form to the columns that matter, so the agent never reads a whole workbook. They use no custom Python. The other skills use small Python scripts for dates, number checks, the agenda check, and the project brief. None of them reads or writes a Word or Excel file: they read text, Markdown, or JSON.
- Documents are written to files and shown in chat as one-line summaries.
- `python tools/check_budget.py .` counts the words each skill loads and flags any over the suggested budgets.

## Every skill (tests differ)

- Asks, never assumes. Questions are tappable multiple choice where the app supports it, with free text always allowed.
- Confirms that shared files hold no personal data before reading them.
- Has its own README with a suggested workflow, its own tests (`python tests/run_tests.py` in each skill folder, except `xlsform-paper-sync` and `enum-manual`, which have shell tests (`check_pick_columns.sh`, `check_scripts.sh`))

## Requirements

`markitdown` (or `extract-text`, `pandoc`, `pdftotext`) to convert files to Markdown. Python 3 for the small scripts in the other skills. Node.js with the `docx` package, or `pandoc`, for Word output. In the Claude app, code execution and file creation must be on. `xlsform-paper-sync` also needs the SurveyCTO skill to create a form: https://github.com/surveycto/surveycto-agent-skill

## Folders

`archive/survey-readiness-v1/` holds the earlier single skill. It is not part of the set. Its reference files cover ethics, sampling, pilot, questionnaire design, and the data quality plan, and are the source for the pointers in the connector. `archive/old-scripts/` holds the earlier form drafting scripts and the Python versions of the form checker, the comparison, and the manual tools, no longer used. `tools/` holds the budget checker.

## Not verified

The Style Guide checks that need the XLSForm template and the variable naming document are not built. The specification-style paper reader is based on one sample layout. Wiki pages dated 2023 to 2024 may be out of date. The USD 50,000 single-source threshold and the privacy office rule in the TOR review were supplied and not checked against a document.
