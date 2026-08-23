import numpy as np


class Holdings():
    def __init__(self, params, impact_fn_g=None, impact_fn_h=None):
        self.p = params
        self.g = impact_fn_g or (lambda v: self.p.gamma * v) # linear permanent impact as per almgrenchriss
        self.h = impact_fn_h or (lambda v: self.p.eta * v) # temporary impact

        
        self.k2 = self.p.lam * self.p.sigma**2 / self.p.eta

        # kappa is a constant of the problem 
        self.kappa = np.arccosh(0.5 * self.k2 * self.p.tau**2 + 1) / self.p.tau

        self.cost = 0

    def reset(self, seed=None):
        self.k = 0
        self.X = self.p.X
        self.S = self.p.S0
        self.cost = 0
        return self._obs(), {}

    def optimal_holdings(self, step_idx):
        """Optimal remaining holdings x_j at a given step index (0..N)."""
        t = step_idx * self.p.tau
        return (self.p.X * np.sinh(self.kappa * (self.p.T - t)) / np.sinh(self.kappa * self.p.T))

    def optimal_action(self):
        """Shares to sell THIS interval to stay on the optimal trajectory."""
        x_next = self.optimal_holdings(self.k + 1)
        n_k = self.X - x_next
        return n_k

    def step(self):

        n_k = self.optimal_action()
        rate = n_k / self.p.tau

        eps = self.p.noise

        # price evolves: permanent impact pushes price down as you sell, plus noise
        self.S = self.S - self.p.tau * self.g(rate) + self.p.sigma * np.sqrt(self.p.tau) * eps

        cost = self.p.tau * self.X * self.g(rate) + n_k * self.h(rate)
        self.cost += cost

        self.X -= n_k
        self.k += 1

        done = self.k >= self.p.N or self.X <= 1e-6
        if done and self.X > 1e-6:
            self.X = 0.0

        return self._obs(), done, False, {}

    def _obs(self):
        return np.array([self.X, self.S, self.k / self.p.N], dtype=np.float32)






    