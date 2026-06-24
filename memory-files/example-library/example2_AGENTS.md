# Project: Supplier-Network Paper

Project-specific notes. My global profile/preferences live in `~/.claude/CLAUDE.md`;
this file adds only what's specific to this work.

## What this is

Applied-micro paper on **firm upgrading in a manufacturing cluster**: how a firm's
exposure to **horizontal cluster peers** vs its **vertical lead buyers** affects firm
performance. Single paper, single pipeline. Main project lives in `Analysis/`.

- Paper source — `Analysis/Paper.tex` (+ PDF).
- Shareable replication package: `Replication_Package/` (`overleaf/` = upload to
  Overleaf; `replication/` = data + code).

## Directory map (`Analysis/`)

- `Paper.tex` — the paper (+ PDF). (`Analysis_old.tex` is an older/separate doc — the
  **paper** is `Paper.tex`.)
- `code/` — all do-files (index below).
- `data_built/` — `sample.dta`, built by `01`.
- `output/{main,appendix,figures}` — generated tables + the one figure (`scatter.png`),
  `\input` by the paper.
- `logs/` — Stata run logs.
- `HANDOFF*.md`, `*_audit*.md`, `structure_rationale.md`, `AUDIT_FINDINGS.md` — older
  working notes; background context only, may be stale.
- **Raw inputs live OUTSIDE this folder** (`../raw_checks/Raw_Data`, `../method_1…`,
  `../templates/sibling`); they're bundled into the replication package under
  `replication/Analysis/data_raw/`.

## Tooling & paths (verified on this machine)

- **Stata 14.2 MP**: `D:\Stata14\StataMP-64.exe` (NOTE: D: drive, not C:).
  Batch run: `StataMP-64.exe -e do file.do arg1 arg2` → args become `1' `2' / `args`.
- **pdflatex (MiKTeX)**: `C:\Users\<user>\AppData\Local\Programs\MiKTeX\miktex\bin\x64`.
  Compile **twice** for cross-refs.
- **Python 3.12** available (for table post-processing; `openpyxl` installed).
- The paper has **no bibliography** — cite as plain text (e.g. "Author and Author (YEAR)"),
  not `\cite`.

## Stata gotchas

- **`StataMP-64.exe` is a GUI app** → launching via `&`/`Start-Process` returns
  IMMEDIATELY (does not block). To actually wait, use `Start-Process ... -Wait`.
  The upside: a detached Stata run **survives** the Claude session ending.
- **Long runs**: a session-owned background task dies on context compaction, silently
  killing Stata. And **`postfile` buffers everything until `postclose`** — an
  interruption loses ALL of it. For long jobs: write **one checkpoint file per cell/unit**
  + per-cell `set seed = base + id` (resumable, reproducible), and run detached.
- **Multi-core/all-core load triggers Windows LiveKernelEvents** (kernel faults that kill
  processes). Keep heavy Stata runs **single-process**.
- Keep-awake during long runs: a live process holding
  `SetThreadExecutionState([uint32]2147483649)` (ES_CONTINUOUS|ES_SYSTEM_REQUIRED).
- PowerShell here: prefer `Start-Process -Wait`; `pdflatex` needs the MiKTeX path on
  `$env:Path`. Backslash-heavy regex in the Bash tool is unreliable — use a Python script.

## Code layout

- `Analysis/code/_paths.do` sets all globals (`built`, `out_main`, `out_app`,
  `raw`, etc.). Every do-file includes it. `00_run_all.do` is the master.
- Do-files `01`–`14` are **numbered to match the paper's table order**. `01_build_sample.do`
  is the only one that reads raw inputs; `02`–`14` read `${built}/sample.dta`.

### Do-file → table(s) it writes (numbered to paper order)

| # | do-file | produces (`output/main/` unless noted) |
|---|---------|------------------------------------------|
| 01 | `build_sample` | `sample.dta` (**only one that reads raw inputs**) |
| 02 | `descriptives` | `t1_descriptives` |
| 03 | `attrition` | `t2_attrition` (surveyed vs non-surveyed firms) |
| 04 | `balance` | `t3_balance` (+ `balance_binary_*` in appendix) |
| 05 | `peer_main` | `peer_main` (headline peer result) |
| 06 | `buyer_main` | `buyer_main` (headline buyer result) |
| 07 | `joint_channels` | `joint_channels` (both exposures in one model) |
| 08 | `exposure_gradient` | `exposure_gradient` |
| 09 | `het_size` | `het_size_peer`, `het_size_buyer` |
| 10 | `het_age` | `het_age_peer`, `het_age_buyer` |
| 11 | `nonlinearity` | `quad_peer`, `quad_buyer` |
| 12 | `decomposition` | `decomp1_productivity`, `decomp2_quality`, `decomp3_upgrading` |
| 13 | `robustness` | `robust_altfe`, `robust_altcluster`, `robust_winsor` |
| 14 | `permutation_inference` | `ri_peer`, `ri_buyer` — **SLOW** (`ritest`) |
| — | `placebo_{run,combine,tables}.do` | `placebo` — **SLOW** 10k-draw permutation; not in `00_run_all` |

Heterogeneity do-files build filenames dynamically (`table_het_*_`split'`), so they don't
appear as literal strings in the do-file.

## esttab output needs post-processing (IMPORTANT)

The committed `output/` tables are **post-processed**; the do-files alone produce raw
`esttab` output that **won't compile**. Two fixes (see
`Replication_Package/replication/postprocess_tables.py`):
1. `esttab` escapes `_`→`\_` inside `\label{}`/`\ref{}` — illegal in hyperref's
   `\csname` (the "Missing `\endcsname`" crash). Unescape them.
