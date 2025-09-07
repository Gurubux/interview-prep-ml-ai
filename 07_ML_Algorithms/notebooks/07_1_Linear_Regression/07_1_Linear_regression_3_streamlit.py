"""
Streamlit: Gradient Descent vs OLS — Modular Linear Regression Explorer
Usage:
  pip install streamlit plotly numpy
  streamlit run streamlit_linear_regression_gd_vs_ols_modular.py
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Dict

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# =====================================
# ---------- Core Data Types ----------
# =====================================

@dataclass
class DataConfig:
    seed: int
    n: int
    noise_sd: float
    true_C: float
    true_M: float
    dist_type: str = "Linear (C+M·x)"


@dataclass
class TrainConfig:
    standardize: bool
    init_mode: str  # "zeros" | "random"
    lr_mode: str  # "Auto (safe)" | "Manual"
    lr_value: float | None
    steps: int
    iter_t: int


@dataclass
class GDHistory:
    w0_hist: np.ndarray
    w1_hist: np.ndarray
    loss_hist: np.ndarray
    grads_hist: np.ndarray  # shape: (T, 2) -> (dC, dM)
    mu_sd: Tuple[float, float]
    used_lr: float


# =====================================
# ----------- Helper / Math -----------
# =====================================

@st.cache_data(show_spinner=False)
def generate_data(cfg: DataConfig) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(cfg.seed)
    x = np.linspace(0, 10, cfg.n)

    y_clean = make_signal(x, cfg, rng)
    # global iid noise still applied on top (keeps UI noise slider meaningful)
    y = y_clean + rng.normal(0, cfg.noise_sd, size=cfg.n)

    xs = np.linspace(x.min(), x.max(), 400)
    return x, y, xs


def add_bias(v: np.ndarray) -> np.ndarray:
    return np.c_[np.ones((len(v), 1)), v]


def closed_form_line(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
    Xb = add_bias(x)
    w = np.linalg.pinv(Xb.T @ Xb) @ (Xb.T @ y)  # [C, M]
    return float(w[0]), float(w[1])


def auto_lr(Xb: np.ndarray, n: int) -> float:
    # Safe step size: lr < 1/L ; L = (2/n) * s_max^2
    smax = np.linalg.svd(Xb, compute_uv=False)[0]
    L = (2.0 / n) * (smax ** 2)
    return 0.8 / L


def make_signal(x: np.ndarray, cfg: DataConfig, rng: np.random.Generator) -> np.ndarray:
    C, M = cfg.true_C, cfg.true_M
    dt = cfg.dist_type

    if dt.startswith("Linear"):
        return C + M * x

    if dt.startswith("Quadratic"):
        return C + M * x + 0.5 * (x ** 2)

    if dt.startswith("Sinusoidal"):
        return C + M * np.sin(x)

    if dt.startswith("Exponential"):
        return C + np.exp(M * x)

    if dt.startswith("Logarithmic"):
        return C + M * np.log1p(x)

    if dt.startswith("Piecewise"):
        # Simple kink: extra slope after x>5
        return C + M * x + 3.0 * np.maximum(0, x - 5)

    if dt.startswith("Heteroscedastic"):
        # Variance grows with x; base linear trend
        noise_scale = (0.2 + 0.15 * x)
        return C + M * x + rng.normal(0, 1, size=len(x)) * noise_scale

    if dt.startswith("With Outliers"):
        y = C + M * x
        # Add a few large spikes
        k = max(2, len(x) // 20)
        idx = rng.choice(len(x), size=k, replace=False)
        y[idx] += rng.normal(0, 12, size=k)
        return y

    # Fallback
    return C + M * x


# --- add: linearity diagnostics helpers ---
def _rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def _r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    ss_res = float(np.sum((y_true - y_pred) ** 2))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2)) + 1e-12
    return 1.0 - ss_res / ss_tot


def fit_linear_xy(x: np.ndarray, y: np.ndarray):
    Xb = np.c_[np.ones_like(x), x]
    w = np.linalg.lstsq(Xb, y, rcond=None)[0]  # [C, M]
    yhat = Xb @ w
    return dict(C=float(w[0]), M=float(w[1]), yhat=yhat, rmse=_rmse(y, yhat), r2=_r2(y, yhat))


def fit_quadratic_xy(x: np.ndarray, y: np.ndarray):
    X = np.c_[np.ones_like(x), x, x ** 2]
    a = np.linalg.lstsq(X, y, rcond=None)[0]  # [a0, a1, a2]
    yhat = X @ a
    return dict(a0=float(a[0]), a1=float(a[1]), a2=float(a[2]), yhat=yhat, rmse=_rmse(y, yhat), r2=_r2(y, yhat))


def linearity_diagnostic(x: np.ndarray, y: np.ndarray, xs: np.ndarray, threshold: float = 0.05):
    lin = fit_linear_xy(x, y)
    quad = fit_quadratic_xy(x, y)
    # relative improvement of quadratic over linear
    delta_rmse = (lin["rmse"] - quad["rmse"]) / (lin["rmse"] + 1e-12)
    meets = delta_rmse <= threshold
    # curves for plotting
    lin_curve = lin["C"] + lin["M"] * xs
    quad_curve = quad["a0"] + quad["a1"] * xs + quad["a2"] * (xs ** 2)
    return {
        "lin": lin, "quad": quad,
        "delta_rmse": float(delta_rmse),
        "meets": bool(meets),
        "lin_curve": lin_curve,
        "quad_curve": quad_curve,
        "threshold": float(threshold),
    }


def _moving_avg(y: np.ndarray, k: int = 11) -> np.ndarray:
    k = max(3, k | 1)  # odd window >=3
    w = np.ones(k) / k
    return np.convolve(y, w, mode="same")


# --- add: Ramsey RESET-style diagnostic (using x^2, x^3 terms) ---
def reset_diagnostic(x: np.ndarray, y: np.ndarray, threshold: float = 0.05):
    lin = fit_linear_xy(x, y)
    X_aug = np.c_[np.ones_like(x), x, x ** 2, x ** 3]
    a = np.linalg.lstsq(X_aug, y, rcond=None)[0]
    yhat_aug = X_aug @ a
    rmse_lin = lin["rmse"]
    rmse_aug = _rmse(y, yhat_aug)
    delta_rmse = (rmse_lin - rmse_aug) / (rmse_lin + 1e-12)
    meets = delta_rmse <= threshold  # if big improvement, flag non-linearity
    return {
        "rmse_lin": float(rmse_lin),
        "rmse_aug": float(rmse_aug),
        "delta_rmse": float(delta_rmse),
        "meets": bool(meets),
    }


# --- add: simple cubic regression spline (truncated power basis) ---
def _spline_design(x: np.ndarray, knots: np.ndarray) -> np.ndarray:
    # basis: [1, x, x^2, x^3, (x-k1)^3_+, ..., (x-km)^3_+]
    X = [np.ones_like(x), x, x ** 2, x ** 3]
    for k in knots:
        X.append(np.maximum(0, x - k) ** 3)
    return np.column_stack(X)


def spline_fit_compare(x: np.ndarray, y: np.ndarray, xs: np.ndarray, n_knots: int = 4, threshold: float = 0.07):
    # equally spaced interior knots
    knots = np.linspace(x.min(), x.max(), n_knots + 2)[1:-1]
    X = _spline_design(x, knots)
    Xs = _spline_design(xs, knots)
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    yhat_spline = X @ b
    yhat_spline_s = Xs @ b

    lin = fit_linear_xy(x, y)
    rmse_lin = lin["rmse"]
    rmse_spl = _rmse(y, yhat_spline)
    delta_rmse = (rmse_lin - rmse_spl) / (rmse_lin + 1e-12)
    meets = delta_rmse <= threshold

    return {
        "knots": knots,
        "yhat_spline": yhat_spline,
        "yhat_spline_s": yhat_spline_s,
        "rmse_lin": float(rmse_lin),
        "rmse_spline": float(rmse_spl),
        "delta_rmse": float(delta_rmse),
        "meets": bool(meets),
    }


# --- Independence (no autocorr) helpers ---
def residuals_from_linear(x: np.ndarray, y: np.ndarray):
    """Fit y ≈ C + Mx and return residuals plus the linear fit dict."""
    lin = fit_linear_xy(x, y)  # uses helper you already added
    e = y - lin["yhat"]
    return e, lin


def durbin_watson(e: np.ndarray) -> float:
    """DW ≈ 2 (no autocorr), <2 positive autocorr, >2 negative autocorr."""
    diff = np.diff(e)
    num = float(np.sum(diff ** 2))
    den = float(np.sum(e ** 2)) + 1e-12
    return num / den


def lag1_autocorr(e: np.ndarray) -> float:
    """Pearson correlation between e_t and e_{t-1}."""
    e0 = e[:-1] - np.mean(e[:-1])
    e1 = e[1:] - np.mean(e[1:])
    num = float(np.sum(e0 * e1))
    den = float(np.sqrt(np.sum(e0 ** 2) * np.sum(e1 ** 2)) + 1e-12)
    return num / den


def simple_acf(e: np.ndarray, max_lag: int = 10) -> np.ndarray:
    """ACF for lags 1..max_lag (quick, unbiased-ish)."""
    e = e - np.mean(e)
    den = np.sum(e ** 2) + 1e-12
    return np.array([np.sum(e[:-k] * e[k:]) / den for k in range(1, max_lag + 1)])


# --- Homoscedasticity helpers ---

def bin_variances(x: np.ndarray, residuals: np.ndarray, nbins: int = 8):
    """Variance of residuals across fitted-value bins."""
    order = np.argsort(x)
    xs = x[order];
    e = residuals[order]
    bins = np.linspace(xs.min(), xs.max(), nbins + 1)
    variances, centers = [], []
    for i in range(nbins):
        if i < nbins - 1:
            mask = (xs >= bins[i]) & (xs < bins[i + 1])
        else:
            mask = (xs >= bins[i]) & (xs <= bins[i + 1])
        if np.any(mask):
            variances.append(float(np.var(e[mask], ddof=1)))
            centers.append(0.5 * (bins[i] + bins[i + 1]))
    return np.asarray(centers, float), np.asarray(variances, float)


# Chi-square survival function for df=1 (for BP p-value)
import math


def _chi2_sf_df1(x: float) -> float:
    # P[ChiSq_1 >= x] = erfc(sqrt(x/2))
    return math.erfc(math.sqrt(max(x, 0.0) / 2.0))


def bp_test(yhat: np.ndarray, residuals: np.ndarray):
    """
    Breusch–Pagan LM test (aux reg: e^2 ~ 1 + yhat). df=1 so p-value via erfc().
    """
    n = len(residuals)
    u = residuals ** 2
    Z = np.c_[np.ones_like(yhat), yhat]  # intercept + fitted
    b = np.linalg.lstsq(Z, u, rcond=None)[0]
    uhat = Z @ b
    ss_res = float(np.sum((u - uhat) ** 2))
    ss_tot = float(np.sum((u - np.mean(u)) ** 2)) + 1e-12
    R2 = 1.0 - ss_res / ss_tot
    LM = n * R2
    p = _chi2_sf_df1(LM)  # df = 1
    return {"LM": float(LM), "R2": float(R2), "df": 1, "p": float(p)}


# --- Normality helpers (no extra deps needed) ---

def _skewness(e: np.ndarray) -> float:
    m = np.mean(e)
    s = np.std(e) + 1e-12
    z = (e - m) / s
    return float(np.mean(z ** 3))


def _excess_kurtosis(e: np.ndarray) -> float:
    m = np.mean(e)
    s = np.std(e) + 1e-12
    z = (e - m) / s
    return float(np.mean(z ** 4) - 3.0)


def jarque_bera(e: np.ndarray) -> dict:
    """Jarque–Bera test (df=2). p ≈ exp(-JB/2)."""
    n = len(e)
    g1 = _skewness(e)
    g2 = _excess_kurtosis(e)
    JB = n / 6.0 * (g1 ** 2 + 0.25 * g2 ** 2)
    p = float(np.exp(-0.5 * JB))  # chi2 df=2 survival function
    return {"JB": float(JB), "p": p, "skew": float(g1), "excess_kurt": float(g2)}


# Optional: Shapiro–Wilk if SciPy is available
def shapiro_pvalue_or_none(e: np.ndarray):
    try:
        from scipy.stats import shapiro
        return float(shapiro(e)[1])
    except Exception:
        return None


# Minimal standard normal inverse CDF (for Q–Q) using Acklam’s approximation
def _norm_ppf(p: np.ndarray) -> np.ndarray:
    # constants from Peter J. Acklam's algorithm
    a = [-39.6968302866538, 220.946098424521, -275.928510446969,
         138.357751867269, -30.6647980661472, 2.50662827745924]
    b = [-54.4760987982241, 161.585836858041, -155.698979859887,
         66.8013118877197, -13.2806815528857]
    c = [-0.00778489400243029, -0.322396458041136, -2.40075827716184,
         -2.54973253934373, 4.37466414146497, 2.93816398269878]
    d = [0.00778469570904146, 0.32246712907004, 2.445134137143,
         3.75440866190742]
    plow, phigh = 0.02425, 1 - 0.02425
    x = np.zeros_like(p, dtype=float)
    # lower region
    mask = p < plow
    q = np.sqrt(-2 * np.log(p[mask]))
    x[mask] = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
              ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    # central region
    mask = (p >= plow) & (p <= phigh)
    q = p[mask] - 0.5
    r = q * q
    x[mask] = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
              (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    # upper region
    mask = p > phigh
    q = np.sqrt(-2 * np.log(1 - p[mask]))
    x[mask] = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
              ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    return x


def gd_history(
        x: np.ndarray,
        y: np.ndarray,
        steps: int,
        lr: float | None,
        standardize: bool = True,
        init: str = "zeros",
        rng: np.random.Generator | None = None,
) -> GDHistory:
    """
    Trains y ≈ C + M*x using GD in z-space (if standardize) or x-space.
    Returns histories in ORIGINAL x-units for interpretability.
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

    return GDHistory(
        w0_hist=np.array(w0_hist),
        w1_hist=np.array(w1_hist),
        loss_hist=np.array(loss_hist),
        grads_hist=np.array(grads_hist),
        mu_sd=(mu, sd),
        used_lr=lr,
    )


