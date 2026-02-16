+++
title = "InkdropとClaudeのMCP統合"
description = "Inkdropの作者の方が、InkdropとClaudeのMCP統合についてYoutubeを上げていたので、早速検証しましたが、自分の書きためたKnowledgeをClaudeで活用できることがこんなに便利かと驚きました。"
date = 2025-03-28
aliases = ["/articles/2025/03/28/claude-integration-with-inkdrop"]

[taxonomies]
tags = ["Tech", "Generative AI"]
[extra]
social_media_card = "ogp.webp"
+++

作者の方の記事「
[Integrating my note app with Claude's MCP](https://www.devas.life/integrating-my-note-app-with-claudes-mcp/)
」と[YouTube](https://www.youtube.com/watch?v=ou4BYmY8Dq0&t=116s&themeRefresh=1)
を参考にしながら、実際にmacOSで検証してみました。前提としてClaude Desktopが稼働している必要が
あります。
元記事が英語なので日本語でまとめてみました。

<!-- toc -->

## メリットとユースケース

実施するまえに、InkdropとClaudeが統合すると何がうれしいのでしょう？

MCP統合により、ClaudeがInkdropのノートに直接アクセスし検索・作成・更新が可能となります。
これにより、次のようなメリットがあります。

- Claudeがユーザーの書きためた複数ノートの知見を横断的に分析・活用できる
- InkdropのNote管理作業を自動化し効率化できる

例えば考えられるユースケースは、次のようなものです。

- **パーソナル知識アシスタント**
  - 技術メモや学習ノートが蓄積されたInkdropで「JavaScriptのPromiseについて教えて」と質問すると、
    Claudeはあなたの過去のノートから関連情報を抽出し、あなた自身の理解や用語に合わせた説明を提供。
    さらに「これをプロジェクトXに適用するには？」と質問すると、プロジェクトXのノートも参照しながら具体的な実装アドバイスを返せる。
- **スマートな情報整理と要約**
  - 「先月の週次会議ノートを要約して月次報告として重要なアクションアイテムを抽出し、新しいノートにまとめて」と指示すると、
    Claudeは該当期間の会議ノートを検索・分析し、重要ポイントとアクションアイテムを抽出した新規ノートを自動生成。
    定期的なレビューや進捗管理が効率化される。

## インストール手順

まず [Inkdrop MCP Server](https://github.com/inkdropapp/mcp-server?tab=readme-ov-file)をインストールします。

```bash
npm install -g @inkdropapp/mcp-server
```

次にInkdrop内のHTTP Serverをセットアップのために、`config.json`を修正します。

Macの場合は`~/Library/Application Support/inkdrop/` です。

Inkdropを修了させて、既存の設定を壊さないように次の設定を追加します。`username`と`password`の設定は例なので、ちゃんと書き換えましょう。

```json
{
  "*": {
    "core": {
      "server": {
        "enabled": true,
        "port": 19840,
        "bindAddress": "127.0.0.1",
        "auth": { "username": "foo", "password": "bar" }
      }
    }
  }
}
```

設定したら、Inkdropを起動し次のコマンドで確認できます。

```bash
curl -v -u foo:bar http://localhost:19840/
# -> {"version":"5.10.0","ok":true}
```

`{"version":"5.10.0","ok":true}`と表示されればOKです。

次にCladue Desktopの設定が必要ですが、Claudeがどうもシェルに`bash`が使用されていることを前提としているため、
「[Integrating my note app with Claude's MCP](https://www.devas.life/integrating-my-note-app-with-claudes-mcp/)」の記事通りに設定しても動作しませんでした。

シェルの問題を回避するため、直接`npx`で実行するのでなく、シェルを指定したシェルスクリプトを作成しそれを実行させるように修正しました。
以下は`~/bin/inkdrop-mcp`などの名前で作成してください[^2]。

[^2]:
    シェルスクリプトを作成するのでなく、Claudeでの指定で、npxをフルパスで
    指定する方法もあります。お好みで。

```bash
#!/usr/bin/env fish
# fish版のMCPスクリプト
npx -y @inkdropapp/mcp-server
```

1行目の`fish`の部分は自身の環境に合わせて修正してください。

実行権限をつけておきます。

```bash
chmod +x ~/bin/inkdrop-mcp
```

## Claude Desktopの設定

設定したInkdropのサーバーの設定をClaude Desktopに追加します。Claude Desktopの設定画面を開くと下記のようになっています。


![Setting画面](setup-claude.webp)

この画面で「構成を編集」というボタンを押すと、Finderが起動して設定ファイルを示してくれます。このボタンを押さなくても、ターミナルから`~/Library/Application
Support/Claude/claude_desktop_config.json`を開いて編集しても大丈夫です。

次のような設定を追加します。`command`の設定は先ほど作成したシェルスクリプトを絶対パスで指定します。

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
    }
  }
}
```

編集後、Claude Desktopを再起動して設定画面を確認すると。`inkdrop`という設定が追加されているはずです。

## Inkdrop/Claude統合を試してみる

### MCP統合で何ができるか？

MCP統合で何ができるかは、[inkdrop/mcp-server](https://github.com/inkdropapp/mcp-server?ref=devas.life#)のREADME.mdを見ると何となく分かってきます。

<Subheading>Inkdrop MCPサーバーのComponents</Subheading>
<dl>
  <dt>`read-note`</dt>
  <dd>Noteの参照</dd>
  <dt>`search-notes`</dt>
  <dd>キーワードでのNoteの検索</dd>
  <dt>`list-notes`</dt>
  <dd> Notebookを指定してのNoteのリスト</dd>
  <dt>`create-note`</dt>{" "}
  <dd>Noteの作成 </dd>
  <dt>`update-note`</dt>{" "}
  <dd>既存の Noteの更新 </dd>
  <dt>`list-notebooks`</dt>{" "}
  <dd>Notebookのリスト </dd>
  <dt>`list-tags`</dt>{" "}
  <dd>タグのリスト </dd>
</dl>

### 実際に試してみる

この記事はInkdropでドラフトを執筆していますが、ここまで書いた時点でClaudeにInkdrop/Claude統合の方法を聞いてみました。
敢えて英語で聞いてみました。途中MCPの使用を許可するかというダイアログが出てくるので、「このチャットで許可」を押します。


![確認画面](dialog-claude.webp)

何度かダイアログが表示されますが、同様に許可していくと次のように表示されました。英語ですが、きちんとまとめられてます。


![結果画面](exampe-claude.webp)

## まとめ

Inkdrop内の自身のドキュメントがClaudeで活用できるのは思った以上に便利ですし、
Inkdropに知見をまとめていく行為もより価値を出せるようになります。

プロジェクトでClaude Codeを利用すると、プロジェクト内のコードをClaude Codeが
見渡してくれるので生産性が飛躍的に向上しますが、同じことをドキュメンテーショ
ンでもInkdropとの組み合わせで実現できます。

実際この記事の「メリットとユースケース」の章はClaudeにドラフトさせて、
Inkdropに追記させたものをもとに微調整しただけです。

しかもClaude Codeはものすごい勢いでAnthoropicのAPIの課金を消費していきます
が、こちらはClaude Desktopを利用するのでProプランを使っていれば特にそれ以上
費用は必要ありません。

Claude周りは最近楽しいな。
