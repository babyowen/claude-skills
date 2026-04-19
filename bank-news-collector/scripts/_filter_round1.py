import json

with open('data/candidates_all.json', 'r') as f:
    data = json.load(f)

items = data['items']
bank_kw = ['银行', '央行', '利率', '息差', '净息差', '存款', '贷款', '信贷', '逆回购', '债市', '理财', '六大行', '风控', '资本充足', 'PMI', '鲍威尔', '美联储', '降息', '加息', '招商', '工行', '建行', '农行', '交行', '邮储', '兴业银行', '中信银行', '浦发', '民生银行', '华夏银行', '徽商银行', '中原银行', '代销', '二永债', '消费贷', '经营贷', '分红', '金融稳定', '财富管理', 'REITs', '国债', '理财公司']

filtered = []
seen = set()
for item in items:
    title = item.get('title', '')
    url = item.get('url', '')
    source = item.get('source', '')
    if url in seen:
        continue
    is_bank = False
    if '银行频道' in source or '银行' in source:
        is_bank = True
    if not is_bank:
        is_bank = any(kw in title for kw in bank_kw)
    if not is_bank:
        if '债市' in title:
            is_bank = True
    if not is_bank:
        if '金融' in title and ('协调' in title or '安全网络' in title):
            is_bank = True
    if is_bank:
        seen.add(url)
        filtered.append({
            'title': title,
            'url': url,
            'source': source,
            'listed_from': item.get('listed_from', '')
        })

with open('data/first_round_filtered.json', 'w') as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)
print(len(filtered))
