+++
title = "Software Development Using Generative AI"
description = "Recently, I had a conversation with someone about software development using ChatGPT, and a few things caught my attention. I decided to summarize my thoughts here."
date = 2024-08-09
aliases = ["/articles/2024/08/09/Software-Development-Using-AI"]

[taxonomies]
tags = ["Tech", "Generative AI","Software Engineering"]
[extra]
social_media_card = "ogp.webp"
+++

日本語は下の方に。

## Dramatic Cost Reduction

The use of generative AI has dramatically reduced the costs of producing images and music.
For example, tasks like illustration creation and music creation (using services like Udio and Suno) previously required specialists.
These tasks can now be done by individuals in about five minutes using generative AI-powered services.

In software development, the use of generative AI for development support is also spreading.
Many developers are likely using tools like Github Copilot.

However, applications of generative AI in software development are progressing beyond mere coding support.
For example, I recently changed the static site generator for my main blog, which required converting the metadata of several hundred articles.
I wrote a conversion program in Python.
But by providing ChatGPT with the prerequisites and requirements, I only needed to make about 10% modifications to the generated code.

This example shows that generative AI can shoulder not only development support but also the creation of software itself.
It is similar to image and music production.
In the example above, what would have taken about two weeks if outsourced to a development vendor was reduced significantly.
This reduction brought the work down to about 30 minutes using generative AI.

The cost is only 0.6%.

## What Generative AI Software Development Brings

The rationale for traditional software development was that it could reduce the
workload of many people through repeated use. Therefore, single-use software
development for specific users was not permitted.

However, there is a world where single-use software development has been
allowed: the realm of data science. This is because of the unique nature of
datasets and the need for trial and error, where speed is prioritized over
reuse. The most significant reason is that the benefits gained from single-use
software development outweigh the costs.

By leveraging generative AI, it becomes possible to reduce costs in general
software development similarly. This means that even single-use software
development for one user, which does not contribute to reducing the workload of
many, becomes feasible.

In other words, we are entering an era where problems that could be solved by software but were left unaddressed due to development costs.
These problems can now be resolved quickly using generative AI for software development.

In practice, when you ask ChatGPT a question like "What is the date 100 days after August 9, 2024?", a single-use Python code is generated.
This specialized code is executed behind the scenes to solve this specific problem.

```python
from datetime import datetime, timedelta

# Starting date
start_date = datetime(2024, 8, 8)

# Calculate the date 100 days later
end_date = start_date + timedelta(days=100)
end_date.strftime('%Y-%m-%d')
```

## Differences from RPA and No-Code

Similar technologies include RPA and no-code solutions. Many companies have
adopted these technologies, riding the wave of the DX trend.

Both have the effect of lowering software development costs, but there are
significant differences in their technology and implementation effects.

From a technical perspective, generative AI software development involves custom development by AI according to requirements.
RPA and no-code solutions appear to meet user requests, but in reality, only pour parameters into pre-made software provided by vendors.
Therefore, what can be achieved must be based on the templates of the pre-made software.

More importantly than these technical differences is the impact of their implementation.
In many cases with RPA and no-code solutions, user departments develop the software themselves.
This happens when they become frustrated with waiting for the development department.

This means that non-developers are creating reusable software, or corporate software assets, which is a nightmare.
Years later, the software will likely become a maintenance burden due to the users' transfer or the vendors' product lifecycle.

In contrast, single-use software development using generative AI emphasizes the outcomes rather than the software itself.
Thus, the specifics of the software do not matter.
Even so, a verifiable artifact in the form of "source code" is created, making it a completely transparent process (white box).

## Conclusion

Seeing companies that claim to have achieved "DX" by introducing RPA and no-code solutions gives me chills.
In contrast, companies should recognize the new application methods of software development.
These methods allow generative AI to be used to solve problems on the spot, similar to the approach taken by data scientists.
This approach is similar to the methods employed by data scientists.

In such a world, engineers with the ability to read source code will become
increasingly necessary. Companies currently investing in RPA and no-code
solutions should be cautious, as they may be going against the trend.

---

## 劇的なコスト削減

生成系AIの活用により、画像や音楽の制作コストが劇的に削減されています。例えば、
これまで専門家に依頼しなければならなかったイラスト作成（MidjourneyやDALL-E 2な
ど）や音楽作成（UdioやSunoなど）を、生成系AIを取り入れたサービスを使うことで、
自分で5分ほどで望みの画像や音楽を制作できます。

ソフトウェア開発においても、生成系AIを活用した開発支援が広がってきています。実
際に、Github Copilotのようなツールを使用している開発者も多いでしょう。

