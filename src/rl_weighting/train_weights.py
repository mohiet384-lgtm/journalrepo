"""
train_weights.py — Month 2 deliverable

Learns dynamic dimension weights w_t (replacing the static Delphi/AHP
weights) via reinforcement learning: the "policy" outputs a weight vector
over the 6 dimensions, the "reward" is how well the resulting weighted
ICAID score predicts a validation outcome (e.g., next-year improvement,
or correlation with an external criterion once one is chosen).

Two paths:
  1. `train_policy_gradient_minimal()` — a small numpy-only REINFORCE loop.
     No stable-baselines3/gymnasium dependency, so it's TESTED here. Good
     enough to validate the reward function and weight-update logic before
     committing to full PPO.
  2. `train_ppo_production()` — the actual PPO setup (Algorithm 3 in the
     paper) via stable-baselines3 in a custom gymnasium Env. Requires
     `pip install gymnasium stable-baselines3` on a machine with internet
     access.

IMPORTANT: the reward function below is a PLACEHOLDER (it rewards weights
that maximize correlation with a synthetic proxy outcome). Before this
produces a result you can put in the paper, you must decide and justify
what the RL is actually optimizing for — e.g. correlation with a
validated external index, predictive power for a downstream policy
outcome, or expert-elicited preference data. That choice is a research
decision, not a coding one, and belongs in Section III-E/VII of the paper.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def softmax(x):
    e = np.exp(x - np.max(x))
    return e / e.sum()


def reward_fn(weights: np.ndarray, X: np.ndarray, proxy_outcome: np.ndarray) -> float:
    """PLACEHOLDER reward: negative squared error between the weighted
    ICAID score and a proxy outcome. Replace `proxy_outcome` with a real,
    justified validation target before reporting results."""
    score = X @ weights
    score = (score - score.mean()) / (score.std() + 1e-8)
    proxy = (proxy_outcome - proxy_outcome.mean()) / (proxy_outcome.std() + 1e-8)
    corr = np.corrcoef(score, proxy)[0, 1]
    return corr  # maximize correlation with the (placeholder) proxy


def train_policy_gradient_minimal(X: np.ndarray, proxy_outcome: np.ndarray,
                                   n_dims: int, iters: int = 300,
                                   lr: float = 0.05, sigma: float = 0.3,
                                   seed: int = 42) -> dict:
    """Evolution-strategies-style policy gradient (a simple, dependency-
    light stand-in for PPO) over a fixed weight vector (theta -> softmax
    -> weights). Returns learned weights + reward curve for a convergence
    plot (Section 4's missing 'reward curve, convergence')."""
    rng = np.random.default_rng(seed)
    theta = rng.normal(0, 0.1, n_dims)
    reward_history = []
    n_pop = 20

    for it in range(iters):
        noises = rng.normal(0, 1, (n_pop, n_dims))
        rewards = np.zeros(n_pop)
        for i in range(n_pop):
            w = softmax(theta + sigma * noises[i])
            rewards[i] = reward_fn(w, X, proxy_outcome)
        # standardize rewards, ES-style update
        A = (rewards - rewards.mean()) / (rewards.std() + 1e-8)
        theta += lr / (n_pop * sigma) * (noises.T @ A)
        reward_history.append(float(rewards.mean()))

    final_weights = softmax(theta)
    return {
        "weights": final_weights.tolist(),
        "reward_history": reward_history,
        "final_reward": reward_history[-1],
        "method": "ES-style policy gradient (minimal/testable stand-in for PPO)",
    }


def train_ppo_production(env_config: dict):
    """Production path: wraps the weight-selection problem as a gymnasium
    Env and trains with PPO (stable-baselines3), matching Algorithm 3 in
    the paper. Requires: pip install gymnasium stable-baselines3 (needs
    internet; not available in this sandbox — run on your own machine).
    See rl_env.py (companion file) for the Env definition to plug in here.
    """
    try:
        from stable_baselines3 import PPO
        from rl_env import ICAIDWeightEnv  # companion file, same folder
    except ImportError as e:
        raise ImportError(
            "gymnasium/stable-baselines3 not installed. Run "
            "`pip install gymnasium stable-baselines3` on a machine with "
            "internet access, then re-run this function."
        ) from e
    env = ICAIDWeightEnv(**env_config)
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=env_config.get("total_timesteps", 20000))
    return model


if __name__ == "__main__":
    path = "../../data/synthetic/icaid_synthetic_panel.csv"
    df = pd.read_csv(path)
    dims = ["CE", "DF", "CA", "SI", "IR", "IP"]
    X = df[dims].values
    # Placeholder proxy outcome: next-year overall improvement (synthetic!)
    df_sorted = df.sort_values(["state", "year"])
    proxy = df_sorted.groupby("state")[dims].mean(axis=1) if False else None
    proxy_outcome = df[dims].mean(axis=1).values + np.random.default_rng(0).normal(0, 5, len(df))

    result = train_policy_gradient_minimal(X, proxy_outcome, n_dims=len(dims), iters=200)
    print("Synthetic smoke test (NOT for the paper) — learned weights:")
    for d, w in zip(dims, result["weights"]):
        print(f"  {d}: {w:.3f}")
    print(f"Final reward (correlation with placeholder proxy): {result['final_reward']:.3f}")
    print(f"Reward history length (for convergence plot): {len(result['reward_history'])}")
