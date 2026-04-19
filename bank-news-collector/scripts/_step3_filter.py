import json

with open('data/candidates_all.json') as f:
    data = json.load(f)

# Banking-related keywords for first round filtering (宽进)
bank_keywords = [
    '银行', '存款', '贷款', '信贷', '息差', '净息差', '央行', '人行',
    '不良', '资本充足', '理财', '二永债', '永续债', '优先股',
    '利率', '降息', '加息', 'LPR', '逆回购', 'MLF',
    '国债', '金融稳定', '金融监管', '银保监', '金管局',
    '招行', '工行', '建行', '农行', '中行', '交行', '邮储',
    '中信银行', '平安银行', '兴业银行', '浦发银行', '民生银行',
    '华夏银行', '光大银行', '招商银行', '工商银行', '建设银行',
    '农业银行', '中国银行', '交通银行', '晋商银行', '徽商银行',
    '六大行', '上市银行', '中小银行', '城商行', '农商行',
    '金融安全', '金融风险', '跨境支付', '银联', '人民币国际化',
    '代销', '财富管理', '资产管理', '私人银行',
    'AIC', '金融资产投资', '风控',
    '金融科技', '数字货币', '跨境', '自贸',
    '债券', '债市', '货币供应', '流动性',
    '保险', '分红险', '信托', '资管新规',
    '巴塞尔', '资本补充', '资本管理',
    '置换债', '地方债', '专项债',
    '金融开放', '金融改革',
    '消费贷', '经营贷', '按揭', '信用卡',
    '美联储', '鲍威尔',
    '国际收支', '外汇储备',
    '苏河财富对话', '陆家嘴金融',
    '工商银行', '农业银行',
]

# Exclude patterns - not news or clearly not banking
exclude_keywords = [
    '涨停', '跌停', '龙虎榜', '概念股', '复盘',
    '申购', '中签', '新股', '北向资金', '融资融券',
    '半导体', '芯片', '光纤', '机器人', 'AI算力',
    '创新药', '碳酸锂', '储能', '光伏', '煤炭',
    '茅台', '猪价', '铝', '油价', '黄金价格',
    '巴菲特', '力箭', '火箭', '航天',
    '小米', '苹果', '微软', '阿里', '千问',
    '印度', '乌克兰', '俄罗斯', '泽连斯基', '特朗普',
    '伊朗', '以色列', '霍尔木兹', '中东',
    '巴基斯坦', '古巴', '日本', '土耳其',
    '内存条', '华强北', '千岸科技', '惠城环保',
    '美的集团', '中手游', '龙湖', '壁仞',
    '摩尔线程', '斯比特', '英矽智能', 'GTC',
    '黄仁勋', '机器人任意', '宇树科技',
    '德适', '港股IPO', '群核科技',
    '爱奇艺', '上市辅导', 'QFII',
    'MACD', 'K线', '什么企业', '判断企业',
    '互动易', '讨论群', '如何挑选',
    '债券ETF', '避险情绪',
]

def is_bank_related(title):
    title_lower = title.lower()
    # First check strong banking keywords
    for kw in bank_keywords:
        if kw in title:
            return True
    return False

def is_excluded(title):
    for kw in exclude_keywords:
        if kw in title:
            return True
    return False

filtered = []
seen_urls = set()

for item in data['items']:
    title = item['title']
    url = item['url']

    # Skip duplicates
    if url in seen_urls:
        continue
    seen_urls.add(url)

    # Skip excluded items
    if is_excluded(title):
        continue

    # Check if bank-related (宽进)
    if is_bank_related(title):
        filtered.append(item)

# Save filtered results
output = {
    'count': len(filtered),
    'timestamp': data['timestamp'],
    'items': filtered
}

with open('data/first_round_filtered.json', 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# Print stats per source
source_counts = {}
for item in filtered:
    src = item['source']
    source_counts[src] = source_counts.get(src, 0) + 1

for src, cnt in sorted(source_counts.items()):
    print(f'{src}: {cnt}')
print(f'Total filtered: {len(filtered)}')
