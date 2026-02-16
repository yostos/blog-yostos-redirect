+++
title = "Next.jsでsitemap.xmlとrobots.txtを実装する"
description = "うっかり実装を忘れていたsitemap.xmlとrobots.txtをNext.jsのApp Routerを使用して実装しました。合わせて、検索エンジン最適化のためのベストプラクティスもまとめています。"
date = 2025-03-25
aliases = ["/articles/2025/03/25/creating-sitemap"]

[taxonomies]
tags = ["Tech","Web"]
[extra]
social_media_card = "ogp.webp"
+++

ウェブサイトを検索エンジンに正しくインデックスしてもらうためには、`sitemap.xml`と`robots.txt`の適切な実装が不可欠です。
このブログではNext.jsのApp Routerを使用して、これらのファイルを動的に生成するよう実装しました。

この記事では、その実装方法とSEOの観点からの注意点を説明します。

## 1. sitemap.xml 実装を実装する

### 1.1. sitemap.xmlとは

`sitemap.xml`は、ウェブサイト内の各ページのURLや更新頻度、優先度などの情報をまとめたXMLファイルです。
これにより、検索エンジンのクローラーがサイト構造を理解しやすくなり、効率的なインデックス作成が可能になります。

主な要素は以下の通りです。

- `<loc>` - ページのURL
- `<lastmod>` - 最終更新日
- `<changefreq>` - 更新頻度
- `<priority>` - 重要度

### 1.2. sitemap.xml の実装例

Next.jsのApp Routerでは、ルートハンドラーを使用して動的にsitemap.xmlを生成できます。
以下はこのブログでの実装例です。

