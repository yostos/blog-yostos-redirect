# blog-yostos-redirect

`blog.yostos.org` から `codedchords.dev` への meta refresh リダイレクト専用サイト。

ドメイン移行に伴い、旧ドメインの全ページを新ドメインの対応ページへリダイレクトする。
GitHub Pages で `blog.yostos.org` として配信する。

## 仕組み

1. Zola で旧ブログと同じ URL 構造の HTML を生成
2. `build_redirects.py` が全 HTML を meta refresh リダイレクトページに差し替え
   - 通常ページ: パスをそのまま `codedchords.dev` にマッピング
   - alias ページ: Zola が生成したリダイレクト先（正規パス）を読み取り、`codedchords.dev` の正規パスに直接リダイレクト
3. 画像・CSS・JS 等の不要ファイルを削除し、CNAME を配置

## デプロイ

`main` ブランチへの push で GitHub Actions が自動デプロイする。

手動で生成する場合:

```bash
python3 build_redirects.py
```

## 新記事追加時

`blog-yostos` リポジトリで記事を追加した後、このリポジトリの `content/` を同期してスクリプトを再実行（または push して CI に任せる）。
