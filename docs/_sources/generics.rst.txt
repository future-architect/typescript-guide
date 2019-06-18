ジェネリクス
===================

.. note::

   書き書け

ジェネリクスは、使われるまで型が決まらないような機能を作るときに使います。ジェネリクスは日本語で総称型と呼ばれることもあります。

``any`` や ``unknown`` との違い
-----------------------------------------

型が未知の場合というと、 ``any`` や ``unknown`` が思いつくでしょう。

これらの変数に値を設定してしまうと、型情報がリセットされます。取り出すときに、適切な型を宣言してあげないと、その後のエラーチェックが無効になったり、エディタの補完ができません。

次の関数は、初回だけ指定の関数を読んで値を取って来るが、2回目以降は保存した値をそのまま返す関数です。初回アクセスまで初期化を遅延させます。

.. code-block:: ts
   :caption: any版の遅延初期化関数

   function lazyInit(init: () => any): () => any {
     let cache: any;
     let isInit = false;
     return function(): any {
       if (!isInit) {
         cache = init();
       } 
       return cache;
     }
   }

``any`` 版を使って見たのが次のコードです。

.. code-block:: ts
   :caption: 非ジェネリック版の使い方

   const getter = lazyInit(() => "initialized");
   const value = getter();
   // valueはany型なので、上記のvalueの後ろで.をタイプしてもメソッド候補はでてこない

この場合、 ``cache`` ローカル変数に入っているのは文字列ですし、 ``value`` にも文字列が格納されます。
しかし、TypeScriptの処理系は ``any`` に入るだけで補完をあきらめてしまいます。

次のジェネリクス版を紹介します。型を関数の引数のように記述します。場所は関数、インタエース、クラスの名前の前に付きます。 この ``T`` には型が入ります。
``T`` は実際に使うときに、全て同じ型名がここに入ります。 ``string`` などを入れることができます。

.. code-block:: ts
   :caption: any版の遅延初期化関数

   function <T>lazyInit(init: () => T): () => T {
     let cache: T;
     let isInit = false;
     return function(): T {
       if (!isInit) {
         cache = init();
       } 
       return cache;
     }
   }

.. code-block:: ts
   :caption: ジェネリック版の使い方

   const getter = lazyInit<string>(() => "initialized");
   const value = getter();
   // valueはany型なので、上記のvalueの後ろで.をタイプしてもメソッド候補はでてこない
