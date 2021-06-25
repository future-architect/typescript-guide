ブラウザ関連の組み込み型
===========================================

* ``fetch``
* ``FormData``
* ``EventListener``
* ``EventSource``\ と\ ``WebSocket``
* ``LocalStorage``\ と\ ``SessionStorage``

Polyfill、Ponyfill
-----------------------------------

``fetch``
----------------------------------------

確実にNode.jsだけでしか使われないコードであれば\ `node-fetch <https://www.npmjs.com/package/node-fetch>`_\ をインポートして利用すれば十分です。

もし、ブラウザでもサーバーでも実行されるコードの場合
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