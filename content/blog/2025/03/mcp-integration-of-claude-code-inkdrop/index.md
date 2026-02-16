+++
title = "Claude CodeをMCPサーバーとして利用する利点"
description = "前回はInkdropとClaudeのMCP統合について紹介しましたが、今回はClaude Codeを MCPサーバーとして活用する方法とそのメリットについて解説します。 開発者にとって、Claude CodeとInkdropの組み合わせがどのように効率的な 知識管理と開発プロセスの向上につながるかを探ります。"
date = 2025-03-29
aliases = ["/articles/2025/03/29/mcp-integration-of-claude-code-inkdrop"]

[extra]
social_media_card = "ogp.webp"
mermaid = true

[taxonomies]
tags = ["Tech", "Generative AI", "Note-taking", "Productivity"]
+++

[前回の記事](/articles/2025/03/28/claude-integration-with-inkdrop)では、 InkdropとClaude Desktopの統合について紹介しました。今回は一歩進んで、Claude CodeをMCPサーバーとして活用する方法とそのメリットについて詳しく解説します。

<!-- toc -->

## MCP ServerにもなれるClade Code

Claude Codeを頻繁に活用することでAnthropicへの支払いコストが増加していますが、一度使い始めるとコーディング作業では手放せなくなりつつあります。

そのClaude Codeは、MCP Clientになれることは知っていました。
しかし、[公式ドキュメント](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/)を読んでいてMCP Serverにもなれるというチュートリアルを発見しました。

次のコマンドでMCP Serverとして起動できます。

```bash
claude mcp serve
```

## Claude DesktopにClaude CodeをMCP Serverとして登録

[Inkdropと同様](/articles/2025/03/28/claude-integration-with-inkdrop)に、Claude Desktopに
Claude CodeをMCP Serverとして登録します。

また、`bash`の問題が起きそうだったので、例のごとくシェルスクリプトでWrapし`~/bin/claude-code-mcp`というファイル名で配置し実行権限を付けした。

```bash
#!/usr/bin/env fish
claude mcp serve
```

作成したスクリプトを指定して、Claude Desktopの設定ファイル `~/Library/Application Support/Claude/claude_desktop_config.json`に追加します。

```json
{
  "mcpServers": {
    "inkdrop": {
      "command": "/Users/foo/bin/inkdrop-mcp",
      "args": [],
      "env": {
        "INKDROP_LOCAL_SERVER_URL": "http://localhost:19840",
        "INKDROP_LOCAL_USERNAME": "foo",
        "INKDROP_LOCAL_PASSWORD": "bar"
      }
    },
    "claude_code": {
      "command": "/Users/foo/bin/claude-code-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

## Claude DesktopからClaude Codeにコード分析を依頼

Claude CodeをClaude Desktopに正常に接続できたことを確認したので、次のステップとして実際にこのブログサイトのコードの分析を依頼してみます。

1. Claude Desktopのチャットインターフェースで、Claude Codeにアクセスするためのプロンプトを入力
2. 分析したいプロジェクトのパスを明示的に指定
3. フォルダ階層の確認を依頼

初回実行時には、Claude Codeがファイルシステムにアクセスするための許可を求めるプロンプトが数回表示されました。これは、セキュリティ上の理由から必要な確認プロセスです。許可を与えると、Claude Codeは指定されたプロジェクトフォルダにアクセスし、次のよう分析しました。

```txt
私：claude_code内の~/ghq/github.com/foo/blog-source
    のプロジェクトにアクセスできますか？
    また、プロジェクト内のフォルダ階層はどうなっていますか？

/Users/foo/ghq/github.com/foo/blog-sourceにアクセスできました。
これはパーソナルブログのソースコードです。

ブログの主な特徴：

Next.js 15, React 19, TypeScript, Tailwind CSSで構築
MDXサポートで記事を書いている
レスポンシブデザイン
ダークモード対応
RSS、コードシンタックスハイライト、Giscusコメントシステム、
ソーシャルリンク、SoundCloudの埋め込み、Whisper機能、目次機能など

