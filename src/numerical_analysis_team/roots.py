"""非線形方程式 f(x) = 0 の解法（第6・7回）。"""

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class RootResult:
    """解法の結果。history に各反復の近似値が入る。"""

    root: float
    iterations: int
    converged: bool
    history: list[float] = field(default_factory=list)


def bisection(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-12,
    max_iter: int = 200,
) -> RootResult:
    """二分法。f(a) と f(b) が異符号であること。

    区間 [a, b] を毎回半分にし、符号が変わる側を残す。
    区間幅が tol 以下になったら止める（1次収束、誤差は毎回 1/2）。
    """
    fa, fb = f(a), f(b)
    if fa == 0:
        return RootResult(a, 0, True, [a])
    if fb == 0:
        return RootResult(b, 0, True, [b])
    if fa * fb > 0:
        raise ValueError("f(a) と f(b) が同符号です")

    history = []
    for k in range(1, max_iter + 1):
        c = (a + b) / 2
        history.append(c)
        fc = f(c)
        if fc == 0 or (b - a) / 2 <= tol:
            return RootResult(c, k, True, history)
        if fa * fc < 0:
            b = c
        else:
            a, fa = c, fc
    return RootResult(c, max_iter, False, history)


def newton(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    tol: float = 1e-12,
    max_iter: int = 50,
) -> RootResult:
    """Newton 法  x_{k+1} = x_k - f(x_k) / f'(x_k)。

    単根の近くから始めれば2次収束。|x_{k+1} - x_k| が tol 以下で止める。
    """
    x = x0
    history = [x]
    for k in range(1, max_iter + 1):
        d = df(x)
        if d == 0:
            raise ZeroDivisionError(f"f'(x) = 0 になりました (x = {x})")
        x_new = x - f(x) / d
        history.append(x_new)
        if abs(x_new - x) <= tol:
            return RootResult(x_new, k, True, history)
        x = x_new
    return RootResult(x, max_iter, False, history)
