#!/usr/bin/env python3
"""
blog.yostos.org → codedchords.dev リダイレクトサイト生成スクリプト

1. zola build を実行
2. public/ 内の全 HTML を meta refresh リダイレクトに差し替え
3. 不要ファイル（画像, CSS, JS, フォント等）を削除
4. CNAME を配置
"""

import os
import re
import subprocess
import sys
from pathlib import Path

OLD_DOMAIN = "https://blog.yostos.org"
NEW_DOMAIN = "https://codedchords.dev"
CNAME_HOST = "blog.yostos.org"

# リダイレクト差し替えをスキップするファイル（Google Search Console 確認等）
PRESERVE_FILES = {
    "googlef2d3aeece0913e24.html",
}

SCRIPT_DIR = Path(__file__).parent
PUBLIC_DIR = SCRIPT_DIR / "public"

REDIRECT_TEMPLATE = """\
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="canonical" href="{url}">
  <meta http-equiv="refresh" content="0; url={url}">
</head>
<body></body>
</html>
"""

# Zola alias ページの meta refresh から URL を抽出する正規表現
# Zola の minified HTML: <meta content="0; url=..." http-equiv=refresh>
# content が http-equiv より前に来るため、content 側で抽出する
REFRESH_RE = re.compile(
    r'<meta\s[^>]*content=["\']?0;\s*url=([^"\'>\s]+)[^>]*http-equiv=["\']?refresh',
    re.IGNORECASE,
)


def run_zola_build():
    """zola build を実行"""
    print("Running zola build...")
    result = subprocess.run(
        ["zola", "build"],
        cwd=SCRIPT_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"zola build failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(result.stdout.rstrip())


def extract_refresh_url(html: str) -> str | None:
    """HTML から meta refresh の URL を抽出。なければ None"""
    m = REFRESH_RE.search(html)
    return m.group(1) if m else None


def path_for_file(html_path: Path) -> str:
    """通常ページ: ファイルパスからリダイレクト先パスを算出"""
    rel = html_path.relative_to(PUBLIC_DIR)
    if rel.name == "index.html":
        # blog/2025/03/foo/index.html → blog/2025/03/foo/
        parent = str(rel.parent)
        return "" if parent == "." else parent + "/"
    else:
        # 404.html → 404.html
        return str(rel)


def path_from_url(url: str) -> str:
    """alias ページ: リダイレクト先 URL からパスを算出"""
    # https://blog.yostos.org/blog/2025/03/foo/ → blog/2025/03/foo/
    if url.startswith(OLD_DOMAIN):
        path = url[len(OLD_DOMAIN):]
        return path.lstrip("/")
    return url.lstrip("/")


def replace_html_files():
    """public/ 内の全 HTML をリダイレクトページに差し替え"""
    html_files = list(PUBLIC_DIR.rglob("*.html"))
    alias_count = 0
    regular_count = 0

    for html_path in html_files:
        if html_path.name in PRESERVE_FILES:
            print(f"  Preserved: {html_path.relative_to(PUBLIC_DIR)}")
            continue

        html = html_path.read_text(encoding="utf-8", errors="replace")

        refresh_url = extract_refresh_url(html)
        if refresh_url:
            # alias ページ: リダイレクト先を新ドメインにマッピング
            path = path_from_url(refresh_url)
            alias_count += 1
        else:
            # 通常ページ: ファイルパスからパスを算出
            path = path_for_file(html_path)
            regular_count += 1

        new_url = f"{NEW_DOMAIN}/{path}"
        html_path.write_text(
            REDIRECT_TEMPLATE.format(url=new_url), encoding="utf-8"
        )

    print(f"Replaced {alias_count} alias pages, {regular_count} regular pages")
    print(f"Total: {alias_count + regular_count} HTML files")


def remove_non_html():
    """HTML と CNAME 以外のファイルを削除し、空ディレクトリも除去"""
    removed = 0
    for path in sorted(PUBLIC_DIR.rglob("*")):
        if path.is_dir():
            continue
        if path.suffix == ".html":
            continue
        if path.name == "CNAME":
            continue
        path.unlink()
        removed += 1

    # 空ディレクトリを削除（深い方から）
    for path in sorted(PUBLIC_DIR.rglob("*"), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()

    print(f"Removed {removed} non-HTML files")


def write_cname():
    """CNAME ファイルを配置"""
    cname_path = PUBLIC_DIR / "CNAME"
    cname_path.write_text(CNAME_HOST + "\n", encoding="utf-8")
    print(f"Created {cname_path}")


def main():
    run_zola_build()
    replace_html_files()
    remove_non_html()
    write_cname()
    print("\nDone!")


if __name__ == "__main__":
    main()
