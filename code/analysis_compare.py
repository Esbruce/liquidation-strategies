from functions import histograms
import pandas as pd


if __name__ == "__main__":

    d = pd.read_csv('model_comparison_results.csv')

    histograms(d,'Liquid + Low Volatility','AC', 'TWAP')
    histograms(d,'Liquid + High Volatility','AC', 'TWAP')
    histograms(d,'Illiquid + Low Volatility','AC', 'TWAP')
    histograms(d,'Illiquid + High Volatility','AC', 'TWAP')