CLIツール作成のための環境設定
=========================================

TypeScriptを使ってNode.jsのためのCLIツールを作成するための環境構築方法を紹介していきます。

作業フォルダを作る
------------------------

ライブラリの時は、ES2015 modulesとCommonJSの2通り準備しましたが、CLIの場合はNode.jsだけ動かせば良いので、出力先もCommonJSだけで十分です。

.. code-block:: bash

   $ mkdir dist   # commonJSだけなので1つだけ

 ``.gitignore`` も、出力先フォルダを1つだけに修正しましょう。

ビルド設定
---------------------------

Node.jsの機能を使うことになるため、Node.jsのAPIの型定義ファイルは入れておきましょう。

コマンドラインで良く使うであろうライブラリを追加しておきます。
カラーでのコンソール出力、コマンドライン引数のパーサ、ヘルプメッセージ表示です。

どれもTypeScriptの型定義があるので、これも落としておきます。
また、ソースマップサポートを入れると、エラーの行番号がソースのTypeScriptの行番号で表示されるようになって便利なので、これも入れておきます。

.. code-block:: bash

   $ npm install --save cli-color command-line-args
      command-line-usage source-map-support
   $ npm install --save-dev @types/node @types/cli-color
      @types/command-line-args @types/command-line-usage
      @types/source-map-support

TypeScriptのビルド設定のポイントは、ブラウザからは使わないので、ターゲットのバージョンを高くできる点にあります。
ローカルでは安定版を使ったとしてもNode.js 10が使えるでしょう。

ライブラリのときとは異なり、成果物を利用するのはNode.jsの処理系だけなので、.d.tsファイルを生成する必要はありません。

.. code-block:: json
   :caption: tsconfig.json

   {
     "compilerOptions": {
       "target": "es2018",        // お好みで変更
       "declaration": false,      // 生成したものを他から使うことはないのでfalseに
       "declarationMap": false,   // 同上
       "sourceMap": true,         // 
       "strict": true,
       "noUnusedLocals": true,
       "noUnusedParameters": true,
       "noImplicitReturns": true,
       "noFallthroughCasesInSwitch": true,
       "esModuleInterop": true,
       "experimentalDecorators": true,
       "emitDecoratorMetadata": true,
       "module": "commonjs",      // Node.jsで使うため
       "outDir": "./dist"         // 出力先を設定
     },
     "include": ["src/**/*"]
   }

``package.json`` 設定時は、他のパッケージから利用されることはないため、 ``main``/``modules``/``types`` の項目は不要です。
代わりに、 ``bin`` 項目でエントリーポイント（ビルド結果の方）のファイルを指定します。
このキー名が実行ファイル名になります。

.. code-block:: json
   :caption: package.js

   {
     "bin": {
       "awesome-cmd": "dist/index.js"
     },
     "scripts": {
       "build": "tsc --project .",
       "lint": "eslint .",
       "fix": "eslint --fix ."
     }
   }

テストの設定、VSCodeの設定は変わりません。

CLIツールのソースコード
-----------------------------------

