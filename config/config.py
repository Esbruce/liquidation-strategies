from dataclasses import dataclass
import numpy as np

@dataclass
class MarketParams:
    X: float = 100_000 # total shares to liquidate
    S0: float = 50 # Initial Price 
    N: float = 100 # number of intervals for trading
    T: float = 1 # duration to make all trades
    lam: float = 1e-2 # risk aversion coefficient
    gamma: float = 2.5e-7 # short term impact coefficient
    sigma: float = 0.3 # long term impact coefficient ----- need to jsutify these and set appropriate value
    eta: float = 2.5e-6
    # randomness

    noise_type: str = 'guassian'

    # guassian params
    mu: float = 0
    std: float = 2


    @property
    def tau(self): # the duration of each trade
        return self.T / self.N

    def noise(self):

        if self.noise_type == 'guassian':
            return np.random.normal(self.mu, self.std)

    

    










