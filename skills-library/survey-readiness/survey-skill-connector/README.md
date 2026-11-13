# Survey Skill Connector

`survey-skill-connector` is a small AI-agent skill that points a survey preparation request to the right skill and carries shared project details between them, so your team is not asked the same question twice.

**Scope:** universal.
**Status:** draft for feedback.

| What it does | How |
|---|---|
| Routes a request | A table of requests and skills, and the suggested order of preparation |
| Carries details | A short `project-brief.md` that each skill can read and add to |
| Covers gaps | Pointers for ethics, sampling, pilot, questionnaire design, and the data quality plan, which no skill covers yet |

It does not do the other skills' work. If the right skill is not installed, it says so and stops.

## Suggested workflow

1. Start here: "where do I begin?" or "what next?"
2. The agent creates a project brief and fills in only what the next skill needs.
3. It routes you to the skill. That skill reads the brief.
4. When the skill finishes, the agent updates the brief and suggests one next step.

## The skills it connects

| Skill | Does |
|---|---|
| `xlsform-paper-sync` | Reviews forms, compares paper and programmed versions, creates one from the other |
| `survey-prep-timeline` | Plans every step and builds a timeline |
| `tor-development-impact` | Creates or reviews a TOR (Development Impact) |
| `enum-manual` | Writes the enumerator manual |
| `enum-training-plan` | Plans the training and testing |
| `hfc-plan` | Data quality plan. Planned, not available yet |

Install only the skills you need. Each works alone.

## The project brief

One short file of `key: value` lines in your project folder. Blank means not given. It holds no personal data, phone numbers, or emails. `python scripts/brief.py check` lists what is still empty. Fields and rules are in `references/project-brief.md`.

## Quick start

```text
your-project/
└── .agents/
    └── skills/
        └── survey-skill-connector/
```

```text
Read .agents/skills/survey-skill-connector/SKILL.md. We are preparing a survey in
[COUNTRY]. What should we do next?
```

## Requirements

Python 3 for the brief tool. Without code execution the agent can still route, and can keep the brief as text in the chat.

## Limitations

- The pointers for ethics, sampling, and pilot are not reviews.
- Wiki pages linked in the pointers can be old. Some are dated 2023.
- The brief is only as current as the last update. Skills confirm a value before relying on it.

## Folder contents

`SKILL.md`, `references/` (routing and the brief), `scripts/brief.py`, `tests/`.

## Feedback

Please send comments to Impact Analytics.
