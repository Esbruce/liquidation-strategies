# Comparing Liquidation Strategies in 4 different Market Conditions.
Implementing and evaluating variations Almgren-Chriss model alongside common liquidation benchmark strategies in various market conditions.

<img width="750" height="500" alt="image" src="https://github.com/user-attachments/assets/bacf0965-5e74-42de-89eb-6bf961c57f73" />


# Project Motivation and Overview

In my second year Engineering Mathematics module "Principles of Physical Modelling", we had a introduction to Lagrangian mechanics. In this module we learnt how to derive second order equations of motions using the Euler-Lagrange Equations. Initially the results seemed surprising and impressive and I wanted to delve deeper into why the maths works and where else is was applicable - leading me to following problem. 

In mechanics the Lagrangian represents the difference in kinetic and potential energy of a body/particle $L = T - U$ where $T$ is the kinetic energy and $U$ is the potential energy.

The Lagrangian therefore is related to the the coordinates and motion of the body. $L = L(q(t),\dot{q}(t),t)$

Interesting the way this relates to the equation of motion of for example a ball in the air is by the action functional (function that takes a function (ie a path through space $q(t)$ ) and returns a value).

The actional functional $S= \int_{t_1}^{t2} L dt$ and the stationarity of this gives the equation of motion. 

This project explores the Almgren-Chriss strategy and variations for liquidating large holdings.  The problem is how to best liquidate a large holding, whilst minimising the risk of volatility in the market and minimising transaction costs arising from long and short term market impact.

Mathematically the problem can be described as follows:

The optimisation problem is given you have $X$ shares to liquidate over $N$ trading blocks, how many shares $n_k$ should be sold in each trading block, in order to minimise the expected cost of the sale. 

The maths that draws parallel between the Almgren-Chriss and Lagrangian Mechanics is the use of calculus of variation used to find the stationarity of a action functional. 

In the case of Almgren-Chriss the action functional takes the trajectory of holdings kept at each trading block in a liquidation and returns the cost of the sale. The aim is to minimise this. 

# Original Almgren-Chriss Model:

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

This is the discrete Almgren-Chriss optimal execution trajectory

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

# VWAP (Volume Weighted Average Pricing) Benchmark Strategy:

VWAP is similar to TWAP but instead of selling an equal number of shares in each trading block, the strategy attempts to trade in proportion to the expected market volume.

If $V_k$ is the expected market volume in trading block $k$, then the proportion of the total market volume occurring in that block is:

$$w_k = \frac{V_k}{\sum_{i=1}^{N}V_i}$$

The number of shares sold by the strategy is then:

$$n_k = Xw_k$$

and the remaining inventory is:

$$x_k = X-\sum_{i=1}^{k}n_i$$

The idea behind VWAP is that trading more when market volume is high should reduce the market impact of the trade, as there are more buyers and sellers available.

Unlike TWAP, VWAP therefore uses information about the expected shape of the market volume throughout the trading period.

However, it still does not directly account for the risk of holding the remaining inventory while the market moves.

# Comparing the Strategies:

The strategies being tested are therefore:

| Strategy | Main idea | Adapts to volatility | Adapts to liquidity | Risk aware |
| ---- | ---- | ---- | ---- | ---- |
| TWAP | Sell at a constant rate | No | No | No |
| VWAP | Sell in proportion to expected volume | No | Yes | No |
| AC | Optimise cost against risk | Through $\lambda$ | Through impact parameters | Yes |
| Adaptive AC | Recalculate AC as conditions change | Yes | Yes | Yes |

The purpose of including these different strategies is not simply to determine which strategy has the lowest average cost. Each strategy makes different assumptions about the market, so the more interesting question is how their relative performance changes when these assumptions are no longer true.

# Testing the Model under Different Market Conditions:

The original Almgren-Chriss model assumes constant parameters throughout the liquidation. In particular, volatility $\sigma$ and the market impact parameters are assumed to remain constant.

This is unlikely to be completely representative of a real market. To investigate how important these assumptions are, the strategies will be tested under four different market conditions.

## 1. Normal Market Conditions:

The baseline case where all model parameters remain constant throughout the liquidation.

$$\sigma_t = \sigma_0$$

$$\eta_t = \eta_0$$

The purpose of this test is to establish how the strategies perform when the assumptions of the original AC model are approximately satisfied.

This provides a control case for the other experiments.

## 2. High Volatility:

In this scenario the volatility of the market increases during the liquidation.

