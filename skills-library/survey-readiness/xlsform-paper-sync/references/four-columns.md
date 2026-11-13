# Reviewing a form: four columns

Read the reduced form (see `reading-files.md`). The focus is the `name`, `label`, `relevant`, and `constraint` columns, with `type` for structure, the `choices` sheet for lists, and `calculation` for calculate fields. Work in chunks. Apply every check to every chunk. Say at the end which checks you did.

Tiers: Mandatory, Priority, Suggested. Say whether Claude can apply each fix: Yes (clear from the form), Conditional (the team must decide or supply something), No (a design decision).

## name

- **Unique** within the form, ignoring case. Priority. Conditional.
- **Length:** 32 characters or fewer, for field names and for group names. Shorter inside repeat groups, because the export adds a suffix. Priority. Conditional.
- **Characters:** letters, digits, underscores. No spaces or special characters, and not starting with a digit. Priority. Conditional.
- **Groups:** every `begin` has a matching `end` of the same type, and the names match. Priority for a wrong type, Suggested for a missing end name. Yes.
- Every `${name}` used in `relevant`, `constraint`, or `label` exists. Mandatory if it does not. Conditional.

## label

- **Present** in the chosen language for every data question and every choice label. A missing label is Priority. Conditional.
- **Numbers:** question numbers in labels are unique, in order, and consistent. Duplicates are Priority. Yes.
- **Piped values:** `${x}` in a label refers to a real field. If it refers to a select question, the enumerator sees the code. Suggested, or Priority if the Style Guide is in use.
- **Text read to the respondent** is not mixed with enumerator instructions. Suggested.
- **Consent** comes first and says what the respondent is agreeing to. Check against the approved consent form. Conditional.
- **Recall periods** in the label agree with the constraint and with the paper (for example "last 7 days" and a constraint of 7 or less). Priority. Conditional.

## relevant

- Refers only to fields **defined earlier** in the form. Mandatory if not. Conditional.
- **Consent gating:** every module after consent is gated on consent, or the form ends on refusal. A form where consent is last or gates nothing is Mandatory. Conditional.
- **Select_multiple** uses `selected(${x}, 'value')`, not `=`. Priority. Yes.
- **Values** compared are in the choice list. A value that is not in the list makes the question unreachable. Mandatory. Conditional.
- **Universe:** each question is asked of the right group. Say what each skip assumes. A skip that hides a question from people who should answer is Priority. Conditional.
- **Effective condition** is the group condition and the question's own condition together. Check them together.
- **Repeated condition** on many questions in a group belongs on the group. Suggested. Yes.
- **Required note with no relevance** blocks the enumerator from moving on. Mandatory. Conditional.
- No question depends on itself, and no two conditions contradict each other.

## constraint

- **Numeric questions** (integer, decimal) have a plausible range. Ask the team for the range. Do not invent one. Priority. No.
- Uses `.` for the current answer. Suggested.
- **Consistent** with the label's recall period and with `relevant`. Priority. Conditional.
- **Select_multiple** with "None" or "Don't know" has a rule so they cannot be picked with other options. Priority. Conditional.
- **Constraint message** present and in the chosen language. Suggested. Conditional.
- **Dates** are not in the future where that makes no sense. Suggested.
- Does not block the special answer (Don't know, Refused) the team wants to allow. Priority. Conditional.

## calculation (calculate fields)

- Every `${name}` exists and is defined earlier. Mandatory if not. Conditional.
- No division by a value that can be 0 or blank. Priority. Conditional.
- No outdated functions (`position()` should be `index()`). Priority. Yes.

## type and choices (read with the four columns)

- Every list named in `type` exists on the `choices` sheet. Mandatory if not. Conditional.
- Choice values are numbers, with no duplicates inside a list. Priority. Conditional.
- Lists loaded from files (`select_one_from_file`, `search(...)`, `pulldata(...)`): list each file and ask the team to share it. Say "not checked" until it is.
- Choice values that are not integers (for example `goat`, `Factory Worker`). Suggested. Conditional.
- Many input questions are not `required`. Priority. Conditional. Allow non-answers as choices and use `relevant`.

## Outside the four columns, always check

- `settings`: an encryption key (`public_key`) when personal data are collected. Missing is Mandatory, and it cannot be added to an existing form. A form version.
- `start`, `end`, and `deviceid` fields exist. Suggested.
- Personal data fields (name, phone, address, GPS) are not marked `publishable`. Priority. Yes.
- **Translations:** for a multilingual form, every data question and choice has a label in each language. Missing is Priority. Conditional.
- **Stata labels:** a `label:stata` column exists in `survey` and `choices`, English, 80 characters or fewer. Missing is Priority. Conditional.

More checks (translations, paradata, the ietestform list, Stata labels) are in `programming-flags.md`, `programming-flags-config.md`, and `ietestform-rules.md`. Load them only for a full review. The Style Guide is optional (`style-guide.md`).

## Do not

- Do not give field counts or estimate interview length. Ask for pilot timings.
- Do not list the same issue twice. Merge repeats with example names.
- Use `Possible:` only where the file does not settle it.
