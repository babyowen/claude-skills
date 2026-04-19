---
name: news-count-report
description: >
  新闻词频统计日报：从 news.liuliang.world API 获取各关键词今日/昨日的新闻数量，
  对比变化趋势，生成 Markdown 对比报告并发送到飞书群。专为定时任务设计，支持无人值守运行。
  当用户提到新闻统计日报、词频报告、word-count report、news count report、新闻抓取统计时使用。
---

# 新闻词频统计日报

## 执行方式

直接运行 Python 脚本完成所有工作（抓取数据、对比分析、生成报告、发送飞书）：

```bash
python3 scripts/report.py
```

### 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--chat-id` | `oc_578717a43c0e5011765d9cada71d8218` | 飞书群 chat_id |
| `--dry-run` | false | 只打印报告不发送飞书 |
| `--api-url` | `http://news.liuliang.world/api/word-count-stats` | API 地址 |
| `--date` | 今天 | 覆盖"今天"日期 (YYYY-MM-DD)，用于测试 |

### 示例

```bash
# 正常运行（发送到默认飞书群）
python3 scripts/report.py

# 只看报告不发送
python3 scripts/report.py --dry-run

# 指定日期测试
python3 scripts/report.py --dry-run --date 2026-03-31
```

## 报告内容

报告为 Markdown 格式，包含：

1. **对比表格**：每个关键词的新闻总量和高分新闻数量，今日 vs 昨日
2. **江苏省国资委明细**：官网 (customGrab) 和官微 (wechat) 的来源分布
3. **合计行**：所有关键词的总计数据

## 数据源

- API: `http://news.liuliang.world/api/word-count-stats`
- 返回所有关键词×日期的统计数据（newsCount, highScoreCount, customGrabCount, wechatCount 等）

## 日期处理

API 的 fetchdate 使用 UTC 时间，对应北京时间凌晨零点减 8 小时：
- 北京时间 3月31日 = fetchdate `2026-03-30T16:00:00.000Z`
