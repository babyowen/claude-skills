#!/usr/bin/env python3
"""
步骤8：生成最终报告

从数据文件中读取统计，按照 assets/output_template.md 模板输出
"""

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SKILL_DIR = Path(__file__).resolve().parent.parent


def load_json(path):
    if not path.exists():
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def main():
    today = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime('%Y-%m-%d')

    # 从 sites.json 读取站点列表（保持顺序）
    sites_path = SKILL_DIR / "sites.json"
    sites = load_json(sites_path) or []
    site_names = [s['site_name'] for s in sites]

    # 读取第一轮筛选结果 → 按 source 统计初筛数量
    first_round_raw = load_json(DATA_DIR / "first_round_filtered.json") or []
    if isinstance(first_round_raw, dict) and 'items' in first_round_raw:
        first_round = first_round_raw['items']
    elif isinstance(first_round_raw, list):
        first_round = first_round_raw
    else:
        first_round = []
    first_round_by_site = Counter(item.get('source', '') for item in first_round if isinstance(item, dict))

    # 读取本次新增的URL列表（由 merge_news_json.py 生成）
    new_urls_data = load_json(DATA_DIR / f"{today}-new-urls.json") or []
    new_urls = set(item.get('url', str(item)) if isinstance(item, dict) else str(item) for item in new_urls_data) if isinstance(new_urls_data, list) else set()

    # 读取最终JSON（今日已收录的所有新闻）
    final = load_json(DATA_DIR / f"{today}.json") or []

    # 从 first_round 构建 source→listed_from 映射
    source_to_site = {}
    for item in first_round:
        src = item.get('source', '')
        lf = item.get('listed_from', '')
        if src and lf and src not in source_to_site:
            source_to_site[src] = lf

    # 二轮入选：仅统计本次运行新增的新闻（new_urls）
    new_items = [item for item in final if item.get('url', '') in new_urls]
    second_round_by_site = Counter()
    for item in new_items:
        src = item.get('source', '')
        # 尝试映射回完整 site_name
        site_name = source_to_site.get(src, src)
        # 如果还是不匹配，尝试模糊匹配
        if site_name not in site_names:
            for sn in site_names:
                if src in sn or sn.startswith(src):
                    site_name = sn
                    break
        second_round_by_site[site_name] += 1

    # 读取模板
    template_path = SKILL_DIR / "assets" / "output_template.md"
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # 构建模板变量
    template_vars = {}
    for site in site_names:
        template_vars[f'{site}_初筛'] = first_round_by_site.get(site, 0)
        template_vars[f'{site}_二轮'] = second_round_by_site.get(site, 0)

    # 今日已收录的所有新闻（全量，不仅限本次新增）
    titles = [f"{i}. {item['title']}" for i, item in enumerate(final, 1)]
    template_vars['二轮入选新闻列表'] = '\n'.join(titles) if titles else '(今日无收录)'

    # 渲染模板
    output = template.format(**template_vars)
    print(output)


if __name__ == '__main__':
    main()
