# Sources and status

Cite sources in findings by short name, for example "Development Impact Wiki: Survey Pilot". Wiki pages are on dimewiki.worldbank.org.

| Source | Date shown | Status |
|---|---|---|
| Impact Analytics survey review resources (guidelines, process, forms, templates, TOR structure, SurveyCTO Style Guide) | Some from 2017 and 2020; others undated | Partly outdated. The 2017 lead times are kept for now. The Style Guide is undated and refers to an XLSForm template and a naming document not yet provided |
| Development Impact Wiki: SurveyCTO Coding Practices | Jul 2023 | **Aging.** Redirect-style page; check against current SurveyCTO features |
| Development Impact Wiki: Research Ethics | Aug 2023 | **Aging.** Points to COVID-era consent template versions |
| Development Impact Wiki: Data Security | Aug 2023 | **Aging.** Names specific tools (VeraCrypt, LastPass); confirm current approved tools |
| Development Impact Wiki: CAPI | Aug 2023 | **Outdated** in the hardware section (old Android versions, 1 GB storage). Replaced by SurveyCTO's own requirements |
| Development Impact Wiki: Questionnaire Design | May 2025 | Most recent wiki source |
| Development Impact Wiki: Survey Pilot, Sampling, Data Quality Assurance Plan, High Frequency Checks, Ietestform, Literature Review for Questionnaire | None shown | Unknown. Older page format; confirm current |
| Development Impact Wiki: Preparing for Field Data Collection | Page created Feb 2018 | **Not read.** Blocked for automated access. It is a hub page linking to hiring a survey firm, field management, back checks, and enumerator training |
| iehfc introduction (World Bank blog) | May 2025 | Current. Source for the five iehfc check types |
| SurveyCTO documentation: devices, encryption, release notes | Mixed | Source for device and encryption points. Some device pages look dated; check SurveyCTO's current pages |
| DECDI SurveyCTO encryption guidelines (GitHub) | None shown | Used for encryption steps and publishable fields |
| DECDI guide to remote data collection | None shown | Used only for the note on contract changes |
| Single-source threshold (USD 50,000) and privacy office approval | Provided by the review owner | Not verified against a document; worded as guidance in reports |

## Conflicts between sources

- **Special codes (resolved):** the Impact Analytics resources use -99 Don't know, -88 Refused, -9 Other. The Development Impact Wiki Questionnaire Design page suggests different codes. The skill follows the Impact Analytics resources.
- **Stata label length:** the Development Impact Wiki Coding Practices page says `label:stata` labels should be 32 characters or fewer. The `ietestform` page flags only labels over 80 characters (and names over 32). The skill uses 80 for labels and 32 for names.

## Open items

- The 2017 lead times are kept for now.
- Confirm severities, especially what counts as mandatory.
- Provide the XLSForm template and the variable naming document (module abbreviations).
- Provide the DQA plan and pilot plan templates or checklists, if they exist.
- Confirm the current `ietestform` test list and the core versus recommended high-frequency checks.
