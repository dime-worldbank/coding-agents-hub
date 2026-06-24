# AGENTS.md — CDI-Jobs (PEJEDEC Public Works RCT)

Operational guide for AI coding agents working in this repository. Humans should
read `README.md` for the replication-package narrative; this file is the set of
rules and context an agent must follow when editing or running code here.
Official data and code repository: https://reproducibility.worldbank.org/catalog/298
Paper: https://www.aeaweb.org/articles?id=10.1257/app.20240586&&from=f


---

## 1. Project description

This repo is the **replication / reproducibility package** for the paper:

> **"Do Workfare Programs Live Up to Their Promises? Experimental Evidence from
> Côte d'Ivoire"** — Marianne Bertrand, Bruno Crépon, Alicia Marguerie, Patrick
> Premand.
> (Earlier working title still used in `README.md`: *"Improving Public Works
> Targeting for Short-Term and Medium-Term Impacts…"*.)

It analyzes a randomized controlled trial (RCT) of the **PEJEDEC public works
program** for urban youth in Côte d'Ivoire: ~7 months of employment at the formal
minimum wage, bundled with complementary training. The code estimates program
impacts (during and post program) and uses **machine learning to study impact
heterogeneity and alternative targeting rules**.

Official package: World Bank Reproducible Research Repository, ref
`PP_CIV_2025_368`, DOI `10.60572/101y-vn15`
(<https://reproducibility.worldbank.org/catalog/298>). Reproducibility was
verified by the World Bank DIME Analytics team.

The code is a mix of **Stata** (impact evaluation, tables, figures) and **R**
(machine-learning heterogeneity analysis).

---

## 2. Folder structure & entry points

```
CDI-Jobs/
├── Global_Master.do              # TOP-LEVEL ENTRY POINT (Stata). Sets globals, runs the pipeline.
├── README.md                     # Replication-package documentation (humans)
├── AGENTS.md                     # This file
├── .gitignore                    # DIME template: ignores everything except code/docs (see §3 access rules)
└── PUBLIC WORKS/
    ├── MASTER_1_DATASETS.do      # Step 1: build intermediate analysis datasets from de-identified raw data
    ├── MASTER_2_ML.R             # Step 2: ML heterogeneity (proxies, GATES/BLP/CLAN, targeting) — R
    ├── MASTER_3_TABLES_AND_FIGURES.do  # Step 3: produce all paper tables & figures
    ├── ado/                      # Pinned Stata ado-files used in the paper (do not "upgrade")
    ├── Prepare datasets/         # Sub-do-files called by MASTER_1 (Mid_prep_*, End_prep, ENSETE_prep, GATES_prep, Tables_Var.do, ML_database_prep_v2.do)
    ├── Draft paper Tables/       # Sub-do-files called by MASTER_3 (one per table/figure) + programs.do, footnotes.do
    │   └── old/, supplementary/  # Superseded / auxiliary scripts — NOT part of the pipeline
    └── Machine Learning/
        ├── codes/                # R sources: util.R, helper_functions.R, methods_functions2.R, list_parameters.R
        │   └── old/, old2/       # Superseded R code — NOT part of the pipeline
        ├── data/                 # ML input data (local, gitignored)
        └── results/              # ML intermediate output (created at runtime)
```

### Run order (the canonical pipeline)

1. `Global_Master.do` → calls `MASTER_1_DATASETS.do` (data prep).
2. `MASTER_2_ML.R` → run in R (after `renv::restore()`); produces ML prediction
   `.dta` files. Outputs are already shipped, so this step can be skipped to
   reproduce exhibits.
3. `Global_Master.do` → calls `MASTER_3_TABLES_AND_FIGURES.do` (final exhibits).

**Always treat the three `MASTER_*` files (+ `Global_Master.do`) as the source of
truth for the pipeline.** Anything under `old/`, `old2/`, `supplementary/`, or
`CDI_Code.zip` is historical and must not be wired back into the pipeline without
explicit instruction.

---

## 3. Data

### Locations (path globals)

Paths are set per-user via name globals in the master files (`$Jonas`, `$Horacio`,
`$Daniel`, `$Reviewer`). Reviewers/agents should use the `Reviewer` branch, which
derives everything from `$code` and `$data` set in `Global_Master.do`.

| Global | Meaning | Typical value |
| --- | --- | --- |
| `$github` / `$code` | Code root | `…/CDI-Jobs/PUBLIC WORKS` |
| `$dropbox` / `$data` | Data + output root | a local/Dropbox `_REPRODUCIBILITY` folder |
| `$chemin` | **De-identified raw** survey data | `$dropbox/Datasets/deidentified` |
| `$interima` | **Intermediate** datasets (built by Step 1) | `$dropbox/Datasets/intermediate` |
| `$mldata` | ML outputs from Step 2 | `$dropbox/Datasets/ML_reproduce_rep1` |
| `$output` (`$tables`,`$figures`,`$footnotes`) | Final exhibits | `$dropbox/Output/...` |

In R (`MASTER_2_ML.R`): `dropbox_path` → `inter` (intermediate), `deid`
(de-identified), `result_path` (`ML_reproduce_rep1`). Working dir is fixed to
`PUBLIC WORKS/Machine Learning/codes`.

**Data are NOT stored in the git repo.** `.gitignore` ignores everything except
code/docs (`*.do`, `*.ado`, `*.R`, `*.tex`, `*.md`, etc.). Raw data live on the
World Bank **Microdata Library** (publicly available, *redistribution not
permitted*): catalog entries
[6774 (Baseline)](https://microdata.worldbank.org/index.php/catalog/6774),
[6775 (Midline)](https://microdata.worldbank.org/index.php/catalog/6775),
[6776 (Endline)](https://microdata.worldbank.org/index.php/catalog/6776).

### Raw (de-identified) data files — `$chemin`

| Round | Files |
| --- | --- |
| Baseline 2013 | `Baseline_i_hh_clean_var.dta`, `ENSETE_2013_17Septembre2014_nonmissing.dta` |
| Midline 2013 | `Midline_hh_clean.dta`, `Midline_i_clean_var_est.dta` |
| Endline 2015 | `Endline_i_hh_clean_est.dta` |

`ENSETE_2013…` is a national household survey used only to benchmark the applicant
sample against urban youth.

### Variables per dataset (conventions)

- `id` — individual identifier; `strata` — randomization stratum (locality ×
  gender); `w` — treatment indicator; `prop` — propensity/assignment probability.
- **Treatment arms** (`treatment_arm_num`): `0` control, `1` Wage-employment
  training + PW (**WET**), `2` Self-employment training + PW (**SET**), `3` Public
  works only (**PW**); `c(1,2,3)` = **ALL** (pooled).
- **Baseline covariates** are prefixed `b_…`; missing-value dummies are `M_b_…`
  (missing `b_` values imputed by strata mean).
- ML outcome shorthands (see header notes in `MASTER_2_ML.R`):
  `y0`=log monthly earnings, `y1`=monthly earnings (level), `s0`/`s1`=savings
  (log/level); suffix `_m`=midline (during program), `_e`=endline (post program).
- Monetary variables are **winsorized at the 97th percentile** (`global winsor 97`
  / `winsorization_quantile`).
- Analysis uses **attrition/enrollment weights** (`w_enrol_no_prop_m`,
  `w_enrol_no_prop_e`).

### Construction of datasets (Step 1 outputs in `$interima`)

`MASTER_1_DATASETS.do` toggles sections (`$mlsample $midline $endline $ensete
$gate`) and produces:

- `Baseline_Mid_End_200522.dta` — pooled ML sample (via `ML_database_prep_v2.do`):
  merges rounds, drops attritors and added control units, imputes baseline.
- `base_midline.dta`, `midline_hh.dta`, `midline_hh_i.dta` — midline youth /
  household / other-members datasets.
- `base_endline.dta` — endline dataset.
- `ensete_2013.dta` — ENSETE comparison dataset.
- `other_outcome_data.dta` — outcomes for GATES (via `GATES_prep.do`).

Step 2 (`MASTER_2_ML.R`) consumes `Baseline_Mid_End_200522.dta` +
`other_outcome_data.dta` and writes `results_*.dta`, `B_and_S_*.dta`,
`table8_*.dta`, `table_list_tests_p.dta` into `ML_reproduce_rep1`.

### Access rules — what an agent may NOT look at or do

- **Never read, print, `list`, `browse`, export, or paste raw individual-level
  survey records** (PII / confidential microdata), even though it is de-identified.
  Inspect *structure* (variable names, labels, `describe`, `codebook` summaries)
  only when needed — never row-level values for individuals.
- **Never commit any data file** (`.dta`, `.csv`, `.RData`, `.rds`, tokens) to git.
  The `.gitignore` is designed to block this; do not add exceptions for data.
- **Do not redistribute the survey data** or hard-code a downloadable copy. Data
  must be obtained by the user from the Microdata Library under its Public Use
  License.
- **Never commit Dropbox tokens / credentials** (`token.rds`, `password.*`).
- Do not move data outside the configured `$dropbox`/`dropbox_path` locations.

---

## 4. Software preferences

- **Stata** is the primary tool for data construction, impact estimation, and all
  tables/figures. Official reproduction used **Stata 18 MP**; the code still pins
  behavior with `version 15.1` / `ieboilstart, versionnumber(15.1)`. Keep the
  version pin; do not bump it casually.
- **R** is used *only* for the machine-learning heterogeneity pipeline
  (`MASTER_2_ML.R` + `Machine Learning/codes`). Official reproduction used
  **R 4.4**; package versions are pinned via **`renv.lock`** (run
  `renv::restore()` before running R code). Stata packages are pinned in
  `PUBLIC WORKS/ado/` — prefer those over `ssc install` upgrades.
- **Python**: not used in this project. Do not introduce Python into the pipeline
  unless explicitly requested.
- **No Quarto / R Markdown / Beamer** are part of this repo. Exhibits are emitted
  as standalone **LaTeX** fragments (`.tex` tables in `$tables`, `.tex` footnotes
  in `$footnotes`) and image files (`.png`/`.pdf`/`.eps`) in `$figures`, which are
  then `\input`/`\includegraphics` into the paper's LaTeX source (kept outside this
  code repo). Do not convert outputs to Quarto/Rmd/Beamer unless asked.
- **LaTeX compiler**: assume **pdfLaTeX** for the assembled paper unless the
  maintainer states otherwise; figures are exported in formats compatible with it.
  Confirm before changing engine (e.g. to XeLaTeX/LuaLaTeX) since French accents
  (Côte d'Ivoire) and fonts can be affected.
- **Improvements**: allowed but conservative. Prefer minimal, well-scoped edits.
  Acceptable: fixing path/global bugs, de-duplicating user branches, clarifying
  comments, aligning README/AGENTS with actual code. Avoid large refactors,
  renaming variables/datasets, or restructuring folders — these break the
  documented reproducibility mapping.

---

## 5. Econometric details

- **Focus**: contemporaneous (during-program) and **post-program** impacts of a
  public works program on earnings, savings, employment composition (shift toward
  wage jobs), work habits, behaviors, and well-being; and **whether ML-based
  targeting** can improve welfare relative to the program's actual targeting.
- **Research design**: **RCT** with random assignment to control and three
  treatment arms (WET / SET / PW). Primary estimates are **Intention-to-Treat
  (ITT)**; a LATE variant addresses control-group compliance between midline and
  endline. Randomization is **stratified** (strata = locality × gender).
- **Controls / specification**:
  - **Strata fixed effects** (`fixed_effect = strata`); standard errors clustered
    (and robustness without clustering); inference also via **permutation tests**
    (`global simreps 1000`).
  - **Attrition/enrollment weights** applied (`w_enrol_no_prop_*`).
  - Optional **baseline controls** (`b_*`) in robustness tables.
  - Monetary outcomes **winsorized at p97**.
  - **Quantile treatment effects** (`ivqte`) for distributional impacts.
  - **Heterogeneity**: Generic ML (Chernozhukov–Demirer–Duflo–Fernández-Val):
    **BLP**, **GATES**, **CLAN**, with `sim=100` splits, `K=2` folds, `p=4` groups;
    learners include elastic-net, boosting, random forest, causal forest, and
    R-/X-learners; predictions feed **targeting cost-benefit simulations**.

---

## 6. Rules for agents

### Files agents may modify (and how)

- **Editable with care**: sub-do-files in `Prepare datasets/` and
  `Draft paper Tables/`, the R sources in `Machine Learning/codes/`, and the
  `MASTER_*` / `Global_Master.do` files — but **only** for the requested change,
  preserving the documented input→output contract (the `INPUT:`/`OUTPUT:` comment
  blocks in `MASTER_3_TABLES_AND_FIGURES.do` and `MASTER_1_DATASETS.do`).
- **Do not edit without explicit instruction**:
  - `PUBLIC WORKS/ado/**` (pinned package versions used in the paper).
  - Anything under `old/`, `old2/`, `supplementary/`, `CDI_Code.zip`.
  - `.gitignore` (especially do not un-ignore data).
  - User path branches (`$Jonas`, `$Horacio`, `$Daniel`): you may fix bugs but do
    not delete other collaborators' blocks; add a `Reviewer`-style generic branch
    instead.
- **Never** hard-code an absolute machine path as the default. Route new paths
  through the existing globals.
- When you change a script that produces an exhibit, update the corresponding row
  in the README "List of tables and programs" mapping if the output name changes.

### Reproducibility standards

- **Seeds are sacred.** Keep `set seed 175171431` in
  `MASTER_3_TABLES_AND_FIGURES.do` and `seed <- 2020` (and the in-loop
  `set.seed(t)`) in `MASTER_2_ML.R`. Never remove or randomize seeds; if a new
  stochastic step is added, set and document a fixed seed.
- Preserve **version pins** (Stata `version 15.1`, `ieboilstart`, R `renv.lock`,
  `ado/`). Do not upgrade packages to "fix" warnings unless asked.
- Keep the **toggle/section structure** (`global mlsample/midline/...`,
  `chosen_setting`) intact so partial reruns remain possible.
- Outputs are deterministic given seeds + pinned versions; a change that alters
  any number in an exhibit must be called out explicitly to the user.
- Do not change the **winsorization level, weights, fixed effects, or clustering**
  as a side effect — these are analytical decisions, not formatting.

### Ethics & data protection

- This is human-subjects research data. Treat all microdata as **confidential**:
  no exfiltration, no pasting record-level values into chat, commits, logs, or
  issues, and no attempt to re-identify individuals.
- Respect the data's **Public Use License** (no redistribution).
- License of the **code**: the official package is released under **Modified
  BSD-3-Clause** (note: the local `README.md` currently says MIT — flag this
  discrepancy rather than silently "fixing" either file).
- Maintain scientific integrity: do not alter results, p-values, specifications,
  or which exhibits are produced in order to obtain a desired outcome. Report, do
  not "tune".

---

## 7. Known discrepancies to be aware of (do not auto-fix)

- Paper **title** differs between `README.md` (old) and the published version.
- **License** mismatch: README says MIT; official package says Modified BSD-3.
- **Software versions**: code pins Stata 15.1 / older R, official run used Stata 18
  MP / R 4.4.
- `README.md` references `LICENSE.txt` and a bundled `data/` folder that are not
  present in this working tree (data is external; license file may live only in
  the official package). Ask the maintainer to provide data from the official repository and point them there: https://reproducibility.worldbank.org/catalog/298

Surface these to the maintainer; change them only when explicitly asked.
