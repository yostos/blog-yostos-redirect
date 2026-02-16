+++
title = "Logic ProのAIFファイルをラウドネス正規化してFLACに変換するスクリプト"
description = """
Logic Proでバウンスした音声ファイルをFLACに変換する際、
ffmpegのloudnormフィルタによる2パス処理を自動化する
Bashスクリプトを作成しました。測定と適用を一度のコマンドで
完結させ、手作業を排除して作業効率を大幅に向上させます。
"""
date = 2026-01-14
aliases =["/articles/2026/01/14/aif2flac"]

[taxonomies]
tags =["Music Production","CLI"]
[extra]
social_media_card = "ogp.webp"
+++

## 背景

Logic Proでバウンスした音声ファイル(Aiff)をFLACに変換する際、適切な音量に正規化する必要があります。ffmpegの`loudnorm`フィルタを使うと高品質なラウドネス正規化が可能ですが、最良の結果を得るには2パス処理が推奨されます。

この2パス処理は以下のような手順です。

1. 1回目の実行で音声のラウドネス値を測定
2. 測定された値を確認し、手動で2回目のコマンドにコピー
3. 2回目の実行で測定値を使用して正規化を適用

毎回この作業を手動で行うのは面倒なので、自動化するスクリプトを作成しました。

## スクリプトの内容

現時点のコードは以下です。[Gist](https://gist.github.com/yostos/004e57e4a905f933e227aa183e3a8fec)でも公開しています。

```bash,name=aif2flac.sh
#!/bin/bash

# Script to convert AIF files to FLAC
# Uses two-pass loudness normalization method (measure first, then encode with measured values)
#
# Copyright (c) 2026 yostos
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

set -e

VERBOSE=false

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [-v|--verbose] <input_file.aif>"
            echo ""
            echo "Options:"
            echo "  -v, --verbose    Show detailed ffmpeg output"
            echo "  -h, --help       Show this help message"
            exit 0
            ;;
        -*)
            echo "Error: Unknown option $1"
            echo "Usage: $0 [-v|--verbose] <input_file.aif>"
            exit 1
            ;;
        *)
            INPUT_FILE="$1"
            shift
            ;;
    esac
done

if [ -z "$INPUT_FILE" ]; then
    echo "Usage: $0 [-v|--verbose] <input_file.aif>"
    echo "Use -h or --help for more information"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' not found"
    exit 1
fi

# Generate output filename (change extension to .flac)
OUTPUT_FILE="${INPUT_FILE%.*}.flac"

echo "=== Step 1: Measuring loudness... ==="
echo

# Measure loudness and get JSON output
LOUDNESS_JSON=$(ffmpeg -i "$INPUT_FILE" -af "loudnorm=print_format=json" -f null - 2>&1 | grep -A 12 "Parsed_loudnorm")

# Extract required values from JSON
MEASURED_I=$(echo "$LOUDNESS_JSON" | grep '"input_i"' | awk -F'"' '{print $4}')
MEASURED_TP=$(echo "$LOUDNESS_JSON" | grep '"input_tp"' | awk -F'"' '{print $4}')
MEASURED_LRA=$(echo "$LOUDNESS_JSON" | grep '"input_lra"' | awk -F'"' '{print $4}')
MEASURED_THRESH=$(echo "$LOUDNESS_JSON" | grep '"input_thresh"' | awk -F'"' '{print $4}')
TARGET_OFFSET=$(echo "$LOUDNESS_JSON" | grep '"target_offset"' | awk -F'"' '{print $4}')

echo "Measurement results:"
echo "  Input Integrated: $MEASURED_I LUFS"
echo "  Input True Peak:  $MEASURED_TP dBTP"
echo "  Input LRA:        $MEASURED_LRA LU"
echo "  Input Threshold:  $MEASURED_THRESH LUFS"
echo "  Target Offset:    $TARGET_OFFSET LU"
echo

echo "=== Step 2: Encoding to FLAC... ==="
echo

# Encode to FLAC using measured values
if [ "$VERBOSE" = true ]; then
    # Verbose mode: show all ffmpeg output
    ffmpeg -y -i "$INPUT_FILE" \
        -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$MEASURED_I:measured_TP=$MEASURED_TP:measured_LRA=$MEASURED_LRA:measured_thresh=$MEASURED_THRESH:offset=$TARGET_OFFSET:linear=true:print_format=summary" \
        -c:a flac "$OUTPUT_FILE"
else
    # Quiet mode: capture output and show only loudnorm summary
    FFMPEG_OUTPUT=$(ffmpeg -y -hide_banner -i "$INPUT_FILE" \
        -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$MEASURED_I:measured_TP=$MEASURED_TP:measured_LRA=$MEASURED_LRA:measured_thresh=$MEASURED_THRESH:offset=$TARGET_OFFSET:linear=true:print_format=summary" \
        -c:a flac "$OUTPUT_FILE" 2>&1)
    FFMPEG_EXIT_CODE=$?

    # Extract and display loudnorm summary
    echo "$FFMPEG_OUTPUT" | grep -A 15 "Input Integrated:" | grep -v "^\[" | grep -v "^$" || true

    # Check for errors
    if [ $FFMPEG_EXIT_CODE -ne 0 ]; then
        echo ""
        echo "Error during encoding (exit code: $FFMPEG_EXIT_CODE)"
        echo "$FFMPEG_OUTPUT"
        exit 1
    fi
fi

echo
echo "=== Completed ==="
echo "Output file: $OUTPUT_FILE"

# Display file sizes
if command -v du &> /dev/null; then
    INPUT_SIZE=$(du -h "$INPUT_FILE" | awk '{print $1}')
    OUTPUT_SIZE=$(du -h "$OUTPUT_FILE" | awk '{print $1}')
    echo "Input file:  $INPUT_SIZE"
    echo "Output file: $OUTPUT_SIZE"
fi
```

## 使い方

AIFファイルのパスを引数に指定して実行します。

```bash
./aif2flac.sh input.aif
```

詳細な出力を確認したい場合は`-v`オプションを付けます。出力ファイルは同じディレクトリに`.flac`拡張子で保存されます。

## loudnormフィルタについて

ffmpegの`loudnorm`フィルタは、EBU R128規格に基づいたラウドネス正規化を行うためのフィルタです。単純な音量の増減ではなく、人間の聴覚特性を考慮した知覚的な音量の均一化を実現します。

このスクリプトでは以下のパラメータを使用しています。

- `I=-14`: 目標のIntegrated Loudness（LUFS単位）
- `TP=-1`: True Peak値の上限（dBTP単位）
- `LRA=11`: Loudness Range（LU単位）

`I=-14 LUFS`は、Spotify、YouTube Music、Apple Musicなどの主要なストリーミングサービスが採用している標準的なラウドネス基準です。世間一般で広く使われているこの基準を参考にすることで、適切な音量バランスを保つことができます。

1パス処理では入力音声の特性を考慮せずに正規化するため、音質劣化の可能性があります。2パス処理では、1回目で測定した入力音声の実際の値を2回目の処理に使用することで、より正確で高品質な正規化が可能になります。

## まとめ

Logic Proから書き出した音声ファイルをFLACに変換する際の2パス処理を自動化することで、手動でパラメータをコピーする手間がなくなり、作業効率が大幅に向上しました。

今後は、複数ファイルの一括処理や、ターゲットラウドネス値のカスタマイズなどの機能を追加するかもしれません。
