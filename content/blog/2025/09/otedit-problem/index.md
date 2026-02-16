+++
title = "フォント編集ソフト OTEdit問題"
description = "フォント編集ソフト「OTEdit」で作成されたフォントの空グリフ問題について解説。Adobe-Japan1文字集合選択時に発生する空グリフによりフォールバック機能が正常に動作しない問題と、Pythonスクリプトを使った修正方法を紹介。"
date = 2025-09-20
aliases = ["/articles/2025/09/20/otedit-problem"]

[taxonomies]
tags = ["Design","Font", "Tech","Python"]
[extra]
social_media_card = "ogp.webp"
+++

<details>
<summary>Table of Contents</summary>
  <!-- toc -->
</details>

フォント編集ソフト「OTEdit」で作成されたフォントの空グリフ問題について解説。Adobe-Japan1文字集合選択時に発生する空グリフによりフォールバック機能が正常に動作しない問題と、Pythonスクリプトを使った修正方法を紹介。

## OTEditとは

**OTEdit**とは、[武蔵システム](https://opentype.jp/)が販売する
OpenTypeフォントを作成・編集を行なうアプリケーションです。
Windows版とMac版が販売されています。

この手のアプリケーションとしては比較的安価で、使用しているフォント作家の方も多いようです。

## OTEditの問題

_(以下の考察は、OTEditの試用版による短時間の検証に基づいています。全ての機能を検証できている訳ではないので誤りを含む可能性があります。)_

OTEditではAdobe-Japan1-3、Adobe-Japan1-4、 Adobe-Japan1-7の3種の文字集合のフォントを作成できます。
新規作成時に選択した文字集合について全てのグリフを設定することを前提としているようです。
OTEditではフォントの新規作成時に選択した文字集合から文字の削除ができず、グリフが作成されなくとも「空グリフ」と
各文字コードとグリフのcmapを作成してしまいます。

すべてのフォントがAdobe社の策定した日本語文字集合規格で作成されればよいのですが、
実際にはいずれかの文字集合を選択してもすべてのグリフをサポートしないフォントも多いようです。
例えば、IPAが配布するIPAフォントです。このフォントがどんなツールを使用して作成されたか不明ですが、
JIS X 0213:2012の文字集合をサポートしておりAdobe社の文字集合規格には従っていません。
Adobeの規格と並べると下表のような食い違いがあります。

| 文字セット      | 総文字数   | JIS第1～2水準（6,355字） | JIS第3～4水準（3,695字） | JIS規格外文字（異体字・独自文字） | 主な特徴           |
| --------------- | ---------- | ------------------------ | ------------------------ | --------------------------------- | ------------------ |
| JIS X 0213:2012 | 11,233文字 | 完全対応                 | 完全対応                 | 含まない                          | 公的規格・政府標準 |
| Adobe-Japan1-3  | 9,354文字  | 完全対応                 | 非対応                   | 機種依存文字等含む                | 一般用途標準       |
| Adobe-Japan1-4  | 15,444文字 | 完全対応                 | 一部対応                 | 多数の独自文字・異体字含む        | 商業印刷用         |
| Adobe-Japan1-7  | 23,060文字 | 完全対応                 | 完全対応                 | 大量の独自文字・異体字含む        | 最上位規格         |

このようなケースでは、OTEditがcmapを生成しますが作者がグリフを用意していない文字には「空グリフ」をマッピングしてしまいます。

通常の使用ではあまり問題にならないかもしれませんが、フォント表示の際にフォールバックを前提にしている
ターミナルやブラウザなどで使用するとマズいことになります。
本来であれば指定したフォントがグリフを持たない場合は、別のフォントのグリフが表示されます。
しかしOTEditで作成したフォントでは、「空グリフ」が設定されている可能性が高いので「空白」が表示されてしまいます。

## フォントの修正

最近購入した中村書体室の「カドマ-R」でこの不具合の遭遇したので、
作者の方に相談させていただき手元のフォントに修正を掛けました。

対応は、空グリフと思われる文字を調査し該当文字についてcmapからエントリーを削除するという乱暴なものです。
以下がそのスクリプトです。

### 分析スクリプト

```python,name=font_analyze.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# HomebrewのPython環境でFontToolsを使用
sys.path.insert(0, '/opt/homebrew/Cellar/fonttools/4.59.2/libexec/lib/python3.13/site-packages')

try:
    from fontTools.ttLib import TTFont
    from fontTools.pens.recordingPen import RecordingPen
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def analyze_font_glyphs(font_path):
    """フォントファイルを分析して空のグリフとスペースグリフを区別する"""

    font = TTFont(font_path)
    cmap = font.getBestCmap()

    if 'CFF ' in font:
        cff = font['CFF ']
        charstrings = cff.cff[0].CharStrings
    else:
        print("This is not a CFF font")
        return

    hmtx = font['hmtx']
    results = []

    space_codes = [0x0020, 0x3000]  # SPACE, IDEOGRAPHIC SPACE

    for unicode_code, glyph_name in sorted(cmap.items()):
        if glyph_name in hmtx.metrics:
            width, lsb = hmtx.metrics[glyph_name]
        else:
            width, lsb = 0, 0

        if glyph_name in charstrings:
            charstring = charstrings[glyph_name]

            pen = RecordingPen()
            try:
                charstring.draw(pen)
                commands = pen.value
                has_drawing = len(commands) > 0
            except Exception:
                has_drawing = False

            # グリフの分類
            is_space_char = unicode_code in space_codes

            if not has_drawing:
                if width > 0:
                    if is_space_char:
                        glyph_type = "SPACE"
                    else:
                        glyph_type = "BLANK_WITH_WIDTH"
                else:
                    glyph_type = "EMPTY"
            else:
                glyph_type = "NORMAL"

            results.append({
                'unicode': f"U+{unicode_code:04X}",
                'code': unicode_code,
                'char': chr(unicode_code),
                'glyph_name': glyph_name,
                'type': glyph_type,
                'width': width,
                'commands_count': len(commands) if has_drawing else 0,
            })

    return results
```

判定基準は、次の通りです。

- NORMAL: 描画データがあるグリフ
- SPACE: スペース文字（U+0020, U+3000）で描画データなし
- BLANK_WITH_WIDTH: スペース以外で幅はあるが描画データなし → 削除対象
- EMPTY: 幅や描画データがない → 削除対象

### 自動修正スクリプト

```python,name=font_cleaner_final.py
def fix_font_cmap_only(input_path, output_path):
    """OTEで作成されたフォントのcmapテーブルから空グリフエントリを削除"""

    font = TTFont(input_path)
    original_cmap = font.getBestCmap()

    if 'CFF ' in font:
        cff = font['CFF ']
        charstrings = cff.cff[0].CharStrings
    else:
        return False

    hmtx = font['hmtx']
    codes_to_remove = []

    space_code = 0x0020
    ideographic_space_code = 0x3000

    for unicode_code, glyph_name in original_cmap.items():
        if glyph_name in hmtx.metrics:
            width, lsb = hmtx.metrics[glyph_name]
        else:
            width, lsb = 0, 0

        if glyph_name in charstrings:
            charstring = charstrings[glyph_name]

            pen = RecordingPen()
            try:
                charstring.draw(pen)
                commands = pen.value
                has_drawing = len(commands) > 0
            except Exception:
                has_drawing = False

            # スペース文字以外で描画データがない場合は削除対象
            if unicode_code not in [space_code, ideographic_space_code]:
                if not has_drawing and width > 0:
                    codes_to_remove.append(unicode_code)

    # cmapテーブルから削除
    for table in font['cmap'].tables:
        if hasattr(table, 'cmap'):
            for code in codes_to_remove:
                if code in table.cmap:
                    del table.cmap[code]

    font.save(output_path)
    return True, len(codes_to_remove)
```

## 修正結果

修正結果は次の通りです。

- 総cmapエントリ数: 10,161 → 5,762個（削減率: 43.3%）
- 削除されたエントリ: 4,399個
- Adobe Japan 1-4拡張範囲: 408個
- その他の範囲: 3,991個
- ファイルサイズ: 2.6% 削減

修正の結果、
今のところターミナルでも問題なく使用できています。

上記のスクリプトは精緻にテストを行なっていませんので、
利用については自己責任でどうぞ。
