"""
run_pipeline.py — one-command smoke test of the whole ICAID pipeline.

Run from the project root: python run_pipeline.py

Uses data/synthetic/ until data/processed/icaid_real_panel.csv exists
(produced by Month 1 data collection). Every printed result is clearly
labeled synthetic. Swap DATA_PATH below once real data is ready — no
other code changes needed, since every module takes a plain DataFrame.
"""
import os
import subprocess
import sys

STEPS = [
    ("Generate/refresh synthetic test data", "src/data_collection/generate_synthetic_testdata.py"),
    ("Causal discovery (skeleton, PC-minimal)", "src/causal_discovery/discover_dag.py"),
    ("Causal inference (ATE, backdoor adjustment)", "src/causal_inference/estimate_effects.py"),
    ("RL dynamic weighting (policy-gradient stand-in)", "src/rl_weighting/train_weights.py"),
    ("Explainability (permutation importance + figure)", "src/xai/explain.py"),
]

REAL_DATA_PATH = "data/processed/icaid_real_panel.csv"

if __name__ == "__main__":
    if os.path.exists(REAL_DATA_PATH):
        print(f"NOTE: {REAL_DATA_PATH} exists but modules still default to "
              f"synthetic data internally — update each script's `path` "
              f"variable once you're ready to switch over.\n")
    else:
        print("No real dataset yet (data/processed/icaid_real_panel.csv missing). "
              "Running on SYNTHETIC pipeline-test data only.\n")

    for label, script in STEPS:
        print(f"\n{'='*70}\n{label}\n{'='*70}")
        script_dir = os.path.dirname(script)
        script_name = os.path.basename(script)
        result = subprocess.run([sys.executable, script_name], cwd=script_dir)
        if result.returncode != 0:
            print(f"FAILED at step: {label}")
            sys.exit(1)

    print("\nAll steps completed. Figures saved under results/figures/.")
    print("Dashboard: cd src/dashboard && streamlit run app.py (needs streamlit installed).")
