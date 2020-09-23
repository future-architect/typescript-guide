====================================================
その他の組み込み型
====================================================

これまでの説明の中で、いくつかのデータの種類（ここでは誤解をおそれず、大雑把にクラスとしておきます）について説明してきました。

* プリミティブ型

  * ``boolean``
  * ``number``
  * ``string``\ と正規表現
  * ``undefined``\ と\ ``null``

* 複合型

  * ``Array``
  * ``Object``
  * ``Map``\ と\ ``WeakMap``
  * ``Set``\ と\ ``WeakSet``

* 関数

TypeScriptとJavaScriptはブラウザの中の言語として作られたため、数多くのブラウザ環境専用のクラスを備えていますが、それ以外にも言語の組み込みのクラスがいくつかありますので、本章ではそれらについて説明していきます。なお、\ ``Error``\ クラスについては\ :doc:`exception`\ で触れます。

``JSON``
========================

JavaScriptで外部のAPIのやりとりなどで一番使うのはこのJSONでしょう。サーバーから帰ってくるJSON形式の文字列を、プログラム中で扱いやすいJavaScriptやTypeScriptのプリミティブなデータ型などに変換します。

基本は\ ``parse()``\ と\ ``stringify()``\ を呼ぶだけですので使い方に迷うことはないでしょう。

JSONのパース
-------------------------

.. code-block:: ts

   // aはany型
   const a = JSON.parse(‘{"name": "John Cleese"}`);

   // asで型情報を付与できる。
   const p = JSON.parse(‘{"name": "Terry Gilliam"}`) as Person;


``parse()``\ は\ ``any``\ 型になります。\ ``as``\ で何かしらの型にキャストする必要がありますが、このパースは当然実行時に行われます。\ ``as``\ はコンパイル時の型チェックのためのものなので、実際に実行時にどのような型が来るかは推測でしかありません。このJSONのパース周りは、コンパイルは通ったのに、想定した型と違う情報がきたためにエラーになる、ということが一番起きやすいポイントです。\ ``as``\ は一見その型と同等であると保証しているように見せてしまいますが、要素の有無のチェックなどは動的な言語を扱っている意識を忘れないで行いましょう。

型定義をする必要がないかと言えば、明らかなスペルチェックは見つけられますし、補完もされるので、可能なら定義しておく方が良いでしょう。

``SyntaxError``\ 例外
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

この関数は、JSONの文法違反があると\ ``SyntaxError``\ 例外を投げます。TypeScriptで例外を扱うことは稀ですが、キャッチしないと何か操作したのに処理が行われていないように見えるなどの不具合になります。大々的にエラーダイアログが出たりはしないので気付きにくかったりしますが、コンソールには出力されていたりします。パースするときには\ ``try``\ でくくって、エラーが出たときにはダミーの値を入れるなり、自分でエラーダイアログを表示するなり、対処しましょう。

.. code-block:: ts

   let person: Person
   try {
       person = JSON.parse(input);
   } catch (e: unknown) {
       // fallback
       person = { name: "Eric Idle" };
   }

この関数は\ ``fetch()``\ の中でも使われています。例外の発生についてもまったく同じです。

.. code-block:: ts

   const res = await fetch("/api/person");
   // 本当はres.okで通信が成功したかチェックが必要！
   person = { name: "Michael Palin" };

HTTPのAPIの場合、エラーがあると、\ ``Forbidden``\ などのステータスコードの文字列がレスポンスとして帰ってくることがあり、これをJSONにパースしようとすると次のような例外が発生します。

.. code-block:: text

   Uncaught SyntaxError: Unexpected token F in JSON at position 0

ほとんどの場合はステータスコードのチェックで防げますが、try文を使うとさらに安心です。

JSONとコメント
~~~~~~~~~~~~~~~~~~~~~~~~~~~

JSONの厳格な文法（\ `json.org <https://json.org>`_\ ）にはコメントはありません。しかし、入れたくなることがあります。

