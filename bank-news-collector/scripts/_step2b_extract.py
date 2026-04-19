import json, re

# Read existing candidates
with open('data/candidates_all.json', 'r') as f:
    data = json.load(f)

existing_urls = set(item['url'] for item in data['items'])
new_items = []

# --- 第一财经-金融频道 ---
with open('data/raw_yicai-finance.md', 'r') as f:
    yicai_content = f.read()

yicai_source = '第一财经-金融频道'
yicai_listed = 'https://www.yicai.com/news/jinrong/'
yicai_urls = set()

# Extract news titles and URLs from the carousel area
# Pattern: ## Title ... ](URL)
for m in re.finditer(r'##\s+([^#\]\[]+?)\s+\d+\s+[\d-]+\s+[\d:]+\]\((https://www\.yicai\.com/news/\d+\.html)\)', yicai_content):
    title = m.group(1).strip()
    url = m.group(2)
    exclude_kws = ['研报金选', '博时ETF更名', '以清晰之名赴时代']
    if any(kw in title for kw in exclude_kws):
        continue
    if url not in yicai_urls and url not in existing_urls:
        yicai_urls.add(url)
        new_items.append({
            'title': title,
            'url': url,
            'source': yicai_source,
            'listed_from': yicai_listed
        })

# Also try broader pattern
for m in re.finditer(r'##\s+([^#\]\[\n]+?)\s+\d+\s+[\d\-]+\s+[\d:]+\]\((https://www\.yicai\.com/news/\d+\.html)\)', yicai_content):
    title = m.group(1).strip()
    url = m.group(2)
    exclude_kws = ['研报金选', '博时ETF更名', '以清晰之名赴时代']
    if any(kw in title for kw in exclude_kws):
        continue
    if url not in yicai_urls and url not in existing_urls:
        yicai_urls.add(url)
        new_items.append({
            'title': title,
            'url': url,
            'source': yicai_source,
            'listed_from': yicai_listed
        })

print(f'yicai extracted: {len(yicai_urls)}')

# --- 东方财富-银行频道 ---
with open('data/raw_eastmoney-bank.md', 'r') as f:
    bank_content = f.read()

bank_source = '东方财富-银行频道'
bank_listed = 'https://bank.eastmoney.com/'
bank_urls = set()

for m in re.finditer(r'\[([^\]]+)\]\((https://finance\.eastmoney\.com/a/\d+\.html)\)', bank_content):
    title = m.group(1).strip()
    url = m.group(2)
    exclude_kws = ['点击查看更多', '银行导读', '银行头条']
    if any(kw in title for kw in exclude_kws):
        continue
    if len(title) < 8:
        continue
    if url not in bank_urls and url not in existing_urls:
        bank_urls.add(url)
        new_items.append({
            'title': title,
            'url': url,
            'source': bank_source,
            'listed_from': bank_listed
        })

print(f'eastmoney-bank extracted: {len(bank_urls)}')

# --- 东方财富-首页 ---
with open('data/raw_eastmoney-home.md', 'r') as f:
    home_content = f.read()

home_source = '东方财富-首页'
home_listed = 'https://www.eastmoney.com/'
home_urls = set()

exclude_title_kws = ['点击查看', '东方财富', '涨停股复盘', '龙虎榜',
    '晚间公告', '财经早餐', '新闻联播', '央视新闻', '头版头条',
    '申购表', '利好消息一览', '公司公告', '全球快讯', '十大成交股',
    '北向资金最新动向', '北向资金动向']

for m in re.finditer(r'\[([^\]]+)\]\((https://finance\.eastmoney\.com/a/\d+\.html)\)', home_content):
    title = m.group(1).strip()
    url = m.group(2)
    if len(title) < 8:
        continue
    if any(kw in title for kw in exclude_title_kws):
        continue
    if url not in home_urls and url not in existing_urls and url not in bank_urls:
        home_urls.add(url)
        new_items.append({
            'title': title,
            'url': url,
            'source': home_source,
            'listed_from': home_listed
        })

print(f'eastmoney-home extracted: {len(home_urls)}')

# Append and save
data['items'].extend(new_items)
data['count'] = len(data['items'])
data['sites'] = 6
data['pending_llm_files'] = []

with open('data/candidates_all.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Total items now: {data["count"]}')
