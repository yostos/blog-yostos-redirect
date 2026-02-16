+++
title = "エンジニアのためのポートフォリオサイトの構築"
description = "あまり経験してこなかった技術スタックでポートフォリオサイトを作ってみました"
date = 2025-03-08
aliases = ["/articles/2025/03/08/Portfolio-site-for-engieer"]

[taxonomies]
tags = ["Tech","Web"]
[extra]
social_media_card = "ogp.webp"
+++

今更ながら年初からWebデザインを教わるというシーンがありました。
しかし、毎朝タイピング練習で始まり、
「BRタグは非奨励」などとW3Cの仕様を知らないレベルの講師が
レベルの低い授業をやっていました。
100年かけてもWebデザインに行きつきそうにない。吐き気がしました。
割り切って我慢できるレベルを超えていました。

辞めましたが、
まぁ折角なのでWEBデザイナーが作るらしい「ポートフォリオ」なるものを、
3日ほど使ってこれまで深くやってこなかった技術スタックを作ってみました。

## はじめに

ポートフォリオサイトは自分のスキルや実績を効果的にアピールするための重要な
ツールらしいです。

Illustratorでデザインカンプ描いて、HTML/CSSでせっせとコーディング
なんてサイト作っても一体誰が見るんでしょう。
「あぁ、いいデザインだね」とか褒められると
本気で思っているバカがいるのでしょうか？
美的デザインだけで勝負するなんて、よほどの審美眼とセンスがないと無駄です。

この記事では、そんな90年代風なWebサイトでなく、
Node.js上でモダンなWebフレームワークであるNext.js/ReactとCSSフレームワークのTailwindCSS、
そしてUIコンポーネントを提供するdaisyUIを組み合わせて
ポートフォリオサイトを構築したのでそれを記録しています。

そして、結局このブログサイトも同じような技術スタック使って
再構築してしまいました。

## 使用する技術スタック

言語は型安全なTypeScriptを使用し、node/Reactベースで以下のようなフレームワークを使っています。

- **Next.js**: Reactベースのフルスタックフレームワーク
- **TailwindCSS**: ユーティリティファーストのCSSフレームワーク
- **daisyUI**: TailwindCSSのプラグインであるUIコンポーネントライブラリ
- **React Three Fiber**: 3DグラフィックスをReactで簡単に使うためのライブラリ
- **Font Awesome**: グラフィカルなアイコン文字を使うためのライブラリ
- **Framer Motion**: Framer Motionは、Reactアプリケーションにアニメーションを実装するためのライブラリ
- **AWS SDK**: 問い合わせフォームからAWSのAmanzon SESを使ってメールを送信するため

## プロジェクトセットアップ

1. プロジェクトを作成

```bash
# Next.jsプロジェクトの作成（TypeScript対応）
npx create-next-app@latest my-portfolio --typescript
√ Would you like to use ESLint? ... Yes
√ Would you like to use Tailwind CSS? ... Yes
√ Would you like to use `src/` directory? ... Yes（好みに応じて）
√ Would you like to use App Router? ... Yes
√ Would you like to customize the default import alias (@/*)? ... Yes
√ What import alias would you like configured? ... @/*
# 作成したプロジェクトディレクトリに移動
cd my-portfolio
# daisyUIのインストール
npm install daisyui
```

2. tailwind.config.jsの設定

プロジェクトルートにある`tailwind.config.js`ファイルを開き、daisyUIをプラグインとして追加します。

ライトとダーク両方のテーマをサポートするようにします。設定によりシステムのダーク／ライトモードの設定に応じて切り替わります。

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      // 必要に応じてテーマの拡張を追加
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark"], // 使用するテーマを設定
  },
};
```

3. 他のライブラリをインストール

```bash
npm install three @react-three/fiber @react-three/drei
npm install framer-motion
npm install @fortawesome/fontawesome-svg-core \
            @fortawesome/free-solid-svg-icons \
            @fortawesome/free-regular-svg-icons \
            @fortawesome/free-brands-svg-icons \
            @fortawesome/react-fontawesome
