"""偏微分方程式の差分法（第3・4・5・12・13・14回）。

いまは拡散方程式だけ。
- 1次元 u_t = α u_xx（区間 [0, L]、両端 Dirichlet 条件）：FTCS 法・Crank–Nicolson 法
- 2次元 u_t = α (u_xx + u_yy)（長方形 [0, Lx]×[0, Ly]、周囲 Dirichlet 条件）：ADI 法
Burgers 方程式・KdV 方程式は今後追加する（Issue #1）。
"""

from dataclasses import dataclass
from typing import Callable

import numpy as np

#データクラスいいね。kotlin系でしか使ったことなかった。
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


# ---- 2次元の拡散方程式：ADI 法 --------------------------------------------------


@dataclass
class PDE2DResult:
    """2次元の解法の結果。u[n, i, j] が時刻 t[n]、点 (x[i], y[j]) での値。"""

    x: np.ndarray  # x 方向の格子点（nx + 1 点）
    y: np.ndarray  # y 方向の格子点（ny + 1 点）
    t: np.ndarray  # 時刻（0 を含む nt + 1 点）
    u: np.ndarray  # 形は (nt + 1, nx + 1, ny + 1)


def heat2d_exact(
    x: np.ndarray,
    y: np.ndarray,
    t: float,
    alpha: float = 1.0,
    Lx: float = 1.0,
    Ly: float = 1.0,
    kx: int = 1,
    ky: int = 1,
) -> np.ndarray:
    """2次元拡散方程式の変数分離解 exp(-α (wx² + wy²) t) sin(wx x) sin(wy y)（周囲 0）。

    wx = kx π / Lx、wy = ky π / Ly。返す配列の形は (len(x), len(y))（[i, j] が (x_i, y_j)）。
    """
    wx, wy = kx * np.pi / Lx, ky * np.pi / Ly
    X, Y = np.meshgrid(np.asarray(x, dtype=float), np.asarray(y, dtype=float), indexing="ij")
    return np.exp(-alpha * (wx**2 + wy**2) * t) * np.sin(wx * X) * np.sin(wy * Y)


