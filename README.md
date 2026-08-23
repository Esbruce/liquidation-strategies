\documentclass{article}
\usepackage{graphicx} % Required for inserting images

\title{liquadation-strategies}
\author{Edward Schuster-Bruce}
\date{August 2026}

\begin{document}

\maketitle

\section{Introduction}

# liquidation-strategies
Exploring how a optimal analytical model and a reinforcement learning model for executing large trades perform and diverge as assumptions of the analytical model are violated.

# Project Overview

Recently I completed a university project on wave energy converter control methods, and came across some interesting hamiltonian based mathematics. I wanted to see what other applications these could have and this project is a result of that. 

The problem investigated is how to best liquidate a large holding, whilst minimising the risk of volatility in the market and minimising transaction costs arising from long and short term market impact.

Mathematically the problem can be described as follows:

A holding of size $X$ is being sold in $K$ increments such that the quantity of each sale is notated as $n_1, n_k ... n_N$. $x_k$ is the remaining amount of the holding that needs to be sold. This is happening in a time frame of $T$ such that all holdings are sold by $t=T$

### Long term impacts of each sale:
are those which affect the price of the holding after the sale is completed. 
Mathematically these can be written as a change in price of the remaining holding: 

$$S_k = S_{k-1} + \sigma \sqrt{\tau} \epsilon - \tau g(n_k / \tau)$$

Here: $\tau$ the length of each discrete trading interval, $\sigma$: volatility, $\epsilon$ random noise, $g(\cdot)$ a function trade velocity dictates the market reaction of the sale. 

### Short term impacts of each sale:
Short term changes in the price of a asset caused by the presence of the trade in the market. 

Mathematically these can be written as: $S_k = S_{k-1} + h(n_k / \tau)$ , where $h(\cdot)$ is commonly a cost that is a percentage of the amount of holding sold in the trading window.

### The result of the sale of the asset is:

$$\sum_{k=1}^{N} n_k S_k = X S_0 + \sum_{k=1}^{N} \left( \sigma \sqrt{\tau} \epsilon_k - \tau g(n_k/\tau) \right) x_k - \sum_{k=1}^{N} n_k h(n_k/\tau)$$

We start from the general cost identity, valid for any impact functions $g$ and $h$:

$$C = \sum_{k=1}^{N} \tau x_k\, g(n_k/\tau) + \sum_{k=1}^{N} n_k\, h(n_k/\tau) - \sigma\sqrt{\tau}\sum_{k=1}^{N} x_k \epsilon_k$$

This decomposes cost into permanent-impact drag, temporary-impact drag, and a noise contribution.

**Linear impact assumption.** Almgren-Chriss assume that impact scales linearly with trading velocity $v = n_k/\tau$:

$$g(v) = \gamma v, \qquad h(v) = \xi\,\mathrm{sgn}(v) + \eta v$$

so permanent impact is proportional to trading rate, and temporary impact combines a fixed cost-per-share $\xi$ (spread/slippage) with a rate-proportional component $\eta$. Substituting:

$$\tau x_k\, g(n_k/\tau) = \gamma x_k n_k, \qquad n_k\, h(n_k/\tau) = \xi|n_k| + \frac{\eta}{\tau}n_k^2$$

**Reducing the permanent-impact sum.** Since $n_k = x_{k-1} - x_k$, we have $x_{k-1}^2 - x_k^2 = 2x_k n_k + n_k^2$, so

$$x_k n_k = \frac{1}{2}\left[(x_{k-1}^2 - x_k^2) - n_k^2\right]$$

Summing over $k = 1, \dots, N$ leaves the first term, using $x_0 = X$ and $x_N = 0$:

$$\sum_{k=1}^{N} x_k n_k = \frac{1}{2}X^2 - \frac{1}{2}\sum_{k=1}^{N} n_k^2$$

so the permanent-impact contribution becomes $\gamma\left(\tfrac{1}{2}X^2 - \tfrac{1}{2}\sum_k n_k^2\right)$.

**Substituting back**,  cost becomes:

$$C = \frac{1}{2}\gamma X^2 + \xi\sum_{k=1}^{N}|n_k| + \left(\frac{\eta}{\tau} - \frac{\gamma}{2}\right)\sum_{k=1}^{N} n_k^2 - \sigma\sqrt{\tau}\sum_{k=1}^{N} x_k\epsilon_k$$

Defining $\tilde{\eta} \equiv \eta - \dfrac{\gamma\tau}{2}$ so the coefficient reads $\tilde{\eta}/\tau$: 

$$C = \frac{1}{2}\gamma X^2 + \xi\sum_{k=1}^{N}|n_k| + \frac{\tilde{\eta}}{\tau}\sum_{k=1}^{N} n_k^2 - \sigma\sqrt{\tau}\sum_{k=1}^{N} x_k\epsilon_k$$

Assuming non-bias Guassian noise  - $\mathbb{E}[\epsilon_k] = 0$, $\mathrm{Var}(\epsilon_k) = 1$, independent across $k$:

$$\mathbb{E}[C] = \frac{1}{2}\gamma X^2 + \xi\sum_{k=1}^{N}|n_k| + \frac{\tilde{\eta}}{\tau}\sum_{k=1}^{N} n_k^2$$

$$\mathbb{V}[C] = \sigma^2\tau\sum_{k=1}^{N} x_k^2$$

**The objective function** is therefore:

