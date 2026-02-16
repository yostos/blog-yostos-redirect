+++
title = "Exploring Claude Code: Hands-On with Anthropic's AI-Powered Coding Assistant"
description = "I tried Claude Code.Claude Code is the latest AI-driven coding assistant developed by Anthropic.It's a command-line coding tool that connects to Anthropic's servers via API andutilizes the Claude 3.7 Sonnet model to support developers. Therefore,you can receive the same level of advanced AI reasoning support as when using Claude 3.7 Sonnet from a browser."
date = 2025-03-12
aliases = ["/articles/2025/03/12/Claude-code"]

[taxonomies]
tags = ["Tech", "Generative AI","Claude Code"]
[extra]
social_media_card = "ogp.webp"
+++

[Claude Code]: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview

[Claude Code][Claude Code]を試してみました。

Claude Codeは、Anthropicが開発した最新のAI駆動型コーディングアシスタントです。
コマンドラインコーディングツールで、AnthropicのサーバーにAPIを介して接続し
Claude 3.7 Sonnetモデルを活用して開発者を支援します。従って、
ブラウザからClaude 3.7 Sonnetを扱うのと同等の高度なAI推論の支援を受けることができます。

## Getting Started With Claude Code

Claude Codeを使う前提がいくつかあります。

1. Claude Codeはまだβ版でResearch Previewのため、
   [Claude Codeのページ][Claude Code]からβ版参加のWaiting Listの登録して、アクセ
   ス許可をもらう必要があ。
2. Node.js 18以上が必要。以下のソフトウェアはオプション。

- git 2.23+
- GitHub or GitLab CLI for PR workflows
- ripgrep

