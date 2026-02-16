+++
title = "Open Graph Protocol対応"
description = "このブログは適当に実装したので、Open Graph Protocolに対応してしていませんでした。今更ですが、Open Graph Protorol対応しSNSでリンクを投稿した時に記事情報が表示できるようにしてみました。"
date = 2025-04-07
aliases = ["/articles/2025/04/07/open-graph-protocol"]

[taxonomies]
tags = ["Tech", "Web"]
[extra]
social_media_card = "ogp.webp"
+++

## Open Graph Protocolとは

Open Graph Protocol(OGPとも呼ばれます)は、Webページの内容をSNSなどで共有する際に、正確な情報を
表示するための仕組みです。
2010年にFacebookが開発し、現在は多くのWebサイトで採用されています。

OGPでは、HTMLのhead内にmeta要素を配置し、「og:」というプレフィックスを持つプ
ロパティを使用して、ページの様々な情報を定義します。
主な要素としては、ページのタイトル、ページの説明、サムネイル画像のURL、
正規URLなどがあります。

これらの情報を適切に設定することで、FacebookやTwitter、LINEなどのSNSでリンクがシェアされた際に、
単なるURLではなく、タイトル、説明文、画像を含む魅力的なプレビューカードが表示されます。

## このブログの対応

記事ページのメタ情報を管理している`lib/metadata.ts`を修正してOGPに対応するヘッダを
追加するロジックを入れました。

```javascript
export function generateArticleMetadata(
  article: Article & { path?: string },
): Metadata {
  // pathがある場合はURLを生成
  const url = article.path
    ? generateArticleUrl(article.date, article.path)
    : undefined;
  // OGP画像のURL
  const ogImageUrl = generateOgImageUrl();

  return {
    title: article.title,
    description: article.description,
    authors: [{ name: article.author || siteConfig.author }],
    // OGP設定
    openGraph: {
      siteName: siteConfig.sitename,
      title: article.title,
      description: article.description,
      type: "article",
      ...(url && { url }),
      images: [
        {
          url: ogImageUrl,
          width: 1200,
          height: 630,
          alt: siteConfig.sitename,
        },
      ],
    },
    // 他にも必要なメタデータがあれば追加可能
  };
}
```

Next.jsがOGPのヘッダを生成する`openGraph`関数を提供しているので呼び出してい
るだけです。記事自体のフルパスが必要ですが、面倒なので記事内でパスを渡すよう
にしました。

また、MDXファイル内の`Image`で参照している画像のフルパスはこの処理では得られ
ないので、仕方なく固定の画像を指定しています。

## まとめ

自身はたまにBlueskeyにリンクを投稿するくらいなので、それほど必要性は高くあり
ませんが、実装自体は簡単なので対応しているの越したことはありませんね。
