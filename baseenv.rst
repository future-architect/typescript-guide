==========================
基本の環境構築
==========================

環境構築の共通部分を紹介しておきます。
プロジェクトでのコーディングであれば、誰が書いても同じスタイルになるなど、コード品質の統一が大切になりますので、単なる個人用の設定ではなく、それをシェアできるというのも目的として説明していきます。
ここでは、基本的にすべてのプロジェクトでJest、ESLint、Prettierなどを選択しています。まあ、どれも相性問題が出にくい、数年前から安定して存在している、公式で推奨といった保守的な理由ですね。きちんと選べば、「JSはいつも変わっている」とは距離を置くことができます。

* Jest

  テスティングフレームワークはたくさんありますが、avaとJestがテスト並列実行などで抜きん出ています。JestはTypeScript用のアダプタが完備されています。avaはBabel/webpackに強く依存しており、単体で使うなら快適ですが、他のBabel Configと相性が厳しくなるのでJestにしています。

* ESLint

  公式が押しているのでこれですね。かつてはTSLintというツールがデファクトスタンダードでしたが、最適化の限界があることなどを理由に、TypeScriptが公式にESLintをメインのLinterとすることが宣言されました。よほどの理由がないかぎりはESLintを使うべきです。

  ESLintはプラグインを使うことでさまざまなルールを足せますし、プラグインを通じて設定を一括で変更できます。これはツール同士の干渉を避けるためだったり、推奨のルールセットを配布する手段として利用されています。

  * @typescript-eslint/eslint-plugin

    ESLintにTypeScriptの設定を追加するプラグインです

* Prettier

  TypeScript以外のSCSSとかにも対応していたりします。現在はシェアが伸びています。

  * eslint-config-prettier

    eslint側で、Prettierと衝突する設定をオフにするプラグインです

* npm scripts

  ビルドは基本的にMakefileとかgulpとかgruntとかを使わず、npm scriptsで完結するようにします。ただし、複数タスクをうまく並列・直列に実行する、ファイルコピーなど、Windowsと他の環境で両対応のnpm scriptsを書くのは大変なので、mysticateaさんのQiitaのエントリーのnpm-scripts で使える便利モジュールたちを参考に、いくつかツールを利用します。

* Visual Studio Code

  TypeScript対応の環境で、最小設定ですぐに使い始められるのはVisual Studio Codeです。しかも、必要な拡張機能をプロジェクトファイルで指定して、チーム内で統一した環境を用意しやすいので、推奨環境として最適です。EclipseなどのIDEの時代とは異なり、フォーマッターなどはコマンドラインでも使えるものを起動するケースが多いため、腕に覚えのある人はVimでもEmacsでもなんでも利用は可能です。

.. todo:: lyntのTypeScript対応状況を注視する

作業フォルダの作成
-------------------------

出力先フォルダの作成はプロジェクト構成ごとに変わってくるため、入力側だけをここでは説明します。
プロジェクトごとにフォルダを作成します。
ウェブだろうがライブラリだろうが、 ``package.json`` が必要なツールのインストールなど、すべてに必要になるため、 ``npm init`` でファイルを作成します。

.. code-block:: bash

   $ mkdir projectdir
   $ cd projectdir
   $ npm init -y
   $ mkdir src
   $ mkdir __tests__

外部に公開しないパッケージの場合には、 ``"private": true`` という設定を忘れずにいれましょう。

srcフォルダ以下に.tsファイルを入れて、出力先のフォルダ以下にビルド済みファイルが入るイメージです。仮にこれを ``dist`` とすると、これはGitでは管理しませんので ``.gitignore`` に入れておきます。

.. code-block:: text
   :caption: .gitignore

   dist
   .DS_Store
   Thumbds.db

もし成果物を配布したい場合は、それとは逆に、配布対象はdistとルートのREADMEとかだけですので、不要なファイルは配布物に入らないように除外しておきましょう。これから作るTypeScriptの設定ファイル類も外して起きましょう。