```typescript
// src/app/sitemap.xml/route.ts

export async function GET() {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL;

  if (!siteUrl) {
    throw Error("Missing NEXT_PUBLIC_SITE_URL environment variable");
  }

  // 記事のIDを取得する関数
  function getArticleIds() {
    const articlesDir = path.join(process.cwd(), "src/app/articles");

    function scanDir(dir: string, baseDir = "") {
      let results: string[] = [];
      const entries = fs.readdirSync(dir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        const relativePath = path.join(baseDir, entry.name);

        if (entry.isDirectory()) {
          results = [...results, ...scanDir(fullPath, relativePath)];
        } else if (entry.name === "page.mdx") {
          results.push(baseDir);
        }
      }

      return results;
    }

    return scanDir(articlesDir);
  }

  const articleIds = getArticleIds();

  // 最新の記事の日付を取得する関数
  function getLatestArticleDate() {
    let latestDate = new Date(0); // 1970-01-01

    for (const id of articleIds) {
      try {
        // ファイルから直接コンテンツを読み込む
        const mdxPath = path.join(
          process.cwd(),
          "src/app/articles",
          id,
          "page.mdx",
        );
        const mdxContent = fs.readFileSync(mdxPath, "utf-8");

        // 日付を抽出
        const dateMatch = mdxContent.match(/date:\s*["'](.+?)["']/);

        if (dateMatch) {
          const extractedDate = new Date(dateMatch[1]);
          // 有効な日付かつ最新の場合は更新
          if (!isNaN(extractedDate.getTime()) && extractedDate > latestDate) {
            latestDate = extractedDate;
          }
        }
      } catch (error) {
        console.error(
          `Error processing article ${id} for date extraction:`,
          error,
        );
      }
    }

    // ISO形式の日付を返す（例: 2025-03-25）
    return latestDate.toISOString().split("T")[0];
  }

  // 最新記事の日付を取得
  const latestArticleDate = getLatestArticleDate();

  // 静的ページのURL、changefreq、priority 設定
  const staticPages = [
    {
      url: "",
      changefreq: "daily",
      priority: "1.0",
      lastmod: latestArticleDate,
    }, // ホームページ
    { url: "/about", changefreq: "monthly", priority: "0.5" },
    {
      url: "/articles",
      changefreq: "daily",
      priority: "0.9",
      lastmod: latestArticleDate,
    }, // 記事一覧ページには最新記事の日付
    { url: "/whisper", changefreq: "daily", priority: "0.4" },
    { url: "/uses", changefreq: "monthly", priority: "0.7" },
    { url: "/music", changefreq: "monthly", priority: "0.5" },
  ];

  // サイトマップXMLの作成
  let sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
`;

  // 静的ページをサイトマップに追加
  for (const page of staticPages) {
    sitemap += `  <url>
    <loc>${siteUrl}${page.url}</loc>
    ${page.lastmod ? `<lastmod>${page.lastmod}</lastmod>` : ""}
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>
`;
  }

  // 記事ページをサイトマップに追加
  for (const id of articleIds) {
    try {
      // ファイルから直接コンテンツを読み込む
      const mdxPath = path.join(
        process.cwd(),
        "src/app/articles",
        id,
        "page.mdx",
      );
      const mdxContent = fs.readFileSync(mdxPath, "utf-8");

      // 日付を抽出
      const dateMatch = mdxContent.match(/date:\s*["'](.+?)["']/);
      let date = new Date().toISOString().split("T")[0];

      if (dateMatch) {
        const extractedDate = new Date(dateMatch[1]);
        // 有効な日付の場合のみ使用
        if (!isNaN(extractedDate.getTime())) {
          date = extractedDate.toISOString().split("T")[0];
        }
      }

      const articleUrl = `${siteUrl}/articles/${id}`;

      sitemap += `  <url>
    <loc>${articleUrl}</loc>
    <lastmod>${date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
`;
    } catch (error) {
      console.error(`Error processing article ${id} for sitemap:`, error);
    }
  }

  // サイトマップを閉じる
  sitemap += `</urlset>`;

  return new Response(sitemap, {
    status: 200,
    headers: {
      "content-type": "application/xml",
      "cache-control": "s-maxage=86400",
    },
  });
}
```

この実装では以下のポイントに注目しています。

1. **記事の動的探索**: `getArticleIds()`関数を使用して、articlesディレクトリ内のすべてのMDXファイルを再帰的に探索
1. **最新記事日付の検出**: `getLatestArticleDate()`関数で、全記事から最新の記事日付を取得
1. **記事以外の設定**: 記事以外はパスが固定なので予め配列にパスと更新頻度を設定
1. **更新頻度と重要度の最適化**: 各ページタイプに適した`changefreq`と`priority`の値を設定
   - 個別記事ページ: `changefreq:monthly` と `priority: 1.0`で固定
   - その他のページ: 配列でページの特性に応じて設定
1. **ホームと記事一覧に最新日付を適用**: トップページと記事一覧ページには最新記事の日付を`lastmod`として使用し、これらのページが最新コンテンツを反映していることを検索エンジンに伝える
1. **柔軟な構造**: `page.lastmod`が存在する場合のみ`<lastmod>`タグを出力する条件付きレンダリング
1. **キャッシュ設定**: `cache-control`ヘッダーで24時間のキャッシュを設定

### 1.3. changefreq の適切な設定

`changefreq`値は検索エンジンへのヒントであり、実際のクロール頻度を保証するものではありません。
一般的な設定の目安。

- `always`: 常に変化するページ（リアルタイムデータ表示など）
- `hourly`: 1時間単位で更新（ニュースページなど）
- `daily`: 毎日更新（ブログトップ、記事一覧など）
- `weekly`: 週単位で更新（プロジェクトページなど）
- `monthly`: 月単位で更新（Aboutページなど）
- `yearly`: 年単位で更新（利用規約など）
- `never`: 更新されないページ（アーカイブなど）

ページの実際の更新パターンに合わせた設定が望ましいですが、最終的なクロール頻度は検索エンジンのアルゴリズムが決定します。

### 1.4. lastmod の意義と適切な設定

`lastmod`はページの最終更新日を示し、以下の点で重要です。

- **クローラーの効率化**: 検索エンジンは最近変更されたページを優先的に再クロールできる
- **インデックス更新の促進**: 新しいコンテンツや変更を素早くインデックスに反映
- **鮮度シグナル**: コンテンツの最新性を伝えるシグナルとなる可能性がある

今回の実装では以下のアプローチを取っています。

1. **個別記事**: 記事のfrontmatterから日付を抽出して使用
2. **ホームページと記事一覧**: すべての記事から最新の日付を取得し反映（最新のコンテンツへのリンクを含むため）
3. **その他のページ**: 明示的に指定しない（検索エンジンが自動判断）

この方法により、各ページが適切な最終更新日を持ち、検索エンジンが最新のコンテンツを効率的に処理できるようになります。

## 2. robots.txt を実装する

`robots.txt`はクローラーに対するルールを記述したファイルで、同様にルートハンドラーで実装できます。

```typescript
// src/app/robots.txt/route.ts
export async function GET() {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL;

  if (!siteUrl) {
    throw Error("Missing NEXT_PUBLIC_SITE_URL environment variable");
  }

  const robotsTxt = `# https://www.robotstxt.org/robotstxt.html
User-agent: *
Allow: /

# Sitemaps
Sitemap: ${siteUrl}/sitemap.xml
`;

  return new Response(robotsTxt, {
    status: 200,
    headers: {
      "content-type": "text/plain",
      "cache-control": "s-maxage=86400",
    },
  });
}
```

この実装ではすべてのロボットにサイト全体へのアクセスを許可し、sitemap.xmlの場所を明示しています。

### 2.1. robots.txt実装上の注意点

1. **環境変数の設定**: `NEXT_PUBLIC_SITE_URL`を必ず設定する
2. **キャッシュの検討**: 頻繁に記事を追加する場合は、キャッシュ期間を短くする(個人のブログサイトなので現在の24時間で十分)
3. **エラーハンドリング**: 記事読み込みエラーが全体に影響しないようtry-catchで処理
4. **検証**: [Google Search Console](https://search.google.com/search-console)でサイトマップを登録し、エラーがないか確認する

## 3. まとめ

適切な`sitemap.xml`と`robots.txt`の実装はSEOの基本です。Next.jsのApp Routerを使うと、これらのファイルを動的に生成できるため、コンテンツの増加に合わせて自動的に更新されるサイトマップを維持できます。

更新頻度や優先度の設定は、サイトのコンテンツ特性を考慮して決定しましょう。最終的には検索エンジンのアルゴリズムが実際のクロール頻度を決定しますが、適切なヒントを提供することで、より効率的なインデックス作成を促進できます。
