Next.js（React）の環境構築
=====================================

ウェブフロントエンドが今のJavaScript/TypeScriptの主戦場です。
本章では、Next.jsについて取り上げます。

.. note:: 素のReactとVue.jsとAngular

   Next.jsはReactの上に作られたフレームワークですが、それ以外に人気のフレームワークにVue.jsとAngularがあります。この2つに関しては、手動で環境を作る必要はありません。

   Vue.jsではvueのCLIコマンドを使ってプロジェクトを作成できますが、作成時に最初に聞かれる質問でdefaultのpreset（babelとeslint）ではなく、Manually select featuresを選択してからTypeScriptを選ぶとインストールと設定が完了します。

   コア自体がTypeScriptで作成されているAngularは、実装言語はTypeScript以外が選べません。

   また、Reactそのものも、create-react-appコマンドを使って環境構築を行う場合、 ``--typescript`` オプションをつけるとTypeScript用のプロジェクトが作成できます。

   .. code-block:: bash

      $ npx create-react-app myapp --typescript

      Creating a new React app in /Users/shibukawa/work/myapp.

      Installing packages. This might take a couple of minutes.
      Installing react, react-dom, and react-scripts...
      :
      Happy hacking!

なるべく、いろんなツールとの組み合わせの検証の手間を減らすために、Next.jsを使います。
JavaScriptは組み合わせが多くて流行がすぐに移り変わっていつも環境構築させられる（ように見える）とよく言われますが、組み合わせが増えても検証されてないものを一緒に使うのはなかなか骨の折れる作業で、結局中のコードまで読まないといけなかったりとか、環境構築の難易度ばかりが上がってしまいます。特にRouterとかすべてにおいて標準が定まっていないReactはそれが顕著です。

その中において、CSS in JS、RouterをオールインワンにしてくれているNext.jsは大変助かります。
issueのところでもアクティブな中の人がガンガン回答してくれていますし、何よりも多種多様なライブラリとの組み合わせをexampleとして公開してくれているのが一番強いです。
Server Side Renderingもありますが、お仕事でやっていて一番ありがたいのはこの設定周りです。

