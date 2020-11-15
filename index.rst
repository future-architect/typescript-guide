.. 今どきのJavaScriptの書き方 documentation master file, created by
   sphinx-quickstart on Thu Dec 13 19:41:54 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

仕事ですぐに使えるTypeScript
======================================================

.. note::

   本ドキュメントは、まだ未完成ですが、ウェブフロントエンドの開発を学ぶときに、JavaScriptを経由せずに、最初からTypeScriptで学んでいく社内向けコンテンツとして作成されはじめました。基本の文法部分以外はまだ執筆されていない章もいくつもあります。書かれている章もまだまだ内容が追加される可能性がありますし、環境の変化で内容の変更が入る可能性もあります。

   書籍の原稿はGitHub上で管理しております。もしTypoを見つけてくださった方がいらっしゃいましたら、 `GitHub上で連絡 <https://github.com/future-architect/typescript-guide/pulls>`_ をお願いします [#]_ 。reSTファイルだけ修正してもらえれば、HTML/PDFの生成までは不要です。フィードバックなども歓迎しております。

   .. [#] https://github.com/future-architect/typescript-guide/pulls

.. raw:: html

   <p><a href="./typescript-guide.pdf">PDF版をダウンロード</a></p>

.. toctree::
   :maxdepth: 2
   :caption: TypeScriptの世界を知る

   preface
   ecosystem

.. toctree::
   :maxdepth: 2
   :caption: TypeScriptの書き方

   variable
   primitive
   complex
   syntax
   typing
   function
   otherbuiltinobjects
   class
   async
   exception
   module
   console

.. toctree::
   :maxdepth: 2
   :caption: 中級のテクニック

   generics
   functional
   class2
   reactive
   advance

.. toctree::
   :maxdepth: 2
   :caption: 環境ごとのTips（共通環境・ブラウザ以外）

   prodenv
   baseenv
   libenv
   clienv
   ci
   deploy
   version

.. toctree::
   :maxdepth: 2
   :caption: 環境ごとのTips（ブラウザ環境）

   browserobjects
   react
   vue
   webpercel
   electron

.. toctree::
   :maxdepth: 2
   :caption: Appendix

   recommended
   contributors

.. todolist::

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
