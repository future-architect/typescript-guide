# -*- coding: utf-8 -*-
"""技術ブログ（future-architect.github.io）のライト用のコード配色。

色は役で持つ。役と色相の対応はテーマで変わるので、赤・緑のような名前にしない。
値はブログの _variables.styl から引き写している。
"""

from pygments.style import Style
from pygments.token import (Comment, Error, Generic, Keyword, Literal, Name,
                            Number, Operator, Other, Punctuation, String, Text,
                            Token, Whitespace)

FG = '#24292E'       # 地の文
COMMENT = '#656D77'  # コメント・区切り記号・プロンプト・引用
KEYWORD = '#CE2A3A'  # キーワード・組み込み・引数
TYPE = '#6F42C1'     # 型名・関数名・アノテーション
STRING = '#032F62'   # 文字列・文字リテラル
NUMBER = '#005CC5'   # 数値・リテラル
ATTR = '#B44E07'     # 名前と値の組の「名前」（YAML・JSON のキー）
TAG = '#207C36'      # タグ・属性・変数・正規表現・CSS のセレクタ


class FutureLightStyle(Style):
    background_color = '#f5f5f5'
    line_number_color = '#757575'
    line_number_background_color = '#f5f5f5'

    styles = {
        Token:              FG,
        Text:               FG,
        Whitespace:         '',
        Other:              FG,
        Error:              KEYWORD,   # 既定は赤い枠。本文に70箇所あり箱が目立つので色だけにする

        Comment:            COMMENT,
        Comment.Preproc:    KEYWORD,
        Punctuation:        COMMENT,
        Operator:           FG,
        Operator.Word:      KEYWORD,

        Keyword:            KEYWORD,
        Keyword.Type:       TYPE,
        Keyword.Constant:   NUMBER,

        Name:               FG,
        Name.Builtin:       KEYWORD,
        Name.Builtin.Pseudo: KEYWORD,
        Name.Class:         TYPE,
        Name.Function:      TYPE,
        Name.Decorator:     TYPE,
        Name.Namespace:     TYPE,
        Name.Exception:     TYPE,
        Name.Attribute:     ATTR,
        Name.Tag:           TAG,
        Name.Variable:      TAG,
        Name.Constant:      NUMBER,
        Name.Label:         ATTR,

        String:             STRING,
        String.Escape:      NUMBER,
        String.Interpol:    NUMBER,
        String.Regex:       TAG,

        Number:             NUMBER,
        Literal:            NUMBER,

        Generic.Deleted:    KEYWORD,
        Generic.Inserted:   TAG,
        Generic.Heading:    'bold ' + TYPE,
        Generic.Subheading: 'bold ' + TYPE,
        Generic.Prompt:     COMMENT,
        Generic.Output:     FG,
        Generic.Emph:       'italic',
        Generic.Strong:     'bold',
        Generic.Error:      KEYWORD,
        Generic.Traceback:  KEYWORD,
    }
