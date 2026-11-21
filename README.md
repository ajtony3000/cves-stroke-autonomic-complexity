
# Hemispheric Dissociation of Multiscale Autonomic Complexity and Cardiovagal Reserve in Chronic Ischemic Stroke

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Data: PhysioNet CVES v1.0.0](https://img.shields.io/badge/PhysioNet-CVES%20v1.0.0-orange.svg)](https://physionet.org/content/cves/1.0.0/)

Reproducible neurophysiological signal-processing, forensic sampling-clock calibration, and hierarchical linear mixed-effects modeling (LMEM) pipeline accompanying the manuscript:

> **Hemispheric Dissociation of Multiscale Autonomic Complexity and Cardiovagal Reserve Predicts Orthostatic Cerebral Perfusion and Gait Speed in Chronic Ischemic Stroke**  
> Aswin Tony Joseph¹\*, Rahul Venugopal²  
> ¹ Government Medical College Thiruvananthapuram, Kerala, India  
> ² Centre for Consciousness Studies (CCS), Department of Neurophysiology, NIMHANS, Bengaluru, India  
> \* Correspondence: `aswintony7@gmail.com`

---

## 1. Scientific & Methodological Highlights

1. **Upfront 1000 Hz LabVIEW Clock Calibration:** Resolves a silent metadata defect in PhysioNet `cves` v1.0.0 where `sit-stand-balance` WFDB `.hea` headers are stamped `500 Hz` despite `1000 Hz` LabVIEW acquisition. Overriding `true_fs = 1000.0` upfront prevents sliding-window contraction ($\pm 200\text{ ms} \to \pm 100\text{ ms}$) in `nabian2018`, restoring 100% `OK` epoch fidelity ($N = 392$ epochs across $75$ subjects; `StandEC` HR vs. `subjects.csv`: $r = 0.994$, $\text{MAE} = 0.81\text{ bpm}$).
2. **Hemispheric Multiscale Complexity Dissociation (H1):** Across $72$ protocol-completing participants ($386$ validated epochs), resting Coarse Multiscale Complexity Ratio ($\text{MSE}_{6\text{–}15}/\text{SampEn}$) separates clinical subtypes ($F = 10.43, p = 0.00002$; Right vs. Left MCA $t = -6.06, p = 0.00001$), with Right MCA stroke dropping below unity ($0.966 \pm 0.225$) and exhibiting accelerated 4-state `HRV_CMSEn` collapse ($\beta_3 = -0.047, p = 0.0280$), while Left MCA stroke suppresses fine-scale vagal irregularity ($1.500 \pm 0.209$).
3. **Pan-Stroke Cardiovagal Depletion & Orthostatic Floor Effect (H2):** Chronic stroke survivors show a **44.6%** reduction in resting PRSA Deceleration Capacity ($6.72$ vs. $12.13\text{ ms}$, Mann–Whitney $U\ p = 0.0013$) and blunted vagal withdrawal upon standing/tilting (4-state LMEM: Left MCA $\times$ Stress $\beta_3 = +1.390, p = 0.0090$; Right MCA $\times$ Stress $\beta_3 = +1.181, p = 0.0137$; $\text{ICC} = 0.551$; all $\text{VIF} \le 1.759$).
4. **Five-Compartment Translational Coupling (H4):**
   - **Orthostatic Cerebral Perfusion ($\Delta\text{MCAL}$ CBFV):** Resting `CCS_Multiscale_Ratio` $r_s = +0.473, p = 0.00046$ ($22.4\%$ rank variance, $N = 51$).
   - **Dynamic Autoregulation Phase (`MMPF`):** Resting `PRSA_DC_clean` $r_s = -0.342, p = 0.0160$ (Right MCA, $N = 49$) and $r_s = -0.276, p = 0.0287$ (Left MCA, $N = 63$).
   - **Executive Set-Shifting (`TMT Part B`):** Orthostatic `PRSA_DC` slope `u1i_Ortho_DC` $r_s = +0.315, p = 0.0106$ ($N = 65$).
   - **Ambulatory Gait Speed (`12-Min Walk 2`):** Tilt fractal reactivity `u1i_Day2Tilt_DFAa1` $r_s = +0.361, p = 0.0063$ ($N = 56$).
   - **Stroke Severity (`NIHSS`):** Stand multiscale slope `u1i_Day1Stand_RCMSEn` $r_s = +0.522, p = 0.00056$ ($27.2\%$ variance, $N = 40$).

---

## 2. Repository Architecture

```text
cves-stroke-autonomic-complexity/
├── README.md                                              # Project overview, architecture & reproducibility guide
├── LICENSE                                                # MIT License
├── CITATION.cff                                           # Machine-readable citation metadata
├── requirements.txt                                       # Pinned Python dependencies
├── .gitignore                                             # Excludes raw PhysioNet WFDB binaries & large QC PNG archives
├── src/
│   ├── cves_stroke_hrv_nabian2018_ccs_pipeline.py         # End-to-end S3 sync, 1000 Hz CCS HRV, sanity audit, LMEMs & figures
│   └── build_github_repo.py                               # Automated repo scaffold & file organizer
├── docs/
│   ├── LMEM_Justification_and_Code_Reasoning.md           # Full statistical defense of LMEM, centering & pipeline constraints
│   └── DATA_DICTIONARY.md                                 # Column definitions for all exported CSV tables
├── results/
│   ├── tables/
│   │   ├── Table_S0_Epoch_Sanity_Audit.csv                # Ground-truth HR correlation & RMSSD audit vs. subjects.csv
│   │   ├── Table_S0B_HR_Outliers_gt5bpm.csv               # Subject-level >5 bpm discrepancy log
│   │   ├── Table_S1_Master_Epoch_Features_Nabian2018_1000Hz.csv  # 392-epoch extracted HRV/MSE/PRSA master table
│   │   ├── Table_S2_VIF_Multicollinearity.csv             # Fixed-effect VIF & tolerance diagnostics
│   │   ├── Table_S3_LMEM_Diagnostics_ICC_R2_Shapiro.csv   # Variance components, ICC, Marginal/Conditional R², Shapiro-Wilk
│   │   ├── Table1_Demographics_and_Resting_Subtypes.csv   # Cohort demographics & resting subtype summaries (N = 72)
│   │   ├── Table1B_Resting_Hypothesis_Tests.csv           # Resting H1 ANOVA/Welch & H2 Welch/Mann-Whitney tests
│   │   ├── Table2_Task_State_Descriptives.csv             # 6-task descriptive distributions across States 0–3
│   │   ├── Table3_LMEM_StrictSinus_Orthostatic.csv        # Strict-sinus orthostatic LMEMs (N = 236 epochs, 67 subjects)
│   │   ├── Table4_LMEM_4State_Continuum.csv               # Calibrated 4-state LMEMs (N = 377–386 epochs, 72 subjects)
│   │   └── Table5_Translational_Spearman_Coupling.csv     # Spearman coupling across TCD, MMPF, TMT-B, Gait & NIHSS
│   ├── figures_publication/
│   │   ├── Figure2_Hemispheric_Dissociation_PRSA_DC.{png,pdf}
│   │   └── Figure3_Translational_4Panel_Synthesis.{png,pdf}
│   ├── figures_supplementary/
│   │   ├── FigureS1_4State_Continuum_Trajectories.{png,pdf}
│   │   ├── FigureS2_LMEM_Residual_Diagnostics.{png,pdf}
│   │   └── FigureS3_Forensic_Calibration_Gait.{png,pdf}
│   └── supplementary_tachograms/                          # 392 cleaned RR-interval CSV tachograms (0.73 MB total)
└── logs/
    └── run_log.txt                                        # Timestamped execution & sanity-audit log

```

> **Note on Raw Data & QC Plots:** Raw PhysioNet `.dat`/`.hea` waveforms (`cves-dataset/`) and high-resolution per-epoch QC PNGs (~784 images) are intentionally excluded via `.gitignore` to keep the repository lightweight (< 5 MB). The pipeline streams raw WFDB files directly from PhysioNet's public AWS S3 bucket (`--no-sign-request`).

---

## 3. Quick Start & Reproducibility

### Option A: Local / Linux / macOS / WSL

```bash
git clone [https://github.com/ajtony3000/cves-stroke-autonomic-complexity.git](https://github.com/ajtony3000/cves-stroke-autonomic-complexity.git)
cd cves-stroke-autonomic-complexity
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Open src/cves_stroke_hrv_nabian2018_ccs_pipeline.py and set:
#   "DOWNLOAD_DATA": True, "RUN_EXTRACTION": True
python src/cves_stroke_hrv_nabian2018_ccs_pipeline.py

```

### Option B: Kaggle Notebook / Google Colab

1. Upload `src/cves_stroke_hrv_nabian2018_ccs_pipeline.py` to `/kaggle/working/` (or `/content/` in Colab).
2. Set `"DOWNLOAD_DATA": True` and `"RUN_EXTRACTION": True` in `CONFIG` for a full fresh run (or `False` to re-run statistical tables/figures from an existing `Table_S1` CSV in ~10 seconds).
3. Execute cleanly from a terminal cell to avoid notebook paste-wrapping:
```bash
!python src/cves_stroke_hrv_nabian2018_ccs_pipeline.py

```


4. On Kaggle, use **Save Version → Save & Run All (Commit)** for long runs with `"SAVE_QC_PLOTS": True` so local internet drops cannot interrupt execution.

---

## 4. Data Source & Attribution

* **Dataset:** Cerebral Vasoregulation in Elderly with Stroke (`cves`, v1.0.0), Beth Israel Deaconess Medical Center (BIDMC), Harvard Medical School. Hosted on PhysioNet: [https://physionet.org/content/cves/1.0.0/](https://physionet.org/content/cves/1.0.0/) (Novak et al., *Stroke* 2010; Goldberger et al., *Circulation* 2000).
* **Signal-Processing Backbone:** Adapted in strict compliance with the NIMHANS Centre for Consciousness Studies (CCS) HRV Pipeline ([https://github.com/rahulvenugopal/HRV_Pipeline](https://github.com/rahulvenugopal/HRV_Pipeline)) built on NeuroKit2 (Makowski et al., *Behav Res Methods* 2021).

---

## 5. Citation & License

If you use this pipeline or derived tables, please cite this repository (via [`CITATION.cff`](CITATION.cff)) and the original PhysioNet `cves` publication. This repository is released under the **MIT License** (see [`LICENSE`](https://www.google.com/search?q=LICENSE)).

```

```
