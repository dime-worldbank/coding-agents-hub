# Comparing the paper and programmed versions

Aim: confirm the two versions flow the same way, ask the same questions in the same words, offer the same choices, route respondents the same way, and apply the same constraints. Always do the full comparison. Never offer a spot check. A matching count is not a match.

Work from Markdown (see `reading-files.md`): the paper converted to Markdown, and the form reduced to `type,name,label,relevant,constraint,required` and the choices sheet. Compare one language: the one both files share.

## Steps

1. **Convert and reduce** both files. Read the paper's first part. Decide what kind of paper it is:
   - **Specification style:** prints variable names, field types, `Required`, and form expressions (`Ask if:`, `Constraint:`). Match by variable name first, then wording.
   - **Respondent style:** wording and skip notes only. Match by wording and order.
2. **Language.** List the form's label languages. Read which language the paper is in. One shared language: use it and say so. Several: ask the team (tappable). None: stop and say so.
3. **Work module by module.** For each paper section, find the matching form group (by name, label, or first questions). Read only that section and those form rows. Build the working ledger in `ledger.md` before you read the next module.
4. **The ledger has a row for every paper question and every form question in the module:** matched, differs, on paper only, or in form only. At the end of each module write the counts: paper questions = matched + differs + paper only. Form questions = matched + form only. If the counts do not reconcile, find the missing row before you go on.
5. **For each matched pair check, in this order:**
   - **Flow:** is the question in the same position relative to its neighbours? Note moved, inserted, and deleted questions. Question numbers are a weak signal. Flow is judged by wording and order.
   - **Wording:** the paper text against the label in the chosen language. Meaning changes (numbers, recall period, negation, who is asked) are the most important.
   - **Choices:** the options on paper against the `choices` sheet rows for the list named in `type`: labels, values, order, and options on one side only ("Other"). Lists loaded from files: note the file and ask the team to share it.
   - **Skip logic:** the effective condition (group `relevant` and the question's own) against the paper's condition or skip note. Decide whether two forms of the same rule route the same people (for example `${a}!=1` and `${a}=0`).
   - **Constraints:** the constraint expression against the paper's rule or range, and the message in the chosen language.
   - **Required, type, variable name** when the paper prints them.
   - **Calculations** only when asked and the `calculation` column was kept.
6. **Consent and introduction text:** compare line by line, separately.
7. **Reconcile:** total counts across modules. Resolve every High row by looking at both texts again.
8. **Write `discrepancies.md`:** one table per section with the columns Paper no., Form name, Check, Confidence, Paper, Form, Suggested response. Quote short exact text. Then convert to `discrepancies.xlsx` (see `reading-files.md`).

## Checks and confidence

| Check | Confidence |
|---|---|
| On paper, not in form; in form, not on paper | High |
| Wording changes meaning | High |
| Choices differ (an option on one side only) | High |
| Skip logic differs | High |
| Constraint differs | High |
| Choice codes differ; order differs; required differs; type differs; variable name differs; preload file differs; calculation differs | Medium |
| Wording differs, meaning the same; piped value differs | Medium |
| Consent or introduction text differs | Medium |
| Minor wording; choice order; constraint message; question number | Low |

## Not compared (say so in the report)

Calculate fields (unless asked), metadata fields, notes other than consent or introduction text, the contents of preload files, and every other language.

## When reading is weak

- A section that is shorter in the Markdown than in the file: read that part again with a fallback converter and say you did.
- Anything the paper prints only as an image: ask for a text version.
- A scanned PDF: read the pages as images, or ask for the Word or Excel original.
- Say "no discrepancies found in the questions read" and give the counts. Never say the versions match unless every High row is resolved and each check was done.

## Do not

- Do not edit either file.
- Do not decide which version is right. List the difference and ask.
- Do not treat a different question number as an error if the team renumbers on purpose. Ask.
