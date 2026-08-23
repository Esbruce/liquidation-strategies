import gymnasium as gym
from gymnasium import spaces
import numpy as np


class ExecutionEnv(gym.Env):
    def __init__(self, params, impact_fn_g=None, impact_fn_h=None):
        self.p = params
        self.g = impact_fn_g or (lambda v: self.p.gamma * v)
        self.h = impact_fn_h or (lambda v: self.p.eta * v)
        self.action_space = spaces.Box(low=0, high=1, shape=(1,))
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(3,))

    def reset(self, seed=None):
        self.k = 0
        self.X = self.p.X
        self.S = self.p.S0
        return self._obs(), {}

    def step(self, action):

        # get shares sold 
        n_k = float(action[0]) * self.X

        rate = n_k / self.p.tau

        eps = self.p.noise # create a short noise var

        self.S = self.S = self.p.tau * self.g(rate) + self.p.sigma * np.sqrt(self.p.tau) * eps

        cost = self.p.tau * self.x * self.g(rate) + n_k * self.h(rate)
        reward = -cost  # add variance penalty term if desired

        self.X -= n_k
        self.k += 1

        done = self.k >= self.p.N or self.x <= 1e-6

        if done and self.x > 1e-6:
            # force liquidate remainder, penalize heavily to teach full liquidation
            reward -= self.x * self.h(self.x / self.p.tau)
            self.x = 0

        return self._obs(), reward, done, False, {}

    def _obs(self):
        return np.array([self.x, self.S, self.k / self.p.N], dtype=np.float32)

    



