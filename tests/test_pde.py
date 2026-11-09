import numpy as np
import pytest

from numerical_analysis_team import pde


def sin_pi(x):
    return np.sin(np.pi * x)


def max_error(res, alpha=1.0):
    return np.max(np.abs(res.u[-1] - pde.heat_exact(res.x, res.t[-1], alpha)))


def test_second_derivative_second_order():
    # sin x の2階微分は -sin x。dx を半分にすると誤差がおよそ 1/4
    errs = []
    for nx in (20, 40):
        x, dx = pde.grid(np.pi, nx)
        errs.append(np.max(np.abs(pde.second_derivative(np.sin(x), dx) + np.sin(x[1:-1]))))
    assert errs[0] / errs[1] == pytest.approx(4, rel=0.01)


def test_thomas_matches_numpy():
    rng = np.random.default_rng(0)
    n = 8
    a, c = rng.normal(size=n - 1), rng.normal(size=n - 1)
    b = 4 + rng.random(n)  # 対角優位
    d = rng.normal(size=n)
    A = np.diag(b) + np.diag(a, -1) + np.diag(c, 1)
    assert pde.thomas(a, b, c, d) == pytest.approx(np.linalg.solve(A, d), abs=1e-12)


def test_thomas_bad_shape():
    with pytest.raises(ValueError):
        pde.thomas([1.0], [2.0, 2.0, 2.0], [1.0, 1.0], [1.0, 1.0, 1.0])


def test_heat_ftcs_exact():
    res = pde.heat_ftcs(sin_pi, nx=50, nt=1000)
    assert res.u.shape == (1001, 51)
    assert max_error(res) < 1e-4


def test_heat_ftcs_second_order_in_space():
    # r = dt / dx² を一定にして dx を半分にすると、誤差 O(dt + dx²) はおよそ 1/4
    e1 = max_error(pde.heat_ftcs(sin_pi, nx=20, nt=500))
    e2 = max_error(pde.heat_ftcs(sin_pi, nx=40, nt=2000))
    assert e1 / e2 == pytest.approx(4, rel=0.02)


def test_heat_ftcs_unstable():
    # r = 0.1 / 200 * 50² = 1.25 > 1/2
    with pytest.raises(ValueError):
        pde.heat_ftcs(sin_pi, nx=50, nt=200)
    # 止めずに計算すると、丸め誤差の高周波成分が増幅されて発散する
    res = pde.heat_ftcs(sin_pi, nx=50, nt=200, check_stability=False)
    assert np.max(np.abs(res.u[-1])) > 1


def test_heat_crank_nicolson_second_order():
    # dt と dx を同時に半分にすると、誤差 O(dt² + dx²) はおよそ 1/4
    e1 = max_error(pde.heat_crank_nicolson(sin_pi, nx=20, nt=20))
    e2 = max_error(pde.heat_crank_nicolson(sin_pi, nx=40, nt=40))
    assert e1 / e2 == pytest.approx(4, rel=0.02)


def test_heat_crank_nicolson_large_r_stable():
    # r = 0.1 / 10 * 50² = 25 でも発散しない
    res = pde.heat_crank_nicolson(sin_pi, nx=50, nt=10)
    assert max_error(res) < 1e-2


def test_heat_steady_state_linear():
    # 境界 u(0)=1, u(1)=3 で十分時間がたつと、定常解 u = 1 + 2x に近づく
    zero = np.zeros_like
    for res in (
        pde.heat_ftcs(zero, T=2.0, nx=20, nt=2000, left=1.0, right=3.0),
        pde.heat_crank_nicolson(zero, T=2.0, nx=20, nt=200, left=1.0, right=3.0),
    ):
        assert res.u[-1] == pytest.approx(1 + 2 * res.x, abs=1e-6)


# ---- 2次元：ADI 法 ----


def sin_sin(X, Y):
    return np.sin(np.pi * X) * np.sin(np.pi * Y)


def max_error_2d(res, alpha=1.0, Lx=1.0, Ly=1.0):
    exact = pde.heat2d_exact(res.x, res.y, res.t[-1], alpha, Lx, Ly)
    return np.max(np.abs(res.u[-1] - exact))


def test_heat2d_adi_shape_and_exact():
    res = pde.heat2d_adi(sin_sin, nx=20, ny=30, nt=40)
    assert res.u.shape == (41, 21, 31)
    assert max_error_2d(res) < 1e-3


def test_heat2d_adi_second_order():
    # dt, dx, dy を同時に半分にすると、誤差 O(dt² + dx² + dy²) はおよそ 1/4
    e1 = max_error_2d(pde.heat2d_adi(sin_sin, nx=16, ny=16, nt=16))
    e2 = max_error_2d(pde.heat2d_adi(sin_sin, nx=32, ny=32, nt=32))
    assert e1 / e2 == pytest.approx(4, rel=0.05)


def test_heat2d_adi_rectangle():
    # 長方形・別のモード・alpha ≠ 1 でも厳密解に合う
    f = lambda X, Y: np.sin(np.pi * X / 2) * np.sin(2 * np.pi * Y)
    res = pde.heat2d_adi(f, alpha=0.5, Lx=2.0, Ly=1.0, T=0.05, nx=40, ny=20, nt=50)
    exact = pde.heat2d_exact(res.x, res.y, 0.05, 0.5, 2.0, 1.0, kx=1, ky=2)
    assert np.max(np.abs(res.u[-1] - exact)) < 1e-2


def test_heat2d_adi_large_r_stable():
    # rx = ry = 0.1 / 5 * 30² = 18 でも発散しない
    res = pde.heat2d_adi(sin_sin, nx=30, ny=30, nt=5)
    assert max_error_2d(res) < 2e-2


def test_heat2d_adi_steady_state():
    # 境界 g = 1 + x + 2y（調和関数）なら、十分時間がたつと u = g に近づく
    g = lambda X, Y: 1 + X + 2 * Y
    res = pde.heat2d_adi(lambda X, Y: np.zeros_like(X), T=2.0, nx=12, ny=12, nt=200, g=g)
    X, Y = np.meshgrid(res.x, res.y, indexing="ij")
    assert res.u[-1] == pytest.approx(g(X, Y), abs=1e-6)
