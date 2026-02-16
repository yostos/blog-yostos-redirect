+++
title = "こだわりのNostr Pubkeyを手に入れる"
description = "Nostrで自分の好きなPubkeyを入手するためにがんばってみました。"
date = 2024-08-25
aliases = ["/articles/2024/08/25/Pubkey-of-nostr"]

[taxonomies]
tags = ["Tech"]
[extra]
social_media_card = "ogp.webp"
+++

NostrでVanity pubkeyのMiningをやってみました。
プリフィックスに`yostos`と近い`y0st0s`を得るため、`rana`を使って数時間Miningしました。

得られた、Pubkeyが`npub1y0st0svvu5xg6dvswx7dz5m2p7004kmvsx6n22w4yjp3l6fa3mvsef2zz7`で、npub1に続く部分が`y0st0s`となっています。自己満足ですが。

ranaのインストールと使い方は次の通りです。Rustの実行環境が事前に必要です。

```bash
cargo install rana
rana --vanity-n-prefix y0st0s
Started mining process for vanity bech32 prefix[es]: 'npub1["y0st0s"]' (estimated pow: 24)
Benchmarking of cores disabled for vanity npub key upon proper calculation.
Mining using 14 cores...
<<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>
Vanity npub found: y0st0s
Found matching Nostr public key:
Hex public key: 23e0b7c18ce50c8d359071bcd1536a0f9efadb6c81b53529d524831fe93d8ed9
Hex private key: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Npub public key: npub1y0st0svvu5xg6dvswx7dz5m2p7004kmvsx6n22w4yjp3l6fa3mvsef2zz7
Nsec private key: nsec1@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
2597711770 iterations (about 2x10^9 hashes) in 3433 seconds. Avg rate 756688 hashes/second

```

プリフィックスに指定する桁数が増えるほどマイニングに時間がかかるので注意しましょう。上記の例ではM3 MAXのMacbook Proで1時間ほどかかりました。

また、PubkeyはNative SegWit(Bech32)でエンコードされており、小文字でl,b,i,oを除いた32文字しか使えません。これらの文字については数字などに置き換えて指定する必要があります（yostos->y0st0sなど）
