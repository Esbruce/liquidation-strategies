from config.config import MarketParams
from analytical.almgren_chriss import ACExecute
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def run_episode(holdings, seed=None):
    if seed is not None:
        np.random.seed(seed)

    holdings.reset(seed=seed)
    done = False
    while not done:
        _, done, _, _ = holdings.step()

    return holdings.to_dataframe()


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


if __name__ == "__main__":

    params = MarketParams()
    holdings = ACExecute(params)
    df = run_episode(holdings, seed=42)
    save_and_plot(df, out_prefix="almgren_chriss")


