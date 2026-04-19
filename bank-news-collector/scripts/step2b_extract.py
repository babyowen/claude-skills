import json

with open('data/candidates_all.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

new_items = []

eb = [
    {"title": "中信银行跻身10万亿俱乐部 去年分红超212亿", "url": "https://finance.eastmoney.com/a/202603223679685564.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "无形资产换贷款 多方搭台推动信贷投放巧发力", "url": "https://finance.eastmoney.com/a/202603303688107625.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "部分中小银行代销业务迎来首单突破", "url": "https://finance.eastmoney.com/a/202603303688097961.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "经营发展质效兼备 特色优势日益彰显 交通银行发布2025年度业绩", "url": "https://finance.eastmoney.com/a/202603273687154213.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "多家中小银行下调存款利率 注重优化存款结构", "url": "https://finance.eastmoney.com/a/202603293687916588.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "已披露年报A股银行近半数净息差未继续下滑 业内判断2026年望进一步企稳", "url": "https://finance.eastmoney.com/a/202603293687929437.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "净息差拐点来了？工行建行这样预测", "url": "https://finance.eastmoney.com/a/202603283687773541.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "央行召开金融稳定工作会议：推动多渠道加大资本补充力度", "url": "https://finance.eastmoney.com/a/202603273687078491.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "信贷精准直达 银行搭建全球南方资金融通桥梁", "url": "https://finance.eastmoney.com/a/202603263684588721.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "二永债市场迎换仓潮 银行发行缘何冷暖不均", "url": "https://finance.eastmoney.com/a/202603263684763553.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "金价短线高波动 银行风控思路转向动态调整", "url": "https://finance.eastmoney.com/a/202603263684543745.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "业内首家 交通银行拟申请撤销私人银行专营机构牌照 已持牌经营13年", "url": "https://finance.eastmoney.com/a/202603243682933074.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "银联二维码互联互通增势显著 跨境支付新基建赋能经贸与人员往来", "url": "https://finance.eastmoney.com/a/202603253683057550.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "AI面试官登场 银行正经历人机协同数智化深潜", "url": "https://finance.eastmoney.com/a/202603253683057474.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "银行理财 黄金价格失稳 净值波动考验运作能力", "url": "https://finance.eastmoney.com/a/202603253683017375.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "和互联网大厂争抢科技人才 银行春招靠什么取胜", "url": "https://finance.eastmoney.com/a/202603253683008061.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "资产首破十万亿 中信银行董事长直言稳降组合打开利润增长空间", "url": "https://finance.eastmoney.com/a/202603243682300148.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "A股首批银行年报分红率提升 会否成趋势", "url": "https://finance.eastmoney.com/a/202603243682310235.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "密集降息 中小银行长期存款利率迈入1字头", "url": "https://finance.eastmoney.com/a/202603243682238857.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "A股持续调整 银行理财资金也在抛售 业内称控回撤被动应对", "url": "https://finance.eastmoney.com/a/202603233681322795.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
    {"title": "多家银行理财子公司成功参与上市公司定增项目", "url": "https://finance.eastmoney.com/a/202603243681358816.html", "source": "东方财富-银行频道", "listed_from": "eastmoney-bank"},
]

yc = [
    {"title": "不止于贷款 兴业银行董事长详解产业金融服务整个生态", "url": "https://www.yicai.com/news/103109902.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "适配L2-L4全级别 北京率先启动智驾车险开发应用", "url": "https://www.yicai.com/news/103109885.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "长期资本入市堵点如何疏通 博鳌论坛开出这些药方", "url": "https://www.yicai.com/news/103109092.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "最高6.6%最低4.04% 不一致披露口径难掩险企投资水平高下", "url": "https://www.yicai.com/news/103109173.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "银行火拼消费贷经营贷 工行邮储兴业信用卡业务降幅超10%", "url": "https://www.yicai.com/news/103109149.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "科创链接中国东盟 人民币成区域贸易投资重要选择", "url": "https://www.yicai.com/news/103109041.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "解码中国太保的大康养 以战略坚守筑基以一体化升级破局", "url": "https://www.yicai.com/news/103109028.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "陆金所控股 陈东起辞任公司总经理", "url": "https://www.yicai.com/news/103108816.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "净息差拐点来了 工行建行这样预测", "url": "https://www.yicai.com/news/103108544.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "国泰海通发布2025年年报 经营业绩创历史新高", "url": "https://www.yicai.com/news/103108548.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "息差回暖财富收入恢复增长 招商银行营收增幅转正", "url": "https://www.yicai.com/news/103108433.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "大量定存到期如何应对 建行回应目前承接率较好", "url": "https://www.yicai.com/news/103108376.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "权益投资比例低于上市同业 太保管理层称具有更优回撤控制能力", "url": "https://www.yicai.com/news/103108256.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "博鳌观察 国际金融协调面临挑战 亚洲呼吁建区域金融安全网", "url": "https://www.yicai.com/news/103108097.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "会否提高分红率 刘珺称若市场确有呼声工行将带头响应", "url": "https://www.yicai.com/news/103108033.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "价值共享 致远未来 徽商银行2025年度业绩", "url": "https://www.yicai.com/news/103107990.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "直击平安业绩发布会 用AI打造超级入口", "url": "https://www.yicai.com/news/103107934.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "锚定高质量发展 东方证券启新程", "url": "https://www.yicai.com/news/103107946.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "出海新动能 护航新征程 中行上海市分行举办出海综合服务新生态共建活动", "url": "https://www.yicai.com/news/103107877.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "锚定新兴支柱产业 中国太保专业护航低空经济高飞", "url": "https://www.yicai.com/news/103107511.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
    {"title": "太保新业务价值大增四成位居前列 股票占比罕见达两位数", "url": "https://www.yicai.com/news/103106500.html", "source": "第一财经-金融频道", "listed_from": "yicai-finance"},
]

new_items = eb + yc
data['items'].extend(new_items)
data['count'] = len(data['items'])
if 'pending_llm_files' in data:
    del data['pending_llm_files']

with open('data/candidates_all.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_items)} items. Total: {data['count']}")
