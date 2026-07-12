# ICAID — Reproducibility Scaffold

Working code + data plan for taking the ICAID paper from proposal to
Q1-submission-ready. See `docs/ROADMAP.md` for the full 3-month plan.

## Quick start

**Dashboard only (e.g. Streamlit Community Cloud deploy):**
```bash
pip install -r requirements.txt   # streamlit + pandas + plotly only, fast install
streamlit run src/dashboard/app.py
```

**Full research pipeline (causal discovery, DoWhy, SHAP, RL — run locally):**
```bash
python3.11 -m venv venv && source venv/bin/activate   # 3.10/3.11 recommended;
                                                        # shap's llvmlite dep doesn't
                                                        # yet support the newest Python
pip install -r requirements-full.txt
python run_pipeline.py            # runs every stage on SYNTHETIC test data
python -m pytest tests/ -v        # unit tests (or run tests manually, see below)
```

Why two files: Streamlit Cloud installs whatever is in `requirements.txt`
at the repo root. Pointing it at the full research stack (dowhy, shap,
gymnasium, stable-baselines3) breaks the dashboard deploy over dependency
conflicts it doesn't even need — see `docs/DEPLOYMENT.md` for the story.

## What's real vs. placeholder
| Piece | Status |
|---|---|
| Project structure, orchestrator | Real, done |
| Indicator schema (16 of ~120 rows) | Real sources listed, needs expansion + verification |
| Data fetcher guardrails + 1 working example (OpenAlex) | Real, tested |
| Synthetic data generator | Real, tested — clearly labeled synthetic |
| Causal discovery (PC-minimal) | Real, tested on synthetic data |
| Causal discovery (causal-learn/NOTEARS) | Real code, needs `pip install` + real data |
| Causal inference (backdoor OLS + bootstrap CI) | Real, tested on synthetic data |
| Causal inference (DoWhy) | Real code, needs `pip install` + real data |
| RL weighting (policy-gradient stand-in) | Real, tested — reward curve included |
| RL weighting (PPO) | Real code, needs `pip install` + a justified reward function |
| Explainability (permutation importance) | Real, tested — figure generated |
| Explainability (SHAP) | Real code, needs `pip install` |
| Dashboard | Real code, needs `pip install streamlit plotly` + real data |
| References addendum | 3 newly verified real citations, plan for 60+ |

## Directory layout
```
data/
  raw/          # untouched downloads, once Month 1 starts
  processed/    # icaid_real_panel.csv goes here once ready
  synthetic/    # pipeline-testing data only — never cite in the paper
src/
  data_collection/   # sources.yaml, fetch_indicator.py, synthetic generator
  causal_discovery/  # PC-minimal (tested) + causal-learn/NOTEARS wrappers
  causal_inference/  # backdoor OLS (tested) + DoWhy wrapper
  rl_weighting/      # policy-gradient stand-in (tested) + PPO/gymnasium env
  xai/               # permutation importance (tested) + SHAP wrapper
  dashboard/         # Streamlit app
docs/
  indicator_schema.md       # Month 1 dataset plan
  references_addendum.md    # newly verified citations
  ROADMAP.md                 # full 3-month plan
results/
  figures/       # attribution_smoketest.png already generated
tests/
  test_pipeline.py
```

## The one thing this scaffold cannot shortcut
Real, source-verified data for 36 states × 2020-2025 × ~120 indicators.
That is genuine data-collection and verification work — see
`docs/indicator_schema.md` and Month 1 of `docs/ROADMAP.md`.
