# Bank News Collector Skill

这是“银行家”专属的新闻筛选与沉淀 skill。

它的职责不是泛泛抓取财经新闻，而是：
- 访问 `sites.json` 中指定的网页
- 读取当前页面可见的标题与链接
- 先按“是否**可能**与银行经营相关”做标题宽松初筛
- 再对初筛后的候选新闻与当天 JSON 做去重
- 只有未重复的候选新闻才继续读取原文
- 只保留对银行经营确实有影响、有风险提示、或有经营启发的内容
- 将结果写入 skill 目录下 `data/YYYY-MM-DD.json`

## 设计原则

### 1. 运行时机不由 skill 负责
这个 skill **不负责定时任务**，也不内置调度逻辑。
何时运行、多久运行一次，由外部调度（例如 cron）决定。

### 2. 只访问指定网页
本 skill 只访问 `sites.json` 中显式列出的 URL：
- 不翻页
- 不站内扩展
- 不自行探索更多栏目或相关文章

### 3. 去重发生在“标题粗筛之后”
流程不是“先把页面所有标题都和 JSON 比一遍”。
正确流程是：
1. 读取当天 JSON 作为已收录参考
2. 访问指定页面，获取标题与链接
3. 先做标题粗筛
4. 再对粗筛通过的候选项去重
5. 只有未重复候选项才继续读原文

这样能避免一开始就做无意义的全量去重，也更符合实际工作流。

### 4. 标题阶段宽松，正文阶段严格
这个 skill 的判断重点放在正文阶段，而不是标题阶段。

- 标题阶段：只要新闻**可能**与银行经营相关，就可以进入候选
- 正文阶段：只有确认其**确实**对银行经营有影响、风险提示或启发，才保留

这样更能发挥 LLM 的语义判断能力，也能减少漏掉潜在重要新闻。

### 5. 流程稳定优先于前置过度精筛
这个 skill 的目标不是把候选标题提前筛到极致纯净，而是保证整条流程稳定跑通：
- 列表页能抓到候选
- 初筛不过度保守
- 去重正常
- 正文能读
- 正文终筛严格
- 最终 JSON 内容可靠

真正重要的是最终写入 `data/YYYY-MM-DD.json` 的结果质量。

### 5. 总结要站在银行经营视角
每条保留新闻都应有约 500 字总结，重点包括：
- 发生了什么
- 为什么对银行重要
- 会影响哪类经营指标或业务条线
- 有什么风险、机会或策略启发

## 文件结构

```text
bank-news-collector/
├── SKILL.md
├── README.md
├── sites.json
├── data/
│   └── YYYY-MM-DD.json
├── scripts/
│   ├── collect_site_candidates.py
│   ├── collect_all_candidates.sh
│   ├── jiemian_finance_extractor.py
│   ├── init_daily_json.py
│   ├── merge_news_json.py
│   └── validate_news_json.py
└── examples/
    └── site-config.example.json
```

## 关键文件说明

### `sites.json`
正式使用的网站配置清单。skill 运行时读取这个文件。

未来新增网站时，直接往这个文件追加条目即可。

建议不要只加 URL，还要尽量补齐这个站点自己的策略信息，例如：
- 页面提示（主新闻区在哪里）
- 噪声过滤（哪些区域不要）
- 列表页抓取方式
- 正文页抓取回退方式
- 等待策略与页面稳定条件
- 标题净化规则（只保留完整标题，不保留关键词拆分链接）
- 候选区块优先级（例如深度页优先于首页）

这样未来新增网站时，skill 可以继续沿用统一框架，但又不会因为所有网站共用同一套死规则而抓偏。

### `examples/site-config.example.json`
单条站点配置的模板示例。

它的作用是告诉你：
- 一条网站配置长什么样
- 字段怎么写
- 新站点如何按相同格式添加

它不是主清单，而是样板。

### `data/YYYY-MM-DD.json`
每天的采集结果文件。

文件内容是 JSON 数组，每一项代表一条已保留新闻。

