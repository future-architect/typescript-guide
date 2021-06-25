Parcelを使ったウェブ開発
=============================================

React開発であればcreate-react-appやNext.js、Vueであれば@vue/cliやNuxt.js、Angularも@angular/cliといった、それぞれのフレームワークごとに環境構築をまとめて行う環境整備ツールが近年では充実してきています。

しかし、そこから多少離れるものであったり、あるいはより高速なビルドが欲しいなど、要件によっては他のビルドツールで環境を作る方がプロジェクトにはマッチする可能性もあります。本章ではParcelを使った環境構築について紹介します。

.. note::

   現時点ではリリースされていないParcel 2.0 beta 2を対象に説明します。なお、このバージョンでは、TypeScript 4系とは依存のバージョンがコンフリクトして同時にりようできませんが、インストール時に--forceをつけることで利用はできます。

Parcelとは
--------------------------

* https://v2.parceljs.org/

Parcelはゼロコンフィグを目指したバンドラーです。ほとんど設定を書くことなく環境を準備できます。たとえプロダクション開発ではwebpackを使ったとしても、小さいコードをすばやく書き上げる場合などに知っておいて損はないでしょう。Parcelはビルド設定ファイルを作成することなく、エントリーポイントのファイルを指定するだけでビルドできます。エントリーポイントのファイルはウェブ開発であればHTMLファイルも使えます。そのHTMLから参照されているスクリプトファイルやCSSなどをすべて辿ってビルドしてくれます。

TypeScriptも最初からサポートしています。tsconfig.jsonがあればそれを拾って解釈してくれますし、なくても動きます。単にtsファイルをscriptタグのsrcにするだけで、そのままTypeScriptの処理系をインストールしつつビルドしてくれます。最初のビルドも高速ですし、キャッシュもしてくれて2回目以降も速いです。TreeShakingとかの生成されたファイルの最適化機構も入っています。

なお、ゼロコンフィグというか、設定ファイルがなかったので、ちょっと凝ったことをしようとすると、Parcelのビルド機能をAPIとして呼び出すウェブサーバーを書かねばならず、かえって大変になることもありましたが、Parcel 2からはちょっとした設定ファイルでデフォルト設定を変更できるようになりました。例えば次のようなことができるようになります。

* TypeScriptのビルドでエラーメッセージが出せるようになった
* APIサーバーへのプロキシができるようになった

Parcelのインストールと環境の構築
----------------------------------------

Parcelは環境構築は簡単ですが、全自動の環境構築ツールはありません。まずはプロジェクトフォルダを作り、\ ``package.json``\ を作成します。

.. code-block:: bash

   $ npm init -y

:doc:`baseenv`\ で紹介したように、PrettierとESLintを設定しておきましょ。

次にParcelを追加します。\ ``parcel-bundler``\ と言うパッケージ名はv1系列です。v2系列は\ ``parcel``\ になりました。まだv2は正式リリースされていないため、インストール時は\ ``@next``\ （比較的安定板）、あるいは明示的に\ ``@2.0.0-beta.3.1``\ などのバージョンを指定するようにしてください。このコードは\ ``@2.0.0-beta.3.1``\ で動作の確認をしています。

.. code-block:: bash

   $ npm install --save-dev parcel@next

ビルドを実行すればそのタイミングで拡張子を見てTypeScriptをインストールして実行はしてくれますが、先にインストールしてtsconfig.jsonを作っておきましょう。
.. code-block:: bash

   $ npx install --save-dev typescript
   $ npx tsc --init

TypeScriptの動作をレベルアップする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

これでビルドと開発はできますが、デフォルトのParcelは\ ``@babel/preset-typescript``\ を使って型情報を切り落とすだけで型のチェックは行ません。VSCodeで編集すればその場でエラーチェックはしてくれますが、変更したファイルが他のファイルに影響を与えていてエラーになっていたり、警告が出ていた、というのはなかなか気付きにくいです。バリデーションを有効化すると、このようなトラブルは防げます。本体のバージョンと合ったバージョンをインストールします。

また、公式の\ ``tsc``\ を実際のビルド時にも利用させる設定があります。これを利用すると、デコレータを利用するようなLitのようなフレームワークのビルドも正しくできるようになります。

この2つは独立しているので、片方だけ入れることも可能です。次のサンプルでは同時に有効化しています。

.. code-block:: bash

   $ npm install --save-dev
       @parcel/validator-typescript@next
       @parcel/transformer-typescript-tsc@next

次に、設定ファイルを書き換えます。

.. code-block:: json
   :caption: .parcelrc

   {
     "extends": "@parcel/config-default",
     "validators": {
       "*.{ts,tsx}": ["@parcel/validator-typescript"]
     },
     "transformers": {
       "*.{ts,tsx}": ["@parcel/transformer-typescript-tsc"]
     }
   }

APIサーバーに対してプロキシする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.proxyrcファイルを作成することで、一部のリクエストをAPIサーバーに受け流すといったことが可能です。これにより、フロントエンドとバックエンドが同じオリジンで動作するようになり、CORSなどのセキュリティの環境整備が簡単になります。もし、本番環境も別ホストで配信するのであれば、元々CORSの設定などは考慮されていて少ない労力でなんとかなると思われますが、そうでない場合、テスト環境のためにCORSを設定するといった大仰なことをしなくて済みます。

