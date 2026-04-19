import json

with open('data/candidates_all.json', encoding='utf-8') as f:
    data = json.load(f)

items = data['items']
seen_urls = set()
filtered = []

for item in items:
    url = item['url']
    title = item['title']
    source = item.get('source', '')
    listed_from = item.get('listed_from', '')

    # 跳过重复URL
    if url in seen_urls:
        continue
    seen_urls.add(url)

    # 默认跳过
    result = 'skip'

    # ========== 逐条判断 ==========

    # --- 财联社深度 + 首页 ---
    # 1. 对话中国平安路昊阳 -> 保险投资策略，非银行
    if '对话中国平安路昊阳' in title:
        result = 'skip'

    # 2. 股债金三线溃败 -> 宏观市场行情
    elif '股债金三线溃败' in title:
        result = 'skip'

    # 3. 上海交易集团管小军 -> 交易集团并购，非银行
    elif '上海交易集团' in title and '管小军' in title:
        result = 'skip'

    # 4. 邮储银行业绩会高管层 -> 银行业绩
    elif '邮储银行' in title and ('业绩会' in title or '零售金融' in title):
        result = 'pass'

    # 5. 资管周报：理财公司自评整改 -> 银行理财子公司相关
    elif '资管周报' in title and '理财公司' in title:
        result = 'pass'

    # 6. 债市公告精选|融创中国 -> 房企债市，排除
    elif '债市公告精选' in title and '融创' in title:
        result = 'skip'

    # 7. 债市早参3月30日|置换债 -> 置换债落地影响银行
    elif '债市早参' in title and '置换债' in title:
        result = 'pass'

    # 8. S基金迎来新玩家 -> PE二级市场，非银行
    elif 'S基金迎来' in title:
        result = 'skip'

    # 9. 已披露年报A股银行近半数净息差 -> 银行净息差分析
    elif 'A股银行' in title and '净息差' in title:
        result = 'pass'

    # 10. 北外滩财富与文化论坛 -> 财富管理
    elif '北外滩财富与文化论坛' in title or ('2026北外滩' in title and '财富管理' in title):
        result = 'pass'

    # 11. 广慧并购研究院 -> 并购基金
    elif '广慧并购研究院' in title:
        result = 'skip'

    # 12. 直面复杂市场环境 中国太保 -> 保险
    elif '中国太保' in title and '权益投资占比' in title:
        result = 'skip'

    # 13. 苏河财富对话 -> 并购重组
    elif '苏河财富对话' in title:
        result = 'skip'

    # 14. 今年存款到期量增加，交行 -> 银行息差/存款
    elif '存款到期量增加' in title and '交行' in title:
        result = 'pass'

    # 15. 招商银行年度交卷 -> 银行业绩
    elif '招商银行年度' in title and '交卷' in title:
        result = 'pass'

    # 16. 分红险演示利率下调 -> 保险产品，但银行代销保险受影响，宽进保留
    elif '分红险演示利率下调' in title:
        result = 'pass'

    # 17. 建行管理层 -> 银行
    elif '上市20年分红超1.4万亿' in title and '建行' in title:
        result = 'pass'

    # 18. 人保管理层 -> 保险
    elif '人保管理层' in title and 'A股净加仓' in title:
        result = 'skip'

    # 19. 总资产突破53万亿，工行 -> 银行
    elif '总资产突破53万亿' in title and '工行' in title:
        result = 'pass'

    # 20. 3月纯债基业绩榜单 -> 基金榜单
    elif '纯债基业绩榜单' in title:
        result = 'skip'

    # 21. 中国保险行业协会 -> 保险自律
    elif '保险行业协会' in title and '自律规范' in title:
        result = 'skip'

    # 22. 债市收盘|国债收益率 -> 影响银行资产
    elif '债市收盘' in title and '国债收益率' in title:
        result = 'pass'

    # 23. 27亿假黄金骗贷案 -> 信贷风控
    elif '27亿假黄金骗贷案' in title:
        result = 'pass'

    # 24. 美联储紧急加息 -> 央行政策影响银行
    elif '美联储' in title and '紧急加息' in title:
        result = 'pass'

    # 25. 非息收入撑住营收，兴业银行 -> 银行
    elif '非息收入撑住营收' in title and '兴业银行' in title:
        result = 'pass'

    # 26. 债市公告精选|合景集团 -> 房企债务
    elif '债市公告精选' in title and '合景集团' in title:
        result = 'skip'

    # 27. 陆家嘴金融沙龙预告 -> 活动预告
    elif '陆家嘴金融沙龙' in title and '即将启幕' in title:
        result = 'skip'

    # 28. 美伊战争历史对比 -> 地缘政治
    elif '美伊战争与历史战事对比' in title:
        result = 'skip'

    # 29. ICMA债务资本市场年度会议 -> 会议广告
    elif 'ICMA' in title and '年度会议' in title:
        result = 'skip'

    # 30. 黄金为何跌不停/央行抛售 -> 央行操作
    elif '黄金为何跌不停' in title and '央妈' in title:
        result = 'pass'

    # --- 财联社首页独有 ---
    # 31. 欧洲主要股指 -> 行情
    elif '欧洲主要股指开盘集体下跌' in title:
        result = 'skip'

    # 32. 国内商品期货 -> 行情
    elif '国内商品期货多数收涨' in title:
        result = 'skip'

    # 33. 收评：沪指 -> 股市行情
    elif '收评：沪指' in title:
        result = 'skip'

    # 34. 泡泡玛特乐园 -> 文娱
    elif '泡泡玛特乐园' in title:
        result = 'skip'

    # 35. 西班牙领空 -> 国际政治
    elif '西班牙宣布' in title and '领空' in title:
        result = 'skip'

    # 36. 防范伊朗打击 -> 国际政治
    elif '防范伊朗打击' in title:
        result = 'skip'

    # 37. 盘中宝AI技术 -> 产品推广
    elif '盘中宝' in title:
        result = 'skip'

    # 38. 日本参议院预算 -> 日本政治
    elif '日本参议院' in title:
        result = 'skip'

    # 39. 财政部注册会计师法 -> 财政立法，宽进保留
    elif '财政部' in title and '注册会计师法' in title:
        result = 'pass'

    # 40. 法国兴业银行布伦特原油 -> 原油预测，非银行经营
    elif '法国兴业银行' in title and '布伦特原油' in title:
        result = 'skip'

    # --- 界面新闻 ---
    # 41. 海尔投资虞美人 -> 企业辟谣
    elif '海尔投资' in title and '虞美人' in title:
        result = 'skip'

    # 42. 千亿赎回潮！上市银行高息优先股 -> 银行资本管理
    elif '上市银行高息优先股' in title:
        result = 'pass'

    # 43. 每周债市看点|泰禾 -> 房企失信
    elif '每周债市看点' in title:
        result = 'skip'

    # 44. 直击交行业绩会 -> 银行
    elif '直击交行业绩会' in title:
        result = 'pass'

    # 45. 直击中国太保业绩会 -> 保险
    elif '直击中国太保' in title and '业绩会' in title:
        result = 'skip'

    # 46. 新掌门首秀！人保财险 -> 保险
    elif '人保财险' in title and '新掌门' in title:
        result = 'skip'

    # 47. 扭亏为盈、连连数字 -> 跨境支付公司
    elif '连连数字' in title:
        result = 'pass'

    # 48. 个人贷款突破9万亿，建行 -> 银行
    elif '个人贷款突破9万亿' in title and '建行' in title:
        result = 'pass'

    # 49. 全球首家！工行资产破50万亿 -> 银行
    elif '工行资产破50万亿' in title:
        result = 'pass'

    # 50. 锚定高质量发展，东方证券 -> 证券
    elif '东方证券' in title and '高质量发展' in title:
        result = 'skip'

    # 51. 11万亿兴业银行三大战略 -> 银行
    elif '11万亿兴业银行' in title:
        result = 'pass'

    # 52. 去年业绩如何？中国平安 -> 保险
    elif '中国平安管理层' in title:
        result = 'skip'

    # --- 东方财富银行频道 ---
    # 53. 中信银行跻身10万亿 -> 银行
    elif '中信银行跻身10万亿俱乐部' in title:
        result = 'pass'

    # 54. 无形资产换贷款 -> 银行信贷
    elif '无形资产换贷款' in title:
        result = 'pass'

    # 55. 部分中小银行代销业务 -> 银行代销
    elif '中小银行代销业务' in title:
        result = 'pass'

    # 56. 经营发展质效兼备 交通银行 -> 银行年报
    elif '交通银行发布2025年度业绩' in title:
        result = 'pass'

    # 57. 多家中小银行下调存款利率 -> 银行利率
    elif '中小银行下调存款利率' in title:
        result = 'pass'

    # 58. 净息差拐点来了？工行建行 -> 银行息差
    elif '净息差拐点' in title and ('工行' in title or '建行' in title):
        result = 'pass'

    # 59. 央行召开金融稳定工作会议 -> 央行政策
    elif '央行召开金融稳定工作会议' in title:
        result = 'pass'

    # 60. 信贷精准直达 银行搭建 -> 银行跨境信贷
    elif '信贷精准直达' in title and '银行' in title:
        result = 'pass'

    # 61. 二永债市场迎换仓潮 -> 银行资本债
    elif '二永债市场迎换仓潮' in title:
        result = 'pass'

    # 62. 金价短线高波动 银行风控 -> 银行风控
    elif '金价短线高波动' in title and '银行风控' in title:
        result = 'pass'

    # 63. 交通银行拟申请撤销私人银行 -> 银行牌照
    elif '交通银行' in title and '私人银行' in title:
        result = 'pass'

    # 64. 银联二维码互联互通 -> 银行支付
    elif '银联二维码互联互通' in title:
        result = 'pass'

    # 65. AI面试官登场 银行 -> 银行数智化
    elif 'AI面试官' in title and '银行' in title:
        result = 'pass'

    # 66. 银行理财 黄金价格失稳 -> 银行理财
    elif '银行理财' in title and '黄金价格失稳' in title:
        result = 'pass'

    # 67. 银行春招 -> 银行人才
    elif '银行春招' in title:
        result = 'pass'

    # 68. 资产首破十万亿 中信银行 -> 银行
    elif '资产首破十万亿' in title and '中信银行' in title:
        result = 'pass'

    # 69. A股首批银行年报分红率 -> 银行分红
    elif '银行年报分红率' in title:
        result = 'pass'

    # 70. 密集降息 中小银行 -> 银行利率
    elif '密集降息' in title and '中小银行' in title:
        result = 'pass'

    # 71. A股持续调整 银行理财资金 -> 银行理财
    elif '银行理财资金' in title:
        result = 'pass'

    # 72. 多家银行理财子公司定增 -> 银行理财
    elif '银行理财子公司' in title and '定增' in title:
        result = 'pass'

    # --- 第一财经 ---
    # 73. 不止于贷款 兴业银行 -> 银行
    elif '兴业银行' in title and ('不止于贷款' in title or '产业金融' in title):
        result = 'pass'

    # 74. 适配L2-L4 智驾车险 -> 保险车险
    elif '智驾车险' in title:
        result = 'skip'

    # 75. 长期资本入市堵点 博鳌 -> 资本市场
    elif '长期资本入市' in title and '博鳌' in title:
        result = 'pass'

    # 76. 险企投资水平高下 -> 保险
    elif '险企投资水平' in title:
        result = 'skip'

    # 77. 银行火拼消费贷经营贷 -> 银行业务
    elif '银行火拼消费贷' in title:
        result = 'pass'

    # 78. 科创链接中国东盟 人民币 -> 人民币跨境
    elif '人民币' in title and '中国东盟' in title:
        result = 'pass'

    # 79. 解码中国太保的大康养 -> 保险
    elif '中国太保' in title and '大康养' in title:
        result = 'skip'

    # 80. 陆金所控股 陈东起 -> 金融科技公司人事
    elif '陆金所控股' in title:
        result = 'pass'

    # 81. 净息差拐点来了 工行建行（第一财经版）-> 银行息差
    elif '净息差拐点来了' in title:
        result = 'pass'

    # 82. 国泰海通发布2025年年报 -> 证券
    elif '国泰海通' in title and '年报' in title:
        result = 'skip'

    # 83. 息差回暖财富收入恢复增长 招商银行 -> 银行
    elif '息差回暖' in title and '招商银行' in title:
        result = 'pass'

    # 84. 大量定存到期如何应对 建行 -> 银行存款
    elif '大量定存到期' in title and '建行' in title:
        result = 'pass'

    # 85. 权益投资比例 太保 -> 保险
    elif '太保' in title and '权益投资比例' in title:
        result = 'skip'

    # 86. 博鳌观察 国际金融协调 -> 国际金融
    elif '博鳌观察' in title and '国际金融协调' in title:
        result = 'pass'

    # 87. 会否提高分红率 刘珺 工行 -> 银行分红
    elif '刘珺' in title and '工行' in title:
        result = 'pass'

    # 88. 价值共享 徽商银行 -> 银行业绩
    elif '徽商银行' in title and '业绩' in title:
        result = 'pass'

    # 89. 直击平安业绩发布会 -> 保险
    elif '直击平安业绩发布会' in title:
        result = 'skip'

    # 90. 出海新动能 中行上海市分行 -> 银行跨境
    elif '中行上海市分行' in title:
        result = 'pass'

    # 91. 锚定新兴支柱产业 中国太保 -> 保险
    elif '中国太保' in title and '低空经济' in title:
        result = 'skip'

    # 92. 太保新业务价值大增 -> 保险
    elif '太保新业务价值' in title:
        result = 'skip'

    if result == 'pass':
        filtered.append({
            'title': title,
            'url': url,
            'source': source,
            'listed_from': listed_from
        })

output = {'items': filtered}
with open('data/first_round_filtered.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'Total unique items: {len(seen_urls)}')
print(f'Passed filter: {len(filtered)}')
print(f'Skipped: {len(seen_urls) - len(filtered)}')
