---
name: survey-skill-connector
description: "Route survey preparation requests to the right skill and carry shared project details between them. Use whenever the user is preparing a primary survey and asks what to do next, where to start, which skill to use, or wants to set up or update the project brief. Covers the form review, prep timeline, TOR, enumerator manual, and training plan skills, and gives pointers for ethics, sampling, and pilot, which no skill covers yet. Never assumes project details."
---

# Survey skill connector

Scope: universal. It routes. It does not do the other skills' work. Never assume a project detail. Ask. Write short sentences.

## Steps

1. **Read the brief.** If `project-brief.md` exists, read it (`python scripts/brief.py show`). If not, offer to create one (`init`). See `references/project-brief.md`.
2. **Ask what the team needs now** (tappable, free text allowed): the request, and only the brief fields the chosen skill needs that are still blank. Ask once. Do not fill the whole brief up front.
3. **Route** with `references/routing.md`. Name the skill and say what it will produce in one line. If it is not in the available skills, say so, point to its README, and stop.
4. **Hand over** the relevant brief fields so the next skill does not ask again. Do not paste the whole brief into chat.
5. **After a skill finishes**, add what it learned to the brief (dates, sample, languages) and set `updated:`. Run `python scripts/brief.py check` and tell the team which fields are still empty.
6. **Offer the next step** from the suggested order of preparation. One suggestion, not a list.

## Gaps with no skill

For ethics, sampling, pilot plan, questionnaire design, and the data quality plan, give the pointer in `references/routing.md`. Say it is a pointer, not a review. Offer to add the step to the timeline with an owner. Never judge those documents from memory.

## Privacy

The brief holds no personal data, phone numbers, or emails. If a team member pastes one, do not store it. Say so.

## Keep it light

Load each reference once. Show only the changed brief fields. Do not restate other skills' instructions.
