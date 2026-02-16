+++
title = "OpenAI o1-preview"
description = "OpenAIのo1-previewを現在評価しています。"
date = 2024-09-17
aliases = ["/articles/2024/09/17/o1-preview"]

[taxonomies]
tags = ["Tech", "Generative AI"]
[extra]
social_media_card = "ogp.webp"
+++

Currently evaluating OpenAI's o1-preview. Although it is said that it is not
always more accurate than GPT-4o, when checked with the "[World Model](https:
//github.com/SingularitySociety/WorldModels/)". It collects problems that
LLMs struggle with, o1-preview correctly solves questions like the following
that GPT-4o gets wrong.

- Q1. What happens if you push a door labeled "Pull" from the opposite side?
- Q2. A cotton candy is 8 centimeters tall, and a brick is 7 centimeters tall. If you place the brick on top of the cotton candy, what is the total height?
- Q3. I left a wallet on a park bench near Shibuya Station for three hours. On that day, the temperature exceeded 39 degrees Celsius, and the wallet was exposed to direct sunlight. What happens to the wallet?
- Q4. Do man-eating tigers live in unexplored jungles?

---

OpenAIのo1-previewを現在評価しています。GPT-4oより常に精度が高いわけではないと言われていますが、LLMが苦手な問題を集めた「[World Model](https://github.com/SingularitySociety/WorldModels/)」で確認すると、GPT-4oで不正解となる次のような問題をo1-previewでは正確に解いてしまいます。

- Q1.「引く」と書かれたドアを反対側から押すとどうるか？
- Q2. 綿菓子の高さは8センチ、レンガの高さは7センチである。綿菓子の上にレ
  ンガを置くと、全体の高さは何センチになるか？
- Q3. 渋谷駅近くの公園のベンチに財布を3時間置き忘れた。
  その日は気温が39度を超え、財布は直射日光にさらされていた。
  財布はどうなるか？
- Q4. 前人未到のジャングルに人喰い虎は生息しているか？
