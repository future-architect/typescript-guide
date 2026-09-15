# 貢献者向けガイド

Typoなどを見つけた方はPull Requestで報告してくださると助かります。

* 原稿のreSTだけ修正すればOKです。HTML/PDFのビルドまでは不要です。
  HTMLはmasterへのマージ時にGitHub Actionsがビルドして公開します。
* contributors.rstにgithubのアカウント名を掲載させていただきます（不要な場合はお知らせ下さい）。

内容への指摘で、修正の仕方がわからない場合はissueとして報告をお願いします。

## 手元でHTMLを確認する

```
pip install -r requirements.txt
make html
```

`_build/html/index.html` ができます。PDFは `make pdf` ですが、日本語のLaTeX環境が要ります。
