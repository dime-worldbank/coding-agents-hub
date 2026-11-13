# Project brief

One file, `project-brief.md`, in the project folder. Under about 20 lines. It carries details between skills so the team is never asked twice.

## Rules

- Blank means the team has not said. Never fill a blank by guessing or from a suggested default.
- Store no personal data, phone numbers, or email addresses. Names of files only.
- Any skill may read it. A skill that learns a detail may add it and sets `updated:` to the date and its own name.
- Do not overwrite a value the team gave. If a new answer differs, ask which is right.
- Before relying on a value that may have changed (dates, sample), confirm it with the team.

## Fields

`survey_name`, `country`, `survey_type` (household, school, phone, facility, firm, panel follow-up, records retrieval, other), `mode` (tablet, paper, phone), `instrument` (new, adapted, follow-up), `executed_by` (world bank, government, other, not applicable), `firm_hired` (yes, no), `units`, `respondents`, `sample_size`, `languages`, `platform` (surveycto, odk, kobo, other), `data_collection_start` and `data_collection_end` (YYYY-MM-DD), `panel` (yes, no), `style_guide` (yes, no), `files` (names only), `updated`.

## Commands

`python scripts/brief.py init`, `check`, and `show`. `check` lists empty fields, invalid values, anything that looks like a phone number or email, and an end date before the start.

## Who uses which field

| Skill | Reads |
|---|---|
| xlsform-paper-sync | languages, platform, style_guide, files |
| survey-prep-timeline | survey_type, mode, instrument, firm_hired, data_collection_start, panel |
| tor-development-impact | survey_name, country, executed_by, units, respondents, sample_size, languages, dates, panel |
| enum-manual | survey_name, survey_type, languages, platform, files |
| enum-training-plan | survey_type, mode, languages, sample_size, data_collection_start |
