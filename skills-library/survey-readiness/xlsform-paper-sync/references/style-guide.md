# Impact Analytics SurveyCTO Style Guide (optional checks)

Load this file only when the team says it follows the Style Guide. Apply the checks below while reading the form Markdown (`four-columns.md`). Read the `settings` sheet for the version.
Source: the Impact Analytics SurveyCTO Style Guide, text provided by the project owner. The guide is undated. It refers to an XLSForm template and a variable naming document that have not been provided, so colour coding and module prefixes cannot be checked.

## What the guide asks for, and how it is checked

| ID | Guide recommendation | Checked by | Tier | AI can apply |
|---|---|---|---|---|
| STYLE-001 | Blank rows between modules, so modules are easy to see | Not visible in the Markdown. Ask the team or look at the file | Suggested | Yes |
| NAME-006 | Names use only a-z, 0-9 and underscores, lowercase, 32 characters or fewer | Reading the name column (the 32 limit is also a default check) | Suggested | Conditional |
| CODE-001 | Special codes the same in every list: -99 Don't know, -88 Refused, -9 Other | Reading the choices sheet | Suggested | Conditional |
| STYLE-002 | Form version set by formula as a date-time (yymmddhhmm) so each upload is greater than the last | Reading the settings sheet | Suggested | Yes |
| STYLE-003 | A label that refers to a select field shows its choice label, loaded by a calculate field, not the numeric code | Reading the label column | Priority | Conditional |
| STYLE-004 | Both begin and end group rows are named and labelled | Default check STRUCT-003 | Suggested | Yes |
| STYLE-005 | Rows colour-coded by field type; form built from the XLSForm template | Not checked. Needs the template and a visual review | Suggested | No |
| STYLE-006 | Names follow `module_varname_add`, with module abbreviations from the naming document | Not checked. Needs the naming document | Suggested | Conditional |
| LIST-005 | Numeric values only in the choices value column | Default check | Suggested | Conditional |

## Version formula (from the guide)

`=TEXT(YEAR(NOW())-2000,"00") & TEXT(MONTH(NOW()),"00") & TEXT(DAY(NOW()),"00") & TEXT(HOUR(NOW()),"00") & TEXT(MINUTE(NOW()),"00")`

## Why the guide gives these

- Numeric choice values make skip logic safe: a text value such as "Factory Worker" fails on a case difference.
- Negative standard codes let the person cleaning data know what -99, -88 and -9 mean in any variable.
- A calculate field that loads a choice label avoids questions such as "How much area is cultivated under 5?".
- Naming both ends of a group makes large forms easier to navigate and lets each team member own a module.

## Report

List these under Suggested, except STYLE-003 (Priority). Say that they come from the Style Guide and that the team chose to apply it.