TypeScriptの設定ファイルの\ ``tsconfig.json``\ や、VSCodeの設定ファイルなどはコメントが入れられます。前者はTypeScriptパーサーを流用したパーサーを使っていますので、TypeScriptと同じコメントが利用できます。後者はJSON with Comments(.jsonc)というモードを持っています。標準の\ ``JSON.parse()``\ は仕様に従っているのでコメントがあるとエラーになります。次のようなライブラリを使う必要があるでしょう。

* `strip-json-comments <https://www.npmjs.com/package/strip-json-comments>`_

設定ファイルとして使って読み手が自分自身だけならいいのですが、サーバーなどとのデータ交換用にJSONを使う場合、読み手がコメントを無視して読んでくれないかぎりはコメントを使うべきではありません。その他の方法としては、JSON Schemaの仕様にある\ ``$comment``\ キーを使うという妥協案もあります。

.. code-block:: json

   {
      "$comment": "コメントです",
      "location": "鳥貴族"
   }

文字列化
--------------------

文字列化はJavaScriptのオブジェクト、配列、数値、文字列、boolean型などの値を渡すと、それを安全に伝送できる文字列にしてくれます。

.. code-block:: ts
   :caption: JSON形式に文字列化

   // bは文字列
   const b = JSON.stringify({person: "Graham Chapman")
   // '{"person":"Graham Chapman"}'

``stringify()``\ には2つ追加の引数があります。1つは置換関数、もう1つはインデントです。

このうち置換関数は\ ``function(key: any, value: any): any``\ な関数で、キーと値を見て、実際に出力する値を決めますが、あまり使い勝手の良いものではありません。階層があったり、配列で同型のオブジェクトがあったりして、仮に同名のキーがあっても、渡される情報だけではどちらの値か区別できなかったりします。\ ``bigint``\ などの変換できない型の場合はreplacerが実行される前にエラーになってしまうため、この関数で出力できるように文字列にするといった使い方もできません。事前に出力可能なオブジェクト・配列・プリミティブだけのきれいな情報に変換しておくべきです。そのため、忘れてしまっても構いません。

インデント
~~~~~~~~~~~~~~~~~~~~~

デフォルトではインデントがなく、文字数最小で出力されます。インデントに数値、あるいは\ ``"    "``\ といった文字列を渡すことでインデントが行われて見やすくなります。ただし、Node.jsやブラウザの\ ``console.log()``\ の場合はインデントを設定しなくても見やすく表示してくれるため、整形してファイル出力したい場合以外は使う必要はないと思います。

.. code-block:: ts
   :caption: インデント

   const montyPython = {
       members: [
           "John Cleese",
           "Terry Gilliam",
           "Eric Idle",
           "Michael Palin",
           "Graham Chapman",
           "Terry Jones"
       ],
   };

   console.log(JSON.stringify(montyPython));
   // {"members":["John Cleese","Terry Gilliam","Eric Idle","Michael Palin","Graham Chapman","Terry Jones"]}

   console.log(JSON.stringify(montyPython, null, 2));
   // {
   //   "members": [
   //     "John Cleese",
   //     "Terry Gilliam",
   //     "Eric Idle",
   //     "Michael Palin",
   //     "Graham Chapman",
   //     "Terry Jones"
   //   ]
   // }

JSONとデータロス
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JSONは言語をまたいで使われるデータのシリアライズのための仕組みです。元はJavaScriptのオブジェクト表現をフォーマットにしたものではありますが（JSONは作成されたのではなく、発見されたと言われています）、いくつかTypeScriptと違うところもあります。

JSONは単純な木構造であり、TypeScriptのメモリ上の表現のすべてを表現できるわけではありません。例えば、親が子を、子が親を参照しているような循環構造の場合、うまく文字列化できず、エラーになります。事前に変換する関数を使って、子から親方向の参照を切った新しいオブジェクト階層を作るなどして単方向の参照になるようにします。

.. code-block:: ts
   :caption: 循環参照があるとTypeError

   const person = {name: "Terry Jones"};
   const group = {name: "Pythons", member: [person]};
   person.group = group; // お互いに参照しあっているため、循環参照になる
   
   JSON.stringify(group)
   // Uncaught TypeError: Converting circular structure to JSON

また、JSONが扱えるデータ型はそれほど多くありません。ネイティブで扱える型は以下の6つです。他のものはうまく文字列にならなかったり、なったとしても再度パースしたときにもとの型が復元できないことがあります。

* オブジェクト
* 配列
* 文字列
* 数値
* boolean型
* null

例えば\ ``undefined``\ の場合はそのキーがなかったことになります。クラスの場合はメンバーフィールドのみのオブジェクトになります。一応データとしては復元できますが、戻すときには単なるオブジェクトで、クラスのインスタンスではなくなります。各クラスに、オブジェクトからインスタンスを復元するファクトリーメソッドを用意してあげる必要があるでしょう。日付は文字列になります。これも、事前に\ ``valueOf()``\ で数値化しても良いでしょう。\ ``Map()``\ などは値が完全に失われたインスタンスになるため、注意が必要です。

.. code-block:: ts
   :caption: クラス、日付

   > class C { constructor() { this.a = 1; this.b = "hello"; } }
   > const i = new C();
   > JSON.stringify(i);
   // '{"a":1,"b":"hello"}'

   > JSON.stringify(new Date())
   // '"2020-09-15T14:41:37.173Z"'

   > const m = new Map([[1, 2], [2, 4], [3, 8]])
   // Map(3) { 1 => 2, 2 => 4, 3 => 8 }
   > JSON.stringify(m);
   // '{}'


``Date``
========================

日付と時間を扱うのが\ ``Date``\ 型です。これは最初期から実装されている型で、TypeScriptやJavaScriptで日付を扱う場合、まず出てくるのがこれです。ただし、即席で作られたこともあって評判がよくなく、大切な機能がいくつか抜け落ちていたり、文字列のパースが柔軟性がなかったりするため、いくつもの追加のモジュールなどが作られています。

以前は `moment.js <https://momentjs.com>`_ が長い間広く使われてきましたが、現在は\ `積極的な開発を中止する声明を出しています <https://momentjs.com/docs/#/-project-status/>`_\ 。そのmoment.jsの声明の中で推奨されているのが次のライブラリです。

* `Luxon <https://moment.github.io/luxon/>`_ (型定義は別に ``npm install @types/luxon`` が必要)
* `Day.js <https://day.js.org/>`_ (TypeScript型定義同梱)
* `date-funs <https://date-fns.org/>`_ (TypeScript型定義同梱)
* `js-Joda <https://js-joda.github.io/js-joda/>`_ (TypeScript型定義同梱)

より便利なフォーマットやパース、日時演算などはこちらのパッケージを利用すると簡単に行えます。

JavaScript本体においても、\ ``Date``\ を置き換える\ ``Temporal``\ が提案されています。

* https://github.com/tc39/proposal-temporal

将来的に、ここの説明は\ ``Temporal``\ ベースで書き換えられると思いますが、ひとまずここでは\ ``Date``\ のよくある使い方について紹介していきます。

TypeScriptの\ ``Date``\ 型は数字に毛の生えたようなものですので、それを前提にみていくと良いと思います。

現在時刻の取得・エポック時刻
-------------------------------

``new Date()``\ で簡単に作成できます。コンピュータに保存されているタイムゾーンの情報も含んだ、\ ``Date``\ のインスタンスが作成できます。

.. code-block:: ts

   // 現在時刻でDateのインスタンス作成
   const now = new Date();
   // newを付けないと文字列として帰ってくる
   const nowStr = Date();
   // 'Sun Sep 06 2020 22:36:08 GMT+0900 (Japan Standard Time)'

コンピュータの世界ではUNIX時刻、あるいはUNIX秒、エポック（Epoch）秒、エポック時刻と呼ばれるものがよく使われます。これは1970年1月1日（UTC基準）からの経過時間で時間を表すものです。JavaScriptの中ではミリ秒単位であって秒ではないため、本章ではエポック時刻という名前で統一します。

.. code-block:: ts

   // ミリ秒単位のエポック時刻取得
   const now = Date.now();

``console.time()``\ と\ ``console.timeEnd()``\ でも時間計測ができますが、何かしらの処理の間の時間を撮りたい場合には、\ ``Date.now()``\ を複数回呼び出すことで、ミリ秒単位で時間が計測できます。ブラウザでは\ ``performance.now()``\ という高精度タイマーがありましたが、セキュリティの懸念もあって現在は精度が落とされていますので、\ ``Date.now()``\ とあまり差はないでしょう。

.. code-block:: ts

   const start = Date.now();
   //  :
   // 時間のかかる処理
   //  :
   const duration = Date.now() - start;
   // 経過時間（ミリ秒）の取得

このエポック時刻から\ ``Date``\ のインスタンスにする場合は\ ``new Date()``\ の引数にミリ秒単位の時間を入れます。逆に、\ ``Date()``\ のインスタンスからエポック時刻を取得するには\ ``valueOf()``\ メソッドを使います。

.. code-block:: ts

   // 現在の時刻から100秒（10万ミリ秒）前の時刻の取得
   const hundredSecAgo = new Date(Date.now() - 100 * 1000);

   // エポック時刻取得
   const epoch = hundredSecAgo.valueOf();

さまざまな時間の情報がありますが、TypeScriptではどれを基準に扱うべきでしょうか？ブラウザはユーザーインタフェースであるため、ユーザーの利用環境のタイムゾーン情報を持っています。しかし、多くのユーザーの情報を同時に扱うサーバーではタイムゾーン情報も含めて扱うのは手間隙がかかります。データベースエンジンによってはタイムゾーン込みの時刻も扱いやすいものもあったりはしますが、シンプルに扱うためには以下の指針で大部分のシステムはまかなえるでしょう。

* クライアントで時刻を取得してサーバーに送信するときは、\ ``Date().now``\ などでエポック時刻にしてからサーバーに送信する（タイムゾーン情報なし）
* サーバーでは常にエポック時刻で扱う（ただし、言語によっては秒単位だったり、ミリ秒単位だったり、マイクロ秒単位だったり違いはあるため、そこはルールを決めておきましょう）
* サーバーからフロントに送った段階で\ ``new Date()``\ などを使って、ローカル時刻化する

特定の日時の\ ``Date``\ インスタンスの作成
-----------------------------------------------------

特定の日時インスタンスを作成するには、\ ``Date()``\ コンストラクタの引数に数値を設定して作成します。月の数値が1少なく評価される（1月は0）な点に注意が必要です。この日時は現在のタイムゾーンで評価されます。

.. code-block:: ts

   // 2020年9月21日21時10分5秒
   // 日本で実行すると日本時間21時（UTCでは9時間前の12時）に
   const d = new Date(2020, 8, 21, 21, 10, 5)

UTCの時刻から生成したい場合には、\ ``Date.UTC()``\ 関数を使います。これはエポック秒を返すのでこれを\ ``new Date()``\ に渡すことで、UTC指定の時刻のインスタンスが作成できます。

.. code-block:: ts

   // UTCの2020年9月21日11時10分5秒
   // 日本で実行すると日本時間20時（日本時間はUTCは9時間進んでいるように見える）に
   const d = new Date(Date.UTC(2020, 8, 21, 11, 10, 5))

日付のフォーマット出力
-------------------------------------------

:RFC:`3393`\ 形式にするには、\ ``toISOString()``\ メソッドを使います。\ ``toString()``\ だとECMAScriptの仕様書で定められたロケール情報も含む文字列で出力を行ます。後者の場合、ミリ秒単位のデータは丸められてしまいます。

.. code-block:: ts

   const now = new Date()
   now.toISOString()
   // '2020-09-21T12:38:15.655Z'

   now.toString()
   // 'Mon Sep 21 2020 21:38:15 GMT+0900 (Japan Standard Time)'

短い形式やオリジナルの形式にするには自分でコードを書く必要があります。短く日時を表現しようとする場合のコードは次のようになります。月のみカレンダーの表記と異なって、0が1月になる点に注意してください。

.. code-block:: ts

   const str = `${
       now.getFullYear()
   }/${
       String(now.getMonth() + 1).padStart(2, '0')
   }/${
       String(now.getDate()).padStart(2, '0')
   } ${
       String(now.getHours()).padStart(2, '0')
   }:${
       String(now.getMinutes()).padStart(2, '0')
   }:${
       String(now.getSeconds()).padStart(2, '0')
   }`;
   // "2020/09/06 13:55:43"

``padStart()``\ と、テンプレート文字列のおかげで、以前よりははるかに書きやすくなりましたが、Day.jsなどの提供するフォーマット関数を使った方が短く可読性も高くなるでしょう。

日付データの交換
-------------------

クライアントとサーバーの間ではJSONなどを通じてデータをやりとりします。JSONでデータを転送するときは数値か文字列で表現する必要があります。日付データは既に説明した通りに、ミリ秒か秒のどちらかの数値で交換するのがもっともコード的には少ない配慮で実現できます。しかし、一方で出力された数字の列を見ても、即座に現在の日時を暗算できる人はいないでしょう。可読性という点では文字列を使いたいこともあるでしょう。本節ではデータをやりとりする相手ごとのデータ変換の仕方について詳しく説明していきます。

TypeScript（含むJavaScript同士）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TypeScript（含むJavaScript）であれば、\ ``toISOString()``\ でも、\ ``toString()``\ でも、どちらの方式で出力した文字列であってもパースできます。\ ``new Date()``\ に渡すと\ ``Date``\ のインスタンスが、\ ``Date.parse()``\ に渡すと、エポック時刻が帰ってきます。

.. code-block:: ts

   const fromToISOString = new Date(`2020-09-21T12:38:15.655Z`)
   // 2020-09-21T12:38:15.655Z
   
   const fromToString = new Date(`Mon Sep 21 2020 21:38:15 GMT+0900 (Japan Standard Time)`)
   // 2020-09-21T12:38:15.000Z

   const fromToISOStringEpoch = Date.parse(`2020-09-21T12:38:15.655Z`)
   // 1600691895655

   const fromToStringEpoch = Date.parse(`Mon Sep 21 2020 21:38:15 GMT+0900 (Japan Standard Time)`)
   // 1600691895000

Goとの交換の場合
~~~~~~~~~~~~~~~~~~~~~~~~

Goでは日付のフォーマットが何種類か選べますが、このうち、タイムゾーンの時差が数値で入っているフォーマットはTypeScriptでパース可能です。ナノ秒の情報がミリ秒に丸められてしまいますが、一番精度良く伝達できるのは\ ``time.RFC3339Nano``\ の出力です。

* ``time.RubyDate``
* ``time.RFC822Z``
* ``time.RFC1123Z``
* ``time.RFC3339``
* ``time.RFC3339Nano``

.. code-block:: go
   :caption: GoでRFC3339Nanoで出力

   package main

   import (
       "fmt"
       "time"
   )

   func main() {
       now := time.Now()
       fmt.Println(now.Format(time.RFC3339Nano))
       // 2020-09-21T21:35:45.057076+09:00
   }

.. code-block:: ts
   :caption: TypeScriptでパース

   const receivedFromGo = new Date(`2020-09-21T21:35:45.057076+09:00`)
   // 2020-09-21T12:35:45.057Z

他の言語に出力する場合、\ ``toISOString()``\ が無難でしょう。Goは\ ``time.RFC3339``\ か、\ ``time.RFC3339Nano``\ を使ってパースできます。結果はどちらも同じです。

.. code-block:: go

   package main

   import (
       "fmt"
       "time"
   )

   func main() {
       t, err := time.Parse(time.RFC3339, "2020-09-21T12:38:15.655Z")
       fmt.Println(t)
       // 2020-09-21 12:38:15.655 +0000 UTC
   }

Pythonとの交換の場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pythonで出力する場合は\ ``datetime.datetime.isoformat()``\ メソッドを使うと良いでしょう。このメソッドはタイムゾーン情報を取り払い、現在のタイムゾーンの表記そのものをフォーマットして出力します。TypeScriptの\ ``new Date()``\ はUTCであることを前提としてパースするため、出力時はUTCとして出すように心がける必要があります。このUTCで出力された文字列はTypeScriptでパースできます。

.. code-block:: python

   from datetime import datetime, timezone

   # localの場合はastimezone()を呼んでUTCに
   localtime = datetime.now()
   utctime = localtime.astimezone(timezone.utc)
   utctime.isoformat()
   # 2020-09-21T13:42:58.279772+00:00

   # あるいは、最初からUTCで扱う
   utctime = datetime.utcnow()
   utctime.isoformat()
   # 2020-09-21T13:42:58.279772+00:00

パースはやっかいです。Stack Overflowでスレッドが立つぐらいのネタです\ [#]_\ 。Python 3.7からは\ ``fromisoformat()``\ というクラスメソッドが増えましたが、以前からの\ ``datetime.strptime()``\ にフォーマット指定を与えた方が高速とのことです。

.. code-block:: python

   from datetime import datetime

   s = '2020-09-21T12:38:15.655Z'

   datetime.fromisoformat(s.replace('Z', '+00:00'))
   # datetime.datetime(2020, 9, 21, 12, 38, 15, 655000, tzinfo=datetime.timezone.utc)

   datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%f%z')
   # datetime.datetime(2020, 9, 21, 12, 38, 15, 655000, tzinfo=datetime.timezone.utc)

いっそのこと、エポック時刻で扱う方法の方がシンプルでしょう。TypeScriptはミリ秒単位で、Pythonは秒単位なので、1000で割ってから渡す必要があるのと、UTCの数値であることを明示する必要があります。

.. code-block:: python

   from datetime import datetime
   datetime.fromtimestamp(1600691895655 / 1000.0, timezone.utc)
   # datetime.datetime(2020, 9, 21, 12, 38, 15, 655000, tzinfo=datetime.timezone.utc)

.. [#] https://stackoverflow.com/questions/127803/how-do-i-parse-an-iso-8601-formatted-date

Javaとの交換の場合(8以降)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Java8から標準になったクラス群\ [#]_\ を使ってTypeScriptとの交換を行ってみます。ここで紹介するコードはJava8以降で動作するはずです。このサンプルはJava 11で検証しています。

``Date.toISOString()``\ と同等の出力は\ ``DateTimeFormatter``\ で作成できます。UTCのゾーンになるようにインスタンスを作成してから\ ``format()``\ メソッドを使って変換します。

.. code-block:: java

   import java.time.Instant;
   import java.time.ZonedDateTime;
   import java.time.ZoneId;
   import java.time.format.DateTimeFormatter;

   class ParseTest {
       public static void main(String[ ] args) {
           var RFC3339_FORMAT = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");

           var l = ZonedDateTime.now();
           var isoString = l.withZoneSameInstant(ZoneOffset.UTC).format(RFC3339_FORMAT);
           System.out.println(isoString);
           // "2020-09-23T13:55:53.780Z"
        }
   }

この文字列はTypeScriptでパースできます。

TypeScriptで生成した文字列のパースには前述の\ ``DateTimeFormatter``\ も使えますが、それ以外には\ ``java.time.Instant``\ が使えます。これはある時点での時刻を表すクラスです。TypeScriptの\ ``Date.toISOString()``\ の出力する文字列をパースできます。実際に日時の操作を行う\ ``LocalDateTime``\ や\ ``ZonedDateTime``\ へも、ここから変換できます。次のサンプルは\ ``Instant``\ でパースし、\ ``ZonedDateTime``\ に変換しています。

.. code-block:: java

   import java.time.Instant;
   import java.time.ZonedDateTime;
   import java.time.ZoneId;
   import java.time.format.DateTimeFormatter;

   class ParseTest {
       public static void main(String[ ] args) {
           var i = Instant.parse("2020-09-23T14:06:11.027Z");
           var l = ZonedDateTime.ofInstant(i, ZoneId.systemDefault());

           var f = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
           System.out.println(l.format(f));
       }
   }

.. [#] `Java8の日時APIはとりあえずこれだけ覚えとけ <https://qiita.com/tag1216/items/91a471b33f383981bfaa>`_
