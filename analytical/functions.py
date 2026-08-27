import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from analytical.almgren_chriss import ACExecute
from config.config import MarketParams
import os
from datetime import datetime


now = datetime.now()

def save_to_csv(df, out_prefix='now'):

    # create the csv path

    file_path = f'{out_prefix}.csv'

    file_exist = os.path.isfile(file_path)

    # extract dataframe and write to csv

    df.to_csv(file_path, mode='a', index=True, header=not file_exist) # mode a for append only header on intial creattion

def save_to_csv(df, out_prefix='now'):

    file_path = f'{out_prefix}.csv'
    file_exists = os.path.isfile(file_path)

    df.to_csv(
        file_path,
        mode='a',
        index=True,
        header=not file_exists   # write header only on first write
    )


def run_model(model, seed=None):
    if seed is not None:
        np.random.seed(seed)

    model.reset(seed=seed)
    done = False
    while not done:
        _, done, _, _ = model.step()

    return model.to_dataframe()

def calc_expected_cost(p):

    term_1 = 0.5 * p.lam * p.X **2 

    term_2 = p.xi * abs(p.X)

    term_3 = (p.eta / p.tau) * (p.X **2 / p.N)

    return term_1 + term_2 + term_3 


def monte_carlo_simulation(params,lambdas, reps):

    p = params

    for lam in lambdas:
        model = ACExecute(p)
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
















            





    



    





def save_and_plot(df, out_prefix='almgren_chriss'):

    # create csv path
    csv_path = f"{out_prefix}_results.csv"

    df.to_csv(csv_path, index=True)

    print('saved results to csv')

    # plot 

    # --- plots ---
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Holdings trajectory
    axes[0, 0].plot(df['time'], df['holdings'], marker='o', markersize=3)
    axes[0, 0].set_xlabel('Time')
    axes[0, 0].set_ylabel('Remaining holdings')
    axes[0, 0].set_title('Optimal Liquidation Trajectory')
    axes[0, 0].grid(alpha=0.3)

    # Price path
    axes[0, 1].plot(df['time'], df['price'], color='tab:orange')
    axes[0, 1].set_xlabel('Time')
    axes[0, 1].set_ylabel('Price')
    axes[0, 1].set_title('Price Evolution')
    axes[0, 1].grid(alpha=0.3)

    # Trade size per interval
    axes[1, 0].bar(df['step'].iloc[1:], df['n_k'].dropna(), width=0.8, color='tab:green')
    axes[1, 0].set_xlabel('Step')
    axes[1, 0].set_ylabel('Shares sold')
    axes[1, 0].set_title('Trade Size per Interval')
    axes[1, 0].grid(alpha=0.3)

    # Cumulative cost
    axes[1, 1].plot(df['time'].iloc[1:], df['cumulative_cost'].iloc[1:], color='tab:red')
    axes[1, 1].set_xlabel('Time')
    axes[1, 1].set_ylabel('Cumulative cost')
    axes[1, 1].set_title('Cumulative Execution Cost')
    axes[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig_path = f"{out_prefix}_plots.png"
    fig.savefig(fig_path, dpi=150)
    print(f"Saved plots to {fig_path}")
    plt.show()






