from config import MarketParams
from functions import lambda_monte_carlo_simulation, plot_efficiency_frontier
import numpy as np

if __name__ == "__main__":

    params = MarketParams()
    lam= np.logspace(-9, -4, 50)
    lambda_monte_carlo_simulation(params, lam, 30)
    print('Monte Carlo simulation completed!')
    print('Generating plot!')
    plot_efficiency_frontier('monte-carlo-results.csv')