npm install aws-amplify @aws-sdk/client-ses @aws-sdk/client-sts
```

4. turbooackの有効化

Next.jsの開発サーバーを高速化するために、package.jsonのscriptsセクションを編集してturbopackを有効にします。

```json
"scripts": {
  "dev": "next dev --turbopack",
  "build": "next build",
  "start": "next start",
  "lint": "next lint"
}
```

## プロジェクトの構造

Next.jsのAppRouterを使用した基本的なプロジェクト構造を整えると、次のようなフォルダ構成になるはずです。

```txt
my-portfolio/
├── src/
│   ├── app/
│   │   ├── about/
│   │   │   └── page.tsx （自己紹介ページ）
│   │   ├── api/
│   │   │   └── contact
│   │   │       └── route.ts （メール送信）
│   │   ├── contact/
│   │   │   └── page.tsx （お問い合わせページ）
│   │   ├── globals.css （グローバルスタイル）
│   │   ├── layout.tsx （ルートレイアウト）
│   │   ├── page.tsx （トップページ）
│   │   └── works/
│   │       └── page.tsx （作品紹介ページ）
│   └── components/ （共通コンポーネント）
├── public/ （静的ファイル）
├── next.config.js
├── package.json
├── tailwind.config.js
└── tsconfig.json
```

## AWS Amplify へのデプロイ

今回はNext.jsアプリケーションのホスティング先としてVercelではなく、AWS Amplifyを選択しました。Amplifyを選んだ理由と、デプロイプロセスについて共有します。

Amplifyを選んだ理由は、次の通りです。

- **AWSエコシステムとの統合**: Amazon SESなど他のAWSサービスとの連携がシーム
  レスで、同じAWSコンソールから管理できる
- **既存のAWS知識の活用**: Amplify自体は今回初見だが一応前職なので管理コンソールなどは慣れており、
  Vercelを新たに学ぶ手間が不要だった。
- **料金体系**: 今回の内容であれば無料枠で十分

デプロイ手順をざっくり並べると次の通りです。

1. AWS管理コンソールからAmplifyサービスにアクセス
2. 「新しいアプリを作成」→「GitHubからホスティング」を選択
3. リポジトリと使用するブランチを選択（今回は`main`ブランチ）
4. ビルド設定を確認（Next.jsの場合は自動的に検出される）。認証情報などは面
   倒なので以下のようにビルドステップに組み込んだ。

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
        # 認証情報の書き込み
        # クライアント再度で必要な環境変数
        - echo "NEXT_PUBLIC_XXXX_API_URL=https://api.example.com" >>.env
        # サーバーサイド限定の環境変数
        - echo "AWS_XXXXX_ACCESS_KEY_ID="hogehogetaratara" >> .env
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - "**/*"
  cache:
    paths:
      - node_modules/**/*
```

## コンポーネント、その他について

- ヘッダー・コンポーネントについてはdaisyUIのNavbarを使わず、レスポンシブ対応、メニューの開閉に対応している。Navbarを使わない理由はないと思われるが、今回は実装検証のため自身で対応してみた。
- Works(作品)コンポーネントについては、トップページと作品ページで共用するため、作品情報をコンポーネントに内包させ引数で表示する作品の数を制御している。
- 一方でニュースのリストを作成するNewsコンポーネントは、現時点ではTopページしか使っていないが他のページでも使いまわせると考え、ニュース自体はコンポーネントに引数で渡すようにしている。
- グラフィカルな要素があまりないので3Dの立方体をトップページに置いている。3DCubeコンポーネントはモデリングする手間が面倒で、立方体をくるくる回しているだけである。
- 問い合わせフォームは、自身で検証したかったのでAmazon SESを使って実際にフォームをメールで飛ばすところまで作り込んでいる。必要な宛先アドレスや認証情報は、ビルド時に設定して環境変数で受け渡している。認証情報はシークレット情報経由などの方が良いと思われるが、どうもうまくいかなかったので妥協した。

具体的なソースは、[GitHubで公開](https://github.com/yostos/yostos-portfolio)しています。また、ポートフォリオ自体は、[https://portfolio.inagales.com](https://portfolio.inagales.com)で公開しています。いつ落とすか分かりませんが。

## まとめ

今回初めてまともにNext.jsを使いました。

- 今回はインターラクティブな要素もあったのでSEO的には良くないと思われるが、SSR/SSGを使わず全てクライアントコンポーネントとした。
- ファイルベースのルーティングは直感的で分かりやすいと感じた。
- APIルートでバックエンドの開発も同じプロジェクトでできるので、開発を分離することなくスムーズで行うことが出来そうである。フルスタックの開発者である前提ではあるが。
- 今回はVercelでなく、GitHubと連携させてAWSのAmplifyにデプロイした。思いの外スムーズにデプロイできた。
- CMSのようにテンプレートベースでなく、コードベースで部品の再利用、共通化ができるので、プログラマーがサイトを作るには非常にCMS特有のテンプレートのお手前を覚える必要がないので生産性がよい感じである。

楽しいお遊びでした。
