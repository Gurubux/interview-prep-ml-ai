# Linear Regression — Algorithm README

![Dashboard demo](https://github.com/Gurubux/interview-prep-ml-ai/blob/main/07_ML_Algorithms/notebooks/07_1_Linear_Regression/media/streamlit-07_1_Linear_regression_3_streamlit-2025-09-03-03-09-02.gif)

Code snippet: [Python Code](https://github.com/Gurubux/interview-prep-ml-ai/blob/main/07_ML_Algorithms/notebooks/07_1_Linear_Regression/07_1_Linear_regression_3_streamlit.py)
> **Crux (one line):**  
> **Xb = \[1, x], w = \[C, M], ŷ = Xb @ w = C + Mx, e = ŷ − y,  
> Loss = mean(e²), grad = (2/n)·Xbᵀ·e, update: w ← w − lr·grad.**  

---

## 0) What you’re learning

We fit a straight line **y ≈ C + M·x** to data points $(x_i, y_i)$ by **nudging** $C$ (intercept) and $M$ (slope) to make predictions closer to targets. That nudge is computed from the **gradient** of Mean Squared Error (MSE).

---

## 1) Notation & shapes (keep this picture in mind)

* **Design matrix:** 

$$
X_b = 
\begin{bmatrix} 1 & x_1 \\ 
1 & x_2 \\ 
\vdots & \vdots \\ 
1 & x_n 
\end{bmatrix}
$$

shape: $(n \times 2)$

* **Parameters:**   

$$
w = \begin{bmatrix} C \\ M \end{bmatrix}
$$

shape: $(2 \times 1)$
* **Predictions:**

$$
\hat y = X_b\,w  
$$

$(vector, shape (n \times 1))$

* **Residuals (errors):**

$$
e = \hat y - y 
$$

$(shape (n \times 1))$

Python equivalence:

* `Xb = np.c_[np.ones(n), x]`
* `w = np.array([C, M])`
* `yhat = Xb @ w`  (here `@` is matrix multiply / dot)

---

## 2) Loss (what we minimize)

$$
L(C,M) = \frac{1}{n}\sum_{i=1}^n (\hat y_i - y_i)^2
= \frac{1}{n} |e|_2^2
= \frac{1}{n} e^\top e
$$

(We use the **square** because it’s smooth and easy to differentiate; $\|e\|_2^2 = e^\top e$ for real vectors.)

---

## 3) Gradient (how we decide the nudge)

Differentiate $L$ w\.r.t. $C$ and $M$.

### Scalar view

$$
\frac{\partial L}{\partial C} = \frac{2}{n}\sum_{i=1}^n e_i,
\qquad
\frac{\partial L}{\partial M} = \frac{2}{n}\sum_{i=1}^n x_i\,e_i.
$$

### Packed vector (both at once)

$$
\begin{aligned}
\nabla_w L
&=
\begin{bmatrix}
\frac{\partial L}{\partial C} \\
\frac{\partial L}{\partial M}
\end{bmatrix}
\
&= \frac{2}{n}\,X_b^{\top} e
\
&= \frac{2}{n}
\begin{bmatrix}
\sum_{i=1}^n e_i \\
\sum_{i=1}^n x_i e_i
\end{bmatrix}.
\end{aligned}
$$


**Intuition:**

* First component (sum of errors) tells how to **shift** the line (adjust $C$).
* Second (sum of error×x) tells how to **tilt** the line (adjust $M$).

---

## 4) Update rule (the learning step)

$$
\boxed{w \leftarrow w - \text{lr}\cdot \nabla_w L = w - \text{lr}\cdot \frac{2}{n}X_b^\top e}
$$

Where **lr** is the learning rate (step size).

---

## 5) Full algorithm (plain steps)

1. **Build** $X_b = [\mathbf{1}, x]$.
2. **Init** $w = [C, M]^\top = [0, 0]^\top$ (or small random).
3. **Loop** for `steps`:

   * $\hat y \leftarrow X_b w$
   * $e \leftarrow \hat y - y$
   * $\text{grad} \leftarrow \dfrac{2}{n}\,X_b^\top e$
   * $w \leftarrow w - \text{lr}\cdot \text{grad}$
4. **Return** $w$ (your fitted $C, M$).

Pseudocode:

```text
Xb = [1, x]
w = [C, M] = [0, 0]
repeat steps:
    yhat = Xb @ w
    e = yhat - y
    grad = (2/n) * (Xb.T @ e)
    w = w - lr * grad
```

---

## 6) Micro derivation (chain rule, one line each)

Let $h(w)=X_b w - y$, $g(u)=\tfrac{1}{n}u^\top u$.  
Then $L(w)=g(h(w))$, $\nabla_u g = \tfrac{2}{n}u$, $\partial h/\partial w = X_b$.

$$
\nabla_w L
= (\partial h/\partial w)^\top \nabla_u g
= X_b^\top \cdot \frac{2}{n}(X_b w - y)
= \frac{2}{n} X_b^\top e.
$$

---

## 7) Tiny NumPy snippet (drop-in)

```python
import numpy as np

def fit_gd(x, y, lr=0.1, steps=200):
    n = len(y)
    Xb = np.c_[np.ones(n), x]       # [1, x]
    w = np.zeros(2)                 # [C, M]
    for _ in range(steps):
        yhat = Xb @ w               # predictions
        e = yhat - y                # residuals
        grad = (2/n) * (Xb.T @ e)   # [dC, dM]
        w = w - lr * grad           # update
    return w  # [C, M]
```

---

## 8) Sanity cues while training

* If predictions are **too high on average** → $\sum e_i > 0$ → gradient’s first entry > 0 → update **reduces $C$**.
* If errors **grow with $x$** → $\sum x_i e_i > 0$ → gradient’s second entry > 0 → update **reduces $M$**.
* Repeat until both sums trend toward **zero** (residuals become uncorrelated with 1 and with $x$).

---

## 9) (Optional) Closed-form (same solution, no looping)

Solve the **normal equations**:

$$
\boxed{\,w = (X_b^\top X_b)^{-1} X_b^\top y\,}
$$

Gradient descent approaches this solution as steps increase (with a sensible `lr`).

---

## 10) FAQ quickies

* **What is `@`?** Matrix multiply / dot in Python (`np.matmul`).
* **Why $e^\top e$?** It’s the squared Euclidean length $\|e\|_2^2$.
* **Why $X_b^\top e$?** It stacks the two sums you need: $\sum e_i$ and $\sum x_i e_i$.

---

**My Mental model.**
$X_b = \[1, x]$,   
w = \[C, M],   
ŷ = C + Mx,   
e = ŷ − y,   
Loss = mean(e²),   
grad = $\tfrac{1}{n}X_b^\top e$,   
update w ← w − lr·grad.  


---

# Assumptions of Linear Regression

| Assumption                                         | How tested                                                                                              | Plot used                                                                                        | Simple use case where it works                                                            | Where it is not met                                                                                             |                                                                                                 |                                                                                                    |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **1) Linearity**                                   | Compare linear vs flexible fits (Quadratic/Spline) and check ΔRMSE; Ramsey **RESET**; partial residuals | Residuals vs *x*; Linear vs Quadratic/Spline overlay; Partial residual (component+residual) plot | Physics lab with linear sensor response; small *x*-range of a smooth function             | Sinusoidal/curved relationships; saturation effects; thresholds; polynomial trends                              |                                                                                                 |                                                                                                    |
| **2) Independence of Errors (No Autocorrelation)** | **Durbin–Watson** (DW≈2 good); Lag-1 autocorr ρ₁; ACF/Ljung–Box                                         | Residuals over ordered *x* (or time); Lag plot (*e*ₜ vs *e*ₜ₋₁); ACF bars                        | Cross-sectional samples collected independently                                           | Time-series with inertia/seasonality (energy load, web traffic); sensor drift; spatial/clustered data           |                                                                                                 |                                                                                                    |
| **3) Homoscedasticity (Constant Variance)**        | **Breusch–Pagan / White** tests; variance-by-bin ratio; correlation of Var(residual) vs fitted          | Residuals vs Fitted (“fan” shape?); Scale–Location (√                                            | residual                                                                                  | vs ŷ); Variance-by-bin bar chart                                                                                | Controlled experiments with uniform measurement noise; stabilized data after log/sqrt transform | Income vs spend (variance grows with mean); counts (Poisson-like); financial volatility clustering |
| **4) Normality of Errors**                         | **Jarque–Bera**, **Shapiro–Wilk** (prefer tests on **studentized residuals**); Q–Q alignment            | Histogram + Normal curve; **Q–Q plot**                                                           | Many small independent noise sources (CLT); well-specified linear models without outliers | Heavy tails (finance returns), skewed positive outcomes (times, costs), mixtures/outliers                       |                                                                                                 |                                                                                                    |
| **5) No Multicollinearity (for multiple *X*)**     | **VIF** (e.g., VIF<5–10), condition number; inspect correlations                                        | Pairwise correlation heatmap; Partial regression plots                                           | Orthogonal experimental designs; well-separated, engineered features                      | Highly correlated features (e.g., height & arm span); one-hot traps; polynomial features without regularization |                                                                                                 |                                                                                                    |
| **6) Exogeneity / No Endogeneity**                 | Study design/causal reasoning; **Hausman test** (panel/IV); use **IV/2SLS** if needed                   | (No definitive residual plot) — may inspect residuals vs suspected omitted drivers               | Randomized experiments; strong controls with no feedback                                  | Omitted variables; reverse causality; measurement error in *X*; simultaneity (price ↔ demand)                   |                                                                                                 |                                                                                                    |