For example, at some point during the liquidation:

$$\sigma_t =
\begin{cases}
\sigma_0 & t < T/2 \\
2\sigma_0 & t \geq T/2
\end{cases}
$$

This represents a sudden increase in the uncertainty of the market price.

The original AC strategy will still follow the trajectory calculated using the initial value of $\sigma$.

The Adaptive AC strategy will instead observe the increase in volatility and recalculate its optimal liquidation trajectory.

This allows the question to be tested:

**Does adapting to changing volatility improve liquidation performance?**

## 3. Low Liquidity:

In this scenario the market becomes less liquid during the liquidation.

This can be represented by increasing the temporary market impact coefficient:

$$\eta_t =
\begin{cases}
\eta_0 & t < T/2 \\
2\eta_0 & t \geq T/2
\end{cases}
$$

A higher $\eta$ means that executing a large quantity in a short period produces a greater price impact.

This scenario tests how the strategies respond when it becomes more expensive to trade quickly.

VWAP should potentially benefit from trading more heavily during periods of high expected volume, while AC should account for the increased cost of rapid execution through its market impact parameters.

## 4. Volatility and Liquidity Shock:

The final scenario combines the two previous cases.

At $T/2$, both volatility and market impact increase:

$$\sigma_t =
\begin{cases}
\sigma_0 & t < T/2 \\
2\sigma_0 & t \geq T/2
\end{cases}
$$

$$\eta_t =
\begin{cases}
\eta_0 & t < T/2 \\
2\eta_0 & t \geq T/2
\end{cases}
$$

This creates a more difficult market condition where both the cost of trading quickly and the risk of holding the remaining position increase.

This should provide the strongest test of whether an adaptive strategy provides an advantage over a strategy calculated once at the beginning of the liquidation.

# Adaptive Almgren-Chriss Strategy:

The original AC strategy calculates the optimal trajectory using the market parameters at the beginning of the liquidation.

The Adaptive AC strategy instead recalculates the optimal trajectory as new information about the market becomes available.

For example, the strategy can operate in the following way:

1. Estimate the current market parameters.
2. Calculate the optimal AC trajectory.
3. Execute the next group of trading blocks.
4. Observe the new market conditions.
5. Update the model parameters.
6. Recalculate the optimal trajectory using the remaining inventory and remaining time.
7. Continue until the position is fully liquidated.

This is essentially a repeated application of the original AC optimisation rather than creating an entirely new optimisation problem.

The important difference is therefore:

$$
\text{Original AC:}
\qquad
\text{Parameters estimated once}
$$

$$
\text{Adaptive AC:}
\qquad
\text{Parameters updated throughout liquidation}
$$

The Adaptive AC strategy can therefore respond to changes in volatility and liquidity that were not known when the initial trajectory was calculated.

# Testing Method:

To compare the strategies fairly, each strategy will be tested using the same simulated market conditions.

For each market condition, a large number of price paths will be generated using the same underlying stochastic process.

For each simulation the strategies will start with the same:

$$X,\quad T,\quad S_0$$

and will be subject to the same realised price movements.

This means that differences in performance should be caused by the liquidation strategy rather than different random price paths.

For each strategy and market condition, the simulation will be repeated many times using different samples of the random price process.

The resulting implementation shortfall will then be compared between strategies.

The main quantities measured will be:

### Mean Implementation Shortfall:

$$\mathbb{E}[C]$$

This measures the average cost of liquidating the position.

A lower value indicates that the strategy is cheaper on average.

### Standard Deviation of Implementation Shortfall:

$$\sqrt{\mathbb{V}[C]}$$

This measures the variability of the liquidation cost.

A lower value means that the execution result is more predictable.

### Value at Risk:

The $95\%$ Value at Risk measures a high-cost outcome of the liquidation.

This can be estimated from the simulated distribution of costs.

### Conditional Value at Risk:

The $95\%$ Conditional Value at Risk measures the average cost of the worst $5\%$ of simulated outcomes.

This is useful for comparing how the strategies behave during particularly poor executions.

### Probability of Beating TWAP:

For each strategy the proportion of simulations where it achieves a lower implementation shortfall than TWAP can be calculated:

$$
P(C_{\text{strategy}} < C_{\text{TWAP}})
$$

This gives a measure of how consistently the strategy outperforms the simple benchmark rather than only comparing average performance.

# Results:

The results will be presented separately for each of the four market conditions.

The main comparison will be between:

