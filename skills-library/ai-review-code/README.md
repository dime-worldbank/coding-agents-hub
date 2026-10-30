# Research Code Review

`research-code-review` is a reusable AI-agent skill for reviewing research code
and complete research-code packages for correctness, stability,
reproducibility, privacy risks, and maintainability.

The skill begins with a read-only review. It does not edit files, open data
files, install dependencies, or run project code during Phase 1.

## Quick start

Copy the complete `research-code-review/` folder into your project's skills
directory, or [download the skill](https://github.com/dime-worldbank/coding-agents-hub/releases/download/research-code-review-latest/research-code-review.zip) as a zip. Do not copy only `SKILL.md`, because the skill also depends on its
`references/` and `assets/` folders.

For example:

```text
your-project/
└── .agents/
    └── skills/
        └── research-code-review/
```

Then prompt the agent:

```text
Read .agents/skills/research-code-review/SKILL.md and use it to review the
research-code package at [PROJECT PATH].
```

For selected files:

```text
Read .agents/skills/research-code-review/SKILL.md and review only:

- [PATH TO FILE 1]
- [PATH TO FILE 2]

Treat this as a selected-files review.
```

Before starting, move any private, confidential, restricted, or
personally identifying data out of the project folder. The agent must obtain your explicit privacy
confirmation before listing or opening project files.

## How the review works

1. **Privacy confirmation:** The agent asks whether the review scope contains
   private, confidential, restricted, or personally identifying data.
2. **Phase 1 review:** The agent reviews the code and documentation without
   opening data files, running code, installing dependencies, reproducing
   outputs, or modifying files.
3. **Phase 1 report:** The agent reports the review scope and limitations,
   flags, severity, code locations, recommendations, AI implementation status,
   and proposed next actions.
4. **Your decision:** You decide which recommendations the agent may implement.
5. **Git confirmation:** Before editing, the agent asks whether the project is
   tracked with Git. Only an explicit `yes` permits changes.
6. **Phase 2 implementation:** The agent implements only approved actions,
   validates the changes, and reports what changed and what remains unresolved.

## Understanding the report

Each finding has one of three AI implementation categories:

| Category | Meaning |
|---|---|
| `Yes` | The intended behavior is established and the agent can implement the proposed action after approval. |
| `Conditional` | A specific approval, value, source, or decision is required first. |
| `No` | A researcher-led, privacy, or methodological decision is required. |

The report also states the proposed next action for each finding.

## Responding to Conditional findings

When Conditional findings exist, the report includes a copy-and-edit response
form. At the beginning of the form, the agent explains that you may respond
with:

- `approve`
- `change: [describe the alternative]`
- `provide: [enter the requested information]`
- `defer`
- `discuss`

Each Conditional finding then includes one response field:

```text
STAB-001 — Random seed

Agent recommendation or information needed:
Provide the seed or seed-selection policy that this workflow should use.

Your response:
```

You may complete the form or respond more concisely:

```text
STAB-001: seed = 12345
CLEAN-003: defer
```

A blank or unclear response remains unresolved.

## Code execution

Phase 1 is always static. The agent does not run code merely because the data
are public.

During Phase 2, the agent may run a specific affected script when execution is
low-risk and approved. Running the complete pipeline or attempting full
computational reproduction requires a separate explicit request.
