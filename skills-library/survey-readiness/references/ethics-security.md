# Research ethics and data security review

**Basis:** DIME Wiki *Research Ethics* and *Data Security*; the DECDI informed consent templates; Impact Analytics survey review resources; SurveyCTO encryption guidance (see `links.md`).
**Documents:** ethics approval status, consent form(s), data security plan. If available, also the SurveyCTO instrument.
**Rule:** this review does not confirm compliance and is not legal or ethics advice. Flag minors, sensitive topics, recording, conflict settings, and cross-border transfer for extra care; the closing note points the team to Impact Analytics.
**Organise the report in two groups:** (A) needed for approvals (IRB, privacy office) and (B) to be done in the field.

## A. Needed for approvals

| ID | What to check | Severity | Fix |
|---|---|---|---|
| ETH-001 | Ethics approval from every board the study requires, covering activities and dates, including the pilot; local institutional or government approvals where required | Blocker | Obtain or extend approval |
| ETH-002 | Consent includes at minimum the authority for the study, intended uses of the information, and that participation is voluntary | Blocker | Add missing elements |
| ETH-003 | Consent for audio audits or any recording, if included: stated in consent, with storage, access, and retention rules | Blocker when applicable | Add recording consent |
| ETH-004 | If data collection is procured by the Bank: approval from the World Bank privacy office obtained. Point the team to the privacy office and ask for the approval status | Blocker when applicable | Obtain approval before collection |
| ETH-005 | Special protections for children, vulnerable groups, or sensitive topics (parental consent, referral protocol, interviewer safety) | Blocker when applicable | Add protocol |
| ETH-006 | Consent covers purpose, procedures and length, follow-up contact, benefits, risks, confidentiality and storage, retention period, compensation, right to decline or stop, and contacts for the survey firm and the review board. Use the DECDI templates (written, oral, SMS) | Important | Complete using the template |
| ETH-007 | Consent matches the instrument: modules, duration, sensitive topics, GPS, audio, photos, and follow-up contact in the form are all disclosed; nothing in consent is missing from or contradicted by the form | Important | Edit consent or form |
| ETH-008 | Consent procedure fits the risk: higher-risk studies use two or more extra measures (recorded verbal consent, third-party notification, written and oral in translation, reminders, a take-home copy, signed form) | Important | Add measures |
| ETH-009 | Oral versus written consent matches what the approval allows; translated into all survey languages; workable for non-literate respondents | Important | Align with approval; translate |
| ETH-010 | Data management plan: identifiers separated early, de-identified working dataset, encrypted raw data, named people with access | Important | Document the workflow |
| ETH-011 | Data ownership, sharing, retention, and destruction rules; the survey firm agreement covers confidentiality and return of data | Important | Add to plan and contract |
| ETH-012 | Compensation or incentives described and not coercive | Minor | Clarify |

## B. To do in the field

| ID | What to check | Severity | Fix |
|---|---|---|---|
| ETH-013 | Consent comes first in the instrument and the interview ends if the respondent refuses | Blocker | Add consent gate |
| ETH-014 | Encryption at rest enabled before collection. In SurveyCTO use its form encryption setup (public key in the form); it must be set when the form is created, and a lost private key cannot be recovered. Test before collecting | Blocker | Enable at form creation; store the key safely |
| ETH-015 | Encryption in transit confirmed. In SurveyCTO use its encryption setup; transit encryption is built in on SurveyCTO servers | Important | Confirm with the provider |
| ETH-016 | Personal data fields are not marked publishable | Important | Review the publishable column |
| ETH-017 | Everyone handling personal identifiers has current human subjects certification, is listed on the approval, and has signed a non-disclosure agreement | Important | Complete certification and agreements |
| ETH-018 | Local copies of identified data are encrypted or not stored; no personal data in unencrypted shared folders or email | Important | Specify encrypted storage |
| ETH-019 | Tablets are password protected; enumerator accounts cannot download data | Important | Set up devices and accounts |
| ETH-020 | Key and password management (password manager, two-factor authentication) for shared accounts and encryption keys | Minor | Add to plan |

**Ask if missing:** boards and countries; whether data collection is procured by the Bank; whether respondents include minors; whether audio, images, or GPS are collected; whether the form already exists on the server.
