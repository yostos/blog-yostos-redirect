+++
title = "スキャンPDFの処理を自動化するClaude Codeプラグインを作った"
description = """
書籍をスキャナーで読み取ってPDF化した後の処理を簡単にするため、
Claude Codeプラグイン「pdf-processor」を開発しました。
複数PDFのマージ、OCR処理、ファイルサイズ最適化、目次の追加を
自動化し、スキャン書籍を実用的なデジタル書籍に変換します。
"""
date = 2026-01-02
aliases =["/articles/2026/01/02/pdf-processor-plugin"]

[taxonomies]
tags =["Tech","Claude Code","PDF"]
[extra]
social_media_card = "ogp.webp"
+++

## はじめに

書籍をスキャナーで読み取ってPDF化すると、複数のファイルに分かれてしまったり、テキスト検索ができなかったりします。また、目次がないため、そのままでは使いにくい状態になります。これらを手作業で処理するのは非常に面倒です。

そこで、スキャンしたPDFの処理を自動化するClaude Codeプラグイン「pdf-processor」を開発しました。このプラグインを使えば、複数のPDFファイルのマージ、OCR処理、目次の追加を簡単に実行でます。

プラグインのソースコードは[GitHub](https://github.com/yostos/claude-code-plugins/tree/main/plugins/pdf-processor)で公開しています。

## pdf-processorプラグインの機能

このプラグインは、スキャンされたPDFファイルを実用的なデジタル書籍に変換するためのツールです。主な機能は以下の通りです。

- **複数PDFファイルのマージ**: バラバラのPDFファイルを1つに統合
- **OCR処理**: 日本語に対応したOCR処理により、画像PDFをテキスト検索可能に変換
- **ファイルサイズ最適化**: 画像の圧縮により、ファイルサイズを削減
- **目次（ブックマーク）の追加**: PDFビューアで使える目次を自動生成
- **メタデータ編集**: PDFのタイトル、著者などのメタデータを設定

## 使い方

pdf-processorプラグインは、3つのステップで処理を行います。

### ステップ1: 前処理の実行

まず、`/pdf-processor:preprocess` コマンドを実行して、複数のPDFファイルをマージし、OCR処理を行います。

```
/pdf-processor:preprocess
```

Claudeが以下の処理を自動で実行します。

- 対象となるPDFファイルの確認
- PDFのマージ
- OCR処理の実行
- 画像の最適化
- 目次テンプレートファイルの生成

処理が完了すると、OCR処理済みのPDFファイルと、メタデータをダンプしたファイルが生成されます。

### ステップ2: 目次情報の編集

ダンプされたメタデータファイルをエディタで開き、目次情報を追加します。目次は以下の形式で記述します。

各目次項目は `BookmarkBegin` で始まり、以下の3つのフィールドで構成されます。

- `BookmarkTitle`: 目次のタイトル（章名など）
- `BookmarkLevel`: 目次の階層レベル（1が最上位、2が第2階層）
- `BookmarkPageNumber`: 目次項目が指すページ番号

例として、以下のように追加します。

```
BookmarkBegin
BookmarkTitle: 第1章 はじめに
BookmarkLevel: 1
BookmarkPageNumber: 1

BookmarkBegin
BookmarkTitle: 1.1 背景
BookmarkLevel: 2
BookmarkPageNumber: 2

BookmarkBegin
BookmarkTitle: 1.2 目的
BookmarkLevel: 2
BookmarkPageNumber: 5

BookmarkBegin
BookmarkTitle: 第2章 実装
BookmarkLevel: 1
BookmarkPageNumber: 10
```

### ステップ3: 目次の適用

目次情報を編集したら、`/pdf-processor:apply-toc` コマンドを実行して、最終的なPDFファイルを生成します。

```
/pdf-processor:apply-toc
```

このコマンドを実行すると、OCR処理済みのPDFに目次が追加され、完成版のPDFファイルが作成されます。

## 技術的な詳細

pdf-processorプラグインは、以下のツールを組み合わせて実装しています。

- **OCRmyPDF**: PythonベースのOCRツールで、Tesseract OCRエンジンを使用してPDFにテキストレイヤーを追加
- **PDFtk**: PDFの操作に特化したコマンドラインツールで、マージやメタデータの編集に使用
- **Ghostscript**: PDFの最適化と圧縮に使用

これらのツールのインストールや設定は、プラグインのREADMEに詳しく記載されています。

## まとめ

pdf-processorプラグインを使うことで、スキャンしたPDFの処理を大幅に効率化できます。複数ファイルのマージ、OCR処理、目次の追加といった面倒な作業を、Claude Codeとの対話だけで完了できるようになりました。

スキャンした書籍や資料をデジタル化する際に、ぜひ活用してみてください。プラグインのソースコードは[GitHub](https://github.com/yostos/claude-code-plugins/tree/main/plugins/pdf-processor)で公開しているので、カスタマイズや改善の提案も歓迎します。
