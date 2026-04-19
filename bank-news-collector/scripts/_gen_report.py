import json

today = json.load(open('data/2026-03-31.json'))
first = json.load(open('data/first_round_filtered.json'))
second = json.load(open('data/second_round_filtered.json'))
incr = json.load(open('data/incremental_candidates.json'))

fr_sites = {}
for item in first:
    s = item['source']
    fr_sites[s] = fr_sites.get(s, 0) + 1

url_to_source = {item['url']: item['source'] for item in incr}
sr_sites = {}
for item in second:
    url = item['url']
    orig_source = url_to_source.get(url, '')
    sr_sites[orig_source] = sr_sites.get(orig_source, 0) + 1

sites_order = ['财联社-首页', '财联社-深度-1032', '界面新闻-金融频道', '东方财富-首页', '东方财富-银行频道', '第一财经-金融频道']

for s in sites_order:
    fr = fr_sites.get(s, 0)
    sr = sr_sites.get(s, 0)
    print(f'{s}: fr={fr} sr={sr}')
print(f'today_total={len(today)}')
print()
for i, item in enumerate(today):
    print(f'{i+1}. {item["title"]}')
