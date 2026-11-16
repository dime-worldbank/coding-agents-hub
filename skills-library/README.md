# Skills Library

This library curates AI coding skills and skill-adjacent resources for Bank teams working in Stata, R, and Python.

It combines:
- Internal resources in this hub (guides, templates, trainings)
- External skill libraries and vetted repositories

Use this catalog to find reusable skills by topic and language, then follow the [installation guidance](skill-installation.md) to install the skill in your project..


## Curated Skill Links

Entries with a pinned commit were statically reviewed at that commit (see [Vetting notes](#vetting-notes)). Install that commit rather than the latest version; newer versions have not been reviewed.

| Topic | Language | Skill Repo | Description | Pinned commit | External | 
|---|---|---|---|---|---|
| Coding | Stata | [dylantmoore/stata-skill](https://github.com/dylantmoore/stata-skill) | General Stata best practices to make code agents better at Stata. | — | Yes |
| Coding | Stata | [haoyu-haoyu/stata-ai-fusion](https://github.com/haoyu-haoyu/stata-ai-fusion/tree/aca70ed6976a338b728cb3be5622bffb9a1046fb) | MCP server + skill + VS Code extension that lets the agent run Stata (requires licensed Stata 17+). ⚠️ Alpha; the agent can execute arbitrary Stata/shell code and Stata output reaches the model. | `aca70ed` | Yes |
| Data | Multi | [worldbank/data360-mcp](https://github.com/worldbank/data360-mcp/tree/355e8a7c83480f1fc8e78bbe03fba658d2389989) | Official World Bank MCP server for Data360 indicators, including WDI. Lets agents pull real values instead of inventing them. MCP server, not a skill. | `355e8a7` | Yes |
| Economics | Multi | [dphdame/claude-code-econ-starter](https://github.com/dphdame/claude-code-econ-starter) | Starter kit for economists using Claude Code: CLAUDE.md template, verification checklist, and starter skills. | — | Yes |
| Econometrics | Multi | [JonasWeinert/EconAgentSkills](https://github.com/JonasWeinert/EconAgentSkills) | Opinionated agent skills for econometrics research: data, analysis, writing, and communication (DIME conventions). | — | Yes |
| Open source | Multi | [worldbank/open-source-kit](https://github.com/worldbank/open-source-kit/tree/fa91b8503d26c6d7dfb542a2ca2286a42d31c7cf) (`wbg-oss-review`) | Official World Bank skill that audits a repository against WBG open-source publication requirements. Optional GitHub Actions compliance workflow. | `fa91b85` | Yes |
| Reproducibility | Multi | [worldbank/wb-reproducible-research-repository](https://github.com/worldbank/wb-reproducible-research-repository/releases/tag/skill-v2026.09.25) | World Bank reproducibility skill release (`skill-v2026.09.25`) for Claude, Claude Code, and Copilot. Starts with a privacy gate and a code-only mode for confidential data. | `25c205b` | Yes |
| Reproducibility | Multi | [dime-worldbank/rrr-package-agent](https://github.com/dime-worldbank/rrr-package-agent/tree/9bfcfa4bacc2bf3270d47da9639b216544239d4f) | ⛔ **On hold.** Reproducibility Verification Team agent for reviewing PRWP reproducibility packages. Work in progress and not yet recommended for general use. | `9bfcfa4` | Yes |
| Slides | Multi | [dime-worldbank/ai-research-training (prepare-slides)](https://github.com/dime-worldbank/ai-research-training/tree/main/sessions/ai-skills-slides/skills/prepare-slides) | Skill for preparing research slides from the DIME AI research training materials. | — | Yes |
| Survey design | XLSForm | [surveycto/surveycto-agent-skill](https://github.com/surveycto/surveycto-agent-skill/tree/c6b1594fac1412dafbc5908eae8c6f268708348d) | Official SurveyCTO skill for designing, checking, and converting survey forms. ⚠️ Public beta; uploads forms to SurveyCTO's hosted MCP server. | `c6b1594` | Yes |
| Writing | Multi | [hanlulong/econ-writing-skill](https://github.com/hanlulong/econ-writing-skill/tree/f2bf7a22c5e3b37921a5e6c73bd1fb380a5e00e8) | Economics paper-writing guidance synthesized from 50+ writing guides (Cochrane, McCloskey, Shapiro, …). Prompt-only, MIT. | `f2bf7a2` | Yes |
| Skill index | Multi | [hanlulong/awesome-ai-for-economists](https://github.com/hanlulong/awesome-ai-for-economists/tree/e1406b3bd20a73b2d9f9624cacd85e27175dfc03) | Curated list of AI tools, skills, and resources for economists. Maintainers state they read each SKILL.md before merging. | `e1406b3` | Yes |
| Skill index | Multi | [meleantonio/awesome-econ-ai-stuff](https://github.com/meleantonio/awesome-econ-ai-stuff/tree/dd890d51c789fb8f8e316a2d7e4ed5d4bd793c50) | Small set of installable econ skills (Stata cleaning, `fixest` IV/DiD/RDD, panel data, API data fetching) plus links. | `dd890d5` | Yes |
| Skill index | Multi | [O0000-code/awesome-academic-skills](https://github.com/O0000-code/awesome-academic-skills/tree/5975c4ee37f01a8e20362d83a2ab3e92198c59ab) | Broad index of academic agent skills, labelling each entry's license and what it runs. Discovery only, not an approved list. | `5975c4e` | Yes |


## Vetting notes

Reviews were static: files were read, nothing was run or installed. A review covers only the pinned commit. Linking a skill index does **not** vet the entries it links to; review each third-party skill before installing it.

**[haoyu-haoyu/stata-ai-fusion](https://github.com/haoyu-haoyu/stata-ai-fusion/tree/aca70ed6976a338b728cb3be5622bffb9a1046fb)**: OK with caveats.
- The agent can run any Stata code, including `shell`/`!` commands and `net install` from any URL. Require approval for every tool call; never auto-approve.
- Everything Stata prints (including `list`, `codebook`, `inspect` output) is sent to the model provider. Do not use on confidential or PII data unless your agent is approved for it.
- The README installs the latest PyPI release (`uvx --from stata-ai-fusion`), not the reviewed commit. Pin the version.
- The VS Code extension writes your user-level `mcp.json` automatically by default. The bundled `stata-ai-fusion-skill.zip` is out of date; use `skill/SKILL.md` instead.
- Alpha (v0.3.0), single maintainer, MIT.

**[worldbank/data360-mcp](https://github.com/worldbank/data360-mcp/tree/355e8a7c83480f1fc8e78bbe03fba658d2389989)**: OK to list.
- Queries only public World Bank APIs; no user data leaves the machine. Telemetry is off unless configured.
- If you host it yourself, bind to `127.0.0.1` (defaults allow any origin and bind to `0.0.0.0`).
- Pre-1.0. MIT plus World Bank IGO Rider.

**[worldbank/open-source-kit](https://github.com/worldbank/open-source-kit/tree/fa91b8503d26c6d7dfb542a2ca2286a42d31c7cf)**: OK with caveats.
- The skill is read-only plus file edits it asks about first; it never commits or pushes.
- Its secret scan reads matched secret values into the model's context. Ask it to report file and line and mask values.
- The optional CI workflow references `@main` and third-party actions pinned to tags, not SHAs. Pin to a SHA if you adopt it, and do not use the `issue-pr-scan` sample on public repos (it echoes matched secrets into public logs).
- The trigger ("review my repo") is broad and may fire on ordinary code-review requests. MIT.

**[worldbank/wb-reproducible-research-repository](https://github.com/worldbank/wb-reproducible-research-repository/releases/tag/skill-v2026.09.25)** (`skill-v2026.07.14` → `skill-v2026.09.25`): OK to list.
- Adds a Phase 0 privacy gate and a code-only mode in which the data must be physically out of the agent's reach, plus local data-inventory scripts that record file metadata and variable names only.
- `assets/data_inventory.do` runs `net install` of `stata-shasum` from an unpinned GitHub branch.

**[dime-worldbank/rrr-package-agent](https://github.com/dime-worldbank/rrr-package-agent/tree/9bfcfa4bacc2bf3270d47da9639b216544239d4f)**: on hold.
- The headless runner starts Claude Code in `auto` permission mode with unrestricted shell and network access while running author-submitted package code. Its command blocklist is easy to bypass.
- In the default mode the agent opens data files and reads free-text survey fields into the model. Use private-data mode only, or an approved enterprise model, for confidential packages.
- Good human gates exist (emails drafted not sent, no push, deletion confirmation, private-data mode), but they are agent instructions, not technical enforcement.
- No license file; marked work in progress. Some repository hygiene issues need fixing before it is listed.

**[surveycto/surveycto-agent-skill](https://github.com/surveycto/surveycto-agent-skill/tree/c6b1594fac1412dafbc5908eae8c6f268708348d)**: OK with caveats.
- The full workflow uploads your XLSForm to SurveyCTO's hosted MCP server (`assistant-be.surveycto.net`), which needs no login and documents no retention terms. Check choice lists, labels, and preload references for sensitive details (village, school, or enumerator names) first.
- Use "needs approval" rather than "always allow" for tool calls. The server can tell the agent to prompt you to update from a URL it supplies; update from the GitHub repo instead.
- The optional `mcp-remote` route runs an unpinned `npx -y mcp-remote`. Bundled scripts are local-only.
- Public beta (`1.0.0-beta.9`), Apache-2.0. Deploying forms needs a SurveyCTO subscription.

**[hanlulong/econ-writing-skill](https://github.com/hanlulong/econ-writing-skill/tree/f2bf7a22c5e3b37921a5e6c73bd1fb380a5e00e8)**: OK with caveats.
- Prompt-only Markdown; no scripts or network calls.
- Install by copying the pinned `skills/econ-write/` folder. Avoid `INSTALL.md`, which pipes `install.sh` from `main` into `bash`.
- For policy briefs and blogs it tells the agent to "supply a defensible illustrative value" when a number is unknown. Do not let it insert made-up figures into Bank outputs.
- Very broad trigger; some journal page-limit claims may be stale. MIT.

**[hanlulong/awesome-ai-for-economists](https://github.com/hanlulong/awesome-ai-for-economists/tree/e1406b3bd20a73b2d9f9624cacd85e27175dfc03)**: OK with caveats.
- Strongest vetting of the three indexes: inclusion criteria, maintainers state they read each SKILL.md, and AI-detection-evasion skills are rejected. CC0, weekly link check.
- Maintainers' own OpenEcon projects are featured (disclosed); one is non-commercial only. Linked tools are unpinned third-party code.

**[meleantonio/awesome-econ-ai-stuff](https://github.com/meleantonio/awesome-econ-ai-stuff/tree/dd890d51c789fb8f8e316a2d7e4ed5d4bd793c50)**: OK with caveats.
- Ships 16 short, generic skill templates; no malicious content found. `api-data-fetcher` reads `FRED_API_KEY` from the environment and calls FRED/World Bank APIs.
- `commit-push-pr` commits, pushes, and opens PRs when you invoke it (user-invoked only).
- Light, single-maintainer review. The `LICENSE` file is a truncated CC0 notice. The website's download button fetches the unpinned `main` branch.

**[O0000-code/awesome-academic-skills](https://github.com/O0000-code/awesome-academic-skills/tree/5975c4ee37f01a8e20362d83a2ab3e92198c59ab)**: OK with caveats, as a discovery index only.
- Labels each entry's license and capabilities (network, hooks, permission bypass), but these are author declarations, not audits.
- Lists AI-detection-evasion ("humanizer") skills, entries that require permission bypass, and unlicensed or non-commercial entries. Do not use those for Bank work.
- CC0. Broad academic scope; about 20 entries are economics- or Stata-specific.

