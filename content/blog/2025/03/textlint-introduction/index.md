+++
title = "textlintで日本語ブログの品質を向上させよう"
description = "textlintを活用して日本語の技術ブログ記事の品質を向上させる方法を紹介します。特にこのブログではMarkdownでなくMDXを使用しているので、MDXファイルに対する最適な設定と導入手順を解説します。"
date = 2025-03-23
aliases = ["/articles/2025/03/23/textlint-introduction"]

[taxonomies]
tags = ["Tech","Writing","Software","Weblog"]
[extra]
social_media_card = "ogp.webp"
+++

## textlintとは

[textlint](https://textlint.github.io/)は、テキスト上の問題を洗い出すための静的解析ツールです。
特に日本語のテキスト校正において優れた機能を持っており、文章のスタイル、用語の統一、表記ゆれ、誤字脱字などをチェックできます。
Markdownファイルなどの構造化されたテキストファイルに対して適用できるため、
ブログ記事や技術文書の品質を向上させるのに最適です。

## なぜtextlintを導入したのか

技術ブログを書く際に直面する問題は、以下のようなものがあります。

- 「ですます調」と「である調」の混在
- 全角と半角の間のスペースの不統一
- 句読点や括弧の前後の余計なスペース
- カタカナ語の間に中黒（・）や半角スペースがない

これらの問題は、読者にとって違和感を与え、プロフェッショナルさを損なう可能性があります。textlintを導入することで、これらの問題を自動的に検出し、一貫した文章スタイルを維持できるようになります。

## インストールと設定

### 1. 必要なパッケージのインストール

次のコマンドでtextlintと必要なルールをインストールします。

```bash
npm install --save-dev textlint \
  textlint-rule-preset-ja-spacing \
  textlint-rule-preset-ja-technical-writing \
  textlint-rule-no-mix-dearu-desumasu \
  textlint-filter-rule-comments \
  textlint-filter-rule-node-types \
  textlint-plugin-mdx
```

### 2. `.textlintrc`の設定

プロジェクトのルートディレクトリに`.textlintrc`ファイルを作成し、以下のように設定します。

```json
{
  "filters": {
    "comments": true,
    "node-types": {
      "nodeTypes": ["jsx", "code", "inline-code", "html", "BlockQuote"]
    },
    "allowlist": {
      "allow": [
        "/<blockquote[^>]*>[\\s\\S]*?<\\/blockquote>/",
        "/<blockquote>([\\s\\S])*?<\\/blockquote>/g"
      ]
    }
  },
  "plugins": ["mdx"],
  "rules": {
    "preset-ja-spacing": {
      "ja-nakaguro-or-halfwidth-space-between-katakana": true,
      "ja-no-space-around-parentheses": true,
      "ja-no-space-between-full-width": true,
      "ja-space-between-half-and-full-width": {
        "space": "always",
        "exceptPunctuation": true
      },
      "ja-space-after-exclamation": true,
      "ja-space-after-question": true,
      "ja-space-around-code": false
    },
    "preset-ja-technical-writing": {
      "sentence-length": {
        "max": 200
      },
      "no-exclamation-question-mark": {
        "allowHalfWidthQuestion": true,
        "allowFullWidthQuestion": true
      },
      "ja-no-weak-phrase": false,
      "max-kanji-continuous-len": {
        "max": 20
      },
      "ja-no-mixed-period": {
        "allowPeriodMarks": ["箇条書き", "リスト", "。", "、", "」"],
        "forceAppendPeriod": false,
        "checkBlockQuote": false,
        "checkListItem": false,
        "allowExceptionContext": true,
        "ignorePeriodInQuotation": true
      }
    },
    "no-mix-dearu-desumasu": {
      "preferInHeader": "である",
      "preferInBody": "ですます",
      "preferInList": "である",
      "strict": false
    },
    "@textlint-rule/textlint-rule-no-invalid-control-character": false,
    "ja-technical-writing/no-doubled-conjunction": false,
    "ja-technical-writing/no-doubled-conjunctive-particle-ga": false
  }
}
```

### 3. package.jsonにスクリプトを追加

```json
{
  "scripts": {
    "check": "textlint \"src/app/articles/**/*.mdx\""
  }
}
```

## 設定の詳細解説

### フィルター

MDXファイルには、本文の他にJSXコンポーネントやコードブロックが含まれています。
これらに対してtextlintのルールを適用すると誤検出が多発します。そのため、
フィルターを設定して特定の部分をチェック対象から除外しました。

```json
"filters": {
  "comments": true,
  "node-types": {
    "nodeTypes": ["jsx", "code", "inline-code", "html", "BlockQuote"]
  },
  "allowlist": {
    "allow": [
      "/<blockquote[^>]*>[\\s\\S]*?<\\/blockquote>/",
      "/<blockquote>([\\s\\S])*?<\\/blockquote>/g"
    ]
  }
}
```

- `comments`: コメント部分をチェック対象から除外
- `node-types`: JSX、コードブロック、インラインコード、HTMLタグ、引用文をチェック対象から除外
- `allowlist`: 正規表現で指定したパターンをチェック対象から除外

blockquote要素内の引用文は自分の文章でなく修正しようもないため、
対象から外しています。

### ルール

#### 1. 「ですます調」と「である調」の統一 (no-mix-dearu-desumasu)

文体の一貫性を保つためのルールです。

```json
"no-mix-dearu-desumasu": {
  "preferInHeader": "である",
  "preferInBody": "ですます",
  "preferInList": "である",
  "strict": false
}
```

- 見出しは「である調」とする
- 本文は「ですます調」とする
- リストは「である調」とする
- `strict: false`で厳密すぎるチェックを回避する

#### 2. 日本語の間隔に関するルール (preset-ja-spacing)

```json
"preset-ja-spacing": {
  "ja-nakaguro-or-halfwidth-space-between-katakana": true,
  "ja-no-space-around-parentheses": true,
  "ja-no-space-between-full-width": true,
  "ja-space-between-half-and-full-width": {
    "space": "always",
    "exceptPunctuation": true
  },
  "ja-space-after-exclamation": true,
  "ja-space-after-question": true,
  "ja-space-around-code": false
}
```

- カタカナ語の間には中黒または半角スペースを入れる規則である
- 括弧の前後には余分なスペースを入れない規則である
- 全角文字の間にはスペースを入れない規則である
- 半角と全角の間には常にスペースを入れる規則である（句読点は例外）
- 感嘆符と疑問符の後にはスペースを入れる規則である
- コードの前後のスペースは不要とする規則である

#### 3. 技術文書向けのルール (preset-ja-technical-writing)

技術文書に適した日本語表現をチェックする包括的なルールセットです。冗長な表
現、読みにくい文章構造、一文の長さなどをチェックする。以下のような設定を追加
しています。

- `max-kanji-continuous-len`: 漢字の連続使用を20文字までに制限を緩和
- 助詞の重複や冗長表現、不自然なアルファベット使用などを検出する機能を含む
- 技術文書らしい表現をチェックし、読みやすさを向上させる

## MDXファイルの対応と実行時の問題解決

Next.jsのブログでは、多くの場合MDXファイルを使用しています。
デフォルトのtextlint設定ではMDXファイルを認識できないことがあります。
実際に`npm run check`を実行してみると、
以下のようなデバッグ情報が表示されました。

```
No Process files that are un-support extensions: ["/path/to/your/blog/src/app/articles/.../page.mdx",...]
```

この問題を解決するには、前述のインストール手順にあるように、`textlint-plugin-mdx`パッケージを追加し、`.textlintrc`ファイルの設定に`"plugins": ["mdx"]`を追加する必要があります。

### 正しく設定した後の実行結果

正しく設定した後、`npm run check`を実行すると、ブログ内のMDXファイルが検査され、以下のような結果が表示されます。

```
/path/to/your/blog/src/app/articles/.../page.mdx
  23:138  ✓ error  原則として、全角文字と半角文字の間にスペースを入れます。                 ja-spacing/ja-space-between-half-and-full-width
  27:32   error    文末が"。"で終わっていません。                                           ja-technical-writing/ja-no-mixed-period
  40:7    ✓ error  原則として、全角文字と半角文字の間にスペースを入れます。                 ja-spacing/ja-space-between-half-and-full-width
  167:15  ✓ error  かっこの外側、内側ともにスペースを入れません。                           ja-spacing/ja-no-space-around-parentheses
  167:41  error    箇条書き: "である"調 でなければなりません                                no-mix-dearu-desumasu
```

チェックマーク（✓）がついているエラーは自動修正可能なものです。これらを一括修正するには、以下のコマンドを実行します。

```bash
npx textlint --fix "src/app/articles/**/*.mdx"
```

ただし、すべてのエラーが自動修正できるわけではありません。特に文体（「ですます調」と「である調」）や文末の句点、文の長さなどに関するエラーは、意図に合わせて手動で修正する必要があります。

### CI/CDパイプラインへの組み込み

品質チェックを自動化するために、GitHub Actionsなどのワークフローにtextlintを組み込むこともできます。例えば、以下のような`.github/workflows/textlint.yml`ファイルを作成することで、プルリクエスト時に自動的に文章をチェックできます。

```yaml
name: Textlint

on:
  pull_request:
    paths:
      - "src/app/articles/**/*.mdx"

jobs:
  textlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "20"
          cache: "npm"
      - run: npm ci
      - run: npm run check
```

## 期待される効果

textlintを導入することで得られる主な効果は以下の通りです。

1. **一貫した文体**: 文体が混在しない文章になる
2. **読みやすさの向上**: 適切な空白や区切りにより、読みやすい文章になる
3. **プロフェッショナルな印象**: 表記の一貫性により、プロフェッショナルな印象を与える
4. **効率的な校正**: 手動での確認作業が減り、効率的に校正できる
5. **品質の均一化**: 複数の執筆者がいる場合でも、文章スタイルを統一できる
6. **CI/CDパイプラインとの統合**: Node.jsベースのツールであるため、GitHub ActionsやJenkins、AWS CodeBuildなどのCI/CDパイプラインに容易に組み込める

## まとめ

textlintは、日本語の技術ブログを書く際の強力な味方です。
適切な設定により、文章の品質を向上させ、読者にとって読みやすく一貫性のある記事を提供できます。特にMDXを使ったブログでは、フィルター設定により、記事本文とコードやJSXを適切に区別してチェックできます。

Next.js + Tailwind Plus(旧Tailwind UI)をベースにしたブログシステムとの相性
も抜群です。Node.jsベースのツールであるため、同じエコシステム内で簡単に導入
でき、npmスクリプトとして実行できます。さらに、GitHub ActionsなどのCI/CD
パイプラインに組み込むことで、プルリクエスト時に自動的に文章をチェックし、品
質を担保も可能です。

今回紹介した設定は、MDXファイルを使ったNext.jsブログに最適化されていますが、他の形式の文書にも応用可能です。自分の文書スタイルや好みに合わせてカスタマイズしてみてください。

定期的に`npm run check`を実行し、指摘された問題を修正することで、ブログ記事の品質を着実に向上させることができます。
