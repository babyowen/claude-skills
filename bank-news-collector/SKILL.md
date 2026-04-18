---
name: bank-news-collector
description: 自动采集与银行经营高度相关的财经新闻，按日期归档并生成统计报告。当用户提到银行新闻、同业动态、监管变化、批量筛选新闻时触发。支持定时任务自动运行。Trigger: bank news, collect banking news, 银行新闻采集, 同业动态, 监管政策, 财经新闻筛选.
---

# Bank News Collector Skill

为"银行家"采集、筛选与**银行经营高度相关**的新闻，沉淀到 `data/YYYY-MM-DD.json`。

## 执行流程

**重要：步骤1-7和步骤9必须静默执行，不输出任何内容。只有步骤8输出。**

```
步骤1：初始化当天文件（静默）
   └─ python3 scripts/init_daily_json.py > /dev/null 2>&1

步骤2a：并发抓取所有站点（静默）
   └─ python3 scripts/fetch_all_candidates.py > /dev/null 2>&1
       ├─ 有专用脚本的站点（财联社、界面新闻）→ 脚本直接提取标题+链接
       ├─ 无专用脚本的站点（东方财富、第一财经）→ jina-reader 抓原始 markdown 保存到 data/raw_{site_id}.md
       └─ 输出 data/candidates_all.json（仅含脚本站点结果）+ pending_llm_files 列表

步骤2b：LLM 从原始 markdown 中提取新闻（静默）
   ├─ 读取 candidates_all.json 中的 pending_llm_files
   ├─ 逐个读取 data/raw_{site_id}.md
   ├─ 用自身判断力从 markdown 中识别真正的新闻标题和链接
   │  ├─ 必须是新闻文章（有明确标题、指向具体文章详情页）
   │  ├─ 排除：导航链接、广告、下载入口、图片、标签词、频道入口、页脚
   │  └─ 参考 sites.json 中对应站点的 candidate_zones 和 noise_filters
   ├─ 输出格式与脚本站点一致：{"title": "...", "url": "...", "source": "...", "listed_from": "..."}
   ├─ 将提取结果追加到 candidates_all.json 的 items 数组
   └─ 删除 data/raw_*.md 临时文件

步骤3：第一轮筛选 - Agent 判断标题相关性（静默）
   ├─ 读取 candidates_all.json 中的所有候选新闻
   ├─ 用 Agent 自身 LLM 判断每条候选：
   │  ├─ ① 是否"新闻文章"？
   │  │  ├─ 必须是具体的事件报道、政策解读、行业分析、机构动态
   │  │  ├─ 排除以下类型（无论标题是否含银行关键词）：
   │  │  │  ├─ 栏目/频道入口（如"银行"、"理财"、"基金"等纯分类名）
   │  │  │  ├─ 数据/行情页面（如"银行间同业拆借利率"、"资金流向"）
   │  │  │  ├─ 搜索/聚合页面（如"银行理财子公司"搜索结果）
   │  │  │  ├─ 教学/科普内容（如"什么是LPR"、"如何理财"）
   │  │  │  ├─ 产品推广/广告（如"稳健理财"、"**理财**"）
   │  │  │  └─ 专题/合集入口（无具体新闻事件）
   │  │  └─ 判断方法：标题是否描述了一个具体的、有时效性的事件或变化
   │  └─ ② 如果是新闻，是否与银行经营相关？
   │     ├─ "银行经营相关"包括：银行业务、监管政策、利率变化、信贷、风控、
   │     │  资本管理、金融科技、同业动态、银行财报、央行政策、存款/贷款等
   │     └─ 只要"可能"相关就保留（宽进）
   ├─ 保存通过筛选的结果到 data/first_round_filtered.json
   └─ 格式与候选一致：{"title", "url", "source", "listed_from"}

步骤4：与 process.json 去重，保留增量（静默）
   └─ python3 scripts/dedup_process.py > /dev/null 2>&1
       ├─ 读取 data/first_round_filtered.json
       ├─ 与 data/{today}-process.json 去重
       ├─ 输出 data/incremental_candidates.json
       └─ 更新 process.json（追加本轮筛选过的URL）

步骤5：读取增量新闻原文（静默）
   ├─ 读取 data/incremental_candidates.json
   └─ 逐条用 jina-reader 读取新闻正文
       ├─ 第一财经特殊处理：直接 curl 抓 HTML，提取 <div id="multi-text">
       └─ 其他站点：curl -s "https://r.jina.ai/{url}" --max-time 30

步骤6：第二轮筛选 - 严筛 + 生成总结（静默）
   ├─ 逐条判断：
   │  ├─ 日期校验：从正文中提取 published_at（详见「日期识别速查」）
   │  │  └─ 规则：日期=今天 → 继续；日期≠今天 → 剔除；找不到 → 剔除
   │  └─ 相关性校验：是否与银行经营高度相关？（严出：有影响、风险提示或启发）
   ├─ 为通过的新闻生成约500字总结（银行经营视角：影响、风险、启发）
   ├─ 添加 why_relevant 字段
   └─ 保存到 data/second_round_filtered.json

步骤6.5：归档中间文件（静默）
   └─ python3 scripts/archive_pipeline.py > /dev/null 2>&1
       ├─ 将 candidates_all.json 复制为 data/{date}-candidates.json
       ├─ 将 first_round_filtered.json 复制为 data/{date}-first_round.json
       ├─ 将 incremental_candidates.json 复制为 data/{date}-incremental.json
       └─ 将 second_round_filtered.json 复制为 data/{date}-second_round.json

步骤7：去重后写入当天JSON（静默）
   └─ python3 scripts/merge_news_json.py data/{today}.json data/second_round_filtered.json > /dev/null 2>&1
       ├─ 日期门禁：published_at 日期必须匹配今天
       ├─ URL 去重：与当天JSON已有条目比对
       └─ 生成 data/{today}-new-urls.json（供步骤8统计）

步骤8：输出统计表格和入选标题（唯一输出）
   └─ python3 scripts/generate_report.py
       ├─ 读取 data/first_round_filtered.json 统计初筛
       ├─ 读取 data/{today}-new-urls.json 统计二轮新增
       └─ 按 assets/output_template.md 模板输出

步骤9：通过飞书发送报告（静默，必须执行）
   ├─ ⚠️ 无论结果如何都必须执行此步骤，即使0条新闻入选也必须发送通知
   ├─ 将步骤8的输出内容通过 lark-im skill 发送给自己
   ├─ 使用 bot 身份，发送到当前用户的 open_id
   │  └─ lark-cli im +messages-send --as bot --user-id ou_e9bf22aaaeae8652f04b87ec28fb6bd9 --text "内容"
   ├─ 消息格式要求：
   │  ├─ 必须使用 --text（纯文本），不能用 --markdown（飞书不支持 markdown 表格）
   │  ├─ 表格改为"站点: 初筛 X | 二轮 Y"的列表格式
   │  ├─ 末尾附上今日已收录的所有新闻标题序号列表
   │  └─ 0条入选时，标题列表显示"今日无入选新闻"
   └─ 不在控制台输出任何内容
```

