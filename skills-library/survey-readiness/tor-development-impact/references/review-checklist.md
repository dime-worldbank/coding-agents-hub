# Reviewing a TOR

Check completeness and internal consistency. Project-specific details (country, sample, dates, names, amounts) are not findings. This review does not check procurement compliance and is not legal advice.

Report tiers: Blocker = Mandatory, Important = Priority, Minor = Suggested.

## First

Convert a Word or PDF TOR to Markdown first (`markitdown`, with `extract-text` or `pandoc -t gfm` as fallbacks). Run `python scripts/check_tor.py tor.md` (add `--recipient-executed` for a government hire). It covers: placeholders, required sections, activity numbering across duties, deliverables and payment, payment shares and selection weights adding to 100, dates against the contract period, percentages to reconcile, and required clauses. Confirm each result in context. Then apply the judgment checks below.

Ask if missing: who procures the firm, the contract value, who programs the questionnaire, whether the pilot happens before or after hiring.

## Judgment checks

| What to check | Tier |
|---|---|
| Each section of a complete TOR is present (see `sources.md` for the reference structure) | Priority |
| Scope states what the research team provides (sample list with contact and location details, questionnaires, programmed instrument, secure server, tracking lists for panels, quality checks it runs) and what the firm provides (tablets, chargers, data plans, set-up) | Priority |
| Every activity, including any later phase, has deliverables, dates, and a payment milestone | Priority |
| Field procedure plan contents are specified: adherence to the sample, revisits and substitution, tracking and attrition for panels, logistics, progress tracking, backup and submission, supervision and spot checks | Priority |
| Training: theory, classroom practice, field practice outside the sample, evaluation against practice scenarios, more trainees than needed, a reserve, selection based on evaluation | Priority |
| Quality provisions: spot-check and back-check coverage, daily upload, regular reporting, corrections, the team's own checks. Consistent with the team's data quality plan, if one exists | Priority |
| Data deliverables and documentation: raw data regularly during fieldwork, questionnaires in all languages with pilot changes, interviewer manual, procedures, ID and linkage guidance, codes for items not pre-coded, problems and fixes, file and variable descriptions | Priority |
| Payment tied to approved deliverables, and remedies for integrity failures with stated thresholds | Priority |
| Devices meet SurveyCTO's current requirements, with chargers, data plans, set-up, and a replacement plan. Check SurveyCTO's current support pages by web search when available: older figures may be out of date | Priority |
| TOR matches the sampling protocol, timeline, pilot plan, and data quality plan. Ask for them if not provided | Priority |
| Quality coverage figures do not conflict inside the TOR | Suggested |
| Confidentiality, ownership, re-use, data security standards, and encryption expectations are stated | Mandatory |
| Ethical provisions: consent required, review board compliance, and the ethical principles annex | Mandatory |
| Selection criteria match the qualifications section | Priority |

## Single-source selection

Single source for contracts below USD 50,000 is allowed. Above USD 50,000 it is possible only with a written justification giving task- and firm-specific reasons and the alternatives considered. Priority. This threshold was provided by the review owner and has not been checked against a document. Word it as guidance and ask the team to confirm it with procurement.

## Hired by the World Bank

- World Bank privacy office approval is in place for the data collection. Point the team to the privacy office and ask for the status. Mandatory. Provided by the review owner. Confirm the process.
- Bank provisions are in the TOR: data and intellectual property owned by the Bank, confidentiality, data security standards, no third-party use without written approval, ethical provisions annex, right to repeat work or withhold payment on integrity failures, and the Bank's own verification checks. Priority.
- Changes to scope, mode, timeline, or budget after signing follow a contract modification, which for Bank funding needs Corporate Procurement approval. Suggested: note it in the plan.

## Hired by a government or statistics office

- The TOR gives the research team written access to the data, the instrument, quality-check outputs, and field reports. Priority.
- Equivalent confidentiality, data ownership, ethics, and security provisions are in the recipient's contract. Priority.
- The recipient's procurement rules and approvals are identified and the timeline allows for them. Priority. Confirm with the recipient.
