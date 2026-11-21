# Data Dictionary — Exported Result Tables (`results/tables/`)

## 1. Signal Quality & Epoch Audit Tables
- **`Table_S0_Epoch_Sanity_Audit.csv`**: Automated comparison of extracted `HR_bpm` against `subjects.csv` reference HR columns (`Pearson_r`, `Spearman_rs`, `MAE_bpm`, `Bias_bpm`, `Med_RMSSD_ms`, `Med_DFA_a1`, `Pass_Check`).
- **`Table_S0B_HR_Outliers_gt5bpm.csv`**: Subject-level list of any epoch differing by >5 bpm from `subjects.csv` (includes `Extracted_HR`, `GT_HR`, `Diff_bpm`, `RMSSD_ms`, `SQI`).
- **`Table_S1_Master_Epoch_Features_Nabian2018_1000Hz.csv`**: Full 392-epoch extracted feature table across 75 subjects (114 columns: metadata, SQI, RR quality flags, HR, EDR respiration, PRSA DC/AC, Coarse MSE 6–15, and full NeuroKit2 linear/spectral/nonlinear HRV battery).

## 2. Multicollinearity & LMEM Diagnostic Tables
- **`Table_S2_VIF_Multicollinearity.csv`**: Variance Inflation Factors (`VIF`) and `Tolerance` (`1 / VIF`) across the main-effects LMEM design matrix (all predictors pass `VIF < 5.0`, range `1.003–1.759`).
- **`Table_S3_LMEM_Diagnostics_ICC_R2_Shapiro.csv`**: Random-intercept variance (`Var_u0`), residual variance (`Var_eps`), Intraclass Correlation Coefficient (`ICC`), Nakagawa–Schielzeth Marginal and Conditional $R^2$, REML log-likelihood, and Shapiro–Wilk residual normality statistics across both modeling suites.

## 3. Primary Manuscript Statistical Tables
- **`Table1_Demographics_and_Resting_Subtypes.csv`**: Cohort demographics ($N = 72$) and resting baseline (`Stress_Score == 0`) subtype means and SDs.
- **`Table1B_Resting_Hypothesis_Tests.csv`**: Resting 4-group ANOVAs and Welch/Mann–Whitney pairwise comparisons for H1 (Multiscale Complexity Ratios) and H2 (`PRSA_DC_clean`).
- **`Table2_Task_State_Descriptives.csv`**: Descriptive statistics (`count`, `mean`, `std`, `median`) across all six protocol tasks (States 0–3).
- **`Table3_LMEM_StrictSinus_Orthostatic.csv`**: REML LMEM parameter estimates (`Beta`, `SE`, `z_stat`, `p_value`, 95% CI, `ICC`) across the strict-sinus orthostatic transition ($N = 236$ epochs, $67$ subjects).
- **`Table4_LMEM_4State_Continuum.csv`**: REML LMEM parameter estimates across the calibrated 4-state stress continuum ($N = 377\text{–}386$ epochs, $72$ subjects).
- **`Table5_Translational_Spearman_Coupling.csv`**: Two-tailed Spearman rank correlations ($r_s$, $R^2$ rank %, $p$-value, $N$) linking resting and Empirical Bayes reactivity slopes (`u1i_*`) to TCD CBFV, MMPF phase shift, Trail Making Part B, 12-min hallway gait velocity, and NIHSS.
