関数
==================

関数の定義、使い方などもいろいろ変わりました。表現したい機能のために、ややこしい直感的でないコードを書く必要性がかなり減っています。

アロー関数
----------------------

JavaScriptでは、やっかいなのが\ ``this``\ です。無名関数をコールバック関数に渡そうとすると、\ ``this``\ がわからなくなってしまう問題があります。
アロー関数を使うと、その関数が定義された場所の\ ``this``\ の保持までセットで行いますので、無名関数の\ ``this``\ 由来の問題をかなり軽減できます。
表記も短いため、コードの幅も短くなり、コールバックを多用するところで ``function`` という長いキーワードが頻出するのを減らすことができます。

.. code-block:: ts
   :caption: アロー関数

   // アロー関数ならその外のthisが維持される。
   this.button.addEventListener("click", () => {
     this.smallAnimal.walkTo("タコ公園");
   });

アロー関数にはいくつかの記法があります。
引数が1つの場合は引数のカッコを、式の結果をそのまま ``return`` する場合は式のカッコを省略できます。
ただし、引数の場所に型をつけたい場合は省略するとエラーになります。

.. code-block:: ts
   :caption: アロー関数の表記方法のバリエーション

   // 基本形
   (arg1, arg2) => { /* 式 */ };

   // 引数が1つの場合は引数のカッコを省略できる
   // ただし型を書くとエラーになる
   arg1 => { /* 式 */ };

   // 引数が0の場合はカッコが必要
   () => { /* 式 */ };

   // 式の { } を省略すると、式の結果が return される
   arg => arg * 2;

   // { } をつける場合は、値を返すときは return を書かなければならない
   arg => {
     return arg * 2;
   };

以前は、 ``this`` がなくなってしまうため、 ``bind()`` を使って束縛したり、別の名前（ここでは ``self`` ）に退避する必要がありました。
そのため、\ ``var self = this;``\ と他の変数に退避するコードがバッドノウハウとして有名でした。

.. code-block:: ts
   :caption: this消失を避ける古い書き方

   // 旧: 無名関数のイベントハンドラではその関数が宣言されたところのthisにアクセスできない
   var self=this;
   this.button.addEventListener("click", function() {
     self.smallAnimal.walkTo("タコ公園");
   });

   // 旧: bind()で現在のthisに強制束縛
   this.button.addEventListener("click", (function() {
     this.smallAnimal.walkTo("タコ公園");
   }).bind(this));

関数の引数と返り値の型定義
----------------------------------

TypeScriptでは関数やクラスのメソッドでは引数や返り値に型を定義できます。
元となるJavaScriptで利用できる、すべての書き方に対応しています。

なお、Javaなどとは異なり、同名のメソッドで、引数違いのバリエーションを定義するオーバーロードは使えません。

.. code-block:: ts
   :caption: 関数への型付け

   // 昔からあるfunctionの引数に型付け。書く引数の後ろに型を書く。
   // 返り値は引数リストの () の後に書く。
   function checkFlag(flag: boolean): string {
     console.log(flag);
     return "check done";
   }

   // アロー関数も同様
   const normalize = (input: string): string => {
     return input.toLowerCase();
   }

変数の宣言のときと同じように、型が明確な場合には省略が可能です。

.. code-block:: ts
   :caption: 関数への型付け

   // 文字列のtoLowerCase()メソッドの返り値は文字列なので
   // 省略してもstringが設定されたと見なされる
   const normalize = (input: string) => {
     return input.toLowerCase();
   }

   // 文字配列の降順ソート
   // ソートに渡される比較関数の型は、配列の型から明らかなので省略してもOK
   // 文字列のtoLowerCase()メソッドも、エディタ上で補完が効く
   const list: string[] = ["小学生", "小心者", "小判鮫"];
   list.sort((a, b) => {
     if (a.toLowerCase() < b.toLowerCase()) {
       return 1;
     } else if (a.toLowerCase() > b.toLowerCase()) {
       return -1;
     }
     return 0;
   });

