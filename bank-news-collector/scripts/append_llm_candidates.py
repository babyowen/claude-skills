import json
import os

os.chdir('/Users/babyowen/.claude/skills/bank-news-collector')

with open('data/candidates_all.json', 'r') as f:
    data = json.load(f)

new_items = []

bank_items = [
    {"title": "交行因分红公告闹乌龙致歉 每股实为每10股", "url": "https://finance.eastmoney.com/a/202603313690341361.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "多家上市银行去年代销保险保费与收入双增 分红险成银保渠道主力", "url": "https://finance.eastmoney.com/a/202603313689311778.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "2025年国有六大行合计净赚1.42万亿元 均拟派发现金股息逾2200亿元", "url": "https://finance.eastmoney.com/a/202603313689311050.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "国有六大行去年日赚超39亿元 5家不良率继续小幅回落", "url": "https://finance.eastmoney.com/a/202603303689044786.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "国有六大行2025年成绩单全部揭晓 农业银行净利润增速领跑", "url": "https://finance.eastmoney.com/a/202603303688895226.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "无形资产换贷款 多方搭台推动信贷投放巧发力", "url": "https://finance.eastmoney.com/a/202603303688107625.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "部分中小银行代销业务迎来首单突破", "url": "https://finance.eastmoney.com/a/202603303688097961.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "经营发展质效兼备 特色优势日益彰显——交通银行发布2025年度业绩", "url": "https://finance.eastmoney.com/a/202603273687154213.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "多家中小银行下调存款利率 注重优化存款结构", "url": "https://finance.eastmoney.com/a/202603293687916588.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "已披露年报A股银行近半数净息差未继续下滑 业内判断2026年望进一步企稳", "url": "https://finance.eastmoney.com/a/202603293687929437.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "净息差拐点来了？工行建行这样预测", "url": "https://finance.eastmoney.com/a/202603283687773541.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "央行召开金融稳定工作会议：推动多渠道加大资本补充力度", "url": "https://finance.eastmoney.com/a/202603273687078491.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "信贷精准直达 银行搭建全球南方资金融通桥梁", "url": "https://finance.eastmoney.com/a/202603263684588721.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "二永债市场迎换仓潮 银行发行缘何冷暖不均", "url": "https://finance.eastmoney.com/a/202603263684763553.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "金价短线高波动 银行风控思路转向动态调整", "url": "https://finance.eastmoney.com/a/202603263684543745.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "业内首家 交通银行拟申请撤销私人银行专营机构牌照 已持牌经营13年", "url": "https://finance.eastmoney.com/a/202603243682933074.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "AI面试官登场 银行正经历人机协同样数智化深潜", "url": "https://finance.eastmoney.com/a/202603253683057474.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
    {"title": "银行理财 黄金价格失稳 净值波动考验运作能力", "url": "https://finance.eastmoney.com/a/202603253683017375.html", "source": "东方财富-银行频道", "listed_from": "https://bank.eastmoney.com/"},
]

home_items = [
    {"title": "央行：继续实施适度宽松的货币政策 促进物价回升", "url": "https://finance.eastmoney.com/a/202603313690482823.html", "source": "东方财富-首页", "listed_from": "https://www.eastmoney.com/"},
    {"title": "4400多只股票下跌 银行股逆市走强 后市怎么看", "url": "https://finance.eastmoney.com/a/202603313690535441.html", "source": "东方财富-首页", "listed_from": "https://www.eastmoney.com/"},
    {"title": "超预期 A股五家险企去年净利增超22% 权益投资扛旗", "url": "https://finance.eastmoney.com/a/202603313690372951.html", "source": "东方财富-首页", "listed_from": "https://www.eastmoney.com/"},
    {"title": "1-2月国企营业收入同比增长0.2% 利润总额下降2%", "url": "https://finance.eastmoney.com/a/202603313690408068.html", "source": "东方财富-首页", "listed_from": "https://www.eastmoney.com/"},
    {"title": "最大股票回购再贷款将至 A股3月实施回购88亿 近万亿分红蓄势待发", "url": "https://finance.eastmoney.com/a/202603313690393426.html", "source": "东方财富-首页", "listed_from": "https://www.eastmoney.com/"},
    {"title": "本外币统一的境内企业境外上市资金管理政策4月1日实施", "url": "https://finance.eastmoney.com/a/202603313689358046.html", "source": "东方财富-首页", "listed_from": "https://www.eastmoney.com/"},
]

yicai_items = [
    {"title": "兴业银行伴飞企业出海全周期，创新金融服务破解全球化壁垒", "url": "https://www.yicai.com/news/103112550.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "中信银行VS兴业银行：同等营收下的利润较量，兴业硬抠多了68亿", "url": "https://www.yicai.com/news/103112443.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "熊猫债发行迎火热开局，银行年报折射人民币国际化提速", "url": "https://www.yicai.com/news/103112374.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "广发证券：坚持稳中求进，以高质量发展服务国家战略", "url": "https://www.yicai.com/news/103111882.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "万亿REITs市场助力存量国有资产盘活 陆家嘴金融沙龙2026年第七期圆满收官", "url": "https://www.yicai.com/news/103111512.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "中国平安郭晓涛回应低利率时代保险应对之策：关注投资收益率与负债成本差值", "url": "https://www.yicai.com/news/103110986.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "奋楫新征程 实干显担当——华夏银行2025年度报告发布", "url": "https://www.yicai.com/news/103110945.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "消费贷风险拐点何时出现？邮储管理层：风险防控压力依然较大，但势头良好", "url": "https://www.yicai.com/news/103110416.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "央行逆回购操作加量护盘，跨季之后资金面如何走", "url": "https://www.yicai.com/news/103110366.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "邮储银行芦苇：推进资本管理高级法落地是今年重点", "url": "https://www.yicai.com/news/103110206.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "不止于贷款，兴业银行董事长详解产业金融：服务整个生态", "url": "https://www.yicai.com/news/103109902.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "适配L2-L4全级别，北京率先启动智驾车险开发应用", "url": "https://www.yicai.com/news/103109885.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "长期资本入市堵点如何疏通？博鳌论坛开出这些药方", "url": "https://www.yicai.com/news/103109092.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "最高6.6%最低4.04% 不一致的披露口径难掩险企高下立现的投资水平", "url": "https://www.yicai.com/news/103109173.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "银行火拼消费贷经营贷 工行邮储兴业信用卡业务降幅超10%", "url": "https://www.yicai.com/news/103109149.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "科创链接中国东盟，人民币成区域贸易投资重要选择", "url": "https://www.yicai.com/news/103109041.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
    {"title": "净息差拐点来了？工行建行这样预测", "url": "https://www.yicai.com/news/103108544.html", "source": "第一财经-金融频道", "listed_from": "https://www.yicai.com/news/jinrong/"},
]

all_new = bank_items + home_items + yicai_items
data['items'].extend(all_new)
data['count'] = len(data['items'])
data['pending_llm_files'] = []

with open('data/candidates_all.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

for fn in ['data/raw_eastmoney-bank.md', 'data/raw_eastmoney-home.md', 'data/raw_yicai-finance.md']:
    if os.path.exists(fn):
        os.remove(fn)