3. [Supported Countries](https://www.anthropic.com/supported-countries)に居
   る必要。日本は対象となっているので大丈夫。

もちろん、ターミナルから使うものなので、MacであればiTerm2などがあったほうが
よいでしょう。

上記がクリアできたら、Claude Codeを認証して使用するために、AnthropicからAPI
キーを生成して払い出しておきます。

Claude Codeのインストールは以下のコマンドで行います。

```bash
npm install -g @anthropic/claude-code
```

インストールが完了したら、次のコマンドでClaude Codeを起動して、初回だけOAuth
認証を完了させておきます。

```bash
claude
```

## What Claude Code Can Do For You?

見てもらったほうが早いので、下に操作した例を貼り付けておきます。
適当に作った[Webサイトのリポジトリ
](https://github.com/yostos/yostos-portfolio)について、分析したのに
`README.md`の更新を依頼してみました。引用ブロック担っている部分が私の指示したものです。

単純なWebサイトですが、Next.jsを使いそこそこコードの量もありましたが、
数秒で私が適当に書いていた`README.md`を依存ソフトウェアなども正確に記載し完璧に仕上
げてくれました。

```markdown
╭──────────────────────────────────────────────────────────────╮
│ ✻ Welcome to Claude Code research preview! │
│ │
│ /help for help │
│ │
│ cwd: /Users/yostos/ghq/github.com/yostos/yostos-portfolio │
╰──────────────────────────────────────────────────────────────╯

Tips for getting started:

1.  Run /init to create a CLAUDE.md file with instructions for Claude.
2.  Ask Claude questions about your codebase.
3.  Ask Claude to implement changes to your codebase.

> プロジェクトの概要を教えてください。これはどのようなプロジェクトで何を目的としていますか？

⏺ プロジェクトの概要を調査します。

⏺ Task(Please analyze this project to understand its purpose and overview. Check the following:…)…
⎿  Done (6 tool uses · 14.6k tokens · 22.1s)

⏺ これは Next.js で構築された個人ポートフォリオサイトです。ウェブ技術とデザイン手法をテストするための練習プロジェ
クトとして開発されています。主な特徴:

- Next.js と TypeScript を使用
- Tailwind CSS とdaisyUI でスタイリング
- Three.js と React Three Fiber による3D要素
- Framer Motion によるアニメーション
- AWS サービス（SES、Amplify）をバックエンド機能に使用

サイト構成:

- 3D要素、サービス、ニュース、作品を含むホームページ
- About ページ
- 問い合わせフォーム
- 作品ポートフォリオ
- 音楽セクション
- ニュース/ブログセクション

> では、README.mdは内容を正しく書き示しているでしょうか？もし齟齬があればアップデートしてください。

⏺ README.mdの内容を確認します。

⏺ Read(file_path: "README.md")…
  ⎿  # Porfolio Site with Next.js
個人でWeb技術とデザイン手法の検証を目的として 片手間で作った練習用ポートフォリオです。
... (+27 lines)

⏺ Task(Compare the actual project features and technologies with what's listed in the README.md. The README seems minimal …
and might be missing some technologies used in the project. …)
⎿  Done (6 tool uses · 18k tokens · 30.4s)

⏺ READMEには更新が必要です。現在のREADMEは非常にシンプルで、プロジェクトで使われている多くの技術が記載されていませ
ん。以下の点を修正すべきです：

1. タイトルのタイプミス（"Porfolio" → "Portfolio"）
2. 使用技術の詳細リスト（Three.js、Framer Motion、AWS services等が未記載）
3. プロジェクト機能の説明（3D要素、ポートフォリオ表示、問い合わせフォーム等）

更新しますか？

> 更新してください。また、表記は日本語でお願いします。英語の部分があれば更新してください。

⏺ READMEを日本語で更新します。

⏺ Update(file_path: README.md)…
⎿ Updated README.md with 54 additions and 14 removals
1 # Porfolio Site with Next.js
1 # ポートフォリオサイト with Next.js
2
3 個人でWeb技術とデザイン手法の検証を目的として 片手間で作った練習用ポートフォリオです。
3 個人でWeb技術とデザイン手法の検証を目的として片手間で作った練習用ポートフォリオです。
4
5 以下を使用しています。
5 ## 使用技術
6
7 - [Next.js](https://nextjs.org)
8 - [Tailwind CSS](https://tailwindcss.com)
9 - [daisyUI](https://daisyui.com)
7 本プロジェクトでは以下の技術を使用しています。
8
9 ## Getting Started
9 ### フロントエンド
10 - [Next.js](https://nextjs.org) - Reactフレームワーク（サーバーサイドレンダリングとルーティング）
11 - [React](https://reactjs.org) - ユーザーインターフェース構築のためのJavaScriptライブラリ
12 - [TypeScript](https://www.typescriptlang.org) - 型付けされたプログラミング言語
13 - [Tailwind CSS](https://tailwindcss.com) - ユーティリティファーストのCSSフレームワーク
14 - [daisyUI](https://daisyui.com) - Tailwind CSS用コンポーネントライブラリ
15 - [Three.js](https://threejs.org) - WebGL用3Dグラフィックスライブラリ
16 - [React Three Fiber](https://github.com/pmndrs/react-three-fiber) - Three.js用Reactレンダラー
17 - [React Three Drei](https://github.com/pmndrs/drei) - React Three Fiber用ヘルパー
18 - [Framer Motion](https://www.framer.com/motion/) - React用アニメーションライブラリ
19
20 First, run the development server:
20 ### バックエンド
21 - [AWS SES](https://aws.amazon.com/ses/) - 問い合わせフォーム用メールサービス
22 - [AWS Amplify](https://aws.amazon.com/amplify/) -
Webおよびモバイルアプリケーションのためのプラットフォーム
23
24 ### UI/UX
25 - [FontAwesome](https://fontawesome.com) - アイコンライブラリ
26 - [M PLUS 1 Code](https://fonts.google.com/specimen/M+PLUS+1+Code) - コード表示用の現代的なフォント
27
28 ## 機能
29
30 - **3Dインタラクティブ要素** - Three.jsとReact Three Fiberを用いたインタラクティブな3Dキューブ
31 - **レスポンシブデザイン** - 様々な画面サイズに適応するモバイルフレンドリーなインターフェース
32 - **ポートフォリオショーケース** - 作品サンプルとプロジェクトのギャラリー
33 - **問い合わせフォーム** - AWS SESを統合した直接コミュニケーション用フォーム
34 - **ダーク/ライトモード** - テーマ切り替え機能
35 - **音楽プレーヤー** - 音楽ショーケース用SoundCloud統合
36
37 ## 始め方
38
39 まず、開発サーバーを実行します:
40
41 `bash
     42  npm run dev
     43  # or
     43  # または
     44  yarn dev
     45  # or
     45  # または
     46  pnpm dev
     47  # or
     47  # または
     48  bun dev
     49  `
50
51 Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
51 ブラウザで [http://localhost:3000](http://localhost:3000) を開くと結果が表示されます。
52
53 You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.
53 `app/page.tsx`
を編集することでページの編集を開始できます。ファイルを編集すると、ページは自動更新されます。
54
55 This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts)
to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.
55 ## 環境変数
56
57 問い合わせフォーム機能を使用するには、以下のAWS環境変数を設定する必要があります:
58
59 `      60  AWS_ACCESS_KEY_ID=あなたのAWSアクセスキー
     61  AWS_SECRET_ACCESS_KEY=あなたのAWSシークレットキー
     62  SES_REGION=あなたのAWSリージョン (デフォルト: ap-northeast-1)
     63  SES_FROM_EMAIL=送信者メールアドレス
     64  SES_TO_EMAIL=受信者メールアドレス
     65  `
66
67 ## その他
68
69 このプロジェクトでは
[`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) を使用して、
最適なパフォーマンスのためにカスタムフォントを自動的に最適化して読み込んでいます。

⏺ README.mdを日本語に完全更新しました。以下の内容を追加・修正しました：

1. タイトルを「ポートフォリオサイト with Next.js」に修正
2. 詳細な技術スタックをフロントエンド、バックエンド、UI/UXの3セクションに分けて記載
3. プロジェクトの主要機能（3D要素、レスポンシブデザイン、ポートフォリオ機能など）を追加
4. 環境変数の設定方法も追加
5. すべての英語部分を日本語に翻訳

これでREADMEは実際のプロジェクトの機能と技術をより正確に反映しています。

╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ > quit │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
! for bash mode · / for commands · esc to undo ✓ Update installed · Restart to apply
```

## まとめ

今回はAnthropicが開発したAI駆動型コーディングアシスタント「Claude Code」を試
してみました。まだResearch Previewの段階ですが、その能力は非常に印象的です。
コマンドラインから簡単に使用でき、コードベースの分析や更新を数秒で行うことが
できます。

実際の使用例として示したように、プロジェクトの概要を理解し、READMEの更新を行
う作業も正確かつ迅速に実行してくれました。Claude 3.7 Sonnetモデルの高度な推
論能力をコマンドラインから活用できることで、開発ワークフローが大幅に効率化さ
れる可能性を感じました。

AI駆動型の開発支援ツールはますます進化しており、Claude Codeはその最前線にあ
るツールの1つと言えるでしょう。今後の正式リリースや機能拡張に期待したいと思
います。