## 建议字段

每条新闻建议包含：
- `title`
- `url`
- `summary`
- `published_at`
- `source`
- `why_relevant`
- `collected_at`（北京时间 / Asia/Shanghai）

## 推荐执行流程

1. 读取 `sites.json`
2. 逐个访问其中配置的网站 URL
3. 初始化当天 JSON 文件
4. 读取当前页面标题与链接
5. 标题宽松初筛
6. 对候选新闻去重
7. 阅读未重复候选的原文
8. 严格判断是否值得保留
9. 生成总结
10. 追加写入当天 JSON
11. 校验 JSON 结构

## 如何新增网站

直接参考 `examples/site-config.example.json`，往 `sites.json` 新增一项，例如：

```json
{
  "id": "new-site",
  "site_name": "某新网站",
  "url": "https://example.com/news",
  "allowed_domains": ["example.com"],
  "use_agent_browser": true,
  "expand_within_site": false,
  "pagination": false,
  "page_hint": "只读取当前页面可见标题与链接，不翻页，不延展。",
  "max_candidate_articles": 30,
  "output_dir": "data"
}
```

## 脚本职责

### `init_daily_json.py`
- 确保当天 JSON 文件存在
- 不存在则创建空数组
- 存在则原样保留

### `collect_site_candidates.py`
- 统一的站点候选采集入口
- 按 `site_id` 读取 `sites.json` 并调用对应站点逻辑
- 当前已接入：`cls-depth-1032`、`jiemian-finance`

示例：
```bash
python3 scripts/collect_site_candidates.py --site-id jiemian-finance --output data/jiemian-finance.candidates.json
```

### `collect_all_candidates.sh`
- 批量执行已接入脚本入口的站点候选采集
- 目前会同时产出财联社深度页、界面新闻金融频道两个候选文件

示例：
```bash
./scripts/collect_all_candidates.sh data/candidates
```

### `jiemian_finance_extractor.py`
- 界面新闻金融频道专用抽取脚本
- 固定使用 `#load-list > li.card-list` + `h3.card-list__title` 提取主列表标题
- 自动去掉同一文章在图片/标题/摘要处的重复链接，只保留标题链接

### `merge_news_json.py`
- 将本轮通过终筛的新闻合并进当天 JSON
- 自动按 `url` / `title` 去重
- 适合做稳定落盘

### `validate_news_json.py`
- 校验 JSON 文件结构是否正确
- 检查每条记录是否具备关键字段
- 防止后续积累出脏数据

## 维护建议

- 如果某个站点结构变化，优先改 `sites.json` 的提示语
- 对 `sites.json` 中已标记 `use_agent_browser: true` 的站点，默认优先使用 `agent-browser`
- 对银行频道列表页，直接以 `agent-browser` 作为主链路，不再依赖 `web_fetch` 抓列表
- 对财联社深度页，当前优先使用已验证可用的专用 API 获取 `top_article` 与 `depth_list`，再拼接 `https://www.cls.cn/detail/{id}` 访问正文；如果 API 失效，再回退到 `agent-browser`
- 对界面新闻金融频道，当前优先使用静态 HTML 主列表规则：锁定 `#load-list > li.card-list`，标题以 `h3.card-list__title` 为准，链接必须匹配 `/article/数字.html`；默认丢弃图片链接、摘要链接、导航和标签词。同一 article URL 在图片/标题/摘要中重复出现时，只保留标题链接那一条。
- 如果页面越来越动态、普通读取不稳定，也优先使用 `agent-browser`
- 对正文页，优先用 `web_fetch` 抽正文；如果失败、抓偏、内容异常或过短，就回退到 `agent-browser`
- 如果未来需要更细的站点提取规则，再扩展配置字段，而不是把逻辑写死在正文里

## 注意

这个 skill 的核心价值不在“多抓”，而在“筛得准、留得住、对银行经营真有用”。
宁可少，也不要把弱相关内容塞进 JSON。
，也不要把弱相关内容塞进 JSON。
� JSON。
