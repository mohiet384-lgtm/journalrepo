"""
Basic tests for the parts of the pipeline that run without dowhy/shap/
stable-baselines3 (not installed in the dev sandbox). Run with:
    cd ICAID_project && python -m pytest tests/ -v
"""
import sys
import os
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "data_collection"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "causal_discovery"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "causal_inference"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "rl_weighting"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "xai"))

from generate_synthetic_testdata import generate, STATES, YEARS  # noqa: E402
from discover_dag import pc_algorithm_minimal, partial_corr  # noqa: E402
from estimate_effects import backdoor_ols_minimal  # noqa: E402
from train_weights import train_policy_gradient_minimal, softmax  # noqa: E402
from explain import permutation_importance_minimal  # noqa: E402


def test_synthetic_shape():
    df = generate()
    assert len(df) == len(STATES) * len(YEARS)
    assert set(["CE", "DF", "CA", "SI", "IR", "IP"]).issubset(df.columns)
    assert df["synthetic"].all()


def test_pc_skeleton_runs():
    df = generate()
    g = pc_algorithm_minimal(df[["CE", "DF", "CA", "SI", "IR", "IP"]], alpha=0.05, max_cond_size=1)
    assert g.number_of_nodes() == 6
    # skeleton should have removed at least one edge from the complete graph (15 possible)
    assert g.number_of_edges() < 15


def test_backdoor_ate_confidence_interval():
    df = generate()
    df["ICAID_score"] = df[["CE", "DF", "CA", "SI", "IR", "IP"]].mean(axis=1)
    result = backdoor_ols_minimal(df, "IR", "ICAID_score", ["DF"], n_bootstrap=50)
    lo, hi = result["ci_95"]
    assert lo <= result["ate"] <= hi
    assert 0.0 <= result["p_value"] <= 1.0


def test_softmax_sums_to_one():
    w = softmax(np.array([1.0, 2.0, 3.0, 0.5, -1.0, 0.0]))
    assert abs(w.sum() - 1.0) < 1e-8
    assert (w >= 0).all()


def test_policy_gradient_produces_valid_weights():
    df = generate()
    dims = ["CE", "DF", "CA", "SI", "IR", "IP"]
    X = df[dims].values
    proxy = df[dims].mean(axis=1).values
    result = train_policy_gradient_minimal(X, proxy, n_dims=6, iters=20)
    w = np.array(result["weights"])
    assert abs(w.sum() - 1.0) < 1e-6
    assert len(result["reward_history"]) == 20


def test_permutation_importance_runs():
    df = generate()
    dims = ["CE", "DF", "CA", "SI", "IR", "IP"]
    df["ICAID_score"] = df[dims].mean(axis=1)
    importances, model = permutation_importance_minimal(df, dims, "ICAID_score")
    assert set(importances["feature"]) == set(dims)
    assert (importances["importance_mean"] >= -1e-6).all()
