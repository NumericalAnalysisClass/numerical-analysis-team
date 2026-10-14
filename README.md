# 自作の数値計算ライブラリを PyPI で公開する

**応用プログラミング　グループワーク企画**　／　企画：[testjikuji](https://github.com/testjikuji)

> 1人1モジュール、最終回までに `pip install numerical-analysis-team` で誰でも使える形へ

この README は、いまは「企画の案内」と「参加の手順」です。最終発表のときに、利用者向けの説明に書き換えます。

---

## やりたいこと

授業で習う数値計算の手法を自分の手で動くプログラムにして、**だれでも `pip install` で使えるライブラリ**として公開します。

```python
!pip install numerical-analysis-team

from numerical_analysis_team import roots   # 非線形方程式（見本・作成済み）
from numerical_analysis_team import pde     # 偏微分方程式（企画者が担当）
from numerical_analysis_team import ...     # ← ここにあなたのモジュールが入ります
```

- **ライブラリは1つ、モジュールは1人1つ。** `numerical-analysis-team` の中に、各自がファイルを1つ足します。
- **申請や登録はいりません。** PyPI の名前はもう取ってあります。
- **テストと公開は自動です。** GitHub Actions が、Pull Request のたびにテストを実行し、リリースのときに PyPI へ公開します。
- **マージしたらすぐ使えます。** 承認待ちはなく、テストが通れば自分でマージでき、その場で Colab から `pip install` できます。
- **中身は自由で、レベルは問いません。** 授業の手法を1つ、教科書どおり素直に書くだけで十分です。

**ねらい**：授業内容を動くソフトウェアにまとめ、他人が使える形で説明できるようになること。

## テーマ例

授業の回に沿った例です。ここにないテーマでもかまいません。手法の細かい一覧は [📋 授業内容チェックリスト](CHECKLIST.md) にあります。

| テーマ例 | モジュール名の例 | 主に使う授業回 |
|---|---|---|
| **1次元偏微分方程式ソルバー（拡散・Burgers・KdV）　← 企画者** | `pde` | 第2、4・5、12・13、14回 |
| 非線形方程式（二分法・Newton 法・割線法） | `roots`（見本あり） | 第6・7回 |
| 反復解法（Jacobi 法・Gauss–Seidel 法・SOR 法・CG 法） | `linalg_iterative` | 第8・9回 |
| 補間（Lagrange 補間・スプライン補間） | `interpolate` | 第10回 |
| 数値積分（台形則・Simpson 則・Gauss 求積） | `integrate` | 第11回 |
| 常微分方程式（Euler 法・Runge–Kutta 法） | `ode` | 第12・13回 |
| 固有値計算（べき乗法・QR 法） | `eigen` | 第14回 |

テーマが重なったら、Issue で相談して調整しましょう。

### 企画者のテーマ：1次元偏微分方程式ソルバー

拡散方程式から始めて、非線形項、分散項と1つずつ足していきます。詳しくは [#1](https://github.com/NumericalAnalysisClass/numerical-analysis-team/issues/1)。

| | 拡散方程式 | 粘性 Burgers 方程式 | KdV 方程式（発展） |
|---|---|---|---|
| 式 | u_t = α u_xx | u_t + u u_x = ν u_xx | u_t + 6u u_x + u_xxx = 0 |
| 特徴 | 線形・放物型 | 非線形項を追加 | 拡散項を分散項に |
| 解き方 | 陽解法、Crank–Nicolson 法 | Cole–Hopf 変換で熱方程式に帰着 | ソリトン解をもつ |
| 検証 | 変数分離解 e^(−απ²t) sin(πx) | 熱方程式の解から作る厳密解 | 1-ソリトン解、保存量 |

どの方程式も厳密解と比べ、格子を細かくしたときの誤差の減り方（収束次数）が理論どおりかを CI で確かめます。

---

## 参加のしかた

**パソコンに Python を入れる必要はありません。** GitHub の画面でコードを書き、Google Colab で動かして確かめます。

1. GitHub のアカウントを作る
2. https://github.com/testjikuji をフォローする（企画者がフォロワーの一覧からあなたを見つけて、グループに招待します）
3. 届いた招待を承認する
4. 作るものを決めて Issue を立て、自分のブランチでモジュールとテストを書く
5. Pull Request を出し、自動テストが通ったら自分でマージする
6. マージした瞬間から、Colab で `pip install` して使える

それぞれの手順は **[📘 開発マニュアル](https://github.com/NumericalAnalysisClass/numerical-analysis-team/blob/main/docs/MANUAL.md)** に、画面の操作から書いてあります。書き方の約束は [CONTRIBUTING.md](https://github.com/NumericalAnalysisClass/numerical-analysis-team/blob/main/CONTRIBUTING.md) にまとめています。

---

## 今使えるもの

| モジュール | 内容 |
|---|---|
| `roots` | 二分法・Newton 法（反復の履歴つき） |

```python
from numerical_analysis_team import roots

r = roots.newton(lambda x: x**2 - 2, lambda x: 2*x, x0=1.0)
r.root        # 1.414213562373095
r.iterations  # 反復回数
r.history     # 各反復の近似値
```