関数が何も返さない場合は、 ``: void`` をつけることで明示的に表現できます。
実装したコードで何も返していなければ、自動で ``: void`` がついているとみなされますが、これから先で紹介するインタフェースや抽象クラスなどで、関数の形だけ定義して実装を書かないケースでは、どのように判断すればいいのか材料がありません。 ``compilerOptons.noImplicitAny`` オプションが ``true`` の場合には、このようなケースで ``: void`` を書かないとエラーになりますので、忘れずに書くようにしましょう。

.. code-block:: ts
   :caption: 何も返さない時はvoid

   function hello(): void {
     console.log("ごきげんよう");
   }

   interface Greeter {
     // noImplicitAny: trueだとエラー
     // error TS7010: 'hello', which lacks return-type annotation,
     //    implicitly has an 'any' return type.
     hello();
   }

要注意なのは、レスポンスの型が一定しない関数です。
次の関数は、2019が指定された時だけ文字列を返します。
この場合、TypeScriptが気を利かせて ``number | '今年'`` という返り値の型を暗黙でつけてくれます。
しかしこの場合、単純な ``number`` ではないため、 ``number`` 型の変数に代入しようとするとエラーになります。

ただ、このように返り値の型がバラバラな関数を書くことは基本的にないでしょう。
バグを生み出しやすくなるため、返り値の型は特定の型1つに限定すべきです。
バリエーションがあるとしても、 ``| null`` をつけるぐらいにしておきます。

内部関数で明らかな場合は省略しても問題ありませんが、公開関数の場合はなるべく省略をやめた方が良いでしょう。

.. code-block:: ts

   // 返り値の型がたくさんある、行儀の悪い関数
   function yearLabel(year: number) {
     if (year === 2019) {
       return '今年';
     }
     return year;
   }

   const label: number = yearLabel(2018);
   //  error TS2322: Type 'number | "今年"' is not assignable to type 'number'.
   //    Type '"今年"' is not assignable to type 'number'.

関数を扱う変数の型定義
------------------------------

関数に型をつけることはできるようになりました。
次は、その関数を代入できる変数の型を定義して見ましょう。

例えば、文字列と数値を受け取り、booleanを返す関数を扱いたいとします。その関数は ``check`` という変数に入れます。
その場合は次のような宣言になります。
引数はアロー関数のままですが、返り値だけは ``=>`` の右につけ、 ``{ }`` は外します。
型定義ではなく、実際のアロー関数の定義の返り値は ``=>`` の左につきます。
ここが逆転する点に注意してください。

.. code-block:: ts

   let check: (arg1: string, arg2: number) => boolean;

``arg2`` がもし関数であったら、関数の引数の中に関数が出てくるということで、入れ子の宣言になります。
多少わかりにくいのですが、内側から順番に剥がして理解していくのがコツです。

.. code-block:: ts

   let check: (arg1: string, arg2: (arg3: string) => number) => boolean;

サンプルとしてカスタマイズ可能なソート関数を作りました。
通常のソートだと、すべてのソートを行うためになんども比較関数が呼ばれます。
大文字小文字区別なく、A-Z順でソートしたいとなると、その変換関数が大量に呼ばれます。
本来は1要素につき1回ソートすれば十分なはずです。それを実装したのが次のコードです。

まず、変換関数を通しながら、 ``[オリジナル, 比較用に変換した文字列]`` という配列を作ります。
その後、後半の変換済みの文字列を使ってソートを行います。
最後に、そのソートされた配列を使い、オリジナルの配列に含まれていた要素だけの配列を再び作成しています。

