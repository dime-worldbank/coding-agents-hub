# Language-Specific Review Flags

Apply these rules alongside `review-flags.md`. This file contains
language-specific detection cues: syntax, idioms, or file formats whose risk
only makes sense in the context of a specific language or package, including
where that risk is a correctness or privacy concern rather than a style one.
Shared cross-language risks such as joins, paths, randomness, dependencies,
hidden state, and output stability are defined in `review-flags.md`; route
language-specific syntax to those shared IDs when it applies, as the
`data.table` cross-reference list below does, rather than creating a
duplicate finding.

## Stata

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| STATA-STYLE-001 | Hard tabs or inconsistent indentation inside braces or after `///` | Low | Replace tabs with consistent spaces and indent nested blocks and continued lines. | Yes |
| STATA-STYLE-002 | Abstract loop locals such as `i` or `x` when a descriptive name is available | Low | Rename the loop local and all references to describe the iterated object. | Yes |
| STATA-STYLE-003 | Long lines that obscure logical components | Low | Break at a meaningful boundary with `///` and indent the continuation. | Yes |
| STATA-STYLE-004 | Missing whitespace around operators or before opening braces | Low | Add consistent spacing without changing expressions. | Yes |
| STATA-COND-001 | Implicit truth checks such as `if var` | Medium | Confirm which values should satisfy the condition, then state the comparison explicitly. | Conditional |
| STATA-COND-002 | Numeric comparisons that unintentionally include Stata missing values | High when the sample or result changes; otherwise Medium | Add an explicit missing-value condition suited to the intended logic. | Conditional |
| STATA-COND-003 | Tilde used for logical negation | Low | Use `!` consistently. | Yes |
| STATA-LABEL-001 | Variables or coded categorical values lack the Stata variable or value labels needed to interpret them, or related label definitions are contradictory | Medium; High when an incorrect label can change interpretation | Obtain the authoritative label definitions from the codebook or project documentation, then add or correct the labels and verify them. Do not invent labels. | Conditional |
| STATA-MACRO-001 | Global reference without `${...}` | Low; raise only when expansion can be ambiguous or incorrect | Use braced global references to avoid ambiguous expansion. | Yes |
| STATA-PATH-001 | Backslashes in likely file paths | Medium | Quote paths and use forward slashes. | Yes |
| STATA-SYNTAX-001 | `#delimit` in analytical code | Low | Prefer readable line continuation with `///`. | Yes |

Do not flag an isolated pattern when surrounding code already makes the
behavior safe. Style findings remain Low unless they create a concrete higher
risk. See the general deduplication rule in `review-flags.md`;
`STATA-LABEL-001` is the more specific ID when both it and `CLEAN-003` match.

## R

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| R-STYLE-001 | Inconsistent naming, spacing, assignment, or file organization materially impedes review | Low | Apply focused Tidyverse-style improvements without broad unrelated formatting changes. | Yes |
| R-DT-REF-001 | `:=`, `set()`, `setnames()`, `setorder()`, `setkey()`, or another `set*()` function modifies an object by reference when later code appears to expect the original object to remain unchanged | Medium; High when the mutation changes the analysis sample or results | Use `copy()` before the modification when an independent object is intended, or make the intentional mutation clear. | Conditional |

When reviewing `data.table` code, use these syntax-specific cues to apply the
shared rules rather than creating duplicate findings:

- Review `x[i, on = ...]`, `merge()`, `allow.cartesian`, `mult`, and `nomatch`
  under `DATA-003` or `DATA-004` when join cardinality or behavior is unclear.
- Review `setkey()` and `setorder()` under `STAB-002` or `STAB-015` when their
  by-reference row reordering can affect later operations or outputs.
- Review `rbindlist(..., fill = TRUE)` under `DATA-006` when filling absent
  columns could conceal incompatible input schemas.
- Review `fread()` under `DATA-007` or `DATA-008` when inferred column types can
  alter identifiers, dates, categories, numeric precision, or required schema.

Do not flag these functions merely because they are used. Report a finding only
when the surrounding code provides evidence of the corresponding risk.

## Python

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| PY-STYLE-001 | PEP 8 naming, spacing, import, or layout problems materially impede readability or obscure logic | Low | Apply focused formatting and naming improvements without broad unrelated changes. | Yes |

## Notebooks

Applies to any notebook format, including Jupyter (`.ipynb`) and rendered R
Markdown/Quarto (`.Rmd`/`.qmd`), regardless of the language in the code cells.

| ID | What to detect | Severity guidance | Recommended response | AI implementation |
|---|---|---:|---|---|
| NB-001 | A notebook's saved cell outputs, execution counts, or rendered previews could contain data values, or out-of-order execution counts suggest the visible code no longer matches the saved outputs | Medium; treat as a privacy question (see the privacy gate) when outputs may contain data values rather than code | Before further inspection, treat embedded outputs the same as a data file under the privacy gate. Recommend clearing outputs before sharing, or restructuring reusable logic into scripts/modules, and re-running top-to-bottom before relying on results. | No |

Notebook output cells can contain data even when the source code does not;
apply the privacy gate to them as you would a data file.

## Other languages

Apply the shared flags in `review-flags.md`. Inspect project-native dependency,
format, and test configuration when present, but do not run it in Phase 1. Do
not invent ecosystem-specific requirements. Flag only patterns whose
effect can be explained from the code and the shared research-code principles.

## Sources

- DECDI coding guide and Stata style guide (DIME Analytics Data Handbook):
  https://worldbank.github.io/dime-data-handbook/coding.html
- DECDI Stata peer code review checklist (DIME Standards):
  https://github.com/worldbank/dime-standards/blob/master/dime-coding-standards/checklists/Stata%20Code%20Review%20Checklist.md
- Tidyverse Style Guide: https://style.tidyverse.org/
- `data.table` reference semantics and documentation:
  https://rdatatable.gitlab.io/data.table/articles/datatable-reference-semantics.html
- PEP 8: https://peps.python.org/pep-0008/
