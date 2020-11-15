Electronアプリケーションの作成
========================================

マルチプラットフォームなデスクトップアプリケーションを簡単に作る方法として近年人気なのがGitHubの開発したElectronを使った開発です。ChromiumとNode.jsが一体となった仕組みになっています。UIはブラウザで「レンダープロセス」が担い、そのUIの起動やローカルファイルへのアクセスなどを行うのが「メインプロセス」です。

レンダープロセスとメインプロセスはなるべく疎結合に作ります。プログラムの量はおそらくレンダープロセスが95%ぐらいの分量になるでしょう。SPAのウェブフロントエンドとウェブサーバーを作る感覚よりも、さらにフロントに荷重が寄った構造になるでしょう。

Electronのランタイムと、ビルドしたJavaScriptをまとめて、インストーラまで作成してくれるのがElectron-Buildです。これを使ってアプリケーションの開発を行っていきます。Vueの場合はVue CLI用のプラグイン\ [#]_\ があります。

* https://www.electron.build/

.. [#] https://nklayman.github.io/vue-cli-plugin-electron-builder/

React+Electronの環境構築の方法
-----------------------------------

Electronの開発は2つ作戦が考えられます。一つが、ウェブのフロントエンドとして、そちらのエコシステムを利用して開発します。もう一つが、普段の開発からElectronをランタイムとして開発する方法です。どちらか慣れている方で良いでしょう。

後者については次のQiitaのエントリーが詳しいです。

* https://qiita.com/yhirose/items/22b0621f0d36d983d8b0
* https://github.com/yhirose/react-typescript-electron-sample-with-create-react-app-and-electron-builder

本書では、前者の方法について紹介します。まず、プロジェクトを作成します。今回は2つのエントリーポイントのビルドが必要なため、これに対応しやすいParcelを利用します。

.. code-block:: bash

   # プロジェクトフォルダ作成
   $ mkdir electronsample
   $ cd electronsample
   $ npm init -y

   # 必要なツールをインストール
   $ npm install --save-dev parcel@next typescript @parcel/validator-typescript@2.0.0-nightly.430
   $ npm install --save-dev react @types/react react-dom @types/react-dom
   $ npm install --save-dev electron npm-run-all

   # tsconfig作成
   $ npx tsc --init

tsconfig.jsonは、いつものようにtarget/module/jsxあたりを修正しておきます。

.. code-block:: json
   :caption: tsconfig.json

   {
     "compilerOptions": {
       "target": "es2020",
       "module": "es2015",
       "jsx": "react",
       "strict": true,
       "moduleResolution": "node",
       "esModuleInterop": true,
       "skipLibCheck": true,
       "forceConsistentCasingInFileNames": true
     }
   }

もう一つ、メインプロセス用のtsconfigも作ります。こちらはNode.js用に近い形式で出力が必要なため、commonjs形式のモジュールに設定しています。

.. code-block:: json
   :caption: tsconfig.main.json

   {
     "extends": "./tsconfig.json",
     "compilerOptions": {
       "outDir": "dist",
       "module": "commonjs",
       "sourceMap": true,
     },
     "include": [
       "src/main/*"
     ]
   }

次にファイルを3つ作ります。

.. code-block:: html
   :caption: src/render/index.html

   <!DOCTYPE html>
   <head>
     <meta http-equiv="Content-Security-Policy" content="script-src 'self' 'unsafe-inline';" />
   </head>
   <body>
     <div id="app"></div><script src="index.tsx"></script>
   </body>

.. code-block:: ts
   :caption: src/render/index.tsx

   import React from "react";
   import { render } from "react-dom";

   const App = () => <h1>Hello!</h1>;

   render(<App />, document.getElementById("app"));

.. code-block:: ts
   :caption: src/main/main.ts

   import { app, BrowserWindow } from 'electron';

   let win: BrowserWindow | null = null;

   function createWindow() {
     win = new BrowserWindow({ width: 800, height: 600 })
     win.loadURL(`file://${__dirname}/index.html`);
     win.on('closed', () => win = null);
   }

   app.on('ready', createWindow);

   app.on('window-all-closed', () => {
     if (process.platform !== 'darwin') {
       app.quit();
     }
   });

   app.on('activate', () => {
     if (win === null) {
       createWindow();
     }
   });

package.jsonのスクリプトも追加しておきましょう。レンダープロセス部分はPercelを使い、メインプロセスにはTypeScriptのtscコマンドをダイレクトで使っています。tscはバンドルをせずに、ソースファイルに対して1:1で変換した結果を出力します。メインプロセスは@vercel/nccを使っても良いと思いますが、Electronではレンダープロセス起動時の初期化スクリプト(preload)も設定できるため、生成したいファイルは複数必要になりますが、残念ながら@vercel/nccは複数のエントリーポイントを扱うのが得意ではないため、ここではバンドルをせずにtscで処理をしています。外部ライブラリを利用する場合などはメインプロセスもnccでバンドルを作成する方が良いでしょう。

もう一つのポイントは"browser"と"main"です。生成したJavaScriptを元に、ユーザーに配布しやすい形にランタイム込みのバンドルを作成するelectron-builderはmainの項目を見てビルドを行います。また、Parcelも同じくデフォルトでmainを見ますが、electron-builderのmainはメインプロセス、Parcelで処理をするのはレンダープロセス側です。そのため、parcelコマンドのオプションで、mainじゃない項目（ここではbrowser）に書かれたファイル名で出力するように--targetオプションを設定しています。

.. code-block:: json
   :caption: package.json

   {
    "browser": "dist/index.html",
    "main": "dist/main.js",
     "scripts": {
       "serve": "parcel serve src/render/index.html",
       "build": "run-p build:main build:render",
       "build:main": "tsc -p tsconfig.main.json",
       "build:render": "parcel build  --dist-dir=dist --public-url --target=browser \"./\" src/render/index.html",
       "start": "run-s build start:electron",
       "start:electron": "electron dist/main/index.js"
     }
   }

次のコマンドで開発を行っていきます。

* ``npm run serve``: フロントエンド部分をブラウザ上で実行します。
* ``npm run build``: レンダープロセス、メインプロセス2つのコードをビルド
* ``npm start``: ビルドした結果をelectronコマンドを使って実行

配布用アプリケーションの構築
-------------------------------------

これまで作ってきた環境は開発環境で、Electron本体をnpmからダウンロードして実行します。エンドユーザー環境にはnpmもNode.jsもないことが普通でしょう。Electronの本体も一緒にバンドルしたシングルバイナリのアプリケーションを作成していきます。ビルドにはelectron-builderを利用します。

* https://www.electron.build/

インストールはnpmで行います。

.. code-block:: bash

   npm install --save-dev electron-builder

electron-builderの設定はpackage.jsonに記述します。outputフォルダを設定しないとdistに出力され、Parcelなどの出力と最終的なバイナリが混ざり、2回目以降のビルド時にその前までにビルドした結果のファイルまでバンドルされてしまってファイルサイズがおかしなことになるため、distと別フォルダを設定します。

.. code-block:: json
   :caption: package.json

   {
     "scripts": {
       "electron:build": "run-s build electron:bundle",
       "electron:bundle": "electron-builder"
     },
     "build": {
       "appId": "com.example.electron-app",
       "files": [
         "dist/**/*",
         "package.json"
       ],
       "directories": {
         "buildResources": "resources",
         "output": "electron_dist"
       },
       "publish": null
     }
   }

次のコマンドで配布用のバイナリが作成できます。

* ``npm run electron:build``

これは本当の最小限です。electron-builderを利用すると、アイコンをつけたり、署名をしたりもできますし、クロスビルドも行えます。

デバッグ
-----------------------------

普段のブラウザでは開発者ツールを開かないことにはconsole.logも利用できません。Electronもレンダープロセスのデバッグには開発者ツールが使いたくなるでしょう。開発者ツールを起動するには1行書くだけで済みます。環境変数やモードを見て開くようにすると便利でしょう。

.. code-block:: ts

   win.webContents.openDevTools();

レンダープロセスとメインプロセス間の通信
--------------------------------------------------------

レンダープロセスは通常のブラウザに近いものと紹介しましたが、セキュリティの考え方もほぼ同様です。Electronではブラウザウインドウを開くときにどのページを開くかを指定しましたが、ここでは外部のサービスを開くこともできます。普段はローカルのファイルで動くが、リモートのサービスも使えるブラウザです。

.. code-block:: ts

   win.loadURL(`https://google.com`);

ただし、このリモートのサービスが使える点がElectronのセキュリティを難しいものにしています。Electronには、レンダープロセスでNode.jsの機能が使えるようになるnodeIntegrationという機能があり、ブラウザウインドウを開くときのオプションで有効化できます。しかしこれを有効化すると、ローカルのユーザー権限で見られるあらゆる場所のファイルにアクセスできますし、ファイルを書き換えたりできてしまい、クロスサイトスクリプティング脆弱性を入れ込んでしまうときのリスクが極大化されてしまうため、レンダープロセスが外部のリソースをロードする場合はこの機能はオフにすべきです（現在のデフォルトはオフです）。OpenID Connectの認証など、外部のリソースをロードしたいことはよくあるので、この機能はもうなかったものとして考えると良いでしょう。

代わりに提供されているのがコンテキストブリッジになります。歴史的経緯などは次のページにまとまっています。

* Electron（v10.1.5現在）の IPC 通信入門 - よりセキュアな方法への変遷: https://qiita.com/hibara/items/c59fb6924610fc22a9db

まず、ウィンドウを開くときのオプションで、nodeIntegrationをオフに、contextIsolationをオンにします。後者は、これからロードするプリロードのスクリプトが直接ブラウザプロセスの情報にアクセスできないようになります。

.. code-block:: ts
   :caption: main.ts

   const win = new BrowserWindow({
     webPreferences: {
       nodeIntegration: false,
       contextIsolation: true,
       preload: __dirname + '/preload.js'
     }
   });

次に、レンダープロセスにAPIを追加します。preloadスクリプトを使うことで、レンダープロセスのグローバル変数に関数を追加できます。ここでは、\ ``window.api.writeFile()``\ という関数を定義しています。このスクリプトは2つのプロセスの中間地点です。ブラウザプロセスとは別のコンテキストで実行されます。どちらかというと、レンダープロセス寄りですが、レンダープロセスの内では直接扱えない機能が利用できます。\ ``ipcRenderer``\ が、メインプロセスとレンダープロセス間の通信を行うオブジェクトです。このコンテキストブリッジ内で\ ``ipcRendererの\ ``send()``\ や\ ``on()``\ を呼び出すことで、メインプロセスに対する送信と受信が実現できます。

.. code-block:: ts
   :caption: preload.ts

   // eslint-disable-next-line
   const { contextBridge, ipcRenderer } = require('electron');
   contextBridge.exposeInMainWorld('api', {
     writeFile: (data) => {
       ipcRenderer.send('writeFile', data);
     },
   })

``ipcRenderer``\ と対になる\ ``ipcMain``\ を使って通信を行います。

.. code-block:: ts
   :caption: main.ts

   import { app, ipcMain } from 'electron';
   import { writeFileSync } from 'fs';
   import { join } from 'path';

   ipcMain.on('writeFile', (_event, data) => {
     const jsonStr = JSON.stringify(data, null, 4);
     writeFileSync(join(app.getPath('userData'), jsonStr, 'utf8');
   });

これにより、ブラウザプロセス側には間接的にファイル読み書きを行うAPIを登録し、それ経由で、実際の危険な操作をともなうメインプロセス側の処理を呼び出すことが可能です。

.. list-table:: Electronのプロセス間通信
   :header-rows: 1

   - * 通信方向
     * レンダープロセス側
     * メインプロセス側
   - * レンダープロセス→メインプロセス
     * ``ipcRenderer.send()``
     * ``ipcMain.on()``\ に登録したコールバック
   - * メインプロセス→レンダープロセス
     * ``ipcRenderer.on()``\ に登録したコールバック
     * ``ipcMain.send()``
　　　
まとめ
------------

Electronについて、環境の構築から配布用バイナリの作成、Electronならではの開発のトピックを紹介してきました。近年のデスクトップアプリケーションの開発ではかなり人気のある選択肢となっています。TypeScriptとブラウザのアプリケーションの知識があればデスクトップアプリケーションが作成できます。フロントエンド系の開発者にとっては福音と言えるでしょう。

ChromeベースのEdgeが利用できるようになって、ブラウザ間の機能差は小さくなりましたが、Electronはすべてのユーザーに同一バージョンの最新ブラウザを提供するようなものでもあるため、社内システム開発でも使いたいというニーズはあるでしょう。また、ファイルシステムアクセスなど、ブラウザだけでは実現できない機能もいろいろ利用できます。

一方で、ツールバー、トレイなど、デスクトップならではのユーザビリティも考慮する必要は出てきますし、メニュー構成もWindows標準とmacの違いなどもあったりもします。フロントエンドの開発だけではなく、違和感なく使ってもらえるアプリケーションにするには、プラスアルファの手間隙がかかることは忘れないようにしてください。