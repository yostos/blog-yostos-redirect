+++
title = "Amazon AmplifyのNode.jsバージョンアップ対応"
description = "2025年9月15日からAWS AmplifyがNode.js 14/16/18のサポートを終了するため、Node.js 24に更新した記録です。"
date = 2025-09-14
aliases = ["/articles/2025/09/14/amazon-amplify-node-versionup"]

[taxonomies]
tags = ["Tech", "AWS","Node"]
[extra]
social_media_card = "ogp.webp"
+++

I recieved the following email from AWS.

This blog does indeed use Amazon Amplify, but I thought it would be fine since I hadn't specified a Node.js version and the default was being used.

<blockquote>

2025 年 9 月 15 日から、AWS Amplify コンソールは Node.js 14、Node.js 16、Node.js 18 のサポートを終了します。この日を過ぎると、Node バージョンをアップグレードするまでアプリケーションへの更新をデプロイできなくなります。2025 年 9 月 15 日までに、Node.js 14、Node.js 16、Node.js 18 を使用するすべてのアプリケーションを Node.js 20 以降に更新してください。

Node.js 14、Node.js 16、Node.js 18 ですでにデプロイされているアプリケーションは引き続き実行され、更新をデプロイする必要がない限り影響はありません。

アップグレードする前に新しいブランチでアプリケーションをテストして、すべての機能が正常に動作することを確認することをお勧めします。移行ガイドラインについては、[1] ページの「アプリケーションの Node.js バージョンを更新する必要がある」セクションを参照してください。

影響を受けるリソースのリストは、AWS ヘルスダッシュボードの「影響を受けるリソース」タブにあります。

<footer>
    AWS 通知メール『AWS Amplify は、2025 年 9 月 15 日をもって Node.js 14/16/18 ベースのアプリのサポートを終了します』
    </footer>
  </blockquote>

Just to be sure, I checked the Node version and found that Node 18 was being used. That's no good.
Let's explicitly specify the version and rebuild.

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        # Node.jsバージョンを24に指定（ローカルのMacと同じ）
        - nvm use 24
        # バージョン確認（ログに出力）
        - node --version
        - npm --version
        # .envを削除
        - rm -f .env
        - npm ci --cache .npm --prefer-offline
        # 環境変数を.envファイルに出力
        - echo "NEXT_PUBLIC_SITE_URL=https://blog.yostos.org" >> .env

        (中略)

    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
  cache:
    paths:
      - .next/cache/**/*
      - .npm/**/*
```
