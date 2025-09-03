# app.py
# Streamlit: Gradient Descent for Linear Regression (with Plotly)
# Usage:
#   pip install streamlit plotly numpy
#   streamlit run app.py

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ----------- Page setup -----------
st.set_page_config(page_title="GD vs OLS — Linear Regression", layout="wide")
st.title("Linear Regression via Gradient Descent — Interactive Explorer")

# ----------- Toy data -----------
with st.sidebar:
    st.header("Data")
    seed = st.number_input("Random seed", value=0, min_value=0, max_value=99999, step=1)
    n = st.slider("Number of points", min_value=20, max_value=500, value=120, step=10)
    noise_sd = st.slider("Noise std. dev.", min_value=0.0, max_value=5.0, value=2.0, step=0.1)
    true_C = st.number_input("True intercept (C*)", value=5.0, step=0.5, format="%.3f")
    true_M = st.number_input("True slope (M*)", value=2.5, step=0.1, format="%.3f")

rng = np.random.default_rng(seed)
x = np.linspace(0, 10, n)
y = true_C + true_M * x + rng.normal(0, noise_sd, size=n)
xs = np.linspace(x.min(), x.max(), 400)


# ----------- Helpers -----------
def add_bias(v):
    return np.c_[np.ones((len(v), 1)), v]


def closed_form_line(x, y):
    Xb = add_bias(x)
    w = np.linalg.pinv(Xb.T @ Xb) @ (Xb.T @ y)  # [C, M]
    return float(w[0]), float(w[1])


def auto_lr(Xb, n):
    # Safe step size: lr < 1/L ; L = (2/n) * s_max^2
    smax = np.linalg.svd(Xb, compute_uv=False)[0]
    L = (2.0 / n) * (smax ** 2)
    return 0.8 / L


