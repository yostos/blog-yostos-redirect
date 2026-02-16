+++
title = "MulmoCast: AIと人間が協働する次世代プレゼンテーション・プラットフォームを試してみた"
description = "AIネイティブなプレゼンテーション・プラットフォーム「MulmoCast」を実際に検証してみました。一つのスクリプトから動画、ポッドキャスト、PDFなど複数フォーマットに自動変換できる革新的なツールの使い方と実用性について詳しく解説します。"
date = 2025-06-24
aliases = ["/articles/2025/06/24/mulmocast-ai-collaboration-platform"]

[taxonomies]
tags = ["Tech", "Generative AI"]
[extra]
social_media_card = "ogp.webp"
+++

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

あの中島聡氏が開発している
[mulmocast](https://github.com/receptron/mulmocast-cli) の検証しました。
ガイドにしたがって、ビジネスプレゼンテーションと子供用の絵本的な動画を作って
みました。生成AIのモデルはClaudeやGeminiも選択できるようですが、今回は
デフォルトのままOpenAIを使いました。

## MulmoCastとは何か？その意義は？

MulmoCastは、AI時代に特化して設計された次世代のプレゼンテーション・プラッ
トフォームです。従来のPowerPointやKeynoteがAI以前の時代に人間のクリエ
イター向けに設計されたのに対し、MulmoCastは最初からAIネイティブなツールと
して開発されています。

最大の特徴は、 1つのスクリプトから動画、ポッドキャスト、スライドショー
など、複数のフォーマットに自動変換できることです。
現代では情報消費のチャネルが多様化しており、Zoomでのプレゼンテーション、Slackでの共有、移動中の動画視聴、通勤時のポッドキャスト聴取など、様々な場面に対応する必要があります。MulmoCastはこの課題を解決します。

核となるのは「MulmoScript」というJSON/YAML形式の中間言語です。これは映画の脚本やWebマークアップのような役割を果たし、ChatGPTやClaudeなどの大規模言語モデルが理解・生成できる形式になっています。AIがストーリー構造からビジュアルまでをすべて定義し、人間はクリエイティブループの中で方向性を決めるという協働モデルを実現しています。

## インストール方法（Mac）

MulmoCastのインストールは比較的簡単です。Node.jsとffmpegが必要になります。

まず、NPMを使ってMulmoCastをグローバルインストールします。

```bash
npm install -g mulmocast
```

次に、動画生成に必要なffmpegをインストールします。Macの場合はHomebrewを使用します。

```bash
brew install ffmpeg
```

最後に、プロジェクトディレクトリに`.env`ファイルを作成し、必要なAPIキーを設定します。

```bash
OPENAI_API_KEY=your_openai_api_key
DEFAULT_OPENAI_IMAGE_MODEL=gpt-image-1
GOOGLE_PROJECT_ID=your_google_project_id
NIJIVOICE_API_KEY=your_nijivoice_api_key
BROWSERLESS_API_TOKEN=your_browserless_api_token
```

OpenAI APIキーは必須ですが、他のAPIキーは使用する機能に応じて設定してください。

## 基本的な使い方

MulmoCastの基本的な使い方は2ステップです。

### ステップ1：スクリプト生成

まず、AIとの対話でストーリースクリプトを作成します。

```bash
mulmo tool scripting -i -t business -o ./ -s story
```

このコマンドの説明は次の通りです。

- `-i`: インタラクティブモード
- `-t business`: ビジネステンプレートを使用
- `-o ./`: 出力ディレクトリ
- `-s story`: ファイル名のプレフィックス

実行すると、AIとの対話が始まります。コンテンツの内容、ターゲット層、長さなどについて質問され、それに応えることでMulmoScript形式のJSONファイル（例：`story-1746600802426.json`）が生成されます。

### ステップ2：動画生成

生成されたスクリプトから動画を作成します。

```bash
mulmo movie story-1746600802426.json
```

このコマンド1つで、音声合成、画像生成、動画編集までが自動実行され、最終的にMP4ファイルが出力されます。

### 利用可能なテンプレート

用途に応じて以下のテンプレートも選択できます。なんとなくどんなものが出来るか
想像できますね。

- akira_comic
- business
- children_book
- coding
- comic_strips,
- drslump_comic
- ghibli_comic
- ghibli_image_only
- ghibli_shorts,
- ghost_comic
- onepiece_comic
- podcast_standard
- portrait_movie,
- realistic_movie
- sensei_and_taro
- shorts
- text_and_image,
- text_only
- trailer

## 検証結果

今回、ビジネスプレゼンテーションと子供用絵本の2つのパターンで検証しました。
生成AIモデルはClaudeやGeminiも選択可能ですが、今回はデフォルトのOpenAIを
使用しました。

`mulmo tool scripting -i -t business -o ./ -s story` でAgentと会話してストーリーを練って、`mulmo movie story-xxxxxxxxxxxxx.json`で動画を生成します。

ちょっとした会話でそれらしいプレゼンテーション動画が出来ます。以下がその動画
です。

{{ youtube(id="mAp5ORk2Zas") }}

実際に使ってみた感想として、簡単な会話だけでそれらしいプレゼンテーション動画
が生成できることに驚きました。内容の深みという点では限界がありますが、1st
Callの資料としては十分に実用的なレベルに達していると感じました。

特に印象的だったのは、一度スクリプトを作成すれば、そこから動画、ポッドキャス
ト、PDFなど複数フォーマットに展開できる点です。コンテンツの再利用性が高く、
効率的な情報発信が可能になります。

## まとめ

MulmoCastは、AI時代のコンテンツ作成における新しい可能性を示すツールです。従
来のプレゼンテーション作成が「人間がすべてを制作する」モデルだったのに対し、
「AIと人間が協働して作成する」という新しいパラダイムを提示しています。

現時点では完全に実用レベルに達しているとは言えませんが、プロトタイプや初期段
階の資料作成には十分活用できると感じました。
特に、アイデアの可視化や概念の説明では、従来よりもはるかにコンテンツ作成を効率化できます。

今後、AIの精度向上とともにMulmoCastのようなツールがより洗練されれば、コンテ
ンツ作成の方法が根本的に変わる可能性があります。単一のスクリプトから多様なメ
ディアフォーマットに展開できる仕組みは、情報発信の効率化に大きく貢献するでし
ょう。

興味のある方は、ぜひ一度試してみることをお勧めします。AI協働時代のコンテンツ作成を体験できる貴重なツールです。