サイト設定では「Coded Chords」という名前のブログで、
著者は「Toshiyuki Yoshida」です。
(以下、省略)
```

## Claude Desktop/Claude Code/InkdropのMCP統合

Claude DesktopにはInkdropもMCP Serverとして登録されているので、コード解析結果をInkdropに記録させることもできます。

次のようにClaude Desktopで依頼してみました。

```txt
では、プロジェクト概要とプロジェクトのフォルダ構成について、
第三者が理解しやすいようサマリーを inkdrop内のNotebook Inboxに
「ブログの概要」というタイトルで作成してください。
なお、形式はMarkdownを使用してください。
```

結果、Claude Codeから取得し分析した結果、Markdown形式でInkdropのNoteとしてドキュメント化してくれました。

作成された結果を[公開](https://e.pcloud.link/publink/show?code=XZiJhdZ3UkXV7lTN8knDkuquFjN147NvQ0y)しておきます。

プロジェクト概要は`README.md`から読み取ったようですが、特筆すべきは、フォルダ構成や各ディレクトリの役割、記事管理の仕組みまで正確に把握・文書化している点です。

仕組みとしては全体像をダイアグラムにしてみました。次の通りです。

<!-- textlint-disable -->

{% mermaid() %}

flowchart TB
UserReq[ユーザーリクエスト/指示]
CD[Claude Desktop]
CC[Claude Code]
BlogRepo[ブログリポジトリ]
InkdropMCP[inkdropapp/mcp-server]

    subgraph Inkdrop[Inkdropアプリ]
        API[HTTP API]
        Notes[ノート]
    end

    %% 通常フロー
    UserReq -->|会話形式の指示| CD
    CD -->|コード分析のリクエスト| CC
    CC -->|ファイル読み取り| BlogRepo
    BlogRepo -->|コードとファイル内容| CC
    CC -->|分析結果| CD

    %% ファイル操作フロー
    CC -->|新記事作成| BlogRepo

    %% Inkdrop連携フロー
    CD -->|ノート作成リクエスト| InkdropMCP
    InkdropMCP -->|APIリクエスト| API
    API -->|ノートデータ保存| Notes

    %% スタイル
    classDef claudeDesktop fill:#f9a8d4,stroke:#be185d,stroke-width:2px
    classDef claudeCode fill:#93c5fd,stroke:#2563eb,stroke-width:2px
    classDef inkdropCompo fill:#ffffff,stroke:#6b7280,stroke-width:1px
    classDef repository fill:#fcd34d,stroke:#d97706,stroke-width:2px
    classDef mcpServer fill:#93c5fd,stroke:#2563eb,stroke-width:2px
    classDef other fill:#e5e7eb,stroke:#6b7280,stroke-width:2px

    class CD claudeDesktop
    class CC,InkdropMCP claudeCode
    class API,Notes inkdropCompo
    class Inkdrop,BlogRepo repository
    class UserReq other

`
{% end %}

<!-- textlint-enable -->

便利です。

開発プロジェクトのドキュメンテーションや`README.md`の作成など、次のようなワークフローにすると大変スマートに仕事が進みそうです。

1. Claude DesktopからClaude Codeにリポジトリーからコード情報を収集し、そのコードを分析しMarkdown文書を生成しInkdropにNote作成させる。
2. Inkdrop上でMarkdown文書をPreviewで確認し、必要に応じて編集する
3. Claude DesktopからInkdrop上のNoteからドキュメントを収集し、Claude Codeを通じてリポジトリーにドキュメントとして格納させる

## Claude Code MCP Server利用コスト

Claude CodeをMCP ServerとしてClaude Desktopから利用した際のコストを確認してみました。

Claude Codeをコマンドラインから普通に使うと、MODELとして `claude-3-7-sonnet-20250219`が使用されています。
このため、多用しているとクレジットも大量に消費されていきます。
しかし、Claude CodeをMCP Serverとして使うと、リクエストあるからと言ってClaude Codeから
MODELを使用したリクエストが出るわけでも無さそうです。またリクエストが出たとしても、今のところ`claude-3-5-haiku-20241022`しか利用されていません。
Tailwind Plusで提供されるコードが大量にlintで引っかかるので修正をClaud
Destop経由で行いましたが、同様Claude Codeからは`claude-3-5-haiku-20241022`を
利用するリクエストかでていませんでした。

