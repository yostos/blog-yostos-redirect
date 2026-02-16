+++
title = "Claude Sonnet 4.5リリース"
description = "9月30日にClaude Sonnet 4.5がリリースされました。"
date = 2025-10-03
aliases = ["/articles/2025/10/03/claude-4-5"]

[taxonomies]
tags = ["Tech", "Generative AI", "Claude Code"]
[extra]
social_media_card = "ogp.webp"
+++

<details>
<summary>Table of Contents</summary>
  <!-- toc -->
</details>

## tl;dr

**Claude Sonnet 4.5** の詳細は
[Anthropic のアナウンス](https://www.anthropic.com/news/claude-sonnet-4-5) を読んでもらうとして、
まとめると次のような点が変更となっています。

- コーディング、ソフトウェアエンジニアリング性能がどえらい高い。Opus 4.1と比較しても負けない
- 人間の感覚に近づいた(ミスアラインメント軽減)
- Claude Codeがv 2.0.0にアプデされ、チェックポイント機能が付いた
- Claude Code SDKがClaude Agent SDKに
- Claude for ChromeがMaxユーザー（ウェイトリスト登録者）に提供開始
- Claude APIのコンテキスト管理に機能追加

## Claude Code v 2

Claude CodeがV 2となりました。

インストールは以下のコマンドで行ないます。

```bash
npm install -g @anthropic-ai/claude-code
```

主な変更点は次の通りです。

- チェックポイント機能が追加された。変更前のタイミングでコードを自動保存し、`/rewind` コマンド(ESCキーを2回押下でも可)で
  前のバージョン戻すことが可能となった。復元は、コード、会話、またはその両方を選ぶことができる。
- 思考モードをタブキーで切り替えることが出来るようになった。
- Ctrl-Rキーで履歴の検索が可能となった。
- 利用状況を確認する `/usage`コマンドが追加となった。

## Claude API のコンテキスト管理機能

Claude Developer Platformに、より長く複雑なエージェントタスクを実行するための新機能が追加されました。

主な機能は次の通りです。

- **コンテキスト編集機能**: トークン制限に近づいた際、古いツール呼び出しと結果をコンテキストウィンドウから自動的にクリアする。
- **メモリツール**: ファイルベースのシステムを通じて、コンテキストウィンドウの外に情報を保存し参照できる。専用のメモリディレクトリでファイルの作成、読み取り、更新、削除が可能である。

これらの機能により、以下のようなことが実現できるようになります。

- 長期的なコーディングプロジェクトで、デバッグ中に発見した洞察を保存し、翌日のセッションでも活用できる
- 調査・研究タスクで、複数のドキュメントから重要な情報を蓄積し、ナレッジベースを構築できる
- 大規模なデータ処理ワークフローで、コンテキストが満杯になっても処理を継続できる

これらの機能を組み合わせることで、ベースラインと比較して39%のパフォーマンス向上が確認されています。

なお、これらはAPIを利用してエージェントやアプリケーションを構築する開発者向けの機能です。Amazon BedrockおよびGoogle CloudのVertex AIでも利用可能です。
