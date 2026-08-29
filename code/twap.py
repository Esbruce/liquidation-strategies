import numpy as np
import pandas as pd

class TWAP():
    def __init__(self, params):
        self.p = params

        self.cost = 0

        self.name = 'TWAP'

        # must not change results
        self.results = { 
        'repeat': [],
        'step': [],
        'time': [],
        'holdings': [],
        'price': [],
        'n_k': [],
        'rate': [],
        'step_cost': [],
        'cumulative_cost': [],
        'X': [],
        'S0': [],
        'N': [],
        'T': [],
        'lam': [],
        'gamma': [],
        'sigma': [],
        'eta': [],
        'mu': [],
        'std': [],
        'noise_type':[],
        }


    def reset(self, seed=None, repeat=None):
        if seed is not None:
            np.random.seed(seed)

        self.k = 0
        self.X = self.p.X
        self.S = self.p.S0
        self.cost = 0
        self.p.repeat += 1

        self.results = {
            "repeat": [],
            "step": [],
            "time": [],
            "holdings": [],
            "price": [],
            "n_k": [],
            "rate": [],
            "step_cost": [],
            "cumulative_cost": [],
            "X": [],
            "S0": [],
            "N": [],
            "T": [],
            "lam": [],
            "gamma": [],
            "sigma": [],
            "eta": [],
            "mu": [],
            "std": [],
            "noise_type": [],
        }

        self._record()
        return self._obs(), {}

    
    def _record(self, n_k=np.nan, rate=np.nan, step_cost=np.nan, cumulative_cost=None):
        self.results['repeat'].append(self.p.repeat) # fine
        self.results['step'].append(self.k) # fine
        self.results['time'].append(self.k * self.p.tau) # fine
        self.results['holdings'].append(self.X) # fine
        self.results['price'].append(self.S) # fine
        self.results['n_k'].append(n_k) # fine
        self.results['rate'].append(rate) # fine
        self.results['step_cost'].append(step_cost) # fine
        self.results['cumulative_cost'].append(
            self.cost if cumulative_cost is None else cumulative_cost
        ) # fine

        self.results['X'].append(self.p.X) # fine
        self.results['S0'].append(self.p.S0) # fine
        self.results['N'].append(self.p.N) # fine
        self.results['T'].append(self.p.T) # fine
        self.results['lam'].append(self.p.lam) # fine
        self.results['gamma'].append(self.p.gamma) # fine
        self.results['sigma'].append(self.p.sigma) # fine
        self.results['eta'].append(self.p.eta) # fine
        self.results['mu'].append(self.p.mu) # fine
        self.results['std'].append(self.p.std) # fine
        self.results['noise_type'].append(self.p.noise_type) # fine

    def optimal_holdings(self, step_idx):
        """Optimal remaining holdings for twap"""

        x = self.p.X * (1 - (step_idx + 1) / self.p.N)
        return x

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

        self.S = self.S - self.p.tau * self.p.gamma * rate + self.p.sigma * np.sqrt(self.p.tau) * eps  # permanent impact + noise

        exec_price = self.S - self.p.eta * rate  # temporary impact on execution price

        step_cost = n_k * (self.p.S0 - exec_price)   # realized shortfall vs arrival price

        self.cost += step_cost

        self.X -= n_k # here we update self.X anyways
        self.k += 1

        # record state AFTER the update 
        self._record(n_k=n_k, rate=rate, step_cost=step_cost, cumulative_cost=self.cost)

        done = self.k >= self.p.N or self.X <= 1e-6
        
        if done and self.X > 1e-6:
            self.X = 0.0

        return self._obs(), done, False, {}

    def _obs(self):
        return np.array([self.X, self.S, self.k / self.p.N, self.optimal_action()], dtype=np.float32)











    