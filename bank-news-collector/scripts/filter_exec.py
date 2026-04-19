import json, re
from datetime import datetime
exec(open("/Users/babyowen/.claude/skills/bank-news-collector/scripts/run_filter_r1.py").read())
NAE = set()
for w in ["银行","理财","基金","保险","信托","债券","期货","外汇","黄金","股市","证券","财经","金融","信贷","广告","推广","更多","全部","热搜","推荐","最新","热点"]:
    NAE.add(w)
NAP = ["^资金流向","^Shibor","^shibor","^什么是","^如何理财","^怎样理财","^理财入门","^稳健理财","^爆款理财","^精选理财","^限时.*理财","^推荐.*理财","^品牌推广","^赞助"]
def is_article(t):
    t = t.strip()
    if len(t) <= 3: return False
    if t in NAE: return False
    for p in NAP:
        if re.match(p, t): return False
    return True
SK = ["银行","央行","人民银行","中央银行","商业银行","银保监","金融监管总局","存款","贷款","房贷","车贷","信用卡","消费贷","经营贷","存贷款","信贷投放","社融","净息差","息差","利差","NPL","不良贷款","不良率","不良资产","拨备","资本充足率","同业","银团","票据","贴现","信用证","保函","托管","代销","农商行","城商行","股份制银行","国有大行","六大行","上市银行","银行股","银行年报","银行一季报","银行半年报","工商银行","建设银行","农业银行","中国银行","交通银行","邮储银行","招商银行","浦发银行","中信银行","光大银行","华夏银行","民生银行","兴业银行","广发银行","平安银行","浙商银行","渤海银行","恒丰银行","汇丰","渣打","花旗","东亚银行","农银理财","工银理财","建信理财","中银理财","交银理财","招银理财","兴银理财","信银理财","光大理财","浦银理财","民生理财","华夏理财","渤银理财","理财子","理财公司","降准","降息","加息","逆回购","MLF","公开市场操作","金融监管","监管政策","监管新规","资管新规","数字人民币","数字货币","私人银行","银行理财","理财规模","理财月报","消费金融","金融科技","AMC","资产管理公司","信达","东方资产","长城资产","反向讨薪","储蓄国债","科技金融","LPR","信贷","放贷","财富管理"]
ER = ["伊朗议长","伊朗媒体披露","伊朗.*善意.*不信任","以驻美大使","英国.*召集.*通航.*霍尔木兹","霍尔木兹航运追踪","中央气象台","特朗普称霍尔木兹","美军.*继续增兵","以.*黎.*真主党.*停火","强对流天气","^企业级.*养虾","^OpenClaw","美伊停火前.*神秘资金","白宫.*警告工作人员.*内幕","中东战火.*引爆.*通胀","美伊冲突.*大类资产.*众生相","^英伟达","^NVIDIA","^大空头.*伯里"]
PS = ["^纳指.*连[涨跌]","^标普.*连[涨跌]","^道指.*连[涨跌]","^美油.*创","^两市.*成交"]
def is_bank(title):
    for p in ER:
        if re.search(p, title): return False
    for p in PS:
        if re.search(p, title): return False
    for kw in ["伊朗议长","伊朗媒体披露","美军继续增兵中东","中央气象台"]:
        if kw in title: return False
    if re.match(r"^(周六|周日|周五|周四|周三|周二|周一|今日|明日)你需要知道的隔夜全球要闻", title):
        bkw = ["银行","金融","降息","利率","债","理财","信贷","央行","贷款","存款","美联储","资管","AMC","稳定币"]
        return any(k in title for k in bkw)
    for kw in SK:
        if kw in title: return True
    if "稳定币" in title and any(c in title for c in ["银行","金融","牌照","汇丰","渣打","监管","发钞"]): return True
    if "利率" in title and any(c in title for c in ["房贷","存款","贷款","信贷","央行","银行","储蓄","LPR","消费贷","分红险"]): return True
    if "债" in title and any(c in title for c in ["银行","国债","地方债","信用债","金融债","同业存单","债市","债券","发行","美元债","点心债","境外债","中资","民企","房企","不良","评级","公告","收盘","早参"]): return True
    if "监管" in title and any(c in title for c in ["金融","银行","保险","证券","资管","信托","农商","严禁","征求"]): return True
    if "保险" in title and any(c in title for c in ["银行","银保","分红险","销售","利率","监管","金融","演示利率"]): return True
    if any(k in title for k in ["年报","一季报","半年报","三季报","业绩"]) and any(c in title for c in ["银行","券商","保险","金融","理财","AMC","资管","上市"]): return True
    if "美联储" in title and any(c in title for c in ["降息","利率","加息","货币政策","缩表","QE"]): return True
    if "理财" in title: return True
    if "资管" in title: return True
    if ("CPI" in title or "PPI" in title) and ("国家统计局" in title or "同比" in title): return True
    if "金融" in title and any(c in title for c in ["监管","政策","改革","开放","科技","融资","租赁","沙龙","服务","平安","结构","体系","安全","稳定"]): return True
    if "融资租赁" in title: return True
    if "金融沙龙" in title: return True
    if "中资" in title and "债" in title: return True
    if "跨境支付" in title or "Swift" in title or "swift" in title: return True
    if "银行间" in title: return True
    if "储蓄国债" in title or ("国债" in title and "发售" in title): return True
    if "券商" in title and ("资管" in title or "规模" in title or "业绩" in title): return True
    if ("出险房企" in title or "扭亏为盈" in title) and ("债" in title or "金融" in title or "监管" in title): return True
    if "平安" in title and re.search(r"(金融|保险|银行|理财|AI.*服务|服务年|专业)", title): return True
    if "资金面" in title and "债市" in title: return True
    return False
def main():
    passed = []
    seen = set()
    for item in items:
        title = item.get("title", "").strip()
        url = item.get("url", "").strip()
        if url in seen: continue
        if not is_article(title): continue
        if not is_bank(title): continue
        seen.add(url)
        passed.append({"title": title, "url": item.get("url",""), "source": item.get("source",""), "listed_from": item.get("listed_from","")})
    out = {"filter_round": "first", "timestamp": datetime.now().isoformat(), "total_input": len(items), "total_passed": len(passed), "items": passed}
    with open(OUTPUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print("Total input:", len(items))
    print("Total passed:", len(passed))
    rate = len(passed) * 100 // len(items)
    print("Filter rate:", str(rate) + "%")
    for i, item in enumerate(passed, 1):
        t = item["title"]
        print("  " + str(i) + ". " + t[:80])
    print("--- EXCLUDED ---")
    seen_all = set()
    excl = []
    for item in items:
        u = item.get("url", "").strip()
        ti = item.get("title", "").strip()
        if u in seen_all: continue
        seen_all.add(u)
        if is_article(ti) and not is_bank(ti): excl.append(ti)
    for i, t in enumerate(excl, 1):
        print("  " + str(i) + ". " + t[:80])
main()