# =====================================
# ----------- UI Components -----------
# =====================================

def setup_page() -> None:
    st.set_page_config(page_title="GD vs OLS — Linear Regression", layout="wide")
    st.title("Linear Regression via Gradient Descent — Interactive Explorer")


def sidebar_data_controls() -> DataConfig:
    with st.sidebar:
        st.header("Data")
        seed = st.number_input("Random seed", value=0, min_value=0, max_value=99999, step=1)
        n = st.slider("Number of points", min_value=20, max_value=500, value=120, step=10)
        noise_sd = st.slider("Noise std. dev.", min_value=0.0, max_value=5.0, value=2.0, step=0.1)
        true_C = st.number_input("True intercept (C*)", value=5.0, step=0.5, format="%.3f")
        true_M = st.number_input("True slope (M*)", value=2.5, step=0.1, format="%.3f")
        dist_type = st.selectbox(
            "Data pattern",
            [
                "Linear (C+M·x)",
                "Quadratic (C+M·x+0.5·x²)",
                "Sinusoidal (C+M·sin x)",
                "Exponential (C+exp(M·x))",
                "Logarithmic (C+M·log(1+x))",
                "Piecewise Linear (kink @ x=5)",
                "Heteroscedastic Linear",
                "With Outliers (Linear)"
            ],
            index=0,
            help="Other ideas to add later: cubic, step, |x|, sigmoid, seasonal+trend."
        )
    return DataConfig(
        seed=seed, n=int(n), noise_sd=float(noise_sd),
        true_C=float(true_C), true_M=float(true_M),
        dist_type=str(dist_type)
    )