2. `esttab` puts notes in a wide `\multicolumn{N}{p{1.3\textwidth}}` row that stretches
   landscape tables and strands the last column. Convert to `threeparttable`/`tablenotes`.
After re-running any Stata pipeline, run the post-processor before compiling.

## Conventions established

- **Exposure** is measured as a **leave-one-out, standardized**. Never include the focal
  firm in its own exposure.
- Continuous covariates are **winsorized at 1/99** before standardizing.
- Permutation/placebo p-values use **`ritest`** with the seed base below.

## Canonical specification (don't deviate silently)

Unit = **firm-year**. Every main table is a column-by-column `reghdfe`, **no weights**, SE
**clustered by cluster-year** (`clusteryear = group(cluster_id year)`). `y` loops over the
`$all_outcomes`. `lnemp` is **always** included; FE are **cohort×region** plus **sector**.

```stata
* PEER (05_peer_main) — headline channel:
*   reghdfe `y' z_peer_exp lnemp, absorb(i.cohort##i.region i.sector) vce(cluster clusteryear)
* BUYER (06_buyer_main) — second main channel:
*   reghdfe `y' z_buyer_exp lnemp, absorb(i.cohort##i.region i.sector) vce(cluster clusteryear)
* JOINT (07_joint_channels) — both exposures together:
*   reghdfe `y' z_peer_exp z_buyer_exp lnemp, absorb(i.cohort##i.region i.sector) vce(cluster clusteryear)
```

**Dropping an `absorb` term, the `lnemp` control, or clustering at the wrong level produces
a table that compiles fine and is wrong.**

## Golden numbers (a correct run must reproduce these)

Headline = Outcome 1 (column 1). Record the committed coefficients and N here as a
regression check after each verified run; treat the values below as placeholders to fill
in from your own `output/main/` tables (clustered SE; `*`=10%, `**`=5%, `***`=1%).

| spec | coef (col 1) | N |
|------|--------------|---|
| Peer exposure (05) | `[+0.NNN]**` | `[N]` |
| Buyer exposure (06) | `[-0.NNN]**` | `[N]` |
| Joint — peer (07) | `[+0.NNN]**` | `[N]` |
| Joint — buyer (07) | `[-0.NNN]*` | `[N]` |

If a change moves these, something broke; investigate before proceeding.

## Data dictionary (load-bearing variables)

- **Peer exposure**: `peer_exp` = leave-one-out exposure over cluster-mates →
  standardised `z_peer_exp = std(peer_exp)`.
- **Buyer exposure**: `buyer_exp` = leave-one-out exposure over the firm's lead-buyer set →
  `z_buyer_exp = std(buyer_exp)`.
- **Outcomes** (`$all_outcomes`, 10): 8 standardized summary indices `= std(mean of std'd
  items)` (productivity, output_quality, export_intensity, input_upgrading, tech_adoption,
  workforce_skill, capacity_utilization, management_quality) + 2 binary certifications
  (cert_claim, cert_obtained). Column order = this list.
- **FE**: `cohort`×`region` plus `sector`. **Cluster**: `clusteryear`.
- Unobserved firm size → mean-imputed with an **absorbed missing-indicator FE** so every
  column keeps the same sample.

## Guardrails — read-only by convention

- **Do not hand-edit committed `output*/` tables** — machine-generated then post-processed;
  edit the do-file → rerun → postprocess instead.
- **Do not modify raw inputs in place.**
- Looks broken but isn't: padded numbers / escaped `\_` in *freshly* generated esttab
  output (postprocess fixes them); empty `data_built/` & `logs/` in the shared package
  (regenerated on first run).

## Reproducibility & version control

- Lives in Dropbox (synced). Source: `code/`, `Paper.tex`, `data_raw` (package), this
  file. Regenerated/disposable: `data_built/`, `logs/`, `output/`, `*.pdf`, LaTeX
  `*.aux/.log`.
- **Pinned**: Stata 14.2 MP; `reghdfe` 6.12.3, `ftools` 2.49.1, `estout` 3.23, `ritest`
  1.1.2. (reghdfe singleton/collinearity handling is version-sensitive — match before
  trusting a diff.) Permutation seed base **12345678** (+cell id).

## Runbooks

- **Full rebuild**: in Stata `cd` to the folder, `do 00_run_all.do` →
  `python postprocess_tables.py "<output dir>"` → `pdflatex` ×2. The replication package's
  `run.do` wraps this.
- **Add a table**: take the next `NN` in paper order; do-file reads `${built}/sample.dta`,
  `esttab` → `${out_main}`; add its line to the master, `\input` it in the `.tex`,
  postprocess, compile.
- **Recover a dead detached run**: each cell wrote its own checkpoint, so just relaunch the
  same do-file detached — it skips finished cells and resumes (per-cell seed → identical
  results). Don't restart from zero.

## Working style & doc authority

- **Authoritative**: this file, `_paths.do`, current `code/`. **Background only (may be
  stale)**: `HANDOFF*.md`, `*_audit*.md`, `AUDIT_FINDINGS.md`, `structure_rationale.md`
  (bigger "why" rationale lives there). If a handoff disagrees with current code, trust the
  code.
