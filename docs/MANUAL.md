# 開発マニュアル

GitHub のアカウントを作るところから、自分の書いたコードを Google Colab で `pip install` して使えるようになるところまで、この1本で説明します。

**パソコンに Python や Git を入れる必要はありません。** GitHub の画面でコードを書き、Google Colab で動かします。手元の Git を使いたい人は [付録 A](#付録-a手元の-git-で同じことをする) を見てください。

---

## 全体の流れ

```
 最初の1回だけ                    モジュールを作るたびに
┌──────────────┐   ┌──────────────────────────────────────────────────────────────┐
│ 1. アカウント │   │ 3. Issue  →  4. ブランチ  →  5. コード  →  6. テスト            │
│ 2. 招待を承認 │ → │      →  7. Colab で確認  →  8. Pull Request  →  9. 自分でマージ  │
└──────────────┘   │      →  10. すぐ Colab で pip install して使える                  │
                   └──────────────────────────────────────────────────────────────┘
                                         ↓ 企画者がリリースしたとき
                          11. PyPI に公開（pip install numerical-analysis-team で入る）
```

- **レビューの承認は必須ではありません。** 自動テストが通れば、自分で `main` にマージできます。
- **マージした瞬間から、だれでも Colab で使えます**（[手順 10](#10-マージしたらすぐ使う)）。
- PyPI への公開は、企画者がまとめて行います（[手順 11](#11-pypi-への公開リリース)）。

---

## 1. GitHub のアカウントを作る

1. https://github.com/signup を開く
2. メールアドレス、パスワード、ユーザー名を入れて登録する
3. 届いたメールのコードを入れて確認する

すでにアカウントがある人は、それを使ってかまいません。ユーザー名とアイコンはほかのメンバーに見えます。

## 2. グループに参加する

1. https://github.com/testjikuji を開き、左側の **Follow** を押す
   - 企画者がフォロワーの一覧からあなたを見つけて、グループ `NumericalAnalysisClass` に招待します。ユーザー名を伝える必要はありません。
2. 登録したメールに「invited you to join the NumericalAnalysisClass organization」が届いたら、**Join @NumericalAnalysisClass** を押す
   - メールが見つからないときは https://github.com/orgs/NumericalAnalysisClass/invitation を開いても承認できます。
3. 承認が済んだら、フォローは外してかまいません。

これで、リポジトリ https://github.com/NumericalAnalysisClass/numerical-analysis-team にブランチを作ったり、ファイルを書いたりできるようになります。

---

## 3. 作るものを決めて Issue を立てる

1. [README のテーマ例](../README.md#テーマ例) と [授業内容チェックリスト](../CHECKLIST.md) を見て、作りたいものを決める（授業の範囲外でもかまいません）
2. リポジトリ上部の **Issues** を開き、同じテーマの Issue がないかを確かめる
3. **New issue** を押し、タイトルを「モジュール名: 作るもの」の形で書いて **Create** を押す

   ```
   integrate: 台形則と Simpson 則
   ```

**モジュール名**は、英小文字とアンダースコアだけで付けます（例：`integrate`、`ode`、`linalg_direct`）。これがファイル名と `import` の名前になります。

Issue を立てると番号（例：`#5`）が付きます。後で Pull Request に書くので覚えておいてください。

以下では、例として `integrate`（数値積分）を作る流れで説明します。

## 4. 自分のブランチを作る

**ブランチ**は「自分専用の作業場所」です。みんなが使う本体（`main`）を壊さずに書けて、できあがったらマージで `main` に入れます。

1. リポジトリのトップページで、左上の **`main`** と書かれたボタンを押す
2. 入力欄に `feat/integrate` と打つ（`feat/` + モジュール名）
3. **Create branch feat/integrate from main** を押す

ボタンの表示が `feat/integrate` に変わっていれば、いまそのブランチにいます。**以降の作業は、必ずこの表示が自分のブランチになっていることを確かめてから行ってください。**

## 5. モジュールを書く

1. ブランチが `feat/integrate` になっていることを確かめて、**Add file** → **Create new file** を押す
2. ファイル名の欄に `src/numerical_analysis_team/integrate.py` と入れる（`/` を打つとフォルダに区切られます）
3. 本文を書く

   ```python
   """数値積分（第11回）。"""

   from typing import Callable


   def trapezoid(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
       """複合台形則。区間 [a, b] を n 等分し、各小区間を台形で近似して足す。

       T_n = h * (f(a)/2 + f(x_1) + ... + f(x_{n-1}) + f(b)/2),  h = (b - a) / n
       誤差は h の2乗に比例する（2次精度）。
       """
       if n < 1:
           raise ValueError("n は1以上にしてください")
       h = (b - a) / n
       s = (f(a) + f(b)) / 2
       for i in range(1, n):
           s += f(a + i * h)
       return s * h
   ```

4. 右上の **Commit changes...** を押し、**Commit directly to the `feat/integrate` branch** が選ばれていることを確かめて **Commit changes** を押す

### 書き方の約束

| 約束 | 理由・やり方 |
|---|---|
| **教科書どおり素直に書く** | 速さより読みやすさ。ほかの人が読んで授業の復習になるように |
| **ファイルの先頭に、何の手法か・授業の何回目かを書く** | `"""数値積分（第11回）。"""` のように |
| **関数の docstring に、式と収束の性質を書く** | 「2次精度」「1次収束」「条件：f(a) と f(b) が異符号」など |
| **反復法は履歴を返す** | 下の「反復法の書き方」を参照 |
| **使ってよいのは Python 標準と NumPy だけ** | SciPy などはテストの答え合わせにだけ使えます |
| **自分のファイル以外は触らない** | `__init__.py`・`pyproject.toml`・ほかの人のファイルは変えません。変えたいときは Issue で相談 |
| **入力がおかしいときは例外を出す** | `ValueError` などに、日本語で理由を書く |

`__init__.py` に足さなくても、`from numerical_analysis_team import integrate` で使えます。

### 反復法の書き方

反復で答えに近づく手法（Newton 法、Jacobi 法、べき乗法など）は、最終的な答えだけでなく**途中の近似値の列**も返します。収束の様子をグラフにしたり、テストで収束次数を確かめたりできるからです。見本は [`roots.py`](../src/numerical_analysis_team/roots.py) です。

```python
from dataclasses import dataclass, field


@dataclass
class RootResult:
    """解法の結果。history に各反復の近似値が入る。"""

    root: float          # 答え
    iterations: int      # 反復回数
    converged: bool      # 収束したか（max_iter で打ち切ったら False）
    history: list[float] = field(default_factory=list)   # 各反復の近似値
```

自分のモジュール用に `〇〇Result` を作ってかまいません。止める条件（`tol`）と最大回数（`max_iter`）は引数にして、既定値を付けます。

## 6. テストを書く

**テスト**は「答えが分かっている問題を解かせて、合っているかを確かめるプログラム」です。Pull Request を出すと、GitHub が Python 3.10〜3.13 の4つで自動的に実行します。

1. ブランチが `feat/integrate` のまま、**Add file** → **Create new file** で `tests/test_integrate.py` を作る

   ```python
   import math

   import pytest

   from numerical_analysis_team import integrate


   def test_trapezoid_sin():
       # 厳密解：∫_0^π sin x dx = 2
       assert integrate.trapezoid(math.sin, 0, math.pi, n=100) == pytest.approx(2, abs=1e-3)


   def test_trapezoid_second_order():
       # n を2倍にすると誤差がおよそ 1/4 になる（2次精度）
       e1 = abs(integrate.trapezoid(math.sin, 0, math.pi, n=50) - 2)
       e2 = abs(integrate.trapezoid(math.sin, 0, math.pi, n=100) - 2)
       assert e1 / e2 == pytest.approx(4, rel=0.01)


   def test_trapezoid_bad_n():
       with pytest.raises(ValueError):
           integrate.trapezoid(math.sin, 0, 1, n=0)
   ```

2. **Commit changes...** → **Commit directly to the `feat/integrate` branch** でコミットする

### 何を確かめるか

関数ごとに、次の3種類を1つずつ書けば十分です。

| 種類 | 例 |
|---|---|
| **厳密解と合うか** | ∫ sin、√2、解析解が分かる微分方程式など。`pytest.approx(期待値, abs=許容誤差)` で比べる |
| **収束の速さが理論どおりか** | 刻みを半分にすると誤差が 1/4（2次精度）、Newton 法の誤差が2乗で減る、など |
| **おかしな入力でエラーになるか** | `with pytest.raises(ValueError):` |

小数は丸め誤差があるので、`==` ではなく `pytest.approx` で比べます。

## 7. Colab で動かして確かめる

https://colab.research.google.com/ を開き、**ノートブックを新規作成** します。

**自分のブランチを入れて使ってみる**（ブランチ名は自分のものに）

```python
!pip install -q --force-reinstall --no-deps git+https://github.com/NumericalAnalysisClass/numerical-analysis-team@feat/integrate

import math
from numerical_analysis_team import integrate
integrate.trapezoid(math.sin, 0, math.pi)   # 2 に近い値が出れば OK
```

**テストを全部実行する**

```python
!rm -rf numerical-analysis-team
!git clone -q -b feat/integrate https://github.com/NumericalAnalysisClass/numerical-analysis-team.git
%cd numerical-analysis-team
!pip install -q -e ".[dev]"
!pytest -v
%cd ..
```

すべて `PASSED` になれば成功です。`FAILED` が出たら、その下に出る `assert` の行と値を読んで直します。

> **GitHub でコードを直したあとは、メニューの「ランタイム」→「セッションを再起動」をしてから、上のセルをもう一度実行してください。** 再起動しないと、一度 `import` した古いコードが使われ続けます。
>
> `--force-reinstall` は「同じ版番号でも入れ直す」という指定です。付けないと、2回目以降は古いコードのままになります。

## 8. Pull Request を出す

**Pull Request（PR）**は「自分のブランチを `main` に入れてください」という申し込みです。

1. リポジトリのトップページに黄色い帯で **Compare & pull request** が出ていれば押す
   - 出ていなければ **Pull requests** → **New pull request** を押し、`compare:` を `feat/integrate` にする
2. タイトルを書く（例：`integrate: 台形則を追加`）
3. 説明欄の `Closes #` の後ろに、手順 3 の Issue 番号を書く（例：`Closes #5`）。マージしたときにその Issue が自動で閉じます
4. チェック項目を確かめて `[ ]` を `[x]` にする
5. **Create pull request** を押す

まだ途中でも PR を出してかまいません。ブランチにコミットを足すと、PR にも自動で反映されます。

### 自動テストの結果を見る

PR の画面の下のほうに、自動テストの結果が4行（`pytest (3.10)` 〜 `pytest (3.13)`）出ます。

- 黄色い ● は実行中です。1分ほど待ちます。
- **緑の ✓ が4つそろえば合格**です。
- **赤い ×** が出たら **Details** を押します。ログの下のほうの `FAILED` や `Error` の行に原因が書いてあります。直してコミットすれば、自動でもう一度実行されます。

分からなければ、PR にそのままコメントで質問してください。

### レビュー（任意・おすすめ）

承認がなくてもマージできますが、だれかに読んでもらうと間違いに気づけます。

- 頼むとき：PR 右側の **Reviewers** でメンバーを選ぶ
- 読むとき：ほかの人の PR の **Files changed** タブでコードを読み、行の横の **+** でコメントする。良ければ **Review changes** → **Approve**

## 9. 自分でマージする

緑の ✓ が4つそろったら、PR の一番下の **Merge pull request** → **Confirm merge** を押します。続けて **Delete branch** を押して、使い終わったブランチを消します。

これで、あなたのコードが `main` に入りました。

- テストが通っていないと、マージボタンは押せません。
- 「This branch has conflicts」と出たら [困ったとき](#困ったとき) を見てください。

## 10. マージしたらすぐ使う

マージした瞬間から、だれでも Colab で次のように使えます。

```python
!pip install -q --force-reinstall --no-deps git+https://github.com/NumericalAnalysisClass/numerical-analysis-team

from numerical_analysis_team import integrate
integrate.trapezoid(lambda x: x**2, 0, 1)
```

`@ブランチ名` を付けないと `main`（みんなのマージ済みのコード）が入ります。グループのほかの人にも、このセルを渡せば使ってもらえます。

## 11. PyPI への公開（リリース）

`main` に十分たまったら、企画者がバージョン番号を上げて PyPI に公開します。公開されると、ブランチや GitHub の URL を指定しなくても入るようになります。

```python
!pip install -U numerical-analysis-team
```

- 公開できるのは、企画者が承認した人（`publishers` チームのメンバー）だけです。`v0.1.0` のような `v` で始まるタグを打つと自動で公開されますが、ほかの人はこのタグを作れないようになっています。
- 公開してほしいタイミングがあれば、Issue で声をかけてください。

---

## 続きを書く・直すとき

**マージした後に続きを書くときは、新しいブランチを `main` から作り直します。** 古いブランチに書き足すと、ほかの人のマージ分が入っていないため、ずれが生じやすくなります。

1. 手順 4 と同じく、`main` を選んだ状態から `feat/integrate-simpson` のような新しいブランチを作る
2. 既存のファイルを直すときは、ファイルを開いて右上の鉛筆マーク（**Edit this file**）を押す
3. あとは手順 6〜10 と同じ

---

## 困ったとき

| こんなとき | 原因と対処 |
|---|---|
| ファイルを作ろうとすると「Fork this repository」と出る | まだ招待を承認していないか、ブランチを作れる権限がまだありません。手順 2 を確かめ、それでも出るときは Issue で知らせてください |
| 「You're making changes in a project you don't have write access to」と出る | 同上 |
| 自動テストが赤い × になる | **Details** を押してログを読みます。`ModuleNotFoundError` ならファイルの場所、`AssertionError` なら計算結果を確かめます |
| Colab で直したはずのコードが反映されない | 「ランタイム」→「セッションを再起動」をしてから、`--force-reinstall` 付きでもう一度入れます |
| `ModuleNotFoundError: No module named 'numerical_analysis_team.integrate'` | ファイルが `src/numerical_analysis_team/` の中にあるか、ブランチ名が合っているかを確かめます |
| PR に「This branch has conflicts that must be resolved」と出る | 同じファイルの同じ場所を、ほかの人も変えています。**Resolve conflicts** を押すと、`<<<<<<<` と `>>>>>>>` で囲まれた食い違う部分が出るので、残したい形に書き直して、印の行を消し、**Mark as resolved** → **Commit merge** を押します。分からなければ PR にコメントで助けを求めてください |
| `main` に間違ったコードを入れてしまった | マージ済みの PR の画面の **Revert** を押すと、その変更を取り消す PR ができます。それをマージします |
| 何をすればいいか分からない | **Issues** → **New issue** で気軽に質問してください |

---

## 付録 A：手元の Git で同じことをする

パソコンに Python（3.10 以上）と Git が入っている人向けです。手順 3（Issue）と 8〜11（PR からあと）は同じで、4〜7 が次のように変わります。

**最初の1回**

```bash
git clone https://github.com/NumericalAnalysisClass/numerical-analysis-team.git
cd numerical-analysis-team
python -m venv .venv
source .venv/bin/activate          # Windows は .venv\Scripts\activate
pip install -e ".[dev]"
pytest                             # 全部通れば準備完了
```

`pip install -e` で入れると、ファイルを書き換えた内容がそのまま `import` に反映されます。

push のときに GitHub へのログインを求められます。[GitHub CLI](https://cli.github.com/) を入れて `gh auth login` を一度実行しておくのが簡単です。

**モジュールを作るたびに**

```bash
git switch main
git pull                                   # ほかの人のマージ分を取り込む
git switch -c feat/integrate               # 手順 4：ブランチを作る
# 手順 5・6：src/numerical_analysis_team/integrate.py と tests/test_integrate.py を書く
pytest                                     # 手順 7：手元でテスト
git add src/numerical_analysis_team/integrate.py tests/test_integrate.py
git commit -m "integrate: 台形則を追加"
git push -u origin feat/integrate
```

push すると表示される URL を開くと、手順 8 の PR 作成画面になります。

コミットに載るメールアドレスは公開されます。気になる人は、GitHub の **Settings** → **Emails** で **Keep my email addresses private** をオンにし、そこに出る `…@users.noreply.github.com` を `git config user.email` に設定してください。

## 付録 B：用語

| 用語 | 意味 |
|---|---|
| リポジトリ | コード一式と、その変更の記録を置く場所 |
| `main` | みんなが使う本体のブランチ |
| ブランチ | `main` から分かれた自分専用の作業場所 |
| コミット | 変更をひとまとまりにして記録すること |
| Pull Request（PR） | 自分のブランチを `main` に入れる申し込み。ここでテストとレビューが行われる |
| マージ | PR の変更を `main` に入れること |
| Issue | やること・相談・質問を書く掲示板の1件 |
| GitHub Actions / CI | PR のたびに自動でテストを実行する仕組み |
| PyPI | Python のパッケージの公開場所。`pip install` はここから入れる |
| リリース | バージョン番号を付けて PyPI に公開すること |
