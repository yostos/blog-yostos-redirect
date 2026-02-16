+++
title = "国税庁の法人番号システムWeb-APIの検証"
description = "I had a requirement at work to uniquely identify companies, and to utilize the corporate number system, I created code to verify the Web API of the Corporate Number System provided by the National Tax Agency."
date = 2025-04-18
aliases = ["/articles/2025/04/18/company-info-api"]

[taxonomies]
tags = ["Tech","API"]
[extra]
social_media_card = "ogp.webp"
+++

仕事で企業を一意に特定するという要件があり、法人番号制度を利用するために
国税庁が提供する法人番号システムのWeb API
の検証のためのコードを作成してみました。

## 法人番号制度とは

法人番号制度は、2015年10月5日に発足しました。
この制度は、行政の効率化、国民の利便性の向上、および公平・公正な社会の実現を
目的として導入されました。法人には13桁の番号が指定され、商号や所在地といった
基本情報とともに国税庁の法人番号公表サイトで公開されています。

特に近年では、2023年10月から開始されたインボイス制度（適格請求書等保存方式）
との関連で、登録番号（T+法人番号等）を記載した適格請求書の発行が消費税の
仕入税額控除の要件となっているためシステムで扱うことも多くなっています。

## 国税庁のWeb APIについて

国税庁が提供するAPIについては、[法人番号システムのWep API](https://www.houjin-bangou.nta.go.jp/webapi/index.html)
のページに利用方法や申し込み方法がガイドされています。

利用には国税庁が振り出す「アプリケーションID」を取得する必要があります。
次の２つのアプリケーションIDがあります。

- インボイスWeb-APIを利用できるアプリケーションID
- 法人番号システムWeb-APIのみ利用できるアプリケーションID

前者は国税庁の承認を受ける必要がありますが、後者の法人番号システムのAPIにつ
いては申請だけでアプリケーションIDを振り出してくれます。ただし、申請してから
２週間から1ヶ月程度かかります。

## 法人情報検索APIクライアント

Typescriptで検証のためのコードを書いてみました。

法人名、または法人番号で検索できます。

実行すると、次のような標準出力にレスポンスをそのまま表示します。
(以下の例では、適当に折り返しています)

[GitHubに公開](https://github.com/yostos/get-company-info)したので、ビルド方法や詳細な使い方はそちらをご覧ください。
検証用なのでエラー処理はいい加減です。

```bash

╰─❯ npm start --  --type name 任天堂株式会社
> company-info-api@1.0.0 start
> node dist/index.js --type name 任天堂株式会社

含まれている日本語： 任天堂株式会社
日本語を含むか： true

<?xml version="1.0" encoding="UTF-8"?><corporations><lastUpdateDate>
2025-04-18</lastUpdateDate><count>1</count><divideNumber>1</divideNumber><di
videSize>1</divideSize><corporation><sequenceNumber>1</sequenceNumber><corpo
rateNumber>1130001011420</corporateNumber><process>01</process><correct>1</c
orrect><updateDate>2018-07-18</updateDate><changeDate>2015-10-05</changeDat
e><name>任天堂株式会社</name><nameImageId/><kind>301</kind><prefectureName>
京都府</prefectureName><cityName>京都市南区</cityName><streetNumber>上鳥羽鉾
立町１１番地１
</streetNumber><addressImageId/><prefectureCode>26</prefectureCode><cityCod
e>107</cityCode><postCode>6018116</postCode><addressOutside/>
<addressOutsideImageId/><closeDate/><closeCause/><successorCorporateNumber/>
<changeCause/><assignmentDate>2015-10-05</assignmentDate><latest>1</latest>
<enName/><enPrefectureName/><enCityName/><enAddressOutside/><furigana>ニンテ
ンドウ</furigana><hihyoji>0</hihyoji></corporation></corporations>

╰─❯ npm start -- --format csv --type name 任天堂株式会社
> company-info-api@1.0.0 start
> node dist/index.js --format csv --type name 任天堂株式会社

含まれている日本語： 任天堂株式会社
日本語を含むか： true

2025-04-18,1,1,1
1,1130001011420,01,1,2018-07-18,2015-10-05,"任天堂株式会社",,301,"京都府","
京都市南区","上鳥羽鉾立町１１番地１",
,26,107,6018116,,,,,,,2015-10-05,1,,,,,"ニンテンドウ",0
```

## まとめ

一応国の仕組みで、一意に法人を特定できるのいろいろ活用できて便利そうです。

私が社会人になりたての頃に同じような要件があり、
当時はこういったものがありませんでした。
そのため、名寄せしたり帝国データバンクの企業情報とぶつけたり苦労しました。
国がこんなものを提供してくれるなんて、いい時代だ。

## 2025-04-20 追記

経済産業省も法人番号で検索できるAPIを公開していたので、対応しました。
