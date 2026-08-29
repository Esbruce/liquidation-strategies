import numpy as np
import pandas as pd

class AC():
    def __init__(self, params, impact_fn_g=None, impact_fn_h=None):
        self.p = params
        self.g = impact_fn_g or (lambda v: self.p.gamma * v) # linear permanent impact as per almgrenchriss
        self.h = impact_fn_h or (lambda v: self.p.eta * v) # temporary impact
        initial_lam = (
            self.p.lam[0] if isinstance(self.p.lam, (list, np.ndarray)) else self.p.lam
        )

        self._recompute_kappa(lam_val=initial_lam)

        self.cost = 0

        self.name = 'AC'

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

    def _recompute_kappa(self, lam_val=None):
        # Use the passed lam_val or fall back to current active self.p.lam
        active_lam = lam_val if lam_val is not None else self.p.lam

        # Handle edge case if a list is still passed directly to self.p.lam
        if isinstance(active_lam, (list, np.ndarray)):
            active_lam = active_lam[0]

        self.k2 = active_lam * (self.p.sigma**2) / self.p.eta
        self.kappa = np.arccosh(0.5 * self.k2 * (self.p.tau**2) + 1) / self.p.tau

    def reset(self, seed=None, repeat=None, active_lam=None):
        if seed is not None:
            np.random.seed(seed)

        self.k = 0
        self.X = self.p.X
        self.S = self.p.S0
        self.cost = 0
        self.p.repeat += 1

        self._recompute_kappa(lam_val=active_lam)

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
        self.results['repeat'].append(self.p.repeat)
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

        self.results['X'].append(self.p.X)
        self.results['S0'].append(self.p.S0)
        self.results['N'].append(self.p.N)
        self.results['T'].append(self.p.T)
        self.results['lam'].append(self.p.lam)
        self.results['gamma'].append(self.p.gamma)
        self.results['sigma'].append(self.p.sigma)
        self.results['eta'].append(self.p.eta)
        self.results['mu'].append(self.p.mu)
        self.results['std'].append(self.p.std)
        self.results['noise_type'].append(self.p.noise_type)  

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

        self.S = self.S - self.p.tau * self.g(rate) + self.p.sigma * np.sqrt(self.p.tau) * eps # price change

        exec_price = self.S - self.h(rate)

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











    