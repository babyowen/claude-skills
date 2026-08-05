---
name: news-count-report
description: >
  新闻词频统计日报：从 news.liuliang.world API 取固定关键词昨日/前日新闻数量，
  对比趋势，生成飞书交互式卡片发群。专为定时任务，无人值守。
  触发：新闻统计日报、词频报告、word-count report、news count report。
---

# 新闻词频统计日报

对比**昨日 vs 前日**固定关键词新闻数量，生成飞书交互式卡片发到固定群。

## 执行方式

```bash
python3 scripts/report.py
```

| 参数 | 默认 | 说明 |
|------|------|------|
| `--chat-id` | `oc_578717a43c0e5011765d9cada71d8218` | 飞书群 |
| `--dry-run` | false | 只打印不发 |
| `--api-url` | `http://news.liuliang.world/api/word-count-stats` | API |
| `--date` | 今天 | 覆盖基准日；基准-1=昨日，-2=前日 |

```bash
python3 scripts/report.py --dry-run --date 2026-03-31   # 指定基准日测试
```

## 报告内容（飞书 interactive 卡片）

1. **汇总行**：昨日总条数 + 高分条数，附 vs 前日变化（`↑+N` / `↓-N` / `→0`）
2. **4 固定关键词**：养老 / 公积金 / 政府基金 / 中国烟草，各列条数、高分数、变化
3. **江苏省国资委明细**：官网(customGrab) / 官微(wechat) 分布 + 前日对比

关键词在 `scripts/report.py` 的 `DISPLAY_KEYWORDS` 硬编码。**非 Markdown 表格，无合计行**。

## 日期换算

API 记录带 `fetchdate`(UTC)，脚本按其精确匹配过滤。北京零点 − 8h = fetchdate（北京 3/31 → `2026-03-30T16:00:00.000Z`）。

## 失败模式与处置

| 触发 | 脚本行为 | 处置 |
|---|---|---|
| API 超时(>30s)/不可达 | `exit(1)` 无重试 | 次日定时补跑；手动重试先确认 API |
| 昨日无数据（周末/节假日） | WARNING + 生成 0 值卡片发送 | 正常，无需干预 |
| `lark-cli` 未找到 | `exit(1)` | 先 `lark-cli auth login` |
| 飞书发送失败 | `exit(1)` 无落盘 | `--dry-run` 验证后重试 |

## 反例（不要做）

- ❌ 改 `DISPLAY_KEYWORDS` 换关键词（需业务确认）
- ❌ 绕过 `--dry-run` 对未知日期直接正式发送
- ❌ 编造 API 未返回的数据；把卡片当 Markdown 表格输出（飞书不支持，已用卡片）