def gd_history(x, y, steps, lr, standardize=True, init="zeros", rng=None):
    """
    Trains y ≈ C + M*x using GD in z-space (if standardize) or x-space.
    Returns histories in ORIGINAL x-units:
      - w0_hist (C), w1_hist (M), loss_hist, grads_hist[(dC, dM)]
      - (mu, sd) used for standardization
      - used_lr
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    n = len(y)

    if standardize:
        mu, sd = x.mean(), x.std() + 1e-12
        z = (x - mu) / sd
        Xb = add_bias(z)
    else:
        mu, sd = 0.0, 1.0
        Xb = add_bias(x)

    if init == "zeros":
        b = np.zeros(2)  # [b0, b1]
    else:
        if rng is None:
            rng = np.random.default_rng(0)
        b = rng.normal(0, 0.1, size=2)

    if lr is None:
        lr = auto_lr(Xb, n)

    w0_hist, w1_hist, loss_hist = [], [], []
    grads_hist = []

    for _ in range(max(1, steps)):
        # Map to original x-units for logging/plotting
        if standardize:
            C = b[0] - b[1] * (mu / sd)
            M = b[1] / sd
            yhat = Xb @ b
        else:
            C, M = b[0], b[1]
            yhat = Xb @ b

        w0_hist.append(C)
        w1_hist.append(M)
        loss_hist.append(float(np.mean((yhat - y) ** 2)))

        # Gradient in training space
        e = yhat - y
        grad_b = (2.0 / n) * (Xb.T @ e)  # [d/db0, d/db1]

        # Convert gradient to original units for display
        dC = float(grad_b[0])
        dM = float(grad_b[1] * (sd if standardize else 1.0))
        grads_hist.append((dC, dM))

        # GD step
        b = b - lr * grad_b

    return {
        "w0_hist": np.array(w0_hist),
        "w1_hist": np.array(w1_hist),
        "loss_hist": np.array(loss_hist),
        "grads_hist": np.array(grads_hist),
        "mu_sd": (mu, sd),
        "used_lr": lr,
    }


# ----------- Controls -----------
with st.sidebar:
    st.header("Training (Gradient Descent)")
    standardize = st.checkbox("Standardize x (z-score)", value=True)
    init_mode = st.selectbox("Initial W", options=["zeros", "random"], index=0)
    lr_mode = st.selectbox("Learning rate", options=["Auto (safe)", "Manual"], index=0)
    lr_value = None
    if lr_mode == "Manual":
        lr_value = st.number_input("lr (try 0.001–0.5)", value=0.1, min_value=1e-6, max_value=10.0, step=0.01,
                                   format="%.6f")
    steps = st.slider("Max steps", min_value=5, max_value=1000, value=200, step=5)

# Precompute histories for chosen settings
hist = gd_history(
    x, y,
    steps=steps,
    lr=lr_value,
    standardize=standardize,
    init=init_mode,
    rng=rng,
)

# Iteration control
iter_max = steps
iter_t = st.sidebar.slider("Iteration to display", min_value=1, max_value=iter_max, value=min(50, iter_max), step=1)
t_idx = iter_t - 1  # 0-based

# OLS reference
C_ols, M_ols = closed_form_line(x, y)
y_ols = C_ols + M_ols * xs
ols_mse = float(np.mean((add_bias(x) @ np.array([C_ols, M_ols]) - y) ** 2))

# Current GD state
C_t = hist["w0_hist"][t_idx]
M_t = hist["w1_hist"][t_idx]
losses = hist["loss_hist"]
dC_t, dM_t = hist["grads_hist"][t_idx]
lr_used = hist["used_lr"]
y_gd = C_t + M_t * xs

# ----------- Plots -----------
fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38],
                    subplot_titles=("Fit (data, GD line, OLS line)", "Loss vs iteration"))
# font size = 12
fig.update_layout(font=dict(size=20))
# Left: data
fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="data", opacity=0.7), row=1, col=1)
# Left: OLS line
fig.add_trace(go.Scatter(x=xs, y=y_ols, mode="lines", name="OLS (closed-form)",
                         line=dict(dash="dash")), row=1, col=1)
# Left: GD current line
fig.add_trace(go.Scatter(x=xs, y=y_gd, mode="lines", name=f"GD (iter {iter_t})"), row=1, col=1)

# Right: GD loss curve up to t, with OLS MSE reference
fig.add_trace(go.Scatter(x=np.arange(1, iter_t + 1),
                         y=losses[:iter_t],
                         mode="lines+markers",
                         name="GD loss"), row=1, col=2)
fig.add_trace(go.Scatter(x=[1, iter_t],
                         y=[ols_mse, ols_mse],
                         mode="lines",
                         name=f"OLS MSE = {ols_mse:.3f}",
                         line=dict(dash="dash")), row=1, col=2)

fig.update_xaxes(title_text="x", row=1, col=1)
fig.update_yaxes(title_text="y", row=1, col=1)
fig.update_xaxes(title_text="iteration", row=1, col=2)
fig.update_yaxes(title_text="MSE", row=1, col=2)
fig.update_layout(height=560, width=1200,
                  title=(f"GD vs OLS — lr={lr_used:.4g} | "
                         f"standardize={standardize} | init={init_mode} | iter {iter_t}/{iter_max}"))

st.plotly_chart(fig, use_container_width=True)

a, b, c, d = st.columns(4)
# NEW: Parameters vs iteration (C & M)
iters_all = np.arange(1, steps + 1)

fig_params = go.Figure()
fig_params.add_trace(go.Scatter(x=iters_all, y=hist["w0_hist"],
                                mode="lines", name="C (intercept)"))
fig_params.add_trace(go.Scatter(x=iters_all, y=hist["w1_hist"],
                                mode="lines", name="M (slope)"))
# OLS references (dashed)
fig_params.add_trace(go.Scatter(x=[1, steps], y=[C_ols, C_ols],
                                mode="lines", line=dict(dash="dash"),
                                name=f"C (OLS) = {C_ols:.3f}"))
fig_params.add_trace(go.Scatter(x=[1, steps], y=[M_ols, M_ols],
                                mode="lines", line=dict(dash="dash"),
                                name=f"M (OLS) = {M_ols:.3f}"))

fig_params.update_layout(title="Parameters vs iteration",
                         xaxis_title="iteration", yaxis_title="value")
a.plotly_chart(fig_params, use_container_width=True)

# NEW: Gradients vs iteration (grad C & grad M)
dC_hist = hist["grads_hist"][:, 0]
dM_hist = hist["grads_hist"][:, 1]

fig_grads = go.Figure()
fig_grads.add_trace(go.Scatter(x=iters_all, y=dC_hist,
                               mode="lines", name="grad C"))
fig_grads.add_trace(go.Scatter(x=iters_all, y=dM_hist,
                               mode="lines", name="grad M"))
# Zero reference
fig_grads.add_trace(go.Scatter(x=[1, steps], y=[0, 0],
                               mode="lines", line=dict(dash="dash"),
                               name="zero"))

fig_grads.update_layout(title="Gradients vs iteration",
                        xaxis_title="iteration", yaxis_title="gradient")
b.plotly_chart(fig_grads, use_container_width=True)

# NEW: Parameter space trajectory (w = [C, M])
fig_wpath = go.Figure()
# Full GD path
fig_wpath.add_trace(go.Scatter(x=hist["w0_hist"], y=hist["w1_hist"],
                               mode="lines+markers", name="GD path",
                               marker=dict(size=6)))
# Start point
fig_wpath.add_trace(go.Scatter(x=[hist["w0_hist"][0]], y=[hist["w1_hist"][0]],
                               mode="markers", name="start",
                               marker=dict(symbol="circle-open", size=10)))
# Current point
fig_wpath.add_trace(go.Scatter(x=[C_t], y=[M_t],
                               mode="markers",
                               name=f"current (iter {iter_t})",
                               marker=dict(symbol="diamond", size=10)))
# OLS optimum
fig_wpath.add_trace(go.Scatter(x=[C_ols], y=[M_ols],
                               mode="markers", name="OLS optimum",
                               marker=dict(symbol="star", size=12)))

fig_wpath.update_layout(title="Parameter space trajectory (C vs M)",
                        xaxis_title="C (intercept)",
                        yaxis_title="M (slope)")
c.plotly_chart(fig_wpath, use_container_width=True)

# OPTIONAL: ||w|| vs iteration
w_norm = np.sqrt(hist["w0_hist"] ** 2 + hist["w1_hist"] ** 2)
fig_wnorm = go.Figure()
fig_wnorm.add_trace(go.Scatter(x=iters_all, y=w_norm, mode="lines", name="‖w‖"))
fig_wnorm.update_layout(title="Parameter vector magnitude ‖w‖ vs iteration",
                        xaxis_title="iteration", yaxis_title="‖w‖")
d.plotly_chart(fig_wnorm, use_container_width=True)

# ----------- Status panel -----------
st.subheader("Status")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Iter", f"{iter_t}/{iter_max}")
c2.metric("C (intercept)", f"{C_t:.4f}")
c3.metric("M (slope)", f"{M_t:.4f}")
c4.metric("Loss (MSE)", f"{losses[t_idx]:.4f}")

c5, c6, c7, c8 = st.columns(4)
c6.metric("grad C", f"{dC_t:.4f}")
c7.metric("grad M", f"{dM_t:.4f}")
c8.metric("lr used", f"{lr_used:.4g}")

st.write(
    "Model: ŷ = C + M·x  \n  Loss: mean((ŷ − y)²)  \n  "
    "Update: [C,M] ← [C,M] − lr·∇, \n  \t where ∇ = (2/n)[∑e, ∑e·x].\n  "
    "Standardization (if on) stabilizes GD; \n "
    "OLS dashed line is the closed-form optimum."
)
