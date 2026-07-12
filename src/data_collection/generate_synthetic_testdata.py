"""
generate_synthetic_testdata.py

Generates a SYNTHETIC panel dataset (36 states x 2020-2025 x 6 dimension
scores) so that the rest of the pipeline (causal discovery, RL weighting,
SHAP, dashboard) can be built, run, and unit-tested end-to-end BEFORE real
data collection (Month 1, docs/indicator_schema.md) is complete.

THIS IS NOT REAL DATA. Every file this script writes is placed under
data/synthetic/ and stamped with a `synthetic=True` column plus a run
timestamp, specifically so it can never be confused with or silently
substituted for data/processed/ (which is reserved for real,
source-verified data). Do not report numbers from data/synthetic/ in the
paper as findings.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timezone

RNG = np.random.default_rng(42)

STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim",
    "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
    "West Bengal", "Delhi", "Jammu and Kashmir", "Ladakh", "Puducherry",
    "Chandigarh", "Andaman and Nicobar Islands", "Dadra and Nagar Haveli and Daman and Diu",
    "Lakshadweep",
]
YEARS = list(range(2020, 2026))
DIMENSIONS = ["CE", "DF", "CA", "SI", "IR", "IP"]


def generate(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    # give each state a latent "development level" so dimensions correlate
    # sensibly (this is what makes it useful for testing causal-discovery
    # code -- a purely iid random table would recover no structure at all
    # and wouldn't exercise the algorithms properly)
    state_latent = {s: rng.normal(0, 1) for s in STATES}
    for state in STATES:
        base = state_latent[state]
        for year in YEARS:
            trend = (year - 2020) * 0.05  # mild improvement over time
            ir = np.clip(50 + 15 * base + 10 * trend + rng.normal(0, 5), 0, 100)
            ip = np.clip(45 + 12 * base + 8 * trend + 0.3 * ir + rng.normal(0, 5), 0, 100)
            ce = np.clip(40 + 10 * base + 0.2 * ir + rng.normal(0, 6), 0, 100)
            df = np.clip(55 - 5 * base + 6 * trend + rng.normal(0, 7), 0, 100)
            ca = np.clip(50 + 4 * base + 0.15 * ce + rng.normal(0, 6), 0, 100)
            si = np.clip(48 + 8 * base + 0.25 * ir + 0.2 * ip + rng.normal(0, 5), 0, 100)
            rows.append({
                "state": state, "year": year,
                "CE": ce, "DF": df, "CA": ca, "SI": si, "IR": ir, "IP": ip,
            })
    df_out = pd.DataFrame(rows)
    df_out["synthetic"] = True
    df_out["generated_at"] = datetime.now(timezone.utc).isoformat()
    return df_out


if __name__ == "__main__":
    out = generate()
    out_path = "../../data/synthetic/icaid_synthetic_panel.csv"
    out.to_csv(out_path, index=False)
    print(f"Wrote {len(out)} rows (SYNTHETIC, pipeline-testing only) to {out_path}")
