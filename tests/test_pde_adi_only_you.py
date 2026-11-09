"""2次元の反応拡散方程式 u_t = D Δu + f(u)（ADI 法＋Newton 法、f は u だけの関数）のテスト。

pytest で実行するとテストだけが動く。
`python tests/test_pde_adi_only_you.py` で直接実行すると、plotly でアニメーションを表示する。
"""

import numpy as np
import pytest

from numerical_analysis_team import pde

# テスト用の小さな格子（数秒もかからない）
SMALL = dict(L=20.0, n=40, tau=0.2, T=2.0, save_every=5)


def zero_reaction():
    return (lambda u: 0 * u), (lambda u: 0 * u)


def constant_source(q):
    return (lambda u: 0 * u + q), (lambda u: 0 * u)


# ---- テスト ----


def test_run_2d_only_you_shapes():
    xc, frames, mass, umin = pde.run_2d_only_you(*zero_reaction(), 3.0, **SMALL)
    nsteps = int(SMALL["T"] / SMALL["tau"])
    assert len(xc) == SMALL["n"] // 2  # 表示用に1つおきに間引いている
    assert len(frames) == 1 + nsteps // SMALL["save_every"]
    assert frames[0].shape == (len(xc), len(xc))
    assert mass.shape == umin.shape == (nsteps + 1,)


def test_mass_conserved_without_reaction():
    # f = 0 なら、Neumann 境界なので総量 ∫u dxdy は保存される
    _, _, mass, _ = pde.run_2d_only_you(*zero_reaction(), 3.0, **SMALL)
    assert mass == pytest.approx(mass[0], rel=1e-12)


def test_constant_source_mass_gain():
    # f = q（定数の熱源）なら、総量は q × 面積 × 時間 だけ増える
    q = 0.5
    _, _, mass, _ = pde.run_2d_only_you(*constant_source(q), 3.0, **SMALL)
    assert mass[-1] - mass[0] == pytest.approx(q * SMALL["L"] ** 2 * SMALL["T"], rel=1e-10)


@pytest.mark.parametrize("reaction", [pde.kpp(), pde.bistable(0.3)], ids=["kpp", "bistable"])
def test_stays_in_0_1(reaction):
    # (τ/2)·max|f'| が小さければ、解は 0 ≤ u ≤ 1 にとどまる
    _, frames, _, umin = pde.run_2d_only_you(*reaction, 3.0, **SMALL)
    assert umin.min() >= -1e-12
    assert max(F.max() for F in frames) <= 1 + 1e-12


def test_kpp_mass_increases():
    # KPP 型では 0 < u < 1 で f(u) > 0 なので、総量は減らない
    _, _, mass, _ = pde.run_2d_only_you(*pde.kpp(), 3.0, **SMALL)
    assert np.all(np.diff(mass) >= -1e-12)


# ---- 表示用（pytest では実行されない） ----


def surface_animation(x, y, frames, times, title="", zlabel="u", xlabel="x", ylabel="y",
                      max_points=80, zrange=None, colorscale="Viridis", duration=80, aspect_z=0.5):
    """frames[k] は形 (len(x), len(y)) の配列（frames[k][i, j] が (x_i, y_j) での値）。

    max_points：表示用に各方向をこの点数まで間引く（ブラウザを軽くするため）。
    """
    import plotly.graph_objects as go

    sx = max(1, len(x) // max_points)
    sy = max(1, len(y) // max_points)
    xs, ys = np.asarray(x)[::sx], np.asarray(y)[::sy]
    Z = [np.round(np.asarray(F)[::sx, ::sy].T, 4) for F in frames]   # Surface は z[行=y, 列=x]
    if zrange is None:
        zrange = (min(float(z.min()) for z in Z), max(float(z.max()) for z in Z))
    kw = dict(x=xs, y=ys, colorscale=colorscale, cmin=zrange[0], cmax=zrange[1], showscale=True)
    fig = go.Figure(
        data=[go.Surface(z=Z[0], **kw)],
        frames=[go.Frame(data=[go.Surface(z=z, **kw)], name=f"{t:.3g}") for z, t in zip(Z, times)],
    )
    fig.update_layout(
        title=title, height=650, uirevision="keep",
        scene=dict(xaxis_title=xlabel, yaxis_title=ylabel, zaxis_title=zlabel,
                   zaxis=dict(range=list(zrange)),
                   aspectmode="manual", aspectratio=dict(x=1, y=1, z=aspect_z)),   # 底面は正方形に（S と v のように単位が違っても見やすい）
        updatemenus=[dict(type="buttons", x=0.05, y=0.02, xanchor="left", yanchor="bottom", buttons=[
            dict(label="▶", method="animate",
                 args=[None, dict(frame=dict(duration=duration, redraw=True), fromcurrent=True,
                                  transition=dict(duration=0))]),
            dict(label="❚❚", method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])])],
        sliders=[dict(x=0.15, y=0.0, len=0.8, currentvalue=dict(prefix="t = "),
                      steps=[dict(label=fr.name, method="animate",
                                  args=[[fr.name], dict(mode="immediate", frame=dict(duration=0, redraw=True))])
                             for fr in fig.frames])],
    )
    return fig


def save_animation(xc, frames, tau, save_every, path, title):
    import plotly.graph_objects as go

    fig = go.Figure(
        data=[go.Heatmap(z=frames[0].T, x=xc, y=xc, zmin=0, zmax=1, colorscale="Viridis")],
        frames=[go.Frame(data=[go.Heatmap(z=F.T, x=xc, y=xc, zmin=0, zmax=1, colorscale="Viridis")],
                         name=f"{k * tau * save_every:.1f}") for k, F in enumerate(frames)],
    )
    fig.update_layout(
        title=title, width=620, height=640, yaxis=dict(scaleanchor="x"),
        updatemenus=[dict(type="buttons", x=0.05, y=-0.05, xanchor="left", buttons=[
            dict(label="▶", method="animate", args=[None, dict(frame=dict(duration=80, redraw=True), fromcurrent=True)]),
            dict(label="❚❚", method="animate", args=[[None], dict(frame=dict(duration=0), mode="immediate")])])],
        sliders=[dict(x=0.15, y=-0.05, len=0.8, currentvalue=dict(prefix="t = "),
                      steps=[dict(label=fr.name, method="animate",
                                  args=[[fr.name], dict(mode="immediate", frame=dict(duration=0, redraw=True))])
                             for fr in fig.frames])],
    )
    return fig


if __name__ == "__main__":
    f, df = pde.bistable(0.3)
    xc, frames, mass, umin = pde.run_2d_only_you(f, df, 5.0, T=60.0)
    times = [k * 0.2 * 10 for k in range(len(frames))]
    surface_animation(xc, xc, frames, times, "双安定型（θ=0.3）の侵入 u(x, y, t)", zrange=(0, 1.05), aspect_z=0.35).show()