$$
\boxed{\text{TWAP},\quad \text{VWAP},\quad \text{AC},\quad \text{Adaptive AC}}
$$

For each strategy the following will be compared:

| Strategy | Mean Cost | Standard Deviation | $VaR_{95}$ | $CVaR_{95}$ | Probability of beating TWAP |
| ---- | ---- | ---- | ---- | ---- | ---- |
| TWAP | - | - | - | - | - |
| VWAP | - | - | - | - | - |
| AC | - | - | - | - | - |
| Adaptive AC | - | - | - | - | - |

The same table can then be produced for each of the four market conditions.

# Analysis:

The first comparison is between the strategies under normal market conditions.

Under the assumptions of the original AC model, AC should provide a good balance between expected transaction cost and exposure to price volatility. TWAP provides a useful baseline because it makes no attempt to optimise this trade-off.

The VWAP strategy should perform differently depending on the shape of the expected market volume. Its main advantage is that it attempts to execute when there is greater liquidity.

The more interesting comparison is between the original AC and Adaptive AC strategies.

Under stable market conditions there may be little difference between the two strategies, as the parameters used to calculate the initial AC trajectory remain approximately correct.

However, when the market conditions change during the liquidation, the original AC strategy continues following a trajectory calculated using outdated parameters.

The Adaptive AC strategy can instead respond to the new conditions.

For example, if volatility increases, the risk associated with holding the remaining inventory increases. This should encourage the Adaptive AC strategy to liquidate more quickly.

Similarly, if market impact increases, executing too quickly becomes more expensive. This creates a competing incentive to slow the liquidation.

The combined volatility and liquidity shock is therefore particularly interesting because the two effects push the optimal strategy in different directions.

# Model Misspecification:

A further test is to deliberately use incorrect parameters when calculating the original AC trajectory.

The true market may have parameters:

$$
\sigma,\quad \eta
$$

but the strategy may estimate:

$$
\hat{\sigma},\quad \hat{\eta}.
$$

The effect of this can be tested by varying the ratio between estimated and true parameters.

For example:

$$
\frac{\hat{\sigma}}{\sigma}
\in
\{0.5,1,2\}
$$

and

$$
\frac{\hat{\eta}}{\eta}
\in
\{0.5,1,2\}.
$$

This tests how sensitive the performance of AC is to errors in its assumptions.

A heatmap can then be produced showing the relative performance of AC compared to TWAP for different levels of parameter error.

This is useful because the theoretical AC solution is optimal when the model parameters are correct, but in a real market these parameters must be estimated and will therefore contain some degree of error.

The main question is therefore:

**How much does the performance of AC deteriorate when the parameters used to calculate the optimal trajectory are wrong?**

# Discussion:

The main aim of this project is not simply to find which strategy produces the lowest average cost.

Instead, it is to investigate how the assumptions made by each strategy affect its performance.

TWAP makes very few assumptions and therefore provides a simple and robust benchmark, but it does not take advantage of information about market liquidity or volatility.

VWAP uses expected market volume to determine when to trade, potentially reducing market impact, but it does not explicitly consider the risk of holding the remaining inventory.

AC explicitly balances transaction costs against price risk and therefore provides a more theoretically informed strategy. However, its performance depends on the parameters used in the model remaining reasonably representative of the market.

Adaptive AC attempts to address this limitation by updating the model as market conditions change.

The results from the four market conditions should therefore show whether the additional complexity of Adaptive AC provides a meaningful improvement over the original AC strategy.

A particularly important result would be a situation where AC performs well under the conditions for which it was designed but performs worse when its assumptions are violated. This would demonstrate the importance of model robustness rather than simply showing that a more complicated strategy is always better.

# Conclusion:

The Almgren-Chriss model provides a mathematically elegant solution to the problem of liquidating a large position while balancing market impact against price risk.

The efficient frontier demonstrates this trade-off clearly, showing that accepting greater exposure to volatility can reduce expected transaction costs.

However, the model relies on assumptions about the market which may not remain true throughout a liquidation.

By comparing TWAP, VWAP, AC and Adaptive AC under different volatility and liquidity conditions, the aim is to investigate how robust these strategies are when the market changes.

The key research question is therefore:

> **How robust is the Almgren-Chriss optimal execution strategy to model misspecification and changing market conditions?**

The results should provide insight into whether the theoretical optimality of Almgren-Chriss translates into an advantage when the assumptions of the model are no longer perfectly satisfied.
