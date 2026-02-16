+++
title = "S3静的ウェブサイトのインデックス解決をCloudFront Functionsで修正"
description = "CloudFlareからブログを移行した際に、パスの指定で問題がでていたので修正しました。"
date = 2024-11-05
aliases = ["/articles/2024/11/05/Fixing-s3-cloudfront-index-resolution"]

[taxonomies]
tags = ["Tech", "AWS","Weblog"]
[extra]
social_media_card = "ogp.webp"
+++

メインブログをCloudflareからAWS S3へと移行した際、
S3のBlock pubic accessをオフ、Static website hostingをオンにしていたので、
CloudFrontがS3のREST APIエンドポイントを使用するよう修正しました。

この場合CloudFrontはサブディレクトリのindex.htmlファイルを自動的に解決できないので、以下のURLのパスを適切に変換するCloudFront Functionsを追加しました。

ありがちな事ですね。

```javascript
function handler(event) {
  var request = event.request;
  var uri = request.uri;

  // URIが/で終わる場合、index.htmlを追加
  if (uri.endsWith("/")) {
    request.uri += "index.html";
  }
  // 拡張子がない場合もindex.htmlを追加
  else if (!uri.includes(".")) {
    request.uri += "/index.html";
  }

  return request;
}
```
