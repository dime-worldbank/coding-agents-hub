# Survey Readiness

`survey-readiness` is a reusable AI-agent skill that helps project teams check their survey preparation before fieldwork. It covers timeline, ethics and data security, sampling, hiring a survey firm, pilot plan, questionnaire design, survey programming, enumerator training and field plan, and the data quality plan.

The skill is a first pass. It does not approve a plan. It reads files without changing them.

**Status:** draft for feedback. Criteria and tiers are being reviewed.

## Quick start

Copy the complete `survey-readiness/` folder into your project's skills directory, or download the skill as a zip. Do not copy only `SKILL.md`, because the skill also depends on its `references/` and `scripts/` folders.

For example:

```text
your-project/
└── .agents/
    └── skills/
        └── survey-readiness/
```

Then prompt the agent:

```text
Read .agents/skills/survey-readiness/SKILL.md and use it to check the survey
preparation files at [PROJECT PATH].
```

For selected files:

```text
Read .agents/skills/survey-readiness/SKILL.md and review only:

- [PATH TO FILE 1]
- [PATH TO FILE 2]

Treat this as a selected-areas review.
```

In the Claude app, upload the zip under Customize, then Skills, and turn it on. Code execution and file creation must be enabled. Check Anthropic's current documentation, as the steps change.

Before starting, move any respondent data or personal identifiers out of the folder. The agent must get your explicit confirmation before it reviews any file. Some apps show the agent a file as soon as you upload it, so check files before uploading them.

## How the review works

1. **Questions:** The agent asks for the stage, the areas to review, and the output you want. Free text is accepted.
2. **Files and confirmation:** The agent asks only for the files those areas need. It asks you to confirm the files hold no respondent data or personal identifiers. It reviews nothing until you confirm.
3. **Review:** The agent reads the matching reference file, then your documents. It does not edit files. It reports only what the files support.
4. **Report:** For each area, the agent gives a verdict and three lists of changes. It adds links and a closing note.
5. **Your decision:** You decide what to change. The skill does not apply anything on its own.
6. **Optional fixes:** If you ask, the agent applies clear, mechanical fixes to a copy and logs each change.

## Areas covered

| Area | What it checks |
|---|---|
| Timeline | Stage order, time to revise after the pilot, owners, buffer for delays, seasonal clashes |
| Ethics and data security | Approvals, consent content and fit with the form, recording consent, encryption, access to personal data |
| Sampling | Population and frame, unique IDs, seed set, code checked by a second person, power assumptions |
| Hiring a survey firm | TOR sections, Bank-executed or recipient-executed provisions, single-source guidance, device needs |
| Pilot plan | What the pilot tests, respondents outside the sample, final form on real devices, plan for recording changes |
| Questionnaire design | Link to outcomes, tested questions, wording, recall, sensitive topics, interview time on shortest and longest paths |
| Survey programming | Skip logic, unreachable questions, consent gate, encryption key, Style Guide conventions, `ietestform` results, comparison with the paper version |
| Training and field plan | Training components, tracking, back-checks, devices that meet SurveyCTO requirements |
| Data quality plan | Back-checks, high-frequency checks (missing core checks are listed), owners, thresholds, tools such as iehfc |

## Understanding the report

Each area gets one verdict:

| Verdict | Meaning |
|---|---|
| Not ready | At least one mandatory change. |
| Ready with fixes | No mandatory changes, but priority ones. |
| Ready | Only suggestions, or nothing. |
| Not assessable | Files are missing. The report says which. |

Verdicts cover only the files reviewed. They are not an approval.

Each area then has three lists:

| List | Meaning |
|---|---|
| Mandatory | Fix before fieldwork starts. |
| Priority | Likely to hurt data quality or cause rework. |
| Suggested | Good practice worth considering. |

Output options:

- **Key changes** (default): Mandatory and Priority.
- **Full review:** adds Suggested items, a short reason for each point, and sources.
- **Format:** in chat, Word, or an Excel checklist.

Every report also lists points that could not be checked, open questions for the team, links to relevant guidance, and a closing note.

### Example

*Illustrative only. The project is invented.*

**Ethics and data security: Not ready**

**Mandatory**
- *Approvals:* Data collection is Bank-procured, but the plan gives no privacy office approval status.
- *Approvals:* The form has an audio audit field, but consent does not mention recording (form row 18).
- *Field:* Encryption at rest is not enabled. It cannot be added to an existing form, so upload a new one.

**Priority**
- *Approvals:* Consent says 30 minutes, but the form also collects GPS and has four modules consent does not describe.
- *Field:* Name and phone fields are marked publishable (form rows 14 and 15).

**Suggested**
- Use a password manager and two-factor authentication for shared keys.

*For guidance on any of these points, you can reach out to Impact Analytics (dimeanalytics@worldbank.org).*

## Re-review

Upload revised files with the earlier report. The agent lists what is fixed, what is still open, and what is new.

## Limitations

- It checks only the files provided.
- It does not recompute power, approve ethics, or judge local logistics.
- It cannot run Stata. The team runs `ietestform` and shares its CSV report.
- The form checker reads XLSForms. Other platforms get a shorter, manual set of checks.
- Row colour coding and module prefixes in variable names are not checked. The XLSForm template and naming document have not been provided.
- Two rules come from the review owner and are not verified against a document: privacy office approval for Bank-procured data collection, and the USD 50,000 single-source threshold. Reports word them as guidance.
- Some sources are dated. See `references/sources.md`.

## Sources

Development Impact Wiki, DECDI research standards and consent templates, SurveyCTO documentation, the iehfc and ietestform tools, and Impact Analytics survey review resources.

`references/sources.md` lists each source with its date and status.

## Folder contents

- `SKILL.md`: the instructions the agent follows.
- `references/`: the criteria for each area, the intake questions, the report format, links, and sources.
- `scripts/`: the form checker.
- `tests/`: a form with planted errors (`planted-errors-form.xlsx`), a test TOR, a test DQA plan, and the expected findings for each (`expected-findings.md`).
- `evals/`: test prompts and checks, one folder per case.

## Feedback

Please send comments to Impact Analytics (dimeanalytics@worldbank.org). Useful feedback includes:

- Items that should move between Mandatory, Priority, and Suggested.
- Missing checks.
- Outdated criteria.
- Whether the report length and tone work for project teams.
