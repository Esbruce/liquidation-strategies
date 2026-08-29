# Implementation of Almgren-Chriss Optimal Liquidation Strategy.

<img width="750" height="500" alt="image" src="https://github.com/user-attachments/assets/bacf0965-5e74-42de-89eb-6bf961c57f73" />

# Project Overview and Motivation:

In my second year Engineering Mathematics module "Principles of Physical Modelling", I was introduced to Lagrangian mechanics and the Euler-Lagrange equations. This introduced me to **calculus of variations**, where an entire function or trajectory is optimised rather than a finite-dimensional set of variables.

In mechanics, the action is a functional of the trajectory \(q(t)\),

$$S[q]=\int_{t_1}^{t_2}L(q,\dot q,t)\,dt,$$

and requiring

$$\delta S=0$$

leads to the Euler-Lagrange equation

$$\frac{\partial L}{\partial q}-\frac{d}{dt}\left(\frac{\partial L}{\partial\dot q}\right)=0.$$

The Almgren-Chriss model presents a direct application of the same mathematics to optimal trade execution. Instead of optimising a physical trajectory \(q(t)\), the problem is to find the optimal **liquidation trajectory** \(x(t)\), where \(x(t)\) represents the remaining number of shares.

The objective can similarly be expressed as a functional,

$$J[x]=\int_0^T L(x,\dot x,t)\,dt,$$

where \(L\) represents the cost and risk associated with the trading trajectory. Applying the same variational principle,

$$\delta J=0,$$

and the Euler-Lagrange equation gives the differential equation governing the optimal liquidation trajectory.

Thus, the mathematical connection explored in this project is specifically the application of **calculus of variations and the Euler-Lagrange equation to a different optimisation problem**: replacing a physical trajectory with a trading trajectory and the mechanical Lagrangian with an execution cost function.

# Mathematics of the Almgren-Chriss Model:

Mathematically the problem the model solves can be described as follows:

A holding of size $X$ is being sold in $K$ increments such that the quantity of each sale is notated as $n_1, n_k ... n_N$. $x_k$ is the remaining amount of the holding that needs to be sold. This is happening in a time frame of $T$ such that all holdings are sold by $t=T$
What is the best trading trajectory to minimise cost?

## Parameters:

$X$: Total number of shares to sell.

$N$: Total number of discrete trading blocks to sell the shares in.

$T$: Time horizon to sell the holdings. 

$\tau_k$: Duration of the $k_th$ trading block.

$C$: Cost of liquidating entire position.

$n_k$: The number of shares sold in the $k_{th}$ trading block.

$x_k$: The number of shares remaining after the $k_{th}$ trading block.

$S_0$: The value of the initial $X$ shares.

$S_k$: The value of the shares sold in the $k_{th}$ trading block. This is equivalent to $n_k$ times the current price of a share.

$\gamma$: Permanent market impact coefficient. 

$\lambda$: Risk aversion parameter that dictates willingness to be exposed to market volatility.

$\xi$: Fixed cost per share (spread).

$\sigma$: Volatility of the price (per unit time standard deviation)

$\epsilon_k$: Standard Normal Gaussian noise sample for the $k_{th}$ trading block.

## Modelling the Costs of Trading:

There are both long term and short term price impacts of liquidating stock. This provides the unattractive cost of selling a position too quickly.

### Long-term  Price impacts of each sale:
are those which affect the price of the holding after the sale is completed. 
Mathematically these can be written as a change in price of the remaining holding: 

$$S_k = S_{k-1} + \sigma \sqrt{\tau} \epsilon - \tau g(n_k / \tau)$$

Term 1: Previous price

Term 2: Random Walk Term modelling the randomness of the price

Term 3: Negative price term that is a function of the trading velocity and proportional to the duration of the trading block. This models the market reaction of the sale. 

### Short-term Price impacts of each sale:
Short term changes in the price of a asset caused by the presence of the trade in the market. 

Mathematically these can be written as: 

$$\tilde{S_k} = S_{k} - h(n_k / \tau)$$

Term 1: Previous Price

Term 2: A function of the trading rate. This models the cost of executing the trade. If liquidate to fast there is insufficient buyers in the market so the price you can sell for decreases. 

### Total Cost of Selling in each Trading Block:

**Revenue:** The summation of number of shares sold at each price.