.. code-block:: ts
   :caption: 一度だけ変換するソート

   function sort(a: string[], conv: (value: string) => string) {
     const entries = a.map((value) => [value, conv(value)])
     entries.sort((a, b) => {
       if (a[1] > b[1]) {
         return 1;
       } else if (a[1] < b[1]) {
         return -1;
       }
       return 0;
     });
     return entries.map(entry => entry[0]);
   }

   const a: string[] = ["a", "B", "D", "c"];
   console.log(sort(a, s => s.toLowerCase()))
   // ["a", "B", "c", "D"]

デフォルト引数
----------------------

TypeScriptは、他の言語と同じように関数宣言のところに引数のデフォルト値を簡単に書くことができます。
また、TypeScriptは型定義通りに呼び出さないとエラーになるため、引数不足や引数が過剰になる、というエラーチェックも不要です。

.. code-block:: js

   // 新しいデフォルト引数
   function f(name="小動物", favorite="小豆餅") {
     console.log(`${name}は${favorite}が好きです`);
   }
   f(); // 省略して呼べる

オブジェクトの分割代入を利用すると、デフォルト値つきの柔軟なパラメータも簡単に実現できます。
以前は、オプショナルな引数は\ ``opts``\ という名前のオブジェクトを渡すこともよくありました。
今時であれば、完全省略時でもデフォルト値が設定されるし、部分的に設定も可能みたいな引数が次のように書けます。

.. code-block:: js

   // 分割代入を使って配列やオブジェクトを変数に展開＆デフォルト値も設定
   // 最後の={}がないとエラーになるので注意
   function f({name="小動物", favorite="小豆餅"}={}) {
       :
   }

JavaScriptは同じ動的言語のPythonとかよりもはるかにゆるく、引数不足でも呼び出すこともでき、その場合には変数に\ ``undefined``\ が設定されました。
``undefined``\ の場合は省略されたとみなして、デフォルト値を設定するコードが書かれたりしました。
どの引数が省略可能で、省略したら引数を代入しなおしたり・・・とか面倒ですし、同じ型の引数があったら判別できなかったりもありますし、関数の先頭行付近が引数の処理で1画面分埋まる、ということも多くありました。
また、可変長引数があってもコールバック関数がある場合は必ず末尾にあるというスタイルが一般的でしたが、この後に説明する\ ``Promise``\ を返す手法が一般的になったので、こちらも取扱いが簡単になりました。

.. code-block:: js

   // デフォルト引数の古いコード
   function f(name, favorite) {
       if (favorite === undefined) {
           favorite = "小豆餅";
       }
   }

   // 古くてやっかいな、コールバック関数の扱い
   function f(name, favorite, cb) {
       if (typeof favorite === "function") {
           cb = favorite;
           favorite = undefined;
       }
       :
   }

関数を含むオブジェクトの定義方法
----------------------------------------

ES2015以降、関数や定義の方法が増えました。
JavaScriptではクラスを作るまでもない場合は、オブジェクトを作って関数をメンバーとして入れることがありますが、それが簡単にできるようになりました。
setter/getterの宣言も簡単に行えるようになりました。

.. code-block:: js
   :caption: 関数を含むオブジェクトの定義方法

   // 旧: オブジェクトの関数
   var smallAnimal = {
      getName: function() {
        return "小動物";
      }
   };
   // 旧: setter/getter追加
   Object.defineProperty(smallAnimal, "favorite", {
     get: function() {
       return this._favorite;
     },
     set: function(favorite) {
       this._favorite = favorite;
     }
   });

   // 新: オブジェクトの関数
   //     functionを省略
   //     setter/getterも簡単に
   const smallAnimal = {
     getName() {
       return "小動物"
     },
     _favorite: "小笠原",
     get favorite() {
       return this._favorite;
     },
     set favorite(favorite) {
       this._favorite = favorite;
     }
   };

``this``\ を操作するコードは書かない（1）
--------------------------------------------------