.. code-block:: json
   :caption: .proxyrc

   {
     "/api": {
       "target": "http://localhost:3000/"
     }
   }

なお、パスのリライトなど、高度なこともできます。しかし、動作しなかったときの問題追跡が面倒になるため、ホスト名の転送だけで済むようにしておくと良いでしょう。

React環境
--------------------------

まずHTMLファイルを用意します。ポイントは前述のように、\ ``<script>``\ タグに読み込ませたいTypeScriptのコードを書くことです。

.. code-block:: html
   :caption: src/index.html

   <!DOCTYPE html>
   <html lang="en">
     <head>
       <meta charset="utf-8" />
       <meta name="viewport" content="width=device-width, initial-scale=1" />
       <meta http-equiv="X-UA-Compatible" content="ie=edge">
       <title>Parcel Project</title>
     </head>
     <body>
       <div id="root"></div>
       <script src="./index.tsx"></script>
     </body>
   </html>

最後にこのスクリプトを書き足します。

.. code-block:: ts
   :caption: src/index.tsx

   import React, { StrictMode } from 'react';
   import { render } from 'react-dom';

   render(
     <StrictMode>
       <div>test</div>
     </StrictMode>,
     document.getElementById('root')
   );

``tsconfig.json``\ のデフォルトではES2015 modulesが有効になっておらず、ビルドターゲットが古いのでそこを修正するのと、今回はReactなのでJSXもreactにしておきます。

.. code-block:: json
   :caption: tsconfig.json

   {
     "compilerOptions": {
       "target": "ES2018",
       "module": "es2015",
       "jsx": "react"
     }
   }

.. code-block:: json
   :caption: package.json

   {
     "scripts": {
       "start": "parcel serve src/index.html",
       "build": "parcel build src/index.html",
     }
   }

Web Components開発環境
--------------------------------

Web Componentsはブラウザ標準のコンポーネントを作成するAPIの集合です。この形式で作ったコンポーネントは、フレームワークの力を借りずに表示できます。CDNにアップロードしておけば追加して静的なHTMLの中でタグを書くだけで表示したりもできますし、他のフレームワークとも組み合わせられます\ [#]_\ 。

Web Componentsを作成するためのフレームワークにはさまざまな種類があります。ここではWeb Componentsを推進しているGoogleが開発する、Litを使ってみます。

* https://lit.dev/

まずはlitをインストールします。

.. code-block:: bash

   $ npm install lit

公式サイトのサンプルを持ってきました。これをどこか適当なところにおきます。

.. code-block:: ts
   :caption: src/my-element.ts

   /**
    * @license
    * Copyright 2019 Google LLC
    * SPDX-License-Identifier: BSD-3-Clause
    */

   import {LitElement, html, css} from 'lit';
   import {customElement, property} from 'lit/decorators.js';

   /**
    * An example element.
    *
    * @slot - This element has a slot
    * @csspart button - The button
    */
   @customElement('my-element')
   export class MyElement extends LitElement {
     static styles = css`
       :host {
         display: block;
         border: solid 1px gray;
         padding: 16px;
         max-width: 800px;
       }
     `;

     /**
      * The name to say "Hello" to.
      */
     @property()
     name = 'World';

     /**
      * The number of times the button has been clicked.
      */
     @property({type: Number})
     count = 0;

     render() {
       return html`
         <h1>Hello, ${this.name}!</h1>
         <button @click=${this._onClick} part="button">
           Click Count: ${this.count}
         </button>
         <slot></slot>
       `;
     }

     private _onClick() {
       this.count++;
     }

     foo(): string {
       return 'foo';
     }
   }

   declare global {
     interface HTMLElementTagNameMap {
       'my-element': MyElement;
     }
   }

次に、タグの入ったHTMLを作ります。先程のtsファイルを直接scriptタグで指定するのがポイントです。ParcelがこのHTMLから取り込んでいるファイルの拡張子を見て適切に処理します。

.. code-block:: html
   :caption: sample.html

   <!doctype html>
   <html lang="en">
   <head>
     <meta charset="utf-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title><my-element> ⌲ Home</title>
     <script type="module" src="src/my-element.ts"></script>
   </head>
   <body>
     <p><my-element name="HTML"></my-element></p>
   </body>
   </html>

最後にparcelのビルド設定をを追加します。

.. code-block:: json
   :caption: package.json

   {
     "scripts": {
       "start": "parcel serve src/index.html"
     }
   }

これでビルドができます。localhost:1234で開発サーバーが起動するので、ここにブラウザでアクセスするとビルドされたWeb Componentsが表示されます。ホットリロードも効くので開発をスムーズに行えます。

.. [#] Polyfillが必要なIEもサポートする場合、PolyfillがDOMを書き換えて再現します。これがDOMをすべて自分の管理のもとに書き換えを行う他のフレームワークとの相性が悪くなるため、ReactやVueと組み合わせる場合はIEサポートを切る必要があります。