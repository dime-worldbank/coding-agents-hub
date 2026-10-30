---
name: research-code-review
description: Review research code or complete research-code packages for correctness, stability, reproducibility, privacy risks, and maintainability. Use for read-only Phase 1 reviews of Stata, R, Python, or other languages, and for user-approved follow-up fixes. Do not list, open, or read any file in the package — not even filenames — until the privacy confirmation in this skill has been obtained.
---

# Research Code Review

Review research code in two phases: first produce an evidence-based, read-only
assessment; then, only if requested, implement approved straightforward fixes.
Do not turn stylistic preferences into findings. Every flag and recommendation
must be supported by the bundled references and by evidence in the code.

## Privacy gate

Before reading or listing filenames, code, documentation, configuration, or data, ask:

> Before I inspect this code or package, please confirm that it contains no
> private, confidential, restricted, or personally identifying data and that I
> may proceed. If you are uncertain, move the data files out of this folder and I can
> perform a code-only review.

Treat only an unambiguous affirmative ("yes," "confirmed," "no private data")
as consent. Treat a hedge such as "probably fine," "should be okay," or "I
think so" the same as a "no": do not proceed, and repeat the offer to move
data files out of the folder for a code-only review.

Wait for explicit confirmation. If the user cannot confirm, do not inspect the
package. Explain how to move data files out of the review folder and offer to resume with code and
documentation only. The confirmation permits inspection, not execution or
modification.

## Phase 1: read-only review

Do not modify files, run project code, install dependencies, or reproduce
outputs in Phase 1.

1. After the privacy gate is confirmed, inventory the files in scope. Identify
   languages, the README, entry-point script, dependency files, tests,
   scripts, and declared outputs. Do not open data files.
2. State the inferred scope when the user did not specify one. Distinguish a
   complete-package review from a review of selected files.
3. Read [references/review-flags.md](references/review-flags.md). Apply only
   flags relevant to the code and research tasks present.
4. Read the applicable sections of
   [references/languages.md](references/languages.md).
5. Trace orchestration from the entry point when possible. Inspect surrounding
   code before flagging a pattern, and account for guards, assertions, comments,
   and validations elsewhere in the package.
6. Record evidence with the narrowest useful file and line location. If a risk
   depends on unavailable data, execution, outputs, or research intent, report
   it as a limitation or question rather than a confirmed failure.
7. Produce the report specified in
   [references/phase-one-report.md](references/phase-one-report.md). Do not add
   a checklist table, PDF, or unsupported numerical score.

### Severity

Assign severity by consequence, evidence, scope, and detectability:

- **Critical:** confirmed privacy exposure, credentials, destructive behavior,
  data corruption, or materially invalid research results.
- **High:** a strong risk of incorrect results or an inability to reproduce a
  consequential workflow.
- **Medium:** material fragility, missing validation, portability problems, or
  maintainability issues not shown to make current results wrong.
- **Low:** localized readability, consistency, or formatting issues.

Do not raise severity because a fix is difficult. Repetition alone does not
make a style issue Critical or High. When evidence is insufficient, qualify the
finding or report a limitation.

## End Phase 1

After presenting the complete report, end with the closing question specified
in [references/phase-one-report.md](references/phase-one-report.md).

Offer implementation only for changes whose intended behavior is clear.
Sampling, treatment assignment, observation exclusions, imputation,
winsorization, variable definitions, and statistical specifications require a
researcher decision.

## Phase 2: optional implementation

If the user asks the agent to make changes, first ask:

> Is this project tracked with Git? If so, should I make the changes on a new
> branch so you can review the complete diff?

If the user already answered the Git-tracked question `yes` in the Phase 1
decision form, do not ask that part again — still ask about the branch before
editing. Treat only an explicit affirmative as confirmation for each part. If
the tracked-with-Git response is blank, `no`, uncertain, or otherwise not
affirmative, do not edit any file; explain that a local diff is possible
without Git and recommend establishing version control, and that
implementation will remain paused until the user confirms Git tracking or
accepts an untracked local diff. Do not initialize a repository or create a
branch unless the user affirmatively asks for that.

Phase 2 may run the specific affected script to confirm a fix behaves as
intended, when execution is low-risk and the user has approved it. Do not run
the full pipeline or reproduce all declared outputs unless the user
separately asks for that.

Agree on which recommendations to implement. A blanket approval such as "do
the straightforward ones" covers only `Yes` items. The user may approve a
clearly stated `Conditional` proposal by ID or approve all such proposals
together. When a Conditional proposed next action states one unambiguous
behavior and the user approves it, treat that approval as establishing the
intended behavior and do not ask the same question again. If the report instead
asks for a missing value or a choice among alternatives, obtain that answer
before editing. Interpret decision-form responses as follows: `approve`
authorizes the exact proposal; `change:` authorizes only the written
alternative; `provide:` supplies the stated prerequisite; `defer` authorizes
no change; and `discuss` requests explanation before a decision. A direct
answer to a requested value or question also supplies that prerequisite.
Accept equivalent natural-language replies. Leave blank, ambiguous, or
contradictory items unresolved and ask only for the missing clarification.
Make only the approved changes, preserve research decisions, and validate in
proportion to risk. Report changed files, verification performed, remaining
limitations, and any recommendations left for the researcher.

## Entry-point assets

The files in `assets/` are optional World Bank reproducibility templates:

- `assets/main.do`
- `assets/main.R`
- `assets/main.py`

Use them only when the user asks to create or replace an entry-point script. Adapt
paths, dependencies, and pipeline steps to the project; do not impose their
exact structure as a review requirement.
