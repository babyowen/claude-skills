#!/usr/bin/env python3
"""Generate the final output report."""
import json
from collections import Counter

# Site ordering from sites.json
SITE_ORDER = [
    ("cls-home", "财联社-首页"),
    ("cls-depth-1032", "财联社-深度-1032"),
    ("jiemian-finance", "界面新闻-金融频道"),
    ("eastmoney-home", "东方财富-首页"),
    ("eastmoney-bank", "东方财富-银行频道"),
    ("yicai-finance", "第一财经-金融频道"),
]

# First round counts
with open('data/first_round_filtered.json', 'r', encoding='utf-8') as f:
    first_round = json.load(f)
first_counts = Counter()
for item in first_round:
    src = item.get('source', '')
    first_counts[src] += 1

# Second round = new URLs added to daily JSON
try:
    with open('data/2026-03-30-new-urls.json', 'r', encoding='utf-8') as f:
        new_urls = json.load(f)
except:
    new_urls = []

with open('data/second_round_filtered.json', 'r', encoding='utf-8') as f:
    second_round = json.load(f)
second_counts = Counter()
for item in second_round:
    second_counts[item['source']] += 1

# Output table
print('| 站点 | 初筛入选 | 二轮入选 |')
print('|------|----------|----------|')
for site_id, site_name in SITE_ORDER:
    fr = first_counts.get(site_name, 0)
    sr = second_counts.get(site_name, 0)
    print('| {} | {} | {} |'.format(site_name, fr, sr))

# Second round titles
print('')
print('**二轮入选新闻：**')
for i, item in enumerate(second_round, 1):
    print('{}. {}'.format(i, item['title']))
