#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import datetime
from html import unescape
from zoneinfo import ZoneInfo

import requests

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
ARTICLE_RE = re.compile(r"https://www\.jiemian\.com/article/\d+\.html")
CARD_RE = re.compile(r'<li class="card-list".*?</li>', re.S)
TITLE_LINK_RE = re.compile(
    r'<a[^>]+href="(https://www\.jiemian\.com/article/\d+\.html)"[^>]*>\s*<h3[^>]*class="card-list__title"[^>]*>(.*?)</h3>\s*</a>',
    re.S,
)
PUBLISH_TS_RE = re.compile(r'publish-time="(\d{10})"')


def fetch_text(url: str) -> str:
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=20)
    resp.raise_for_status()
    resp.encoding = resp.encoding or "utf-8"
    return resp.text


def clean_text(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw)
    text = unescape(" ".join(text.split()))
    return text.strip()


def looks_like_fragment(title: str) -> bool:
    title = title.strip()
    if not title:
        return True
    if len(title) <= 6:
        return True
    noisy_prefixes = (
        "现货黄金",
        "现货白银",
        "WTI原油",
        "LME",
        "国际油价",
        "国际金银",
        "国内商品期市",
    )
    if any(title.startswith(prefix) for prefix in noisy_prefixes):
        return True
    if re.fullmatch(r"[\d.%+\-\sA-Za-z/]+", title):
        return True
    return False


def extract_candidates(html: str, source: str, url: str, keep_fragments: bool = False):
    items = []
    seen = set()
    for block in CARD_RE.findall(html):
        m = TITLE_LINK_RE.search(block)
        if not m:
            continue
        article_url = m.group(1)
        if not ARTICLE_RE.fullmatch(article_url):
            continue
        title = clean_text(m.group(2))
        if not title:
            continue
        if (not keep_fragments) and looks_like_fragment(title):
            continue
        if article_url in seen:
            continue
        seen.add(article_url)
        items.append({
            "title": title,
            "url": article_url,
            "source": source,
            "listed_from": url,
        })
    return items


def extract_published_at(article_url: str):
    try:
        html = fetch_text(article_url)
    except Exception:
        return None
    m = PUBLISH_TS_RE.search(html)
    if not m:
        return None
    ts = int(m.group(1))
    return datetime.fromtimestamp(ts, tz=ZoneInfo("Asia/Shanghai")).isoformat()


def main():
    parser = argparse.ArgumentParser(description="Extract candidate article titles from Jiemian finance list page")
    parser.add_argument("--url", default="https://www.jiemian.com/lists/9.html")
    parser.add_argument("--source", default="界面新闻-金融频道")
    parser.add_argument("--output", help="Write JSON output to this file; default stdout")
    parser.add_argument("--max-items", type=int, default=0)
    parser.add_argument("--keep-fragments", action="store_true")
    parser.add_argument("--with-published-at", action="store_true", help="Fetch each article page and attach published_at")
    args = parser.parse_args()

    html = fetch_text(args.url)
    items = extract_candidates(html, args.source, args.url, keep_fragments=args.keep_fragments)
    if args.max_items and args.max_items > 0:
        items = items[: args.max_items]

    if args.with_published_at:
        for item in items:
            item["published_at"] = extract_published_at(item["url"])

    payload = {
        "site": args.url,
        "source": args.source,
        "count": len(items),
        "items": items,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    else:
        print(text)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
