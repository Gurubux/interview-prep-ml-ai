# Linear Regression — Algorithm README (your mental model)

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
X_b = \begin{bmatrix} 1 & x_1 \\ 1 & x_2 \\ \vdots & \vdots \\ 1 & x_n \end{bmatrix}
$$

  shape: $(n \times 2)$
* **Parameters:** 
$w = \begin{bmatrix} C \\ M \end{bmatrix}$
  shape: $(2 \times 1)$
* **Predictions:** $\hat y = X_b\,w$  (vector, shape $(n \times 1)$)
* **Residuals (errors):** $e = \hat y - y$ (shape $(n \times 1)$)

Python equivalence:

* `Xb = np.c_[np.ones(n), x]`
* `w = np.array([C, M])`
* `yhat = Xb @ w`  (here `@` is matrix multiply / dot)

---

## 2) Loss (what we minimize)

$$
L(C,M) = \frac{1}{n}\sum_{i=1}^n (\hat y_i - y_i)^2
\;=\; \frac{1}{n}\, \|e\|_2^2
\;=\; \frac{1}{n}\, e^\top e
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
\nabla_w L
=
\begin{bmatrix}
\partial L/\partial C\\
\partial L/\partial M
\end{bmatrix}
=
\frac{2}{n}\,X_b^\top e
=
\frac{2}{n}
\begin{bmatrix}
\sum e_i\\
\sum x_i e_i
\end{bmatrix}.
$$

**Intuition:**

* First component (sum of errors) tells how to **shift** the line (adjust $C$).
* Second (sum of error×x) tells how to **tilt** the line (adjust $M$).

---

## 4) Update rule (the learning step)

$$
\boxed{\,w \leftarrow w - \text{lr}\cdot \nabla_w L \;=\; w - \text{lr}\cdot \frac{2}{n}\,X_b^\top e\,}
$$

Where **lr** is the learning rate (step size).

> Your earlier line had a formatting slip — the correct factor is **(2/n)**, not **n/2**.

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

**You nailed the mental model.**
I’ll keep explanations anchored to:
**“Xb = \[1, x], w = \[C, M], ŷ = C + Mx, e = ŷ − y, Loss = mean(e²), grad = (2/n)Xbᵀe, update w ← w − lr·grad.”**
