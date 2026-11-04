# Sampling review

**Basis:** DIME Wiki *Sampling*.
**Documents:** sampling protocol, power calculations, frame description, sampling code if available.
**Rule:** check completeness, consistency, and reproducibility. Do not recompute power or approve the design; DECDI guidance is to consult Impact Analytics before a sample goes to the field.

| ID | What to check | Severity | Fix |
|---|---|---|---|
| SAMP-001 | Population of interest defined, with region and characteristics, and inclusion and exclusion rules | Blocker | Define precisely |
| SAMP-002 | Sampling frame and a master dataset exist for the unit being sampled. If not, a listing at the lowest feasible cluster level is planned | Blocker | Create the master dataset or plan a listing |
| SAMP-003 | Approach stated (simple random, multi-stage or cluster, stratified), with the unit of randomization distinguished from the unit of observation | Blocker | State and justify the design |
| SAMP-004 | Stratification variables and why they were chosen, including subgroup reporting needs | Important | Document |
| SAMP-005 | Spot or random-walk selection is avoided, or its bias and monitoring risks are acknowledged | Important | Use a master dataset or document safeguards |
| SAMP-006 | Power calculation states effect size, power, significance level, outcome, baseline mean and variance, and intra-cluster correlation for clustered designs, with sources | Important | Add assumptions |
| SAMP-007 | Sample size allows for non-response and attrition, with the rate sourced | Important | Add rate |
| SAMP-008 | Replacement, refusal, and absent-respondent rules; respondent selection within the unit | Important | Specify |
| SAMP-009 | Sampling and randomization are done in code with the seed set, plus sort order and software version, and the code is stored | Blocker | Set the seed and store the code |
| SAMP-013 | Every sampling unit has a unique ID in the master dataset, used as the ID in the survey form | Blocker | Create unique IDs |
| SAMP-010 | A second person has checked the sampling code before the sample is used | Blocker | Arrange a check |
| SAMP-011 | Sample sizes match the TOR, budget, timeline, and field plan | Important | Reconcile documents |
| SAMP-012 | Hard-to-reach subgroups are covered or the gap is acknowledged | Minor | Oversample or note limitation |

**Ask if missing:** primary outcome; whether this is a baseline, midline, or endline; whether the sample is from an existing master dataset.
