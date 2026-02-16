+++
title = "AWS CodeCommit新規受付凍結の影響について"
description = "Business Insider などを読んでいるとAWSのCodeCommitやCloud9の新規受付凍結は、米国でもかなり問題になっている模様。"
date = 2024-08-13
aliases = ["/articles/2024/08/13/CodeCommit-Impact"]

[taxonomies]
tags = ["Tech", "AWS", "Cloud"]
[extra]
social_media_card = "ogp.webp"
+++

<blockquote>
  Amazon's recent decision to stop accepting new users for several cloud
  services caught some customers, partners and even a few employees by surprise.
  (Amazon
  が展開中の複数のクラウドサービスについて新規ユーザー登録受付を中止したことで、顧客や協力企業の間で混乱が広がっている。)
  <footer>
    <cite>
      Business Insider -{" "}
      <a href="https://www.businessinsider.com/aws-deprioritized-cloud-services-surprising-customers-salespeople-2024-8">
        Amazon decision to deprioritize 7 cloud services caught customers and
        even some salespeople by surprise
      </a>
    </cite>
  </footer>
</blockquote>

以下の記事は、最近の報道などを見た個人的な意見です。既に中の人ではないので、この件に関しては報道以上の情報は持ち合わせていません。

## サービス凍結の状況

同記事によると、次のように説明されている模様です。

> As the public outcry grew, AWS's chief evangelist Jeff Barr wrote a short X post on Tuesday to explain that the company decided to "discontinue new access to a small number of services," but it would continue running them in a secure environment.
>
> 関係者から懸念の声が高まったことを受け、AWSのバイスプレジデント兼チーフエバンジェリストを務めるジェフ・バー氏は7月30日のX（旧Twitter）投稿を通じて詳細な事実を説明するとともに、今後の対応を明らかにした。

これまで使ってきたユーザーはそのまま使用でき、新規ユーザーはGitHubなど別のソリューションを選択すればよいのですぐに何か問題となる訳でありません。

## 新規受付凍結の影響

この変更により直近大きな影響はなさそうですが、顧客としては不安でしょう。

既存ユーザーに対してはサポートを継続すると言われていますが、ほとんどの顧客は遠からずこれらのサービスが終了すると考えているでしょう。つまり、顧客は将来のサービス終了に備えた対応を迫られています。

[AWSのブログ](https://aws.amazon.com/jp/blogs/devops/how-to-migrate-your-aws-codecommit-repository-to-another-git-provider/)でリポジトリーの移行方法が紹介されていますが、CodeCommitやCloud9などのツールは開発プロセスの中に組み込まれて使用しているので、最低でも次のような対応が必要です。

- リポジトリーの移行
- ユーザーの移行
- CI/CDの組み直し
- 開発プロセスの対応変更
- 社内の移管手続きの変更
- 開発者や運用者の再教育

ちょっとした組織横断のプロジェクトになりそうです。

## 何が悪かったのか？

第一の問題は、AWSがCodeCommitやCloud9のサービスの重要性をAWSが図り損ねたことでしょう。

想像するに、CodeCommitやCloud9はそれほど利用者が多くなかったのでしょう。
ユーザーの利用度が低い、サービス提供側から見ると金を生まないサービスを統廃合していくのは当たり前の話です。

これが本番環境のRuntimeだけに関わる問題であれば、ここまでの問題にならなかったかもしれません。
ところが、CodeCommitやCloud9などは企業ITの組織やプロセスに深く関わるので、サービスの移行だけでなく人やプロセスの移行も必要です。
少数かもしれませんが、AWSを信じてCodeCommitやCloud9を利用していた企業は多大な移行コストが必要となります。

その認識がAWSには足りてなかったのではないかと思います。
アプリ開発の側の人だったので偏見かもしれませんが、どうもインフラ屋さんというのはこういう部分のセンスが足りていないのではないかと思うことがよくあります。

結果として、Business Insiderが報じるよう、AWS自身も以下のようは羽目になってしまっています。

> The company is trying to keep supporting clients while signaling that these offerings are no longer a strategic priority.
>
> 同社は、これらのサービスがもはや戦略的優先事項ではないことを示しながら、顧客のサポートを続けようとしている。

2点目は、これらの決定に至るAWS社内での連携の問題でしょう。

AWS CLIの[CHANGE LOG](https://github.com/aws/aws-cli/blob/v2/CHANGELOG.rst)を見ると、7月26日にCommitされた2.17.18のコメントに以下のように記述されています。これを受けて一部の顧客が気付いて徐々に騒ぎが大きくなっていったようです。

```
api-change:`codecommit`: CreateRepository API now throws OperationNotAllowedException when the account has been restricted from creating a repository.
```

実際には6月6日から新規顧客への制限を加えていたという話もあります。当然これらの決定は更に数ヶ月前には行われていたことでしょう。一方でBusiness Insiderが報じるようにAWS内部でも十分に周知されないまま決定されたようです。

> It turns out that even some of Amazon's own salespeople were not aware of the change until after it was made public late last week.
>
> なお、アマゾンの営業部門の中には事前に何も聞かされておらず、同社が先週末に受付中止を公表した時点で初めてその事実を知った従業員が複数いることも分かった。

アグレッシブな機能の改善は美点でもあり機能やサービスをどんどん追加している時はよかったかもしれませんが、ある程度利用が定着した段階に入っているこれからはこれまでのようなカジュアルな変更は難しいのかもしれません。