def sidebar_train_controls(steps_default: int = 200) -> TrainConfig:
    with st.sidebar:
        st.header("Training (Gradient Descent)")
        standardize = st.checkbox("Standardize x (z-score)", value=True)
        init_mode = st.selectbox("Initial W", options=["zeros", "random"], index=0)
        lr_mode = st.selectbox("Learning rate", options=["Auto (safe)", "Manual"], index=0)
        lr_value = None
        if lr_mode == "Manual":
            lr_value = st.number_input(
                "lr (try 0.001–0.5)", value=0.1, min_value=1e-6, max_value=10.0, step=0.01, format="%.6f"
            )
        steps = st.slider("Max steps", min_value=5, max_value=1000, value=steps_default, step=5)
        iter_t = st.slider("Iteration to display", min_value=1, max_value=int(steps), value=min(50, int(steps)), step=1)
    return TrainConfig(
        standardize=bool(standardize),
        init_mode=str(init_mode),
        lr_mode=str(lr_mode),
        lr_value=float(lr_value) if lr_value is not None else None,
        steps=int(steps),
        iter_t=int(iter_t),
    )


# -------------- Visualizations --------------

def build_main_figure(
        x: np.ndarray,
        y: np.ndarray,
        xs: np.ndarray,
        C_t: float,
        M_t: float,
        C_ols: float,
        M_ols: float,
        losses: np.ndarray,
        iter_t: int,
        iter_max: int,
        lr_used: float,
        standardize: bool,
        init_mode: str,
) -> go.Figure:
    y_ols = C_ols + M_ols * xs
    y_gd = C_t + M_t * xs
    Xb = add_bias(x)
    ols_mse = float(np.mean((Xb @ np.array([C_ols, M_ols]) - y) ** 2))

    fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38],
                        subplot_titles=("Fit (data, GD line, OLS line)", "Loss vs iteration"))

    # Font size
    fig.update_layout(font=dict(size=20))

    # Left: data & lines
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="data", opacity=0.7), row=1, col=1)
    fig.add_trace(go.Scatter(x=xs, y=y_ols, mode="lines", name="OLS (closed-form)", line=dict(dash="dash")), row=1,
                  col=1)
    fig.add_trace(go.Scatter(x=xs, y=y_gd, mode="lines", name=f"GD (iter {iter_t})"), row=1, col=1)

    # Right: loss curve & OLS MSE
    fig.add_trace(go.Scatter(x=np.arange(1, iter_t + 1), y=losses[:iter_t], mode="lines+markers", name="GD loss"),
                  row=1, col=2)
    fig.add_trace(go.Scatter(x=[1, iter_t], y=[ols_mse, ols_mse], mode="lines", name=f"OLS MSE = {ols_mse:.3f}",
                             line=dict(dash="dash")), row=1, col=2)

    fig.update_xaxes(title_text="x", row=1, col=1)
    fig.update_yaxes(title_text="y", row=1, col=1)
    fig.update_xaxes(title_text="iteration", row=1, col=2)
    fig.update_yaxes(title_text="MSE", row=1, col=2)
    fig.update_layout(height=560, width=1200,
                      title=(
                          f"GD vs OLS — lr={lr_used:.4g} | standardize={standardize} | init={init_mode} | iter {iter_t}/{iter_max}"))
    return fig


