import numpy as np
import pandas as pd

class ACExecute():
    def __init__(self, params, impact_fn_g=None, impact_fn_h=None):
        self.p = params
        self.g = impact_fn_g or (lambda v: self.p.gamma * v) # linear permanent impact as per almgrenchriss
        self.h = impact_fn_h or (lambda v: self.p.eta * v) # temporary impact
        self.k2 = self.p.lam * self.p.sigma**2 / self.p.eta

        # kappa is a constant of the problem 
        self.kappa = np.arccosh(0.5 * self.k2 * self.p.tau**2 + 1) / self.p.tau

        self.cost = 0

        self.results = {
        'step': [],
        'time': [],
        'holdings': [],
        'price': [],
        'n_k': [],
        'rate': [],
        'step_cost': [],
        'cumulative_cost': [],
        }

    def reset(self, seed=None):
        self.k = 0
        self.X = self.p.X
        self.S = self.p.S0
        self.cost = 0

        self.results = {
        'step': [],
        'time': [],
        'holdings': [],
        'price': [],
        'n_k': [],
        'rate': [],
        'step_cost': [],
        'cumulative_cost': [],
        }

        self._record()  # log the t=0 starting state

        return self._obs(), {}
    
    def _record(self, n_k=np.nan, rate=np.nan, step_cost=np.nan, cumulative_cost=None):
        self.results['step'].append(self.k)
        self.results['time'].append(self.k * self.p.tau)
        self.results['holdings'].append(self.X)
        self.results['price'].append(self.S)
        self.results['n_k'].append(n_k)
        self.results['rate'].append(rate)
        self.results['step_cost'].append(step_cost)
        self.results['cumulative_cost'].append(
            self.cost if cumulative_cost is None else cumulative_cost
        )


    def optimal_holdings(self, step_idx):
        """Optimal remaining holdings x_j at a given step index (0..N)."""
        t = step_idx * self.p.tau
        return (self.p.X * np.sinh(self.kappa * (self.p.T - t)) / np.sinh(self.kappa * self.p.T))

    def optimal_action(self):
        """Shares to sell THIS interval to stay on the optimal trajectory."""
        x_next = self.optimal_holdings(self.k + 1)
        n_k = self.X - x_next
        return n_k
    
    def to_dataframe(self):
        return pd.DataFrame(self.results)

    def step(self):

        n_k = self.optimal_action()
        rate = n_k / self.p.tau

        eps = self.p.noise()

        # price evolves: permanent impact pushes price down as you sell, plus noise
        self.S = self.S - self.p.tau * self.g(rate) + self.p.sigma * np.sqrt(self.p.tau) * eps

        step_cost = self.p.tau * self.X * self.g(rate) + n_k * self.h(rate)
        self.cost += step_cost

        self.X -= n_k
        self.k += 1

        # record state AFTER the update 
        self._record(n_k=n_k, rate=rate, step_cost=step_cost, cumulative_cost=self.cost)

        done = self.k >= self.p.N or self.X <= 1e-6
        if done and self.X > 1e-6:
            self.X = 0.0

        return self._obs(), done, False, {}

    def _obs(self):
        return np.array([self.X, self.S, self.k / self.p.N], dtype=np.float32)











    