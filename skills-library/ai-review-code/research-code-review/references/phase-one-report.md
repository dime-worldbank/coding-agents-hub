# Phase 1 Report

Begin with a brief **Review scope and limitations** section. Then present the
findings and recommendations table.

## Required structure

### Review scope and limitations

Include:

- review type: **Complete package** or **Selected files**;
- files and directories reviewed;
- languages and research tasks detected;
- presence of a README and entry point when reviewing a package;
- excluded files or components;
- data, execution, tests, and outputs not examined;
- any uncertainty about intended behavior.

State explicitly that Phase 1 is a static review and does not establish
computational reproducibility.

If the reviewed scope contains no readable code files (empty package, all
files excluded for privacy, or all files unreadable), state that explicitly
instead of producing a findings table, and ask the user how they would like to
proceed.

### Flags and recommendations

Sort findings by severity: Critical, High, Medium, then Low. Within a severity,
follow execution order when it can be inferred.

| ID | Flag | Severity | Code location | Recommendation | AI implementation | Proposed next action |
|---|---|---|---|---|---|---|
| e.g. `STAB-011` | Concise evidence-based finding | Critical / High / Medium / Low | `path/file.ext:line` | Specific best-practice response | Yes / Conditional / No | Concrete edit, decision, and validation plan |

The **Flag** cell must state what was observed and the concrete concern. Use
`Possible:` when the evidence is incomplete. The **Recommendation** cell must
state when researcher judgment is required. Consolidate repeated instances
when they share one cause, while listing representative locations. Copy the
**ID** and **AI implementation** values directly from `review-flags.md` or
`languages.md`; do not infer a new value.

Use **Proposed next action** to make the path after Phase 1 explicit without
implying that editing or execution has already been authorized:

- For **Yes**, state the concrete edit, the likely files or locations, and how
  the change should be validated.
- For **Conditional**, state one evidence-supported proposed choice and what
  will be changed if the user approves it. If the evidence does not support a
  single choice, ask the precise question or request the exact value needed,
  then state what will happen after the answer.
- For **No**, state the researcher, privacy, or methodological decision that
  must occur. Do not present it as part of straightforward implementation.

After the table, summarize applicable findings under these labels without
repeating the full recommendations:

- **Ready to implement (`Yes`):** list the IDs.
- **Awaiting approval or input (`Conditional`):** list each ID with the
  proposed choice or unanswered question.
- **Researcher-led (`No`):** list the IDs excluded from the implementation
  offer.

### Conditional decision form

When at least one `Conditional` finding exists, include a prefilled plain-text
form that the user can copy, edit, and return. Customize one block per finding;
do not leave generic IDs or recommendations in the delivered form.

```text
CONDITIONAL DECISIONS

How to respond

- approve
- change: <describe the alternative>
- provide: <enter the requested value, definition, or source>
- defer
- discuss

You may also answer directly when the requested information is clear, such as
seed = 12345.

<ID> — <short title>

Agent recommendation or information needed:
<prefilled recommendation, question, or requested value>

Your response:


VERSION CONTROL — complete only if asking the agent to edit

Is this project tracked with Git? If so, should I make the changes on a new
branch so you can review the complete diff?
Your response:
```

Explain the accepted responses once at the beginning of the form, as shown
above. Do not repeat the options under each finding. Interpret them as follows:

- **approve:** implement the exact proposed choice;
- **change:** implement only the alternative written after `change:`;
- **provide:** use the supplied value, definition, or authoritative source;
- **defer:** make no change for that finding;
- **discuss:** explain the options before any decision or edit.

Also accept concise natural-language replies such as `DATA-003: approve`,
`STAB-001: seed = 12345`, or `CLEAN-003: defer`; completing the full form is
optional. Do not include `No` findings as approval choices. Blank, ambiguous,
or contradictory responses remain unresolved. Only an explicit `yes` to the
Git question permits editing; a blank, `no`, or unclear response does not.

If there are no findings, say:

> No actionable flags were identified within the reviewed scope. This does
> not establish computational reproducibility because the code and outputs
> were not executed.

### Next step

End with:

> Would you like to make these changes yourself, or would you like me to
> implement the ready (`Yes`) actions? You may also approve any clearly stated
> `Conditional` proposal by ID, approve all such proposals together, or copy,
> complete, and return the Conditional decision form. Please answer the listed
> question for any Conditional item that does not yet contain one complete
> proposed choice.

Exclude `No` findings from the implementation offer. Do not describe any
action as approved until the user explicitly selects it.

## Recommendation quality

Every recommendation must be:

- traceable to a rule in `review-flags.md` or `languages.md`;
- supported by evidence in the reviewed code;
- relevant to the project and proportionate to the risk;
- specific enough to act on;
- clear about what was not verified.