> Notes:  
> • For **Normality**, test **studentized** residuals (scale by √(1−hᵢᵢ)) to avoid leverage-induced variance mixing.  
> • When assumptions fail for **inference**, you can often keep the mean model but use **robust SEs** (HC/Newey–West), transforms, or more appropriate models (GLMs, ARIMA/GLS, mixed effects).

---

# Regression Diagnostics Quick Reference

When you fit a linear regression, check these diagnostics to validate assumptions and spot issues. Here’s a quick guide:

### Model fit & shape

* **Residuals vs Fitted** — “Are misses random?”
  Random cloud around 0 = good. Curve/funnel = wrong shape or non-constant variance.

* **Scale–Location (√|residual| vs ŷ)** — “Does spread change?”
  Flat band = constant variance. Upward slope = heteroscedasticity.

* **Q–Q Plot (residuals)** — “Bell-shaped?”
  Points on the line = normal-ish. S-curve = skew. Bent tails = heavy/light tails.

* **Ramsey RESET** — “Too simple a line?”
  Significant = model misspecification/nonlinearity; add transforms/terms.

* **Partial (Component+Residual) Plot** — “Each X linear on y?”
  Straight-ish = fine. Curvy = transform that predictor.

### Error independence (time/ordering)

* **Durbin–Watson (DW)** — “Are mistakes chained?”
  \~2 = independent. <2 = positive autocorr; >2 = negative autocorr.

