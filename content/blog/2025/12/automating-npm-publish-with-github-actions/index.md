+++
title = "GitHub Actionsでnpmパッケージ公開を自動化する - Trusted Publishingで実現するトークンレス運用"
description = "npm パッケージの公開を手動で行っていると、毎回トークンの管理やビルド、テストの実行など煩雑な作業が発生します。また、2025 年 9 月 29 日に GitHub が発表したnpmの認証強化により、Classic Token の廃止と、Trusted Publishing または Granular Access Token への移行が必要になりました。Trusted Publishing (OIDC) を使ってトークン管理不要のセキュアな公開フローを構築した手順を解説します。"
date = 2025-12-05
aliases = ["/articles/2025/12/05/automating-npm-publish-with-github-actions"]

[taxonomies]
tags = ["Tech","Node"]
[extra]
social_media_card = "ogp.webp"
+++

本記事では、私が開発している[jrnl-mcp](https://github.com/yostos/jrnl-mcp)パッケージで実装した、
GitHubが発表した[npmの認証強化](https://github.blog/changelog/2025-09-29-strengthening-npm-security-important-changes-to-authentication-and-token-management/)
対応の
Trusted Publishing (OIDC) を使用したトークン管理不要の自動公開について記載しています。

## npmの認証変更の背景

GitHubは2025年9月29日に、npmのセキュリティ強化として以下の変更を発表しました。

- Classic Access Tokenの廃止
- Trusted Publishing (OIDC) またはGranular Access Tokenへの移行推奨
- より細かい権限管理の実現

移行先として2つの選択肢があります。

1. Granular Access Token
2. Trusted Publishing (OIDC)

Granular Access Tokenは、従来のトークン方式を改良したものでパッケージごとの権限管理が可能となっていますが、定期的なトークンのローテーションが必要です。
Trusted Publishingはトークンを完全に排除した新しい認証方式で、公開を自動化しトークンを完全に排除したものです。

jrnl-mcpでは、トークン管理の手間を完全に排除できる **Trusted Publishing** を採用しました。

## 自動公開の仕組み

### 全体のフロー

jrnl-mcpでは、以下のフローで自動公開を実現しています。

1. GitHubでリリースを作成
2. GitHub Actionsが自動起動
3. 依存関係のインストールとテストを実行
4. npmへ自動公開

この仕組みにより、リリース作成だけでパッケージの公開が完了します。

### GitHub Actionsの設定

実際に使用しているワークフロー設定は以下の通りです。

```yaml
name: Publish to npm

on:
  release:
    types: [published]

permissions:
  contents: read
  id-token: write

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          registry-url: "https://registry.npmjs.org"

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm run test:ci

      - name: Publish to npm
        run: npm publish --provenance --access public
```

重要なポイントは、

1. GitHubのリリース機能を使用することで、手動でのトリガーが可能になる。これにより、意図しないタイミングでの公開を防ぐ。
2. `permissions`の設定により、GitHub Actionsはnpmに対して一時的なOIDCトークンを発行・認証する。長期的なトークンをSecretに保存する必要がない。
3. `npm publish --provenance --access public`により自動的にprovenance（出所証明）が生成され、パッケージがどのリポジトリから公開されたか検証可能となる。
4. `npm run test:ci`により公開前のテストを自動化する。

## Trusted Publishing の設定方法

Trusted Publishingを使用する場合、npm側での設定が必要です。

### 1. npm でパッケージを公開

まず、通常の方法で初回のパッケージを公開します（トークンを使用）。npm側でパッケージが存在している必要があるためです。

### 2. npm で Trusted Publishing を設定

1. [npm のパッケージ設定](https://www.npmjs.com/)にアクセス
2. 公開したパッケージの"Settings"タブを開く
3. "Publishing access"セクションで"Add a publisher"を選択
4. GitHub Actionsを選択し、以下を設定する
   - Repository: `<username>/<repository-name>`（例: `yostos/jrnl-mcp`）
   - Workflow: ワークフローファイル名（例: `publish.yml`）
   - Environment: 未指定（デフォルト）または特定の環境名

### 3. GitHub Actions の設定

前述のワークフロー設定で、`id-token: write` 権限を付与するだけで完了です。トークンをSecretに保存する必要はありません。

### トークンベースとの比較

Trusted Publishingを使用することで、以下の作業が不要になります。

- npmトークンの作成と保存
- GitHub Secretsへのトークン登録
- トークンの定期的なローテーション（Granular Access Tokenの場合、最大90日ごと）
- トークン漏洩のリスク管理

## まとめ

Trusted Publishing (OIDC) とGitHub Actionsを使用したnpmパッケージの自動公開により、以下のメリットが得られました。

- 公開作業の効率化
- トークン管理の完全な排除
- セキュリティの向上
- 品質の担保
- 透明性の確保（自動provenance生成）

特に、Trusted Publishingの導入により、トークンの定期的なローテーションや漏洩リスクの心配が不要になり、セキュリティと運用性が大幅に向上しました。npmパッケージを公開している方は、ぜひTrusted Publishingへの移行とGitHub Actionsによる自動化を検討してみてください。

Granular Access Tokenでもセキュリティは向上しますが、定期的なローテーション（最大90日ごと）が必要なため、可能であればTrusted Publishingの使用を推奨します。

## 参考リンク

- [Strengthening npm security: Important changes to authentication and token management](https://github.blog/changelog/2025-09-29-strengthening-npm-security-important-changes-to-authentication-and-token-management/)
- [jrnl-mcp GitHub Repository](https://github.com/yostos/jrnl-mcp)
- [npm Documentation: About access tokens](https://docs.npmjs.com/about-access-tokens)
