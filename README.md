# numerical-analysis-team

数値解析の授業用ライブラリ。教科書のアルゴリズムをそのまま書き、反復の途中経過（履歴）を返します。

```
pip install numerical-analysis-team
```

```python
import numerical_analysis_team as na

r = na.roots.newton(lambda x: x**2 - 2, lambda x: 2*x, x0=1.0)
r.root        # 1.4142135623730951
r.iterations  # 反復回数
r.history     # 各反復の近似値
```

## 収録状況

| 授業回 | モジュール | 状況 |
|---|---|---|
| 第6・7回 非線形方程式 | `roots` | 二分法・Newton法 |
