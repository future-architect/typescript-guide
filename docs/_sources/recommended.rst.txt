おすすめのパッケージ・ツール
=================================

ぼちぼち追加

TypeScript Playgournd各種
-------------------------------

ブラウザでTypeScriptが試せるPlaygroundにも何種類かあります。

.. note::

   これらのサイトを使うということは、ソースコードを外部のサービスに送信することになります。実際にこれらのサービスがサーバーにデータを保存はしていないはずですが、普段からの心がけとして、業務で書いた外部公開できないコードを安易に貼り付けるようなことはしないようにしてください。

標準のPlayground
~~~~~~~~~~~~~~~~~~~

* URL: https://www.typescriptlang.org/play/

TypeScriptの公式サイトが提供するPlaygroundです。エラーチェックの厳格さのオプションの設定はできます。
共有もできますが、URLのクエリーにすべてのソースコードを詰め込むストロングスタイルです。

https://typescript-play.js.org/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* URL: https://typescript-play.js.org/

標準のPlaygroundよりも少し高機能なPlaygroundです。
TypeScriptのコンパイラのバージョンを切り替えたり、標準よりも多くのオプションが設定できます。
特に、出力先ターゲットの変更は検証には便利です。

共有ボタンはありませんが、入力するたびにURLが変更され、共有が行えます。

ビルド補助ツール
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

コマンドラインツール用ライブラリ
---------------------------------------

convict
~~~~~~~~~~~~~~

* npmパッケージ: `convict <https://www.npmjs.com/package/convict>`_
* TypeScript型定義: ``@types/convict``

コマンドライン引数、設定ファイル、環境変数などを統合的に扱える設定情報管理ライブラリ。型情報付きで設定を管理できるし、設定内容のバリデーションもできる。TypeScriptで使うとさらに便利。

アルゴリズム関連のライブラリ
-------------------------------------

p-map
~~~~~~~~~~~~~~

* npmパッケージ: `p-map <https://www.npmjs.com/package/p-map>`_
* TypeScript型定義: 同梱

並列数を制御しながら多数の仕事を平行で処理できる ``Promise.all()``.