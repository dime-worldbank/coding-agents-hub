# TOR for Development Impact Surveys

`tor-development-impact` is a reusable AI-agent skill for creating and reviewing the terms of reference (TOR) used to hire a survey firm for a Development Impact survey.

**Scope:** Development Impact. It uses the standard Development Impact TOR text, adapted from a completed project TOR.
**Status:** draft for feedback.

It does two things:

| Task | What you get |
|---|---|
| Create a TOR | The standard template, updated in conversation with you: project description, instruments, timeline, activities, qualifications, payment, and selection weights. A Word file and a Markdown file. |
| Review a TOR | Mandatory, Priority, and Suggested changes, with a verdict, for a TOR written from the template or from your own layout |

It is a drafting and review aid. It does not check procurement rules and is not legal advice.

## Suggested workflow

1. **Create** the TOR from the template. Tell the agent what to change. The standard activities stay unless you edit or remove them, and you can edit any of them in the chat.
2. **Check:** the agent runs the consistency checks on the draft (numbering, dates, payment shares, selection weights, required clauses).
3. **Review** the Word file with your team, procurement, and Impact Analytics.
4. After edits outside the chat, ask the agent to **review** the TOR again before it goes out.

## Quick start

Copy the complete `tor-development-impact/` folder into your project's skills directory, or upload it as a zip. Do not copy only `SKILL.md`: the skill also needs `assets/`, `references/`, and `scripts/`.

```text
your-project/
└── .agents/
    └── skills/
        └── tor-development-impact/
```

Then prompt the agent:

```text
Read .agents/skills/tor-development-impact/SKILL.md and use it to create a TOR
for our [SURVEY] in [COUNTRY].
```

Or: "review this TOR" with the file attached.

## How it works

1. **Questions:** The agent asks whether you are creating or reviewing, and who hires the firm (the World Bank, or a government or statistics office). Free text is accepted.
2. **Confirmation:** It asks you to confirm you may share the documents.
3. **Create:** It edits a copy of the template one section at a time, shows only the changed section, and never invents a detail. Anything you have not said stays a bracketed placeholder.
4. **Check and deliver:** It runs the checks, fixes what it can, and gives you the Word and Markdown files with a list of open decisions.

## Understanding a review

| Verdict | Meaning |
|---|---|
| Not ready | At least one mandatory change. |
| Ready with fixes | No mandatory changes, but priority ones. |
| Ready | Only suggestions, or nothing. |

Each item says whether the agent can apply the fix: `Yes` (clear from the TOR), `Conditional` (you must decide or supply something), or `No` (a procurement or method decision). For Conditional items the report has a copy-and-edit form. Reply with `approve`, `change: [alternative]`, `provide: [information]`, `defer`, or `discuss`:

```text
1: provide: contract value is USD 80,000
3: defer
```

A blank or unclear response stays unresolved.

## What the checks cover

- Placeholders or drafting notes left in the text.
- All required sections present.
- Every activity has a deliverable and a payment milestone, and the numbers match across the duties, the deliverables table, and the payment schedule.
- Payment shares and selection weights add to 100, and subtotals agree.
- Deliverable dates sit inside the work period, and the contract does not end before the work.
- Percentages for spot checks and re-visits, listed so you can reconcile them.
- Required clauses: ownership, data security, consent, review board, reserve enumerators, daily upload, weekly reports, and remedies for integrity failures.
- Judgment checks by the agent: scope, field procedure plan, training, data deliverables, devices, and consistency with your sampling, pilot, and quality plans.

## If a government or statistics office hires the firm

The template is written for a firm hired by the World Bank. The agent asks what the recipient's contract says on data ownership, confidentiality, ethics, and security. It does not reuse the World Bank wording without asking.

## Requirements

- **Reading a Word TOR:** convert it to Markdown first with `markitdown` (or `extract-text` or `pandoc`). Nothing here parses Word files with code.
- **Checks:** Python 3 for `check_tor.py`, which reads Markdown only and does arithmetic: shares, weights, dates.
- **Word file:** Node.js with the `docx` package (`md_to_docx.js`). In the Claude app this is available when code execution and file creation are on. If it is missing, `pandoc` makes a plainer Word file.
- Without code execution the agent can still draft and review in the chat, but it cannot run the numeric checks or make the Word file.

## Limitations

- The template comes from one project TOR. Some wording, such as the activity list, suits school-based or household surveys. Edit or remove what does not fit.
- The single-source threshold and the privacy office approval rule were supplied by the review owner and have not been checked against a document.
- Dollar figures in the background paragraph are copied from the source TOR. Confirm they are current.
- The checker reads the template's layout. A TOR laid out very differently may need a manual check of the numbers. A Word TOR converted to Markdown can lose table layout, so check the converted tables.

## Folder contents

- `SKILL.md`: the instructions the agent follows.
- `assets/`: the template as Markdown (for editing) and Word.
- `references/`: how to create a TOR, the review checklist, and sources.
- `scripts/`: the consistency checker and the Markdown to Word converter.
- `tests/`: an invented filled TOR, a copy with planted errors, and `run_tests.py`.

## Feedback

Please send comments to Impact Analytics. Useful feedback includes TOR sections that do not fit your survey type, checks that should change tier, and wording that needs updating.
