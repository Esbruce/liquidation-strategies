from config.config import MarketParams
from analytical.functions import monte_carlo_simulation, plot_efficiency_frontier
import numpy as np

if __name__ == "__main__":

    params = MarketParams()
    lam= np.logspace(-9, -4, 50)
    monte_carlo_simulation(params, lam, 30)
    print('Monte Carlo simulation completed!')
    print('Generating plot!')
    plot_efficiency_frontier('monte-carlo-results.csv')
    


