import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from almgren_chriss import AC
from config import MarketParams
import os
from datetime import datetime


now = datetime.now()

def save_to_csv(df, out_prefix='now'):

    # create the csv path

    file_path = f'{out_prefix}.csv'

    file_exist = os.path.isfile(file_path)

    # extract dataframe and write to csv

    df.to_csv(file_path, mode='a', index=True, header=not file_exist) # mode a for append only header on intial creattion


def run_model(model, seed=None):
    if seed is not None:
        np.random.seed(seed)

    model.reset(seed=seed)
    done = False
    while not done:
        _ , done, _, _ = model.step()

    return model.to_dataframe()

def get_optimal_trajectory(model):
    model.reset()
    done = False
    holdings = []
    while not done:
        obs, done, _, _ = model.step()
        holdings.append(obs[0])   # remaining holdings, not next-step trade size
    return holdings

def calc_expected_cost(p):

    term_1 = 0.5 * p.lam * p.X **2 

    term_2 = p.xi * abs(p.X)

    term_3 = (p.eta / p.tau) * (p.X **2 / p.N)

    return term_1 + term_2 + term_3 

def calc_variance(p):

    model = AC(p)
    holdings = np.array(get_optimal_trajectory(model))
    holdings = (holdings)**2
    sum = np.sum(holdings)
    return p.sigma ** 2 * p.tau * sum


def theoretical_efficiency_frontier(params, lambdas):

    p = params

    # create lists for expected cost and theoretical variance

    ECList, VARList = [], []

    for lam in lambdas:
        p.lam = lam
        EC = calc_expected_cost(p)
        VAR = calc_variance(p)
        ECList.append(EC)
        VARList.append(VAR) 

    

    plt.plot(VARList, ECList, color="#205fe6", linewidth=2.2, marker='')

    plt.xlabel('Variance (Exposure to risk)')
    plt.ylabel('Expected Cost of Strategy')
    plt.title('Almgren-Chriss Efficiency Frontier', fontsize=14)

    plt.grid(True, linestyle='--', alpha=0.4, zorder=0)
    plt.show()


def lambda_monte_carlo_simulation(params,lambdas, reps):

    p = params

    for lam in lambdas:
        model = AC(p)
        p.lam = lam
        EC = calc_expected_cost(p) # calculate the expected cost

        for i in range(reps):

            results = run_model(model)
            results['EC'] = EC # append results with Expected Cost

            save_to_csv(results, 'monte-carlo-results')


def plot_efficiency_frontier(data):

    results = pd.read_csv(data)

    # get all unique expected cost values

    EC_list = results['EC'].tolist()

    print(f'{len(EC_list)} expected costs to evaluate variance of')

    # for each_EC calculat the risk uncertainty

    VAR_list = []

    for EC in EC_list:

        # get the cost results

        results['cumulative_cost'] = pd.to_numeric(results['cumulative_cost'], errors='coerce')

        costs = results.loc[results['EC'] == EC, 'cumulative_cost']

        variance = costs.std() **2

        VAR_list.append(variance)

    # plot the data

    print('Plotting')

    plt.plot(VAR_list, EC_list, linestyle='', marker='o', markersize=3)
    plt.xlabel('Variance')
    plt.ylabel('Expected Cost')
    plt.title('Empirical Efficiency Frontier of Almberg-Chriss Liquadation ')
    plt.show()
    # plt.savefig('Almberg-Chriss Efficiency Frontier')


def get_market_params(condition: str) -> MarketParams:
    match condition:
        case 'Liquid + Low Volatility':
            return MarketParams(sigma=0.02, eta=2.5e-6, gamma=2.5e-7, lam=1e-6)
        case 'Liquid + High Volatility':
            return MarketParams(sigma=0.06, eta=2.5e-6, gamma=2.5e-7, lam=1e-6)
        case 'Illiquid + Low Volatility':
            return MarketParams(sigma=0.02, eta=1.0e-5, gamma=2.5e-7, lam=1e-6)
        case 'Illiquid + High Volatility':
            return MarketParams(sigma=0.06, eta=1.0e-5, gamma=2.5e-7, lam=1e-6)
        case _:
            raise ValueError(f"Unknown condition: {condition}")


############################################### functions for cross model comparison ######################################################


def conditions_monte_carlo_simulation(model, reps):

    conditions = ['Liquid + Low Volatility', 'Liquid + High Volatility', 'Illiquid + Low Volatility', 'Illiquid + High Volatility']

    for condition in conditions:

        params = get_market_params(condition)

        m = model(params)

        for rep in range(reps):

            results = run_model(m)
            results['model'] = m.name
            results['condition'] = condition

            save_to_csv(results, 'model_comparison_results')


# def histograms(data, condition, model_type1, model_type2):

#     # select the relevant data
#     subset = data[data['condition'] == condition]