## 执行要求

**绝对静默执行：**
- 步骤1-7、步骤9的所有操作必须静默，不输出任何中间结果
- 所有Python脚本调用必须重定向：`python3 script.py > /dev/null 2>&1`
- 步骤3和步骤6中Agent使用LLM判断时，不输出思考过程，直接操作文件
- 只有步骤8（最终统计）才输出内容

**步骤9必须执行：**
- 步骤9（飞书通知）是强制步骤，无论采集结果如何都必须执行
- 即使0条新闻入选、即使所有站点都返回空，也必须发送飞书通知
- 跳过步骤9是严重错误，等同于任务未完成

**最终输出格式：**
- 严格按照 `assets/output_template.md` 模板输出
- 不得添加任何表格外的文字、空行、说明

**输出统计说明：**
- **初筛入选**：本次运行第一轮LLM筛选后保留的数量
- **二轮入选**：本次运行最终追加到JSON文件的数量
- 保证：初筛入选 >= 二轮入选

## 三条硬约束（必须遵守）

### 1. 今天新闻硬约束
- 当天 JSON 文件**只允许收录发布日期为当天**的新闻
- `published_at` 日期部分必须与文件名日期一致
- 拿不到 `published_at` 或日期不一致，**一律不得写入**
- 日期识别由 LLM 在步骤6从正文中提取（见步骤6的日期识别规则）

