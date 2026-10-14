# 参加のしかた

授業（数値解析）のグループで、1人1つずつモジュールを書いて、1つのライブラリにまとめます。

**手順は [📘 開発マニュアル](docs/MANUAL.md) にすべて書いてあります。** GitHub のアカウント作成から、Colab で `pip install` して使えるようになるまでを、画面の操作から説明しています。ここには、書くときの約束だけをまとめます。

## 流れ（要約）

1. https://github.com/testjikuji をフォローし、届いた招待を承認する
2. [Issues](https://github.com/NumericalAnalysisClass/numerical-analysis-team/issues) で同じテーマがないかを確かめて、**自分で** Issue を立てる（タイトルは「モジュール名: 作るもの」）
3. `main` から `feat/<モジュール名>` のブランチを作り、モジュールとテストを書く
4. Pull Request を出す。自動テスト（Python 3.10〜3.13）が4つとも通れば、**自分でマージできます**（承認は必須ではありません。レビューを頼むのは歓迎）
5. マージしたら、すぐ Colab で使えます

   ```python
   !pip install -q --force-reinstall --no-deps git+https://github.com/NumericalAnalysisClass/numerical-analysis-team
   ```

`main` には直接 push できません。必ず Pull Request を通します。

## 書き方の約束

- **教科書どおりに素直に書く。** 速さより読みやすさを優先します。
- **1モジュール1ファイル。** `src/numerical_analysis_team/<モジュール名>.py`。モジュール名は英小文字とアンダースコアだけ（例：`integrate`、`linalg_direct`）。
- **自分のファイル以外は触らない。** `__init__.py`・`pyproject.toml`・ほかの人のファイルを変えたいときは、Issue で相談してから。`__init__.py` に足さなくても `from numerical_analysis_team import <モジュール名>` で使えます。
- **ファイルの先頭に手法の名前と授業の回、関数の docstring に式と収束の性質を書く。**
- **反復法は履歴を返す。** `roots.RootResult` のように、結果に `history`（各反復の近似値）を入れます。
- **実行時に使えるのは Python 標準と NumPy だけ。** SciPy は答え合わせのためにテストでだけ使えます。
- **テストは `tests/test_<モジュール名>.py`。** 「厳密解と合うか」「収束の速さが理論どおりか」「おかしな入力でエラーになるか」を確かめます。

## リリース（企画者）

PyPI への公開は、`publishers` チームのメンバーだけができます。

1. `pyproject.toml` の `version` と `src/numerical_analysis_team/__init__.py` の `__version__` を上げる PR をマージする
2. 同じ番号のタグを打って push する

```
git switch main && git pull
git tag v0.1.0
git push origin v0.1.0
```

GitHub Actions がテスト・ビルドのあと PyPI に公開します。`v` で始まるタグは `publishers` 以外には作れません。
