# Building the agenda

Never assume. Ask first, then build.

## What to ask (tappable where possible, with free text)

1. **Days:** how many training days are available, which dates, rest days, holidays, venue availability, daily start and end times, and any other restriction. Remote or in person.
2. **People:** how many trainees, how many positions, languages, experience level, number of facilitators and supervisors.
3. **Survey:** mode (tablet, paper, phone), modules and repeat groups, scales or experiments, whether the enumerator manual and questionnaire exist (if the form is shared, convert it to Markdown and read only the modules and group names).
4. **Practice:** can field practice happen outside the sample, with which sites, travel time; can administrative officials be used; is the pilot done.
5. **Assessment:** who marks quizzes and when, whether the firm or the team selects, what happens to people who do not pass.
6. **Anything else** the team wants in or out.

If a team gives a number, use it. If it gives none, show the wiki's guidance and ask. Do not fill in a duration for the team.

## Build in this order

1. Fix the frame: days, hours per day, rest, fixed constraints.
2. Place the fixed blocks: opening and study overview; protocols; confidentiality and the scientific approach; the questionnaire structure before tablets; tablet use; module-by-module sessions sized to complexity; classroom practice; field practice with facilitators and daily feedback; quizzes (one a day from day 2, on the previous day's topics); the final test; a feedback session; the selection step.
3. Add rest and meal breaks. Keep sessions after long travel short.
4. For each session: time, topic, objective, method, materials, lead.
5. Run `python scripts/check_agenda.py agenda.md --days N --hours-per-day H`. Fix every MISSING and review every CHECK.

## If the days are too few

Do not silently cut. Show what is cut and what each cut risks (for example fewer practice interviews, no separate selection day, one final test only). Offer options and a recommendation. A one-day training can work for a narrow task: the Zambia school feeding protocol used one day of centralised training with a practical exercise using sample reports with planted errors, and deployed only those who passed. That is an example, not a rule for interview surveys.

## Agenda table to produce

| Day | Time | Session | Objective | Method | Materials | Lead |
|---|---|---|---|---|---|---|

Follow the table with: the quiz plan (topics, day, marker, when marked), the final test outline (the four assessed skills), the field practice plan (groups, facilitators, sites, observation checklist, feedback time), the selection plan (criteria and weights the team chooses), the logistics list (venue, devices, printed materials, spares), and open decisions.

## Reminder: elements to use for testing

Give the team this list at the end: understanding of materials; reading in each language; understanding of questions and scales; numeracy and tablet entry; daily quiz on the previous day; same-day marking and feedback; a final test aimed at weak areas; field practice scored with the observation checklist; participation scored 1 to 5; train more than needed; keep a reserve.