Claude CodeをMCP Serverとして利用する場合、提供されるツールは以下のとおりです。これらのうち、AgentTool以外の大半はClaude Code内部で処理が完結するため、高度な分析などはClaude Desktop側から直接リクエストされると考えられます。

| Tool             | Description                                          | Permission Required |
| ---------------- | ---------------------------------------------------- | ------------------- |
| AgentTool        | Runs a sub-agent to handle complex, multi-step tasks | No                  |
| BashTool         | Executes shell commands in your environment          | Yes                 |
| GlobTool         | Finds files based on pattern matching                | No                  |
| GrepTool         | Searches for patterns in file contents               | No                  |
| LSTool           | Lists files and directories                          | No                  |
| FileReadTool     | Reads the contents of files                          | No                  |
| FileEditTool     | Makes targeted edits to specific files               | Yes                 |
| FileWriteTool    | Creates or overwrites files                          | Yes                 |
| NotebookReadTool | Reads and displays Jupyter notebook contents         | No                  |
| NotebookEditTool | Modifies Jupyter notebook cells                      | Yes                 |

(2025-03-31追記)

その後、もう少し複雑な処理で確認しました。ソースを複雑に分析するような場合は、
Claude CodeでのリクエストからもMODELとして `claude-3-7-sonnet-20250219`が使用されていました。

依頼した処理は次のようなものです。

> プロジェクトがOGP対応しているか、対応している場合はどのようなコンポーネントが関係しどのような仕様になっているか調査し、
> InkdropのNotebook blogに新たに Noteを作成して仕様書にしてください。仕様書に
> は静的モデルと動的モデルをMermaid でダイアグラム化してください。

Claude DesktopがInkdropに書き出した文書をそのままPDFにしたものも[公開](https://e.pcloud.link/publink/show?code=XZiJhdZ3UkXV7lTN8knDkuquFjN147NvQ0y)しておき
ます。

## まとめ

Claude CodeのMCP Serverを利用する利点は2つです。

1つは、Claude Codeからのリクエスト発行を押さえ、Claude Desktopからのリクエストになることでの**コスト削減**が大きくできることです。
(2025-03-31追記) 処理内容によってはClaude Code側の処理でもSonnet 3.7が使用
されるため注意は必要です。

本来次のようにClaude DesktopとClaude Codeは使い分けるべきだと思います。

<dl>
  <dt>**Claude Code**</dt>
  <dd>
    - コマンドライン志向
    - ファイルシステムへの直接アクセス
    - コードリポジトリとの統合
    - 開発タスクに特化
  </dd>

  <dt>**Claude Desktop**</dt>
  <dd>
    - GUI ベースの使いやすさ
    - 会話形式のインターフェース
    - 画像認識機能
    - 一般的な質問応答に最適
  </dd>
</dl>

しかし、MCP統合によりファイルシステムへの直接アクセス、コードリポジトリとの統合のメリットを
Claude Desktopからも享受できるようになります。Claude Desktopは月額固定料金なので、ユーザーには非常に恩恵があります。

2つ目の利点は、**ワークフロー改善の可能性**です。
Claude CodeとInkdropの統合のような仕組みは、開発者のワークフローを大幅に改善する可能性を秘めており、以下のような発展が期待できそうです。

1. **より高度なコンテキスト理解**:
   - コードとドキュメントの関係性をより深く理解
   - プロジェクト全体の知識グラフ構築
2. **自動ドキュメント更新**:
   - コード変更に基づく関連ドキュメントの自動更新
   - コメントとドキュメントの一貫性維持
3. **協調作業の強化**:
   - チームメンバー間の知識共有と協調作業の促進
   - コードレビューとドキュメントレビューの統合

この統合は特に、複雑なプロジェクトやドキュメント駆動開発を実践している開発者にとって大きなメリットをもたらします。知識の管理と活用、コード生成、ドキュメント作成の一連のプロセスがシームレスに繋がることで、開発プロセス全体の質と効率が向上するでしょう。
