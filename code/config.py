from dataclasses import dataclass, field
import numpy as np

@dataclass
class MarketParams():

    rng = np.random.default_rng()

    repeat: int = 0
    X: float = 100_000 # total shares to liquidate
    S0: float = 50 # Initial Price 
    N: float = 50 # number of intervals for trading
    T: float = 1 # duration to make all trades
    lam: float = 1e-6 # risk aversion coefficient
    gamma: float = 2.5e-7 # short term impact coefficient
    xi = 0.0625  #fixed cost coefficeint bid-ask spread cost
    sigma: float = 2 # volatility of the assest price
    eta: float = 2.5e-6 # temporary impact coefficient penalises trading to quickily

    # randomness

    noise_type: str = 'gaussian'

    # guassian params
    mu: float = 0
    std: float = 1

    seed: int = None

    rng: np.random.Generator = field(init=False, repr=False)

    def __post_init__(self):
        self.rng = np.random.default_rng(self.seed)

    @property
    def tau(self): # the duration of each trade
        return self.T / self.N

    def noise(self):

        if self.noise_type == 'gaussian':
            return self.rng.normal(self.mu, self.std)

    






    

    

    