$$J = \mathbb{E}[C] + \lambda\,\mathbb{V}[C] = \frac{1}{2}\gamma X^2 + \xi\sum_{k=1}^{N}|n_k| + \frac{\tilde{\eta}}{\tau}\sum_{k=1}^{N} n_k^2 + \lambda\sigma^2\tau\sum_{k=1}^{N} x_k^2$$

where the final term encodes risk aversion: holding a large residual position $x_k$ exposes the trader to price risk over the remaining horizon, and $\lambda$ controls the trade-off against impact cost.

## Optimal Solution to the Objective Function

Taking the above objective equation the first two terms are constants, assuming that holdings are never bought back. This means they do not effect the efficacy of the trade and can be dropped. 
$$\tilde{J}(x_1,\dots,x_{N-1}) = \frac{\tilde\eta}{\tau}\sum_{k=1}^{N}(x_{k-1}-x_k)^2 + \lambda\sigma^2\tau\sum_{k=1}^{N} x_k^2$$

Every term here is a **square** of a linear expression in the $x_k$'s, multiplied by a positive coefficient ($\tilde\eta/\tau$ and $\lambda\sigma^2\tau$ respectively). Expanding the squares confirms $\tilde J$ is a sum of $x_k^2$ and $x_kx_{k-1}$ cross-terms with fixed positive/negative coefficients — i.e. $\tilde J$ is a **quadratic form** in the vector of free variables $(x_1,\dots,x_{N-1})$.

### Convexity

The quadratic is convex as it is composed of squared terms with positive coefficients.  A property of this is that all zero gradient points is a global minimum. 

This means the is no need to reason about second-order conditions, boundary behaviour of the objective, or compare candidate minima. To find the optimal trajectory is equivalent to finding the point where every partial derivative vanishes.

### Taking the partial derivative and setting it to zero

Pick a generic interior index $j$, with $1 \le j \le N-1$. Scanning $\tilde J$, only two terms in the impact sum involve $x_j$ (the $k=j$ term and the $k=j+1$ term), plus the direct risk term $x_j^2$:

$$\tilde J \supset \frac{\tilde\eta}{\tau}\Big[(x_{j-1}-x_j)^2 + (x_j-x_{j+1})^2\Big] + \lambda\sigma^2\tau\, x_j^2$$

Differentiating with respect to $x_j$:

$$\frac{\partial \tilde J}{\partial x_j} = \frac{\tilde\eta}{\tau}\Big[-2(x_{j-1}-x_j) + 2(x_j-x_{j+1})\Big] + 2\lambda\sigma^2\tau\, x_j$$

Setting this to zero (the stationarity condition) and dividing by 2:

$$\frac{\tilde\eta}{\tau}\Big[2x_j - x_{j-1} - x_{j+1}\Big] + \lambda\sigma^2\tau\, x_j = 0$$

This holds for every $j = 1,\dots,N-1$, giving a system of $N-1$ equations that together pin down the minimizing trajectory.

### Rearrange into a recursion

Multiply through by $\tau/\tilde\eta$ and collect terms:

$$x_{j+1} - 2x_j + x_{j-1} = \frac{\lambda\sigma^2\tau^2}{\tilde\eta}\, x_j$$

Define $\kappa^2 \equiv \dfrac{\lambda\sigma^2}{\tilde\eta}$, so:

$$x_{j+1} - \big(2+\kappa^2\tau^2\big)x_j + x_{j-1} = 0$$

This is a **linear, constant-coefficient recursion** relating each point on the optimal trajectory to its two neighbours.

### Solve via the ansatz $x_j = z^j$

For linear recursions of this type, the standard approach is to guess a solution of the form $x_j = z^j$ and find which values of $z$ are consistent with the equation. Substituting:

$$z^{j+1} - (2+\kappa^2\tau^2)z^j + z^{j-1} = 0$$

Dividing through by $z^{j-1}$ (assuming $z \ne 0$):

$$z^2 - (2+\kappa^2\tau^2)z + 1 = 0$$

This is the **characteristic equation** of the recursion. Its two roots multiply to $1$ and sum to $2+\kappa^2\tau^2 \ge 2$ — exactly the structure satisfied by $z = e^{\pm\alpha}$ for some $\alpha > 0$, since $e^\alpha \cdot e^{-\alpha} = 1$ and $e^\alpha + e^{-\alpha} = 2\cosh(\alpha)$. Defining $\alpha$ implicitly by

$$\cosh(\alpha) = 1 + \frac{\kappa^2\tau^2}{2}$$

the two roots of the characteristic equation are $z = e^{\alpha}$ and $z = e^{-\alpha}$.

Because the recursion is linear, the general solution is any combination of the two root-solutions:

$$x_j = A\,e^{\alpha j} + B\,e^{-\alpha j}$$

with constants $A,B$ still undetermined.

### SFix the constants using boundary conditions, obtain the optimal solution

The two boundary conditions we haven't used yet, $x_0 = X$ and $x_N = 0$, give:

$$A + B = X, \qquad Ae^{\alpha N} + Be^{-\alpha N} = 0$$

Solving this $2\times2$ system for $A$ and $B$ and substituting back (using $\sinh(u) = \tfrac12(e^u-e^{-u})$ to simplify) yields the closed-form optimal trajectory:

$$x_j = X\,\frac{\sinh\big(\alpha(N-j)\big)}{\sinh(\alpha N)}$$

This is the discrete Almgren-Chriss optimal execution trajectory

## Reinforcement Learning Strategy

## Test Environment

## Results

## Analysis





\end{document}
