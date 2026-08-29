from functions import conditions_monte_carlo_simulation
from almgren_chriss import AC
from twap import TWAP

if __name__ == "__main__":

    conditions_monte_carlo_simulation(AC, reps=500)
    conditions_monte_carlo_simulation(TWAP, reps=500)





