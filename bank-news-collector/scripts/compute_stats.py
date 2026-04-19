#!/usr/bin/env python3
"""Compute per-site statistics for the report."""
import json
from collections import Counter

with open('data/first_round_filtered.json', 'r', encoding='utf-8') as f:
    first_round = json.load(f)

first_counts = Counter()
for item in first_round:
    src = item.get('source', item.get('listed_from', ''))
    first_counts[src] += 1

print('=== First round counts by source ===')
for src, cnt in sorted(first_counts.items()):
    print('  {}: {}'.format(src, cnt))
print('Total: {}'.format(len(first_round)))

try:
    with open('data/2026-03-30-new-urls.json', 'r', encoding='utf-8') as f:
        new_urls = json.load(f)
    print('\n=== New URLs ===')
    print('Count: {}'.format(len(new_urls)))
    for u in new_urls:
        print('  {}'.format(u))
except Exception as e:
    print('\nNo new-urls file: {}'.format(e))

try:
    with open('data/second_round_filtered.json', 'r', encoding='utf-8') as f:
        second_round = json.load(f)
    second_counts = Counter()
    for item in second_round:
        second_counts[item['source']] += 1
    print('\n=== Second round counts by source ===')
    for src, cnt in sorted(second_counts.items()):
        print('  {}: {}'.format(src, cnt))
    print('Total: {}'.format(len(second_round)))
except Exception as e:
    print('\nSecond round error: {}'.format(e))

try:
    with open('data/2026-03-30.json', 'r', encoding='utf-8') as f:
        daily = json.load(f)
    print('\n=== Daily JSON items: {} ==='.format(len(daily)))
    for item in daily:
        print('  - {} [{}]'.format(item['title'][:60], item.get('source', '')))
except Exception as e:
    print('\nDaily JSON error: {}'.format(e))
