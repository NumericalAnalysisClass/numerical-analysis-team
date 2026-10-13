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

## 作るものを選ぶ

担当の割り振りはしません。作りたいものを自由に選んでください。

- 授業に出てくる手法の一覧は、ピン留めした [📋 授業内容チェックリスト（#11）](https://github.com/NumericalAnalysisClass/numerical-analysis-team/issues/11) にあります。何を作るか迷ったときの目安です。
- 授業の範囲外のテーマも歓迎します（例：[偏微分方程式の差分法 #12](https://github.com/NumericalAnalysisClass/numerical-analysis-team/issues/12)）。
- 作り始めるときは Issue を1つ立て、チェックリストの該当行に Issue 番号を書き添えてください。同じものを2人が作るのを防ぐためです。

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
- **docstring に手法の式と収束の性質を書く。** 授業の手法なら何回目かも。
- **テストは `tests/test_<モジュール名>.py`。** 解析解か SciPy の結果と比べます。

## 置き場所の目安

授業の回ごとにモジュールを分けています。新しいテーマは、Issue で相談して名前を決めてください。

| 授業回 | モジュール |
|---|---|
| 2 | `errors` |
| 3 | `basics` |
| 4・5 | `linalg.direct` |
| 6・7 | `roots` |
| 8・9 | `linalg.iterative` |
| 10 | `interpolate` |
| 11 | `integrate` |
| 12・13 | `ode` |
| 14 | `eigen` |
| 自由テーマ | `pde` など |

## リリース（管理者）

`pyproject.toml` の `version` を上げて main に merge したあと、同じ番号のタグを push すると PyPI に公開されます。

```
git tag v0.1.0
git push origin v0.1.0
```