def heat2d_adi(
    f: Callable[[np.ndarray, np.ndarray], np.ndarray],
    alpha: float = 1.0,
    Lx: float = 1.0,
    Ly: float = 1.0,
    T: float = 0.1,
    nx: int = 30,
    ny: int = 30,
    nt: int = 50,
    g: Callable[[np.ndarray, np.ndarray], np.ndarray] | None = None,
) -> PDE2DResult:
    """ADI 法（Peaceman–Rachford 法）で u_t = α (u_xx + u_yy) を解く。

    初期値 u(x, y, 0) = f(x, y)、周囲の境界 u = g(x, y)（時間によらない。None なら 0）。
    f, g は 2次元配列 X, Y（indexing="ij" の meshgrid）を受け取って同じ形の配列を返す関数。

    2次元で Crank–Nicolson 法をそのまま使うと、毎ステップ (nx-1)(ny-1) 元の
    帯行列を解くことになる。ADI 法は1ステップを半分ずつに分け、片方の向きだけ陰的にする。
    δx², δy² を2階中心差分（dx², dy² を掛けたもの）、rx = α dt / dx²、ry = α dt / dy² として
        (I - rx/2 δx²) u*      = (I + ry/2 δy²) u^n     … x 向きに陰的
        (I - ry/2 δy²) u^{n+1} = (I + rx/2 δx²) u*      … y 向きに陰的
    どちらも1本の格子線ごとに三重対角系なので、Thomas 法で O(nx ny) で解ける。
    誤差は O(dt² + dx² + dy²)、rx, ry によらず安定（Crank–Nicolson 法と同じ性質）。
    g が時間によらないので、途中の u* の境界値も g でよい。
    """
    if alpha <= 0:
        raise ValueError("alpha は正にしてください")
    if T <= 0:
        raise ValueError("T は正にしてください")
    if nt < 1:
        raise ValueError("nt は1以上にしてください")
    x, dx = grid(Lx, nx)
    y, dy = grid(Ly, ny)
    dt = T / nt
    X, Y = np.meshgrid(x, y, indexing="ij")
    G = np.zeros_like(X) if g is None else np.broadcast_to(np.asarray(g(X, Y), dtype=float), X.shape)

    u = np.empty((nt + 1, nx + 1, ny + 1))
    u[0] = f(X, Y)
    u[0][0, :], u[0][-1, :], u[0][:, 0], u[0][:, -1] = G[0, :], G[-1, :], G[:, 0], G[:, -1]

    rx, ry = alpha * dt / dx**2, alpha * dt / dy**2
    # x 向き（未知数 i = 1..nx-1）と y 向き（未知数 j = 1..ny-1）の三重対角行列
    ax, bx = np.full(nx - 2, -rx / 2), np.full(nx - 1, 1 + rx)
    ay, by = np.full(ny - 2, -ry / 2), np.full(ny - 1, 1 + ry)

    for n in range(nt):
        un = u[n]
        # 前半：各 y = y_j の線上で x 向きに陰的
        us = G.copy()  # 境界は g、内部はこれから埋める
        for j in range(1, ny):
            d = un[1:-1, j] + ry / 2 * dy**2 * second_derivative(un[1:-1, j - 1 : j + 2].T, dy).ravel()
            d[0] += rx / 2 * G[0, j]  # 境界 x = 0, Lx の値を右辺へ移す
            d[-1] += rx / 2 * G[-1, j]
            us[1:-1, j] = thomas(ax, bx, ax, d)
        # 後半：各 x = x_i の線上で y 向きに陰的
        un1 = u[n + 1]
        un1[:] = G
        for i in range(1, nx):
            d = us[i, 1:-1] + rx / 2 * dx**2 * second_derivative(us[i - 1 : i + 2, 1:-1], dx).ravel()
            d[0] += ry / 2 * G[i, 0]  # 境界 y = 0, Ly の値を右辺へ移す
            d[-1] += ry / 2 * G[i, -1]
            un1[i, 1:-1] = thomas(ay, by, ay, d)
    return PDE2DResult(x, y, np.linspace(0.0, T, nt + 1), u)

def LU_batched(a,b,c,d):
  """LU分解"""
  n = d.shape[0]
  #以降a,b,cも同じ形、かつ成分の型はfloatに抑える。
  a = np.broadcast_to(a,d.shape).astype(float)
  b = np.broadcast_to(b,d.shape).astype(float)
  c = np.broadcast_to(c,d.shape).astype(float)
  #同じ型で同じ行列型の行列をメモリ上に仮置き
  cp = np.empty_like(d,dtype=float)
  dp = np.empty_like(d,dtype=float)
  cp[0] = c[0] / b[0]
  dp[0] = d[0] / b[0]
  for k in range(1,n):
    denom = b[k] -a[k]*cp[k-1]
    cp[k] = c[k] / denom
    dp[k] = (d[k] - a[k] * dp[k-1]) /denom
  x = np.empty_like(d,dtype=float)
  x[-1] = dp[-1]
  for k in range(n-2, -1, -1):
    x[k] = dp[k] - cp[k] * x[k+1]
  return x

def lap1d(U, h, axis):
    """セル中心格子・同次 Neumann 境界の 2 階差分 δ²U（axis 方向）。

    境界の外に鏡像のゴースト点（U_{-1} = U_0, U_N = U_{N-1}）を置く。
    この離散化では行列が対称になり、総和 Σ U が厳密に保存される（f = 0 のとき）。
    """
    Up = np.moveaxis(U, axis, 0)
    out = np.empty_like(Up)
    out[1:-1] = Up[2:] - 2 * Up[1:-1] + Up[:-2]
    out[0] = Up[1] - Up[0]
    out[-1] = Up[-2] - Up[-1]
    return np.moveaxis(out, 0, axis) / h**2


