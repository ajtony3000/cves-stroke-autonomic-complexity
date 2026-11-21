#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated GitHub Repository Scaffold Builder
Organizes downloaded Kaggle/Colab outputs and generates all required GitHub
root & documentation files:
    - requirements.txt
    - .gitignore
    - LICENSE (MIT)
    - CITATION.cff
    - docs/DATA_DICTIONARY.md
    - Full folder hierarchy (src/, docs/, results/tables/, results/figures_publication/,
      results/figures_supplementary/, results/supplementary_tachograms/, logs/)

Usage:
    python build_github_repo.py --source ./unzipped_kaggle_outputs --target ./cves-stroke-autonomic-complexity
"""

import argparse
import shutil
import sys
from pathlib import Path

# =============================================================================
# 1. STANDARD GITHUB COMPANION FILE TEMPLATES
# =============================================================================
REQUIREMENTS_TXT = """# Core scientific computing
numpy>=1.24.0
pandas>=2.0.0
scipy>=1.10.0

# Signal processing & PhysioNet WFDB I/O
neurokit2>=0.2.7
wfdb>=4.1.0
awscli>=1.29.0

# Hierarchical mixed-effects modeling & diagnostics
statsmodels>=0.14.0
patsy>=0.5.3

# Publication visualization & progress reporting
matplotlib>=3.7.0
seaborn>=0.13.0
tqdm>=4.65.0
"""

GITIGNORE_TXT = """# Raw PhysioNet CVES binary waveforms & clinical registry (download via AWS S3)
cves-dataset/
*.dat
*.hea
subjects.csv

# Large archives & optional bulk QC plots (~784 PNGs; archive on OSF/Zenodo instead)
*.zip
*.tar.gz
Supplementary_QC_Plots/
results/supplementary_qc_plots/

# Python environments & caches
.venv/
venv/
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/

# Jupyter, Kaggle & IDE metadata
.ipynb_checkpoints/
.virtual_documents/
.vscode/
.idea/

# OS metadata
.DS_Store
Thumbs.db
"""

MIT_LICENSE_TXT = """MIT License

Copyright (c) 2026 Aswin Tony Joseph

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

CITATION_CFF_TXT = """cff-version: 1.2.0
message: "If you use this pipeline or derived feature tables, please cite this software and the PhysioNet CVES dataset."
title: "Hemispheric Dissociation of Multiscale Autonomic Complexity and Cardiovagal Reserve in Chronic Ischemic Stroke (CCS 1000 Hz Pipeline)"
version: "1.0.0"
date-released: "2026-11-20"
license: MIT
authors:
  - family-names: "Joseph"
    given-names: "Aswin Tony"
    email: "aswintony7@gmail.com"
    affiliation: "Government Medical College Thiruvananthapuram, Kerala, India"
  - family-names: "Venugopal"
    given-names: "Rahul"
    affiliation: "Centre for Consciousness Studies, Department of Neurophysiology, NIMHANS, Bengaluru, India"
keywords:
  - chronic ischemic stroke
  - heart rate variability
  - multiscale entropy
  - deceleration capacity
  - linear mixed-effects models
  - PhysioNet CVES
"""

DATA_DICTIONARY_MD = """# Data Dictionary — Exported Result Tables (`results/tables/`)

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
- **`Table4_LMEM_4State_Continuum.csv`**: REML LMEM parameter estimates across the calibrated 4-state stress continuum ($N = 377\\text{–}386$ epochs, $72$ subjects).
- **`Table5_Translational_Spearman_Coupling.csv`**: Two-tailed Spearman rank correlations ($r_s$, $R^2$ rank %, $p$-value, $N$) linking resting and Empirical Bayes reactivity slopes (`u1i_*`) to TCD CBFV, MMPF phase shift, Trail Making Part B, 12-min hallway gait velocity, and NIHSS.
"""

# Mapping from Kaggle workspace folder names to clean GitHub repo paths
FOLDER_MAP = {
    "Tables_CSV": "results/tables",
    "Figures_Publication": "results/figures_publication",
    "Figures_Supplementary": "results/figures_supplementary",
    "Supplementary_Tachograms": "results/supplementary_tachograms",
}


