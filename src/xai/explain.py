"""
explain.py — Month 2 deliverable

Per-state, per-dimension attribution for the ICAID score (Section III-I /
Section IV of the paper — currently text-only, no figure).

Two paths:
  1. `permutation_importance_minimal()` — sklearn permutation importance,
     a reasonable stand-in for global attribution. TESTED in this sandbox.
  2. `run_shap_production()` — real SHAP (TreeExplainer/KernelExplainer)
     for per-state, per-dimension local attributions, matching what the
     paper claims ("every ICAID score auditable at the individual
     [state] level"). Requires `pip install shap` on a machine with
     internet access.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib
import shap
import graphviz
import pydot
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance


def permutation_importance_minimal(df: pd.DataFrame, feature_cols: list[str],
                                    target_col: str, seed: int = 42) -> pd.DataFrame:
    """Fits a RandomForest to predict target_col from feature_cols, then
    computes permutation importance as a global attribution stand-in for
    SHAP. Returns a DataFrame ready for a bar-chart figure."""
    X = df[feature_cols].values
    y = df[target_col].values
    model = RandomForestRegressor(n_estimators=200, random_state=seed).fit(X, y)
    result = permutation_importance(model, X, y, n_repeats=30, random_state=seed)
    out = pd.DataFrame({
        "feature": feature_cols,
        "importance_mean": result.importances_mean,
        "importance_std": result.importances_std,
    }).sort_values("importance_mean", ascending=False)
    return out, model


def run_shap_production(model, X: pd.DataFrame):
    """Production path: real SHAP values (per-state local attributions).
    Requires: pip install shap (needs internet; not available in this
    sandbox — run on your own machine)."""
    try:
        import shap
    except ImportError as e:
        raise ImportError(
            "shap not installed. Run `pip install shap` on a machine with "
            "internet access, then re-run this function."
        ) from e
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    return shap_values


if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path = "../../data/synthetic/icaid_synthetic_panel.csv"
    df = pd.read_csv(path)
    dims = ["CE", "DF", "CA", "SI", "IR", "IP"]
    df["ICAID_score"] = df[dims].mean(axis=1)

    importances, model = permutation_importance_minimal(df, dims, "ICAID_score")
    print("Synthetic smoke test (NOT for the paper) — dimension importances:")
    print(importances.to_string(index=False))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(importances["feature"], importances["importance_mean"],
            xerr=importances["importance_std"], color="#2c6e91")
    ax.set_xlabel("Permutation importance (stand-in for mean |SHAP value|)")
    ax.set_title("ICAID dimension attribution — SYNTHETIC smoke test, not for paper")
    plt.tight_layout()
    fig.savefig("../../results/figures/attribution_smoketest.png", dpi=150)
    print("Saved figure to results/figures/attribution_smoketest.png")