def neumann_coeffs(n, h, a):
    """(I - a δ²) の三重対角係数（セル中心・Neumann）。a は δ² に掛かる係数（例：拡散係数×半ステップ幅）。"""
    s = a / h**2
    lower = np.full(n, -s)
    upper = np.full(n, -s)
    diag = np.full(n, 1 + 2 * s)
    diag[0] = diag[-1] = 1 + s       # ゴースト点の鏡像で端の対角が変わる
    return lower, diag, upper


def implicit_solve(rhs, h, a, axis):
    """(I - a δ²_axis) X = rhs を axis 方向に解く（他の方向の各列はまとめて解く）。"""
    R = np.moveaxis(rhs, axis, 0)
    n = R.shape[0]
    lo, di, up = neumann_coeffs(n, h, a)
    R2 = R.reshape(n, -1)
    X = LU_batched(lo[:, None], di[:, None], up[:, None], R2) 
    return np.moveaxis(X, 0, axis)



# ---------------- 反応項（f と f' を返す） ----------------
def kpp(a=1.0):
    return (lambda u: a * u * (1 - u)), (lambda u: a * (1 - 2 * u))


def bistable(theta=0.25):
    f = lambda u: u * (1 - u) * (u - theta)
    df = lambda u: -3 * u**2 + 2 * (1 + theta) * u - theta
    return f, df


# ---------------- 1 ステップ（HV 型 ADI） ----------------
def adi_step_only_you(U, tau, hx, hy, D, f, df, newton_iter=3):
    #fがuにしか依らない(x,y,tには依らない)場合を暫定的に考えた結果。
    a = tau / 2
    # 前半：x 陰的、y と f は陽的（古い時刻）
    V = implicit_solve(U + a * (D * lap1d(U, hy, 1) + f(U)), hx, a * D, axis=0)
    # 後半：y と f を陰的に。G(W) = W - a D δy² W - a f(W) - rhs = 0 を Newton 法で
    rhs = V + a * D * lap1d(V, hx, 0)
    W = V.copy()
    ny = U.shape[1]
    s = a * D / hy**2
    for _ in range(newton_iter):
        G = W - a * D * lap1d(W, hy, 1) - a * f(W) - rhs
        # ヤコビ行列 J = I - a D δy² - a diag(f'(W))：y 方向の三重対角、列ごとに対角が違う
        diag = 1 + 2 * s - a * df(W)
        diag[:, 0] -= s
        diag[:, -1] -= s                        # Neumann の端
        lower = np.full_like(W, -s)
        upper = np.full_like(W, -s)
        dW = LU_batched(lower.T, diag.T, upper.T, G.T).T
        W = W - dW
    return W



#ggh
# ---------------- 実験 3：2 次元・臨界半径 ----------------
def run_2d_only_you(f, df, R0, L=60.0, n=150, tau=0.2, T=60.0, save_every=10):
    #fがuにしか依らない(x,y,tには依らない)場合を暫定的に考えた結果。
    h = L / n
    xc = (np.arange(n) + 0.5) * h
    X, Y = np.meshgrid(xc, xc, indexing="ij")
    U = ((X - L / 2) ** 2 + (Y - L / 2) ** 2 < R0**2).astype(float)
    frames, mass, umin = [np.round(U[::2, ::2], 3)], [U.sum() * h * h], [U.min()]
    for k in range(int(T / tau)):
        U = adi_step_only_you(U, tau, h, h, 1.0, f, df)
        mass.append(U.sum() * h * h)
        umin.append(U.min())
        if (k + 1) % save_every == 0:
            frames.append(np.round(U[::2, ::2], 3))   # 表示用に間引いて丸める（ファイルを軽くする）
    return xc[::2], frames, np.array(mass), np.array(umin)