# =============================================================================
# 2. REPOSITORY BUILDER LOGIC
# =============================================================================
def create_directory_tree(repo_root: Path) -> None:
    """Creates the standardized GitHub folder hierarchy."""
    subdirs = [
        "src",
        "docs",
        "results/tables",
        "results/figures_publication",
        "results/figures_supplementary",
        "results/supplementary_tachograms",
        "logs",
    ]
    for rel in subdirs:
        (repo_root / rel).mkdir(parents=True, exist_ok=True)


def write_companion_files(repo_root: Path) -> None:
    """Writes requirements.txt, .gitignore, LICENSE, CITATION.cff, and DATA_DICTIONARY.md."""
    files_to_write = {
        "requirements.txt": REQUIREMENTS_TXT,
        ".gitignore": GITIGNORE_TXT,
        "LICENSE": MIT_LICENSE_TXT,
        "CITATION.cff": CITATION_CFF_TXT,
        "docs/DATA_DICTIONARY.md": DATA_DICTIONARY_MD,
    }
    for rel_path, content in files_to_write.items():
        dest = repo_root / rel_path
        dest.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"  [WRITE] {rel_path}")


def copy_kaggle_outputs(source_dir: Path, repo_root: Path) -> None:
    """Copies unzipped Kaggle workspace folders and logs into their clean GitHub paths."""
    if not source_dir.exists():
        print(f"  [WARN] Source directory not found: {source_dir} (created empty scaffold only).")
        return

    # Copy mapped output folders
    for src_sub, dst_rel in FOLDER_MAP.items():
        src_path = source_dir / src_sub
        dst_path = repo_root / dst_rel
        if src_path.exists() and src_path.is_dir():
            count = 0
            for item in sorted(src_path.iterdir()):
                if item.is_file() and not item.name.startswith("."):
                    shutil.copy2(item, dst_path / item.name)
                    count += 1
            print(f"  [COPY]  {src_sub:<26} -> {dst_rel} ({count} files)")

    # Copy run_log.txt if present
    log_src = source_dir / "run_log.txt"
    if log_src.exists():
        shutil.copy2(log_src, repo_root / "logs" / "run_log.txt")
        print("  [COPY]  run_log.txt                -> logs/run_log.txt")

    # Copy pipeline Python scripts if present in source_dir
    for py_file in sorted(source_dir.glob("*.py")):
        if py_file.name != Path(__file__).name:
            shutil.copy2(py_file, repo_root / "src" / py_file.name)
            print(f"  [COPY]  {py_file.name:<26} -> src/{py_file.name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a clean GitHub repository scaffold for the CVES Stroke HRV project."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("./cves_nabian2018_ccs_workspace"),
        help="Path to the unzipped Kaggle/Colab workspace folder.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path("./cves-stroke-autonomic-complexity"),
        help="Target path for the new GitHub repository folder.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = args.target.resolve()
    source_dir = args.source.resolve()

    print("=" * 72)
    print(f"Building GitHub Repository Scaffold at: {repo_root}")
    print("=" * 72)

    try:
        create_directory_tree(repo_root)
        write_companion_files(repo_root)
        copy_kaggle_outputs(source_dir, repo_root)
    except Exception as exc:
        print(f"[ERROR] Failed to construct repository scaffold: {exc}", file=sys.stderr)
        sys.exit(1)

    print("-" * 72)
    print("[DONE] Repository scaffold ready. Next Git commands:")
    print(f"       cd {repo_root}")
    print("       # Place README.md at root, LMEM_Justification_and_Code_Reasoning.md in docs/,")
    print("       # and cves_stroke_hrv_nabian2018_ccs_pipeline_v2.py in src/.")
    print("       git init && git branch -M main")
    print("       git add . && git commit -m 'Initial release: 1000 Hz CCS Nabian2018 stroke HRV pipeline'")
    print("       git remote add origin https://github.com/<your-username>/cves-stroke-autonomic-complexity.git")
    print("       git push -u origin main")
    print("=" * 72)


if __name__ == "__main__":
    main()