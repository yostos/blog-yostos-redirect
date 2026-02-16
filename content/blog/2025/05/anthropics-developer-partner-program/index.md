+++
title = "Claude Codeのディスカウントを得る - Developer Partner Program"
description = "Claude Code APIの利用料割引が可能となるDeveloper Partner ProgrameがAnthropicより発表されました。今後のモデル改善のためのプログラムで参加するとClaude 3.5 Sonnet および Claude 3.7Sonnet モデルの Claude Code 入力トークンが30%割引になる可能性があります。"
date = 2025-05-02
aliases = ["/articles/2025/05/02/anthropics-developer-partner-program"]

[taxonomies]
tags = ["Tech", "Generative AI"]
[extra]
social_media_card = "ogp.webp"
+++

Claude Code APIの利用料割引が可能となるDeveloper Partner ProgrameがAnthropicより発表されました。今後のモデル改善のためのプログラムで参加するとClaude 3.5 SonnetおよびClaude 3.7SonnetモデルのClaude Code入力トークンが30%割引になる可能性があります。

## Anthropic's Developer Partner Programのポイント

AnthropicのClaudeは基本的にユーザーの入力をトレーニングに使用しませんが、
この [Anthropic's Developer Partner Program](https://support.anthropic.com/en/articles/11174108-about-the-development-partner-program) では、Anthropicのサービスやモデルトレーニングを改善
するために、Claude Codeセッションを自主的にAnthropicと共有することになります。

その代わりに、Claude 3.5 SonnetとClaude 3.7 SonnetのClaude Code入力トークンに対して、
標準API価格から30%オフを受けることができます。具体的には次の通りです。

- 標準入力: 100万トークンあたり-$0.9
- キャッシュ書き込み: 100万トークンあたり-$1.125
- キャッシュ読み取り: 100万トークンあたり-$0.09

利用するに当たっては、次のような注意点があります。

- AnthropicのファーストパーティAPIからのClaude Codeの入出力トークンのみが共
  有され、ClaudeアプリやClaude Code以外のAPI呼び出しには適用されない。
  つまり、Amazon Bedrockなどを経由するとプログラムは適用されず割引の対象外である
- データは最大2年間安全に保存される。モデルトレーニングに使用されるデータは
  他の顧客情報と関連付けらない
- この設定は組織内のすべてのメンバーに適用される
- プログラムに登録した場合、組織内のすべてのメンバーに通知される
- いつでもプログラムから離脱可能だが、以前に共有されたデータは削除不可
- 割引は請求後2025年7月31日まで適用され、プログラムを離脱すると終了する

## プログラムへの参加方法

AnthropicのConsoleの設定(Claudeの設定画面でないことに注意)から、
「Privacy Controls」を開いて「Join our Development Partner Program to help improve Claude」
で「Join」ボタンを押すだけです。

離脱時は、「Leave」ボタンが現れるので、押すとプログラムを離脱できます。

ただし、すべてのアカウントがこのプログラムの対象ではないようです。
アカウントが対象でない場合は、上記の参加オプションが表示されません。

## まとめ

どれくらいの人がClaude Codeを使っているわかりませんが、GitHub Copilotのよう
「コード入力支援」を超えClaude Codeは優れた開発者とペアプログラミングしているような
錯覚に陥るほど生産性が上がります。

このため、Claude Codeの利用料が30%の割引となるのは魅力的です。
参加をためらうとしたら、「自身のコンテンツが学習に利用される」という
プライバシーの点でしょう。業務で利用している場合は、成果物が他社に共有される
ことになるためハードルが高そうです。

私自身は個人の活動で利用なので、プライバシーの観点での懸念はありません。
自身のClaude Codeセッションを共有することでClaudeのコーディング能力向上に
寄与し、AIによるコーディング支援技術の発展できることはモチベーションにも繋が
ります。
更に割引まで恩恵を受けることができるならば参加しない理由はないため、即座に参加しました。
