ブラウザ関連の組み込み型
===========================================

* ``fetch``
* ``FormData``
* ``EventListener``
* ``EventSource``\ と\ ``WebSocket``
* ``LocalStorage``\ と\ ``SessionStorage``

Polyfill、Ponyfill
-----------------------------------

``fetch()``
----------------------------------------

Node.js 18からは標準で組み込まれました。2022年10月にLTSになった以降は特に設定せずに利用できます。

クラウドのランタイムなど、それ以前のバージョンを扱う必要があれば追加のパッケージが必要です。

確実にNode.jsだけでしか使われないコードであれば\ `node-fetch <https://www.npmjs.com/package/node-fetch>`_\ をインポートして利用すれば十分です。

もし、ブラウザでもサーバーでも実行されるコードを書く必要があれば、次のパッケージを利用すると、Node.js環境ではPolyfillが使われ、ブラウザではネイティブの ``fetch()`` 関数が利用されます。

https://www.npmjs.com/package/isomorphic-unfetch
https://www.npmjs.com/package/isomorphic-fetch
https://www.npmjs.com/package/fetch-ponyfill

``FormData``
----------------------------------------

https://www.npmjs.com/package/form-data

``EventListener``
----------------------------------------

``EventSource``\ と\ ``WebSocket``
----------------------------------------

https://www.npmjs.com/package/eventsource
https://www.npmjs.com/package/ws
https://www.npmjs.com/package/isomorphic-ws

``LocalStorage``\ と\ ``SessionStorage``
----------------------------------------


https://www.npmjs.com/package/localstorage-memory
https://www.npmjs.com/package/node-localstorage