+++
title = "元AWS社員が読むClaude Code社内禁止騒動"
description = """
AmazonがClaude Codeの社内利用を制限し
Kiroの使用を推進する中、
約1,500人のエンジニアが反発しています。
2024年夏にAWSを退職した元社員の視点から、
開発ツール戦略の歴史と
Amazon-Anthropicの三重構造が
生み出す矛盾を考察します。
"""
date = 2026-02-15T17:00:00+09:00
[taxonomies]
tags = ["AWS", "Generative AI", "Claude Code",
  "Current Affairs"]
[extra]
social_media_card = "ogp.webp"
+++

<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>

## Amazon社内でClaude Code利用禁止に？

Business Insider 2月11日記事に、
Amazon社内のClaude Code
使用制限が行われているとの記事を見つけました。

<!-- textlint-disable -->

{{ linkcard(url="https://www.businessinsider.com/amazon-engineers-grate-against-internal-limits-claude-code-kiro-ai-2026-2") }}

<!-- textlint-enable -->

Amazonが社内でClaude Codeの
プロダクションコードへの使用を制限し、
社内製AIコーディングツールKiroの利用を
推進しているというものです。
これに対して、社内フォーラムでは
約1,500人のエンジニアが
Claude Codeの正式採用を支持しています。

私は2024年夏にAWSを退職しましたが、
この記事を読んで、当時の社内の空気と
重ね合わせずにはいられませんでした。

## 売るものを自分で使えない皮肉

社内での開発に自社開発ツールの使用を
推奨するのは当然のように思いますが、
この問題で最も深刻なのは、
AWSはClaude Codeも売っているという事実です。

AWSは[Amazon Bedrock](https://aws.amazon.com/bedrock/)を通じてClaude Codeを
顧客に販売しています。
現在KiroよりもClaude Codeの方が
市場での注目度は高いので、
Solution ArchitectやProfessional Servicesは
Claude Codeの解説や導入支援を求められます。

そのため、日常の開発ツールとして
利用するのは自然な流れですが、
彼らは社内でClaude Codeをプロダクションコードに
使う正式な承認を得られていません。

Business Insider記事中のある従業員は
「自分たちが社内利用を承認していない
ツールを、なぜ顧客が信頼して
使ってくれるのか」と指摘しています。
これはもっともな疑問です。

Amazon Bedrockは当時から
社内で推進されていました。
ファインチューニングや
ガードレールなど独自の付加価値を持つ
プラットフォームですが、
多くの顧客がAmazon Bedrockに来る理由は
Claudeを使いたいからです。
ところがAmazon Bedrockという
プラットフォームを挟むことで、
社内では「自社が競合製品を販売している」
という意識が薄れているように感じます。
Claude Codeの社内利用を制限しながら
顧客にはそれを売るという矛盾が
放置されているのは、
この認識の甘さが一因ではないでしょうか。

## 投資家・パートナー・競合の三重構造

この問題の根底にあるのは、
AmazonとAnthropicの関係そのものの
複雑さです。
Amazonは累計80億ドル超を出資した
Anthropicの最大の投資家であり、
その持分の評価額は
600億ドル超に達しています。
AnthropicにとってAWSは
最大のクラウドパートナーです。
AnthropicはAWSのクラウドサービスと
少なくとも100万個のTrainiumチップの
利用をコミットしています。
しかし同時に、AmazonはKiroや
Q DeveloperでAnthropicの製品と
直接競合しています。

「投資家・パートナー・競合」という
三重構造が社内ポリシーの歪みとして
表面化しているのが、
今回の記事の本質だと考えています。
Amazonとしては自社製品を推進したい。
しかし出資先の製品を社内で制限している
ことが表沙汰になれば、
パートナーシップへの影響も避けられません。

Amazonの広報は「明示的な禁止ではなく、
プロダクションコード用のツールに対して
厳格な要件を適用している」と
コメントしています。
しかし社内で1,500人もの
エンジニアがClaude Codeの
正式採用を求めている状況を見ると、
現場はこの説明に
納得していないことが明らかです。

さらに気になるのは透明性の問題です。
一度はClaude Codeがセキュリティおよび
法務レビューを通過したという
社内ガイドラインが存在したにもかかわらず、
その記述が後から編集・削除されたと
記事は指摘しています。
判断の根拠を示さずに方針を変えれば、
不信感が深まるのは当然です。

開発者の生産性に直結する
ツールの選択を政治的な理由で制限することは、
短期的には自社製品の利用数に
つながるかもしれません。
しかし長期的にはエンジニアの信頼を損ない、
優秀な人材が流出する原因になりかねません。
Amazonの広報は
「Kiroのエンジニアの70%が1月に
少なくとも一度は利用した」と言っていますが、
「少なくとも一度」という表現が
すべてを物語っています。
AWSの開発ツール戦略がこの矛盾を
どう解消していくのか、
元社員として注目しています。

## 社内で見た開発ツール戦略の軌跡

私の退職した2024年当時は、AWS CodeCommitとCloud9の
整理が進行中でした。
社内ではCodeWhisperer
（後にAmazon Q Developerへ統合）が
強く推奨されていました。

AWSの開発ツールはサービスの新設と廃止を
繰り返してきた歴史があり、
「次もまた消えるのでは」という不安は
エンジニアの間で常につきまとっていました。
当時、顧客への説明で困ったものです。
私自身も開発ツール戦略に関しては
懐疑的でした。

Kiroは[re:Inventでのインタビュー](https://www.sixfivemedia.com/content/from-prompt-to-production-ai-spec-driven-development-with-kiro---six-five-on-the-road)によると、
チーム発足時にPR FAQ
（Amazonのプロダクト企画文書）を書いて
2024年末から具体化し、
2025年7月にパブリックプレビューとなっています。
私の退職後に本格化したため、
直接触れていません。
VS Codeのフォークと聞いていますが、
仮に在籍中に推奨されていたとしても
使わなかった可能性が高いです。

Kiroが掲げる「spec-driven development」
というコンセプト自体は理解できます。
私自身、Claude Codeで仕様ファイルを
ベースにした開発を日常的にやっています。
ただし、Claude Codeの自由度と比べると、
AIをツールに組み込む方式には
根本的な限界があります。
Claude Codeはターミナルから
あらゆる操作ができるエージェントであり、
開発者のワークフロー全体に介入できます。
一方、KiroのようにIDEにAIを組み込む方式は、
そのIDEが想定した枠組みの中でしか
能力を発揮できません。
この差は使い込むほど大きくなります。
社内で反発が出るのは当然のことです。

同記事中で、あるAmazonのエンジニアは
こう書いています。

> A tool that can't keep pace with rivals
> offers no real innovation.
> And without competitive strength,
> Kiro's only survival mechanism becomes
> forced adoption rather than genuine value.
> （競合についていけないツールから
> 本当のイノベーションは生まれない。
> 競争力がなければ、Kiroの唯一の生存戦略は
> 真の価値ではなく強制採用になる）

CodeCommitやCloud9がたどった道を
見てきた身としては、
この指摘はまさに的を射ています。