読者のみなさんはJavaScriptの\ ``this``\ が何種類あるか説明できるでしょうか？
``apply()``\ や\ ``call()``\ で実行時に外部から差し込み、何も設定しない（グローバル）、\ ``bind()``\ で固定、メソッドのピリオドの右辺が実行時に設定、といったバリエーションがあります。
これらの\ ``this``\ の違いを知り、使いこなせるのがかつてのJavaScript上級者でしたが、このようなコードはなるべく使わないように済ませたいものです。

無名関数で\ ``this``\ がグローバル変数になってはずれてしまうのはアロー関数で解決できます。

``apply()``\ は、関数に引数セットを配列で引き渡したいときに使っていました。
配列展開の文法のスプレッド構文\ ``...``\ を使うと、もっと簡単にできます。

.. code-block:: js

   function f(a, b, c) {
       console.log(a, b, c);
   }
   const params = [1, 2, 3];

   // 旧: a=1, b=2, c=3として実行される
   f.apply(null, params);

   // 新: スプレッド構文を使うと同じことが簡単に行える
   f(...params);

``call()``\ は配列の\ ``push()``\ メソッドのように、引数を可変長にしたいときに使っていました。
関数の中では\ ``arguments``\ という名前のちょっと配列っぽいオブジェクトです。
ちょっと使いにくいので、一旦本物の配列にする時に\ ``call()``\ を使って配列のメソッドを\ ``arguments``\ に適用するハックがよく利用されていました。
これも引数リスト側にスプレッド構文を使うことで本体にロジックを書かずに実現できます。

.. code-block:: js

   // 旧: 可変長配列の古いコード
   function f(a, b) {
       // この2は固定引数をスキップするためのもの
       var list = Array.prototype.slice.call(arguments, 2);
       console.log(a, b, list);
   }
   f(1, 2, 3, 4, 5, 6);
   // 1, 2, [3, 4, 5, 6];

   // 新: スプレッド構文。固定属性との共存もラクラク
   const f = (a, b, ...c) => {
       console.log(a, b, c);
   };
   f(1, 2, 3, 4, 5, 6);
   // 1, 2, [3, 4, 5, 6];

ただし、jQueryなどのライブラリでは、\ ``this``\ がカレントのオブジェクトを指すのではなく、選択されているカレントノードを表すという別解釈を行います。
使っているフレームワークが特定の流儀を期待している場合はそれに従う必要があります。

``bind()``\ の排除はクラスの中で紹介します。

即時実行関数はもう使わない
------------------------------------

関数を作ってその場で実行することで、スコープ外に非公開にしたい変数などが見えないようにするテクニックがかつてありました。即時実行関数と呼びます。
``function(){}``\ をかっこでくくって、その末尾に関数呼び出しのための\ ``()``\ がさらに付いています。これで、エクスポートしたい特定の変数だけを\ ``return``\ で返して公開をしていました。
今時であれば、公開したい要素に明示的に\ ``export``\ をつけると、webpackなどのツールがそれ以外の変数をファイル単位のスコープで隠してくれます。

.. code-block:: js
   :caption: 古いテクニックである即時実行関数

   var lib = (function() {
     var libBody = {};
     var localVariable;

     libBody.method = function() {
       console.log(localVariable);
     }
     return libBody;
   })();

まとめ
-----------

関数についてさまざまなことを紹介してきました。

* アロー関数
* 関数の引数と返り値の型定義
* 関数を扱う変数の型定義
* デフォルト引数
* 関数を含むオブジェクトの定義方法
* thisを操作するコードは書かない（1）
* 即時実行関数はもう使わない

省略、デフォルト引数など、JavaScriptでは実現しにくかった機能も簡単に実装できるようになりました。
関数は、TypeScriptのビルディングブロックのうち、大きな割合をしめています。
近年では、関数型言語の設計を一部取り入れ、堅牢性の高いコードを書こうというムーブメントが起きています。
ここで紹介した型定義をしっかり行うと、その関数型スタイルのコードであっても正しく型情報のフィードバックされますので、ぜひ怖がらずに型情報をつけていってください。

関数型志向のプログラミングについては後ろの方の章で紹介します。