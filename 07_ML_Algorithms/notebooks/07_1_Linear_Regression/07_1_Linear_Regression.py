# If needed:  %pip install plotly -q

import numpy as np
import plotly.graph_objects as go

# ----- 1) Toy data: y = 5 + 2.5x + noise -----
rng = np.random.default_rng(0)
n = 120
x = np.linspace(0, 10, n)
y = 5 + 2.5 * x + rng.normal(0, 2.0, size=n)


# ----- 2) Gradient Descent with a tiny bit of math safety -----
def gd_linreg_history(x, y, steps=400, lr=None):
    """
    Returns (weights_history, losses, (mu, sd))
      - We standardize x for stable GD: z = (x - mu)/sd
      - Model in z-space: y_hat = b0 + b1 * z
      - weights_history: array of [b0, b1] for each step
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    mu, sd = x.mean(), x.std() + 1e-12
    z = (x - mu) / sd

    # Design matrix with bias
    Xb = np.c_[np.ones((len(z), 1)), z]

    # Auto step size if not provided (safe upper bound ~ 1/L)
    if lr is None:
        smax = np.linalg.svd(Xb, compute_uv=False)[0]  # largest singular value
        L = (2.0 / len(y)) * (smax ** 2)
        lr = 0.8 / L

    w = np.zeros(2)  # [b0, b1]
    W = [w.copy()]
    losses = [np.mean((Xb @ w - y) ** 2)]

    for _ in range(steps):
        yhat = Xb @ w
        grad = (2 / len(y)) * (Xb.T @ (yhat - y))
        w = w - lr * grad
        W.append(w.copy())
        losses.append(np.mean((Xb @ w - y) ** 2))

    return np.array(W), np.array(losses), (mu, sd), lr


W, losses, (mu, sd), used_lr = gd_linreg_history(x, y, steps=20, lr=0.1)
print(f"Learning rate used: {used_lr:.4g}")

# Convert the final weights back to ORIGINAL x-units for curiosity:
b0_std, b1_std = W[-1]
w0 = b0_std - b1_std * (mu / sd)  # intercept in x-units
w1 = b1_std / sd  # slope in x-units
print(f"Final line (original units): y ≈ {w0:.3f} + {w1:.3f}·x")