def build_params_figure(steps: int, hist: GDHistory, C_ols: float, M_ols: float) -> go.Figure:
    iters_all = np.arange(1, steps + 1)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=iters_all, y=hist.w0_hist, mode="lines", name="C (intercept)"))
    fig.add_trace(go.Scatter(x=iters_all, y=hist.w1_hist, mode="lines", name="M (slope)"))
    fig.add_trace(
        go.Scatter(x=[1, steps], y=[C_ols, C_ols], mode="lines", line=dict(dash="dash"), name=f"C (OLS) = {C_ols:.3f}"))
    fig.add_trace(
        go.Scatter(x=[1, steps], y=[M_ols, M_ols], mode="lines", line=dict(dash="dash"), name=f"M (OLS) = {M_ols:.3f}"))
    fig.update_layout(title="Parameters vs iteration", xaxis_title="iteration", yaxis_title="value")
    return fig


def build_grads_figure(steps: int, hist: GDHistory) -> go.Figure:
    iters_all = np.arange(1, steps + 1)
    dC_hist = hist.grads_hist[:, 0]
    dM_hist = hist.grads_hist[:, 1]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=iters_all, y=dC_hist, mode="lines", name="grad C"))
    fig.add_trace(go.Scatter(x=iters_all, y=dM_hist, mode="lines", name="grad M"))
    fig.add_trace(go.Scatter(x=[1, steps], y=[0, 0], mode="lines", line=dict(dash="dash"), name="zero"))
    fig.update_layout(title="Gradients vs iteration", xaxis_title="iteration", yaxis_title="gradient")
    return fig


def build_wpath_figure(C_t: float, M_t: float, hist: GDHistory, C_ols: float, M_ols: float) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.w0_hist, y=hist.w1_hist, mode="lines+markers", name="GD path", marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=[hist.w0_hist[0]], y=[hist.w1_hist[0]], mode="markers", name="start",
                             marker=dict(symbol="circle-open", size=10)))
    fig.add_trace(go.Scatter(x=[C_t], y=[M_t], mode="markers", name="current", marker=dict(symbol="diamond", size=10)))
    fig.add_trace(
        go.Scatter(x=[C_ols], y=[M_ols], mode="markers", name="OLS optimum", marker=dict(symbol="star", size=12)))
    fig.update_layout(title="Parameter space trajectory (C vs M)", xaxis_title="C (intercept)", yaxis_title="M (slope)")
    return fig


