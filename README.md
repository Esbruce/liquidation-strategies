# Liquidation Strategies
Implementing and evaluating the Almgren-Chriss model and strategy for liquidising large holdings.

# Project Motivation and Overview

In my second year Engineering Mathematics module "Principles of Physical Modelling", we had a introduction to Lagrangian mechanics. In this module we learnt how to derive second order equations of motions using the Euler-Lagrange Equations. Initially the results seemed surprising and impressive and I wanted to delve deeper into why the maths works and where else is was applicable - leading me to following problem. 

In mechanics the Lagrangian represents the difference in kinetic and potential energy of a body/particle $L = T - U$ where $T$ is the kinetic energy and $U$ is the potential energy.

The Lagrangian therefore is related to the the coordinates and motion of the body. $L = L(q(t),\dot{q}(t),t)$

Interesting the way this relates to the equation of motion of for example a ball in the air is by the action functional (function that takes a function (ie a path through space $q(t)$ ) and returns a value).

The actional functional $S= \int_{t_1}^{t2} L dt$ and the stationarity of this gives the equation of motion. 

This project explores the Almgren-Chriss strategy for liquidation a large holding.  The problem is how to best liquidate a large holding, whilst minimising the risk of volatility in the market and minimising transaction costs arising from long and short term market impact.

Mathematically the problem can be described as follows:

The optimisation problem is given you have $X$ shares to liquidate over $N$ trading blocks, how many shares $n_k$ should be sold in each trading block, in order to minimise the expected cost of the sale. 

The maths that draws parallel between the Almgren-Chriss and Lagrangian Mechanics is the use of calculus of variation used to find the stationarity of a action functional. 

In the case of Almgren-Chriss the action functional takes the trajectory of holdings kept at each trading block in a liquidation and returns the cost of the sale. The aim is to minimise this. 

# Mathematics of the Problem

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

**Taking expectations** under i.i.d. noise ($\mathbb{E}[\epsilon_k]=0$, $\mathrm{Var}(\epsilon_k)=1$), the noise term vanishes in mean and contributes $\sigma^2\tau\sum_k x_k^2$ to the variance:

$$\mathbb{E}[C] = \frac12\gamma X^2 + \xi\sum_{k=1}^N|n_k| + \frac{\tilde\eta}{\tau}\sum_{k=1}^N n_k^2 \qquad \mathbb{V}[C] = \sigma^2\tau\sum_{k=1}^N x_k^2$$

**Objective:**

$$J = \mathbb{E}[C] + \lambda \mathbb{V}[C] = \frac12\gamma X^2 + \xi\sum_{k=1}^N|n_k| + \frac{\tilde\eta}{\tau}\sum_{k=1}^N n_k^2 + \lambda\sigma^2\tau\sum_{k=1}^N x_k^2$$

where $\lambda$ trades off expected cost against the price risk of holding residual inventory $x_k$ over the remaining horizon.

## Drawing Parallel's with Lagrangian Mechanics:

TBC

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

Solving this $2\times2$ system for $A$ and $B$ and substituting back (using $\sinh(u) = \tfrac12(e^u-e^{-u})$ to simplify) yields the closed-form optimal trajectory:

$$x_j = X\,\frac{\sinh\big(\alpha(N-j)\big)}{\sinh(\alpha N)}$$

This is the discrete Almgren-Chriss optimal execution trajectory

## Efficiency Frontier:

## Testing the Model under Misspecification:

## Analysis:

## Disscusion:


