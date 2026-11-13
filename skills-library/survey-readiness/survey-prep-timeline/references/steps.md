# Survey preparation steps

Use this list to make sure every step is covered. Durations are suggested ranges from earlier Impact Analytics guidance (2017) and the Development Impact Wiki. They are starting points. Ask the team for its own durations and never schedule from a suggestion the team has not confirmed.

## Step catalogue

| ID | Step | Owner (suggest) | Applies when | After | Suggested weeks |
|---|---|---|---|---|---|
| P01 | Objectives, indicators, and sampling plan agreed | Research team | Always | none | ask |
| P02 | Sampling frame or listing, sample drawn, code checked by a second person | Research team | The team draws the sample | P01 | ask |
| P03 | Questionnaire design | Research team | New or adapted instrument | P01 | about 4 |
| P04 | Pre-pilot (context and design) | Research team | New instrument or new context | P03 | 1 to 2 |
| P05 | Content test on paper | Research team | New instrument | P04 | 2 to 3 |
| P06 | Ethics approval and consent forms. Must come before any contact with respondents, including the pilot | Research team | Human subjects | P01 | ask |
| P07 | Translation. The questionnaire is frozen first | Research team or firm | More than one language | P05 | 2 to 3 |
| P08 | Programming the form. Can run alongside ethics and translation | Research team | Electronic collection | P05 | 4 to 6 |
| P09 | Data test on the programmed form | Research team | Electronic collection | P08 | 2 to 3 |
| P10 | Revision and re-test after the pilot | Research team | Any pilot | P05, P09 | ask |
| P11 | TOR drafted (submit for review about 12 weeks before the survey starts) | Research team | A firm is hired | P01 | ask |
| P12 | Firm procurement and contract | Research team and procurement | A firm is hired | P11 | ask |
| P13 | Data quality plan, checks set up, back-check protocol (about 2 weeks before start) | Research team | Always | P09 | ask |
| P14 | Enumerator manual (about 4 weeks before start) | Research team | Enumerators are used | P10 | ask |
| P15 | Training plan and agenda | Research team and firm | Enumerators are used | P14 | ask |
| P16 | Devices bought and configured, with spares | Firm or team | Electronic collection | P12 | ask |
| P17 | Field plan by the firm (about 2 weeks before start) | Firm | A firm is hired | P12 | ask |
| P18 | Recruitment of enumerators and supervisors | Firm | Enumerators are used | P12 | ask |
| P19 | Training, field practice, and enumerator selection | Firm and research team | Enumerators are used | P15, P16, P18 | about 2, ask |
| P20 | Buffer for delays in approvals, procurement, access, or equipment. Larger in fragile, remote, or insecure settings | Research team | Always | all | ask |
| P21 | Start of data collection (the anchor) | Firm | Always | P10, P13, P17, P19, P20 | 0 |
| P22 | After fieldwork: raw data delivery, cleaning, quality checks, documentation | Firm and research team | Always | P21 | ask |

## Rules to check

- Ethics approval comes before any respondent contact, including the pilot.
- The questionnaire is frozen before translation. Leave time to revise and re-test after the pilot.
- Procurement comes before every step that depends on the firm.
- Plan fieldwork at least six months ahead. The pilot starts roughly four to six months before launch so findings can change the instrument and protocols (a suggestion).
- Field practice at the end of training is not the pilot. A survey that has not been in the field before should have a separate pilot.
- A follow-up with no major changes may start at the data test stage and skip early pilot steps. Ask.
- Fieldwork avoids harvest, rainy season, holidays, elections, and school terms where they matter. Ask for the team's known constraints.
- Every step has a named owner.

## By survey type (ask, never assume)

- **In-person household or school survey:** all steps. Training about two weeks including field practice, unless the team says otherwise.
- **Phone survey:** remote training works better in shorter sessions over more days. One Development Impact blog reports panelists aiming for about 4 hours a day. Ask what the team plans.
- **Panel follow-up:** panel tracking needs the previous round's list and time for tracing. Some early pilot steps may be skipped.
- **Records retrieval (administrative data):** the Zambia school feeding protocol used one day of centralised training followed by deployment the same week. Short training suits a narrow task and is not a rule for interview surveys.

## Plan file for the script

`python scripts/build_timeline.py plan.json` (add `--md schedule.md` to save the table). Each step: `id`, `name`, `owner`, `weeks`, `after` (list of ids), optional `done` and `done_date`, and `field: true` for steps that must avoid blackout dates. Add `anchor_step`, `anchor_date`, `from_date`, and `blackouts` (name, from, to). See `tests/sample-plan.json`.

## Sources

Development Impact Wiki, Preparing for Field Data Collection (page created 2018; the search extract says to plan at least six months ahead and to allow time for design, pilot, approval, procurement, protocols, and training). Earlier Impact Analytics review notes: stage ranges and minimum submission lead times from 2017, kept for now and due for a refresh. Development Impact Wiki, Enumerator Training and Survey Pilot. Zambia school feeding enumerator field protocol (July 2026).
