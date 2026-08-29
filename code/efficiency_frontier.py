from config import MarketParams
from functions import theoretical_efficiency_frontier
import numpy as np

if __name__ == "__main__":

    params = MarketParams()
    lam= np.logspace(-9, -4, 1000)
    theoretical_efficiency_frontier(params, lam)
    
    