def build_wnorm_figure(hist: GDHistory, steps: int) -> go.Figure:
    w_norm = np.sqrt(hist.w0_hist ** 2 + hist.w1_hist ** 2)
    iters_all = np.arange(1, steps + 1)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=iters_all, y=w_norm, mode="lines", name="‖w‖"))
    fig.update_layout(title="Parameter vector magnitude ‖w‖ vs iteration", xaxis_title="iteration", yaxis_title="‖w‖")
    return fig


def build_linearity_plot(
        x: np.ndarray, y: np.ndarray, xs: np.ndarray,
        lin_curve: np.ndarray, quad_curve: np.ndarray,
        lin_rmse: float, quad_rmse: float, delta_rmse: float
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="data", opacity=0.7))
    fig.add_trace(go.Scatter(x=xs, y=lin_curve, mode="lines", name=f"Linear fit (RMSE={lin_rmse:.3f})"))
    fig.add_trace(go.Scatter(x=xs, y=quad_curve, mode="lines", name=f"Quadratic fit (RMSE={quad_rmse:.3f})",
                             line=dict(dash="dash")))
    title = f"Linearity Check — ΔRMSE (quad vs linear) = {delta_rmse * 100:.1f}%"
    fig.update_layout(title=title, xaxis_title="x", yaxis_title="y")
    return fig


# --- add: residuals plot (data-driven linearity check) ---
def build_residuals_plot(x: np.ndarray, y: np.ndarray, yhat_lin: np.ndarray) -> go.Figure:
    r = y - yhat_lin
    order = np.argsort(x)
    xs, rs = x[order], r[order]
    rs_smooth = _moving_avg(rs, k=max(5, len(rs) // 20 | 1))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=rs, mode="markers", name="residuals", opacity=0.6))
    fig.add_trace(go.Scatter(x=xs, y=rs_smooth, mode="lines", name="smooth (moving avg)", line=dict(dash="dash")))
    fig.add_trace(go.Scatter(x=[xs.min(), xs.max()], y=[0, 0], mode="lines", name="zero", line=dict(dash="dot")))
    fig.update_layout(title="Residuals vs x (pattern-free ≈ linearity)", xaxis_title="x", yaxis_title="residual")
    return fig


# --- add: RESET comparison plot ---
def build_reset_plot(x: np.ndarray, y: np.ndarray, lin_pred: np.ndarray) -> go.Figure:
    order = np.argsort(x)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="data", opacity=0.6))
    fig.add_trace(go.Scatter(x=x[order], y=lin_pred[order], mode="lines", name="Linear fit"))
    fig.update_layout(title="RESET view (linear fit shown; model misspec can show as structure in residuals)",
                      xaxis_title="x", yaxis_title="y")
    return fig


# --- add: spline vs linear plot ---
def build_spline_compare_plot(xs: np.ndarray, y_lin_curve: np.ndarray, y_spline_curve: np.ndarray) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=y_lin_curve, mode="lines", name="Linear fit"))
    fig.add_trace(go.Scatter(x=xs, y=y_spline_curve, mode="lines", name="Cubic spline fit", line=dict(dash="dash")))
    fig.update_layout(title="Spline vs Linear — shape comparison", xaxis_title="x", yaxis_title="y")
    return fig


def build_residual_index_plot(x: np.ndarray, residuals: np.ndarray) -> go.Figure:
    order = np.argsort(x)  # treat x-order as "time" if data are time-like
    xs = x[order];
    rs = residuals[order]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=rs, mode="lines+markers", name="residual"))
    fig.add_trace(go.Scatter(x=[xs.min(), xs.max()], y=[0, 0], mode="lines",
                             name="zero", line=dict(dash="dot")))
    fig.update_layout(title="Residuals over x (look for runs)",
                      xaxis_title="x (ordered)", yaxis_title="residual")
    return fig


def build_residual_lag_plot(residuals: np.ndarray) -> go.Figure:
    e0, e1 = residuals[:-1], residuals[1:]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=e0, y=e1, mode="markers", name="(e_{t-1}, e_t)", opacity=0.7))
    fig.update_layout(title="Residual lag plot (e_t vs e_{t-1})",
                      xaxis_title="e_{t-1}", yaxis_title="e_t")
    return fig


def build_acf_bar(acf_vals: np.ndarray) -> go.Figure:
    lags = np.arange(1, len(acf_vals) + 1)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=lags, y=acf_vals, name="ACF"))
    fig.add_trace(go.Scatter(x=[lags.min(), lags.max()], y=[0.0, 0.0], mode="lines",
                             name="zero", line=dict(dash="dot")))
    fig.update_layout(title="Residual ACF (first 10 lags)",
                      xaxis_title="lag", yaxis_title="correlation")
    return fig


def build_residuals_vs_fitted_plot(yhat: np.ndarray, residuals: np.ndarray) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=yhat, y=residuals, mode="markers", name="residuals", opacity=0.6))
    fig.add_trace(go.Scatter(x=[float(np.min(yhat)), float(np.max(yhat))], y=[0, 0],
                             mode="lines", name="zero", line=dict(dash="dot")))
    fig.update_layout(title="Residuals vs Fitted (look for 'fan' shape)",
                      xaxis_title="Fitted (ŷ)", yaxis_title="Residual")
    return fig


