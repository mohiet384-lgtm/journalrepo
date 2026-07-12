"""
discover_dag.py — Month 2 deliverable

Two paths:
  1. `pc_algorithm_minimal()` — a hand-rolled, dependency-light PC algorithm
     (partial-correlation based conditional independence tests). Runs with
     only numpy/scipy/networkx, so it is TESTED in this sandbox on the
     Month-1 synthetic panel.
  2. `run_notears_production()` / `run_causal_learn_production()` — thin
     wrappers around the `causal-learn` package's PC/GES and a NOTEARS
     implementation. These are the versions you should actually use for
     the paper (more robust, peer-reviewed implementations) — install
     `causal-learn` (see requirements.txt) on a machine with internet
     access and swap this wrapper in.

Both paths operate on the same input: a wide DataFrame with one column per
ICAID dimension (CE, DF, CA, SI, IR, IP) and one row per (state, year).
"""
from __future__ import annotations
import itertools
import numpy as np
import pandas as pd
import networkx as nx
from scipy import stats


def partial_corr(df: pd.DataFrame, x: str, y: str, controls: list[str]) -> tuple[float, float]:
    """Partial correlation of x,y controlling for `controls`, via residual
    regression. Returns (r, p_value)."""
    if not controls:
        r, p = stats.pearsonr(df[x], df[y])
        return r, p
    from numpy.linalg import lstsq
    Z = np.column_stack([np.ones(len(df))] + [df[c].values for c in controls])
    def resid(v):
        coef, *_ = lstsq(Z, df[v].values, rcond=None)
        return df[v].values - Z @ coef
    rx, ry = resid(x), resid(y)
    r, p = stats.pearsonr(rx, ry)
    return r, p


def pc_algorithm_minimal(df: pd.DataFrame, alpha: float = 0.05, max_cond_size: int = 2) -> nx.Graph:
    """Simplified PC algorithm (skeleton discovery only, no orientation
    rules applied — orientation requires more careful handling of
    v-structures, left to the causal-learn production path). Returns an
    undirected skeleton graph; edges removed when a conditioning set makes
    x _||_ y (p > alpha).

    This is a TEACHING/TESTING implementation, not a substitute for a
    validated library on real submission results — use
    run_causal_learn_production() for the paper's actual reported DAG.
    """
    nodes = list(df.columns)
    g = nx.complete_graph(nodes)
    for cond_size in range(0, max_cond_size + 1):
        for x, y in list(g.edges()):
            neighbors = [n for n in g.neighbors(x) if n != y]
            if len(neighbors) < cond_size:
                continue
            for controls in itertools.combinations(neighbors, cond_size):
                r, p = partial_corr(df, x, y, list(controls))
                if p > alpha:
                    if g.has_edge(x, y):
                        g.remove_edge(x, y)
                    break
    return g


def run_causal_learn_production(df: pd.DataFrame):
    """Production path: PC algorithm via `causal-learn`.
    Requires: pip install causal-learn (needs internet; not available in
    this sandbox — run on your own machine)."""
    try:
        from causallearn.search.ConstraintBased.PC import pc
    except ImportError as e:
        raise ImportError(
            "causal-learn not installed. Run `pip install causal-learn` "
            "on a machine with internet access, then re-run this function."
        ) from e
    cg = pc(df.values, alpha=0.05)
    return cg


def run_notears_production(df: pd.DataFrame):
    """Production path: NOTEARS continuous-optimization structure learning.
    Requires a NOTEARS implementation, e.g.
    `pip install git+https://github.com/xunzheng/notears.git`
    (needs internet; not available in this sandbox)."""
    try:
        from notears import notears_linear
    except ImportError as e:
        raise ImportError(
            "notears package not installed. Install from "
            "https://github.com/xunzheng/notears on a machine with "
            "internet access, then re-run this function."
        ) from e
    W = notears_linear(df.values, lambda1=0.1, loss_type="l2")
    return W


if __name__ == "__main__":
    # Smoke test on Month-1 synthetic panel (NOT real results)
    path = "../../data/synthetic/icaid_synthetic_panel.csv"
    df = pd.read_csv(path)
    dims = ["CE", "DF", "CA", "SI", "IR", "IP"]
    g = pc_algorithm_minimal(df[dims], alpha=0.05, max_cond_size=2)
    print("Skeleton edges (synthetic smoke test, not for the paper):")
    for e in g.edges():
        print(" ", e)