.. [#] https://github.com/zeit/next.js/tree/canary/examples

Next.jsとは
------------------------

まず、Next.jsとは何かについて説明します。Next.jsはZeit社が開発しているReactのオールインワンパッケージです。\ ``next``\ コマンドでプロジェクトを作成すると、多くの必要な開発環境整備が完了した環境が一発で作成できます。

この開発環境はWebPackのビルド環境の整備も完了しています。ビルド環境は素早くコンパイルして確認が行えるビルドサーバーも設定されています。TypeScriptも設定済みです。何より、自分で設定すると相当難易度の高いサーバーサイドレンダリングが最初から得られます。

Next.jsを使うからといって、オールインワンですべて付いてくる状態でしか動かせないわけではなく、デプロイする方式によって自由に使い分けることができます。

デフォルトではサーバーサイドレンダリングを行うフロントエンド機能のみですが、カスタムサーバー機能を使えば、Express.jsなどのNode.jsのAPIサーバーにサーバーサイドレンダリング機能などを乗せることができます。Express.jsへの薄いラッパーになりますので、Express.jsの知識を利用して、APIサーバー機能も同一のサーバー上に追加できます。また、サーバーサイドレンダリングを使わずに静的なHTMLとJavaScriptコードを生成することも可能です。

出発点としては十分なケースが多いと思われます。

作業フォルダを作る
------------------------

Next.jsではpagesフォルダにおいてあるコンポーネントがRouterに自動登録されるので、このフォルダをとりあえず作ります。あとは基本の環境構築と同じです。

.. code-block:: bash

   $ mkdir pages

ウェブサービスをnpmに公開することはあんまりないと思うので、 ``.npmignore`` は不要ですが、 ``.gitignore`` の方は、Next.jsのファイル生成先の出力先フォルダを設定しておきます。

.. code-block:: text
   :caption: .gitignore

   .next

ビルドのツールのインストールと設定
--------------------------------------

Next.jsではnext以外にも、react、react-domをインストールします。他にも必要なものを入れてしまいましょう。ReactのJSXに対応させるために、eslint-plugin-reactを忘れないようにしましょう。

.. code-block:: bash

   $ npm install --save next react react-dom
   $ npm install --save-dev @types/node @types/next @types/react @types/react-dom
   $ npm install --save-dev typescript prettier
       eslint @typescript-eslint/eslint-plugin eslint-plugin-prettier
       eslint-config-prettier eslint-plugin-react npm-run-all 
   $ npm install --save-dev jest ts-jest @types/jest

Next.jsを快適にするためにTypeScriptと、SCSSを入れます。Next.jsでは、本家が提供しているプラグインを使います。

.. code-block:: bash

   $ npm install --save-dev @zeit/next-typescript @zeit/next-sass node-sass

Next.jsだけでは真っ白なシンプルなHTMLになってしまうので、よくメンテナンスされているMaterial Designのライブラリである、Material UIを入れましょう。ウェブ開発になると急に必要なパッケージが増えますね。

.. code-block:: bash

   $ npm install --save @material-ui/core @material-ui/icons react-jss

```tsconfig.json``` は今までと少し異なります。後段でBabelが処理してくれる、ということもあって、モジュールタイプはES6 modules形式、ファイルを生成することはせず、Babelに投げるので\ ``noEmit: true``\ 。
ReactもJSX構文をそのまま残す必要があるので"preserve"。
また、JSで書かれたコードも一部あるので、allowJsも: trueでなければなりません。

.. code-block:: json
   :caption: tsconfig.json

   {
     "compilerOptions": {
       "allowJs": true,
       "allowSyntheticDefaultImports": true,
       "baseUrl": ".",
       "jsx": "preserve",
       "lib": ["dom", "es2017"],
       "module": "esnext",
       "moduleResolution": "node",
       "noEmit": true,
       "noUnusedLocals": true,
       "noUnusedParameters": true,
       "preserveConstEnums": true,
       "removeComments": false,
       "skipLibCheck": true,
       "sourceMap": true,
       "strict": true,
       "target": "esnext"
     }
   }

Babel側にも設定を足します。

.. code-block:: json
   :caption: .babelrc

   {
     "presets": [
       "next/babel",
       "@zeit/next-typescript/babel"
     ]
   }

TypeScriptと、SCSSのプラグインを有効化します。

.. code-block:: js
   :caption: next.config.js

   const withTypescript = require("@zeit/next-typescript");
   const withSass = require("@zeit/next-sass");

   module.exports = withTypescript(
     withSass({
       webpack(config) {
         return config;
       }
     })
   );

Next.jsの場合は、nextコマンドがいろいろやってくれるので、やっていることの分量のわりにscriptsがシンプルになります。

.. code-block:: json
   :caption: package.json

   {
     "scripts": {
       "dev": "next",
       "build": "next build",
       "export": "next export",
       "start": "next start",
       "lint": "eslint .",
       "fix": "eslint --fix .",
       "test": "jest",
       "watch": "jest --watchAll"
     }
   }

ESLintはJSX関連の設定や、.tsxや.jsxのコードがあったらJSXとして処理する必要があるため、これも設定に含めます。
あと、next.config.jsとかで一部Node.jsの機能をそのまま使うところがあって、CommonJSのrequireを有効にしてあげないとエラーになるので、そこも配慮します。

.. code-block:: json
   :caption: .eslintrc

   {
     "plugins": [
       "prettier"
     ],
     "extends": [
       "plugin:@typescript-eslint/recommended",
       "plugin:prettier/recommended",
       "plugin:react/recommended"
     ],
     "rules": {
       "no-console": 0,
       "prettier/prettier": "error",
       "@typescript-eslint/no-var-requires": false,
       "@typescript-eslint/indent": "ingore",
       "react/jsx-filename-extension": [1, {
         "extensions": [".ts", ".tsx", ".js", ".jsx"]
       }]
     }
   }

Next.js+TSのソースコード
----------------------------------------


まずMaterial UIを使うときに設定しなければならないコードがあるので、Material UIのサンプルページのsrc/getPageContext.js、 pages/_app.js、pages/_document.jsの3つのファイルをダウンロードして同じように起きます。Material UIのCSS in JSがNext.js標準の方法と違うので、それを有効化してやらないと、サーバーサイドレンダリングのときに表示がおかしくなってしまいます。

次にページのコンテンツです。Next.jsの規約としては、pages以下のファイルが、export defaultでReactコンポーネントを返すと、それがページとなります。ちょっと長いですが、TypeScriptでページ作成するための方法を色々埋め込んであります。

.. code-block:: ts
   :caption: pages/index.tsx

   import Link from "next/link";
   import React from "react";

   import { Toolbar } from "@material-ui/core";
   import AppBar from "@material-ui/core/AppBar";
   import Button from "@material-ui/core/Button";
   import Dialog from "@material-ui/core/Dialog";
   import DialogActions from "@material-ui/core/DialogActions";
   import DialogContent from "@material-ui/core/DialogContent";
   import DialogContentText from "@material-ui/core/DialogContentText";
   import DialogTitle from "@material-ui/core/DialogTitle";
   import {
     createStyles,
     Theme,
     withStyles,
     WithStyles
   } from "@material-ui/core/styles";
   import Typography from "@material-ui/core/Typography";

   function styles(theme: Theme) {
     return createStyles({
       root: {
         paddingTop: theme.spacing.unit * 20
       }
     });
   }

   interface Props {
     children?: React.ReactNode;
   }

   interface State {
     openDialog: boolean;
   }

   class Index extends React.Component<
     Props & WithStyles<typeof styles>,
     State
   > {
     public state = {
       openDialog: false
     };

     constructor(props: Props & WithStyles<typeof styles>) {
       super(props);
     }

     public handleCloseDialog = () => {
       this.setState({
         openDialog: false
       });
     };

     public handleClickShowDialog = () => {
       this.setState({
         openDialog: true
       });
     };

     public render() {
       const { classes } = this.props;
       const { openDialog } = this.state;

       return (
         <div className={classes.root}>
           <Dialog open={openDialog} onClose={this.handleCloseDialog}>
             <DialogTitle>Dialog Sample</DialogTitle>
             <DialogContent>
               <DialogContentText>
                 Easy to use Material UI Dialog.
               </DialogContentText>
             </DialogContent>
             <DialogActions>
               <Button
                 color="primary"
                 onClick={this.handleCloseDialog}
               >
                            OK
                        </Button>
                    </DialogActions>
                </Dialog>
                <AppBar>
                    <Toolbar>
                        <Typography variant="h6" color="inherit">
                            TypeScript + Next.js + Material UI Sample
                        </Typography>
                    </Toolbar>
                </AppBar>
                <Typography variant="display1" gutterBottom={true}>
                    Material-UI
                </Typography>
                <Typography variant="subheading" gutterBottom={true}>
                    example project
                </Typography>
                <Typography gutterBottom={true}>
                    <Link href="/about">
                        <a>Go to the about page</a>
                    </Link>
                </Typography>
                <Button
                    variant="contained"
                    color="secondary"
                    onClick={this.handleClickShowDialog}
                >
                    Shot Dialog
                </Button>
                <style jsx={true}>{`
                    .root {
                        text-align: center;
                    }
                `}</style>
         </div>
       );
     }
   }

   export default withStyles(styles)(Index);

まずは、ReactのコンポーネントをTypeScriptで書くためのPropsやStateの型定義の渡し方ですね。Componentのパラメータとしてtypeを設定します。やっかいなのは、Material UIのスタイル用の機能です。テーマを元に少し手を加えればできる、という仕組みが実現されていますが、TypeScriptでやるには少々骨が折れます。それが ``styles`` 関数と ``withStyles(styles)`` の部分です。

まとめと、普段の開発
------------------------

これで一通り、Reactを使う環境ができました。BFF側にAPI機能を持たせたいとか、Reduxを使いたい、というのがあればここからまた少し手を加える必要があるでしょう。

開発はnpm run devで開発サーバーが起動し、ローカルのファイルの変更を見てホットデプロイとリロードを行ってくれます。

デプロイ時はnpm run buildとすると、.nextフォルダ内にコンテンツが生成されます。npm run buildの後に、npm run exportをすると、静的ファイルを生成することもできます。ただし、いくつか制約があったりしますので、ドキュメントをよくご覧ください。

Reactも、ここまでくればそんなに難しくないですよ。
