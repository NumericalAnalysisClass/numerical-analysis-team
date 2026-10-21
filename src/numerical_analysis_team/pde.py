"""1次元偏微分方程式の差分法（第3・4・5・12・13・14回）。

いまは拡散方程式 u_t = α u_xx（区間 [0, L]、両端 Dirichlet 条件）だけ。
Burgers 方程式・KdV 方程式は今後追加する（Issue #1）。
"""

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class PDEResult:
    """解法の結果。u[n] が時刻 t[n] での格子点 x 上の値。"""

    x: np.ndarray  # 格子点（両端を含む nx + 1 点）
    t: np.ndarray  # 時刻（0 を含む nt + 1 点）
    u: np.ndarray  # 形は (nt + 1, nx + 1)


# ---- 格子 ------------------------------------------------------------------


def grid(L: float, nx: int) -> tuple[np.ndarray, float]:
    """区間 [0, L] を nx 等分した格子点（両端を含む nx + 1 点）と刻み dx = L / nx。"""
    if nx < 2:
        raise ValueError("nx は2以上にしてください")
    if L <= 0:
        raise ValueError("L は正にしてください")
    return np.linspace(0.0, L, nx + 1), L / nx


# ---- 差分演算子（第3回）--------------------------------------------------------


def second_derivative(u: np.ndarray, dx: float) -> np.ndarray:
    """中心差分による u_xx の近似。内部の点（両端を除く）での値を返す。

    u_xx(x_i) ≈ (u_{i-1} - 2 u_i + u_{i+1}) / dx²
    Taylor 展開から、誤差は dx² に比例する（2次精度）。
    """
    u = np.asarray(u, dtype=float)
    if u.size < 3:
        raise ValueError("u は3点以上にしてください")
    return (u[:-2] - 2 * u[1:-1] + u[2:]) / dx**2


# ---- 三重対角系の直接解法（第4・5回）-------------------------------------------


def thomas(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Thomas 法（三重対角行列に対する Gauss の消去法）で A x = d を解く。

    A の下対角が a（長さ n-1）、対角が b（長さ n）、上対角が c（長さ n-1）。
    前進消去で上対角だけを残し、後退代入で x を求める。計算量は O(n)。
    ピボット選択はしないので、A が対角優位であることを前提にする。
    """
    a, b, c, d = (np.asarray(v, dtype=float) for v in (a, b, c, d))
    n = b.size
    if a.size != n - 1 or c.size != n - 1 or d.size != n:
        raise ValueError("長さは a, c が n-1、b, d が n にしてください")

    cp = np.empty(n - 1)
    dp = np.empty(n)
    if b[0] == 0:
        raise ZeroDivisionError("ピボットが 0 になりました (i = 0)")
    if n > 1:
        cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i - 1] * cp[i - 1]
        if m == 0:
            raise ZeroDivisionError(f"ピボットが 0 になりました (i = {i})")
        if i < n - 1:
            cp[i] = c[i] / m
        dp[i] = (d[i] - a[i - 1] * dp[i - 1]) / m

    x = np.empty(n)
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


# ---- 拡散方程式（第12・13・14回）-----------------------------------------------


def heat_exact(x: np.ndarray, t: float, alpha: float = 1.0, L: float = 1.0, k: int = 1) -> np.ndarray:
    """拡散方程式の変数分離解 u = exp(-α (kπ/L)² t) sin(kπx/L)（両端 0）。"""
    w = k * np.pi / L
    return np.exp(-alpha * w**2 * t) * np.sin(w * np.asarray(x, dtype=float))


def _heat_setup(f, alpha, L, T, nx, nt, left, right):
    if alpha <= 0:
        raise ValueError("alpha は正にしてください")
    if T <= 0:
        raise ValueError("T は正にしてください")
    if nt < 1:
        raise ValueError("nt は1以上にしてください")
    x, dx = grid(L, nx)
    dt = T / nt
    u = np.empty((nt + 1, nx + 1))
    u[0] = f(x)
    u[:, 0], u[:, -1] = left, right
    return x, dx, dt, np.linspace(0.0, T, nt + 1), u


def heat_ftcs(
    f: Callable[[np.ndarray], np.ndarray],
    alpha: float = 1.0,
    L: float = 1.0,
    T: float = 0.1,
    nx: int = 50,
    nt: int = 1000,
    left: float = 0.0,
    right: float = 0.0,
    check_stability: bool = True,
) -> PDEResult:
    """前進 Euler 法＋中心差分（FTCS 法）で u_t = α u_xx を解く。

    u_i^{n+1} = u_i^n + r (u_{i-1}^n - 2 u_i^n + u_{i+1}^n),  r = α dt / dx²
    初期値 u(x, 0) = f(x)、境界 u(0, t) = left、u(L, t) = right。
    誤差は O(dt + dx²)。陽解法なので r ≤ 1/2 のときだけ安定（von Neumann の解析）。
    check_stability=False にすると、r > 1/2 でも計算して振動・発散する様子を見られる。
    """
    x, dx, dt, t, u = _heat_setup(f, alpha, L, T, nx, nt, left, right)
    r = alpha * dt / dx**2
    if check_stability and r > 0.5:
        raise ValueError(
            f"r = α dt / dx² = {r:.3g} > 1/2 で不安定です。nt を {int(np.ceil(2 * alpha * T / dx**2))} 以上にしてください"
        )
    for n in range(nt):
        u[n + 1, 1:-1] = u[n, 1:-1] + alpha * dt * second_derivative(u[n], dx)
    return PDEResult(x, t, u)


def heat_crank_nicolson(
    f: Callable[[np.ndarray], np.ndarray],
    alpha: float = 1.0,
    L: float = 1.0,
    T: float = 0.1,
    nx: int = 50,
    nt: int = 100,
    left: float = 0.0,
    right: float = 0.0,
) -> PDEResult:
    """Crank–Nicolson 法で u_t = α u_xx を解く。

    u_xx を時刻 n と n+1 の平均で近似する（台形則）。r = α dt / dx² として
    -r/2 u_{i-1}^{n+1} + (1 + r) u_i^{n+1} - r/2 u_{i+1}^{n+1}
        = r/2 u_{i-1}^n + (1 - r) u_i^n + r/2 u_{i+1}^n
    毎ステップ三重対角系を Thomas 法で解く。誤差は O(dt² + dx²)、r によらず安定。
    """
    x, dx, dt, t, u = _heat_setup(f, alpha, L, T, nx, nt, left, right)
    r = alpha * dt / dx**2
    m = nx - 1  # 未知数（内部の点）の数
    a = np.full(m - 1, -r / 2)
    b = np.full(m, 1 + r)
    c = np.full(m - 1, -r / 2)
    for n in range(nt):
        d = u[n, 1:-1] + r / 2 * dx**2 * second_derivative(u[n], dx)
        d[0] += r / 2 * left  # 時刻 n+1 の境界値を右辺へ移す
        d[-1] += r / 2 * right
        u[n + 1, 1:-1] = thomas(a, b, c, d)
    return PDEResult(x, t, u)