TypeScriptはシェバング(#!)があると特別扱いしてくれます。
必ず入れておきましょう。
ここで紹介したcommand-line-argsとcommand-line-usageはWikiで用例などが定義されているので、実装イメージに近いものをベースに加工していけば良いでしょう。

.. code-block:: ts

   index.ts
   #!/usr/bin/env node

   import * as clc from "cli-color";
   import * as commandLineArgs from "command-line-args";
   import * as commandLineUsage from "command-line-usage";

   // あとで治す
   require('source-map-support').install();

   async function main() {
       // 内部実装
   }

   main();

バンドラーで1つにまとめる
-------------------------------

npmで配るだけであればバンドルは不要ですが、ちょっとしたスクリプトをTypeScriptで書いてDockerサーバーで実行したいが、コンテナを小さくしたいのでnode_modulesは入れたくないということは今後増えていくと思いますので、そちらの方法も紹介します。
また、low.js [#]_ という、ES5しか動かないもののNode.jsと一部互換性があるモジュールを提供し、ファイルサイズがごく小さいインタプリタがありますが、これと一緒に使うこともできます。

バンドラーでは一番使われているのは間違いなくwebpackですが、昔ながらのBrowserifyは設定ファイルレスで、ちょっとした小物のビルドには便利です。BrowserifyはNode.jsのCommonJS形式のコードをバンドルしつつ、Node.js固有のパッケージは互換ライブラリを代わりに利用するようにして、Node.jsのコードをそのままブラウザで使えるようにするものです。オプションでNode.jsの互換ライブラリを使わないようにもできます。

webpackでもちょっと設定ファイルを書けばいけるはずですが、TypeScript対応以外に、shebang対応とかは別のプラグインが必要だったり、ちょっと手間はかかります。

Browserifyをインストールします。tsifyはBrowserifyプラグインで、TypeScriptのコードを変換します。
バンドルしてしまうので、バイナリのインストールが必要なパッケージ以外の各種ライブラリはすべて--save-devで入れても大丈夫です。

.. code-block:: bash

   $ npm install --save-dev browserify tsify

``tsconfig.json`` に関してはそのままで問題ありません。この手のバンドラーから使われる時は、.tsと.jsの1:1変換ではなくて、複数の.tsをメモリ上で.jsに変換し、そのあとにまとめて1ファイルにするn:1変換になります。そのため、個別の変換ファイルを出力しないnoEmit: trueをつけたりdistDirを消したりする必要がありますが、そのあたりはtsifyが勝手にやってくれます。

ただし、ES5しか動作しないlow.jsを使う場合は、出力ターゲットをES5にする必要があります。

.. code-block:: json
   :caption: tsconfig.json (low.jsを使う場合)

   {
     "compilerOptions": {
       "target": "es5",             // もしlow.jsを使うなら
       "lib": ["dom", "es2017"]     // もしlow.jsで新しいクラスなどを使うなら
     }
   }

ビルドスクリプトは次の形式になります。
``--node`` をつけないと、ブラウザ用のコードを生成しますが、ファイル入出力などが使えなくなりますので、CLIでは ``--node`` を忘れずにつけます。
TypeScript変換のために、 ``-p`` で ``tsify`` を追加しています。
もしminifyとかしたくなったら、minifyifyなどの別のプラグインを利用します。

.. code-block:: json

   {
     "scripts": {
       "build": "browserify --node -o dist/script.js -p [ tsify -p . ] src/index.ts"
     }
   }

もし、バイナリを入れる必要のあるライブラリがあると、Browserifyがエラーになります。その場合は、そのパッケージを ``--exclude パッケージ名`` で指定してバンドルされないようにします。
ただし、この場合は配布環境でこのライブラリだけはnpm installしなければなりません。

これで、TypeScript製かつ、必要なライブラリが全部バンドルされたシングルファイルなスクリプトができあがります。

.. [#] https://www.lowjs.org/

まとめ
--------------

コマンドラインツールの場合は、npmで配布する場合はライブラリ同様、バンドラーを使わずに、TypeScriptだけを使えば大丈夫です。
ここにある設定で、次のようなことが達成できました。

* TypeScriptでCLIツールのコードを記述する
* 使う人は普段通りnpm installすれば実行形式がインストールされ、特別なツールやライブラリの設定をしなくても利用できる。

また、おまけで1ファイルにビルドする方法も紹介しました。

``package.json`` の ``scripts`` のところに、開発に必要なタスクがコマンドとして定義されています。
npmコマンドを使って行うことができます。すべてライブラリと同じです。

.. code-block:: bash

   # ビルドしてパッケージを作成
   $ npm run build
   $ npm pack

   # テスト実行 (VSCodeだと、⌘ R Tでいける）
   $ npm test

   # 文法チェック
   $ npm run lint

   # フォーマッター実行
   $ npm run fix

