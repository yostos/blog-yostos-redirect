+++
title = "OpenAI will support MCP"
description = "MCPをサポートしたAnthropicのClaudeで試しましたが、その可能性に驚きました。3月末にはOpenAIもMCP対応を表明していたので楽しみです。"
date = 2025-04-08
aliases = ["/articles/2025/04/08/openai-mcp-support"]

[taxonomies]
tags = ["Tech", "Generative AI"]
[extra]
social_media_card = "ogp.webp"
+++

## AltmanのツイートによるMCP対応のアナウンス

以下が3月末のAltmanのツイート(X)です。

<blockquote cite="https://x.com/sama/status/1904957253456941061">
  people love MCP and we are excited to add support across our products.
  available today in the agents SDK and support for chatgpt desktop app +
  responses api coming soon!
  <footer>
    <cite>
      <a href="https://x.com/sama/status/1904957253456941061">
        &mdash; Sam Altman (March 26, 2025)
      </a>
    </cite>
  </footer>
</blockquote>

MCP(Model Context Protocol)はAnthropicが提唱しているフレームワーク
ですが、上記は**OpenAIもMCPをサポートする**というアナウンスです。

とても重要な意味を持つアナウンスだと思います。
AnthropicはOpenAIの強力なライバルで競合関係にあります。
デファクト・スタンダードが無い現状では対応する規格を提唱できたはずですが、
それをせずMCPサポートに舵を切ったのは素晴らしい経営判断だと思います。

これにより、MCPがほぼ業界のデファクト・スタンダードになると思います。

## MCP(Model Context Protocol)とは

以前いくつか記事を書いていますが、ちゃんとMCPの説明を書いていませんでした。

Model Context Protocol (MCP)は、大規模言語モデル(LLM)に対する指示を構造化す
るためのフレームワークです。

次のような要素から構成されています。

- **Model（モデル）** - AIモデルがどのように自分自身を認識し、振る舞うべきかを定義する
- **Context（コンテキスト）** - モデルが参照すべき情報や知識を提供する
- **Protocol（プロトコル）** - モデルの動作や応答方法のルールを設定する

[以前の記事](/articles/2025/03/28/claude-integration-with-inkdrop)では、
**Context**を使って独自のナレッジ(Inkdrop)をClaudeに追加するということをやっただけですが、
Claude活用の可能性が途端に広がりものすごい効果を体感できました。これまでも
Contextの部分にだけ限るとRAG (Retrieval-Augmented Generation)という手法があ
りましたが、こんなに簡単にはできなかったと思います。

MCPではContextだけでなく、Protocolを通じて行動規範の設定や、Modelを通じた企業の
ブランドトーンに合わせた応答スタイルなどに応用できます。

MCPにより、明確に分離された要素(Model/Context/Protocol)に整理され、
単なるプロンプトエンジニアリングを超えて体系化されたアプローチで
AIの応答をより予測可能で一貫性のあるものにすることが可能となりました。

## MCPがデファクト・スタンダードになると

MCPがデファクト・スタンダードとなればAI関連ツール間の標準化された通信パターンを
提供していることになるでしょう。

この事実を踏まえるとClaudeデスクトップがClaude Codeをナレッジソースとして扱えるように、次のよう
なことが可能になるかもしれません。

- **ChatGPT-Claudeクロス連携**: ChatGPTの回答をClaudeが評価するようなAIシステム間の直接的な情報交換や連携
- **AIオーケストレーション**: 複数の生成AIがそれぞれ
  の強みを生かした連携し、結果を統合するようなワークフロー構築の可能性。例え
  ば、データ解析はChatGPT、文章生成はClaude、検証はGeminiなどの役割分担するイ
  メージ。
- **統一ナレッジアクセス**: マーケットにMCP準拠した多数のナレッジベースが
  登場し、簡単に新しいナレッジを自社のAIに追加できる可能性

いずれも現時点で実現できるかどうか検証が必要というレベルです。
AIオーケストレーションなどは追加の標準化やツールが必要でしょう。
また、技術的に標準化の方向で協力できたからと言って、今後ビジネス上の判断で
その適用範囲が制限される可能性はあります。

しかし、このような動きを見ていると、加速度的にAIの世界が拡がっていくのを実感しています。楽しみです。
