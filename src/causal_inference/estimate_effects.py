"""
estimate_effects.py — Month 2 deliverable

Estimates ATE / CATE of a dimension (e.g., IR = Infrastructure Readiness)
on the overall ICAID score, adjusting for confounders identified by the
discovered DAG (src/causal_discovery/discover_dag.py).

Two paths, same pattern as discover_dag.py:
  1. `backdoor_ols_minimal()` — manual backdoor adjustment via OLS
     (statsmodels-free, uses sklearn — TESTED in this sandbox).
  2. `run_dowhy_production()` — the actual DoWhy pipeline you should use
     for the paper (identify_effect -> estimate_effect -> refute_estimate).
     Requires `pip install dowhy` on a machine with internet access.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.utils import resample


def backdoor_ols_minimal(df: pd.DataFrame, treatment: str, outcome: str,
                          confounders: list[str], n_bootstrap: int = 500,
                          seed: int = 42) -> dict:
    """ATE via linear backdoor adjustment: regress outcome on
    [treatment] + confounders, coefficient on treatment = ATE under the
    linear-SCM assumption. Bootstrap for a CI (this is the 'p-value /
    confidence interval' the paper is currently missing)."""
    rng = np.random.default_rng(seed)
    X_cols = [treatment] + confounders
    X = df[X_cols].values
    y = df[outcome].values

    model = LinearRegression().fit(X, y)
    ate_point = model.coef_[0]

    boot_ates = []
    n = len(df)
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, n)
        Xb, yb = X[idx], y[idx]
        m = LinearRegression().fit(Xb, yb)
        boot_ates.append(m.coef_[0])
    boot_ates = np.array(boot_ates)
    ci_low, ci_high = np.percentile(boot_ates, [2.5, 97.5])
    # bootstrap p-value for H0: ATE = 0 (two-sided)
    p_value = 2 * min((boot_ates > 0).mean(), (boot_ates < 0).mean())
    p_value = min(p_value, 1.0)

    return {
        "treatment": treatment, "outcome": outcome, "confounders": confounders,
        "ate": float(ate_point), "ci_95": (float(ci_low), float(ci_high)),
        "p_value": float(p_value), "n_bootstrap": n_bootstrap,
        "method": "linear backdoor adjustment (minimal/testable implementation)",
    }


def run_dowhy_production(df: pd.DataFrame, treatment: str, outcome: str,
                          graph_gml: str):
    """Production path: full DoWhy identify -> estimate -> refute pipeline.
    `graph_gml` is a GML-format causal graph string produced from the
    discovered DAG (orient src/causal_discovery output before passing here).
    Requires: pip install dowhy (needs internet; not available in this
    sandbox — run on your own machine)."""
    try:
        from dowhy import CausalModel
    except ImportError as e:
        raise ImportError(
            "dowhy not installed. Run `pip install dowhy` on a machine "
            "with internet access, then re-run this function."
        ) from e
    model = CausalModel(data=df, treatment=treatment, outcome=outcome, graph=graph_gml)
    identified_estimand = model.identify_effect()
    estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
    # Always run at least one refutation before reporting in the paper
    refute = model.refute_estimate(identified_estimand, estimate, method_name="random_common_cause")
    return {"estimand": identified_estimand, "estimate": estimate, "refutation": refute}


if __name__ == "__main__":
    path = "../../data/synthetic/icaid_synthetic_panel.csv"
    df = pd.read_csv(path)
    df["ICAID_score"] = df[["CE", "DF", "CA", "SI", "IR", "IP"]].mean(axis=1)

    result = backdoor_ols_minimal(
        df, treatment="IR", outcome="ICAID_score",
        confounders=["DF"],  # from discovered skeleton; refine once real DAG is oriented
    )
    print("Synthetic smoke test (NOT for the paper) — ATE of IR on ICAID_score:")
    for k, v in result.items():
        print(f"  {k}: {v}")
