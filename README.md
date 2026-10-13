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

拡散方程式から始めて、非線形項、分散項と1つずつ足していきます。詳しくは [#12](https://github.com/NumericalAnalysisClass/numerical-analysis-team/issues/12)。

| | 拡散方程式 | 粘性 Burgers 方程式 | KdV 方程式（発展） |
|---|---|---|---|
| 式 | u_t = α u_xx | u_t + u u_x = ν u_xx | u_t + 6u u_x + u_xxx = 0 |
| 特徴 | 線形・放物型 | 非線形項を追加 | 拡散項を分散項に |
| 解き方 | 陽解法、Crank–Nicolson 法 | Cole–Hopf 変換で熱方程式に帰着 | ソリトン解をもつ |
| 検証 | 変数分離解 e^(−απ²t) sin(πx) | 熱方程式の解から作る厳密解 | 1-ソリトン解、保存量 |

どの方程式も厳密解と比べ、格子を細かくしたときの誤差の減り方（収束次数）が理論どおりかを CI で確かめます。

---

## 参加のしかた（ブラウザと Google Colab だけでできます）

**パソコンに Python を入れる必要はありません。** GitHub の画面でファイルを書き、Google Colab で動かして確かめます。

### 1. GitHub のアカウントを作る

1. https://github.com/signup を開く
2. メールアドレス、パスワード、ユーザー名を入れて登録する
3. 届いたメールのコードを入れて確認する

すでにアカウントがある人は、そのアカウントを使ってかまいません。

### 2. testjikuji をフォローする

1. https://github.com/testjikuji を開く
2. 左側の **Follow** ボタンを押す

企画者がフォロワーの一覧からあなたを見つけて、グループ（`NumericalAnalysisClass`）に招待します。**招待が届いたら、フォローは外してかまいません。**

### 3. 招待を承認する

1. GitHub に登録したメールに「invited you to join the NumericalAnalysisClass organization」が届く
2. メールの **Join @NumericalAnalysisClass** を押す

メールが見つからないときは、https://github.com/orgs/NumericalAnalysisClass/invitation を開いても承認できます。

### 4. 作るものを決めて、Issue を立てる

1. [テーマ例](#テーマ例) と [チェックリスト](CHECKLIST.md) を見て、作りたいものを決める
2. このリポジトリの上にある **Issues** を開き、同じテーマの Issue がないかを確かめる
3. **New issue** を押す
4. タイトルに `integrate: 台形則と Simpson 則` のように「モジュール名: 作るもの」を書いて **Create** を押す

Issue は自分で立てます。ほかの人と同じものを作ってしまうのを防ぐためと、自分の作業の記録になるためです。以下では、例として `integrate`（数値積分）を作る流れを説明します。

### 5. GitHub の画面でモジュールのファイルを作る

1. このリポジトリのトップページで **Add file** → **Create new file** を押す
2. ファイル名の欄に `src/numerical_analysis_team/integrate.py` と入れる（`/` を打つとフォルダに区切られます）
3. 本文にコードを書く。たとえば次のようにします。

   ```python
   """数値積分（第11回）。"""

   from typing import Callable


   def trapezoid(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
       """複合台形則。区間 [a, b] を n 等分し、各小区間を台形で近似して足す。

       誤差は刻み h = (b - a) / n の2乗に比例する（2次精度）。
       """
       h = (b - a) / n
       s = (f(a) + f(b)) / 2
       for i in range(1, n):
           s += f(a + i * h)
       return s * h
   ```

4. 右上の **Commit changes...** を押す
5. 出てきた画面で **Create a new branch for this commit and start a pull request** を選び、ブランチ名を `feat/integrate` にして **Propose changes** を押す
6. 次の画面で **Create pull request** を押す（まだ途中でかまいません。Pull Request は後から何度でも書き足せます）

> **ブランチ**は「自分専用の作業場所」です。`main`（みんなが使う本体）を壊さずに作業でき、できあがったら Pull Request で `main` に入れてもらいます。

### 6. テストを書く

テストは「答えが分かっている問題を解かせて、合っているかを確かめるプログラム」です。

1. ページ左上のブランチ切り替えボタン（`main` と書かれたところ）を押し、`feat/integrate` を選ぶ
2. **Add file** → **Create new file** で、`tests/test_integrate.py` を作る

   ```python
   import math

   import pytest

   from numerical_analysis_team import integrate


   def test_trapezoid_sin():
       # ∫_0^π sin x dx = 2
       assert integrate.trapezoid(math.sin, 0, math.pi, n=100) == pytest.approx(2, abs=1e-3)


   def test_trapezoid_second_order():
       # n を2倍にすると、誤差はおよそ 1/4 になる（2次精度）
       e1 = abs(integrate.trapezoid(math.sin, 0, math.pi, n=50) - 2)
       e2 = abs(integrate.trapezoid(math.sin, 0, math.pi, n=100) - 2)
       assert e1 / e2 == pytest.approx(4, rel=0.01)
   ```

3. **Commit changes...** で、今度は **Commit directly to the `feat/integrate` branch** を選んでコミットする

### 7. Google Colab で動かして確かめる

https://colab.research.google.com/ で新しいノートブックを作り、セルに次を書いて実行します。

**自分のブランチを入れて使ってみる**

```python
!pip install -q git+https://github.com/NumericalAnalysisClass/numerical-analysis-team@feat/integrate

import math
from numerical_analysis_team import integrate
integrate.trapezoid(math.sin, 0, math.pi)   # 2 に近い値が出れば OK
```

**テストを実行する**

```python
!git clone -q -b feat/integrate https://github.com/NumericalAnalysisClass/numerical-analysis-team.git
%cd numerical-analysis-team
!pip install -q -e ".[dev]"
!pytest -v
```

すべて `PASSED` になれば成功です。

> GitHub でコードを直したあとは、メニューの **ランタイム → セッションを再起動** をしてから、上のセルをもう一度実行してください。再起動しないと、古いコードが使われたままになります。

### 8. Pull Request をレビューしてもらう

1. リポジトリの **Pull requests** から、自分の Pull Request を開く
2. 説明欄のチェック項目を埋める
3. 下のほうに自動テストの結果が出る。緑の ✓ ならテストが通っています（赤の × のときは **Details** を押すとエラーの内容が見られます）
4. 右側の **Reviewers** でグループのだれか1人を選ぶ
5. レビューで「ここを直して」とコメントが付いたら、同じブランチでファイルを直す（直すと Pull Request にも自動で反映されます）
6. **Approve**（承認）がもらえたら **Merge pull request** を押す

ほかの人の Pull Request のレビューも、ぜひやってみてください。**Files changed** タブでコードを読み、行の横の **+** を押すとコメントを付けられます。

### 9. 公開されたら pip install で確かめる

企画者がリリース（バージョン番号のタグ付け）をすると、GitHub Actions が自動で PyPI に公開します。公開されたら、Colab で確かめましょう。

```python
!pip install -U numerical-analysis-team

from numerical_analysis_team import integrate
```

これで、世界中のだれでもあなたのモジュールを使えるようになります。

---

## 困ったとき

| こんなとき | 原因と対処 |
|---|---|
| ファイルを作ろうとすると「Fork this repository」と出る | まだ招待を承認していません。[手順 3](#3-招待を承認する) をやってください |
| 自動テストが赤い × になる | **Details** を押してエラーを読みます。分からなければ、そのまま Pull Request にコメントで質問してください |
| Colab で直したはずのコードが反映されない | **ランタイム → セッションを再起動** をしてから、もう一度実行します |
| `ModuleNotFoundError` が出る | ファイルの場所が `src/numerical_analysis_team/` の中になっているかを確かめます |
| 何をすればいいか分からない | **Issues** → **New issue** で気軽に質問してください |

書き方の約束（ファイルの分け方、テストの書き方など）は [CONTRIBUTING.md](CONTRIBUTING.md) にまとめています。

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
