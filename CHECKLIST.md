# 授業内容チェックリスト

授業（数値解析、全14回）に出てくる手法の一覧です。**割り当てではありません。** 何を作るか迷ったときの目安にしてください。✅ は作成済みです。

作るものが決まったら、[Issues](https://github.com/NumericalAnalysisClass/numerical-analysis-team/issues) で同じテーマがないかを確かめてから、自分で Issue を立ててください。

## 第2回 誤差 — `errors`
- 機械イプシロンの計算
- 絶対誤差・相対誤差
- 桁落ちの例と回避（2次方程式の解の公式など）

## 第3回 基本的な計算 — `basics`
- Horner 法
- Taylor 級数の打ち切りと誤差
- Kahan の補正付き総和

## 第4・5回 連立一次方程式（直接法） — `linalg.direct`
- Gauss 消去法（部分ピボット付き）
- 前進代入・後退代入
- LU 分解
- Cholesky 分解
- 条件数

## 第6・7回 非線形方程式 — `roots`
- ✅ 二分法
- ✅ Newton 法
- 割線法
- はさみうち法（regula falsi）
- 不動点反復
- 多変数の Newton 法

## 第8・9回 連立一次方程式（反復法） — `linalg.iterative`
- Jacobi 法
- Gauss-Seidel 法
- SOR 法
- 共役勾配法（CG 法）

## 第10回 補間 — `interpolate`
- Lagrange 補間
- Newton の差分商補間
- 3次スプライン補間
- Runge 現象の例

## 第11回 数値積分 — `integrate`
- 複合台形則
- 複合 Simpson 則
- Romberg 積分
- Gauss-Legendre 求積

## 第12・13回 常微分方程式 — `ode`
- 前進 Euler 法
- 後退 Euler 法
- Heun 法（2次 Runge-Kutta 法）
- 古典的 4次 Runge-Kutta 法
- 連立・高階の常微分方程式への適用

## 第14回 固有値問題 — `eigen`
- べき乗法
- 逆べき乗法
- Jacobi 法（対称行列）
- QR 法

## 授業の範囲外・自由テーマ
- 1次元偏微分方程式ソルバー（拡散・Burgers・KdV） — `pde`（企画者）
- ここにないテーマも歓迎です