.. code-block:: text
   :caption: .npmignore

   dist
   .DS_Store
   Thumbds.db
   __tests__/
   src/
   tsconfig.json
   jest.config.json
   .eslintrc
   .travis.yml
   .editorconfig
   .vscode

ビルドのツールのインストールと設定
--------------------------------------

まず、最低限、インデントとかの統一はしたいので、editorconfigの設定をします。editorconfigを使えばVisual Studio、vimなど複数の環境があってもコードの最低限のスタイルが統一されます（ただし、各環境で拡張機能は必要）。また、これから設定するprettierもこのファイルを読んでくれます。

.. code-block:: ini
   :caption: .editorconfig

   root = true

   [*]
   indent_style = space
   indent_size = 4
   end_of_line = lf
   charset = utf-8
   trim_trailing_whitespace = true
   insert_final_newline = true

ツール群はこんな感じで入れました。

.. code-block:: bash

   $ npm install --save-dev typescript prettier
      eslint @typescript-eslint/eslint-plugin
      @typescript-eslint/parser
      eslint-plugin-prettier
      eslint-config-prettier npm-run-all

設定ファイルは以下のコマンドを起動すると雛形を作ってくれます。これを対象の成果物ごとに編集していきます。
詳細は各パッケージの種類の章で取り扱います。

.. code-block:: bash

   $ npx tsc --init

ESLintの設定も作ります。Prettierと連携するようにします。

.. code-block:: json
   :caption: .eslintrc

   {
     "plugins": [
       "prettier"
     ],
     "extends": [
       "plugin:@typescript-eslint/recommended",
       "plugin:prettier/recommended"
     ],
     "rules": {
       "no-console": 0,
       "@typescript-eslint/indent": 0,
       "prettier/prettier": 2
     }
   }

ESLintを起動するタスクを ``package.json`` に追加しましょう。
これで、 ``npm run lint`` や ``npm run fix`` でコードチェックをしたり、スタイル修正が行えます。

.. code-block:: json
   :caption: package.json

   "scripts": {
     "lint": "eslint .",
     "fix": "eslint --fix ."
   }

テスト
-----------

ユニットテスト環境も作ります。TypeScriptを事前に全部ビルドしてからJasmineとかも見かけますが、公式でTypeScriptを説明しているJestにしてみます。

.. code-block:: bash

   $ npm install --save-dev jest ts-jest @types/jest

scripts/testと、jestの設定を追加します。古い資料だと、transformの値がnode_modules/ts-jest等になっているのがありますが、今はts-jestだけでいけます。

.. code-block:: json
   :caption: package.json

   {
     "scripts": {
       "test": "jest"
     }
   }

.. code-block:: js
   :caption: jest.config.js

   module.exports = {
     transform: {
       "^.+\\.tsx?$": "ts-jest"
     },
     moduleFileExtensions: [
       "ts",
       "tsx",
       "js",
       "json",
       "jsx"
     ]
   };

Visual Studio Codeの設定
--------------------------------

Visual Stuido Codeでフォルダを開いたときに、eslintの拡張と、editorconfigの拡張がインストールされるようにします。

.. code-block:: json
   :caption: .vscode/extensions.json

   {
     "recommendations": [
       "dbaeumer.vscode-eslint",
       "EditorConfig.editorconfig"
     ]
   }

ファイル保存時にeslint --fixが自動実行されるように設定しておきましょう。これでVisual Studio Codeを使う限り、誰がプロジェクトを開いてもコードスタイルが保たれます。Visual Studio Codeのeditor.codeActionsOnSaveは、files.autoSaveがafterDelayのときは効かないので、offに設定しておきます。

.. code-block:: json
   :caption: .vscode/settings.json

   {
     "editor.codeActionsOnSave": {
       "source.fixAll.eslint": true,
     },
     "files.autoSave": "off"
   }

.. todo:: tsdocとかドキュメントツールを紹介

.. todo:: eslintやテストの書き方の紹介

