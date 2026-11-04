# Questionnaire design review

**Basis:** DIME Wiki *Questionnaire Design* and *Literature Review for Questionnaire*; Impact Analytics survey review resources.
**Documents:** questionnaire (Word, PDF, or workbook), list of outcomes and indicators, theory of change or pre-analysis plan if available.
**Overlap with programming:** skip logic, constraints, labels, translation, hints, and special codes are checked in the programming module (`programming-flags.md`). Report each issue once under the most specific ID. The Style Guide applies to programming only.
**Rule:** wording and flow findings are judgments; prefix with `Possible:` unless unambiguous. Do not change validated items without flagging the loss of comparability. Teams should start from the DECDI Questionnaire Dashboard and existing field-tested instruments instead of drafting from scratch.

| ID | What to check | Severity | Fix |
|---|---|---|---|
| DES-001 | Modules trace to the theory of change or pre-analysis plan; every key outcome and indicator is measured and every question has a purpose | Important | Add or drop questions |
| DES-002 | Questions come from existing, tested instruments where possible, with a source noted for each. Catalogs to search: World Bank Microdata (impact evaluation), J-PAL and IFPRI Dataverse, DHS, IHSN. Authors often share instruments that are not public | Important | Substitute or cite |
| DES-003 | Relevance and looping per module are defined: who is asked, and whether questions repeat per household member, plot, or crop | Important | Specify |
| DES-004 | Nuanced concepts are defined in the questionnaire (for example who counts as a household member) and age is handled for respondents without documents | Important | Add definitions |
| DES-005 | Recall bias addressed: objective sources where feasible, consistency checks, multiple measures of the same indicator | Important | Redesign or add checks |
| DES-006 | Sensitive questions: anonymity stated, comfort built first, reframing, self-administration, or indirect methods considered | Important | Revise |
| DES-007 | Abstract concepts (empowerment, cohesion) are defined from prior studies or local experts before measures are chosen | Important | Define concept |
| DES-008 | Double-barreled, leading, or loaded wording | Important | Split or neutralize |
| DES-009 | Ambiguous terms, undefined reference periods, missing units | Important | Define |
| DES-010 | Answer choices are complete and mutually exclusive, and coded consistently across the instrument (code scheme: see CODE-001 in the programming checks) | Important | Revise choices |
| DES-011 | Consent comes first, and the interview ends if the respondent refuses (report once; see ETH-013 and ELEC-001) | Blocker | Add consent gate |
| DES-012 | Unique ID for each respondent and each completed interview | Important | Add |
| DES-013 | Introductory script for each module to guide the interview flow | Minor | Add scripts |
| DES-014 | Final version stored as a workbook with one tab per module and a main tab linked to them, for programming. The final version is not the programmed form | Minor | Restructure |
| DES-015 | Duplicated or inconsistent questions across modules (same concept, different period, unit, or codes) | Important | Consolidate |
| DES-016 | Interview time is estimated for the shortest and longest path (from the pilot or a desk estimate) and compared with the planned length. Ask the team for pilot timings; field counts for both paths come from the programming script. Also check module order and respondent burden | Important | Cut, split, or reorder |
| DES-017 | Length and expected time calibrated against similar surveys found in the literature review | Minor | Compare with similar instruments |

**Ask if missing:** target interview length; outcomes list; whether the instrument is new, adapted, or a follow-up.