### 2. 宽进严出（两轮筛选）
- **第一轮（标题）**：只要**可能**与银行经营相关，就进入候选
- **第二轮（正文）**：只有**确实**对银行经营有影响、风险提示或启发的才保留

### 3. 先筛后重（去重时机）
- **错误流程**：抓取所有标题 → 与JSON全量比对 → 读原文
- **正确流程**：抓取标题 → LLM粗筛 → 与process.json去重 → 只读增量原文

## 异常处理与回退

### 站点全失败
- 若所有站点返回空或全部抓取失败：
  - 步骤8正常输出（所有站点计数为0）
  - 步骤9仍必须发送飞书通知，内容为"今日无入选新闻"
  - 不报错、不中断流程

### 飞书发送失败
- 若 lark-cli 不可用或发送失败：
  - 将通知内容追加写入 `data/{today}-notification-fallback.txt`
  - 控制台静默，不输出错误信息
  - 下次运行成功时不再补发

### 日期格式异常
- 步骤6中提取日期失败时，直接剔除该条目
- 不猜测、不补默认值

### 网络请求失败
- jina-reader 超时（> 30s）或返回空：
  - 标记该条目为待重试，进入重试队列
  - 最多重试2次，间隔5秒
  - 仍失败则跳过，不阻断流程
- curl 返回非200：记录站点错误日志，跳过该站点

### 文件损坏或缺失
- `process.json` 不存在或解析失败：
  - 自动创建空文件 `[]`
  - 视为首次运行，不报错
- `data/{today}.json` 不存在：
  - 步骤1自动初始化

## 速查表：日期识别规则

步骤6中 LLM 从正文提取 `published_at` 的判定标准：

| 维度 | 规则 |
|------|------|
| **查找位置** | 标题与正文之间、作者署名行附近、正文开头第一段、文末附近 |
| **绝对日期** | `03-29`、`2026/03/29`、`2026年3月29日` |
| **相对日期** | `昨天`、`2小时前`、`刚刚`（结合当前时间推断） |
| **混合格式** | `第一财经 _03-27 23:50_` |
| **判定逻辑** | 日期明确=今天 → 继续；日期明确≠今天 → 剔除；找不到 → 剔除 |
| **输出格式** | 填入 `published_at` 字段，ISO 8601 格式带时区 |

## 数据格式

每条新闻必须包含：
```json
{
  "title": "新闻标题",
  "url": "https://...",
  "summary": "约500字总结，站在银行经营视角提炼影响、风险、启发",
  "published_at": "2026-03-27T09:30:00+08:00",
  "source": "站点名或栏目名",
  "why_relevant": "一句话说明为什么与银行经营高度相关",
  "collected_at": "2026-03-27T20:30:00+08:00"
}
```

**注意：最终JSON只保留500字总结，不保留完整原文。**

## 运行边界

- 只访问 `sites.json` 中显式指定的网页
- **不翻页**、**不站内延展**、**不自行探索更多栏目**
- 运行时机由外部调度决定，skill 不负责定时任务

## 网页读取策略

