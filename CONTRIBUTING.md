# 参加のしかた

授業（数値解析、全14回）のグループで、モジュールを1人1つずつ分担して書きます。

## はじめての人へ（最初の1回だけ）

1. GitHub のアカウントを作る：https://github.com/signup
2. 作ったアカウント名（ユーザー名）を管理者に伝える
3. 届いた招待メールから `NumericalAnalysisClass` に参加する
   （メールが見つからなければ https://github.com/orgs/NumericalAnalysisClass/invitation を開く）
4. 手元に持ってくる

```
git clone https://github.com/NumericalAnalysisClass/numerical-analysis-team.git
cd numerical-analysis-team
python -m venv .venv
source .venv/bin/activate          # Windows は .venv\Scripts\activate
pip install -e ".[dev]"
pytest                             # 全部通れば準備完了
```

`pip install -e` で入れると、手元のファイルを書き換えた内容がそのまま `import` に反映されます。

## 担当を決める

[Issues](https://github.com/NumericalAnalysisClass/numerical-analysis-team/issues) にモジュールごとの Issue があります。
やりたいものを開いて「やります」とコメントし、右側の Assignees に自分を入れてください。
表にないものを作りたいときは、新しく Issue を立てて相談しましょう。

## 書いて出す流れ

```
git switch main
git pull
git switch -c feat/linalg-direct           # ブランチ名は feat/<モジュール名>
# 書く・テストする
git add src/numerical_analysis_team/linalg/direct.py tests/test_linalg_direct.py
git commit -m "linalg.direct: Gauss 消去法を追加"
git push -u origin feat/linalg-direct
```

push すると表示される URL から Pull Request（PR）を作ります。

- 自動テスト（GitHub Actions）が通ること
- 他のメンバー1人以上が Approve すること

この2つがそろうと main に merge できます。main に直接 push はできません。

## 書き方の約束

- **教科書どおりに素直に書く。** 速さより読みやすさを優先します。
- **1モジュール1ファイル。** 他の人のファイルを触るときは、その人の PR か Issue で相談してから。
- **反復法は履歴を返す。** `roots.RootResult` のように、結果に `history` を入れます。
- **実行時の依存は NumPy だけ。** SciPy は答え合わせのためにテストでだけ使ってかまいません。
- **docstring に授業の何回目か、手法の式、収束の性質を書く。**
- **テストは `tests/test_<モジュール名>.py`。** 解析解か SciPy の結果と比べます。

## モジュールの割り当て（シラバス対応案）

| 授業回 | モジュール | 内容の例 |
|---|---|---|
| 2 | `errors` | 丸め誤差・桁落ち・機械イプシロン |
| 3 | `basics` | Horner 法、級数の打ち切り |
| 4・5 | `linalg.direct` | Gauss 消去、LU 分解、Cholesky 分解 |
| 6・7 | `roots` | 二分法・Newton 法（済）、割線法、はさみうち法 |
| 8・9 | `linalg.iterative` | Jacobi 法、Gauss-Seidel 法、SOR 法、共役勾配法 |
| 10 | `interpolate` | Lagrange 補間、Newton 補間、スプライン |
| 11 | `integrate` | 台形則、Simpson 則、Gauss 求積 |
| 12・13 | `ode` | Euler 法、Runge-Kutta 法 |
| 14 | `eigen` | べき乗法、QR 法 |

## リリース（管理者）

`pyproject.toml` の `version` を上げて main に merge したあと、同じ番号のタグを push すると PyPI に公開されます。

```
git tag v0.1.0
git push origin v0.1.0
```
