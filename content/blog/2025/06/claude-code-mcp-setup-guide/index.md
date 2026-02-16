+++
title = "Claude Code MCPセットアップガイド：Inkdrop統合の実践"
description = "Claude CodeでInkdrop MCPサーバーを設定し、リモートMCPサーバーとして統合する手順を詳しく解説します。実際のセットアップから高度なワークフローの実演まで、ステップバイステップで紹介。"
date = 2025-06-21
aliases = ["/articles/2025/06/21/claude-code-mcp-setup-guide"]

[taxonomies]
tags = ["Tech", "Generative AI","Claude Code"]
[extra]
social_media_card = "ogp.webp"
+++

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

5月Claude Codeが正式リリースされて以来手放せなくなっています。
Anthropicの
ブログに"
[Remote MCP support in Claude Code](https://www.anthropic.com/news/claude-code-remote-mcp)"
という記事が掲載されました。

早速Claude CodeでInkdrop MCPサーバーを設定し、リモートMCPサーバーとして統合
する手順を実際にセットアップしながら検証してみました。単純な設定から高度なワ
ークフローまで、実践的な内容をまとめています。

## MCPサーバーの追加

Claude CodeにInkdrop MCPサーバーを追加するには、以下のコマンドを実行します。

```bash
claude mcp add inkdrop /Users/hogehoge/bin/inkdrop-mcp \
  -e INKDROP_LOCAL_SERVER_URL=http://localhost:19840 \
  -e INKDROP_LOCAL_USERNAME=hogehoge \
  -e INKDROP_LOCAL_PASSWORD=***************** \
  -s local
```

このコマンドの設定は次の通りです。

- `inkdrop`：MCPサーバー名
- `/Users/hogehoge/bin/inkdrop-mcp`：実行ファイルパス
- `-e`：環境変数の設定（サーバーURL、認証情報）
- `-s local`：ローカルスコープでの設定

## 設定の確認

追加したMCPサーバーが正しく設定されているか確認します。

```bash
# MCPサーバー一覧の表示
claude mcp list

# 特定のMCPサーバーの詳細確認
claude mcp get inkdrop
```

正常に設定されていれば、以下のような出力が表示されます。

```
inkdrop:
  Scope: Local (private to you in this project)
  Type: stdio
  Command: /Users/hogehoge/bin/inkdrop-mcp
  Environment:
    INKDROP_LOCAL_SERVER_URL=http://localhost:19840
    INKDROP_LOCAL_USERNAME=hogehoge
    INKDROP_LOCAL_PASSWORD=************
```

## Claude Codeでの動作確認

Claude Codeを起動してMCPサーバーとの接続を確認します。

```bash
claude
```

Claude Code内で `/mcp` コマンドを実行すると、接続されたMCPサーバーの状態を確認できます。正常に接続された場合は、次のような結果になります。
接続状況とどんなコマンドが利用可能か確認できます。

```
❯ 1. inkdrop  ✔ connected · Enter to view details

Status: ✔ connected
Command: /Users/yostos/bin/inkdrop-mcp
Capabilities: tools · prompts
Tools: 7 tools

利用可能なツール:
1. read-note
2. search-notes
3. list-notes
4. create-note
5. update-note
(他2つのツールあり)
```

## 実際の使用例

### 基本的な検索機能

明示的にInkdropを指定することで、MCPツールが確実に呼び出されます。例えば私は
Inkdrop内にflacのエンコーディング方法をまとめているので、以下のような出力が
表示されます適切に該当するノートを読み取ってくれました。

```
Inkdropの"Tech Tips"から適切なflacファイルの作り方を検索して、示してください。
```

この指示により、以下の処理が自動実行されます。

1. `search-notes`でキーワード検索
2. `read-note`で該当ノートの内容取得
3. 結果の整理と表示

### 高度なワークフロー実演

より複雑な処理として、ブログ記事の管理を試してみました。

```
このブログプロジェクトから、2025年5月と6月の記事を確認して、
タイトル一覧をInkdropのInboxノートブックに新ノートとして作成してください。
```

この指示では以下の処理が連携して実行されました。

1. **ファイルシステム分析**：記事ディレクトリの探索
2. **並列処理**：5月・6月を別々のTaskエージェントで同時処理
3. **内容解析**：各記事のタイトル抽出とカテゴライズ
4. **MCP統合**：分析結果をInkdropに保存

結果として24記事（5月13件、6月11件）のタイトル一覧が自動的にカテゴリ別に整理され、Inkdropに新規ノートとして作成されました。

## セットアップのポイント

### 明示的指示の重要性

「Inkdropの...」という明示的な指示により、Claude CodeがMCPツールを確実に呼び出します。曖昧な指示では期待通りに動作しない場合があります。

### 自動ツール選択

Claude Codeは文脈に応じて適切なMCPツールを自動選択し、複数のツールを連携させて処理を完了します。

### 複合タスクの処理能力

ファイルシステム分析、内容理解、MCP統合といった複合的なタスクを自動化できるのがClaude Codeの真の能力です。

## まとめ

Claude CodeとInkdrop MCPの統合により、以下のメリットが得られます。

- **コード開発中のメモ参照**：開発中にInkdropのメモを即座に検索・参照可能
- **プロジェクト分析の自動化**：コード分析結果の知識ベース化
- **ワークフローの完全自動化**：複雑な処理を単一の指示で実行

### MCP を軸とした Claude 連携の実例

実は、この記事の制作プロセス自体がMCP統合の真価を示しています。

1. **Claude Desktop での検証設計**：セットアップ手順の相談と検証方法の策定
2. **Claude Desktop による知識蓄積**：検証結果をMCP経由でInkdropのノートに整理・保存
3. **Claude Code による記事生成**：MCP経由でInkdropから検証ノートを読み込み、ブログ記事として再構成

このワークフローでは、Claude DesktopとClaude Codeが同一のInkdropをMCPサーバーとして共有し、知識の橋渡し役として機能しています。単体のツール利用では不可能な、複数のClaude環境を跨いだ継続的な作業が実現されています。

この統合は、開発プロセスにおける知識管理と自動化の新しい可能性を示しており、MCPを軸としたClaudeエコシステムの真の価値がここにあります。