### 列表页（提取标题+链接）
| 站点类型 | 方式 |
|---------|------|
| 有专用脚本 | `collect_site_candidates.py --site-id xxx` |
| 无脚本 | `jina-reader` + Agent LLM 提取标题链接 |

### 正文页（读取全文）

**通用优先级**：jina-reader → web_fetch → agent-browser

**第一财经特殊处理**：**直接抓HTML** → jina-reader → web_fetch → agent-browser

```bash
# 第一财经正文提取（首选）
curl -s "URL" \
  | tr -d '\n' \
  | grep -o '<div id="multi-text"[^>]*>.*</div>' \
  | sed 's/<[^>]*>//g' \
  | sed 's/&ldquo;/"/g' \
  | sed 's/&rdquo;/"/g' \
  | sed 's/&nbsp;/ /g' \
  | sed 's/&lt;/</g' \
  | sed 's/&gt;/>/g' \
  | sed 's/&quot;/"/g' \
  | sed 's/&amp;/\&/g'

# 通用jina-reader（次选）
curl -s "https://r.jina.ai/https://目标URL" --max-time 30
```

**为什么第一财经要特殊处理？**
- jina-reader访问第一财经时会遇到"AI速读"付费墙，正文被挡住
- 直接抓取HTML，正文在`<div id="multi-text">`，反而能获取完整内容

## 站点策略

每个站点的具体提取规则写在 `sites.json` 的 `page_hint` 字段中，包括：
- 主新闻区域位置
- 噪声过滤规则
- CSS选择器（如界面新闻的 `#load-list > li.card-list`）
- 回退策略

**当前已接入站点：**
- 财联社首页/深度页：API直出
- 界面新闻金融频道：BeautifulSoup精确提取 `#load-list > li.card-list` + `h3.card-list__title`
- 东方财富-银行频道：jina-reader + Agent LLM提取
- 第一财经-金融频道：jina-reader + Agent LLM提取列表；**正文需直接抓HTML**（避开AI速读付费墙）

## 去重逻辑

- 默认按 `url` 去重
- URL不稳定时补充按 `title` 去重
- **步骤4去重**：与 process.json 对比，保留增量
- **步骤7去重**：与 YYYY-MM-DD.json 对比，保留增量

## 输出要求（绝对约束）

**完成后只输出表格和标题列表，不要输出任何其他内容。**

**最终输出格式：**

```
| 站点 | 初筛入选 | 二轮入选 |
|------|----------|----------|
| 财联社-首页 | 15 | 2 |
| 财联社-深度-1032 | 8 | 1 |
| 界面新闻-金融频道 | 5 | 0 |
| 东方财富-首页 | 0 | 0 |
| 东方财富-银行频道 | 3 | 0 |
| 第一财经-金融频道 | 10 | 1 |

**今日已收录新闻：**
1. [标题1]
2. [标题2]
3. [标题3]
```

**硬性要求：**
- 每个站点占一行，按 sites.json 顺序排列
- 表格后列出今日已收录的所有新闻标题（序号列表）
- 不要输出表格和标题列表以外的任何内容

## 输出禁令（绝对禁止）

完成技能后，**绝对禁止输出以下任何内容**：