def build_scale_location_plot(yhat: np.ndarray, residuals: np.ndarray) -> go.Figure:
    z = np.sqrt(np.abs(residuals))
    order = np.argsort(yhat)
    yhat_s, z_s = yhat[order], z[order]
    z_smooth = _moving_avg(z_s, k=max(5, (len(z_s) // 20) | 1))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=yhat, y=z, mode="markers", name="√|residual|", opacity=0.6))
    fig.add_trace(go.Scatter(x=yhat_s, y=z_smooth, mode="lines", name="smooth", line=dict(dash="dash")))
    fig.update_layout(title="Scale–Location (√|residual| vs Fitted)",
                      xaxis_title="Fitted (ŷ)", yaxis_title="√|residual|")
    return fig


def build_var_by_bin_bar(centers: np.ndarray, variances: np.ndarray) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=centers, y=variances, name="Var(residual) by bin"))
    fig.update_layout(title="Residual Variance by Fitted-value Bins",
                      xaxis_title="Fitted (bin centres)", yaxis_title="Variance of residuals")
    return fig


def build_residual_histogram(residuals: np.ndarray) -> go.Figure:
    mu, sd = float(np.mean(residuals)), float(np.std(residuals) + 1e-12)
    xs = np.linspace(mu - 4 * sd, mu + 4 * sd, 300)
    pdf = (1 / (sd * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((xs - mu) / sd) ** 2)

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=residuals, histnorm="probability density",
                               name="residuals", opacity=0.6, nbinsx=40))
    fig.add_trace(go.Scatter(x=xs, y=pdf, mode="lines", name="Normal PDF (μ,σ from residuals)"))
    fig.update_layout(title="Residuals Histogram + Normal Curve",
                      xaxis_title="residual", yaxis_title="density")
    return fig


def build_qq_plot(residuals: np.ndarray) -> go.Figure:
    e = np.sort(residuals.astype(float))
    n = len(e)
    mu, sd = float(np.mean(residuals)), float(np.std(residuals) + 1e-12)
    probs = (np.arange(1, n + 1) - 0.5) / n
    q_theory = _norm_ppf(probs) * sd + mu  # theoretical normal quantiles

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q_theory, y=e, mode="markers", name="Q–Q points", opacity=0.7))
    # reference line (through first & third quartiles)
    x1, x3 = np.percentile(q_theory, [25, 75])
    y1, y3 = np.percentile(e, [25, 75])
    m = (y3 - y1) / (x3 - x1 + 1e-12)
    b = y1 - m * x1
    xx = np.array([q_theory.min(), q_theory.max()])
    fig.add_trace(go.Scatter(x=xx, y=m * xx + b, mode="lines", name="reference line", line=dict(dash="dash")))
    fig.update_layout(title="Normal Q–Q Plot (residuals vs theoretical)",
                      xaxis_title="theoretical quantiles", yaxis_title="sample quantiles")
    return fig


# =====================================
# --------------- Panels ---------------
# =====================================

def render_status_panel(iter_t: int, iter_max: int, C_t: float, M_t: float, losses: np.ndarray, dC_t: float,
                        dM_t: float, lr_used: float) -> None:
    st.subheader("Status")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Iter", f"{iter_t}/{iter_max}")
    c2.metric("C (intercept)", f"{C_t:.4f}")
    c3.metric("M (slope)", f"{M_t:.4f}")
    c4.metric("Loss (MSE)", f"{losses[iter_t - 1]:.4f}")

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


# =====================================
# ----------------- App ----------------
# =====================================

