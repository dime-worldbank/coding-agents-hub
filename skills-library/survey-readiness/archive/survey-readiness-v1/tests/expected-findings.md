# Expected findings for the test documents

Use these to judge a run of the skill. They are planted on purpose. Wording will differ.

## planted-errors-form.xlsx (programming)
Script should flag: unknown list `regions` (LIST-001); undefined `${n_sheep}` (LOGIC-001); required note with no relevance (VALID-005); duplicate choice name `2` (LIST-002); `resp_edu` referenced before it is defined (LOGIC-002); `select_multiple` compared with `=` (LOGIC-005); duplicate name `age` (NAME-001); no `public_key` (META-004); phone marked publishable (META-006); missing French labels (LANG-001); no `start` or `deviceid` (META-001, META-002); outdated `position()` (SYNTAX-001); no `label:stata` (STATA-001); non-integer choice codes (LIST-005); no exclusivity constraint (VALID-004).
Judgment (script cannot see): consent comes last and does not gate any group (ELEC-001); `first_name` is asked of respondents with no stated universe (LOGIC-007); `goat_ratio` divides by a value that can be 0 or blank (LOGIC-011).
Report should: show no IDs; put encryption under ethics and data security only; give shortest and longest path counts and ask for pilot timings; end with the Impact Analytics closing note; give verdict Not ready.

## test-tor.md (hiring, Bank-executed)
Should flag: selection weights sum to 90, not 100 (PROC-011); D2 pilot report is due before D1 translation and before the pilot could run (PROC-005); no deliverable or payment milestone for field activities 3.4 to 3.5 beyond the final dataset, and payments sum to 100% but nothing is tied to approved deliverables or integrity thresholds (PROC-004, PROC-010); back-check 5% conflicts with 10% in the first two weeks (PROC-014); no confidentiality, ownership, or data security text (PROC-015); no ethical provisions or annex (PROC-016); no privacy office approval or Bank provisions (PROC-018, PROC-019); training lacks field practice, evaluation, and reserve trainees (PROC-007); no field procedure plan content (PROC-006); no device specification (PROC-012); single source above USD 50,000 has no written justification (PROC-017, worded as "The guidance used here says...").
Must not raise: country, sample size, or interview length as findings.

## test-dqa-plan.md (data quality)
Should flag: no back-check coverage in the first weeks, no missing-respondent or flagged-case back-checks (DQA-004); missing core checks: enumerator completion and average responses beyond counts, progress by administrative unit, unit-level tracking, interview duration, missing values and non-response, consent and refusal rates, sample progress against plan (HFC checklist); no named tool such as iehfc (DQA-013); no thresholds, actions, or check code tested on pilot data (DQA-006, DQA-007); feedback given during interviews instead of after (DQA-008); risks incomplete, no fatigue or fabrication (DQA-001); no paradata named (DQA-009).
Each missing check is one line with why, tool, and paradata needed.
