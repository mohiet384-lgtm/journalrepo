# Deployment notes — Streamlit Community Cloud

## What went wrong (and the fix)
The first deploy failed with two independent errors:

1. `shap==0.52.0` depends on `llvmlite==0.36.0`, which does not support the
   Python version Streamlit Cloud was using (3.14) — `llvmlite` only
   supports up to roughly Python 3.11/3.12 as of when this was written.
2. `dowhy>=0.11` doesn't exist on PyPI (latest published version at the
   time was 0.8), so pip/uv couldn't resolve it at all.

Both packages come from the **research pipeline** (causal inference,
explainability), not from the dashboard itself. `src/dashboard/app.py`
only imports `streamlit`, `pandas`, and `plotly.express` — it never
touches `shap` or `dowhy`. Streamlit Cloud installs whatever is in
`requirements.txt` at the repo root, so a requirements file written for
local research work was breaking a deploy that didn't need most of it.

**Fix:** `requirements.txt` now lists only `streamlit`, `pandas`, `plotly`
— what the dashboard actually imports. The full stack (`dowhy`,
`causal-learn`, `shap`, `gymnasium`, `stable-baselines3`, etc.) moved to
`requirements-full.txt`, used only when running the research pipeline
(`run_pipeline.py`) on your own machine.

## Redeploying after this fix
```bash
git pull                       # or copy the two updated files in manually
git add requirements.txt requirements-full.txt README.md docs/DEPLOYMENT.md
git commit -m "Split dashboard vs. research-pipeline requirements to fix Streamlit Cloud deploy"
git push
```
Streamlit Cloud auto-redeploys on every push to the watched branch — no
extra step needed on the Streamlit Cloud side. If it doesn't pick it up
within a minute or two, use the app's "Manage app" menu → "Reboot app".

## If you later want the FULL pipeline running on Streamlit Cloud too
Streamlit Cloud lets you pin a Python version via a `runtime.txt` file at
the repo root (e.g. containing just `python-3.11`). Do this only if you
actually need `shap`/`dowhy` inside the deployed app itself — for now the
dashboard reads pre-computed results (figures, CSVs) rather than running
causal discovery or SHAP live, so it doesn't need them.
