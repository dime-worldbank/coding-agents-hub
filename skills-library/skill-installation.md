# Skill Installation

Skills are installed by simply copying them to your project folder. If needed, this can be done manually as the agents will find the skills if they are in the right place. However, for ease of installation and keeping them up to date as the source is updated, we recommend using a tool. 

## Manual Installation

While this is not the recommended approach, it is still covered as it is a great fallback if the skill you want is not available for installation via tools. Also, knowing how skills are installed manually can be helpful for troubleshooting if you are having issues with the installation tools.

### Common Project Skill Locations by Agent

Different agents look for skills in different locations. However, this mainly matters for how efficiently they can find them. If the path matches the format expected by the agent you are using, it will always be directly available to the agent. If not, the agent will have to spend time and tokens searching for the skill.

| Agent | Typical project skill location |
|---|---|
| Claude | `<project-root>/.claude/skills` |
| GitHub Copilot | `<project-root>/.github/skills` |
| Cursor | `<project-root>/.cursor/skills` |
| Codex | `<project-root>/.codex/skills` |

### Skill Folder Structure

Within the skills folder above, each skill should be in its own folder named after the skill. The skill folder must contain a `SKILL.md` file with the main instructions. Many skills also include optional files that the agent will use as needed. For example:

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for the agent to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script the agent can execute
```

### Manual Installation Steps

Simply copy the skill folder into your project skills folder location.

## VS Code Skill Manager Extension

If you are comfortable using command line tools, we recommend skipping to the next section and using the npx skill CLI tool for installation and maintenance. This has already been established as the standard approach to install skills, and the VS Code extensions are a layer on top of the same CLI tool.

There is no established standard for how to install skills directly in VS Code, as the early adopters of agents tend to be computer scientists who are comfortable with command line tools. Therefore, it is especially likely that the VS Code tools we currently recommend below will be replaced by another extension or built into the functionality of the agent extensions themselves.

A currently common tool for skill installation in VS Code is `Copilot MCP + Agent Skills Manager`. This extension allows you to search for skills in the marketplace and install them directly from VS Code. It also allows you to manage your installed skills and keep them up to date.

If you are choosing another tool, we recommend checking the download statistics and reviews to ensure it is widely used and trusted by the community.

### Copilot MCP + Agent Skills Manager

TODO: How to use

## npx skill Installation

This is the approach we currently recommend as long as you are comfortable with CLI tools. We recommend it because it is already an established standard practice. Below is a quick reference for the most common installation and maintenance commands. For full installation and maintenance instructions, see [https://www.skills.sh/docs/cli](https://www.skills.sh/docs/cli).

### Prerequisites

- Node.js and npm installed
- Access to the target GitHub repository
- A local folder where your agent looks for installed skills

### Install a Skill From GitHub

Run the installer directly without global setup:

```bash
npx skill install <github-org>/<repo>
```

Check installed skills:

```bash
npx skill list
```

Update installed skills:

```bash
npx skill update
```

