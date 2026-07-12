# ICAID: 3-Month Roadmap to Q1-Ready Paper

Status as of this scaffold: **code skeleton complete and tested on
synthetic data**. Nothing here is a reported result yet — every number in
the current codebase is synthetic and every script says so on screen.

## What's done today (this scaffold)
- [x] Project structure (`data/`, `src/`, `results/`, `docs/`)
- [x] Indicator schema: 16 illustrative indicators mapped to real candidate
      sources (`docs/indicator_schema.md`) — needs expansion to 100-150 and
      manual verification of every URL
- [x] Guarded data-collection driver (`src/data_collection/fetch_indicator.py`)
      that refuses to run against unverified sources
      — one real, working example wired up (OpenAlex API)
- [x] Synthetic panel generator for pipeline testing
      (`src/data_collection/generate_synthetic_testdata.py`)
- [x] Causal discovery: hand-rolled PC skeleton (tested) +
      causal-learn/NOTEARS production wrappers (need `pip install`)
- [x] Causal inference: bootstrap backdoor-adjustment ATE with CI/p-value
      (tested) + DoWhy production wrapper (needs `pip install dowhy`)
- [x] RL weighting: ES-style policy-gradient stand-in with reward-curve
      output (tested) + PPO/gymnasium production path (needs
      `pip install stable-baselines3 gymnasium`)
- [x] Explainability: permutation-importance figure (tested, real PNG
      generated) + SHAP production wrapper (needs `pip install shap`)
- [x] Dashboard skeleton (Streamlit + Plotly) that auto-detects real vs.
      synthetic data and warns loudly if only synthetic is present
- [x] `run_pipeline.py` — one command runs every stage end to end
- [x] References addendum with 3 newly verified real citations (not
      fabricated) + a concrete plan for reaching 60+

## Month 1 — Dataset (the hard, unavoidable part)
1. Expand `docs/indicator_schema.md` from 16 to 100-150 indicators.
   For each one: find a real source, open the URL, confirm it has
   state-level, multi-year coverage (or document why it doesn't).
2. Fill in `src/data_collection/sources.yaml` only for verified sources.
3. Write one `fetch_*` function per access type (api / bulk_download /
   manual_pdf / scrape) in `fetch_indicator.py`, modeled on the OpenAlex
   example.
4. Handle missing data explicitly (NSS/Census rounds aren't annual) —
   document every imputation choice; this is a defensible methodology
   section, not just plumbing.
5. Output: `data/processed/icaid_real_panel.csv`, with a data dictionary
   and provenance log (source + access date per cell, ideally).
6. **Reality check:** this is the single biggest time sink. Budget more
   like 6-8 weeks than 4 if this is a side project.

## Month 2 — Analysis pipeline (code already scaffolded above)
1. `pip install -r requirements.txt` on a machine with internet access.
2. Swap `discover_dag.py`'s smoke test for `run_causal_learn_production()`
   on the real panel; orient the DAG (not just skeleton) and compare
   against the paper's hand-specified DAG (Section III) — report where
   they agree/disagree, this is itself a finding.
3. Swap `estimate_effects.py`'s smoke test for `run_dowhy_production()`;
   run at least one refutation test per estimate (placebo treatment,
   random common cause) before trusting any ATE.
4. Decide and justify the RL reward function (this is a research
   decision — see the warning in `train_weights.py`) before running
   `train_ppo_production()`. Save the reward curve for the paper's
   convergence figure.
5. Run `run_shap_production()` for per-state local attributions; these
   feed Section IV's case-study figures.
6. Build the dashboard against `data/processed/icaid_real_panel.csv`.

## Month 3 — Experiments and validation
1. Ablation: drop each of the 6 dimensions one at a time, re-rank states,
   report rank-correlation (Kendall's tau) with the full model.
2. Sensitivity: perturb weights ±10-20%, report rank stability.
3. Comparison: benchmark ICAID rankings against the Global AI Index /
   OECD AI Policy Observatory subset covering India (if state-disaggregated
   data isn't available there, compare at the national level only, and say
   so).
4. Statistical tests: bootstrap CIs (already implemented) for every
   reported ATE; permutation tests for the RL-vs-static-weight comparison.
5. Replace every "illustrative" table/figure in the current manuscript
   with the real, dataset-derived version, keeping the same structure
   Section III already defines.
6. Rewrite tense throughout: "we propose / will validate" → "we validate /
   we found" only for things actually run — leave genuinely unfinished
   pieces as explicit "future work," which is normal and expected, not
   the entire paper's voice.

## Honest bottom line
This scaffold removes the "starting from zero" problem — the causal
discovery, causal inference, RL, and SHAP code all run today, are tested,
and are ready to point at real data the moment it exists. The dataset
(Month 1) is the actual bottleneck and cannot be shortcut by better code;
it needs real time verifying real sources.
