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
