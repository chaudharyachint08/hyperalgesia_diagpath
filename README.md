# Hyperalgesia — Impact of Drug Treatment

**Unveiling the Multivariate Diagnostic Signature and Mechanistic Pathways of Nicotine Withdrawal-Induced Hyperalgesia**

This repository contains the computational analysis for a preclinical rodent model of passive cigarette smoke and oral nicotine exposure (4- and 12-week studies). The pipeline combines mixed-effects modeling, bootstrap mediation, and machine learning to test whether BDNF–Trk-β signaling mediates mecamylamine-related analgesia and to derive a multivariate diagnostic signature (notably **Nrf-2** and **IL-6**).

- **Notebook author:** Pooja Singhal  
- **Underlying experiments:** Shrimali V, Rathore D, Joshi A, Naha N — *Hyperalgesia and Neuropathic Pain Mechanism in Rodent Models of Cigarette Smoking- and Nicotine-Induced Precipitated Withdrawal Study* (in press, NTR–NIOH / ICMR-NIOH, Ahmedabad).

For full methods and results narrative, see the project technical report (`hyperalgesia_report.pdf`).

---

## Repository layout

| Path | Description |
|------|-------------|
| [`data/proc/`](data/proc/) | Processed CSV tables used by the notebook |
| [`nbs/main.ipynb`](nbs/main.ipynb) | Main EDA, statistical, and ML pipeline (**run this**) |
| [`scripts/`](scripts/) | Optional Excel-to-CSV helper (not required to replicate) |
| [`figures/`](figures/) | Notebook CSV exports; curated copies in `figures/new_figures/` |

---

## Dataset

Replication uses the four processed files in `data/proc/` (no raw Excel required).

**Behavioral data** — `behavior_04week.csv`, `behavior_12week.csv`  
10 treatment groups × 5 biological replicates per study duration (**N = 50** per timepoint).

Columns: `group_id`, `body_wt`, `brain_wt`, `cgrt_cnt`, `nctn_mg`, `dose_mg`, `hypalg_bfr`, `hypalg_aft`

**Genetic / IHC data** — `genetic_04week.csv`, `genetic_12week.csv`  
Immunohistochemistry for groups **{1, 2, 4, 6, 8}** with 10 technical replicates per group.

Columns include study parameters (`group_id`, `cgrt_cnt`, `nctn_mg`, `dose_mg`) and markers: `nAChR`, `BDNF_n`, `Trk-β`, `BDNF_T`, `BDNF_I`, `IL-6`, `iNOS`, `Nrf-2`.

The notebook harmonizes the mismatch between 10 behavioral groups and 5 genetic groups (aggregation and ElasticNet imputation), then stacks 4- and 12-week data for combined analyses (**N ≈ 100**).

---

## Requirements

- **Python 3.13** (developed with kernel `py313`, Python 3.13.12)
- **[uv](https://docs.astral.sh/uv/)** for virtual environments and package installation
- Python packages listed in [`requirements.txt`](requirements.txt): NumPy, Pandas, Matplotlib, Seaborn, scikit-learn, scikit-optimize, statsmodels, tqdm, Plotly, Jupyter, ipykernel

---

## Setup

Clone the repository and create an environment with `uv`:

```bash
git clone <repo-url>
cd hyperalgesia

uv venv --python 3.13
source .venv/bin/activate   # Windows: .venv\Scripts\activate

uv pip install -r requirements.txt
python -m ipykernel install --user --name hyperalgesia --display-name "hyperalgesia"
```

Launch Jupyter from the project root (or open the notebook in VS Code / Cursor with the `hyperalgesia` kernel):

```bash
jupyter lab
# or: jupyter notebook
```

---

## Running the experiments

1. **Paths:** The notebook expects paths relative to `nbs/` (`../data/proc`, `../figures`). Open [`nbs/main.ipynb`](nbs/main.ipynb) from that folder or ensure the kernel’s working directory is `nbs/`.
2. **Kernel:** Select the **hyperalgesia** (Python 3.13) kernel.
3. **Execute:** Run all cells top to bottom (**Run All**).

### Analysis pipeline (in order)

1. Load the four CSV files from `data/proc/`
2. Pre-processing (e.g. control-group handling for `hypalg_aft`)
3. EDA — BDNF column correlations; within-group variability in gene expression
4. **Imputation** — Bayesian-optimized ElasticNet to predict mean gene expression for behavioral groups without direct IHC data
5. Merge behavior with (imputed) genetics; define outcomes such as `hypalg_del` and `hypalg_rel`
6. **Statistical methods** — linear mixed models (LMM), canonical correlation analysis (**BDNF_SUP** latent feature), bootstrap mediation
7. **Machine learning** — PLS-DA (VIP scores), multi-target random forest with RFE and leave-one-group-out CV, hierarchical clustering (Ward), Plotly radar phenotypic fingerprints
8. Optional publication-style figure cells (mediation diagram, conceptual flowchart)

Bayesian hyperparameter search (`BayesSearchCV`, often with `n_jobs=-1`) is the slowest step. The notebook defines `SafeTqdmCallback` so progress bars work under joblib in Jupyter.

---

## Expected outputs

When the export cells run successfully, CSV files are written to **`figures/`** (relative to the repo root):

- `PLS-DA_scores.csv`
- `PLS-DA_vip_df.csv`
- `Phenotypic_Clustered_Data.csv`
- `Phenotypic_Radar_Data.csv`

Reference copies of some tables are also kept under `figures/new_figures/`. Most plots render inline in the notebook (heatmaps, clustermap, PLS-DA, RF importance, Plotly radar). Plotly figures require a Jupyter-compatible renderer.

---

## Reproducibility notes

- Several sections use `random_state=None` or an unseeded mediation bootstrap (**1000** iterations). Numeric results may differ slightly from the technical report between runs.
- Random forest and related BayesSearch steps use `random_state=42` and are more stable.
- Leave-one-group-out **R²** across 4- vs 12-week studies can be strongly negative; this reflects temporal heterogeneity reported in the analysis, not necessarily a broken pipeline.
- The publication mediation path diagram cell uses **fixed** coefficients from the report (e.g. indirect effect **ab = 0.3460**, 95% CI **[0.1504, 0.5986]**).

---

## Citation

If you use this code or processed data, please cite:

1. The computational technical report: *Unveiling the Multivariate Diagnostic Signature and Mechanistic Pathways of Nicotine Withdrawal-Induced Hyperalgesia: A Machine Learning and Mixed-Effects Modeling Approach* (February 2026).
2. The experimental parent manuscript: Shrimali V, Rathore D, Joshi A, Naha N — hyperalgesia and neuropathic pain in rodent models of cigarette smoking– and nicotine-induced precipitated withdrawal (NTR–NIOH, in press).

---

## Optional: rebuilding CSVs from Excel

[`scripts/raw_excel_to_csv.py`](scripts/raw_excel_to_csv.py) is a legacy helper for converting pasted Excel values into genetic CSVs. It is **not** required when using the files already in `data/proc/`.