* **Residual ACF (bars)** — “Memory in errors?”
  Bars near 0 = independent. Big early spikes = autocorrelation.

### Variance constancy (homoscedasticity)

* **Breusch–Pagan / White test** — “Equal spread?”
  p<0.05 → heteroscedasticity. Use robust SEs/transform/WLS.

* **Variance-by-bin (residuals)** — “Does variance grow?”
  Similar bin heights = OK. Rising pattern = hetero.

### Normality (for inference)

* **Jarque–Bera / Shapiro–Wilk** — “Bell-ish tails?”
  p≥0.05 = no strong evidence against normality (prefer tests on **studentized** residuals).

* **Histogram + Normal curve** — “Visual sanity check.”
  Symmetric bell around 0 = fine. Long tails/lopsided = not normal.

### Multicollinearity (multiple X)

* **VIF** — “Are X’s saying the same thing?”
  VIF > 5–10 → multicollinearity risk (unstable coeffs).

* **Condition Number** — “Overall collinearity.”

  > 30 → potential problems; consider regularization/feature changes.

### Outliers & influence

* **Studentized Residuals** — “Big misses?”
  |r| > 3 → outlier candidate.

* **Leverage (hᵢᵢ)** — “Unusual X?”

  > 2p/n (roughly) = high leverage; watch combined with big residuals.

* **Cook’s Distance** — “Does a point sway the fit?”

  > 4/n → influential; inspect.

---

### Handy thresholds (sound confident)

* **DW ≈ 2** OK; **<1.5 / >2.5** suspicious.
* **VIF > 5–10** concerning.
* **BP/White p < 0.05** heteroscedastic.
* **JB/Shapiro p ≥ 0.05** normal enough (use **studentized** residuals).
* **|studentized residual| > 3** outlier; **Cook’s D > 4/n** influential.

If you want, I can drop a compact “Diagnostics” section into your README with these bullets and a one-liner on what to do when each flag trips.