- ❌ **开场白**："采集完成"、"运行结束"、"本次运行结果"、"以下是统计表格"等
- ❌ **统计说明**："共抓取X个站点"、"筛选Y条新闻"、"新增Z条"等
- ❌ **额外章节**："说明"、"注意"、"提示"、"总结"、"建议"、"参考"等
- ❌ **延伸服务**："是否需要我..."、"接下来可以..."、"如需..."等
- ❌ **表格装饰**：表格前后的空行、分隔线、markdown代码块标记（如 ```）
- ❌ **中间过程**：任何步骤1-7的进度信息、调试信息、错误提示
- ❌ **时间信息**："耗时X秒"、"于XX时间运行"等

**唯一允许的输出**：
严格按照 `assets/output_template.md` 模板输出统计表格和标题列表，除此之外一个字符都不能多。

## 定时任务模式

此技能专为定时任务设计，支持完全自动化的无人值守运行：

### 自动化特性
- **无用户交互**：不需要任何手动输入或确认
- **完全静默**：步骤1-7 不输出任何内容
- **幂等性**：多次运行同一天不会重复添加新闻
- **自动清理**：自动清理临时文件

### 适用场景
- 定时任务每日自动采集
- 间隔监控（如每4小时、每8小时）
- 后台自动运行，无需人工干预

## 脚本说明

### 核心脚本（被执行）

| 脚本 | 用途 | 对应步骤 |
|------|------|----------|
| `init_daily_json.py` | 确保当天JSON存在 | 步骤1 |
| `fetch_all_candidates.py` | 并发抓取所有站点候选 | 步骤2a |
| `step2b_extract.py` | LLM从raw markdown提取新闻 | 步骤2b |
| `step2b_run.py` | 步骤2b运行入口 | 步骤2b |
| `step5_fetch.py` | 逐条读取增量新闻正文 | 步骤5 |
| `dedup_process.py` | 与process.json去重，保留增量 | 步骤4 |
| `archive_pipeline.py` | 归档中间文件为日期副本 | 步骤6.5 |
| `merge_news_json.py` | 合并新闻进JSON，含日期门禁 | 步骤7 |
| `generate_report.py` | 按模板生成最终报告 | 步骤8 |
| `send_feishu.py` | 飞书通知发送 | 步骤9 |
| `send_feishu_notification.py` | 飞书通知备用入口 | 步骤9 |
| `collect_site_candidates.py` | 统一采集入口（脚本站点） | 步骤2a |
| `jiemian_finance_extractor.py` | 界面新闻专用提取器 | 步骤2a |

### 辅助脚本（按需手动使用）

| 脚本 | 用途 |
|------|------|
| `append_llm_candidates.py` | 追加LLM提取的候选 |
| `merge_rounds.py` | 合并多轮筛选结果 |
| `fix_json.py` | JSON结构修复 |
| `fix_first_round.py` | 第一轮筛选结果修复 |
| `debug_json.py` | JSON调试工具 |
| `compute_stats.py` | 统计计算 |
| `validate_news_json.py` | 校验JSON结构 |
| `validate_output.py` | 验证输出格式 |
| `check_lark.py` | 检查飞书CLI配置 |
| `check_keychain.py` | 检查密钥存储 |

> **注意**：`scripts/` 目录下以 `_` 开头的脚本为开发/调试用的临时脚本，不应在正式流程中引用。
> `filter_round1.py` 位于项目根目录，不在 `scripts/` 目录中。

## 中间文件说明

| 文件 | 生命周期 | 说明 |
|------|----------|------|
| `data/candidates_all.json` | 步骤2 → 步骤3 | 所有候选新闻 |
| `data/first_round_filtered.json` | 步骤3 → 步骤4 | 第一轮筛选结果 |
| `data/incremental_candidates.json` | 步骤4 → 步骤5 | 去重后的增量候选 |
| `data/second_round_filtered.json` | 步骤6 → 步骤7 | 第二轮筛选结果（含总结） |
| `data/raw_*.md` | 步骤2a → 步骤2b | jina-reader原始页面（临时） |
| `data/{date}-candidates.json` | 步骤6.5归档 | 候选新闻日期快照 |
| `data/{date}-first_round.json` | 步骤6.5归档 | 初筛结果日期快照 |
| `data/{date}-incremental.json` | 步骤6.5归档 | 增量候选日期快照 |
| `data/{date}-second_round.json` | 步骤6.5归档 | 二轮筛选日期快照 |
| `data/{today}-new-urls.json` | 步骤7 → 步骤8 | 本次新增URL列表 |
| `data/{today}-process.json` | 持久 | 已处理URL记录 |
| `data/{today}.json` | 持久 | 当天最终新闻 |