def app() -> None:
    setup_page()

    # Controls
    data_cfg = sidebar_data_controls()
    train_cfg = sidebar_train_controls()

    # Data
    x, y, xs = generate_data(data_cfg)

    # Histories
    rng = np.random.default_rng(data_cfg.seed)
    hist = gd_history(
        x, y,
        steps=train_cfg.steps,
        lr=(train_cfg.lr_value if train_cfg.lr_mode == "Manual" else None),
        standardize=train_cfg.standardize,
        init=train_cfg.init_mode,
        rng=rng,
    )

    # OLS reference
    C_ols, M_ols = closed_form_line(x, y)

    # Current GD state
    t_idx = train_cfg.iter_t - 1
    C_t = float(hist.w0_hist[t_idx])
    M_t = float(hist.w1_hist[t_idx])
    losses = hist.loss_hist
    dC_t, dM_t = map(float, hist.grads_hist[t_idx])

    # Main figure
    main_fig = build_main_figure(
        x=x, y=y, xs=xs,
        C_t=C_t, M_t=M_t,
        C_ols=C_ols, M_ols=M_ols,
        losses=losses, iter_t=train_cfg.iter_t, iter_max=train_cfg.steps,
        lr_used=hist.used_lr, standardize=train_cfg.standardize, init_mode=train_cfg.init_mode,
    )
    st.plotly_chart(main_fig, use_container_width=True)
    # --- optional: after main_fig ---
    st.caption(
        "This app always fits a **linear** model. The linearity check compares linear vs quadratic fits to flag possible underfit when the data pattern is non-linear.")

    # Secondary charts
    a, b, c, d = st.columns(4)
    a.plotly_chart(build_params_figure(train_cfg.steps, hist, C_ols, M_ols), use_container_width=True)
    b.plotly_chart(build_grads_figure(train_cfg.steps, hist), use_container_width=True)
    c.plotly_chart(build_wpath_figure(C_t, M_t, hist, C_ols, M_ols), use_container_width=True)
    d.plotly_chart(build_wnorm_figure(hist, train_cfg.steps), use_container_width=True)

    # Status
    render_status_panel(train_cfg.iter_t, train_cfg.steps, C_t, M_t, losses, dC_t, dM_t, hist.used_lr)

    # --- add: Assumption 1 — Linearity block (right after Status) ---
    st.subheader("Assumption 1: Linearity")

    diag = linearity_diagnostic(x, y, xs, threshold=0.05)  # 5% default tolerance
    left, right = st.columns([0.32, 0.68])

    with left:
        if diag["meets"]:
            st.success("Looks linear ✅")
        else:
            st.error("Likely non-linear ❗")
        st.metric("RMSE (Linear)", f"{diag['lin']['rmse']:.4f}")
        st.metric("RMSE (Quadratic)", f"{diag['quad']['rmse']:.4f}")
        st.metric("ΔRMSE (improvement)", f"{diag['delta_rmse'] * 100:.2f}%")
        st.caption("Rule: if quadratic improves RMSE by > 5%, we flag potential non-linearity.")

    with right:
        st.plotly_chart(
            build_linearity_plot(
                x, y, xs,
                diag["lin_curve"], diag["quad_curve"],
                diag["lin"]["rmse"], diag["quad"]["rmse"], diag["delta_rmse"]
            ),
            use_container_width=True
        )
    # --- add: Advanced linearity checks (tabs) ---
    st.markdown("### More Linearity Diagnostics")

    # Fit the baseline linear once
    _lin = fit_linear_xy(x, y)

    # (A) Residuals pattern check
    res_fig = build_residuals_plot(x, y, _lin["yhat"])
    # Simple heuristic: if the smoothed residual range is large relative to RMSE, flag
    res_order = np.argsort(x)
    residuals_sorted = (y - _lin["yhat"])[res_order]
    smooth = _moving_avg(residuals_sorted, k=max(5, len(residuals_sorted) // 20 | 1))
    res_span = float(np.percentile(smooth, 95) - np.percentile(smooth, 5))
    residual_flag = res_span > 2.0 * _lin["rmse"]

    # (B) RESET (x^2, x^3)
    reset = reset_diagnostic(x, y, threshold=0.05)

    # (C) Spline comparison (cubic regression spline)
    spl = spline_fit_compare(x, y, xs, n_knots=4, threshold=0.07)
    lin_curve_xs = _lin["C"] + _lin["M"] * xs

    # Summary badge
    any_flag = (not reset["meets"]) or (not spl["meets"]) or residual_flag
    if any_flag:
        st.error("Linearity likely **violated** based on at least one diagnostic.")
    else:
        st.success("Linearity looks **reasonable** across diagnostics.")

    tabs = st.tabs(["Residuals vs x", "RESET test (ΔRMSE)", "Spline vs Linear"])

    with tabs[0]:
        st.plotly_chart(res_fig, use_container_width=True)
        st.caption(
            "A **pattern-free** residual cloud supports linearity. Systematic waves/kinks suggest non-linearity.")

    with tabs[1]:
        col1, col2 = st.columns([0.45, 0.55])
        with col1:
            if reset["meets"]:
                st.success("RESET: OK (no big gain from x²,x³)")
            else:
                st.error("RESET: Non-linearity indicated (x²,x³ improved fit).")
            st.metric("RMSE (Linear)", f"{reset['rmse_lin']:.4f}")
            st.metric("RMSE (Augmented x²,x³)", f"{reset['rmse_aug']:.4f}")
            st.metric("ΔRMSE", f"{reset['delta_rmse'] * 100:.2f}%")
            st.caption("Heuristic: >5% ΔRMSE improvement → likely non-linear.")
        with col2:
            st.plotly_chart(build_reset_plot(x, y, _lin["yhat"]), use_container_width=True)

    with tabs[2]:
        if spl["meets"]:
            st.success("Spline: OK (no big improvement over linear)")
        else:
            st.error("Spline: Non-linearity indicated (curved fit helps).")
        st.metric("RMSE (Linear)", f"{spl['rmse_lin']:.4f}")
        st.metric("RMSE (Spline)", f"{spl['rmse_spline']:.4f}")
        st.metric("ΔRMSE", f"{spl['delta_rmse'] * 100:.2f}%")
        st.plotly_chart(
            build_spline_compare_plot(xs, lin_curve_xs, spl["yhat_spline_s"]),
            use_container_width=True
        )
        st.caption("Cubic regression spline (~4 knots) offers flexible curvature; big gains suggest non-linearity.")

    # --- Assumption 2: Independence of Errors (No Autocorrelation) ---
    st.subheader("Assumption 2: Independence of Errors (No Autocorrelation)")

    # Residuals from a simple linear fit (same baseline used for other diagnostics)
    residuals, lin_fit = residuals_from_linear(x, y)

    dw = durbin_watson(residuals)
    rho1 = lag1_autocorr(residuals)
    acf_vals = simple_acf(residuals, max_lag=10)

    # Heuristic bands for indicator
    # DW ~ 2 ok; <1.5 positive autocorr; >2.5 negative autocorr; also check |rho1|
    ok_dw = (1.5 <= dw <= 2.5)
    ok_rho = (abs(rho1) < 0.2)
    independence_ok = ok_dw and ok_rho

    left, right = st.columns([0.32, 0.68])
    with left:
        if independence_ok:
            st.success("Residuals look independent ✅")
        else:
            if dw < 1.5 or rho1 > 0.2:
                st.error("Positive autocorrelation likely ❗ (streaky residuals)")
            elif dw > 2.5 or rho1 < -0.2:
                st.error("Negative autocorrelation likely ❗ (flip-flopping residuals)")
            else:
                st.warning("Borderline — inspect charts.")

        st.metric("Durbin–Watson", f"{dw:.3f}")
        st.metric("Lag-1 autocorr (ρ₁)", f"{rho1:.3f}")
        st.caption("DW≈2 ⇒ no autocorr; <2 ⇒ positive; >2 ⇒ negative. |ρ₁| < 0.2 is a simple comfort rule.")

    with right:
        tabs = st.tabs(["Residuals over x", "Lag plot", "ACF (first 10 lags)"])
        with tabs[0]:
            st.plotly_chart(build_residual_index_plot(x, residuals), use_container_width=True)
            st.caption("Random cloud around 0 supports independence; long runs above/below 0 suggest autocorrelation.")
        with tabs[1]:
            st.plotly_chart(build_residual_lag_plot(residuals), use_container_width=True)
            st.caption("If points cluster along a diagonal line, residuals are correlated with their previous values.")
        with tabs[2]:
            st.plotly_chart(build_acf_bar(acf_vals), use_container_width=True)
            st.caption("Large bars at small lags → autocorrelation. Ideally bars hover near 0.")

    # --- Assumption 3: Homoscedasticity (Constant Variance) ---
    st.subheader("Assumption 3: Homoscedasticity (Constant Variance)")

    # Use residuals from the baseline linear fit
    residuals, lin_fit = residuals_from_linear(x, y)
    yhat = lin_fit["yhat"]

    # Variance by bins across fitted values
    centers, vars_by_bin = bin_variances(yhat, residuals, nbins=8)
    var_ratio = float(np.max(vars_by_bin) / (np.min(vars_by_bin) + 1e-12)) if len(vars_by_bin) > 1 else 1.0
    corr_trend = float(np.corrcoef(centers, vars_by_bin)[0, 1]) if len(vars_by_bin) > 1 else 0.0

    # Breusch–Pagan
    bp = bp_test(yhat, residuals)

    # Heuristics (interactive-friendly thresholds)
    flag_hetero = (var_ratio > 2.5) or (abs(corr_trend) > 0.40) or (bp["p"] < 0.05)

    left, right = st.columns([0.34, 0.66])
    with left:
        if flag_hetero:
            st.error("Heteroscedasticity likely ❗ (non-constant error variance)")
        else:
            st.success("Variance looks roughly constant ✅")
        st.metric("Variance ratio (max/min)", f"{var_ratio:.2f}")
        st.metric("Trend corr (var vs ŷ)", f"{corr_trend:.2f}")
        st.metric("Breusch–Pagan LM", f"{bp['LM']:.3f}")
        st.metric("BP p-value (df=1)", f"{bp['p']:.3f}")
        st.caption("Heuristics: ratio>2.5 or |corr|>0.40 or BP p<0.05 ⇒ flag.")

    with right:
        tabs = st.tabs(["Residuals vs Fitted", "Scale–Location", "Variance by Bins"])
        with tabs[0]:
            st.plotly_chart(build_residuals_vs_fitted_plot(yhat, residuals), use_container_width=True)
            st.caption("‘Fan’ shape (spreading with ŷ) suggests heteroscedasticity.")
        with tabs[1]:
            st.plotly_chart(build_scale_location_plot(yhat, residuals), use_container_width=True)
            st.caption("A flat smooth line supports constant variance.")
        with tabs[2]:
            st.plotly_chart(build_var_by_bin_bar(centers, vars_by_bin), use_container_width=True)
            st.caption("Similar bar heights across bins ≈ homoscedasticity.")

    # --- Assumption 4: Normality of Errors ---
    st.subheader("Assumption 4: Normality of Errors")

    # residuals from baseline linear fit
    residuals, lin_fit = residuals_from_linear(x, y)

    # Tests
    jb = jarque_bera(residuals)
    sh_p = shapiro_pvalue_or_none(residuals)

    # Heuristic decision
    normal_ok = (jb["p"] >= 0.05) and (sh_p is None or sh_p >= 0.05)

    left, right = st.columns([0.34, 0.66])
    with left:
        if normal_ok:
            st.success("Residuals look roughly normal ✅")
        else:
            st.error("Non-normal residuals likely ❗ (heavy tails / skew)")

        st.metric("Jarque–Bera (p)", f"{jb['p']:.3f}")
        st.metric("Skewness", f"{jb['skew']:.3f}")
        st.metric("Excess Kurtosis", f"{jb['excess_kurt']:.3f}")
        if sh_p is not None:
            st.metric("Shapiro–Wilk (p)", f"{sh_p:.3f}")
            st.caption("Install SciPy to enable Shapiro–Wilk: `pip install scipy`")

        st.caption("Rule of thumb: p ≥ 0.05 ⇒ no strong evidence against normality.")

    with right:
        tabs = st.tabs(["Histogram + Normal", "Q–Q Plot"])
        with tabs[0]:
            st.plotly_chart(build_residual_histogram(residuals), use_container_width=True)
            st.caption("Bell-shaped, symmetric histogram supports normality.")
        with tabs[1]:
            st.plotly_chart(build_qq_plot(residuals), use_container_width=True)
            st.caption("Points near the dashed line ≈ normal. S-shaped curve ⇒ skew; bowed tails ⇒ heavy/light tails.")


# -------------- Main --------------
if __name__ == "__main__":
    app()
