"""
rl_env.py — custom gymnasium environment for PPO-based dynamic weighting.

Requires `gymnasium` (pip install gymnasium — needs internet, not
available in this sandbox). This file is not imported by anything unless
train_ppo_production() is called, so its import failing does not break the
rest of the scaffold.

State: current weight vector (6,)
Action: continuous adjustment to each weight (6,), renormalized via softmax
Reward: see train_weights.reward_fn — swap in your justified validation
        target before using this for reported results.
"""
import numpy as np

try:
    import gymnasium as gym
    from gymnasium import spaces
except ImportError:
    gym = None
    spaces = None


def _softmax(x):
    e = np.exp(x - np.max(x))
    return e / e.sum()


if gym is not None:
    class ICAIDWeightEnv(gym.Env):
        def __init__(self, X: np.ndarray, proxy_outcome: np.ndarray, n_dims: int = 6,
                     episode_len: int = 50):
            super().__init__()
            self.X = X
            self.proxy_outcome = proxy_outcome
            self.n_dims = n_dims
            self.episode_len = episode_len
            self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(n_dims,), dtype=np.float32)
            self.observation_space = spaces.Box(low=-5.0, high=5.0, shape=(n_dims,), dtype=np.float32)
            self.theta = None
            self.t = 0

        def reset(self, seed=None, options=None):
            super().reset(seed=seed)
            self.theta = np.zeros(self.n_dims, dtype=np.float32)
            self.t = 0
            return self.theta.copy(), {}

        def step(self, action):
            self.theta = self.theta + 0.1 * np.asarray(action, dtype=np.float32)
            weights = _softmax(self.theta)
            score = self.X @ weights
            score = (score - score.mean()) / (score.std() + 1e-8)
            proxy = (self.proxy_outcome - self.proxy_outcome.mean()) / (self.proxy_outcome.std() + 1e-8)
            reward = float(np.corrcoef(score, proxy)[0, 1])
            self.t += 1
            terminated = self.t >= self.episode_len
            return self.theta.copy(), reward, terminated, False, {"weights": weights}
else:
    ICAIDWeightEnv = None  # gymnasium not installed in this environment
