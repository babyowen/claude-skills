#!/usr/bin/env python3
"""
新闻词频统计日报：从 API 获取各关键词的新闻数量，对比昨天与前天的变化，
生成飞书卡片消息并发送到飞书群。
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone

CHINA_TZ = timezone(timedelta(hours=8))
DEFAULT_API_URL = "http://news.liuliang.world/api/word-count-stats"
DEFAULT_CHAT_ID = "oc_578717a43c0e5011765d9cada71d8218"

# 固定展示的关键词列表
DISPLAY_KEYWORDS = ["养老", "公积金", "政府基金", "中国烟草"]


def to_int(value):
    if value is None:
        return 0
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def fetch_data(api_url):
    import urllib.request
    import urllib.error
    try:
        req = urllib.request.Request(api_url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"ERROR fetching data from {api_url}: {e}", file=sys.stderr)
        sys.exit(1)


def china_date_to_fetchdate(china_date_str):
    year, month, day = map(int, china_date_str.split("-"))
    china_midnight = datetime(year, month, day, 0, 0, 0, tzinfo=CHINA_TZ)
    utc_dt = china_midnight.astimezone(timezone.utc)
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def compute_dates(override=None):
    if override:
        base_str = override
    else:
        now_china = datetime.now(CHINA_TZ)
        base_str = now_china.strftime("%Y-%m-%d")

    year, month, day = map(int, base_str.split("-"))
    base_date = datetime(year, month, day).date()
    yesterday_date = base_date - timedelta(days=1)
    day_before_date = base_date - timedelta(days=2)
    yesterday_str = yesterday_date.strftime("%Y-%m-%d")
    day_before_str = day_before_date.strftime("%Y-%m-%d")

    return (
        yesterday_str,
        day_before_str,
        china_date_to_fetchdate(yesterday_str),
        china_date_to_fetchdate(day_before_str),
    )


def filter_by_date(data, fetchdate_str):
    result = {}
    for record in data:
        if record.get("fetchdate") == fetchdate_str:
            keyword = record.get("keyword", "")
            result[keyword] = {
                "newsCount": to_int(record.get("newsCount")),
                "highScoreCount": to_int(record.get("highScoreCount")),
                "customGrabCount": to_int(record.get("customGrabCount", 0)),
                "wechatCount": to_int(record.get("wechatCount", 0)),
                "customGrabDetails": record.get("customGrabDetails", {}),
                "wechatDetails": record.get("wechatDetails", {}),
            }
    return result


def fmt_change(today_val, yesterday_val):
    if yesterday_val is None:
        return ""
    diff = today_val - yesterday_val
    if diff > 0:
        return f"↑+{diff}"
    elif diff < 0:
        return f"↓{diff}"
    return "→0"


def sort_details(details_dict):
    if not details_dict:
        return []
    return sorted(details_dict.items(), key=lambda x: x[1], reverse=True)


def build_card(today_data, yesterday_data, today_str, yesterday_str):
    """生成飞书交互式卡片 JSON dict。"""
    elements = []

    # 汇总
    total_today = sum(r["newsCount"] for r in today_data.values())
    total_yesterday = sum(r["newsCount"] for r in yesterday_data.values())
    high_today = sum(r["highScoreCount"] for r in today_data.values())
    high_yesterday = sum(r["highScoreCount"] for r in yesterday_data.values())

    total_chg = fmt_change(total_today, total_yesterday)
    high_chg = fmt_change(high_today, high_yesterday)

    elements.append({
        "tag": "markdown",
        "content": f"**昨日汇总**  抓取 **{total_today}** 条 {total_chg}  |  高分 **{high_today}** 条 {high_chg}"
    })
    elements.append({"tag": "hr"})

    # 4 个关键词
    keyword_lines = []
    for kw in DISPLAY_KEYWORDS:
        td = today_data.get(kw)
        yd = yesterday_data.get(kw)
        news = td["newsCount"] if td else 0
        high = td["highScoreCount"] if td else 0
        y_news = yd["newsCount"] if yd else None
        y_high = yd["highScoreCount"] if yd else None

        news_chg = fmt_change(news, y_news)
        high_chg = fmt_change(high, y_high)

        chg_part = f" {news_chg}" if news_chg else ""
        hchg_part = f" {high_chg}" if high_chg else ""
        keyword_lines.append(f"**{kw}**  {news} 条{chg_part}  |  高分 {high} 条{hchg_part}")

    elements.append({
        "tag": "markdown",
        "content": "\n".join(keyword_lines)
    })

    # 江苏省国资委明细
    jsgzw_today = today_data.get("江苏省国资委")
    jsgzw_yesterday = yesterday_data.get("江苏省国资委")

    if jsgzw_today:
        elements.append({"tag": "hr"})

        news = jsgzw_today["newsCount"]
        high = jsgzw_today["highScoreCount"]
        y_news = jsgzw_yesterday["newsCount"] if jsgzw_yesterday else None
        y_high = jsgzw_yesterday["highScoreCount"] if jsgzw_yesterday else None

        news_chg = fmt_change(news, y_news)
        high_chg = fmt_change(high, y_high)
        chg_part = f" {news_chg}" if news_chg else ""
        hchg_part = f" {high_chg}" if high_chg else ""

        detail_lines = [
            f"**江苏省国资委**  {news} 条{chg_part}  |  高分 {high} 条{hchg_part}",
        ]

        # 官网
        cg = jsgzw_today["customGrabCount"]
        cg_details = sort_details(jsgzw_today.get("customGrabDetails", {}))
        cg_str = "、".join(f"{n}({c})" for n, c in cg_details) if cg_details else "无"

        # 官微
        wc = jsgzw_today["wechatCount"]
        wc_details = sort_details(jsgzw_today.get("wechatDetails", {}))
        wc_str = "、".join(f"{n}({c})" for n, c in wc_details) if wc_details else "无"

        detail_lines.append(f"📄 官网({cg})：{cg_str}")
        detail_lines.append(f"📱 官微({wc})：{wc_str}")

        # 昨日对比
        if jsgzw_yesterday:
            cg_y = jsgzw_yesterday["customGrabCount"]
            wc_y = jsgzw_yesterday["wechatCount"]
            cg_chg = fmt_change(cg, cg_y)
            wc_chg = fmt_change(wc, wc_y)
            detail_lines.append(f"📊 前日对比  官网 {cg_y}→{cg} {cg_chg}  |  官微 {wc_y}→{wc} {wc_chg}")

        elements.append({
            "tag": "markdown",
            "content": "\n".join(detail_lines)
        })

    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "📊 新闻词频统计日报"},
            "subtitle": {"tag": "plain_text", "content": f"{today_str}  对比前日 ({yesterday_str})"},
            "template": "blue"
        },
        "elements": elements
    }

    return card


def card_to_text(card):
    """将卡片转为可读文本（用于 dry-run 输出）。"""
    lines = []
    lines.append(f"## {card['header']['title']['content']}")
    lines.append(f"{card['header']['subtitle']['content']}")
    lines.append("")
    for el in card["elements"]:
        if el["tag"] == "hr":
            lines.append("─" * 40)
        elif el["tag"] == "markdown":
            lines.append(el["content"])
        lines.append("")
    return "\n".join(lines)


def find_lark_cli():
    candidates = [
        "/usr/local/bin/lark-cli",
        "/opt/homebrew/bin/lark-cli",
        os.path.expanduser("~/.npm-global/bin/lark-cli"),
        os.path.expanduser("~/.local/bin/lark-cli"),
    ]
    try:
        npm_root = subprocess.check_output(
            ["npm", "root", "-g"], stderr=subprocess.DEVNULL, text=True
        ).strip()
        candidates.append(os.path.join(os.path.dirname(npm_root), "bin", "lark-cli"))
    except Exception:
        pass

    for path in candidates:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    found = shutil.which("lark-cli")
    if found:
        return found

    raise FileNotFoundError("lark-cli not found")


def send_card_to_feishu(card, chat_id):
    """通过 lark-cli 发送交互式卡片消息。"""
    try:
        lark_cli = find_lark_cli()
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    card_json = json.dumps(card, ensure_ascii=False)

    result = subprocess.run(
        [lark_cli, "im", "+messages-send", "--as", "bot",
         "--chat-id", chat_id,
         "--msg-type", "interactive",
         "--content", card_json],
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        print(f"ERROR sending to Feishu: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    print(f"Message sent successfully: {result.stdout.strip()}")


def main():
    parser = argparse.ArgumentParser(description="新闻词频统计日报")
    parser.add_argument("--chat-id", default=DEFAULT_CHAT_ID, help="飞书群 chat_id")
    parser.add_argument("--dry-run", action="store_true", help="只打印报告不发送")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help="API 地址")
    parser.add_argument("--date", default=None, help="覆盖今天日期 (YYYY-MM-DD)")
    args = parser.parse_args()

    # 1. 获取数据
    print(f"Fetching data from {args.api_url} ...")
    data = fetch_data(args.api_url)
    print(f"Fetched {len(data)} records")

    # 2. 计算日期
    yesterday_str, day_before_str, yesterday_fd, day_before_fd = compute_dates(args.date)
    print(f"Yesterday: {yesterday_str} (fetchdate: {yesterday_fd})")
    print(f"Day before: {day_before_str} (fetchdate: {day_before_fd})")

    # 3. 过滤数据
    yesterday_data = filter_by_date(data, yesterday_fd)
    day_before_data = filter_by_date(data, day_before_fd)
    print(f"Yesterday: {len(yesterday_data)} keywords, Day before: {len(day_before_data)} keywords")

    if not yesterday_data:
        print("WARNING: No data found for yesterday")

    # 4. 生成卡片
    card = build_card(yesterday_data, day_before_data, yesterday_str, day_before_str)

    # 5. 输出
    text = card_to_text(card)
    print()
    print("=" * 50)
    print(text)
    print("=" * 50)

    if args.dry_run:
        print("\n[DRY RUN] Report not sent to Feishu.")
    else:
        send_card_to_feishu(card, args.chat_id)


if __name__ == "__main__":
    main()
