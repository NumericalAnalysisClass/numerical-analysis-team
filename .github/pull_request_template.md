## 何をしたか

<!-- 例：linalg_direct に Gauss 消去法（部分ピボット付き）を追加 -->

Closes #<!-- Issue の番号 -->

## チェック

- [ ] ファイルの先頭に手法と授業の回、docstring に式と収束の性質を書いた
- [ ] 反復法なら結果に履歴（history）を入れた
- [ ] 実行時の依存は NumPy だけ（SciPy はテストでだけ使う）
- [ ] `tests/test_<モジュール名>.py` にテストを足し、Colab か手元で `pytest` が通った
- [ ] 自分のファイル以外（`__init__.py`・`pyproject.toml`・ほかの人のファイル）は変えていない
