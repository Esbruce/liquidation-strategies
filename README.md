# liquidation-strategies
Exploring how a optimal analytical model and a reinforcement learning model for executing large trades perform and diverge as assumptions of the analytical model are violated.

# Project Overview

Recently I completed a university project on wave energy converter control methods, and came across some interesting hamiltonian based mathematics. I wanted to see what other applications these could have and this project is a result of that. 

The problem investigated is how to best liquidate a large holding, whilst minimising the risk of volatility in the market and minimising transaction costs arising from long and short term market impact.

Mathematically the problem can be described as follows:

A holding of size $X$ is being sold in $K$ increments such that each sale is notated as $n_1, n_k ... n_N$. $X_k$ is the remaining amount of the holding that needs to be sold. 

This is happening in a time frame of $T$ such that all holdings are sold by $t=T$

Long term impacts of the sale are those which affect the price of the holding after the sale is completed. 
Mathematically these can be written as a change in price of the remaining holding: $S_k = S_{k-1} + \sigma \sqrt{\tau} \epsilon - \tau g(n_k / \tau)$
Here: $\tau$ the length of each discrete trading interval, $\sigma$: volatility

Short term impacts of each sale are short term changes in price of a asset caused by the presence of the trade in the market. 

Mathematically these can be written as: $S_k = S_{k-1} + h(n_k / \tau)$

The result of the sell of the asset is:

$\sum_{k=1}^{N} n_k \overline{S_k} = X S_0 + \sum_{k=1}^{N} \left( \sigma \sqrt{\tau} \epsilon_k - \tau g(n_k/\tau) \right) x_k - \sum_{k=1}^{N} n_k h(n_k/\tau)$

The cost of the trade is:

$C = X S_0 - \sum_{k=1}^{N} n_k \overline{S_k}$

In order to best liquidate the large holding we want to minimize and object function: $J = E[C] + \lambda V[C]$ where lambda is a parameter that sets the risk aversion of the mathematics. 


# Analytical Optimal Derivation

## Almgren–Chriss: General Cost and Variance

For a trading trajectory $x_k$ (shares remaining after period $k$) with trade sizes
$n_k = x_{k-1}-x_k$, the general (model-free) expected cost and variance of execution are:

$$
E[C] = \sum_{k=1}^N \left[\tau x_k\, g\!\left(\frac{n_k}{\tau}\right) + n_k\, h\!\left(\frac{n_k}{\tau}\right)\right]
$$

$$
V[C] = \sigma^2 \sum_{k=1}^N \tau x_k^2
$$

where:

- $g(\cdot)$ is the **permanent impact** function - trading at rate $n_k/\tau$ permanently shifts the price, and this shift acts on *all remaining shares* $x_k$, hence the $\tau x_k\, g(n_k/\tau)$ term.
- $h(\cdot)$ is the **temporary impact** function - it only affects the shares traded *this period*, $n_k$, and reverts afterward.
- $\lambda$ is the **risk-aversion parameter**, weighting how much variance you're willing to trade off against expected cost.

# Almgren–Chriss Hypothesis: Linear Impact

Almgren and Chriss assume both impact functions are **linear** in trading rate:

$$
g\!\left(\frac{n_k}{\tau}\right) = \gamma \frac{n_k}{\tau}, \qquad
h\!\left(\frac{n_k}{\tau}\right) = \xi\,\mathrm{sgn}(n_k) + \eta \frac{n_k}{\tau}
$$

## Reinforcement Learning Strategy

## Test Environment

## Results

## Analysis




