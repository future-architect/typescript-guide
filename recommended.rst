おすすめのパッケージ・ツール
=================================

ぼちぼち追加。まだ実戦投入していないものも多数あります。

TypeScript Playground
-------------------------------

ブラウザでTypeScriptが試せるPlaygroundにも何種類かありますが、現在は公式のPlaygroundが一番おすすめです。以前は本家よりも強力というのを売りにしていたオープンソースのサイトもありました\ [#]_\ が、v2になり、処理系のバージョン設定、細かいビルドオプションの設定など、この別実装にあった機能はすべて本家にも実装されました。また、本書執筆時点ではV3となった最新のPlaygroundが利用できるようになりました。こちらはビルド結果の.d.tsファイルの結果も確認することができ、書いたコードがどのようにTypeScript処理系に解釈されたのかを確認するのも簡単になりました。

* URL: https://www.typescriptlang.org/play/

.. note::

   これらのサイトを使うということは、ソースコードを外部のサービスに送信することになります。実際にこれらのサービスがサーバーにデータを保存はしていないはずですが、普段からの心がけとして、業務で書いた外部公開できないコードを安易に貼り付けるようなことはしないようにしてください。

.. [#] https://typescript-play.js.org

ビルド補助ツール
--------------------

Rush
~~~~~~~~~~~~~~~~~~~~~~

* npmパッケージ: `@microsoft/api-extractor <https://www.npmjs.com/package/@microsoft/rush>`_
* TypeScript型定義: CLIツールなので不要
* URL: https://rushjs.io/

ひとつのGitリポジトリの中に、多数のTypeScriptベースのパッケージを入れて管理するための補助ツール。次のサンプルを見ると、このツールを使った結果がわかります。

https://github.com/microsoft/web-build-tools

* appsフォルダ: ウェブアプリケーションが格納される
* librariesフォルダ: npm installで使うライブラリが格納される
* toolsフォルダ: npm installで使うコマンドラインツールが格納される

API extractor
~~~~~~~~~~~~~~~~~~~~~~

* npmパッケージ: `@microsoft/api-extractor <https://www.npmjs.com/package/@microsoft/api-extractor>`_
* TypeScript型定義: CLIツールなので不要
* URL: https://api-extractor.com/pages/overview/demo_docs/

ドキュメントジェネレータ。パッケージのリファレンスマニュアルが作れる。

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

@microsoft/ts-command-line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* npmパッケージ: `@microsoft/ts-command-line <https://www.npmjs.com/@microsoft/ts-command-line>`_
* TypeScript型定義: 内蔵

TypeScript用のコマンドライン引数ライブラリです。Microsoft社純正。

アルゴリズム関連のライブラリ
-------------------------------------

p-map
~~~~~~~~~~~~~~

* npmパッケージ: `p-map <https://www.npmjs.com/package/p-map>`_
* TypeScript型定義: 同梱

並列数を制御しながら多数の仕事を平行で処理できる ``Promise.all()``.