しかし、これらのコーディング支援とは別の次元で、ソフトウェア開発への応用も進ん
でいます。例えば、最近私はメインブログの静的サイトジェネレータを変更しました
が、それに伴い記事のメタデータの変換が必要でした。数百ある記事の変換プログラム
をPythonで書きましたが、ChatGPTに前提と要件を伝えて生成されたコードをベースに、
10%程度の修正するだけで済みました。

これは、開発作業の支援だけでなく、画像や音楽の制作と同様にソフトウェア制作その
ものを生成系AIに肩代わりさせることができる例です。上記の例では、開発ベンダーに
依頼すると2週間ほどの時間がかかるところを、生成系AIを使って自分でコードを作成す
れば30分程度で済みます。

コストは0.6%で済んでしまいます。

## 生成系AIによるソフトウェア開発がもたらすもの

従来のソフトウェア開発のRationale（根拠）は、何度も使用されることで多くの人の作
業を軽減できることにありました。そのため、特定のユーザーのための使い切りのソフ
トウェア開発は許されませんでした。

しかし、使い切りのソフトウェア開発が許されてきた世界があります。それはデータサ
イエンスの領域です。これは、データセットの特異性やそれに伴う試行錯誤の必要性、
再利用より迅速性が重視されたためです。最も大きな理由は、使い切りのソフトウェア
開発のコストに対して得られる成果が大きいからです。

生成系AIを活用すれば、一般的なソフトウェア開発でも同様にコスト削減が可能とな
り、多くの人の作業軽減に貢献しない、一人のユーザーのためだけの使い切りのソフト
ウェアを開発することも可能になります。

つまり、これまで開発コストを理由にソフトウェアで解決出来る問題が放置されていた
状況を「生成系AI使って、ささっとソフトウェア開発をして解決すればよい」という時
代になってきていると感じます。

実際、ChatGPTで「2024年8月9日の100日後は何日？」というような質問の回答を作るの
に、裏では以下のようはこの問題に特化した使い切りのPythonコードが生成されて実行
されています。

```python
from datetime import datetime, timedelta

# Starting date
start_date = datetime(2024, 8, 8)

# Calculate the date 100 days later
end_date = start_date + timedelta(days=100)
end_date.strftime('%Y-%m-%d')
```

## RPAやノーコードとの違い

似たような技術にはRPAやノーコードがあります。DXの流行に乗って、これらを導入した
企業も多いと思います。

どちらもソフトウェア開発コストを下げるという効果がありますが、その技術と導入効
果の面で大きな違いがあります。

技術面で見ると、生成系AIによるソフトウェア開発では要件に従いAIよるソフトウェア
のカスタム開発が行われています。しかし、RPAやノーコードではユーザーのリクエストに沿っ
て必要なソフトウェアを実現しているように見えますが、実際にはベンダーが用意した
ソフトウェアにパラメータを流し込んでいるだけです。そのため、実現できることもあ
らかじめ用意されたソフトウェアのひな形を意識した要件に落とし込む必要があります。

こういった技術的な違いよりも、問題はその導入効果です。
RPAやノーコードで多く行われているのは、開発要望が開発部門のバックログ
いつまでも実現されないと
業を煮やしたユーザー部門が自身で開発するというパターンです。これは使い回すソフト
ウェア、つまり企業のソフトウェア資産を開発者でない素人が開発してしまうことを意
味します。悪夢でしかありません。数年後には開発したユーザーの異動やベンダーの製
品ライフサイクルから、メンテナンスできないソフトウェアという負の遺産になってい
ることでしょう[^1]。

一方で生成系AIによる使い切りソフトウェア開発は生成したソフトウェアそのもので
はなく成果が重視されるため、どのようなソフトウェアだったかは問題になりま
せん。それでも、「ソースコード」という検証可能な成果物が作成されるため、完全に
透明な状態（ホワイトボックス）です。

[^1]:
    「サーバー型RPAならば集中管理できてそうはならない」という意見もあり
    ます。それならばIT部門が開発して管理すればよくベンダー依存のランタイム
    上でシステムを構築する意味がないのではないでしょうか？　もっともここに
    AIを応用すると世界が変わる可能性はありますが、現時点ではまだ予測不能で
    す。

## まとめ

RPAやノーコードのソリューションを導入して「DX実現」としている企業の将来を思うと
暗い未来しか想像できません。

一方で従来のソフトウェア開発とは異なる、これまでデータサイエンティストが取り組
んできたようなアプローチ、つまるソフトウェア開発によるその場の問題解決が生成系
AIを使うと可能になるので、新しいソフトウェアの応用方法として企業はしっかりと認
知すべきだと思います。

こういった世界ではソースコードを読む能力を持ったエンジニアはますます必要になっ
てくるので、そういった意味でもRPAやノーコードに取り組んでいる企業は逆流している
ので気をつけたほうがよいと思います。
