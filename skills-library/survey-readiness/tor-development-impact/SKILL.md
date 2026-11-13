---
name: tor-development-impact
description: "Create or review a survey firm terms of reference (TOR) for Development Impact surveys. Use whenever the user wants to draft, update, or check a TOR for hiring a survey or data collection firm: deliverables, payment schedule, selection criteria, qualifications, ethics and data security clauses, or whether the World Bank or a government hires the firm. Starts from the standard Development Impact template, asks what to change in chat, and checks numbering, dates, payment shares, and weights."
---

# TOR for Development Impact surveys

Scope: Development Impact. A drafting and review aid. It does not check procurement compliance and is not legal advice. Write short sentences. Never assume or invent a detail. Ask.

## Two tasks

| Task | Method |
|---|---|
| Create a TOR | `assets/tor-template.md`, edited through chat (`references/create-flow.md`) |
| Review a TOR | `scripts/check_tor.py` plus judgment checks (`references/review-checklist.md`) |

Read `project-brief.md` first if it exists (survey name, country, instruments, dates, who hires). Load only the reference the task needs.

## Step 1: Ask

Tappable questions if available (ask_user_input), always with free text. One turn, skipping what is known:
1. Create a new TOR, or review an existing one (and which file).
2. Who hires the firm: the World Bank, or a government, ministry, or statistics office.
3. For a review: contract value if single-source is planned, and whether the sampling, pilot, and quality plans can be shared.

## Step 2: Confirm the documents

Ask: "Please confirm you may share these documents here, and that they contain no personal identifiers." Accept only a clear yes. A TOR may hold confidential contract details. Say that you will not repeat them outside the report.

## Step 3: Work

- **Create:** follow `references/create-flow.md`. Keep standard text. Ask what to update, then update. Offer to edit any activity through chat. Show only the changed section. Finish with `check_tor.py`, then the Word file (`node scripts/md_to_docx.js`, or `pandoc` if it fails).
- **Review:** convert a Word or PDF TOR to Markdown first (`markitdown tor.docx -o tor.md`; if that fails, `extract-text` or `pandoc -t gfm`) and say which you used. Run `python scripts/check_tor.py tor.md`, which reads Markdown only. Then apply `references/review-checklist.md` to the Markdown. Never raise project-specific details as findings.

## Step 4: Report (reviews)

Verdict first: Not ready (any Mandatory), Ready with fixes (no Mandatory, any Priority), Ready. Then three lists: **Mandatory**, **Priority**, **Suggested**, each item as issue, place (section), fix, and whether Claude can apply the fix: **Yes** (clear from the TOR), **Conditional** (the team must decide or supply something), **No** (a procurement or methodology decision). No internal IDs. Add "Not checked" and "Open questions for the team". For Conditional items add a short copy-and-edit form: reply `approve`, `change: [alternative]`, `provide: [information]`, `defer`, or `discuss`, one block per item. If an item rests on a rule the review owner supplied and nobody has verified, say so.

## Step 5: Fixes (only if asked)

Edit a copy, never the original. Log each change (section, before, after). Rerun `check_tor.py` and report what changed and what remains open.

## Keep it light

Never read the whole template into chat. Edit it in the file. Use the script for numbers and dates. Do not restate guidance.
