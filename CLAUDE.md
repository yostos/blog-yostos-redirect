# blog-yostos-redirect

`blog.yostos.org` から `codedchords.dev` への
リダイレクト専用サイト。

## 背景

ブログを `blog.yostos.org` → `codedchords.dev` に
ドメイン移行する。`yostos.org` の DNS は Fastmail で
管理しており Cloudflare への移行は行わないため、
Cloudflare Redirect Rules は使えない。

代わりに、全ページの meta refresh リダイレクトを
生成して GitHub Pages で `blog.yostos.org` として
配信する。

詳細な移行計画:
`../blog-yostos/docs/domain-migration.md` の Phase 4

## 現在の状態

- blog-yostos リポジトリから Zola ソースをコピー済み
- `config.toml` の `base_url` は
  `https://blog.yostos.org`（旧ドメイン）に設定済み
- `themes/tabi` は submodule として追加済み
- `zola build` で 247ページ + 25セクションの
  生成を確認済み

## やるべきこと

### 1. リダイレクト差し替えスクリプトの作成

`zola build` で生成される `public/` 内の全 HTML を
meta refresh リダイレクトページに差し替える
スクリプトを作成する。

処理の流れ:

1. `zola build` を実行
2. `public/` 内の全 `.html` ファイルを走査
3. 各ファイルについて:
   - **通常ページ**: パス（`public/` からの相対）を
     そのまま新ドメインの URL にマッピング
   - **alias ページ**: Zola が生成した alias ページは
     meta refresh で正規パスへのリダイレクトを含む。
     このリダイレクト先を読み取り、新ドメインの
     正規パスに直接リダイレクトする。
     例: `/articles/2024/09/06/Weekly-buzz-20240906`
     → `codedchords.dev/blog/2024/09/Weekly-buzz-20240906/`
     **重要**: 新サイトから aliases は削除されるため、
     alias パスをそのまま新ドメインに向けると 404 になる
4. HTML を以下の内容に差し替え:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="canonical"
    href="https://codedchords.dev/{path}">
  <meta http-equiv="refresh"
    content="0; url=https://codedchords.dev/{path}">
</head>
<body></body>
</html>
```

`{path}` は `public/` からの相対パスで、
`public/blog/2024/09/foo/index.html` なら
`blog/2024/09/foo/` となる。
ルートの `index.html` は空文字列（トップページ）。

### 2. 不要ファイルの削除

リダイレクトサイトには HTML だけあればよい。
`public/` 内の画像、CSS、JS、フォント、
sitemap.xml、atom.xml 等は削除してよい。

### 3. CNAME の配置

`static/CNAME` に `blog.yostos.org` を記載する
（現在は codedchords.dev になっている可能性あり）。
もしくはスクリプト内で `public/CNAME` を生成する。

### 4. GitHub リポジトリの作成とデプロイ

```bash
gh repo create blog-yostos-redirect --public \
  --description "Redirect blog.yostos.org → codedchords.dev"
git add . && git commit -m "Initial commit"
git remote add origin \
  https://github.com/yostos/blog-yostos-redirect.git
git push -u origin main
```

GitHub Pages を有効化し、カスタムドメインに
`blog.yostos.org` を設定する。

### 5. 動作確認

- `blog.yostos.org/` →
  `codedchords.dev/` にリダイレクトされること
- `blog.yostos.org/blog/2024/09/Weekly-buzz-20240906/` →
  対応する新ドメインページにリダイレクトされること
- 旧 Next.js パス
  `blog.yostos.org/articles/2024/09/06/Weekly-buzz-20240906`
  → aliases 経由でリダイレクトされること

## 注意事項

- スクリプト言語は問わない（bash, python 等）
- 本リポジトリの `content/` は参照用コピーであり、
  記事の編集は `blog-yostos` リポジトリで行うこと
- 新記事追加時はスクリプトを再実行して
  リダイレクトページを再生成する
