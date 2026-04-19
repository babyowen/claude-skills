# Final Notes

`bank-news-collector` 的最终设计原则如下：

## 核心目标
不是把前置候选筛到最纯，而是保证完整流程稳定跑通，并让最终写入 JSON 的内容尽量准确。

## 最终工作流
1. 使用 `agent-browser` 访问指定列表页（尤其是银行频道列表页、财联社深度页）
2. 抓取可见标题与链接
3. 标题阶段做宽松初筛：只要“可能与银行经营相关、值得进一步读正文确认”即可进入候选
4. 对候选项做去重
5. 对未重复候选阅读正文
6. 正文阶段做严格终筛：只有确实对银行经营有影响、风险提示或启发的内容才保留
7. 结果写入当天 JSON
8. 校验 JSON 结构

## 质量标准
- 前置候选不必极致精确
- 最终 JSON 要相对准确
- 宁可前面多看几篇，也不要漏掉真正重要的银行经营新闻

## 当前站点结论
- `https://bank.eastmoney.com/`：当前最稳，适合作为主力来源
- `https://www.cls.cn/depth?id=1032`：可作为补充深度来源
- 当前对财联社深度页优先使用已验证可用的 API：`/v3/depth/home/assembled/1032?app=CailianpressWeb&os=web&sv=8.4.6&sign=9f8797a1f4de66c2370f7a03990d2737`
- 从 `top_article` 和 `depth_list` 提取 `id` 与 `title`，正文按 `https://www.cls.cn/detail/{id}` 访问
- 如果该 API 后续失效，再回退到页面可见内容方案
- `https://www.jiemian.com/lists/9.html`：已验证可用静态主列表规则。优先从 `#load-list` 下的 `li.card-list` 抽取标题卡片，标题只认 `h3.card-list__title`，链接只认 `/article/数字.html`。同一 URL 在图片、标题、摘要三处重复出现时，只保留标题链接；短行情/纯报价碎片标题直接过滤。
- 已新增固化脚本 `scripts/jiemian_finance_extractor.py`，并通过统一入口 `scripts/collect_site_candidates.py --site-id jiemian-finance` 接入主采集链路。
- 同时提供批量入口 `scripts/collect_all_candidates.sh`，当前可一键产出财联社深度页与界面新闻金融频道候选文件。
- 界面新闻正文页可直接用 `web_fetch` 获取主要内容；若抽取结果仅剩摘要、内容异常过短或页面结构变化，再回退 `agent-browser`
- 正文页优先 `web_fetch`，失败时回退 `agent-browser`