#     def get_total_costs(model_type):
#         model_data = subset[subset['model'] == model_type]
#         # total cost = final cumulative_cost value for each repeat
#         totals = model_data.groupby('repeat')['cumulative_cost'].last()
#         return totals.values

#     costs1 = get_total_costs(model_type1)
#     costs2 = get_total_costs(model_type2)

#     fig, ax = plt.subplots(figsize=(7, 5))

#     bins = 30
#     ax.hist(costs1, bins=bins, alpha=0.5, label=model_type1, density=True)
#     ax.hist(costs2, bins=bins, alpha=0.5, label=model_type2, density=True)
#     ax.set_xlabel('Total cost')
#     ax.set_ylabel('Density')
#     ax.set_title(f'Total cost histogram\n({condition})')
#     ax.legend()

#     plt.tight_layout()
#     plt.show()

#     return fig, ax


def histograms(data, condition, model_type1, model_type2):

    savepath = f'{condition}-histogram'

    # select the relevant data
    subset = data[data['condition'] == condition]

    # normalise by initial portfolio value (S0 * X) -> percentage
    first_row = subset.iloc[0]
    portfolio_value = first_row['S0'] * first_row['X']
    sigma = first_row['sigma']
    eta = first_row['eta']

    def get_total_costs(model_type):
        model_data = subset[subset['model'] == model_type]
        # total cost = final cumulative_cost value for each repeat
        totals = model_data.groupby('repeat')['cumulative_cost'].last()
        return (totals.values / portfolio_value) * 100  # as % of initial portfolio

    costs1 = get_total_costs(model_type1)
    costs2 = get_total_costs(model_type2)

    mean1, std1 = np.mean(costs1), np.std(costs1)
    mean2, std2 = np.mean(costs2), np.std(costs2)

    fig, ax = plt.subplots(figsize=(8, 5))

    bins = 50
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    ax.hist(costs1, bins=bins, alpha=0.5, color=colors[0],
            label=f'{model_type1} (μ={mean1:.3f}%, σ={std1:.3f}%)', density=True)
    ax.hist(costs2, bins=bins, alpha=0.5, color=colors[1],
            label=f'{model_type2} (μ={mean2:.3f}%, σ={std2:.3f}%)', density=True)

    # vertical lines marking the means
    ax.axvline(mean1, color=colors[0], linestyle='--', linewidth=1.5)
    ax.axvline(mean2, color=colors[1], linestyle='--', linewidth=1.5)

    ax.set_xlabel('Total cost (% of initial portfolio value S₀ × X)')
    ax.set_ylabel('Density')
    ax.set_title(f'Condition: {condition}\nσ={sigma}, η={eta}')
    ax.legend()

    plt.tight_layout()
    plt.savefig(savepath)


            





    
















            





    



    





# def save_and_plot(df, out_prefix='almgren_chriss'):

#     # create csv path
#     csv_path = f"{out_prefix}_results.csv"

#     df.to_csv(csv_path, index=True)

#     print('saved results to csv')

#     # plot 

#     # --- plots ---
#     fig, axes = plt.subplots(2, 2, figsize=(12, 8))

#     # Holdings trajectory
#     axes[0, 0].plot(df['time'], df['holdings'], marker='o', markersize=3)
#     axes[0, 0].set_xlabel('Time')
#     axes[0, 0].set_ylabel('Remaining holdings')
#     axes[0, 0].set_title('Optimal Liquidation Trajectory')
#     axes[0, 0].grid(alpha=0.3)

#     # Price path
#     axes[0, 1].plot(df['time'], df['price'], color='tab:orange')
#     axes[0, 1].set_xlabel('Time')
#     axes[0, 1].set_ylabel('Price')
#     axes[0, 1].set_title('Price Evolution')
#     axes[0, 1].grid(alpha=0.3)

#     # Trade size per interval
#     axes[1, 0].bar(df['step'].iloc[1:], df['n_k'].dropna(), width=0.8, color='tab:green')
#     axes[1, 0].set_xlabel('Step')
#     axes[1, 0].set_ylabel('Shares sold')
#     axes[1, 0].set_title('Trade Size per Interval')
#     axes[1, 0].grid(alpha=0.3)

#     # Cumulative cost
#     axes[1, 1].plot(df['time'].iloc[1:], df['cumulative_cost'].iloc[1:], color='tab:red')
#     axes[1, 1].set_xlabel('Time')
#     axes[1, 1].set_ylabel('Cumulative cost')
#     axes[1, 1].set_title('Cumulative Execution Cost')
#     axes[1, 1].grid(alpha=0.3)

#     fig.tight_layout()
#     fig_path = f"{out_prefix}_plots.png"
#     fig.savefig(fig_path, dpi=150)
#     print(f"Saved plots to {fig_path}")
#     plt.show()






