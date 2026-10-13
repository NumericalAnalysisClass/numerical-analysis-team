import math

import pytest

from numerical_analysis_team import roots


def test_bisection_sqrt2():
    r = roots.bisection(lambda x: x**2 - 2, 0, 2)
    assert r.converged
    assert r.root == pytest.approx(math.sqrt(2), abs=1e-12)


def test_bisection_halves_interval():
    # 区間幅 2 を tol 以下まで半分にする回数
    tol = 1e-6
    r = roots.bisection(lambda x: x**2 - 2, 0, 2, tol=tol)
    assert r.iterations == math.ceil(math.log2(2 / tol))


def test_bisection_same_sign_raises():
    with pytest.raises(ValueError):
        roots.bisection(lambda x: x**2 + 1, -1, 1)


def test_newton_sqrt2():
    r = roots.newton(lambda x: x**2 - 2, lambda x: 2 * x, x0=1.0)
    assert r.converged
    assert r.root == pytest.approx(math.sqrt(2), rel=1e-15)


def test_newton_quadratic_convergence():
    # f(x) = x^2 - 2 では e_{k+1} = e_k^2 / (2 x_k) が厳密に成り立つ（2次収束）
    s = math.sqrt(2)
    r = roots.newton(lambda x: x**2 - 2, lambda x: 2 * x, x0=1.0)
    x = r.history
    for k in range(3):
        assert abs(x[k + 1] - s) == pytest.approx((x[k] - s) ** 2 / (2 * x[k]), rel=1e-9)


def test_newton_cos():
    r = roots.newton(lambda x: math.cos(x) - x, lambda x: -math.sin(x) - 1, x0=1.0)
    assert r.root == pytest.approx(0.7390851332151607, abs=1e-14)