$$ \text{Revenue} = \sum_{k=1}^{N} n_k S_k = X S_0 + \sum_{k=1}^{N-1} \left( \sigma \sqrt{\tau} \epsilon_k - \tau g(n_k/\tau) \right) x_k - \sum_{k=1}^{N} n_k h(n_k/\tau)$$

**Cost of Trading:** The difference between the revenue and the price of the holdings at the first trading block.

$$C = \sum_{k=1}^{N} \tau x_k g(n_k/\tau) + \sum_{k=1}^{N} n_k h(n_k/\tau) - \sigma\sqrt{\tau}\sum_{k=1}^{N} x_k \epsilon_k$$

This decomposes cost into permanent-impact drag, temporary-impact drag, and a noise contribution.

### Linear impact assumption:

Almgren-Chriss assume that price impact scales linearly with trading velocity $v = n_k/\tau$:

The impact functions $g(v)$ and $h(v)$ in the above equations are defined, as per the Almgren-Chriss model.

$$g(v) = \gamma v, \qquad h(v) = \xi \mathrm{sgn}(v) + \eta v$$

so permanent impact $g(v)$ is proportional to trading rate, and temporary impact $h(v)$ combines a fixed cost-per-share $\xi$ (spread/slippage) with a rate-proportional component $\eta$. 

## Formulating Objective Function:

Substituting the impact functions and rearranging them cost becomes:

$$C = \frac12\gamma X^2 + \xi\sum_{k=1}^N|n_k| + \frac{\tilde\eta}{\tau}\sum_{k=1}^N n_k^2 - \sigma\sqrt\tau\sum_{k=1}^N x_k\epsilon_k$$

note* $\tilde{\eta}$ was introduce to improve readability $\tilde\eta \equiv \eta - (\gamma\tau) / 2 $

**Taking expectations** under i.i.d. noise ($\mathbb{E}[\epsilon_k]=0$, $\mathrm{Var}[\epsilon_k]=1$), the noise term vanishes in mean and contributes $\sigma^2\tau\sum_k x_k^2$ to the variance:

$$\mathbb{E}[C] = \frac12\gamma X^2 + \xi\sum_{k=1}^N|n_k| + \frac{\tilde\eta}{\tau}\sum_{k=1}^N n_k^2 \qquad \mathbb{V}[C] = \sigma^2\tau\sum_{k=1}^N x_k^2$$

**Objective:**

$$J = \mathbb{E}[C] + \lambda \mathbb{V}[C] = \frac12\gamma X^2 + \xi\sum_{k=1}^N|n_k| + \frac{\tilde\eta}{\tau}\sum_{k=1}^N n_k^2 + \lambda\sigma^2\tau\sum_{k=1}^N x_k^2$$

where $\lambda$ trades off expected cost against the price risk of holding residual inventory $x_k$ over the remaining horizon.

## Optimal Solution to the Objective Function:

Taking the above objective equation the first two terms are constants, assuming that holdings are never bought back. This means they do not effect the outcome of the trade and can be dropped. 

$$\tilde{J}(x_1,\dots,x_{N-1}) = \frac{\tilde\eta}{\tau}\sum_{k=1}^{N}(x_{k-1}-x_k)^2 + \lambda\sigma^2\tau\sum_{k=1}^{N} x_k^2$$

### Convexity of the Objective Function:

The quadratic is convex as it is composed of squared terms with positive coefficients.  A property of this is that all zero gradient points are global minima. 

To find the optimal trajectory is equivalent to finding the point where every partial derivative vanishes.

### Taking the partial derivatives:

Picking a generic representative interior index $j$, with $1 \le j \le N-1$ and take the partial derivative and making it equal to zero.

Differentiating with respect to $x_j$:

$$\frac{\partial \tilde J}{\partial x_j} = \frac{\tilde\eta}{\tau}\Big[-2(x_{j-1}-x_j) + 2(x_j-x_{j+1})\Big] + 2\lambda\sigma^2\tau\, x_j = 0$$

This holds for every $j = 1,\dots,N-1$, giving a system of $N-1$ equations that together pin down the minimizing trajectory.

### Rearrangement into recursion:

Multiply through by $\tau/\tilde\eta$ and collect terms:

$$x_{j+1} - 2x_j + x_{j-1} = \frac{\lambda\sigma^2\tau^2}{\tilde\eta}\, x_j$$

Define $\kappa^2 \equiv (\lambda\sigma^2)/ (\tilde\eta)$, so:

$$x_{j+1} - \big(2+\kappa^2\tau^2\big)x_j + x_{j-1} = 0$$

This is a **linear, constant-coefficient recursion** relating each point on the optimal trajectory to its two neighbours.

### Solve via the Ansatz $x_j = z^j$:

For linear recursions of this type, the standard approach is to guess a solution of the form $x_j = z^j$ and find which values of $z$ are consistent with the equation. Substituting:

$$z^{j+1} - (2+\kappa^2\tau^2)z^j + z^{j-1} = 0$$

Dividing through by $z^{j-1}$ (assuming $z \ne 0$):

$$z^2 - (2+\kappa^2\tau^2)z + 1 = 0$$

This is the **characteristic equation** of the recursion. The two roots of the characteristic equation are $z = e^{\alpha}$ and $z = e^{-\alpha}$.

Because the recursion is linear, the general solution is any combination of the two root-solutions:

$$x_j = A\,e^{\alpha j} + B\,e^{-\alpha j}$$

with constants $A,B$ still undetermined.

### Fix the constants using boundary conditions, obtain the optimal solution

The two boundary conditions we haven't used yet, $x_0 = X$ and $x_N = 0$, give:

$$A + B = X, \qquad Ae^{\alpha N} + Be^{-\alpha N} = 0$$

Solving this $2\times2$ system for $A$ and $B$ and substituting back (using $\sinh(u) = 0.5(e^u-e^{-u})$ to simplify) yields the closed-form optimal trajectory:

$$x_j = X\,\frac{\sinh\big(\alpha(N-j)\big)}{\sinh(\alpha N)}$$

This is the discrete Almgren-Chriss optimal execution trajectory.

# Running the Code:

The two models are written as python classes in the project. The main Almgren-Chriss model and the TWAP model used as a benchmark comparison. Each model is written in its own python file ie almgren_chriss.py, analysis_compare.py.
To run the models to gain results run scripts monte_carlo_compare.py, monte_carlo_ac.py. Afterwards analysis scripts can be run analysis_compare.py.
Functions.py contains helper functions used.

## Efficiency Frontier:

<img width="750" height="500" alt="image" src="https://github.com/user-attachments/assets/048772a5-66a5-4fbe-821b-2b32eccea7dc" />

Here is a graph I produced the shows the classic Almgren-Chriss efficiency frontier. The graph has expected cost of the strategy vs the exposure to volatility. 
This plot is produced by calculating Expected Cost and Variance for different values of $\lambda$ (risk aversion parameter).

The obvious result is that as you take more risk by staying in the market and selling slower the expected cost of the liquidation reduces. However this is under assumptions of neglected external non-symmetric drivers of price that could be occurring in the market. 

# TWAP (Time Weighted Average Pricing) Benchmark Strategy:

TWAP is the simplest liquidation strategy and provides a useful benchmark against which the more complex strategies can be compared. The idea is to sell the position at a constant rate over the entire time horizon.

If $X$ shares are to be sold over $N$ trading blocks, then the number of shares sold in each block is:

$$n_k = \frac{X}{N}$$

and therefore the remaining inventory after each block is:

$$x_k = X\left(1-\frac{k}{N}\right)$$

This means that the liquidation trajectory is a straight line from $X$ to $0$.

The main advantage of TWAP is that it does not require any assumptions about future market conditions. It does not attempt to predict volatility, market impact or trading volume.

However, because it does not adapt to market conditions, it may not be the most efficient strategy when volatility or liquidity changes during the liquidation.

TWAP will therefore be used as the basic benchmark strategy throughout the testing.

# Results:

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/dae74426-5a77-4a46-ab7b-f7c85e91f366" />
<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/b6915024-f807-4c1f-ab3a-b67ca229e989" />
<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/5ef9ca32-18a7-4cac-9098-c7acceb0572b" />
<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/273b0f0d-3e04-49de-97b1-81ac784ccac7" />

Looking at the above histograms. It shows that the Almberg-Chriss model increases its performance lead over TWAP in more illiquid markets. This is expected as it has the ability to decrease the rate of selling as a strategy. 
A further trivial observation to make is that the greatest discrepancy occurs when the market it highly illiquid and not volatile, as the model can decrease the rate of trading without exposing itself to much risk. 
This analysis has only confirmed expected results. A issue with this analysis is defining market conditions on arbitrary values of $\eta$ and $\sigma$. 
