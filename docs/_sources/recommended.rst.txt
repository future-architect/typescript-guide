おすすめのパッケージ
=============================

ぼちぼち追加

開発ツール
--------------------

cash
~~~~~~~~~~~~~

* npmパッケージ: `cash <https://www.npmjs.com/package/cash>`_
* TypeScript型定義:``@types/cash`` 

UnixシェルコマンドをNode.jsで再実装したもの。WindowsのPowerShellがrmなどのエイリアスを提供してしまっている（しかも ``rm -Force -Recurse`` のようにオプションが違う）が、cashを使うとクロスプラットフォームで動くファイル操作が行える。npm scriptsでも利用できるが、プログラム中からも使えるらしい。

.. todo:: cashにexportがあるので、cross-envはいらないかも？

cross-env
~~~~~~~~~~~~~~~

* npmパッケージ: `cross-env <https://www.npmjs.com/package/cross-env>`_
* TypeScript型定義: CLIツールなので不要

WindowsとLinux/macOSで環境変数変更を統一的に扱えるパッケージ。

typesync
~~~~~~~~~~~~~~~

* npmパッケージ: `typesync <https://www.npmjs.com/package/typesync>`_
* TypeScript型定義: CLIツールなので不要

インストールされているパッケージの型定義パッケージを自動取得してくるCLIツール。

コマンドラインツール
----------------------

convict
~~~~~~~~~~~~~~

* npmパッケージ: `convict <https://www.npmjs.com/package/convict>`_
* TypeScript型定義: ``@types/convict``

コマンドライン引数、設定ファイル、環境変数などを統合的に扱える設定情報管理ライブラリ。型情報付きで設定を管理できるし、設定内容のバリデーションもできる。TypeScriptで使うとさらに便利。

アルゴリズム
------------------

p-map
~~~~~~~~~~~~~~

* npmパッケージ: `p-map <https://www.npmjs.com/package/p-map>`_
* TypeScript型定義: 同梱

並列数を制御しながら多数の仕事を平行で処理できる ``Promise.all()``.